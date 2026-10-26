# Testing Documentation

## Test Suites Overview
The project contains 4 focused unit and integration test scripts:

1. **`tests/test_analyzer.py`**:
   - Tests Low complexity categorization (`"What is RAM?"`).
   - Tests Medium complexity categorization (`"Write a Java program to implement binary search and explain its time complexity."`).
   - Tests High complexity categorization (`"Analyze a distributed application architecture and identify possible performance and concurrency problems."`).
   - Tests Privacy keyword detection (`"Aadhaar 4589-1234-8765"` -> `SENSITIVE`).

2. **`tests/test_router.py`**:
   - Verifies LOW routes to `Small Model`.
   - Verifies MEDIUM routes to `Medium Model`.
   - Verifies HIGH routes to `Large Model`.
   - Verifies SENSITIVE triggers local security policy routing.

3. **`tests/test_cost.py`**:
   - Verifies savings equations against Large model baseline (₹0.08).
   - Validates small model savings: ₹0.07 (87.5%).
   - Validates medium model savings: ₹0.05 (62.5%).

4. **`tests/test_api.py`**:
   - Integration testing of `/api/health`, `/api/models`, `/api/analyze`, `/api/generate`, `/api/compare`, and `/api/dashboard/stats`.
   - Validates first request produces `Cache: MISS` and repeat request produces `Cache: HIT` (cost ₹0.00).

## Execution
Run all test suites via PowerShell:
```powershell
python tests/test_analyzer.py
python tests/test_router.py
python tests/test_cost.py
python tests/test_api.py
```
All tests execute synchronously in under 3 seconds.
