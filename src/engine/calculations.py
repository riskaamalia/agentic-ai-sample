"""Deterministic arithmetic for the DBH Perikanan prototype."""

from decimal import Decimal, ROUND_HALF_UP


TWO_PLACES = Decimal("0.01")


def calculate_metrics(budget: Decimal, realization: Decimal) -> dict[str, Decimal | str]:
    """Calculate display-unit metrics. Inputs must use the same unit."""
    if budget < 0 or realization < 0:
        raise ValueError("Pagu dan realisasi tidak boleh negatif.")

    gap = budget - realization
    if budget == 0:
        ratio: Decimal | None = None
        signal = "REVIEW_ZERO_BUDGET"
    else:
        ratio = (realization / budget * Decimal("100")).quantize(
            TWO_PLACES, rounding=ROUND_HALF_UP
        )
        signal = (
            "MONITOR_GAP"
            if realization < budget
            else "REVIEW_OVER_BUDGET"
            if realization > budget
            else "NO_GAP_VISIBLE"
        )

    return {"ratio_pct": ratio, "gap": gap, "signal": signal}


def compare_scenarios(
    baseline_budget: Decimal,
    baseline_realization: Decimal,
    scenario_budget: Decimal,
    scenario_realization: Decimal,
) -> dict[str, Decimal | None]:
    """Return scenario deltas against baseline in the shared display unit."""
    baseline = calculate_metrics(baseline_budget, baseline_realization)
    scenario = calculate_metrics(scenario_budget, scenario_realization)

    baseline_ratio = baseline["ratio_pct"]
    scenario_ratio = scenario["ratio_pct"]
    ratio_delta = (
        scenario_ratio - baseline_ratio
        if baseline_ratio is not None and scenario_ratio is not None
        else None
    )

    return {
        "budget_delta": scenario_budget - baseline_budget,
        "realization_delta": scenario_realization - baseline_realization,
        "ratio_delta_pct_points": ratio_delta,
    }
