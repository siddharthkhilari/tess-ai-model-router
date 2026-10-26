"""
Privacy detection service (need.md Section 11).
Demonstration-level privacy detector for identifying sensitive keywords and PII.
"""

import re
from typing import Dict, Any, List

SENSITIVE_PATTERNS = [
    (r"\baadhaar\b", "Aadhaar Card identifier"),
    (r"\bpan\b", "PAN Card identifier"),
    (r"\bpassport\b", "Passport identifier"),
    (r"\bcredit\s*card\b", "Credit Card information"),
    (r"\bdebit\s*card\b", "Debit Card information"),
    (r"\bcvv\b", "Card verification value"),
    (r"\bpassword\b", "Authentication password"),
    (r"\bconfidential\b", "Confidential enterprise indicator"),
    (r"\bprivate\b", "Private data marker"),
    (r"\bsecret\b", "Secret token/credential"),
    (r"\bmedical\s*record\b", "Protected Health Information (PHI)"),
    (r"\bpatient\b", "Patient medical context"),
    (r"\bbiopsy\b", "Pathological diagnostic report"),
    (r"\bsalary\b", "Confidential compensation details"),
    (r"\bpayroll\b", "Internal financial record"),
    (r"\bapi\s*key\b", "API credential secret")
]

def check_privacy(text: str) -> Dict[str, Any]:
    """Scans input prompt for sensitive patterns and returns privacy status."""
    text_lower = text.lower()
    detected = []

    for pattern, desc in SENSITIVE_PATTERNS:
        if re.search(pattern, text_lower):
            detected.append(desc)

    if detected:
        return {
            "level": "SENSITIVE",
            "matched_keywords": list(set(detected)),
            "routing_note": "Prefer local/demo processing to avoid third-party API data exposure."
        }
    return {
        "level": "PUBLIC",
        "matched_keywords": [],
        "routing_note": "Public request; safe for standard cloud or local routing."
    }
