# need.md

# Efficient AI Infrastructure for TESS
## College-Level AI Inference Router Prototype

---

## 1. IMPORTANT PROJECT INSTRUCTION

Build this project as a **simple, working college-level prototype**.

The original project topic mentions advanced technologies such as Kubernetes, NVIDIA Triton, vLLM, MLflow, quantization, distributed systems, and GPU infrastructure. **DO NOT implement production-grade or distributed infrastructure.**

The goal is to create a clear demonstration/prototype of the core idea:

> An intelligent inference layer that decides which AI model should process a request based on complexity, expected quality, latency, cost, and basic privacy considerations.

The application must be:
- Simple enough for a college project
- Easy to run locally
- Easy to explain in a viva
- Visually professional
- Fully functional
- Easy to demonstrate
- Modular enough that advanced features can be added later

Do NOT over-engineer the project.

---

# 2. PROJECT TITLE

**Efficient AI Infrastructure for TESS – Cost and Performance Aware AI Model Router**

Alternative short title:

**AI Model Router for Cost-Efficient Inference**

---

# 3. PROJECT OBJECTIVE

Build a web-based AI inference router that:

1. Accepts a user question.
2. Analyzes the request.
3. Determines its approximate complexity.
4. Selects the most suitable AI model.
5. Sends the request to the selected model.
6. Measures response latency.
7. Calculates estimated inference cost.
8. Displays the response and routing decision.
9. Stores request metrics.
10. Provides a dashboard showing model usage, latency, cost, and estimated savings.
11. Provides a model comparison feature.

The system should demonstrate that simple requests can be processed by cheaper/faster models while complex requests can be sent to stronger models.

---

# 4. CORE CONCEPT

The system should work approximately as follows:

User
  ↓
Web Interface
  ↓
Request Analyzer
  ↓
Complexity Detection
  ↓
AI Model Router
  ↓
Select Small / Medium / Large Model
  ↓
AI Inference
  ↓
Measure Latency
  ↓
Calculate Estimated Cost
  ↓
Store Metrics
  ↓
Display Response
  ↓
Dashboard Analytics

---

# 5. VERY IMPORTANT SCOPE LIMITATION

This is NOT a production AI infrastructure platform.

Do NOT implement:

- Kubernetes cluster
- GPU cluster
- Multi-node inference
- Distributed inference
- GPU autoscaling
- NVIDIA Triton production deployment
- Complex reinforcement learning routing
- Multi-GPU scheduling
- Service mesh
- Production cloud deployment
- Complex MLOps pipelines
- Training a large language model
- Building an LLM from scratch
- Complex vector databases
- Complex microservice architecture
- Real enterprise authentication
- Payment systems
- Real billing integration

These may be mentioned as future scope only.

---

# 6. TECHNOLOGY STACK

Use a simple and reliable stack.

## Backend

- Python 3.11+
- FastAPI
- Uvicorn

## Frontend

Prefer:
- HTML5
- CSS3
- JavaScript
- Bootstrap or Tailwind CDN if useful

React is NOT required.

Keep the frontend simple.

## Database

Use:
- SQLite

Do NOT use PostgreSQL/MySQL unless there is a strong technical reason.

## AI

The application should support an AI provider through a configurable API key.

Use an adapter architecture so the project can work with a real AI API if an API key is available.

Also provide a **Demo/Mock AI Mode** so the complete project can run without an API key.

This is mandatory.

## Charts

Use:
- Chart.js

## Optional

- Dockerfile
- docker-compose.yml

Docker should remain optional and simple.

---

# 7. MODEL CONCEPT

The application should represent three model tiers:

### Small Model

Characteristics:
- Low cost
- Low latency
- Lower expected quality
- Suitable for simple requests

Example configuration:

```text
Name: Small Model
Cost per request: ₹0.01
Expected quality: 75
Expected latency: 1.0 sec
```

### Medium Model

```text
Name: Medium Model
Cost per request: ₹0.03
Expected quality: 85
Expected latency: 2.0 sec
```

### Large Model

```text
Name: Large Model
Cost per request: ₹0.08
Expected quality: 95
Expected latency: 4.0 sec
```

IMPORTANT:

These values are **demo/estimated values**, not claims about real commercial API pricing.

