"""
Cost and Savings Calculation Service (need.md Section 17, 18).
Calculates per-request estimated costs and savings relative to a large model baseline.
"""

from typing import Dict, Any

BASELINE_MODEL_COST = 0.08  # Large Model Cost (₹0.08)

def calculate_cost_and_savings(selected_model_cost: float) -> Dict[str, float]:
    """
    Computes estimated cost and savings compared to using a Large model baseline.
    Note: These are demo/estimated values per need.md instructions.
    """
    baseline = BASELINE_MODEL_COST
    actual = float(selected_model_cost)
    saving = max(0.0, baseline - actual)
    saving_pct = (saving / baseline) * 100.0 if baseline > 0 else 0.0

    return {
        "estimated_cost": round(actual, 4),
        "baseline_cost": round(baseline, 4),
        "estimated_saving": round(saving, 4),
        "estimated_saving_pct": round(saving_pct, 1)
    }
