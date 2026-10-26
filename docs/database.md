# SQLite Database Schema Design

The application utilizes an embedded SQLite database (`data/tess_router.db`) configured with zero external dependencies.

## Table: `requests`
Logs every inference query processed by the gateway.
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Unique auto-incrementing ID |
| `question` | TEXT | User prompt text |
| `response` | TEXT | Model generated answer |
| `task_type` | TEXT | Domain (Coding, Math, etc.) |
| `complexity_score` | REAL | Continuous score (0.0 – 1.0) |
| `complexity_level` | TEXT | Categorical tier (LOW, MEDIUM, HIGH) |
| `privacy_level` | TEXT | PUBLIC or SENSITIVE |
| `selected_model` | TEXT | Model ID ('small', 'medium', 'large') |
| `latency_ms` | REAL | Total execution time in ms |
| `estimated_cost` | REAL | Cost incurred (₹ INR) |
| `baseline_cost` | REAL | Cost if Large Model was used (₹0.08) |
| `estimated_saving`| REAL | Net savings (₹ INR) |
| `cache_hit` | INTEGER | 1 if served from cache, 0 otherwise |
| `routing_reason` | TEXT | Human-readable explanation |
| `created_at` | TIMESTAMP | Timestamp of request execution |

## Table: `models`
Maintains registered model configurations.
| Column | Type | Description |
|---|---|---|
| `id` | TEXT PRIMARY KEY | 'small', 'medium', 'large' |
| `name` | TEXT | 'Small Model', etc. |
| `tier` | TEXT | Tier classification |
| `description` | TEXT | Model role & specification |
| `estimated_cost` | REAL | Per-request cost in INR |
| `expected_quality`| INTEGER | Normalized quality score (0–100) |
| `expected_latency`| REAL | Typical SLA in seconds |
| `available` | INTEGER | Availability flag (1 or 0) |

## Table: `cache`
Accelerated query lookup table.
| Column | Type | Description |
|---|---|---|
| `question_hash` | TEXT PRIMARY KEY | SHA-256 hash of normalized text |
| `question` | TEXT | Original prompt text |
| `response` | TEXT | Cached output string |
| `model` | TEXT | Model that generated response |
| `created_at` | TIMESTAMP | Cache insertion time |
