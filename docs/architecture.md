# System Architecture Document

## 1. Overview
The **TESS AI Inference Router** serves as an intelligent proxy layer positioned between client applications and heterogeneous AI models. Rather than relying on a static, monolithic deployment, the system continuously analyzes incoming requests to balance accuracy, latency, privacy, and cost.

## 2. Component Pipeline
```text
User Request
    │
    ▼
[ FastAPI Gateway ]
    │
    ├───────────────┐
    ▼               ▼
[ Analyzer ]    [ Cache ]
    │               │
    ▼               ├─ Hit ──> Return cached output (0ms, ₹0)
[ Router ]          │
    │               └─ Miss ─┐
    ▼                        │
[ Model Registry ]           ▼
    │                 [ AI Provider ]
    └───────────────> (Small/Med/Large)
                             │
                             ▼
                    [ Metric Logging ]
                             │
                             ▼
                    [ SQLite Database ]
                             │
                             ▼
                    [ Analytics Dashboard ]
```

## 3. Subsystem Breakdown
1. **Request Analyzer:** Computes text length, syntactic tokens, task domains (Coding, Math, Reasoning, General), and privacy markers.
2. **Cache Subsystem:** Normalized SHA-256 hash lookup in SQLite to bypass LLM generation for duplicate queries.
3. **Routing Engine:** Evaluates utility score:
   $$Score = w_q \cdot Quality - w_c \cdot Cost - w_l \cdot Latency$$
4. **Provider Adapter:** Supports offline `DemoProvider` and external `APIProvider`.
5. **Observability Layer:** Logs request metrics and renders live visualizations via Chart.js.
