"""Exp3: separação conforme o tamanho do texto e a janela do compressor."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.compress import ncd
from src.config import ROOT
from src.data import load_abstracts
from src.plots import save_figure, setup_style


def run(config: dict) -> None:
    abstracts = load_abstracts().query("split == 'train'")
    by_area = {area: group.text.to_numpy() for area, group in abstracts.groupby("area")}
    rng = np.random.default_rng(config["seed"])
    rows = []
    for size in config["exp3_sizes"]:
        samples = {}
        for area in config["areas"]:
            pair = []
            for _ in range(2):
                chunks: list[str] = []
                length = 0
                while length < size:
                    chunk = str(rng.choice(by_area[area]))
                    chunks.append(chunk)
                    length += len(chunk) + 1
                pair.append("\n".join(chunks)[:size])
            samples[area] = tuple(pair)
        for compressor in config["compressors"]:
            within = [ncd(first, second, compressor) for first, second in samples.values()]
            between = [ncd(samples[a][0], samples[b][0], compressor) for i, a in enumerate(config["areas"]) for b in config["areas"][i + 1:]]
            rows.append({"bytes": size, "compressor": compressor, "within": np.mean(within), "between": np.mean(between), "separation": np.mean(between) - np.mean(within), "gzip_window_bytes": 32768})
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
