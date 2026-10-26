# Efficient AI Infrastructure for TESS – Cost and Performance Aware AI Model Router

> **Problem Based Learning (PBL) Prototype**  
> *Savitribai Phule Pune University (SPPU) — Department of Computer Engineering*

---

## 1. Project Overview & Problem Statement
Modern generative AI workflows default to routing all incoming user queries directly to expensive, frontier Large Language Models (LLMs like GPT-4 or Llama-70B). However, industry studies and empirical benchmarks demonstrate that **70–80% of real-world queries** are simple factual lookups, standard definitions, or basic questions that do not warrant a high-parameter model.

This causes:
1. **Excessive Cloud & GPU Expenses:** Overpaying up to $0.08 per request when a $0.01 Small Language Model (SLM) is sufficient.
2. **Elevated Response Latency:** Users wait 3–5 seconds for simple answers that could be returned in <1 second.
3. **Data Privacy Risks:** Sensitive enterprise or personal data (e.g., Aadhaar, medical reports) is inadvertently exposed to third-party public cloud APIs.

### The Solution: Intelligent AI Inference Router
This project develops an **intelligent, explainable AI inference routing prototype** that inspects prompt complexity, tasks, privacy constraints, and expected SLAs to route requests to the most cost-effective model tier:
- **Small Model (SLM):** ₹0.01 / request, ~1.0s latency, quality score 75/100 (for basic Q&A, definitions, and privacy-sensitive data).
- **Medium Model:** ₹0.03 / request, ~2.0s latency, quality score 85/100 (for moderate coding and explanations).
- **Large Model (LLM):** ₹0.08 / request, ~4.0s latency, quality score 95/100 (for complex systems architecture, mathematical proofs, and multi-step reasoning).
- **Exact SQLite Caching:** Returns previously answered queries in <5 ms at ₹0.00 compute cost (100% savings).

---

## 2. Key Features
- **Deterministic Complexity Detection:** Transparent scoring ($0.0 - 1.0$) categorizing prompts into `LOW`, `MEDIUM`, or `HIGH`.
- **Privacy Shield:** Scans for sensitive PII (Aadhaar, PAN, passport, medical records, credentials) and forces local execution.
- **Explainable Multi-Objective Routing:** Balances Quality (0.50), Cost (0.30), and Latency (0.20) with plain-English viva explanations.
- **Dynamic Cost Savings Calculation:** Automatically measures savings relative to a large-model-only baseline.
- **Zero-Dependency Demo Mode:** Runs completely offline without API keys, GPU hardware, or cloud accounts.
- **Live Analytics Dashboard:** Interactive Chart.js graphs computing real telemetry from SQLite.
- **Side-by-Side Model Comparison:** Run a prompt across all 3 tiers simultaneously to inspect quality, latency, and cost differences.

---

## 3. Technology Stack
- **Backend:** Python 3.12, FastAPI, Uvicorn
- **Database:** SQLite 3 (zero external configuration)
- **Machine Learning & EDA:** scikit-learn, pandas, numpy, matplotlib, seaborn
- **Frontend:** Vanilla HTML5, CSS3 (modern academic theme), JavaScript, Chart.js

---

## 4. System Architecture
```text
                         [ User / Web Client ]
                                  │
                                  ▼
                        [ FastAPI Application ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
 [ Request Analyzer ]                             [ SQLite Cache ]
 (Complexity 0.0-1.0 + Privacy)                   (Question Hash Lookup)
          │                                               │
          ▼                                               ├─ HIT ──> [ Return in 5ms, ₹0 ]
   [ AI Router ]                                          │
 (Multi-Objective Utility Scoring)                        └─ MISS ─┐
          │                                                        │
          ├───────────────────────────────┬────────────────────────┘
          ▼                               ▼
 [ Model Registry ]              [ AI Provider ]
 (Small / Med / Large)           (Demo Provider / Optional API)
          │                               │
          ▼                               ▼
 [ SQLite Logging & DB ] <─────── [ Response & Latency Timer ]
 (Requests, Latency, Cost)
          │
          ▼
 [ Live Analytics Dashboard ]
```

---

## 5. Quick Start & Execution

### Prerequisites
Make sure Python 3.10+ is installed.

