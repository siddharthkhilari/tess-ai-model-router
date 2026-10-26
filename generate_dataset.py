"""
Generate benchmark dataset for AI Inference Routing.
Produces dataset/inference_routing_dataset.csv with 300+ realistic queries
across multiple domains, complexities, and privacy levels.
"""

import csv
import random
import os

SEED = 42
random.seed(SEED)

CATEGORIES = {
    "General Question": [
        ("What is RAM?", 0.15, "PUBLIC"),
        ("What is an Operating System?", 0.18, "PUBLIC"),
        ("Define Cloud Computing.", 0.20, "PUBLIC"),
        ("What does HTTP stand for?", 0.12, "PUBLIC"),
        ("What is the difference between TCP and UDP?", 0.28, "PUBLIC"),
        ("Who is the creator of the Python programming language?", 0.14, "PUBLIC"),
        ("What is a primary key in relational databases?", 0.22, "PUBLIC"),
        ("Explain the term 'bandwidth' in networking.", 0.20, "PUBLIC"),
        ("What is the function of an ALU in a CPU?", 0.22, "PUBLIC"),
        ("What is a compiler vs an interpreter?", 0.25, "PUBLIC"),
        ("Define virtual memory and paging in OS.", 0.30, "PUBLIC"),
        ("What is the difference between IPv4 and IPv6?", 0.26, "PUBLIC"),
        ("What is an API endpoint?", 0.20, "PUBLIC"),
        ("What is git and why is version control used?", 0.24, "PUBLIC"),
        ("What is DNS and how does domain resolution work?", 0.30, "PUBLIC"),
        ("What is an IP address?", 0.15, "PUBLIC"),
        ("Explain the purpose of a firewall.", 0.22, "PUBLIC"),
        ("What is bytecode in Java?", 0.25, "PUBLIC"),
        ("What is normalization in DBMS?", 0.30, "PUBLIC"),
        ("What is the difference between RAM and ROM?", 0.18, "PUBLIC"),
    ],
    "Explanation": [
        ("Explain the concept of inheritance in Object-Oriented Programming with a Java example.", 0.42, "PUBLIC"),
        ("Explain how binary search works, its algorithm steps, and why its complexity is O(log n).", 0.48, "PUBLIC"),
        ("Explain how QuickSort works and analyze its best, average, and worst case time complexity.", 0.55, "PUBLIC"),
        ("Explain the ACID properties of database transactions with real banking examples.", 0.50, "PUBLIC"),
        ("Explain deadlock conditions in operating systems and the four Coffman conditions.", 0.58, "PUBLIC"),
        ("Explain the OSI 7-layer model and the key protocol operating at each layer.", 0.54, "PUBLIC"),
        ("Explain the working of Garbage Collection in the Java Virtual Machine (JVM).", 0.56, "PUBLIC"),
        ("Explain asynchronous programming, event loops, and promises in modern JavaScript.", 0.52, "PUBLIC"),
        ("Explain Docker containerization and how it differs from traditional Virtual Machines.", 0.49, "PUBLIC"),
        ("Explain the difference between SQL and NoSQL databases with use cases.", 0.46, "PUBLIC"),
        ("Explain public key cryptography and RSA encryption mechanism.", 0.59, "PUBLIC"),
        ("Explain the concept of microservices architecture vs monolithic systems.", 0.55, "PUBLIC"),
        ("Explain paging and segmentation in memory management with pros and cons.", 0.58, "PUBLIC"),
        ("Explain how TLS/SSL handshake establishes an encrypted communication channel.", 0.62, "PUBLIC"),
        ("Explain convolutional neural networks (CNNs) and pooling operations.", 0.65, "PUBLIC"),
    ],
    "Coding - Basic": [
        ("Write a Python function to check whether a given string is a palindrome.", 0.42, "PUBLIC"),
        ("Write a Java program to reverse an array in-place without using extra space.", 0.45, "PUBLIC"),
        ("Implement a basic binary search algorithm in Python that returns the target index.", 0.48, "PUBLIC"),
        ("Write a C++ function to check if a number is prime in O(sqrt(n)) time.", 0.46, "PUBLIC"),
        ("Write a JavaScript function to remove duplicates from an array.", 0.40, "PUBLIC"),
        ("Implement a stack using two queues in Python with push and pop operations.", 0.52, "PUBLIC"),
        ("Write a Python script to count word frequencies in a given text file.", 0.44, "PUBLIC"),
        ("Implement a single linked list insertion and deletion in C++.", 0.55, "PUBLIC"),
        ("Write a SQL query to find the second highest salary from an Employee table.", 0.48, "PUBLIC"),
        ("Write a recursive function to compute the N-th Fibonacci number in Python.", 0.40, "PUBLIC"),
        ("Write a program to validate email format using regular expressions in Python.", 0.44, "PUBLIC"),
        ("Write a function to find the maximum contiguous subarray sum (Kadane's algorithm).", 0.58, "PUBLIC"),
    ],
    "Coding - Complex": [
        ("Design and implement a concurrent thread-safe LRU Cache in C++17 with O(1) operations, mutex locking, and condition variables.", 0.85, "PUBLIC"),
        ("Implement a distributed Raft consensus state machine in Go including Leader Election and Heartbeat RPC mechanisms.", 0.94, "PUBLIC"),
        ("Write a custom memory allocator in C implementing buddy allocation with memory coalescing and fragmentation benchmarks.", 0.92, "PUBLIC"),
        ("Implement a complete B-Tree indexing structure in Rust with node splitting, merging, and disk page serialization.", 0.91, "PUBLIC"),
        ("Build a multi-producer multi-consumer lock-free ring buffer queue using atomic CAS operations in C++.", 0.89, "PUBLIC"),
        ("Develop an asynchronous HTTP/2 multiplexing parser and server socket handler from scratch in Python asyncio.", 0.88, "PUBLIC"),
        ("Write a high-performance matrix multiplication routine using SIMD AVX-512 intrinsics and cache tiling in C.", 0.93, "PUBLIC"),
        ("Design an automated query optimizer in Python that parses SQL ASTs and applies cost-based index scan joins.", 0.87, "PUBLIC"),
        ("Implement an inverted index and BM25 ranking retrieval search engine pipeline in Java.", 0.84, "PUBLIC"),
        ("Implement a WebSocket event-driven distributed pub-sub broker with topic wildcard filtering in Node.js.", 0.82, "PUBLIC"),
    ],
    "Reasoning & Architecture": [
        ("Analyze a distributed cloud-native architecture for high concurrency e-commerce checkout. Identify race conditions, idempotency patterns, and propose two-phase commit vs Saga orchestrations.", 0.92, "PUBLIC"),
        ("Evaluate the CAP theorem trade-offs when transitioning from a Cassandra database cluster to CockroachDB for global financial ledger consistency.", 0.89, "PUBLIC"),
        ("Conduct an in-depth architectural trade-off analysis between monolithic kernels and microkernels regarding context-switch overhead, IPC latency, and fault isolation.", 0.86, "PUBLIC"),
        ("Perform a comprehensive threat model analysis for a federated OAuth2 and OpenID Connect identity provider, covering token theft, replay attacks, and PKCE mitigations.", 0.88, "PUBLIC"),
        ("Design a fault-tolerant distributed streaming ingestion pipeline capable of handling 500,000 events/sec with exactly-once processing semantics.", 0.91, "PUBLIC"),
        ("Compare the memory latency and bandwidth implications of Uniform Memory Access (UMA) vs Non-Uniform Memory Access (NUMA) architectures under heavy multi-threaded workloads.", 0.87, "PUBLIC"),
        ("Formulate a comprehensive disaster recovery and data replication strategy across three AWS availability zones with RPO < 1 minute and RTO < 5 minutes.", 0.84, "PUBLIC"),
        ("Analyze the algorithmic complexity and space-time trade-offs of Paxos vs Raft consensus algorithms in Byzantine and non-Byzantine failure models.", 0.90, "PUBLIC"),
    ],
    "Mathematics & Algorithms": [
        ("Solve the recurrence relation T(n) = 3T(n/4) + n*log(n) using the Akra-Bazzi method and explain each mathematical step.", 0.78, "PUBLIC"),
        ("Prove that 3-SAT is NP-complete by reducing from Circuit-SAT with detailed polynomial reduction steps.", 0.88, "PUBLIC"),
        ("Compute the eigenvalues and eigenvectors of a 3x3 symmetric matrix step-by-step and show diagonalizability.", 0.68, "PUBLIC"),
        ("Derive the backpropagation gradient equations for a multi-layer perceptron with cross-entropy loss and softmax output.", 0.76, "PUBLIC"),
        ("Prove the correctness and termination of Dijkstra's algorithm using mathematical induction on the visited set.", 0.74, "PUBLIC"),
        ("Formulate the dual linear programming problem for a primal transportation optimization problem and explain shadow prices.", 0.80, "PUBLIC"),
        ("Derive the closed-form time complexity of Strassen's matrix multiplication algorithm using the Master Theorem.", 0.65, "PUBLIC"),
    ],
    "Sensitive & Privacy": [
        ("Review this employee Aadhaar card number 4589-1234-8765 and PAN ABCDE1234F for internal HR database verification.", 0.35, "SENSITIVE"),
        ("Analyze this confidential patient discharge summary and diagnosis notes: Patient has diabetes mellitus and elevated BP.", 0.50, "SENSITIVE"),
        ("Verify these customer credit card transaction records for fraud detection: card 4111-2222-3333-4444 CVV 123.", 0.45, "SENSITIVE"),
        ("Inspect this confidential company executive salary ledger and performance rating table for Q3 payroll auditing.", 0.52, "SENSITIVE"),
        ("Validate internal admin password hashes and secret API tokens against known corporate leak databases.", 0.60, "SENSITIVE"),
        ("Parse confidential passport number Z1234567 and visa status for international background clearance.", 0.38, "SENSITIVE"),
        ("Evaluate this confidential medical laboratory report containing blood biomarkers and biopsy pathology analysis.", 0.62, "SENSITIVE"),
        ("Verify customer billing address and private banking account routing numbers for wire transfer verification.", 0.44, "SENSITIVE"),
    ]
}

