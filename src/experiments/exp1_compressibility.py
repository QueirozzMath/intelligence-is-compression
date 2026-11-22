"""Exp1: compressibilidade e entropia empírica por área."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.compress import bits_per_character, compressed_size
from src.config import ROOT
from src.data import load_corpora
from src.ngram import empirical_entropy
from src.plots import AREA_COLORS, save_figure, setup_style


def run(config: dict) -> None:
    corpora = load_corpora().query("split == 'train'")
    rows = []
    for record in corpora.itertuples():
        original = len(record.text.encode("utf-8"))
        for compressor in config["compressors"]:
            rows.append({"area": record.area, "kind": "compressor", "method": compressor, "value": bits_per_character(record.text, compressor), "ratio": compressed_size(record.text, compressor) / original})
        for order in (0, 1, 2):
            rows.append({"area": record.area, "kind": "entropy", "method": f"H{order}", "value": empirical_entropy(record.text, order), "ratio": None})
    frame = pd.DataFrame(rows)
    frame.to_csv(ROOT / "results/tables/exp1_compressibility.csv", index=False)
    setup_style()
    compressed = frame.query("kind == 'compressor'")
    pivot = compressed.pivot(index="area", columns="method", values="value").reindex(config["areas"])
    fig, ax = plt.subplots()
    pivot.plot.bar(ax=ax, color=["#0072B2", "#E69F00", "#009E73"])
    ax.set(title="Áreas diferem em previsibilidade até para compressores genéricos", ylabel="bits por caractere", xlabel="Área")
    save_figure(fig, "exp1_bpc_compressors")
    entropy = frame.query("kind == 'entropy'").pivot(index="method", columns="area", values="value")
    fig, ax = plt.subplots()
    for area in entropy.columns:
        ax.plot([0, 1, 2], entropy[area], marker="o", label=area, color=AREA_COLORS[area])
    ax.set(title="Mais contexto reduz a incerteza sobre o próximo caractere", xlabel="Ordem do modelo", ylabel="entropia (bits/caractere)", xticks=[0, 1, 2])
    ax.legend(ncol=5)
    save_figure(fig, "exp1_entropy_by_order")