Clearly label them as:

**Estimated/Demo Cost**

---

# 8. AI PROVIDER ARCHITECTURE

Create an abstraction such as:

```text
AIProvider
    ├── DemoProvider
    └── APIProvider
```

The router should not directly depend on one AI provider.

### DemoProvider

Mandatory.

It should generate realistic demo responses without requiring an API key.

For example:

```text
Question:
What is inheritance in Java?

Demo response:
Inheritance is an OOP mechanism...
```

The exact response can be generated from simple templates or deterministic demo logic.

The system must work completely in Demo Mode.

### APIProvider

Optional real AI API integration.

Read API configuration from `.env`.

Never hard-code API keys.

---

# 9. REQUEST ANALYZER

Create a simple request analyzer.

It should estimate:

- Word count
- Character count
- Complexity
- Task type
- Basic privacy level

Do NOT build a complicated NLP model.

Use transparent and explainable rules.

Example task types:

- General Question
- Explanation
- Coding
- Mathematics
- Summarization
- Reasoning
- Analysis

---

# 10. COMPLEXITY CALCULATION

Implement a simple explainable scoring system.

Example:

```text
Base score = 0

If word count > 50:
    +1

If word count > 150:
    +1

If coding keywords exist:
    +1

If reasoning/analysis keywords exist:
    +1

If multiple requirements are detected:
    +1

If long-form generation is requested:
    +1
```

Normalize the score to:

```text
0.0 – 1.0
```

Then classify:

```text
0.00 – 0.39 = LOW
0.40 – 0.69 = MEDIUM
0.70 – 1.00 = HIGH
```

The exact thresholds may be adjusted during implementation.

The UI should explain why the request received its complexity level.

Example:

```text
Complexity: MEDIUM

Reasons:
- Coding task detected
- Request contains multiple requirements
- Moderate request length
```

---

# 11. PRIVACY DETECTION

Implement only a simple demonstration-level privacy detector.

Look for obvious sensitive keywords/patterns such as:

- Aadhaar
- PAN
- passport
- credit card
- password
- confidential
- private
- secret
- medical record

Classify:

```text
PUBLIC
SENSITIVE
```

If sensitive information is detected:

- Prefer the configured local/demo model.
- Display a warning.
- Do NOT send sensitive data to an external API unless the user explicitly chooses to do so.

Do not claim this is a complete privacy/security system.

Display:

```text
Privacy Level: Sensitive
Routing Note: Prefer local/demo processing
```

---

# 12. ROUTING ALGORITHM

This is the main feature.

The router should consider:

1. Complexity
2. Expected quality
3. Cost
4. Expected latency
5. Privacy

Use a simple transparent scoring algorithm.

Example conceptual score:

```text
final_score =
    quality_weight * quality_score
    - cost_weight * cost_score
    - latency_weight * latency_score
```

Use configurable weights.

Suggested default:

```text
quality_weight = 0.50
cost_weight = 0.30
latency_weight = 0.20
```

For sensitive requests:

```text
Privacy becomes a routing constraint.
```

The router should select the lowest-cost model that can reasonably satisfy the request, rather than always selecting the strongest model.

---

# 13. SIMPLE ROUTING RULE

As a fallback and for explainability, implement:

```text
LOW complexity
    → Small Model

MEDIUM complexity
    → Medium Model

HIGH complexity
    → Large Model
```

Then allow the scoring system to adjust the decision according to cost/latency/quality.

This makes the project easy to explain.

---

# 14. ROUTING EXPLANATION

Every request must return a routing explanation.

Example:

```text
Selected Model: Small Model

Reason:
- Request complexity is LOW
- High model quality is not required
- Small model has lower estimated cost
- Small model has lower expected latency
```

For a complex request:

```text
Selected Model: Large Model

Reason:
- Request complexity is HIGH
- Stronger reasoning capability is preferred
- Higher cost is justified for the expected quality
```

This explanation is important for the viva.

---

# 15. MODEL REGISTRY

Create a simple model configuration/registry.

Each model should contain:

```text
id
name
tier
description
estimated_cost
expected_quality
expected_latency
available
```

Example:

