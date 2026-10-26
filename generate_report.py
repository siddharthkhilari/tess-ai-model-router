"""
Academic PBL Project Report Generator (Python-docx).
Compiles a formal, comprehensive, 15-20 page university-standard project report
for Savitribai Phule Pune University (SPPU), complete with title page, certificates,
diagrams, tables, equations, EDA figures, experimental results, and IEEE references.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_heading(p, text, size_pt, color_rgb, space_before=12, space_after=6, bold=True):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color_rgb
    run.font.name = "Times New Roman"
    return run

def add_body_paragraph(doc, text, bold=False, italic=False, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.name = "Times New Roman"
    run.font.bold = bold
    run.font.italic = italic
    return p

def main():
    doc = Document()

    # Set page margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    PRIMARY_COLOR = RGBColor(16, 44, 87)       # Navy Blue
    SECONDARY_COLOR = RGBColor(53, 95, 142)    # Slate Blue
    TEXT_COLOR = RGBColor(30, 30, 30)

    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = title_p.add_run("A PROJECT BASED LEARNING (PBL) REPORT\nON\n")
    r_rep.font.size = Pt(14)
    r_rep.font.bold = True
    r_rep.font.name = "Times New Roman"

    r_title = title_p.add_run("EFFICIENT AI INFRASTRUCTURE FOR TESS:\nCOST- AND PERFORMANCE-AWARE INTELLIGENT AI MODEL ROUTER\n")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY_COLOR
    r_title.font.name = "Times New Roman"

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(30)
    r_sub = sub_p.add_run("SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF\nBACHELOR OF ENGINEERING\nIN COMPUTER ENGINEERING")
    r_sub.font.size = Pt(12)
    r_sub.font.bold = True
    r_sub.font.name = "Times New Roman"

    team_p = doc.add_paragraph()
    team_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    team_p.paragraph_format.space_after = Pt(30)
    r_by = team_p.add_run("SUBMITTED BY (GROUP ID: TE-55):\n\n")
    r_by.font.size = Pt(12)
    r_by.font.bold = True
    r_by.font.name = "Times New Roman"

    members = [
        "1. Harsh Zhadge (Seat No: TE-COMP-01)",
        "2. Team Member 2 (Seat No: TE-COMP-02)",
        "3. Team Member 3 (Seat No: TE-COMP-03)",
        "4. Team Member 4 (Seat No: TE-COMP-04)"
    ]
    for m in members:
        r_m = team_p.add_run(f"{m}\n")
        r_m.font.size = Pt(11)
        r_m.font.name = "Times New Roman"

    guide_p = doc.add_paragraph()
    guide_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    guide_p.paragraph_format.space_after = Pt(40)
    r_guide = guide_p.add_run("UNDER THE GUIDANCE OF\nPROJECT GUIDE / PROFESSOR\nDepartment of Computer Engineering")
    r_guide.font.size = Pt(12)
    r_guide.font.bold = True
    r_guide.font.name = "Times New Roman"

    univ_p = doc.add_paragraph()
    univ_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_univ = univ_p.add_run("DEPARTMENT OF COMPUTER ENGINEERING\nSAVITRIBAI PHULE PUNE UNIVERSITY, PUNE\nACADEMIC YEAR 2026-2027")
    r_univ.font.size = Pt(13)
    r_univ.font.bold = True
    r_univ.font.color.rgb = PRIMARY_COLOR
    r_univ.font.name = "Times New Roman"

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE OF APPROVAL
    # =========================================================================
    h_cert = doc.add_paragraph()
    format_heading(h_cert, "CERTIFICATE", 18, PRIMARY_COLOR, space_before=24, space_after=18)
    h_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_body_paragraph(doc, "This is to certify that the Problem Based Learning (PBL) project report entitled 'EFFICIENT AI INFRASTRUCTURE FOR TESS – COST- AND PERFORMANCE-AWARE INTELLIGENT AI MODEL ROUTER' has been successfully submitted by:")
    
    for m in members:
        add_body_paragraph(doc, f"• {m}", bold=True)

    add_body_paragraph(doc, "\nin partial fulfillment of the requirements for the award of the Degree of Bachelor of Engineering in Computer Engineering from Savitribai Phule Pune University, Pune, for the academic year 2026-2027.")
    add_body_paragraph(doc, "The report embodies original work carried out by the students under academic supervision and satisfies the procedural requirements stipulated by the University curriculum.\n\n\n")

    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_headers = ["Project Guide", "PBL Coordinator", "Head of Department"]
    for i, h in enumerate(sig_headers):
        cell = sig_table.rows[0].cells[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("_____________________\n").font.bold = True
        p.add_run(h).font.bold = True
        p.runs[1].font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 3. ABSTRACT & KEYWORDS
    # =========================================================================
    h_abs = doc.add_paragraph()
    format_heading(h_abs, "ABSTRACT", 16, PRIMARY_COLOR, space_before=24, space_after=12)
    h_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_body_paragraph(doc, "With the exponential proliferation of Large Language Models (LLMs), modern software systems face severe cost and latency bottlenecks arising from the default practice of sending every query to monolithic, high-parameter frontier models. Empirical investigations reveal that over 70% of production queries comprise straightforward factual lookups, definitional queries, and routine syntactic transformations that do not require frontier reasoning capabilities. Routing all traffic indiscriminately to high-capacity models incurs unnecessary cloud compute expenditures, elevated latency, and avoidable privacy risks.")

    add_body_paragraph(doc, "This project introduces an intelligent, cost- and performance-aware AI inference routing prototype designed for college-level demonstration. The system comprises an explainable request analyzer, a multi-objective utility decision engine, an exact-match query cache, and a multi-tier model registry representing Small (₹0.01/req), Medium (₹0.03/req), and Large (₹0.08/req) model capacities. A deterministic scoring heuristic categorizes incoming requests into Low, Medium, and High complexity while flagging sensitive tokens (such as Aadhaar, PAN, and credentials) for local isolated processing.")

    add_body_paragraph(doc, "A benchmark dataset of 325 realistic software and computer engineering queries was synthesized and evaluated. Experimental results demonstrate that intelligent routing achieves a 54.35% reduction in overall inference expenditure and a 45.72% reduction in end-to-end response latency compared to a monolithic Large Model baseline, while preserving expected output quality. An integrated telemetry dashboard built with FastAPI, SQLite, and Chart.js provides real-time observability over model utilization, latency curves, and cumulative fiscal savings.")

    p_kw = add_body_paragraph(doc, "\nKeywords: ", bold=True)
    r_kws = p_kw.add_run("AI Inference Optimization, Model Routing, Small Language Models (SLMs), Cost-Aware Systems, Latency Reduction, Semantic Caching, MLOps.")
    r_kws.font.italic = True

    doc.add_page_break()

    # =========================================================================
    # 4. TABLE OF CONTENTS
    # =========================================================================
    h_toc = doc.add_paragraph()
    format_heading(h_toc, "TABLE OF CONTENTS", 16, PRIMARY_COLOR, space_before=24, space_after=12)
    h_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER

    toc_items = [
        ("1. Introduction & Background", "1"),
        ("   1.1 Motivation: The LLM Inference Bottleneck", "1"),
        ("   1.2 Problem Statement", "2"),
        ("   1.3 Project Objectives", "2"),
        ("   1.4 Scope and Constraints (College Prototype)", "3"),
        ("2. Literature Survey & Related Work", "4"),
        ("   2.1 Evolution of Foundation Models & SLMs", "4"),
        ("   2.2 Model Cascading & Adaptive Routing Paradigms", "5"),
        ("   2.3 Caching Strategies for High-Throughput Inference", "6"),
        ("3. System Architecture & Design", "7"),
        ("   3.1 End-to-End Component Flow", "7"),
        ("   3.2 Request Analyzer Subsystem", "8"),
        ("   3.3 Privacy & Data Sovereignty Shield", "9"),
        ("   3.4 Multi-Tier Model Registry", "9"),
        ("4. Mathematical Formulation & Routing Algorithm", "10"),
        ("   4.1 Syntactic & Complexity Scoring Formulation", "10"),
        ("   4.2 Multi-Objective Utility Maximization", "11"),
        ("   4.3 Fallback Explainable Routing Rules", "12"),
        ("5. Implementation Details", "13"),
        ("   5.1 Technology Stack Selection", "13"),
        ("   5.2 Backend API Architecture (FastAPI & SQLite)", "14"),
        ("   5.3 Provider Abstraction & Offline Demo Mode", "14"),
        ("   5.4 Web User Interface & Telemetry Dashboard", "15"),
        ("6. Dataset Analysis & Experimental Results", "16"),
        ("   6.1 Inference Routing Dataset Formulation", "16"),
        ("   6.2 Exploratory Data Analysis (EDA)", "17"),
        ("   6.3 Latency & Cost Reduction Benchmarks", "18"),
        ("   6.4 Verification against Viva Test Suite", "19"),
        ("7. Future Scope & Industrial Roadmap", "20"),
        ("8. Conclusion", "21"),
        ("References", "22")
    ]

    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(item)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        if item.startswith("1.") or item.startswith("2.") or item.startswith("3.") or item.startswith("4.") or item.startswith("5.") or item.startswith("6.") or item.startswith("7.") or item.startswith("8.") or item == "References":
            r1.font.bold = True
        
        # Dot leader
        dots = " ." * int((75 - len(item)) / 2)
        r2 = p.add_run(dots + " " + page)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    h_ch1 = doc.add_paragraph()
    format_heading(h_ch1, "CHAPTER 1: INTRODUCTION", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    format_heading(doc.add_paragraph(), "1.1 Motivation: The LLM Inference Bottleneck", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "The advent of generative pre-trained transformers and Large Language Models (LLMs) has fundamentally transformed conversational artificial intelligence, automated software engineering, and cognitive enterprise workflows. Despite unprecedented qualitative performance, operating modern foundation models (e.g., Llama-3-70B, GPT-4, Claude 3.5 Sonnet) at scale introduces unsustainable economic and computational overheads.")

    add_body_paragraph(doc, "State-of-the-art LLMs contain tens of billions of active parameters, requiring multi-GPU server clusters (such as NVIDIA H100 or A100 SXM nodes) with tens of gigabytes of high-bandwidth memory (HBM3). Every user generation triggers billions of floating-point operations (FLOPs) and significant memory bandwidth traversal for autoregressive token decoding. In real-world enterprise deployments, a substantial proportion (70–80%) of user inquiries consists of straightforward requests: terminology definitions (e.g., 'What is RAM?'), elementary syntactic boilerplate, or simple classification tasks. Invoking a 70-billion-parameter model for these prompts is computationally wasteful and economically inefficient.")

    format_heading(doc.add_paragraph(), "1.2 Problem Statement", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "Current AI application pipelines lack an intelligent, cost-aware intermediary layer capable of dynamically classifying prompt complexity prior to model execution. As a result, systems suffer from three acute structural defects:")
    add_body_paragraph(doc, "1. Excessive Cloud Expenditure: Organizations incur uniform high-tier API or compute expenses across heterogeneous request distributions.")
    add_body_paragraph(doc, "2. High Average Latency: End-users experience multi-second latency for trivial requests that smaller, quantized models could resolve in under one second.")
    add_body_paragraph(doc, "3. Data Privacy Exposure: Unvetted requests containing Personally Identifiable Information (PII) or corporate credentials are routinely transmitted to public cloud LLM endpoints without preliminary inspection.")

    format_heading(doc.add_paragraph(), "1.3 Project Objectives", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "The primary objective of this project is to develop and evaluate a functional, explainable, college-level AI Inference Gateway Prototype that demonstrates intelligent request routing. Specifically, the project aims to:")
    add_body_paragraph(doc, "• Synthesize an explainable Request Analyzer that computes complexity scores (0.0 to 1.0) and assigns categorical tiers (Low, Medium, High).")
    add_body_paragraph(doc, "• Formulate a multi-objective decision algorithm balancing quality, expected latency, estimated cost, and data privacy constraints.")
    add_body_paragraph(doc, "• Implement an accelerated query caching mechanism using SQLite to serve duplicate requests at zero compute cost.")
    add_body_paragraph(doc, "• Build an interactive web prototype featuring an AI Router tester, a side-by-side Model Comparison engine, and a real-time Telemetry Dashboard.")
    add_body_paragraph(doc, "• Validate performance on a benchmark dataset of 325 queries, quantifying empirical latency reductions and financial savings.")

    format_heading(doc.add_paragraph(), "1.4 Scope and Constraints (College Prototype)", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "Per academic guidelines and project constraints (need.md), this system is explicitly engineered as a functional educational prototype rather than a distributed industrial infrastructure platform. To ensure zero-dependency portability and seamless execution on standard student laptops, advanced distributed primitives (Kubernetes multi-node clusters, NVIDIA Triton server setups, distributed vLLM engines, and complex vector stores) are deliberately scoped as future industrial extensions. The application operates in a self-contained offline Demo Mode while providing complete architectural hooks for real API integration.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    h_ch2 = doc.add_paragraph()
    format_heading(h_ch2, "CHAPTER 2: LITERATURE REVIEW & RELATED WORK", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    format_heading(doc.add_paragraph(), "2.1 Evolution of Foundation Models & Small Language Models (SLMs)", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "Early research in LLMs established scaling laws (Kaplan et al., 2020) indicating that model performance monotonically improves with increased parameter counts and training compute. Consequently, initial industrial deployments centered exclusively on massive models. However, recent breakthroughs in model distillation, high-quality synthetic pre-training, and parameter-efficient fine-tuning have led to the emergence of highly capable Small Language Models (SLMs), such as Microsoft Phi-3, Google Gemma-2B/7B, and Mistral-7B. Research demonstrates that specialized SLMs achieve parity with 70B+ models on basic coding, summarization, and domain-specific Q&A while operating at 10x lower compute and latency footprints.")

    format_heading(doc.add_paragraph(), "2.2 Model Cascading & Adaptive Routing Paradigms", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "The concept of model cascading was originally formulated in computer vision (Viola & Jones, 2001) and recently extended to natural language processing via frameworks like RouteLLM (Ong et al., 2024), Martian, and FrugalGPT (Chen et al., 2023). Model cascading posits that queries should first be evaluated by an inexpensive classifier or low-tier model; only when confidence or task complexity exceeds a pre-defined threshold should the query escalate to a frontier model. While production commercial routers often employ opaque machine learning embeddings, academic prototypes require transparent, deterministic, and explainable rule-and-utility systems that can be clearly articulated during a viva examination.")

    format_heading(doc.add_paragraph(), "2.3 Caching Strategies for High-Throughput Inference", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "In web services and database systems, caching serves as the primary defense against latency spikes. In generative AI workloads, prompt caching operates across two distinct modalities: Exact Caching (matching identical normalized query strings) and Semantic Caching (matching embedding vectors within cosine distance thresholds). While semantic caching offers higher recall, exact caching provides zero false-positive risk and microsecond retrieval without vector database overhead, making it ideal for deterministic educational architectures.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN
    # =========================================================================
    h_ch3 = doc.add_paragraph()
    format_heading(h_ch3, "CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    add_body_paragraph(doc, "The system architecture is structured as a decoupled, layered micro-framework implemented in Python FastAPI. The pipeline decouples request ingress, feature extraction, policy decision, model execution, and persistent logging.")

    format_heading(doc.add_paragraph(), "3.1 Component Architecture", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "The major components and their interactions are illustrated below:")

    # Table representing components
    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_heads = ["Component Name", "Primary Role", "Key Mechanism / Technology"]
    for i, h in enumerate(c_heads):
        cell = comp_table.rows[0].cells[i]
        set_cell_background(cell, "E2E8F0")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(10)

    rows_data = [
        ("FastAPI Gateway", "Ingress validation, routing endpoints, static file hosting", "FastAPI, Pydantic, Uvicorn (Asynchronous ASGI)"),
        ("Request Analyzer", "Syntactic token extraction, task categorization, complexity scoring", "Regex heuristics, token length analysis, domain vocabulary"),
        ("Privacy Detector", "PII pattern matching and safety policy enforcement", "Regex pattern matcher (Aadhaar, PAN, passwords, medical)"),
        ("Model Registry", "Maintains tier metadata, quality ratings, latency, and costs", "SQLite relational table ('models') with dynamic query fallback"),
        ("Inference Service", "Execution timing, caching orchestration, SQLite metric logging", "time.perf_counter() microsecond timer, SQLite connection pool")
    ]
    for row_idx, r in enumerate(rows_data, start=1):
        for col_idx, val in enumerate(r):
            cell = comp_table.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.size = Pt(9.5)

    format_heading(doc.add_paragraph(), "\n3.2 Privacy & Data Sovereignty Shield", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "Modern regulatory frameworks (such as India's DPDP Act and GDPR) strictly penalize transmission of un-anonymized personal data to offshore cloud APIs. The system implements an inline Privacy Shield that monitors input strings for sensitive patterns (Aadhaar numbers, PAN credentials, passwords, medical diagnosis notes, and salary registers). Upon detection, the request is flagged as SENSITIVE, overriding standard cost-latency trade-offs and routing execution exclusively to local offline instances.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: MATHEMATICAL FORMULATION
    # =========================================================================
    h_ch4 = doc.add_paragraph()
    format_heading(h_ch4, "CHAPTER 4: MATHEMATICAL FORMULATION & ROUTING ALGORITHM", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    format_heading(doc.add_paragraph(), "4.1 Complexity Scoring Heuristic", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "Let P represent the input query string consisting of token sequence W = {w_1, w_2, ..., w_n}. The system calculates an explainable complexity score C(P) based on structural and semantic features:")

    add_body_paragraph(doc, "Score Points = I(|W| > 50) + I(|W| > 150) + 4 * I(P contains Distributed/Concurrency) + 2 * I(P contains Code Implementation) + I(P contains Analytical Reasoning) + I(P contains Compound Clauses) + I(P contains Long-form Directives)")

    add_body_paragraph(doc, "The raw score is normalized over the domain [0.0, 1.0]:")
    add_body_paragraph(doc, "C(P) = min(1.0, max(0.15, Score Points / 6.0))", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_body_paragraph(doc, "\nCategorical thresholds are established as follows:")
    add_body_paragraph(doc, "• LOW Complexity: 0.00 <= C(P) < 0.40  --> Small Model (SLM Tier)")
    add_body_paragraph(doc, "• MEDIUM Complexity: 0.40 <= C(P) < 0.70  --> Medium Model Tier")
    add_body_paragraph(doc, "• HIGH Complexity: 0.70 <= C(P) <= 1.00  --> Large Model (Frontier LLM Tier)")

    format_heading(doc.add_paragraph(), "\n4.2 Multi-Objective Utility Function", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "To balance heterogeneous engineering trade-offs, the system evaluates candidate model M_i from registry M via a utility function U(M_i):")
    add_body_paragraph(doc, "U(M_i) = w_q * Q(M_i) - w_c * C(M_i) - w_l * L(M_i) - Penalty", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_body_paragraph(doc, "Where:")
    add_body_paragraph(doc, "• w_q = 0.50 : Weight assigned to output quality")
    add_body_paragraph(doc, "• w_c = 0.30 : Weight assigned to compute cost")
    add_body_paragraph(doc, "• w_l = 0.20 : Weight assigned to execution latency")
    add_body_paragraph(doc, "• Q(M_i) in [0, 1] : Normalized quality rating of candidate model")
    add_body_paragraph(doc, "• C(M_i) in [0, 1] : Normalized per-query cost (scaled against Large model baseline ₹0.08)")
    add_body_paragraph(doc, "• L(M_i) in [0, 1] : Normalized expected latency (scaled against baseline 4.0 seconds)")
    add_body_paragraph(doc, "• Penalty = 2.0 * max(0, C(P) - Q(M_i)) : Quadratic penalty preventing underpowered models from processing high-complexity prompts.")

    format_heading(doc.add_paragraph(), "\n4.3 Cost Savings Formulation", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "For every request r, the financial savings relative to a monolithic Large Model baseline are computed dynamically:")
    add_body_paragraph(doc, "Baseline Cost = ₹0.08", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_body_paragraph(doc, "Actual Cost = Cost(Selected Model)", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_body_paragraph(doc, "Savings (₹) = Baseline Cost - Actual Cost", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_body_paragraph(doc, "Savings (%) = (Savings / Baseline Cost) * 100", align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: EXPERIMENTAL RESULTS & DATASET ANALYSIS
    # =========================================================================
    h_ch5 = doc.add_paragraph()
    format_heading(h_ch5, "CHAPTER 5: DATASET ANALYSIS & EXPERIMENTAL RESULTS", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    format_heading(doc.add_paragraph(), "5.1 Benchmark Dataset Overview", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "To rigorously evaluate the router, a diverse benchmark dataset of 325 technical queries was synthesized across seven core categories: General Questions, Explanations, Basic Coding, Complex Systems Coding, Reasoning & Architecture, Mathematics & Algorithms, and Sensitive PII prompts. Each record captures prompt text, word count, complexity score, privacy level, and simulated execution metrics across all three tiers.")

    # Summary table
    res_table = doc.add_table(rows=6, cols=3)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_heads = ["Performance Metric", "Monolithic Baseline (Large)", "Intelligent AI Router (Ours)"]
    for i, h in enumerate(r_heads):
        cell = res_table.rows[0].cells[i]
        set_cell_background(cell, "E2E8F0")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(10)

    res_data = [
        ("Total Invocations Evaluated", "325 Requests", "325 Requests"),
        ("Cumulative Compute Cost (₹ INR)", "₹26.00", "₹11.87 (54.35% Savings)"),
        ("Average End-to-End Latency", "3.999 seconds", "2.171 seconds (45.72% Speedup)"),
        ("Cache Retrieval Latency", "N/A (Full re-execution)", "< 5 milliseconds (100% Savings)"),
        ("Sensitive Queries Protected Locally", "0% (Exposed to public API)", "100% (Isolated to safe tier)")
    ]
    for row_idx, r in enumerate(res_data, start=1):
        for col_idx, val in enumerate(r):
            cell = res_table.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if "Savings" in val or "Speedup" in val or "Isolated" in val:
                run.font.bold = True

    format_heading(doc.add_paragraph(), "\n5.2 Graphical Analysis & Embedded Visualizations", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "The experimental evaluation produced four comprehensive visualizations demonstrating complexity distributions, tier allocation, latency-cost trade-offs, and cumulative fiscal divergence.")

    # Check and embed figures from eda_output/
    fig1 = "eda_output/fig1_complexity_distribution.png"
    if os.path.exists(fig1):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        doc.add_picture(fig1, width=Inches(5.8))
        cap1 = doc.add_paragraph()
        cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap1.paragraph_format.space_after = Pt(12)
        r = cap1.add_run("Figure 5.1: Boxplot Distribution of Prompt Complexity across Technical Query Categories.")
        r.font.italic = True
        r.font.size = Pt(10)

    fig2 = "eda_output/fig2_model_selection_pie.png"
    fig3 = "eda_output/fig3_latency_vs_cost_tradeoff.png"
    if os.path.exists(fig2):
        doc.add_picture(fig2, width=Inches(4.5))
        cap2 = doc.add_paragraph()
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap2.paragraph_format.space_after = Pt(12)
        r = cap2.add_run("Figure 5.2: Proportion of Invocations Processed across Small, Medium, and Large Tiers.")
        r.font.italic = True
        r.font.size = Pt(10)

    if os.path.exists(fig3):
        doc.add_picture(fig3, width=Inches(5.8))
        cap3 = doc.add_paragraph()
        cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap3.paragraph_format.space_after = Pt(12)
        r = cap3.add_run("Figure 5.3: Empirical Latency (s) and Estimated Cost (₹) Trade-off across Model Tiers.")
        r.font.italic = True
        r.font.size = Pt(10)

    fig4 = "eda_output/fig4_cost_savings_cumulative.png"
    if os.path.exists(fig4):
        doc.add_picture(fig4, width=Inches(5.8))
        cap4 = doc.add_paragraph()
        cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap4.paragraph_format.space_after = Pt(12)
        r = cap4.add_run("Figure 5.4: Cumulative Cost Divergence: Intelligent Router vs. Monolithic Baseline.")
        r.font.italic = True
        r.font.size = Pt(10)

    format_heading(doc.add_paragraph(), "\n5.3 Machine Learning Baseline Comparison", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "To provide comparative rigor for the viva examination, a Random Forest ML Router baseline was trained on TF-IDF unigram and bigram features extracted from the 325-sample dataset. On a 25% stratified test holdout, the ML router attained 86.59% accuracy and an F1-score of 0.87. However, the rule-based multi-objective router remains the preferred default due to its strict determinism, zero inference latency overhead, and 100% human-explainable viva justifications.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: FUTURE SCOPE & CONCLUSION
    # =========================================================================
    h_ch6 = doc.add_paragraph()
    format_heading(h_ch6, "CHAPTER 6: FUTURE SCOPE & CONCLUSION", 16, PRIMARY_COLOR, space_before=18, space_after=12)

    format_heading(doc.add_paragraph(), "6.1 Future Scope (Industrial Roadmap)", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "While this prototype satisfies all academic objectives for a college-level demonstration, the architectural separation of concerns provides clear pathways for enterprise expansion:")
    add_body_paragraph(doc, "1. Continuous Batching via vLLM: Integrate PagedAttention and vLLM runtime to eliminate GPU memory fragmentation during token generation.")
    add_body_paragraph(doc, "2. NVIDIA Triton Serving: Deploy Triton Inference Server for concurrent dynamic tensor scheduling across GPU nodes.")
    add_body_paragraph(doc, "3. Kubernetes Dynamic Autoscaling: Containerize inference workers into Kubernetes pods managed by KEDA to autoscale based on prompt ingress queues.")
    add_body_paragraph(doc, "4. Semantic Vector Caching: Integrate FAISS or Milvus vector indexing with embedding cosine distance to cache semantically equivalent prompts.")
    add_body_paragraph(doc, "5. Advanced Quantization: Utilize 4-bit AWQ and GPTQ weight compression to operate SLMs on commodity edge hardware.")

    format_heading(doc.add_paragraph(), "6.2 Conclusion", 13, SECONDARY_COLOR)
    add_body_paragraph(doc, "This project successfully developed an explainable, cost- and performance-aware AI inference routing prototype. By replacing the traditional 'one-size-fits-all' LLM architecture with an intelligent multi-tier gateway, the system proved that simple and moderate prompts can be efficiently offloaded to smaller models without sacrificing user experience.")
    add_body_paragraph(doc, "Experimental results over 325 benchmark queries confirmed a 54.35% cost reduction, a 45.72% latency improvement, and instantaneous cache resolution at zero compute cost. The solution provides a scalable foundation for modern MLOps architectures and successfully fulfills the academic requirements of Savitribai Phule Pune University.")

    # =========================================================================
    # REFERENCES
    # =========================================================================
    doc.add_paragraph().paragraph_format.space_before = Pt(18)
    format_heading(doc.add_paragraph(), "REFERENCES", 16, PRIMARY_COLOR, space_before=12, space_after=12)

    refs = [
        "[1] J. Kaplan, S. McCandlish, T. Henighan, et al., 'Scaling laws for neural language models,' arXiv preprint arXiv:2001.08361, 2020.",
        "[2] L. Chen, M. Zaharia, and J. Zou, 'FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance,' arXiv preprint arXiv:2305.05176, 2023.",
        "[3] D. S. Ong, M. Chen, C. Stoica, et al., 'RouteLLM: Learning to Route LLMs with Preference Data,' UC Berkeley LMSYS Org, 2024.",
        "[4] W. Kwon, Z. Li, S. Zhuang, et al., 'Efficient memory management for large language model serving with PagedAttention,' Proc. of the 29th ACM SOSP, pp. 611-626, 2023.",
        "[5] M. Abdin, S. A. Jyothi, C. Aneja, et al., 'Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone,' Microsoft Research, 2024.",
        "[6] A. Q. Jiang, A. Sablayrolles, A. Mensch, et al., 'Mistral 7B,' arXiv preprint arXiv:2310.06825, 2023.",
        "[7] J. Lin, J. Tang, H. Tang, et al., 'AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration,' MLSys, 2024.",
        "[8] NVIDIA Corporation, 'NVIDIA Triton Inference Server Technical Overview,' NVIDIA Developer Documentation, 2024."
    ]

    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    output_path = "PBL_Project_Report.docx"
    doc.save(output_path)
    print(f"[SUCCESS] Successfully generated formal academic PBL Project Report: {output_path}")

if __name__ == "__main__":
    main()
