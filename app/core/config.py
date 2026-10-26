"""
Application configuration module.
Loads settings from environment variables or defaults.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "tess_router.db"))
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

# AI API configuration (optional)
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "demo")  # 'demo', 'openai', etc.

# Default multi-objective routing weights (need.md Section 12)
DEFAULT_QUALITY_WEIGHT = float(os.getenv("QUALITY_WEIGHT", "0.50"))
DEFAULT_COST_WEIGHT = float(os.getenv("COST_WEIGHT", "0.30"))
DEFAULT_LATENCY_WEIGHT = float(os.getenv("LATENCY_WEIGHT", "0.20"))
