"""Exp2: matrizes NCD, árvores e mapas MDS."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, dendrogram, linkage
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

from src.compress import ncd
from src.config import ROOT
from src.data import load_corpora
from src.experiments.utils import classical_mds, upper_values
from src.plots import AREA_COLORS, heatmap, save_figure, setup_style


def run(config: dict) -> None:
    corpora = load_corpora().query("split == 'train'").set_index("area")
    labels = config["areas"]
    matrices: dict[str, np.ndarray] = {}
    metric_rows = []
    for compressor in config["compressors"]:
        matrix = np.zeros((len(labels), len(labels)))
        for row, area_a in enumerate(labels):
            for column in range(row + 1, len(labels)):
                area_b = labels[column]
                value = ncd(corpora.loc[area_a, "text"][:config["ncd_sample_bytes"]], corpora.loc[area_b, "text"][:config["ncd_sample_bytes"]], compressor)
                matrix[row, column] = matrix[column, row] = value
        matrices[compressor] = matrix
        pd.DataFrame(matrix, index=labels, columns=labels).to_csv(ROOT / f"results/tables/exp2_ncd_{compressor}.csv")
        condensed = squareform(matrix, checks=False)
        tree = linkage(condensed, method="average")
        coefficient, _ = cophenet(tree, condensed)
        metric_rows.append({"metric": "cophenetic", "compressor_a": compressor, "compressor_b": compressor, "value": coefficient})
        heatmap(matrix, labels, f"A compressão {compressor} revela estrutura compartilhada entre áreas", f"exp2_ncd_heatmap_{compressor}")
        setup_style()
        fig, ax = plt.subplots()
        dendrogram(tree, labels=labels, orientation="right", ax=ax)
        ax.set(title=f"Áreas com linguagem parecida se fundem primeiro ({compressor})", xlabel="NCD")
        save_figure(fig, f"exp2_dendrogram_{compressor}")
        coordinates, eigenvalues = classical_mds(matrix)
        pd.DataFrame({"area": labels, "x": coordinates[:, 0], "y": coordinates[:, 1], "compressor": compressor}).to_csv(ROOT / f"results/tables/exp2_mds_{compressor}.csv", index=False)
        fig, ax = plt.subplots()
        for index, area in enumerate(labels):
            ax.scatter(*coordinates[index], s=180, color=AREA_COLORS[area])
            ax.annotate(area, coordinates[index], xytext=(7, 7), textcoords="offset points")
        ax.set(title=f"Um mapa 2D preserva as distâncias de compressão ({compressor})", xlabel="MDS 1", ylabel="MDS 2")
        save_figure(fig, f"exp2_mds_{compressor}")
    for index, first in enumerate(config["compressors"]):
        for second in config["compressors"][index + 1:]:
            metric_rows.append({"metric": "spearman", "compressor_a": first, "compressor_b": second, "value": spearmanr(upper_values(matrices[first]), upper_values(matrices[second])).statistic})
    pd.DataFrame(metric_rows).to_csv(ROOT / "results/tables/exp2_metrics.csv", index=False)

