"""Figure generation script for standardized thesis visuals.

Generates:
1. Return trajectories with confidence bands
2. Improvement bar chart
3. Baseline performance comparison
4. Reward shaping illustration placeholder (requires raw reward components)
5. Stability index trend

Usage: python -m analysis.generate_thesis_figures --results data.csv --out figs/
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import List, Dict

import math

try:
    import matplotlib.pyplot as plt  # type: ignore
except ImportError:
    plt = None  # type: ignore

from .metrics import summarize_returns


def read_results(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def improvement_bar(results: List[Dict[str, str]], out: Path):
    if plt is None:
        return
    exps = [r["Experiment"] for r in results]
    vals = [float(r["Improvement"]) for r in results]
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(exps, vals, color="#4B7BEC")
    ax.set_ylabel("Improvement (Return Δ)")
    ax.set_xlabel("Experiment")
    ax.set_title("Episodic Return Improvement Across Experiments")
    ax.tick_params(axis='x', rotation=45, ha='right')
    fig.tight_layout()
    fig.savefig(out / "improvement_bar.png", dpi=220)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    results = read_results(args.results)
    improvement_bar(results, args.out)

if __name__ == "__main__":
    main()
