"""Deriva, de resultados reais, todas as tabelas consumidas pelo ManimGL."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

from src.compress import compressed_size
from src.config import ROOT
from src.data import load_abstracts, load_corpora
from src.experiments.exp4_cross_entropy import train_models
from src.experiments.utils import classical_mds
from src.ngram import CharNGramModel


def _pca(values: np.ndarray, dimensions: int = 3) -> tuple[np.ndarray, np.ndarray]:
    centered = values - values.mean(axis=0)
    u, singular, _ = np.linalg.svd(centered, full_matrices=False)
    coordinates = u[:, :dimensions] * singular[:dimensions]
    variance = singular ** 2 / max(1, len(values) - 1)
    return coordinates, variance[:dimensions] / variance.sum()


def run(config: dict) -> None:
    labels = config["areas"]
    matrix_frame = pd.read_csv(ROOT / "results/tables/exp2_ncd_lzma.csv", index_col=0).loc[labels, labels]
    matrix = matrix_frame.to_numpy()
    coordinates, eigenvalues = classical_mds(matrix, 3)
    pd.DataFrame({"area": labels, "x": coordinates[:, 0], "y": coordinates[:, 1], "z": coordinates[:, 2], "eigenvalue_1": eigenvalues[0], "eigenvalue_2": eigenvalues[1], "eigenvalue_3": eigenvalues[2]}).to_csv(ROOT / "results/tables/mds3d_areas.csv", index=False)
    tree = linkage(squareform(matrix, checks=False), method="average")
    pd.DataFrame(tree, columns=["left", "right", "height", "count"]).assign(step=range(len(tree))).to_csv(ROOT / "results/tables/dendrogram_linkage.csv", index=False)

    corpora = load_corpora()
    train = corpora.query("split == 'train'").set_index("area").text.to_dict()
    models = train_models(train, min(6, max(config["ngram_orders"])))
    abstracts = load_abstracts()
    selected = pd.concat([group.head(150) for _, group in abstracts.query("split == 'test'").groupby("area")], ignore_index=True)
    features = np.array([[models[area].cross_entropy(text) for area in labels] for text in selected.text])
    pca_coordinates, explained = _pca(features)
    pca = pd.DataFrame({"id": selected.id, "area": selected.area, "cross_list": selected.cross_areas.map(bool), "x": pca_coordinates[:, 0], "y": pca_coordinates[:, 1], "z": pca_coordinates[:, 2]})
    pca.to_csv(ROOT / "results/tables/pca3d_articles.csv", index=False)
    pd.DataFrame({"component": [1, 2, 3], "explained_variance_ratio": explained}).to_csv(ROOT / "results/tables/pca3d_explained_variance.csv", index=False)

    example_context = train[labels[0]][:500]
    context = example_context[-4:]
    distribution = models[labels[0]].distribution(context)
    pd.DataFrame(sorted(distribution.items(), key=lambda item: item[1], reverse=True)[:12], columns=["symbol", "probability"]).assign(context=context, area=labels[0]).to_csv(ROOT / "results/tables/manim_next_char.csv", index=False)

    ncd_pairs = []
    for row, area_a in enumerate(labels):
        for column in range(row + 1, len(labels)):
            ncd_pairs.append((matrix[row, column], area_a, labels[column]))
    ncd_pairs.sort()
    pair_records = []
    for pair_type, (_, area_a, area_b) in (("próximo", ncd_pairs[0]), ("distante", ncd_pairs[-1])):
        a, b = train[area_a][:config["ncd_sample_bytes"]], train[area_b][:config["ncd_sample_bytes"]]
        pair_records.append({"pair_type": pair_type, "area_a": area_a, "area_b": area_b, "bytes_a": len(a.encode()), "bytes_b": len(b.encode()), "compressed_a": compressed_size(a), "compressed_b": compressed_size(b), "compressed_ab": (compressed_size(a + b) + compressed_size(b + a)) / 2, "ncd": matrix[labels.index(area_a), labels.index(area_b)]})
    pd.DataFrame(pair_records).to_csv(ROOT / "results/tables/manim_ncd_examples.csv", index=False)

    predictions = pd.read_csv(ROOT / "results/tables/exp6_predictions.csv")
    article_scores = pd.read_csv(ROOT / "results/tables/exp6_article_bpc.csv")
    ngram_predictions = predictions[predictions.method == "n-grama"]
    examples = []
    for kind, subset in (("acerto", ngram_predictions[ngram_predictions.correct]), ("erro", ngram_predictions[~ngram_predictions.correct])):
        if subset.empty:
            continue
        record = subset.iloc[0]
        article = abstracts[abstracts.id == record.id].iloc[0]
        scores = article_scores[article_scores.id == record.id].iloc[0]
        examples.append({"kind": kind, "id": record.id, "text": article.text[:800], "true_area": record.true_area, "predicted_area": record.predicted_area, "bpc": {area: float(scores[area]) for area in labels}})
    (ROOT / "results/tables/manim_classification_examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2), encoding="utf-8")

    trio = sorted(distribution, key=distribution.get, reverse=True)[:3]
    total = sum(distribution[letter] for letter in trio)
    pd.DataFrame({"symbol": trio, "probability": [distribution[letter] / total for letter in trio]}).to_csv(ROOT / "results/tables/manim_simplex_p.csv", index=False)

