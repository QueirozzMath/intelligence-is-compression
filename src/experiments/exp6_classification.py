"""Exp6: classificação individual por NCD, n-gramas e TF-IDF."""
from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.preprocessing import normalize

from src.compress import ncd
from src.config import ROOT
from src.data import load_abstracts, load_corpora
from src.experiments.exp4_cross_entropy import train_models
from src.plots import save_figure, setup_style


def _ncd_job(arguments: tuple[str, str, str]) -> float:
    return ncd(arguments[0], arguments[1], arguments[2])


def _evaluate(name: str, truth: list[str], prediction: list[str], labels: list[str]) -> tuple[dict, np.ndarray]:
    matrix = confusion_matrix(truth, prediction, labels=labels, normalize="true")
    return ({"method": name, "accuracy": accuracy_score(truth, prediction), "f1_macro": f1_score(truth, prediction, average="macro")}, matrix)


def run(config: dict) -> None:
    frame = load_abstracts()
    labels = config["areas"]
    train = frame.query("split == 'train'")
    test = frame.query("split == 'test'")
    rng = np.random.default_rng(config["seed"])
    references = pd.concat([group.sample(min(len(group), config["exp6_reference_per_area"]), random_state=config["seed"]) for _, group in train.groupby("area")], ignore_index=True)
    tests = pd.concat([group.sample(min(len(group), config["exp6_test_per_area"]), random_state=config["seed"]) for _, group in test.groupby("area")], ignore_index=True)
    truth = tests.area.tolist()

    corpus = load_corpora().query("split == 'train'").set_index("area").text.to_dict()
    models = train_models(corpus, min(6, max(config["ngram_orders"])))
    cross_scores = np.array([[models[area].cross_entropy(text) for area in labels] for text in tests.text])
    pred_ngram = [labels[index] for index in cross_scores.argmin(axis=1)]

    vectorizer = TfidfVectorizer(min_df=2, max_features=50000, ngram_range=(1, 2), sublinear_tf=True)
    train_matrix = vectorizer.fit_transform(train.text)
    test_matrix = vectorizer.transform(tests.text)
    centroids = np.vstack([np.asarray(train_matrix[train.area.to_numpy() == area].mean(axis=0)).ravel() for area in labels])
    centroids = normalize(centroids)
    pred_tfidf = [labels[index] for index in np.asarray(test_matrix @ centroids.T).argmax(axis=1)]

    cache = ROOT / "results/tables/exp6_ncd_distances.csv"
    if cache.exists():
        distances = pd.read_csv(cache).distance.to_numpy().reshape(len(tests), len(references))
    else:
        jobs = [(text, reference, "lzma") for text in tests.text for reference in references.text]
        workers = min(8, max(1, __import__("os").cpu_count() or 1))
        with ProcessPoolExecutor(max_workers=workers) as executor:
            values = list(executor.map(_ncd_job, jobs, chunksize=max(1, len(jobs) // (workers * 20))))
        distances = np.array(values).reshape(len(tests), len(references))
        pd.DataFrame({"test_id": np.repeat(tests.id.to_numpy(), len(references)), "reference_id": np.tile(references.id.to_numpy(), len(tests)), "distance": distances.ravel()}).to_csv(cache, index=False)
    nearest = distances.argsort(axis=1)
    pred_ncd1 = references.area.to_numpy()[nearest[:, 0]].tolist()
    pred_ncd5 = [Counter(references.area.to_numpy()[row[:5]]).most_common(1)[0][0] for row in nearest]

    predictions = {"NCD k=1": pred_ncd1, "NCD k=5": pred_ncd5, "n-grama": pred_ngram, "TF-IDF": pred_tfidf}
    metrics, matrices, detail_rows = [], {}, []
    for method, prediction in predictions.items():
        metric, matrix = _evaluate(method, truth, prediction, labels)
        metrics.append(metric)
        matrices[method] = matrix
        detail_rows.extend({"id": article_id, "true_area": actual, "predicted_area": predicted, "method": method, "correct": actual == predicted} for article_id, actual, predicted in zip(tests.id, truth, prediction))
    pd.DataFrame(metrics).to_csv(ROOT / "results/tables/exp6_metrics.csv", index=False)
    pd.DataFrame(detail_rows).to_csv(ROOT / "results/tables/exp6_predictions.csv", index=False)
    pd.DataFrame(cross_scores, columns=labels).assign(id=tests.id.to_numpy(), true_area=truth).to_csv(ROOT / "results/tables/exp6_article_bpc.csv", index=False)

    setup_style()
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    for ax, (method, matrix) in zip(axes.flat, matrices.items()):
        image = ax.imshow(matrix, vmin=0, vmax=1, cmap="Blues")
        ax.set(title=method, xticks=range(len(labels)), yticks=range(len(labels)), xticklabels=labels, yticklabels=labels)
        ax.tick_params(axis="x", rotation=45)
    fig.suptitle("Métodos simples revelam quais áreas compartilham vocabulário e estrutura", fontsize=22)
    save_figure(fig, "exp6_confusion_matrices")
    metric_frame = pd.DataFrame(metrics)
    fig, ax = plt.subplots()
    metric_frame.set_index("method")[["accuracy", "f1_macro"]].plot.bar(ax=ax, color=["#0072B2", "#E69F00"])
    ax.set(title="Entropia cruzada compete com um baseline lexical forte", ylabel="pontuação", ylim=(0, 1))
    save_figure(fig, "exp6_method_comparison")

