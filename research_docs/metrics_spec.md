# Cyberwheel Advanced Metrics Specification

Defines formal metrics integrated into thesis (implementation status tracked in benchmark).

## Core Statistical Metrics
| Metric | Symbol | Definition | Notes |
|--------|--------|------------|-------|
| Mean Return | \(\mu\) | \(\frac{1}{n}\sum_{i=1}^n R_i\) | Episodic aggregate |
| Std Dev | \(\sigma\) | \(\sqrt{\frac{1}{n-1}\sum (R_i-\mu)^2}\) | Sample std |
| 95% CI | CI | Student t or bootstrap | Use t for n<10 fallback bootstrap |
| Cohen's d | d | \((\mu_1-\mu_2)/s_p\) | Effect size baseline vs PPO |

## Defense-Specific Metrics
| Metric | Symbol | Definition | Interpretation |
|--------|--------|------------|----------------|
| Deception Efficacy Rate | DER | decoy_contacts / hostile_contacts | Higher → better red diversion |
| Protection Success Rate | PSR | prevented / attempts | Defensive blocking ability |
| Decoy Efficiency Index | DEI | DER / avg_active_decoys | Resource-normalized deception |
| Stability Index | SI | std(windowed returns) | Lower → convergence stability |
| Action Entropy | H | \(-\sum_a p(a)\log p(a)\) | Exploration vs exploitation |
| Time-to-Impact Median | TTI | median first-impact step | Delaying attacker |
| Resource Cost Normalized Return | RCNR | return / total_defense_cost | Efficiency |

## Pending / Conditional Metrics
| Metric | Condition | Action |
|--------|----------|--------|
| False Attraction Ratio (FAR) | Requires benign event modeling | Defer if absent |
| Survival Curve (Kaplan–Meier) | Sufficient censoring events | Optional extension |

## Data Requirements
- Logging schema update: record per-episode decoy contacts, hostile contacts, prevented compromises, active decoys, total defense cost.
- Policy distribution snapshot every k episodes for action entropy.

## Implementation Notes
- All metric computations must be pure functions (see `analysis/metrics.py`).
- Figures: unify color palette (primary #4B7BEC, accent #E67E22, neutral #2D3436, success #27AE60, danger #C0392B).
- Provide LaTeX export (JSON→TeX) script for embedding tables.
