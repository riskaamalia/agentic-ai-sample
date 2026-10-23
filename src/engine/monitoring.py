"""Pagu/realisasi monitoring engine and single-scenario comparison.

This is not the DBH allocation formula. It only compares budget and
realization figures copied from SIKD, records every calculation step, and
packages the result as evidence that a human (or later an LLM explainer)
can review. Values stay in Rp juta as stored in the fixture.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

ENGINE_VERSION = "monitoring-v1"
RULESET_VERSION = "signals-v1"
UNIT = "IDR_MILLION"
AVAILABLE = "AVAILABLE"
ROUNDED_DISPLAY = "ROUNDED_DISPLAY"
HUNDRED = Decimal("100")


@dataclass(frozen=True)
class Observation:
    observation_id: str
    fiscal_year: int
    region_name: str
    region_level: str
    budget: Decimal | None
    realization: Decimal | None
    value_status: str
    precision_status: str
    snapshot_date: str
    source_url: str

    @classmethod
    def from_record(cls, record: dict) -> Observation:
        def to_decimal(value: object) -> Decimal | None:
            # pandas turns JSON null into NaN; both mean "not available", never zero.
            if value is None or (isinstance(value, float) and value != value):
                return None
            # str() keeps the fixture's written digits instead of binary float noise.
            return Decimal(str(value))

        return cls(
            observation_id=record["observation_id"],
            fiscal_year=int(record["fiscal_year"]),
            region_name=record["region_name"],
            region_level=record["region_level"],
            budget=to_decimal(record.get("budget_million_idr")),
            realization=to_decimal(record.get("realization_million_idr")),
            value_status=record["value_status"],
            precision_status=record["precision_status"],
            snapshot_date=record["snapshot_date"],
            source_url=record["source_url"],
        )


@dataclass(frozen=True)
class ScenarioOverride:
    """User assumption applied on top of an observation; never overwrites it."""

    scenario_id: str
    label: str
    assumption_note: str
    budget: Decimal | None = None
    realization: Decimal | None = None
    created_by: str = "demo_user"

    def __post_init__(self) -> None:
        if not self.assumption_note.strip():
            raise ValueError("Skenario wajib memiliki catatan asumsi.")
        if self.budget is None and self.realization is None:
            raise ValueError("Skenario harus mengubah minimal satu parameter.")
        for name, value in (("pagu", self.budget), ("realisasi", self.realization)):
            if value is not None and value < 0:
                raise ValueError(f"Nilai {name} negatif tidak diterima pada input sederhana.")


@dataclass
class MonitoringResult:
    observation_id: str
    budget: Decimal | None
    realization: Decimal | None
    ratio_pct: Decimal | None
    gap: Decimal | None
    computable: bool
    trace: list[dict] = field(default_factory=list)
    signals: list[dict] = field(default_factory=list)


@dataclass
class ScenarioComparison:
    observation: Observation
    override: ScenarioOverride
    baseline: MonitoringResult
    scenario: MonitoringResult
    changed_parameters: list[dict]
    deltas: dict[str, Decimal | None]


def evaluate(
    observation: Observation,
    budget: Decimal | None = None,
    realization: Decimal | None = None,
) -> MonitoringResult:
    """Compute ratio/gap and rule signals; explicit values replace observed ones."""
    budget = observation.budget if budget is None else budget
    realization = observation.realization if realization is None else realization
    result = MonitoringResult(
        observation_id=observation.observation_id,
        budget=budget,
        realization=realization,
        ratio_pct=None,
        gap=None,
        computable=False,
    )

    if budget is None or realization is None or observation.value_status != AVAILABLE:
        # Missing or unverified data is never turned into zero, and no
        # monitoring alert is raised on it.
        result.signals.append(
            _signal(
                "DQ-001",
                "DATA_INCOMPLETE",
                "Pagu/realisasi tidak tersedia atau belum terverifikasi; kesimpulan numerik ditahan.",
                observation,
                value_status=observation.value_status,
            )
        )
        return result

    result.computable = True
    result.gap = budget - realization
    result.trace.append(
        _step("sisa_pagu", "B - R", {"B": budget, "R": realization}, result.gap)
    )
    if budget > 0:
        result.ratio_pct = realization / budget * HUNDRED
        result.trace.append(
            _step(
                "rasio_realisasi_pct",
                "R / B × 100",
                {"B": budget, "R": realization},
                result.ratio_pct,
            )
        )
    else:
        result.trace.append(
            _step("rasio_realisasi_pct", "R / B × 100", {"B": budget, "R": realization}, None,
                  note="B = 0: rasio tidak terdefinisi (N/A).")
        )

    if observation.precision_status == ROUNDED_DISPLAY:
        result.signals.append(
            _signal(
                "DQ-002",
                "PRECISION_LIMITED",
                "Sumber hanya menampilkan angka dibulatkan; hasil bukan nominal rupiah exact.",
                observation,
            )
        )
    if realization < budget:
        result.signals.append(
            _signal(
                "MON-001",
                "MONITOR_GAP",
                "Ada sisa pagu pada tanggal snapshot; bukan bukti keterlambatan atau masalah.",
                observation,
                gap=result.gap,
            )
        )
    elif realization > budget:
        result.signals.append(
            _signal(
                "MON-002",
                "REVIEW_OVER_BUDGET",
                "Realisasi melampaui pagu; periksa beda basis, perubahan pagu, atau koreksi data.",
                observation,
                gap=result.gap,
            )
        )
    return result


def run_scenario(observation: Observation, override: ScenarioOverride) -> ScenarioComparison:
    baseline = evaluate(observation)
    scenario = evaluate(observation, budget=override.budget, realization=override.realization)

    changed = []
    for name, base_value, new_value in (
        ("pagu", observation.budget, override.budget),
        ("realisasi", observation.realization, override.realization),
    ):
        if new_value is not None and new_value != base_value:
            changed.append({"parameter": name, "baseline": base_value, "scenario": new_value, "unit": UNIT})

    deltas = {
        "gap": _diff(scenario.gap, baseline.gap),
        "gap_pct": _pct_change(scenario.gap, baseline.gap),
        "ratio_pp": _diff(scenario.ratio_pct, baseline.ratio_pct),
    }
    return ScenarioComparison(observation, override, baseline, scenario, changed, deltas)


def build_evidence_packet(comparison: ScenarioComparison) -> dict:
    """JSON-safe bundle of everything an explainer may cite, and nothing more."""
    obs = comparison.observation
    body = {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": RULESET_VERSION,
        "calculation_type": "MONITORING_PAGU_REALISASI",
        "is_allocation_formula": False,
        "unit": UNIT,
        "presentation_rounding": "ROUND_HALF_UP, 2 desimal",
        "observation": {
            "observation_id": obs.observation_id,
            "fiscal_year": obs.fiscal_year,
            "region_name": obs.region_name,
            "region_level": obs.region_level,
            "value_status": obs.value_status,
            "precision_status": obs.precision_status,
            "snapshot_date": obs.snapshot_date,
            "source_url": obs.source_url,
        },
        "scenario": {
            "scenario_id": comparison.override.scenario_id,
            "label": comparison.override.label,
            "assumption_note": comparison.override.assumption_note,
            "created_by": comparison.override.created_by,
        },
        "changed_parameters": [
            {**item, "baseline": _fmt(item["baseline"]), "scenario": _fmt(item["scenario"])}
            for item in comparison.changed_parameters
        ],
        "baseline": _result_payload(comparison.baseline),
        "scenario_result": _result_payload(comparison.scenario),
        "deltas": {key: _fmt(value) for key, value in comparison.deltas.items()},
        "limitations": [
            "Angka sumber adalah tampilan SIKD yang dibulatkan, bukan nominal rupiah exact.",
            "Tahun anggaran berjalan; snapshot bukan angka final tahunan.",
            "Skenario adalah asumsi pengguna, bukan realisasi resmi atau ramalan.",
            "Perhitungan ini bukan formula alokasi DBH Perikanan.",
        ],
        "review_status": "needs_review",
        "human_review_required": True,
    }
    digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()
    return {"packet_id": f"pkt-{digest[:12]}", **body}


def _result_payload(result: MonitoringResult) -> dict:
    return {
        "computable": result.computable,
        "budget": _fmt(result.budget),
        "realization": _fmt(result.realization),
        "ratio_pct": _fmt(result.ratio_pct),
        "gap": _fmt(result.gap),
        "trace": [
            {**step, "inputs": {k: _fmt(v) for k, v in step["inputs"].items()}, "output": _fmt(step["output"])}
            for step in result.trace
        ],
        "signals": [
            {**signal, "evidence": {k: _fmt(v) if isinstance(v, Decimal) else v
                                    for k, v in signal["evidence"].items()}}
            for signal in result.signals
        ],
    }


def _step(name: str, expression: str, inputs: dict, output: Decimal | None, note: str = "") -> dict:
    step = {"step": name, "expression": expression, "inputs": inputs, "output": output}
    if note:
        step["note"] = note
    return step


def _signal(rule_id: str, output: str, message: str, observation: Observation, **evidence) -> dict:
    return {
        "rule_id": rule_id,
        "rule_version": RULESET_VERSION,
        "output": output,
        "message": message,
        "evidence": {
            "observation_id": observation.observation_id,
            "snapshot_date": observation.snapshot_date,
            **evidence,
        },
        "human_review_required": True,
    }


def _diff(new: Decimal | None, old: Decimal | None) -> Decimal | None:
    return None if new is None or old is None else new - old


def _pct_change(new: Decimal | None, old: Decimal | None) -> Decimal | None:
    if new is None or old is None or old == 0:
        return None
    return (new - old) / old * HUNDRED


def _fmt(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
