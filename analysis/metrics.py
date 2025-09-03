"""Metrics and statistical analysis utilities for Cyberwheel thesis.

Implements core aggregation, confidence intervals, effect sizes, and custom
cyber defense metrics (deception efficacy, protection success, etc.).

All functions are pure (no side effects) to facilitate deterministic testing.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Dict, Any, Tuple
import math
import statistics as stats

try:
    import numpy as np  # type: ignore
except ImportError:  # minimal fallback
    np = None  # type: ignore

# ---------------- Core Statistical Utilities ---------------- #

def mean(values: Sequence[float]) -> float:
    return float(sum(values) / len(values)) if values else float('nan')

def std(values: Sequence[float], ddof: int = 1) -> float:
    if len(values) <= ddof:
        return float('nan')
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - ddof))

@dataclass
class Interval:
    lower: float
    upper: float
    level: float


def t_confidence_interval(values: Sequence[float], level: float = 0.95) -> Interval:
    """Student t CI for small samples. Falls back to normal approx if numpy/scipy unavailable.
    """
    n = len(values)
    if n < 2:
        return Interval(float('nan'), float('nan'), level)
    m = mean(values)
    s = std(values)
    if np is None:
        # Normal approx
        from math import erf, sqrt
        # z ~ 1.96 for 95%
        z = 1.96 if abs(level - 0.95) < 1e-6 else 1.96
        half = z * s / math.sqrt(n)
        return Interval(m - half, m + half, level)
    else:
        import scipy.stats as st  # type: ignore
        tcrit = st.t.ppf(0.5 + level / 2, df=n - 1)
        half = tcrit * s / math.sqrt(n)
        return Interval(m - half, m + half, level)

# ---------------- Effect Sizes ---------------- #

def cohens_d(group1: Sequence[float], group2: Sequence[float]) -> float:
    if len(group1) < 2 or len(group2) < 2:
        return float('nan')
    m1, m2 = mean(group1), mean(group2)
    s1, s2 = std(group1), std(group2)
    # pooled std
    n1, n2 = len(group1), len(group2)
    pooled = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    if pooled == 0:
        return 0.0
    return (m1 - m2) / pooled

# ---------------- Cyber Defense Derived Metrics ---------------- #

def deception_efficacy(decoy_contacts: int, hostile_contacts: int) -> float:
    if hostile_contacts <= 0:
        return float('nan')
    return decoy_contacts / hostile_contacts

def protection_success(prevented: int, attempts: int) -> float:
    if attempts <= 0:
        return float('nan')
    return prevented / attempts

def decoy_efficiency(decoy_contacts: int, hostile_contacts: int, avg_active_decoys: float) -> float:
    base = deception_efficacy(decoy_contacts, hostile_contacts)
    if math.isnan(base) or avg_active_decoys <= 0:
        return float('nan')
    return base / avg_active_decoys

def stability_index(returns: Sequence[float], window: int = 50) -> float:
    if len(returns) < window:
        return float('nan')
    segment = returns[-window:]
    return std(segment, ddof=0)

# Rolling action entropy could be added when raw policy/action distribution accessible.

# ---------------- Aggregate Pipeline ---------------- #

def summarize_returns(returns: Sequence[float]) -> Dict[str, Any]:
    ci = t_confidence_interval(returns)
    return {
        "n": len(returns),
        "mean": mean(returns),
        "std": std(returns),
        "ci_lower": ci.lower,
        "ci_upper": ci.upper,
        "ci_level": ci.level,
    }

# Placeholder for ANOVA / non-parametric tests (to be implemented when multiple groups available)

def placeholder_anova(groups: Dict[str, Sequence[float]]) -> Dict[str, Any]:
    return {"implemented": False, "k": len(groups)}

__all__ = [
    "mean","std","Interval","t_confidence_interval","cohens_d","deception_efficacy",
    "protection_success","decoy_efficiency","stability_index","summarize_returns","placeholder_anova"
]