```json
{
  "id": "small",
  "name": "Small Model",
  "tier": "small",
  "estimated_cost": 0.01,
  "expected_quality": 75,
  "expected_latency": 1.0
}
```

The model registry should be easy to modify.

Do NOT hard-code model information throughout the application.

---

# 16. INFERENCE

After selecting the model:

```text
Request
  ↓
Selected Model
  ↓
AI Provider
  ↓
Response
```

Measure actual application execution time.

Example:

```python
start = time.perf_counter()

response = provider.generate(...)

latency = time.perf_counter() - start
```

Store the measured latency.

In Demo Mode, latency can be simulated realistically if necessary, but clearly label simulated/demo metrics.

---

# 17. COST CALCULATION

Calculate estimated cost using the selected model configuration.

For the college prototype, request-level cost is sufficient.

Example:

```text
Small = ₹0.01
Medium = ₹0.03
Large = ₹0.08
```

Show:

```text
Estimated Cost: ₹0.01
```

Also calculate:

```text
Potential Cost
```

if the Large Model had been used.

Example:

```text
Selected model cost: ₹0.01
Large model cost: ₹0.08

Estimated saving: ₹0.07
Estimated saving percentage: 87.5%
```

Clearly label all such values as estimated/demo values.

---

# 18. COST SAVING CALCULATION

For every request:

```text
baseline_cost = large_model_cost

actual_cost = selected_model_cost

saving = baseline_cost - actual_cost

saving_percentage =
    (saving / baseline_cost) * 100
```

This should be displayed on the result page.

---

# 19. SIMPLE CACHE

Implement a basic cache.

Use SQLite for the first implementation.

Before calling the AI provider:

```text
Normalize question
     ↓
Check cache
     ↓
Cache HIT?
   YES → return cached response
   NO  → call model
```

Store:

```text
question_hash
question
response
model
created_at
```

Show:

```text
Cache: HIT
```

or:

```text
Cache: MISS
```

Do NOT implement semantic vector caching.

---

# 20. DATABASE

Use SQLite.

Create at least these tables.

## requests

```text
id
question
response
task_type
complexity_score
complexity_level
privacy_level
selected_model
latency_ms
estimated_cost
baseline_cost
estimated_saving
cache_hit
created_at
```

## models

```text
id
name
tier
description
estimated_cost
expected_quality
expected_latency
available
```

The application can seed the default models automatically.

---

# 21. API ENDPOINTS

Implement simple REST endpoints.

### Health

```http
GET /api/health
```

Returns:

```json
{
  "status": "ok"
}
```

### Models

```http
GET /api/models
```

Returns available models.

### Analyze

```http
POST /api/analyze
```

Input:

```json
{
  "question": "Explain binary search in Java"
}
```

Return analysis.

### Generate

```http
POST /api/generate
```

Input:

```json
{
  "question": "Explain binary search in Java"
}
```

Return:

```json
{
  "response": "...",
  "selected_model": "small",
  "complexity": "low",
  "latency_ms": 1200,
  "estimated_cost": 0.01,
  "estimated_saving": 87.5,
  "cache_hit": false
}
```

### Dashboard statistics

```http
GET /api/dashboard/stats
```

Return:

- total requests
- model usage
- average latency
- estimated total cost
- estimated savings
- cache hit rate

### Request history

```http
GET /api/requests
```

Return recent requests.

---

# 22. FRONTEND PAGES

Keep the frontend small.

## Page 1: Home / AI Router

Components:

- Project title
- Question textarea
- Send button
- Demo Mode indicator
- Result card

Result card:

```text
Selected Model
Complexity
Privacy
Latency
Estimated Cost
Estimated Saving
Cache Status
Routing Reason
AI Response
```

---

## Page 2: Dashboard

Show:

### Summary cards

```text
Total Requests
Average Latency
Estimated Cost
Estimated Savings
Cache Hit Rate
```

### Charts

1. Model usage pie/doughnut chart
2. Latency by model
3. Cost by model
4. Requests over time

Use Chart.js.

---

## Page 3: Model Comparison

Allow the user to enter one question.

Run the question through all configured models.

Display:

| Metric | Small | Medium | Large |
|---|---:|---:|---:|
| Estimated Quality | 75 | 85 | 95 |
| Estimated Cost | ₹0.01 | ₹0.03 | ₹0.08 |
| Expected Latency | 1s | 2s | 4s |
| Actual Latency | ... | ... | ... |

