"""
Dashboard API endpoints (need.md Section 21, 30, 38).
Calculates real dynamic metrics from SQLite requests history.
"""

from fastapi import APIRouter
from typing import Dict, Any, List
from app.core.database import get_db_connection

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats():
    """Calculates statistics from stored requests in SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM requests")
    total_requests = cursor.fetchone()[0]

    if total_requests == 0:
        conn.close()
        return {
            "total_requests": 0,
            "average_latency_ms": 0.0,
            "estimated_total_cost": 0.0,
            "estimated_total_savings": 0.0,
            "overall_saving_percentage": 0.0,
            "cache_hit_rate": 0.0,
            "cache_hits": 0,
            "model_usage": {"small": 0, "medium": 0, "large": 0},
            "model_usage_percentage": {"small": 0.0, "medium": 0.0, "large": 0.0},
            "latency_by_model": {"small": 0.0, "medium": 0.0, "large": 0.0},
            "cost_by_model": {"small": 0.0, "medium": 0.0, "large": 0.0},
            "complexity_distribution": {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        }

    # Average latency
    cursor.execute("SELECT AVG(latency_ms) FROM requests")
    avg_latency = cursor.fetchone()[0] or 0.0

    # Total cost & baseline
    cursor.execute("SELECT SUM(estimated_cost), SUM(baseline_cost), SUM(estimated_saving) FROM requests")
    row_cost = cursor.fetchone()
    total_cost = row_cost[0] or 0.0
    total_baseline = row_cost[1] or 0.0
    total_savings = row_cost[2] or 0.0
    overall_saving_pct = (total_savings / total_baseline * 100.0) if total_baseline > 0 else 0.0

    # Cache hit rate
    cursor.execute("SELECT COUNT(*) FROM requests WHERE cache_hit = 1")
    cache_hits = cursor.fetchone()[0]
    cache_hit_rate = (cache_hits / total_requests * 100.0) if total_requests > 0 else 0.0

    # Model usage counts
    cursor.execute("SELECT selected_model, COUNT(*) FROM requests GROUP BY selected_model")
    usage_rows = cursor.fetchall()
    model_usage = {"small": 0, "medium": 0, "large": 0}
    for r in usage_rows:
        m = r[0].lower() if r[0] else "small"
        if m in model_usage:
            model_usage[m] = r[1]
        else:
            model_usage[m] = r[1]

    model_usage_pct = {
        m: round((count / total_requests) * 100.0, 1) for m, count in model_usage.items()
    }

    # Average latency by model
    cursor.execute("SELECT selected_model, AVG(latency_ms) FROM requests GROUP BY selected_model")
    latency_rows = cursor.fetchall()
    latency_by_model = {"small": 0.0, "medium": 0.0, "large": 0.0}
    for r in latency_rows:
        m = r[0].lower() if r[0] else "small"
        latency_by_model[m] = round(r[1] or 0.0, 1)

    # Total cost by model
    cursor.execute("SELECT selected_model, SUM(estimated_cost) FROM requests GROUP BY selected_model")
    cost_rows = cursor.fetchall()
    cost_by_model = {"small": 0.0, "medium": 0.0, "large": 0.0}
    for r in cost_rows:
        m = r[0].lower() if r[0] else "small"
        cost_by_model[m] = round(r[1] or 0.0, 2)

    # Complexity distribution
    cursor.execute("SELECT complexity_level, COUNT(*) FROM requests GROUP BY complexity_level")
    comp_rows = cursor.fetchall()
    comp_dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for r in comp_rows:
        lvl = r[0] or "LOW"
        comp_dist[lvl] = r[1]

    conn.close()

    return {
        "total_requests": total_requests,
        "average_latency_ms": round(avg_latency, 1),
        "estimated_total_cost": round(total_cost, 2),
        "estimated_total_savings": round(total_savings, 2),
        "overall_saving_percentage": round(overall_saving_pct, 1),
        "cache_hits": cache_hits,
        "cache_hit_rate": round(cache_hit_rate, 1),
        "model_usage": model_usage,
        "model_usage_percentage": model_usage_pct,
        "latency_by_model": latency_by_model,
        "cost_by_model": cost_by_model,
        "complexity_distribution": comp_dist
    }

@router.get("/requests")
def get_recent_requests(limit: int = 25):
    """Returns recent requests history for dashboard table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question, response, task_type, complexity_score, complexity_level,
               privacy_level, selected_model, latency_ms, estimated_cost,
               estimated_saving, cache_hit, created_at
        FROM requests
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "question": r["question"],
            "response_preview": r["response"][:90] + "..." if len(r["response"]) > 90 else r["response"],
            "task_type": r["task_type"],
            "complexity_score": r["complexity_score"],
            "complexity_level": r["complexity_level"],
            "privacy_level": r["privacy_level"],
            "selected_model": r["selected_model"],
            "latency_ms": round(r["latency_ms"], 1),
            "estimated_cost": r["estimated_cost"],
            "estimated_saving": r["estimated_saving"],
            "cache_hit": bool(r["cache_hit"]),
            "created_at": r["created_at"]
        })
    return items
