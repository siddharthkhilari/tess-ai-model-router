"""
Application Runner Script (need.md Section 24).
Initializes database, seeds initial realistic demonstration queries if empty, and launches Uvicorn server.
"""

import os
import sys
import uvicorn
from app.core.database import init_db, get_db_connection
from app.services.inference import process_inference_request

def seed_initial_demo_requests():
    """Seeds a few initial sample requests so the dashboard is immediately rich for evaluation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM requests")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        print("[*] Seeding initial demonstration queries into SQLite database...")
        demo_queries = [
            "What is RAM?",
            "What is inheritance in Java?",
            "Write a Java program to implement binary search and explain its time complexity.",
            "Analyze a distributed application architecture and identify possible performance and concurrency problems.",
            "What is an Operating System?",
            "Explain Docker containerization and how it differs from traditional Virtual Machines.",
            "What is RAM?", # Second time to demonstrate cache HIT!
            "Analyze this confidential employee record: Aadhaar 4589-1234-8765."
        ]
        for q in demo_queries:
            process_inference_request(q)
        print(f"[✓] Seeded {len(demo_queries)} initial requests (including cache HIT demonstration).")

def main():
    print("=" * 60)
    print("  TESS AI INFERENCE ROUTER — COLLEGE PROTOTYPE")
    print("=" * 60)
    print("Initializing SQLite Database...")
    init_db()
    seed_initial_demo_requests()

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")

    print("\nStarting Web Application...")
    print(f" -> Local Web Interface: http://{host}:{port}")
    print(f" -> AI Router:           http://{host}:{port}/")
    print(f" -> Live Dashboard:      http://{host}:{port}/dashboard")
    print(f" -> Model Comparison:    http://{host}:{port}/comparison")
    print(f" -> Interactive API Docs: http://{host}:{port}/docs")
    print("=" * 60)
    print("Press Ctrl+C to terminate.")

    uvicorn.run("app.main:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
