"""
Deterministic Rule-Based Prompt Complexity Analyzer.
Analyzes prompt length, instruction counts, reasoning depth, technical keywords,
and implementation requirements to produce an explainable score (0-100) and
classification: LOW (0-35), MEDIUM (36-65), HIGH (66-100).
"""

import re
from typing import Dict, Any, List

# B. Action / Instruction Keywords (0-20 pts)
INSTRUCTION_KEYWORDS = [
    r"\bexplain\b", r"\bcompare\b", r"\banalyze\b", r"\banalyse\b",
    r"\bdesign\b", r"\bimplement\b", r"\blist\b", r"\bevaluate\b",
    r"\bdescribe\b", r"\bdevelop\b", r"\bcreate\b", r"\bwrite\b",
    r"\bbuild\b", r"\bderive\b", r"\bprove\b", r"\bsolve\b",
    r"\bdiscuss\b", r"\bidentify\b", r"\bpropose\b", r"\boptimize\b",
    r"\bdebug\b", r"\brefactor\b", r"\bcontrast\b"
]

# C. Reasoning-Oriented Keywords & Phrases (0-25 pts)
REASONING_PATTERNS = [
    r"\banalyz(e|is)\b", r"\banalys(e|is)\b", r"\bcompare\b", r"\bevaluate\b",
    r"\bwhy\b", r"\bhow\b", r"\btrade-?offs?\b", r"\bpros and cons\b",
    r"\badvantages and disadvantages\b", r"\bcritically evaluate\b",
    r"\bjustify\b", r"\breason(ing)?\b", r"\bexplain why\b",
    r"\bmitigation strategies\b", r"\bvulnerabilit(y|ies)\b",
    r"\bconcurrency\b", r"\bdeadlock\b", r"\brace condition\b",
    r"\bcap theorem\b", r"\bscalabilit(y|ies)\b", r"\bfault-?tolerant\b"
]

# D. Technical Complexity Keywords (0-20 pts)
TECHNICAL_KEYWORDS = [
    r"\barchitecture\b", r"\balgorithm\b", r"\bdistributed\b", r"\bsecurity\b",
    r"\bcryptography\b", r"\bdatabase\b", r"\bapi\b", r"\bauthentication\b",
    r"\bauthorization\b", r"\boptimization\b", r"\bmachine learning\b",
    r"\bdeep learning\b", r"\bnetwork\b", r"\bcybersecurity\b", r"\bblockchain\b",
    r"\bmicroservices\b", r"\bscalability\b", r"\bperformance\b", r"\boauth2?\b",
    r"\boidc\b", r"\bsaml\b", r"\btcp\b", r"\budp\b", r"\bhttp\b", r"\bhttps\b",
    r"\bdns\b", r"\boperating system\b", r"\bkernel\b", r"\bfirewall\b",
    r"\bcache\b", r"\bindexing\b", r"\bconsensus\b", r"\braft\b", r"\bpaxos\b",
    r"\bfibonacci\b", r"\bbinary search\b", r"\bquicksort\b", r"\btree\b",
    r"\bgraph\b", r"\bvector\b", r"\bmatrix\b"
]

# F. Code / Implementation Keywords (0-15 pts)
CODE_KEYWORDS = [
    r"\bcode\b", r"\bprogram\b", r"\bfunction\b", r"\bclass\b", r"\bscript\b",
    r"\bjava\b", r"\bpython\b", r"\bjavascript\b", r"\bc\+\+\b", r"\bc#\b",
    r"\brust\b", r"\bgolang\b", r"\bgo\b", r"\bsql\b", r"\bhtml\b", r"\bcss\b",
    r"\bprint\b", r"\bmethod\b", r"\bsyntax\b", r"\bbug\b", r"\brecursion\b"
]

