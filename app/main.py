"""
FastAPI Main Application entry point.
Mounts API routes and serves frontend static assets.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.routes import api_router

# Initialize database schema and default model registry
init_db()

app = FastAPI(
    title="TESS AI Model Router",
    description="Cost- and Performance-Aware AI Inference Layer & Model Routing Architecture",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routes
app.include_router(api_router)

# Mount frontend directory for static assets
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_home():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(str(FRONTEND_DIR / "dashboard.html"))

@app.get("/comparison")
def serve_comparison():
    return FileResponse(str(FRONTEND_DIR / "comparison.html"))