Highlight the recommended model.

This page is important for demonstrating why intelligent routing is useful.

---

# 23. UI DESIGN

Make the UI clean but simple.

Use:

- Responsive layout
- Cards
- Tables
- Simple navigation
- Clear labels
- Loading indicator
- Error messages
- Empty states

Do NOT spend excessive time on animations.

The project should look like a professional academic prototype.

---

# 24. DEMO MODE

This is mandatory.

The project must run without:

- GPU
- Kubernetes
- vLLM
- paid API
- cloud account

Command:

```bash
python run.py
```

or an equivalent simple startup command.

Demo Mode should:

1. Analyze the question.
2. Select a model.
3. Generate a demo response.
4. Measure/simulate latency.
5. Calculate cost.
6. Save the request.
7. Update dashboard.

The evaluator must be able to run the project on a normal college laptop.

---

# 25. OPTIONAL REAL AI MODE

If an API key is configured:

```env
AI_API_KEY=...
AI_PROVIDER=...
```

the application may use a real AI provider.

Provide:

```env
DEMO_MODE=true
```

as the default.

Never expose API keys in frontend code.

Never commit `.env`.

Provide `.env.example`.

---

# 26. PROJECT STRUCTURE

Use a clean structure similar to:

```text
tess-ai-router/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   ├── analyze.py
│   │   ├── generate.py
│   │   └── dashboard.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── model_registry.py
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── analyzer.py
│   │   ├── router.py
│   │   ├── cache.py
│   │   ├── cost.py
│   │   ├── privacy.py
│   │   └── inference.py
│   │
│   └── providers/
│       ├── base.py
│       ├── demo_provider.py
│       └── api_provider.py
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── comparison.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── dashboard.js
│       └── comparison.js
│
├── data/
│   └── .gitkeep
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_router.py
│   ├── test_cost.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── need.md
└── run.py
```

The exact structure can be adjusted if necessary, but keep the separation of concerns.

---

# 27. TESTING

Implement basic tests.

At minimum:

### Analyzer tests

Test:

- Simple question
- Medium question
- Complex question

### Router tests

Test:

```text
LOW → Small
MEDIUM → Medium
HIGH → Large
```

### Cost tests

Verify cost calculations.

### Cache tests

Verify:

```text
First request → MISS
Same request → HIT
```

### API tests

Verify the major endpoints.

The project does not need enterprise-level test coverage.

---

# 28. SAMPLE TEST QUESTIONS

Include a small set of demo questions.

### Low

```text
What is RAM?
```

Expected:

```text
LOW
Small Model
```

### Low

```text
What is inheritance in Java?
```

Expected:

```text
LOW
Small Model
```

### Medium

```text
Write a Java program to implement binary search and explain its time complexity.
```

Expected:

```text
MEDIUM
Medium Model
```

### High

```text
Analyze a distributed application architecture and identify possible performance and concurrency problems.
```

Expected:

```text
HIGH
Large Model
```

### Sensitive

```text
Analyze this confidential employee record.
```

Expected:

```text
SENSITIVE
Prefer Demo/Local Processing
```

---

# 29. MODEL COMPARISON DEMONSTRATION

The final project must support a demonstration such as:

Question:

```text
Explain binary search and provide Java implementation.
```

The system shows:

```text
Small Model
Quality: 75
Cost: ₹0.01
Latency: 1.2 sec

Medium Model
Quality: 85
Cost: ₹0.03
Latency: 2.0 sec

Large Model
Quality: 95
Cost: ₹0.08
Latency: 4.0 sec

Recommended:
Medium Model
```

This demonstrates the project's core research concept.

---

# 30. DASHBOARD EXAMPLE

Dashboard should eventually show something similar to:

```text
========================================
       TESS AI INFERENCE DASHBOARD
========================================

Total Requests       120
Average Latency      1.72 sec
Estimated Cost       ₹3.42
Estimated Savings    ₹6.18
Cache Hit Rate       24%

MODEL USAGE

Small Model          60%
Medium Model         28%
Large Model          12%

========================================
```

The numbers should come from the database, not hard-coded dashboard values.

