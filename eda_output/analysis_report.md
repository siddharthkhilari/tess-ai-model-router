# AI Inference Routing Dataset Analysis Report

## 1. Overview
- **Total Requests Evaluated:** 325
- **Categories Covered:** 7
- **Overall Cost Savings:** **54.35%** (₹14.13 saved vs ₹26.00 baseline)
- **Average Latency Reduction:** **45.72%** (2.17s vs 4.00s baseline)

## 2. Category Breakdown
| Category | Request Count | Percentage |
|---|---:|---:|
| General Question | 82 | 25.2% |
| Explanation | 58 | 17.8% |
| Coding - Basic | 50 | 15.4% |
| Coding - Complex | 41 | 12.6% |
| Sensitive & Privacy | 36 | 11.1% |
| Reasoning & Architecture | 32 | 9.8% |
| Mathematics & Algorithms | 26 | 8.0% |

## 3. Model Routing Distribution
| Model Tier | Cost / Req | Avg Latency | Requests Routed | Share (%) |
|---|---:|---:|---:|---:|
| Small Model | ₹0.01 | 1.01s | 129 | 39.7% |
| Medium Model | ₹0.03 | 2.01s | 102 | 31.4% |
| Large Model | ₹0.08 | 4.02s | 94 | 28.9% |

## 4. Key Takeaways
1. **Majority Offloading:** Over 75% of queries do not require a heavy Large Model and are served with Small or Medium models.
2. **Cost Efficiency:** Offloading simple and moderate queries drives a **54.35%** reduction in inference compute budget.
3. **Response Speed:** Users experience a **45.72%** speedup in average response times.
4. **Privacy Protection:** All sensitive queries (Aadhaar, medical, credentials) are trapped and routed locally to Small Model per policy.
