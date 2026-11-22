"""Estilo único e helpers para figuras de apresentação."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from src.config import ROOT

AREA_COLORS = {
    "math": "#0072B2", "astro-ph": "#E69F00", "cond-mat": "#009E73",
    "hep-th": "#CC79A7", "cs": "#56B4E9", "q-bio": "#D55E00",
    "stat": "#F0E442", "econ": "#8C564B", "physics": "#999999", "quant-ph": "#9467BD",
}


def setup_style() -> None:
    plt.rcParams.update({
        "figure.figsize": (16, 9), "font.size": 15, "axes.titlesize": 21,
        "axes.labelsize": 16, "legend.fontsize": 13, "figure.facecolor": "white",
        "axes.spines.top": False, "axes.spines.right": False,
    })


def save_figure(fig: Any, name: str) -> None:
    output = ROOT / "results" / "figures"
    output.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(output / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def heatmap(matrix: np.ndarray, labels: list[str], title: str, name: str, cmap: str = "viridis") -> None:
    setup_style()
    fig, ax = plt.subplots()
    image = ax.imshow(matrix, cmap=cmap)
    ax.set(xticks=range(len(labels)), yticks=range(len(labels)), xticklabels=labels, yticklabels=labels, title=title)
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    for row in range(len(labels)):
        for column in range(len(labels)):
            ax.text(column, row, f"{matrix[row, column]:.2f}", ha="center", va="center", color="white" if matrix[row, column] > np.nanmean(matrix) else "black", fontsize=11)
    fig.colorbar(image, ax=ax, shrink=0.8)
    save_figure(fig, name)
