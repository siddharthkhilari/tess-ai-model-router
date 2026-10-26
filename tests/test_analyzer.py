import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.analyzer import analyze_prompt

def test_simple_queries():
    res1 = analyze_prompt("Hello")
    assert res1["complexity_level"] == "LOW"
    assert res1["score"] <= 35

    res2 = analyze_prompt("What is a firewall?")
    assert res2["complexity_level"] == "LOW"
    assert res2["score"] <= 35

    res3 = analyze_prompt("What is TCP?")
    assert res3["complexity_level"] == "LOW"
    assert res3["score"] <= 35

def test_medium_queries():
    # User test case:
    res1 = analyze_prompt("write java code to print fibonacci series")
    assert res1["complexity_level"] == "MEDIUM"
    assert 36 <= res1["score"] <= 65

    # Comparative explanation test case:
    res2 = analyze_prompt("Explain how a firewall works and compare stateful and stateless firewalls.")
    assert res2["complexity_level"] == "MEDIUM"
    assert 36 <= res2["score"] <= 65

    res3 = analyze_prompt("Explain TCP and UDP and compare their differences.")
    assert res3["complexity_level"] == "MEDIUM"
    assert 36 <= res3["score"] <= 65

def test_high_queries():
    prompt = (
        "Design a secure distributed authentication architecture for a banking system, "
        "compare OAuth2, OIDC and SAML, identify vulnerabilities, and propose mitigation strategies."
    )
    res = analyze_prompt(prompt)
    assert res["complexity_level"] == "HIGH"
    assert res["score"] >= 66

def test_empty_query():
    res = analyze_prompt("   ")
    assert "error" in res

if __name__ == "__main__":
    test_simple_queries()
    test_medium_queries()
    test_high_queries()
    test_empty_query()
    print("All analyzer tests passed successfully!")
