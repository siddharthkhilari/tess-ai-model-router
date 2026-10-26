"""
AI Inference Router Model.
Implements:
1. Explainable Rule-and-Scoring Based Router (per need.md Section 10-14, 39)
2. Machine Learning Baseline Classifier (TF-IDF + Random Forest / Logistic Regression)
3. Model evaluation, accuracy, F1-score, and persistent model serialization.
"""

import os
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# =====================================================================
# 1. MODEL REGISTRY DEFINITIONS (need.md Section 7, 15)
# =====================================================================
MODEL_REGISTRY = {
    "small": {
        "id": "small",
        "name": "Small Model",
        "tier": "small",
        "description": "Fast, lightweight SLM suitable for simple questions & definitions.",
        "estimated_cost": 0.01,
        "expected_quality": 75,
        "expected_latency": 1.0,
        "available": True
    },
    "medium": {
        "id": "medium",
        "name": "Medium Model",
        "tier": "medium",
        "description": "Balanced model for intermediate code snippets & explanations.",
        "estimated_cost": 0.03,
        "expected_quality": 85,
        "expected_latency": 2.0,
        "available": True
    },
    "large": {
        "id": "large",
        "name": "Large Model",
        "tier": "large",
        "description": "Frontier reasoning model for complex systems architecture & math.",
        "estimated_cost": 0.08,
        "expected_quality": 95,
        "expected_latency": 4.0,
        "available": True
    }
}

# =====================================================================
# 2. PRIVACY DETECTOR (need.md Section 11)
# =====================================================================
SENSITIVE_KEYWORDS = [
    r"\baadhaar\b", r"\bpan\b", r"\bpassport\b", r"\bcredit\s*card\b",
    r"\bdebit\s*card\b", r"\bpassword\b", r"\bconfidential\b",
    r"\bprivate\b", r"\bsecret\b", r"\bmedical\s*record\b",
    r"\bpatient\b", r"\bbiopsy\b", r"\bsalary\b", r"\bpayroll\b",
    r"\bcvv\b", r"\btoken\b", r"\bapi\s*key\b"
]

