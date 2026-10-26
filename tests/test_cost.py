import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.cost import calculate_cost_and_savings

def test_small_cost():
    res = calculate_cost_and_savings(0.01)
    assert res["estimated_cost"] == 0.01
    assert res["baseline_cost"] == 0.08
    assert round(res["estimated_saving"], 2) == 0.07
    assert res["estimated_saving_pct"] == 87.5

def test_medium_cost():
    res = calculate_cost_and_savings(0.03)
    assert res["estimated_cost"] == 0.03
    assert res["baseline_cost"] == 0.08
    assert round(res["estimated_saving"], 2) == 0.05
    assert res["estimated_saving_pct"] == 62.5

def test_large_cost():
    res = calculate_cost_and_savings(0.08)
    assert res["estimated_cost"] == 0.08
    assert res["baseline_cost"] == 0.08
    assert res["estimated_saving"] == 0.0
    assert res["estimated_saving_pct"] == 0.0

if __name__ == "__main__":
    test_small_cost()
    test_medium_cost()
    test_large_cost()
    print("All cost tests passed successfully!")
