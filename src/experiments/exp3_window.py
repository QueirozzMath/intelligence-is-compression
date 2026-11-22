"""Exp3: separação conforme o tamanho do texto e a janela do compressor."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.compress import ncd
from src.config import ROOT
from src.data import load_corpora
from src.plots import save_figure, setup_style


def run(config: dict) -> None:
    corpora = load_corpora().query("split == 'train'").set_index("area")
    rows = []
    for size in config["exp3_sizes"]:
        halves = {area: (text[:size], text[size:size * 2]) for area, text in corpora.text.items()}
        for compressor in config["compressors"]:
            within = [ncd(first, second, compressor) for first, second in halves.values() if second]
            between = [ncd(halves[a][0], halves[b][0], compressor) for i, a in enumerate(config["areas"]) for b in config["areas"][i + 1:]]
            rows.append({"bytes": size, "compressor": compressor, "within": np.mean(within), "between": np.mean(between), "separation": np.mean(between) - np.mean(within)})
    frame = pd.DataFrame(rows)
    frame.to_csv(ROOT / "results/tables/exp3_window.csv", index=False)
    setup_style()
    fig, ax = plt.subplots()
    for compressor, group in frame.groupby("compressor"):
        ax.plot(group.bytes, group.separation, marker="o", linewidth=3, label=compressor)
    ax.set_xscale("log")
    ax.axvline(32768, linestyle="--", color="gray", label="janela gzip (32 KB)")
    ax.set(title="A janela curta do gzip limita a memória sobre textos longos", xlabel="bytes por amostra", ylabel="separação entre áreas")
    ax.legend()
    save_figure(fig, "exp3_compressor_window")
