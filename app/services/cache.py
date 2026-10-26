"""
Simple SQLite Query Cache Service (need.md Section 19).
Stores and retrieves exact question matches to eliminate redundant inference costs.
"""

import hashlib
from typing import Optional, Dict, Any
from app.core.database import get_db_connection

def normalize_question(question: str) -> str:
    """Normalizes question string by trimming and lowercasing."""
    return " ".join(question.strip().lower().split())

def compute_hash(normalized_text: str) -> str:
    """Computes SHA-256 hash of the normalized question."""
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()

def get_cached_response(question: str) -> Optional[Dict[str, Any]]:
    """Checks the SQLite cache for a normalized question match."""
    norm = normalize_question(question)
    q_hash = compute_hash(norm)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, response, model, created_at FROM cache WHERE question_hash = ?", (q_hash,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "question": row["question"],
            "response": row["response"],
            "model": row["model"],
            "created_at": row["created_at"]
        }
    return None

def set_cached_response(question: str, response: str, model: str):
    """Stores query and response in the SQLite cache."""
    norm = normalize_question(question)
    q_hash = compute_hash(norm)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO cache (question_hash, question, response, model)
        VALUES (?, ?, ?, ?)
    """, (q_hash, question.strip(), response.strip(), model))
    conn.commit()
    conn.close()
