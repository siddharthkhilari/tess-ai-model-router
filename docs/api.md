# API Reference Specification

Base URL: `http://127.0.0.1:8000/api`

## 1. System Health
- **Endpoint:** `GET /health`
- **Response:**
  ```json
  {
    "status": "ok",
    "demo_mode": true,
    "weights": { "quality": 0.50, "cost": 0.30, "latency": 0.20 }
  }
  ```

## 2. Model Registry
- **Endpoint:** `GET /models`
- **Response:** Array of model objects with id, name, cost, expected quality, and expected latency.

## 3. Analyze Prompt
- **Endpoint:** `POST /analyze`
- **Request Body:** `{"question": "What is RAM?"}`
- **Response:**
  ```json
  {
    "question": "What is RAM?",
    "word_count": 3,
    "char_count": 12,
    "task_type": "General Question",
    "complexity_score": 0.15,
    "complexity_level": "LOW",
    "privacy": { "level": "PUBLIC", "matched_keywords": [], "routing_note": "..." },
    "reasons": ["Simple factual lookup"]
  }
  ```

## 4. Route & Generate
- **Endpoint:** `POST /generate`
- **Request Body:** `{"question": "What is RAM?"}`
- **Response:** Returns selected model, response text, measured latency, calculated cost, savings, cache hit status, and explanation reasons.

## 5. Model Comparison
- **Endpoint:** `POST /compare`
- **Request Body:** `{"question": "Explain binary search in Java"}`
- **Response:** Returns side-by-side execution metrics across Small, Medium, and Large models with the recommended model flagged.

## 6. Dashboard Analytics
- **Endpoint:** `GET /dashboard/stats`
- **Response:** Aggregate telemetry, model usage percentages, latency/cost breakdown, and cache hit metrics.
