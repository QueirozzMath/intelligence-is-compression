"""Resumo automático e verificação dos entregáveis produzidos."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ROOT


def write_summary() -> None:
    exp1 = pd.read_csv(ROOT / "results/tables/exp1_compressibility.csv").query("kind == 'compressor' and method == 'lzma'").sort_values("value")
    ncd = pd.read_csv(ROOT / "results/tables/exp2_ncd_lzma.csv", index_col=0)
    pairs = sorted((ncd.loc[a, b], a, b) for index, a in enumerate(ncd.index) for b in ncd.index[index + 1:])
    metrics = pd.read_csv(ROOT / "results/tables/exp6_metrics.csv")
    lines = ["# Resumo dos resultados", "", "Todos os valores abaixo são lidos dos CSVs gerados pelo pipeline.", "", "## Bits por caractere (LZMA)", "", exp1[["area", "value"]].rename(columns={"value": "bpc"}).to_markdown(index=False), "", "## Pares NCD", "", f"- Mais próximo: **{pairs[0][1]} ↔ {pairs[0][2]}** ({pairs[0][0]:.3f})", f"- Mais distante: **{pairs[-1][1]} ↔ {pairs[-1][2]}** ({pairs[-1][0]:.3f})", "", "## Classificação", "", metrics.to_markdown(index=False), ""]
    (ROOT / "results/summary.md").write_text("\n".join(lines), encoding="utf-8")


def verify_outputs() -> list[str]:
    required = [
        "results/tables/corpus_stats.csv", "results/tables/exp1_compressibility.csv",
        "results/tables/exp2_ncd_lzma.csv", "results/tables/exp3_window.csv",
        "results/tables/exp4_cross_entropy.csv", "results/tables/exp5_word_contributions.csv",
        "results/tables/exp6_metrics.csv", "results/tables/exp7_interdisciplinary.csv",
        "results/tables/exp8_cluster_support.csv", "results/tables/mds3d_areas.csv",
        "results/tables/pca3d_articles.csv", "results/summary.md",
    ]
    missing = [relative for relative in required if not (ROOT / relative).exists()]
    (ROOT / "results/manifest.txt").write_text("\n".join(f"{'MISSING' if item in missing else 'OK'} {item}" for item in required), encoding="utf-8")
    return missing

