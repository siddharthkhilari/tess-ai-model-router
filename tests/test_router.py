import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import init_db
from app.services.analyzer import analyze_prompt
from app.services.router import route_request

init_db()

def test_routing_low():
    analysis = analyze_prompt("What is RAM?")
    decision = route_request(analysis)
    assert decision["selected_model"] == "small"
    assert "LOW" in decision["reasons"][0]

def test_routing_medium():
    analysis = analyze_prompt("Write a Java program to implement binary search and explain its time complexity.")
    decision = route_request(analysis)
    assert decision["selected_model"] == "medium"
    assert "MEDIUM" in decision["reasons"][0]

def test_routing_high():
    analysis = analyze_prompt("Analyze a distributed application architecture and identify possible performance and concurrency problems.")
    decision = route_request(analysis)
    assert decision["selected_model"] == "large"
    assert "HIGH" in decision["reasons"][0]

def test_routing_sensitive():
    analysis = analyze_prompt("Analyze this confidential employee record: Aadhaar 4589-1234-8765.")
    decision = route_request(analysis)
    # Sensitive should route to small/local
    assert decision["selected_model"] == "small"
    assert decision["decision_type"] == "Privacy Policy Constraint"

if __name__ == "__main__":
    test_routing_low()
    test_routing_medium()
    test_routing_high()
    test_routing_sensitive()
    print("All router tests passed successfully!")
