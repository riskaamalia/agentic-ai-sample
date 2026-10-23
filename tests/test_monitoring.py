import json
from decimal import Decimal
from pathlib import Path

import pytest

from engine.monitoring import (
    Observation,
    ScenarioOverride,
    build_evidence_packet,
    evaluate,
    run_scenario,
)

FIXTURE = Path(__file__).resolve().parents[1] / "src" / "data" / "observations.json"


def load(observation_id: str) -> Observation:
    records = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return Observation.from_record(next(r for r in records if r["observation_id"] == observation_id))


def make(budget, realization, value_status="AVAILABLE") -> Observation:
    return Observation(
        observation_id="test-obs",
        fiscal_year=2026,
        region_name="Uji",
        region_level="NATIONAL",
        budget=None if budget is None else Decimal(budget),
        realization=None if realization is None else Decimal(realization),
        value_status=value_status,
        precision_status="ROUNDED_DISPLAY",
        snapshot_date="2026-10-22",
        source_url="https://example.invalid",
    )


def rule_ids(result):
    return [signal["rule_id"] for signal in result.signals]


def test_national_2026_matches_documented_reference():
    result = evaluate(load("sikd-2026-national-perikanan"))
    assert result.gap == Decimal("42430.0")
    assert result.ratio_pct.quantize(Decimal("0.01")) == Decimal("81.22")
    assert rule_ids(result) == ["DQ-002", "MON-001"]


def test_zero_budget_ratio_is_not_available_not_zero():
    result = evaluate(make("0", "0"))
    assert result.computable
    assert result.ratio_pct is None
    assert result.trace[-1]["note"].startswith("B = 0")


def test_missing_value_is_not_treated_as_zero():
    result = evaluate(make("100", None))
    assert not result.computable
    assert result.gap is None and result.ratio_pct is None
    assert rule_ids(result) == ["DQ-001"]


def test_nan_from_pandas_is_loaded_as_not_available():
    record = {
        "observation_id": "x", "fiscal_year": 2026, "region_name": "Uji", "region_level": "NATIONAL",
        "budget_million_idr": float("nan"), "realization_million_idr": 1.0,
        "value_status": "AVAILABLE", "precision_status": "ROUNDED_DISPLAY",
        "snapshot_date": "2026-10-22", "source_url": "https://example.invalid",
    }
    assert Observation.from_record(record).budget is None


def test_not_verified_status_blocks_monitoring_signals():
    result = evaluate(make("100", "50", value_status="NOT_VERIFIED"))
    assert rule_ids(result) == ["DQ-001"]


def test_over_budget_is_not_capped_and_flags_review():
    result = evaluate(make("100", "120"))
    assert result.ratio_pct == Decimal("120")
    assert "MON-002" in rule_ids(result)


def test_scenario_does_not_mutate_observation_and_reports_deltas():
    observation = load("sikd-2026-national-perikanan")
    override = ScenarioOverride(
        scenario_id="sc-1",
        label="Realisasi tambahan",
        assumption_note="Asumsi penyaluran tambahan Rp20 M sebelum akhir tahun.",
        realization=Decimal("203470"),
    )
    comparison = run_scenario(observation, override)
    assert observation.realization == Decimal("183470.0")
    assert comparison.deltas["gap"] == Decimal("-20000.0")
    assert comparison.deltas["ratio_pp"].quantize(Decimal("0.01")) == Decimal("8.85")
    assert [c["parameter"] for c in comparison.changed_parameters] == ["realisasi"]


def test_scenario_requires_assumption_and_rejects_negative():
    with pytest.raises(ValueError):
        ScenarioOverride("sc", "x", "  ", realization=Decimal("1"))
    with pytest.raises(ValueError):
        ScenarioOverride("sc", "x", "catatan", budget=Decimal("-1"))
    with pytest.raises(ValueError):
        ScenarioOverride("sc", "x", "catatan")


def test_evidence_packet_is_json_safe_stable_and_flagged_for_review():
    observation = load("sikd-2026-national-perikanan")
    override = ScenarioOverride("sc-1", "Pagu turun", "Asumsi penyesuaian pagu.", budget=Decimal("200000"))
    packet = build_evidence_packet(run_scenario(observation, override))
    again = build_evidence_packet(run_scenario(observation, override))

    assert json.loads(json.dumps(packet)) == packet
    assert packet["packet_id"] == again["packet_id"]
    assert packet["is_allocation_formula"] is False
    assert packet["human_review_required"] is True
    assert packet["baseline"]["ratio_pct"] == "81.22"
    assert packet["scenario_result"]["ratio_pct"] == "91.74"
    assert packet["changed_parameters"][0]["parameter"] == "pagu"
