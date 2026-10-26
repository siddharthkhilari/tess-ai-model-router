# Routing Algorithm & Mathematical Formulation

## 1. Complexity Scoring
Input prompt $P$ is analyzed for syntactic and domain features:
- Word Count: $+1$ if $|W| > 50$, $+1$ if $|W| > 150$
- System/Architecture Keywords: $+4$ points
- Coding Keywords: $+2$ points
- Reasoning / Analysis Keywords: $+1$ point
- Compound Clauses ("and", "also", "step by step"): $+1$ point
- Long-form Requests: $+1$ point

Score normalization:
$$C(P) = \min\left(1.0, \max\left(0.15, \frac{\sum \text{Points}}{6}\right)\right)$$

### Complexity Tiers:
- **LOW:** $0.00 \le C(P) < 0.40 \longrightarrow$ Small Model (SLM)
- **MEDIUM:** $0.40 \le C(P) < 0.70 \longrightarrow$ Medium Model
- **HIGH:** $0.70 \le C(P) \le 1.00 \longrightarrow$ Large Model (LLM)

## 2. Multi-Objective Utility Function
For candidate model $M_i$:
$$U(M_i) = w_q \cdot Q(M_i) - w_c \cdot C(M_i) - w_l \cdot L(M_i) - \text{Penalty}$$
Where:
- $w_q = 0.50$ (Quality Weight)
- $w_c = 0.30$ (Cost Weight)
- $w_l = 0.20$ (Latency Weight)
- $Q(M_i) \in [0, 1]$: normalized model quality score
- $C(M_i) \in [0, 1]$: normalized cost
- $L(M_i) \in [0, 1]$: normalized latency
- $\text{Penalty} = 2.0 \cdot \max(0, C(P) - Q(M_i))$ (prevents selecting underpowered models for high-complexity queries)

## 3. Privacy Constraint Policy
$$\text{If } \text{Privacy}(P) == \text{SENSITIVE} \implies \text{Route}(P) = \text{Small Model (Local Safe Perimeter)}$$
Ensures zero external cloud data exposure.
