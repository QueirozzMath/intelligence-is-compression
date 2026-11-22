"""Exp5: palavras que mais contribuem para a divergência entre áreas."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import ROOT
from src.data import WORD, load_corpora
from src.ngram import WordUnigramModel, kl_word_contributions
from src.plots import save_figure, setup_style


def run(config: dict) -> None:
    corpora = load_corpora().query("split == 'train'").set_index("area")
    models = {area: WordUnigramModel().fit(WORD.findall(corpora.loc[area, "text"])) for area in config["areas"]}
    matrix = pd.read_csv(ROOT / "results/tables/exp2_ncd_lzma.csv", index_col=0)
    pairs = [(a, b, matrix.loc[a, b]) for i, a in enumerate(config["areas"]) for b in config["areas"][i + 1:]]
    pairs.sort(key=lambda item: item[2])
    chosen = [("próximo", *pairs[0]), ("intermediário", *pairs[len(pairs) // 2]), ("distante", *pairs[-1])]
    rows = []
    setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(20, 9))
    for ax, (distance_class, area_a, area_b, distance) in zip(axes, chosen):
        contributions = kl_word_contributions(models[area_a], models[area_b])
        top = sorted(contributions.items(), key=lambda item: item[1], reverse=True)[:15]
        for rank, (word, value) in enumerate(top, 1):
            rows.append({"pair_type": distance_class, "area_a": area_a, "area_b": area_b, "ncd": distance, "rank": rank, "word": word, "contribution": value})
        words, values = zip(*reversed(top))
        ax.barh(words, values, color="#0072B2")
        ax.set_title(f"{distance_class}: {area_a} → {area_b}")
        ax.set_xlabel("contribuição para KL (bits)")
    fig.suptitle("Poucas palavras especializadas carregam grande parte da diferença", fontsize=22)
    save_figure(fig, "exp5_word_contributions")
    pd.DataFrame(rows).to_csv(ROOT / "results/tables/exp5_word_contributions.csv", index=False)
