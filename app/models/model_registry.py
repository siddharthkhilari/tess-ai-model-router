"""
Model Registry service.
Manages available AI models, their configurations, costs, quality, and latency metrics.
"""

from typing import Dict, Any, List
from app.core.database import get_db_connection

def get_all_models() -> List[Dict[str, Any]]:
    """Retrieves all registered models from database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, tier, description, estimated_cost, expected_quality, expected_latency, available FROM models")
    rows = cursor.fetchall()
    conn.close()

    models = []
    for r in rows:
        models.append({
            "id": r["id"],
            "name": r["name"],
            "tier": r["tier"],
            "description": r["description"],
            "estimated_cost": float(r["estimated_cost"]),
            "expected_quality": int(r["expected_quality"]),
            "expected_latency": float(r["expected_latency"]),
            "available": bool(r["available"])
        })
    return models

def get_model_by_id(model_id: str) -> Dict[str, Any]:
    """Retrieves a single model by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, tier, description, estimated_cost, expected_quality, expected_latency, available FROM models WHERE id = ?", (model_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row["id"],
            "name": row["name"],
            "tier": row["tier"],
            "description": row["description"],
            "estimated_cost": float(row["estimated_cost"]),
            "expected_quality": int(row["expected_quality"]),
            "expected_latency": float(row["expected_latency"]),
            "available": bool(row["available"])
        }
    # Fallback to small model if not found
    return {
        "id": "small",
        "name": "Small Model",
        "tier": "small",
        "description": "Fallback SLM",
        "estimated_cost": 0.01,
        "expected_quality": 75,
        "expected_latency": 1.0,
        "available": True
    }