### Installation
```bash
# Clone or navigate to project directory
cd "c:\Users\Admin\Desktop\Projects\Harsh"

# Install dependencies
pip install -r requirements.txt
```

### Running the Application (One Command)
```bash
python run.py
```

The terminal will launch the Uvicorn server:
- **AI Router Home:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Live Dashboard:** [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
- **Model Comparison:** [http://127.0.0.1:8000/comparison](http://127.0.0.1:8000/comparison)
- **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 6. Project Directory Structure
```text
tess-ai-router/
│
├── app/
│   ├── main.py                 # FastAPI application & static mount
│   ├── api/
│   │   ├── routes.py           # Consolidated API router
│   │   ├── analyze.py          # /api/analyze endpoint
│   │   ├── generate.py         # /api/generate & /api/compare endpoints
│   │   └── dashboard.py        # /api/dashboard/stats & /api/requests
│   ├── core/
│   │   ├── config.py           # Settings & weights
│   │   └── database.py         # SQLite setup, tables & logging
│   ├── models/
│   │   ├── model_registry.py   # Small, Medium, Large tier configurations
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── services/
│   │   ├── analyzer.py         # Complexity & task detection
│   │   ├── privacy.py          # PII & sensitive keyword detection
│   │   ├── router.py           # Multi-objective routing logic
│   │   ├── cost.py             # Cost & savings calculation
│   │   ├── cache.py            # SQLite query caching
│   │   └── inference.py        # Pipeline orchestrator & timing
│   └── providers/
│       ├── base.py             # Base provider interface
│       ├── demo_provider.py    # Realistic offline demo responses
│       └── api_provider.py     # Optional OpenAI/HuggingFace adapter
│
├── frontend/
│   ├── index.html              # AI Router interactive page
│   ├── dashboard.html          # Analytics Dashboard (Chart.js)
│   ├── comparison.html         # Side-by-side comparison page
│   ├── css/
│   │   └── style.css           # Clean responsive academic styling
│   └── js/
│       ├── app.js              # Router client logic
│       ├── dashboard.js        # Live metrics polling & charts
│       └── comparison.js       # Comparison benchmark logic
│
├── dataset/
│   └── inference_routing_dataset.csv  # 325-sample benchmark dataset
├── eda_output/                 # EDA report & 4 high-res visualization figures
├── tests/                      # Automated unit & integration tests
│   ├── test_analyzer.py
│   ├── test_router.py
│   ├── test_cost.py
│   └── test_api.py
├── generate_dataset.py         # Dataset generation script
├── dataset_analysis.py         # Statistical EDA & plotting script
├── router_model.py             # Rule + ML baseline router with 87% accuracy
├── PBL_Project_Report.docx     # 5th Attachment: Formal academic report
├── Team_Members_IA.docx        # 1st Attachment: 4-Member IA & rubric sheet
├── run.py                      # One-command server runner
└── requirements.txt
```

---

## 7. Running the Tests
Run all unit and integration tests:
```powershell
python tests/test_analyzer.py
python tests/test_router.py
python tests/test_cost.py
python tests/test_api.py
```

---

## 8. Viva & Presentation Guide

### Quick 5-Minute Demo Flow:
1. **Low Complexity Demo:** Select preset `"What is RAM?"`. Show: Routed to **Small Model**, Latency ~250ms, Cost ₹0.01, Savings 87.5%.
2. **Medium Complexity Demo:** Select preset `"Write a Java program to implement binary search and explain its time complexity."`. Show: Routed to **Medium Model**, Latency ~450ms, Cost ₹0.03, Savings 62.5%.
3. **High Complexity Demo:** Select preset `"Analyze a distributed application architecture and identify possible performance and concurrency problems."`. Show: Routed to **Large Model**, Cost ₹0.08, High reasoning capacity.
4. **Cache Demo:** Click Route again on the same question. Show: **Cache: HIT**, Cost ₹0.00, Latency 4ms, Savings 100%!
5. **Privacy Demo:** Enter `"Analyze this confidential employee record: Aadhaar 4589-1234-8765."`. Show: **SENSITIVE** warning triggered, routed locally.
6. **Comparison Tab:** Enter any query and show side-by-side output, latency, and cost across all 3 tiers with recommended tier highlighted.
7. **Dashboard Tab:** Show real SQLite-calculated metrics: Total requests, savings curve, model usage distribution, and request logs.
