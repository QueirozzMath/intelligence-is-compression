"""Exp8: estabilidade da árvore e intervalos bootstrap de classificação."""
from __future__ import annotations

from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from scipy.spatial.distance import squareform

from src.compress import ncd
from src.config import ROOT
from src.data import load_abstracts
from src.plots import save_figure, setup_style


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
    support = {cluster: count / config["bootstrap_samples"] for cluster, count in counts.items()}
    pd.DataFrame([{"cluster": "|".join(sorted(cluster)), "support": value} for cluster, value in support.items()]).sort_values("support", ascending=False).to_csv(ROOT / "results/tables/exp8_cluster_support.csv", index=False)

    base_matrix = pd.read_csv(ROOT / "results/tables/exp2_ncd_lzma.csv", index_col=0).loc[labels, labels].to_numpy()
    base_tree = linkage(squareform(base_matrix, checks=False), method="average")
    setup_style()
    fig, ax = plt.subplots()
    rendered = dendrogram(base_tree, labels=labels, orientation="right", ax=ax)
    leaf_y = {leaf_id: 5.0 + 10.0 * position for position, leaf_id in enumerate(rendered["leaves"])}

    def annotate(node) -> tuple[set[str], float]:
        if node.is_leaf():
            return {labels[node.id]}, leaf_y[node.id]
        left_members, left_y = annotate(node.left)
        right_members, right_y = annotate(node.right)
        members = left_members | right_members
        y = (left_y + right_y) / 2
        if len(members) < len(labels):
            ax.annotate(f"{100 * support.get(frozenset(members), 0):.0f}%", (node.dist, y), xytext=(5, 0), textcoords="offset points", va="center", fontsize=11, color="#D55E00")
        return members, y

    annotate(to_tree(base_tree))
    ax.set(title="Os ramos persistentes sobrevivem ao bootstrap dos resumos", xlabel="NCD (LZMA)")
    save_figure(fig, "exp8_dendrogram_stability")

    predictions = pd.read_csv(ROOT / "results/tables/exp6_predictions.csv")
    rows = []
    for method, group in predictions.groupby("method"):
        articles = group[["id", "correct"]].drop_duplicates("id")
        estimates = []
        for _ in range(max(100, config["bootstrap_samples"])):
            estimates.append(rng.choice(articles.correct.to_numpy(), size=len(articles), replace=True).mean())
        rows.append({"method": method, "accuracy": articles.correct.mean(), "ci_low": np.quantile(estimates, 0.025), "ci_high": np.quantile(estimates, 0.975)})
    intervals = pd.DataFrame(rows)
    intervals.to_csv(ROOT / "results/tables/exp8_accuracy_ci.csv", index=False)
    fig, ax = plt.subplots()
    errors = np.vstack([intervals.accuracy - intervals.ci_low, intervals.ci_high - intervals.accuracy])
    ax.bar(intervals.method, intervals.accuracy, color="#0072B2", yerr=errors, capsize=8)
    ax.set(title="A incerteza da classificação é visível nos ICs bootstrap", ylabel="acurácia (IC 95%)", ylim=(0, 1))
    ax.tick_params(axis="x", rotation=20)
    save_figure(fig, "exp8_accuracy_intervals")