def analyze_prompt(prompt: str) -> Dict[str, Any]:
    text = prompt.strip()
    if not text:
        return {
            "error": "Please enter a prompt.",
            "complexity_level": "INVALID",
            "score": 0
        }

    prompt_lower = text.lower()
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    # Sentence count approximated by punctuation or newline
    sentences = [s.strip() for s in re.split(r"[.!?\n]+", text) if s.strip()]
    sentence_count = max(1, len(sentences))

    reasons = []

    # -------------------------------------------------------------
    # 1. Prompt Length Score (0–20 points)
    # -------------------------------------------------------------
    # Short: < 10 words -> 3-8 pts
    # Medium: 10 - 30 words -> 9-15 pts
    # Long: > 30 words -> 16-20 pts
    if word_count <= 4:
        length_score = 4
    elif word_count <= 10:
        length_score = 8
    elif word_count <= 25:
        length_score = 14
        reasons.append(f"Moderate prompt length ({word_count} words)")
    elif word_count <= 50:
        length_score = 18
        reasons.append(f"Substantial prompt length ({word_count} words, {sentence_count} sentences)")
    else:
        length_score = 20
        reasons.append(f"Long multi-sentence prompt ({word_count} words, {sentence_count} sentences)")

    # -------------------------------------------------------------
    # 2. Instructions Score (0–20 points)
    # -------------------------------------------------------------
    matched_instructions = []
    for pattern in INSTRUCTION_KEYWORDS:
        found = re.findall(pattern, prompt_lower)
        if found:
            matched_instructions.extend(found)

    unique_instructions = list(set(matched_instructions))
    instr_count = len(unique_instructions)

    if instr_count == 0:
        instruction_score = 4  # Implicit question
    elif instr_count == 1:
        instruction_score = 10
        reasons.append(f"Single instruction detected: '{unique_instructions[0].capitalize()}'")
    elif instr_count == 2:
        instruction_score = 16
        reasons.append(f"Multiple instructions detected: {', '.join(k.capitalize() for k in unique_instructions)}")
    else:
        instruction_score = 20
        reasons.append(f"Complex compound instructions ({instr_count} directives: {', '.join(k.capitalize() for k in unique_instructions[:4])})")

    # -------------------------------------------------------------
    # 3. Reasoning Score (0–25 points)
    # -------------------------------------------------------------
    matched_reasoning = []
    for pattern in REASONING_PATTERNS:
        found = re.findall(pattern, prompt_lower)
        if found:
            matched_reasoning.append(pattern.replace(r"\b", "").replace("?", ""))

    unique_reasoning = list(set(matched_reasoning))
    reason_count = len(unique_reasoning)

    if reason_count == 0:
        reasoning_score = 0
    elif reason_count == 1:
        reasoning_score = 10
        reasons.append(f"Analytical reasoning required: '{unique_reasoning[0]}'")
    elif reason_count == 2:
        reasoning_score = 18
        reasons.append(f"Multi-step comparison/reasoning required: {', '.join(unique_reasoning)}")
    else:
        reasoning_score = 25
        reasons.append(f"Deep architectural / critical evaluation: {', '.join(unique_reasoning[:3])}")

    # -------------------------------------------------------------
    # 4. Technical Content Score (0–20 points)
    # -------------------------------------------------------------
    matched_tech = []
    for pattern in TECHNICAL_KEYWORDS:
        found = re.findall(pattern, prompt_lower)
        if found:
            matched_tech.extend(found)

    unique_tech = list(set(matched_tech))
    tech_count = len(unique_tech)

    if tech_count == 0:
        tech_score = 0
    elif tech_count == 1:
        tech_score = 8
        reasons.append(f"Technical concept: '{unique_tech[0]}'")
    elif tech_count == 2:
        tech_score = 14
        reasons.append(f"Multiple technical concepts: {', '.join(unique_tech)}")
    else:
        tech_score = 20
        reasons.append(f"Advanced domain technical terminology ({tech_count} concepts: {', '.join(unique_tech[:4])})")

    # -------------------------------------------------------------
    # 5. Code / Implementation & Task Complexity (0–15 points)
    # -------------------------------------------------------------
    matched_code = []
    for pattern in CODE_KEYWORDS:
        found = re.findall(pattern, prompt_lower)
        if found:
            matched_code.extend(found)

    unique_code = list(set(matched_code))
    code_count = len(unique_code)

    task_score = 0
    if code_count > 0:
        if code_count == 1:
            task_score += 8
            reasons.append(f"Code / implementation indicator: '{unique_code[0]}'")
        elif code_count >= 2:
            task_score += 12
            reasons.append(f"Programming & code generation request ({', '.join(unique_code[:3])})")

    # Multiple requirements detection (clauses with 'and', 'also', multiple commas)
    if ("," in text and (" and " in prompt_lower or "also" in prompt_lower)) or len(unique_instructions) >= 2:
        task_score = min(15, task_score + 5)
        if "Multiple compound requirements" not in str(reasons):
            reasons.append("Multiple separate requirements identified in prompt")

    task_score = min(15, task_score)

    # -------------------------------------------------------------
    # Total Score (0–100) & Classification
    # -------------------------------------------------------------
    total_score = min(100, length_score + instruction_score + reasoning_score + tech_score + task_score)

    # Classification Thresholds (Section 4):
    # 0–35    = LOW
    # 36–65   = MEDIUM
    # 66–100  = HIGH
    if total_score <= 35:
        complexity_level = "LOW"
    elif total_score <= 65:
        complexity_level = "MEDIUM"
    else:
        complexity_level = "HIGH"

    if not reasons:
        reasons = ["Simple greeting, factual query, or brief statement"]

    # Task type estimation
    if code_count > 0:
        task_type = "Coding"
    elif reason_count > 0 or tech_count >= 2:
        task_type = "Reasoning & Architecture"
    elif instr_count > 0:
        task_type = "Explanation"
    else:
        task_type = "General Question"

    from app.services.privacy import check_privacy
    privacy_info = check_privacy(text)

    return {
        "question": text,
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": sentence_count,
        "task_type": task_type,
        "score": total_score,
        "complexity_score": round(total_score / 100.0, 2),
        "complexity_level": complexity_level,
        "privacy": privacy_info,
        "breakdown": {
            "length_score": length_score,
            "instruction_score": instruction_score,
            "reasoning_score": reasoning_score,
            "technical_score": tech_score,
            "task_score": task_score
        },
        "reasons": reasons
    }
