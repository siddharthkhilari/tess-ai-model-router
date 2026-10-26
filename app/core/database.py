"""
Database management module using SQLite.
Creates required tables (requests, models, cache) and seeds default model registry.
"""

import sqlite3
from typing import Dict, Any, List
from app.core.config import DATABASE_PATH

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables and seeds default models."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. requests table (need.md Section 20)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        response TEXT NOT NULL,
        task_type TEXT,
        complexity_score REAL,
        complexity_level TEXT,
        privacy_level TEXT,
        selected_model TEXT,
        latency_ms REAL,
        estimated_cost REAL,
        baseline_cost REAL,
        estimated_saving REAL,
        cache_hit INTEGER DEFAULT 0,
        routing_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. models table (need.md Section 20)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tier TEXT NOT NULL,
        description TEXT,
        estimated_cost REAL NOT NULL,
        expected_quality INTEGER NOT NULL,
        expected_latency REAL NOT NULL,
        available INTEGER DEFAULT 1
    );
    """)

    # 3. cache table (need.md Section 19)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cache (
        question_hash TEXT PRIMARY KEY,
        question TEXT NOT NULL,
        response TEXT NOT NULL,
        model TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed default models if table is empty (need.md Section 7)
    cursor.execute("SELECT COUNT(*) FROM models")
    if cursor.fetchone()[0] == 0:
        default_models = [
            ("small", "Small Model", "small", "Lightweight SLM for basic Q&A, definitions, and high throughput.", 0.01, 75, 1.0, 1),
            ("medium", "Medium Model", "medium", "Balanced model for code generation, summaries, and medium explanations.", 0.03, 85, 2.0, 1),
            ("large", "Large Model", "large", "Frontier LLM for complex multi-step reasoning, distributed architecture & math.", 0.08, 95, 4.0, 1)
        ]
        cursor.executemany("""
            INSERT INTO models (id, name, tier, description, estimated_cost, expected_quality, expected_latency, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, default_models)

    conn.commit()
    conn.close()

def log_request(record: Dict[str, Any]) -> int:
    """Inserts a processed request into the database and returns the new ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requests (
            question, response, task_type, complexity_score, complexity_level,
            privacy_level, selected_model, latency_ms, estimated_cost,
            baseline_cost, estimated_saving, cache_hit, routing_reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("question", ""),
        record.get("response", ""),
        record.get("task_type", "General Question"),
        record.get("complexity_score", 0.0),
        record.get("complexity_level", "LOW"),
        record.get("privacy_level", "PUBLIC"),
        record.get("selected_model", "small"),
        record.get("latency_ms", 0.0),
        record.get("estimated_cost", 0.0),
        record.get("baseline_cost", 0.08),
        record.get("estimated_saving", 0.0),
        1 if record.get("cache_hit", False) else 0,
        record.get("routing_reason", "")
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id
