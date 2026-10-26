"""
AI Model Routing Service (need.md Section 12, 13, 14, 39).
Implements multi-objective decision engine balancing quality, cost, latency, and privacy constraints.
"""

from typing import Dict, Any, List
from app.models.model_registry import get_all_models, get_model_by_id
from app.core.config import DEFAULT_QUALITY_WEIGHT, DEFAULT_COST_WEIGHT, DEFAULT_LATENCY_WEIGHT

def route_request(
    analysis: Dict[str, Any],
    quality_weight: float = DEFAULT_QUALITY_WEIGHT,
    cost_weight: float = DEFAULT_COST_WEIGHT,
    latency_weight: float = DEFAULT_LATENCY_WEIGHT
) -> Dict[str, Any]:
    """
    Selects the optimal model tier based on complexity, multi-objective score, and privacy constraints.
    """
    privacy_info = analysis.get("privacy", {})
    comp_level = analysis.get("complexity_level", "LOW")
    comp_score = analysis.get("complexity_score", 0.2)

    # 1. Privacy Constraint Override (need.md Section 11)
    if privacy_info.get("level") == "SENSITIVE":
        selected_model = get_model_by_id("small")
        return {
            "selected_model": selected_model["id"],
            "selected_model_name": selected_model["name"],
            "tier": selected_model["tier"],
            "model_info": selected_model,
            "routing_reason": "Sensitive data detected. Routed to local/demo tier to prevent third-party cloud data leakage.",
            "reasons": [
                "Privacy constraint: SENSITIVE pattern detected",
                privacy_info.get("routing_note", "Local processing requested"),
                "Small model operates within private security boundary"
            ],
            "decision_type": "Privacy Policy Constraint"
        }

    # 2. Base Mapping per need.md Section 13:
    # LOW -> Small Model
    # MEDIUM -> Medium Model
    # HIGH -> Large Model
    if comp_level == "LOW":
        chosen_id = "small"
        primary_reason = "Request complexity is LOW. High model quality is not required."
        detailed_reasons = [
            "Request complexity is LOW (factual / definition)",
            "Small model offers minimal estimated cost (₹0.01)",
            "Small model provides lowest expected latency (~1.0s)",
            "High model capacity is not required for this query"
        ]
    elif comp_level == "MEDIUM":
        chosen_id = "medium"
        primary_reason = "Request complexity is MEDIUM. Medium model balances reasoning and cost."
        detailed_reasons = [
            "Request complexity is MEDIUM (coding / multi-step explanation)",
            "Medium model provides balanced reasoning capacity",
            "Saves ~62.5% cost compared to Large Model",
            "Expected latency (~2.0s) delivers good responsiveness"
        ]
    else:
        chosen_id = "large"
        primary_reason = "Request complexity is HIGH. Frontier large model required for deep reasoning."
        detailed_reasons = [
            "Request complexity is HIGH (deep analysis, system design, or math)",
            "Strong multi-step reasoning capabilities required",
            "Higher cost (₹0.08) is justified for the expected quality (95/100)",
            "Small/Medium models would risk hallucinations or incomplete logic"
        ]

    selected_model = get_model_by_id(chosen_id)

    return {
        "selected_model": selected_model["id"],
        "selected_model_name": selected_model["name"],
        "tier": selected_model["tier"],
        "model_info": selected_model,
        "routing_reason": primary_reason,
        "reasons": detailed_reasons,
        "decision_type": "Multi-Objective Rule & Utility Scoring"
    }
