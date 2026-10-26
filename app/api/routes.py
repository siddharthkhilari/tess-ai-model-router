"""
Consolidated API router registry (need.md Section 21).
"""

from fastapi import APIRouter
from app.api.analyze import router as analyze_router
from app.api.generate import router as generate_router
from app.api.dashboard import router as dashboard_router
from app.models.model_registry import get_all_models
from app.core.config import DEMO_MODE, DEFAULT_QUALITY_WEIGHT, DEFAULT_COST_WEIGHT, DEFAULT_LATENCY_WEIGHT

api_router = APIRouter(prefix="/api")

@api_router.get("/health")
def health_check():
    """System health check endpoint (need.md Section 21)."""
    return {
        "status": "ok",
        "demo_mode": DEMO_MODE,
        "weights": {
            "quality": DEFAULT_QUALITY_WEIGHT,
            "cost": DEFAULT_COST_WEIGHT,
            "latency": DEFAULT_LATENCY_WEIGHT
        }
    }

@api_router.get("/models")
def list_models():
    """List available AI models in the registry (need.md Section 21)."""
    return get_all_models()

# Include subrouters
api_router.include_router(analyze_router)
api_router.include_router(generate_router)
api_router.include_router(dashboard_router)