---

# 31. FUTURE SCOPE SECTION

The application should include a small "Future Scope" section/documentation explaining that the prototype can later be extended with:

- vLLM
- NVIDIA Triton
- Kubernetes
- GPU autoscaling
- MLflow
- Advanced quantization
- Redis
- Semantic caching
- ML-based routing
- Load-aware routing
- Distributed inference
- Cloud deployment

IMPORTANT:

These should be documented as future improvements, NOT required for this college implementation.

---

# 32. DOCUMENTATION

Create a good README.md containing:

1. Project introduction
2. Problem statement
3. Objectives
4. Features
5. Technology stack
6. Architecture
7. Installation
8. Running the project
9. Demo Mode
10. API configuration
11. Database
12. Routing algorithm
13. Cost calculation
14. Screenshots/placeholders
15. Testing
16. Future scope
17. Limitations

---

# 33. ACADEMIC DOCUMENTATION

Also create:

```text
docs/
├── architecture.md
├── routing-algorithm.md
├── database.md
├── api.md
├── testing.md
└── future-scope.md
```

Keep these concise and understandable for a college student.

---

# 34. ARCHITECTURE DIAGRAM

Create a simple architecture diagram in documentation:

```text
User
 ↓
Frontend
 ↓
FastAPI
 ↓
Request Analyzer
 ↓
AI Router
 ↓
Model Registry
 ↓
AI Provider
 ↓
Response
 ↓
Metrics + SQLite
 ↓
Dashboard
```

Do not create a complicated distributed architecture diagram.

---

# 35. ERROR HANDLING

Handle:

- Empty question
- API failure
- Invalid configuration
- Database failure
- Provider timeout
- Unknown model
- Invalid request

Display user-friendly errors.

Never expose Python stack traces to the normal user interface.

---

# 36. SECURITY BASICS

For a college project implement basic security practices:

- Never hard-code API keys.
- Use `.env`.
- Add `.env` to `.gitignore`.
- Validate input.
- Limit excessively large user input.
- Do not store API keys in database.
- Do not claim the project is production secure.

---

# 37. PERFORMANCE REQUIREMENT

The project should work comfortably on a normal laptop in Demo Mode.

Target:

- Application startup within a few seconds.
- Normal page response within a few seconds.
- Dashboard loads quickly.
- No GPU required.
- No Kubernetes required.

---

# 38. DO NOT USE FAKE HARD-CODED DASHBOARD RESULTS

The dashboard must calculate statistics from actual stored requests.

It is acceptable for model cost/quality configuration to use demo values.

It is NOT acceptable to hard-code:

```text
Total requests = 125
Savings = 60%
```

The numbers must be generated from database records.

---

# 39. DO NOT OVERCOMPLICATE THE ROUTER

The router should be:

- Explainable
- Deterministic
- Easy to modify
- Easy to demonstrate

Do not train a complex ML model unless it is genuinely necessary.

A rule + scoring based router is sufficient for this project.

---

# 40. ACCEPTANCE CRITERIA

The project is considered complete only when:

### Application

- [ ] Application starts locally.
- [ ] Home page works.
- [ ] User can enter a question.
- [ ] Request is analyzed.
- [ ] Complexity is calculated.
- [ ] Privacy level is calculated.
- [ ] Model is selected.
- [ ] Response is generated.
- [ ] Latency is measured.
- [ ] Estimated cost is calculated.
- [ ] Estimated savings is calculated.
- [ ] Result is saved to SQLite.

### Cache

- [ ] First identical request produces cache MISS.
- [ ] Repeated request produces cache HIT.
- [ ] Cache statistics appear on dashboard.

### Dashboard

- [ ] Total request count works.
- [ ] Model usage works.
- [ ] Average latency works.
- [ ] Estimated cost works.
- [ ] Estimated savings works.
- [ ] Cache hit rate works.
- [ ] Charts use real database data.

### Comparison

- [ ] User can compare Small/Medium/Large models.
- [ ] Cost/quality/latency values are displayed.
- [ ] Recommended model is highlighted.

### Demo

- [ ] Project works without API key.
- [ ] Project works without GPU.
- [ ] Project works without Kubernetes.
- [ ] Demo Mode is clearly visible.