def generate_variations():
    rows = []
    pid = 1

    # Base pricing and latency parameters per need.md
    # Small: ~₹0.01, ~1.0s
    # Medium: ~₹0.03, ~2.0s
    # Large: ~₹0.08, ~4.0s

    prefixes = [
        "", "Please ", "Can you ", "Provide a detailed answer: ", "Kindly ", 
        "Write a comprehensive explanation for: ", "Step by step: ", "Quick answer: "
    ]
    suffixes = [
        "", " Explain clearly.", " Provide code if applicable.", " Be concise.",
        " Include relevant examples.", " Highlight key considerations.", " In detail."
    ]

    for category, prompt_list in CATEGORIES.items():
        for base_prompt, base_comp, base_priv in prompt_list:
            # Create 3-5 variations of each base prompt to reach 300+ total rows
            num_vars = random.randint(3, 5)
            for v in range(num_vars):
                prefix = random.choice(prefixes) if v > 0 else ""
                suffix = random.choice(suffixes) if v > 0 else ""
                prompt_text = f"{prefix}{base_prompt}{suffix}".strip()

                # Add minor realistic noise to complexity score
                comp = min(1.0, max(0.05, round(base_comp + random.uniform(-0.06, 0.06), 2)))

                # Determine complexity level
                if comp < 0.40:
                    comp_level = "LOW"
                    optimal_model = "Small Model"
                elif comp < 0.70:
                    comp_level = "MEDIUM"
                    optimal_model = "Medium Model"
                else:
                    comp_level = "HIGH"
                    optimal_model = "Large Model"

                # Privacy override: if sensitive, prefer Small/Local model
                if base_priv == "SENSITIVE":
                    optimal_model = "Small Model (Local)"
                    routed_model = "Small Model"
                else:
                    routed_model = optimal_model

                words = len(prompt_text.split())
                chars = len(prompt_text)

                # Simulated latency (with natural variance)
                s_lat = round(random.uniform(0.7, 1.3), 3)
                m_lat = round(random.uniform(1.6, 2.4), 3)
                l_lat = round(random.uniform(3.4, 4.6), 3)

                # Estimated costs in INR per need.md
                s_cost = 0.01
                m_cost = 0.03
                l_cost = 0.08

                if routed_model == "Small Model":
                    r_lat = s_lat
                    r_cost = s_cost
                elif routed_model == "Medium Model":
                    r_lat = m_lat
                    r_cost = m_cost
                else:
                    r_lat = l_lat
                    r_cost = l_cost

                baseline_cost = l_cost
                saving_inr = round(baseline_cost - r_cost, 4)
                saving_pct = round((saving_inr / baseline_cost) * 100, 1)

                rows.append({
                    "prompt_id": f"PBL-{pid:04d}",
                    "prompt": prompt_text,
                    "category": category,
                    "word_count": words,
                    "char_count": chars,
                    "complexity_score": comp,
                    "complexity_level": comp_level,
                    "privacy_level": base_priv,
                    "optimal_model": optimal_model,
                    "small_model_latency_s": s_lat,
                    "small_model_cost_inr": s_cost,
                    "medium_model_latency_s": m_lat,
                    "medium_model_cost_inr": m_cost,
                    "large_model_latency_s": l_lat,
                    "large_model_cost_inr": l_cost,
                    "routed_model": routed_model,
                    "routed_latency_s": r_lat,
                    "routed_cost_inr": r_cost,
                    "baseline_large_cost_inr": baseline_cost,
                    "saving_inr": saving_inr,
                    "saving_percentage": saving_pct
                })
                pid += 1

    return rows

def main():
    os.makedirs("dataset", exist_ok=True)
    rows = generate_variations()
    output_path = os.path.join("dataset", "inference_routing_dataset.csv")

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} samples in {output_path}")

if __name__ == "__main__":
    main()
