"""Exp4: entropia cruzada, KL e escala de dados com n-gramas."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import ROOT
from src.data import load_corpora
from src.ngram import CharNGramModel
from src.plots import AREA_COLORS, heatmap, save_figure, setup_style


def train_models(train: dict[str, str], order: int) -> dict[str, CharNGramModel]:
    alphabet = set("".join(train.values()))
    return {area: CharNGramModel(order, alphabet).fit(text) for area, text in train.items()}


def run(config: dict) -> None:
    corpora = load_corpora()
    train = corpora.query("split == 'train'").set_index("area").text.to_dict()
    test = corpora.query("split == 'test'").set_index("area").text.to_dict()
    labels = config["areas"]
    order = max(config["ngram_orders"])
    models = train_models(train, order)
    cross = np.array([[models[model_area].cross_entropy(test[text_area]) for model_area in labels] for text_area in labels])
    diagonal = np.diag(cross)
    kl = np.maximum(0.0, cross - diagonal[:, None])
    pd.DataFrame(cross, index=labels, columns=labels).to_csv(ROOT / "results/tables/exp4_cross_entropy.csv")
    pd.DataFrame(kl, index=labels, columns=labels).to_csv(ROOT / "results/tables/exp4_kl.csv")
    heatmap(cross, labels, "O modelo da própria área geralmente gasta menos bits", "exp4_cross_entropy", "magma")
    heatmap(kl, labels, "Bits extras revelam a direção da diferença entre áreas", "exp4_kl", "magma")
    pairs = []
    for row, a in enumerate(labels):
        for column in range(row + 1, len(labels)):
            b = labels[column]
            pairs.append({"area_a": a, "area_b": b, "kl_a_b": kl[row, column], "kl_b_a": kl[column, row], "asymmetry": kl[row, column] - kl[column, row]})
    asymmetry = pd.DataFrame(pairs).sort_values("asymmetry", key=abs, ascending=False)
    asymmetry.to_csv(ROOT / "results/tables/exp4_asymmetry.csv", index=False)
    setup_style()
    shown = asymmetry.head(12).sort_values("asymmetry")
    fig, ax = plt.subplots()
    ax.barh(shown.area_a + " → " + shown.area_b, shown.asymmetry, color=np.where(shown.asymmetry >= 0, "#D55E00", "#0072B2"))
    ax.axvline(0, color="black", linewidth=1)
    ax.set(title="A divergência depende da direção da comparação", xlabel="KL(A‖B) − KL(B‖A), bits/caractere")
    save_figure(fig, "exp4_kl_asymmetry")

    sizes = sorted({min(len(next(iter(train.values()))), value) for value in (1000, 3000, 10000, 30000, 100000, 300000, 1000000)})
    loss_rows = []
    alphabet = set("".join(train.values()))
    curve_order = min(4, order)
    for area in labels:
        for size in sizes:
            model = CharNGramModel(curve_order, alphabet).fit(train[area][:size])
            loss_rows.append({"area": area, "train_chars": size, "bpc": model.cross_entropy(test[area])})
    loss = pd.DataFrame(loss_rows)
    loss.to_csv(ROOT / "results/tables/exp4_loss_curve.csv", index=False)
    fig, ax = plt.subplots()
    for area, group in loss.groupby("area"):
        ax.plot(group.train_chars, group.bpc, marker="o", label=area, color=AREA_COLORS[area])
    ax.set_xscale("log")
    ax.set(title="Mais dados permitem códigos melhores, com retornos decrescentes", xlabel="caracteres de treino (log)", ylabel="entropia cruzada no teste (bits/caractere)")
    ax.legend(ncol=5)
    save_figure(fig, "exp4_loss_vs_data")