### Code

- [ ] Code is organized.
- [ ] No API keys are hard-coded.
- [ ] Basic tests are included.
- [ ] README is included.
- [ ] `.env.example` is included.

---

# 41. DEVELOPMENT ORDER

Build the project in this order.

## Phase 1

Create:

- Project structure
- FastAPI application
- SQLite database
- Basic frontend

## Phase 2

Implement:

- Model registry
- Request analyzer
- Complexity scoring
- Privacy detection

## Phase 3

Implement:

- Router
- Cost calculation
- Routing explanation

## Phase 4

Implement:

- Demo AI provider
- Optional API provider
- Latency measurement

## Phase 5

Implement:

- SQLite request logging
- Cache

## Phase 6

Implement:

- Dashboard
- Charts
- Request history

## Phase 7

Implement:

- Model comparison

## Phase 8

Implement:

- Tests
- Error handling
- Documentation
- UI cleanup

---

# 42. FINAL DEMO FLOW

The final presentation should be possible in approximately 5–10 minutes.

### Demo 1

Enter:

```text
What is RAM?
```

Show:

```text
Complexity: LOW
Selected: Small Model
Low cost
Low latency
```

### Demo 2

Enter:

```text
Write a Java program for binary search and explain the algorithm.
```

Show:

```text
Complexity: MEDIUM
Selected: Medium Model
```

### Demo 3

Enter a complex architecture/reasoning question.

Show:

```text
Complexity: HIGH
Selected: Large Model
```

### Demo 4

Repeat the same question.

Show:

```text
Cache HIT
```

### Demo 5

Open Model Comparison.

Show:

```text
Small vs Medium vs Large

Cost
Latency
Quality

Recommended model
```

### Demo 6

Open Dashboard.

Show:

```text
Total Requests
Model Distribution
Average Latency
Cost
Savings
Cache Hit Rate
```

---

# 43. VIVA EXPLANATION

The student should be able to explain the project simply:

> "Our project implements an AI inference routing layer. Instead of sending every request to the most expensive model, our system analyzes the request complexity and selects an appropriate model. Simple requests are sent to a smaller and cheaper model, while complex requests are routed to stronger models. We measure latency and estimated cost and store these metrics for analytics. We also implement basic caching to avoid processing identical requests repeatedly. The prototype demonstrates how intelligent routing can reduce inference cost while maintaining suitable response quality."

---

# 44. EXPECTED PROJECT RESULT

The final application should demonstrate:

```text
                    AI REQUEST
                        ↓
                Request Analysis
                        ↓
             Complexity + Privacy
                        ↓
                Intelligent Router
                        ↓
       ┌────────────────────────────┐
       │                            │
       ↓                            ↓
   Cheap/Fast                   Powerful
   Model                         Model
       │                            │
       └──────────────┬─────────────┘
                      ↓
                   Response
                      ↓
              Metrics + Cache
                      ↓
                  Dashboard
```

The main achievement is demonstrating:

**Cost awareness + Performance awareness + Basic intelligent model selection.**

---

# 45. FINAL INSTRUCTION TO THE DEVELOPMENT AI

When implementing this project:

1. Prioritize functionality over complexity.
2. Keep the project college-level.
3. Do not add technologies just because they appear in the original research description.
4. Do not introduce unnecessary dependencies.
5. Do not require GPU hardware.
6. Do not require Kubernetes.
7. Do not require cloud infrastructure.
8. Do not require a paid API.
9. Demo Mode must always work.
10. Keep the routing algorithm explainable.
11. Keep the UI simple and professional.
12. Use real database data for analytics.
13. Clearly distinguish estimated/demo metrics from real measurements.
14. Write clean, readable Python.
15. Add comments only where they help understanding.
16. Do not generate unnecessary enterprise architecture.
17. Do not implement features outside this specification unless they are required for the application to function.
18. If there is a choice between a complicated implementation and a simple implementation that demonstrates the same concept, choose the simple implementation.
19. Before considering the project complete, verify every acceptance criterion above.
20. Make sure a student can explain every major component during a college viva.

**The final product should be a simple, functional, demonstrable prototype of an intelligent AI inference router — NOT a production-grade AI infrastructure platform.**
