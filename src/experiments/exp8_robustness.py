"""Exp8: estabilidade da árvore e intervalos bootstrap de classificação."""
from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

from src.compress import ncd
from src.config import ROOT
from src.data import load_abstracts


def _clusters(tree: np.ndarray, labels: list[str]) -> set[frozenset[str]]:
    root = to_tree(tree)
    result: set[frozenset[str]] = set()
    def visit(node) -> set[str]:
        if node.is_leaf():
            return {labels[node.id]}
        members = visit(node.left) | visit(node.right)
        if 1 < len(members) < len(labels):
            result.add(frozenset(members))
        return members
    visit(root)
    return result


def run(config: dict) -> None:
    frame = load_abstracts().query("split == 'train'")
    labels = config["areas"]
    rng = np.random.default_rng(config["seed"])
    counts: Counter[frozenset[str]] = Counter()
    for _ in range(config["bootstrap_samples"]):
        texts = {}
        for area in labels:
            values = frame[frame.area == area].text.to_numpy()
            sample = rng.choice(values, size=len(values), replace=True)
            texts[area] = "\n".join(sample)[:config["ncd_sample_bytes"]]
        matrix = np.zeros((len(labels), len(labels)))
        for row, a in enumerate(labels):
            for column in range(row + 1, len(labels)):
                matrix[row, column] = matrix[column, row] = ncd(texts[a], texts[labels[column]], "lzma")
        counts.update(_clusters(linkage(squareform(matrix, checks=False), method="average"), labels))
    pd.DataFrame([{"cluster": "|".join(sorted(cluster)), "support": count / config["bootstrap_samples"]} for cluster, count in counts.items()]).sort_values("support", ascending=False).to_csv(ROOT / "results/tables/exp8_cluster_support.csv", index=False)

    predictions = pd.read_csv(ROOT / "results/tables/exp6_predictions.csv")
    rows = []
    for method, group in predictions.groupby("method"):
        articles = group[["id", "correct"]].drop_duplicates("id")
        estimates = []
        for _ in range(max(100, config["bootstrap_samples"])):
            estimates.append(rng.choice(articles.correct.to_numpy(), size=len(articles), replace=True).mean())
        rows.append({"method": method, "accuracy": articles.correct.mean(), "ci_low": np.quantile(estimates, 0.025), "ci_high": np.quantile(estimates, 0.975)})
    pd.DataFrame(rows).to_csv(ROOT / "results/tables/exp8_accuracy_ci.csv", index=False)