def detect_privacy(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    matched = []
    for pattern in SENSITIVE_KEYWORDS:
        if re.search(pattern, prompt_lower):
            matched.append(pattern.replace(r"\b", "").replace(r"\s*", " "))

    if matched:
        return {
            "level": "SENSITIVE",
            "matched_keywords": matched,
            "routing_note": "Prefer local/demo processing to avoid external API exposure."
        }
    return {
        "level": "PUBLIC",
        "matched_keywords": [],
        "routing_note": "Public request; safe for standard cloud/local routing."
    }

# =====================================================================
# 3. REQUEST ANALYZER & COMPLEXITY SCORING (need.md Section 9, 10)
# =====================================================================
CODING_KEYWORDS = ["write", "code", "implement", "function", "program", "class", "algorithm", "java", "python", "c++", "rust", "sql", "bug", "syntax"]
REASONING_KEYWORDS = ["analyze", "evaluate", "compare", "trade-off", "prove", "derive", "architecture", "distributed", "concurrency", "threat model", "optimize", "consensus"]
MATH_KEYWORDS = ["solve", "equation", "matrix", "eigenvalue", "recurrence", "theorem", "induction", "proof", "gradient"]

def analyze_request(prompt: str) -> dict:
    words = prompt.split()
    word_count = len(words)
    char_count = len(prompt)
    prompt_lower = prompt.lower()

    # Determine Task Type
    if any(re.search(rf"\b{k}\b", prompt_lower) for k in MATH_KEYWORDS):
        task_type = "Mathematics"
    elif any(re.search(rf"\b{k}\b", prompt_lower) for k in CODING_KEYWORDS):
        task_type = "Coding"
    elif any(re.search(rf"\b{k}\b", prompt_lower) for k in REASONING_KEYWORDS):
        task_type = "Reasoning & Architecture"
    elif prompt_lower.startswith("explain") or "how does" in prompt_lower or "difference between" in prompt_lower:
        task_type = "Explanation"
    else:
        task_type = "General Question"

    # Explainable Scoring (need.md Section 10)
    score_points = 0
    reasons = []

    if word_count > 50:
        score_points += 1
        reasons.append("Prompt word count > 50 words")
    if word_count > 150:
        score_points += 1
        reasons.append("Prompt word count > 150 words (long-form input)")

    if any(k in prompt_lower for k in ["implement", "concurrent", "thread-safe", "distributed", "consensus"]):
        score_points += 2
        reasons.append("Advanced system-level coding/architecture keywords detected")
    elif any(k in prompt_lower for k in CODING_KEYWORDS):
        score_points += 1
        reasons.append("Coding requirements detected")

    if any(k in prompt_lower for k in REASONING_KEYWORDS):
        score_points += 1
        reasons.append("Analytical or multi-step reasoning keywords detected")

    if any(k in prompt_lower for k in ["and also", "step by step", "multiple", "pros and cons", "compare and contrast"]):
        score_points += 1
        reasons.append("Multiple compound requirements detected")

    if any(k in prompt_lower for k in ["comprehensive", "in detail", "detailed explanation"]):
        score_points += 1
        reasons.append("Detailed long-form generation requested")

    # Normalize to 0.0 - 1.0 (max points ~ 7)
    complexity_score = min(1.0, round(score_points / 7.0, 2))
    # Give a base score for general queries so 0.0 isn't zero
    if complexity_score < 0.15:
        complexity_score = 0.15

    # Classification thresholds (need.md Section 10)
    if complexity_score < 0.40:
        complexity_level = "LOW"
    elif complexity_score < 0.70:
        complexity_level = "MEDIUM"
    else:
        complexity_level = "HIGH"

    privacy = detect_privacy(prompt)

    return {
        "word_count": word_count,
        "char_count": char_count,
        "task_type": task_type,
        "complexity_score": complexity_score,
        "complexity_level": complexity_level,
        "privacy": privacy,
        "reasons": reasons if reasons else ["Basic factual or definitional lookup"]
    }

# =====================================================================
# 4. EXPLAINABLE MULTI-OBJECTIVE ROUTER (need.md Section 12, 13, 14)
# =====================================================================
def route_request(
    analysis: dict,
    quality_weight: float = 0.50,
    cost_weight: float = 0.30,
    latency_weight: float = 0.20
) -> dict:
    privacy_info = analysis["privacy"]
    comp_level = analysis["complexity_level"]
    comp_score = analysis["complexity_score"]

    # 1. Privacy Constraint Check
    if privacy_info["level"] == "SENSITIVE":
        selected_model = MODEL_REGISTRY["small"]
        return {
            "selected_model_id": selected_model["id"],
            "selected_model_name": selected_model["name"],
            "tier": selected_model["tier"],
            "reasons": [
                "Privacy constraint: SENSITIVE data detected",
                privacy_info["routing_note"],
                "Routed to local/demo tier to prevent data leakage"
            ],
            "decision_type": "Privacy Policy Override"
        }

    # 2. Multi-Objective Scoring across Model Registry
    # Normalize metrics to 0.0-1.0 scale
    # Quality: 75->0.75, 85->0.85, 95->0.95
    # Cost: 0.01->0.125, 0.03->0.375, 0.08->1.00 (divided by 0.08)
    # Latency: 1.0->0.25, 2.0->0.50, 4.0->1.00 (divided by 4.0)
    scores = {}
    for m_id, model in MODEL_REGISTRY.items():
        norm_q = model["expected_quality"] / 100.0
        norm_c = model["estimated_cost"] / 0.08
        norm_l = model["expected_latency"] / 4.0

        # Penalty if model quality is lower than required complexity
        req_quality = comp_score
        quality_penalty = max(0.0, (req_quality - norm_q) * 2.0)

        model_score = (quality_weight * norm_q) - (cost_weight * norm_c) - (latency_weight * norm_l) - quality_penalty
        scores[m_id] = model_score

    # 3. Fallback explainable rule (need.md Section 13)
    if comp_level == "LOW":
        chosen_id = "small"
        routing_reasons = [
            "Request complexity is LOW",
            "High model capacity is not required for this query",
            f"Small model offers minimal estimated cost (₹{MODEL_REGISTRY['small']['estimated_cost']})",
            f"Small model delivers lowest expected latency ({MODEL_REGISTRY['small']['expected_latency']}s)"
        ]
    elif comp_level == "MEDIUM":
        chosen_id = "medium"
        routing_reasons = [
            "Request complexity is MEDIUM (coding/explanation)",
            "Medium model provides balanced reasoning capacity",
            f"Saves ~62.5% cost compared to Large Model",
            f"Expected latency ({MODEL_REGISTRY['medium']['expected_latency']}s) meets typical SLA"
        ]
    else:
        chosen_id = "large"
        routing_reasons = [
            "Request complexity is HIGH (deep analysis, system design, or math)",
            "Strong multi-step reasoning capabilities required",
            "Higher cost is justified for required accuracy and output fidelity",
            f"Estimated latency ({MODEL_REGISTRY['large']['expected_latency']}s) within acceptable limits"
        ]

    selected_model = MODEL_REGISTRY[chosen_id]

    return {
        "selected_model_id": selected_model["id"],
        "selected_model_name": selected_model["name"],
        "tier": selected_model["tier"],
        "reasons": routing_reasons,
        "decision_type": "Multi-Objective Rule & Utility Optimization",
        "utility_scores": {k: round(v, 3) for k, v in scores.items()}
    }

# =====================================================================
# 5. MACHINE LEARNING ROUTER TRAINING & EVALUATION (RESEARCH BASELINE)
# =====================================================================
MODEL_SAVE_PATH = "router_model.pkl"

def train_ml_router(dataset_path: str = "dataset/inference_routing_dataset.csv"):
    if not os.path.exists(dataset_path):
        print(f"Dataset {dataset_path} not found. Generate it first.")
        return None

    df = pd.read_csv(dataset_path)
    X = df["prompt"]
    y = df["routed_model"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n=======================================================")
    print("      MACHINE LEARNING ROUTER EVALUATION RESULTS       ")
    print("=======================================================")
    print(f"Accuracy on Test Set (25% split): {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)
    print("=======================================================\n")

    pipeline = {
        "vectorizer": vectorizer,
        "classifier": clf,
        "classes": clf.classes_.tolist()
    }
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"Saved trained ML router artifact to: {MODEL_SAVE_PATH}")
    return pipeline

def predict_ml(prompt: str) -> dict:
    if not os.path.exists(MODEL_SAVE_PATH):
        train_ml_router()

    pipeline = joblib.load(MODEL_SAVE_PATH)
    vec = pipeline["vectorizer"].transform([prompt])
    pred = pipeline["classifier"].predict(vec)[0]
    probs = pipeline["classifier"].predict_proba(vec)[0]

    prob_dict = {cls: round(float(p), 3) for cls, p in zip(pipeline["classes"], probs)}
    return {
        "predicted_model": pred,
        "probabilities": prob_dict
    }

# =====================================================================
# 6. STANDALONE DEMONSTRATION & TEST RUNNER
# =====================================================================
if __name__ == "__main__":
    print("Training ML Router Baseline...")
    train_ml_router()

    print("\nTesting Router on Sample Questions from need.md Section 28:")
    test_queries = [
        "What is RAM?",
        "What is inheritance in Java?",
        "Write a Java program to implement binary search and explain its time complexity.",
        "Analyze a distributed application architecture and identify possible performance and concurrency problems.",
        "Analyze this confidential employee record: Aadhaar 4589-1234-8765."
    ]

    for q in test_queries:
        analysis = analyze_request(q)
        decision = route_request(analysis)
        ml_pred = predict_ml(q)
        print(f"\nQuery: '{q}'")
        print(f"  -> Task: {analysis['task_type']} | Comp: {analysis['complexity_level']} ({analysis['complexity_score']}) | Privacy: {analysis['privacy']['level']}")
        print(f"  -> Rule Router: {decision['selected_model_name']} ({decision['decision_type']})")
        print(f"  -> ML Router Prediction: {ml_pred['predicted_model']} (Confidence: {ml_pred['probabilities'].get(ml_pred['predicted_model'])})")
        print(f"  -> Reasons: {decision['reasons'][0]}")
