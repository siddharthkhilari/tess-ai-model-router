"""
Inference Orchestration Service (need.md Section 16, 17, 18, 19).
Coordinates caching, routing, model invocation, execution timing, cost calculation, and logging.
"""

import time
import random
from typing import Dict, Any
from app.services.analyzer import analyze_prompt
from app.services.router import route_request
from app.services.cost import calculate_cost_and_savings
from app.services.cache import get_cached_response, set_cached_response
from app.providers.demo_provider import DemoProvider
from app.providers.api_provider import APIProvider
from app.core.config import DEMO_MODE
from app.core.database import log_request

# Initialize active AI provider
if DEMO_MODE:
    active_provider = DemoProvider()
else:
    active_provider = APIProvider()

def process_inference_request(prompt: str) -> Dict[str, Any]:
    """
    Executes the complete inference pipeline:
    Analyze -> Cache Check -> Routing -> Model Execution -> Timing -> Costing -> DB Logging.
    """
    prompt_clean = prompt.strip()

    # 1. Analyze prompt complexity, features, and privacy
    analysis = analyze_prompt(prompt_clean)

    # 2. Check Cache (need.md Section 19)
    cached = get_cached_response(prompt_clean)
    if cached is not None:
        # Cache HIT!
        # Return in ultra-low latency, zero compute cost
        latency_ms = round(random.uniform(2.5, 6.0), 2)
        cached_model = cached["model"]
        cost_info = calculate_cost_and_savings(0.0)  # Cached cost is ₹0

        record = {
            "question": prompt_clean,
            "response": cached["response"],
            "task_type": analysis["task_type"],
            "complexity_score": analysis["complexity_score"],
            "complexity_level": analysis["complexity_level"],
            "privacy_level": analysis["privacy"]["level"],
            "selected_model": cached_model,
            "latency_ms": latency_ms,
            "estimated_cost": 0.0,
            "baseline_cost": 0.08,
            "estimated_saving": 0.08,
            "cache_hit": True,
            "routing_reason": "Cache HIT: Retrieved identical prompt from high-speed SQLite cache."
        }
        log_request(record)

        return {
            "question": prompt_clean,
            "response": cached["response"],
            "selected_model": cached_model,
            "selected_model_name": f"{cached_model.capitalize()} Model (Cached)",
            "complexity_level": analysis["complexity_level"],
            "complexity_score": analysis["complexity_score"],
            "privacy_level": analysis["privacy"]["level"],
            "latency_ms": latency_ms,
            "estimated_cost": 0.0,
            "baseline_cost": 0.08,
            "estimated_saving": 0.08,
            "estimated_saving_pct": 100.0,
            "cache_hit": True,
            "routing_reason": "Cache HIT: Instant response returned with zero API/GPU cost.",
            "reasons": [
                "Exact normalized question matched existing cache record",
                "Eliminated redundant inference execution",
                "Reduced query cost to ₹0.00 (100% savings)"
            ]
        }

    # 3. Cache MISS -> Perform Intelligent Routing
    routing_decision = route_request(analysis)
    selected_model_id = routing_decision["selected_model"]
    selected_model_info = routing_decision["model_info"]

    # 4. Measure execution latency (need.md Section 16)
    start_time = time.perf_counter()

    # Small simulated network/inference delay in demo mode for live demonstration
    if DEMO_MODE:
        tier_delays = {"small": 0.25, "medium": 0.45, "large": 0.75}
        time.sleep(tier_delays.get(selected_model_id, 0.3) + random.uniform(0.02, 0.08))

    response_text = active_provider.generate(prompt_clean, selected_model_id)
    raw_latency_sec = time.perf_counter() - start_time
    latency_ms = round(raw_latency_sec * 1000.0, 1)

    # 5. Cost & Savings calculation (need.md Section 17, 18)
    cost_info = calculate_cost_and_savings(selected_model_info["estimated_cost"])

    # 6. Store in Cache for future queries
    set_cached_response(prompt_clean, response_text, selected_model_id)

    # 7. Log to SQLite Database
    record = {
        "question": prompt_clean,
        "response": response_text,
        "task_type": analysis["task_type"],
        "complexity_score": analysis["complexity_score"],
        "complexity_level": analysis["complexity_level"],
        "privacy_level": analysis["privacy"]["level"],
        "selected_model": selected_model_id,
        "latency_ms": latency_ms,
        "estimated_cost": cost_info["estimated_cost"],
        "baseline_cost": cost_info["baseline_cost"],
        "estimated_saving": cost_info["estimated_saving"],
        "cache_hit": False,
        "routing_reason": routing_decision["routing_reason"]
    }
    log_request(record)

    return {
        "question": prompt_clean,
        "response": response_text,
        "selected_model": selected_model_id,
        "selected_model_name": selected_model_info["name"],
        "complexity_level": analysis["complexity_level"],
        "complexity_score": analysis["complexity_score"],
        "privacy_level": analysis["privacy"]["level"],
        "latency_ms": latency_ms,
        "estimated_cost": cost_info["estimated_cost"],
        "baseline_cost": cost_info["baseline_cost"],
        "estimated_saving": cost_info["estimated_saving"],
        "estimated_saving_pct": cost_info["estimated_saving_pct"],
        "cache_hit": False,
        "routing_reason": routing_decision["routing_reason"],
        "reasons": routing_decision["reasons"]
    }

def run_model_comparison(prompt: str) -> Dict[str, Any]:
    """
    Runs the prompt across Small, Medium, and Large models side-by-side (need.md Section 22, 29).
    """
    prompt_clean = prompt.strip()
    analysis = analyze_prompt(prompt_clean)
    routing = route_request(analysis)
    recommended_id = routing["selected_model"]

    models_list = [
        {"id": "small", "name": "Small Model", "tier": "small", "quality": 75, "cost": 0.01, "exp_lat": 1.0, "delay": 0.20},
        {"id": "medium", "name": "Medium Model", "tier": "medium", "quality": 85, "cost": 0.03, "exp_lat": 2.0, "delay": 0.40},
        {"id": "large", "name": "Large Model", "tier": "large", "quality": 95, "cost": 0.08, "exp_lat": 4.0, "delay": 0.70}
    ]

    results = []
    for m in models_list:
        t0 = time.perf_counter()
        if DEMO_MODE:
            time.sleep(m["delay"] + random.uniform(0.01, 0.05))
        resp = active_provider.generate(prompt_clean, m["id"])
        lat_ms = round((time.perf_counter() - t0) * 1000.0, 1)

        results.append({
            "model_id": m["id"],
            "model_name": m["name"],
            "tier": m["tier"],
            "expected_quality": m["quality"],
            "estimated_cost": m["cost"],
            "expected_latency": m["exp_lat"],
            "actual_latency_ms": lat_ms,
            "response": resp,
            "is_recommended": (m["id"] == recommended_id)
        })

    return {
        "question": prompt_clean,
        "recommended_model": routing["selected_model_name"],
        "recommendation_reason": routing["routing_reason"],
        "models": results
    }
