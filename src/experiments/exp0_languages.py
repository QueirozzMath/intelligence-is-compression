"""Exp0: validação qualitativa com traduções da UDHR."""
from __future__ import annotations

import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

from src.compress import ncd
from src.config import ROOT
from src.experiments.utils import upper_values
from src.plots import save_figure, setup_style


def run(config: dict) -> None:
    import matplotlib.pyplot as plt
    import nltk
    from nltk.corpus import udhr

    try:
        udhr.fileids()
    except LookupError:
        nltk.download("udhr", quiet=True)
    languages = {
        "Português": "Portuguese_Portugues-Latin1", "Espanhol": "Spanish_Espanol-Latin1",
        "Francês": "French_Francais-Latin1", "Italiano": "Italian_Italiano-Latin1",
        "Inglês": "English-Latin1", "Alemão": "German_Deutsch-Latin1", "Holandês": "Dutch_Nederlands-Latin1",
        "Sueco": "Swedish_Svenska-Latin1", "Polonês": "Polish-Latin2", "Tcheco": "Czech-Latin2",
        "Croata": "Croatian_Hrvatski-Latin2", "Esloveno": "Slovene_Slovenscina-Latin2",
    }
    available = set(udhr.fileids())
    languages = {name: file_id for name, file_id in languages.items() if file_id in available}
    labels, texts = list(languages), [udhr.raw(file_id)[:20000] for file_id in languages.values()]
    matrix = [[ncd(a, b, "bz2") for b in texts] for a in texts]
    frame = pd.DataFrame(matrix, index=labels, columns=labels)
    frame.to_csv(ROOT / "results/tables/exp0_udhr_ncd.csv")
    tree = linkage(squareform(frame.to_numpy(), checks=False), method="average")
    setup_style()
    fig, ax = plt.subplots()
    dendrogram(tree, labels=labels, orientation="right", ax=ax)
    ax.set_title("Um compressor comum recupera famílias linguísticas")
    ax.set_xlabel("NCD (bz2)")
    save_figure(fig, "exp0_udhr_dendrogram")

