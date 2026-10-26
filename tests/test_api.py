import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

init_db()
client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_api_models():
    res = client.get("/api/models")
    assert res.status_code == 200
    models = res.json()
    assert len(models) >= 3

def test_api_analyze():
    res = client.post("/api/analyze", json={"question": "What is RAM?"})
    assert res.status_code == 200
    data = res.json()
    assert data["complexity_level"] == "LOW"

def test_api_generate_and_cache():
    import time
    # First request: Cache MISS
    q = f"What is a compiler vs an interpreter? - {time.time()}"
    res1 = client.post("/api/generate", json={"question": q})
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["cache_hit"] is False

    # Second request: Cache HIT
    res2 = client.post("/api/generate", json={"question": q})
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["cache_hit"] is True
    assert d2["estimated_cost"] == 0.0

def test_api_compare():
    res = client.post("/api/compare", json={"question": "Explain binary search in Java"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["models"]) == 3
    assert any(m["is_recommended"] for m in data["models"])

def test_api_dashboard_stats():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert "total_requests" in data
    assert "average_latency_ms" in data

if __name__ == "__main__":
    test_api_health()
    test_api_models()
    test_api_analyze()
    test_api_generate_and_cache()
    test_api_compare()
    test_api_dashboard_stats()
    print("All API integration tests passed successfully!")
