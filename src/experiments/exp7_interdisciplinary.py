"""Exp7: artigos cross-listados ou misturas explicitamente simuladas."""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd

from src.config import ROOT
from src.data import load_abstracts, load_corpora
from src.experiments.exp4_cross_entropy import train_models
from src.plots import AREA_COLORS, save_figure, setup_style


def run(config: dict) -> None:
    frame = load_abstracts()
    train = load_corpora().query("split == 'train'").set_index("area").text.to_dict()
    models = train_models(train, min(6, max(config["ngram_orders"])))
    cross = frame[frame.cross_areas.map(bool)]
    simulated = cross.empty
    if simulated:
        pair = ("cs", "stat") if {"cs", "stat"}.issubset(config["areas"]) else tuple(config["areas"][:2])
    else:
        first = cross.iloc[0]
        pair = (first.area, first.cross_areas[0])
    area_a, area_b = pair
    rows = []
    for area, kind in ((area_a, "puro A"), (area_b, "puro B")):
        subset = frame.query("split == 'test' and area == @area").head(100)
        for record in subset.itertuples():
            rows.append({"id": record.id, "kind": kind, "area_a": area_a, "area_b": area_b, "bpc_a": models[area_a].cross_entropy(record.text), "bpc_b": models[area_b].cross_entropy(record.text), "simulated": False})
    if simulated:
        left = frame.query("split == 'test' and area == @area_a").head(100).text.tolist()
        right = frame.query("split == 'test' and area == @area_b").head(100).text.tolist()
        for index, (a, b) in enumerate(zip(left, right)):
            mixed = a[:len(a) // 2] + " " + b[len(b) // 2:]
            rows.append({"id": f"sim-{index}", "kind": "mistura simulada", "area_a": area_a, "area_b": area_b, "bpc_a": models[area_a].cross_entropy(mixed), "bpc_b": models[area_b].cross_entropy(mixed), "simulated": True})
    else:
        subset = cross[(cross.area == area_a) & cross.cross_areas.map(lambda values: area_b in values)].head(100)
        for record in subset.itertuples():
            rows.append({"id": record.id, "kind": "cross-list", "area_a": area_a, "area_b": area_b, "bpc_a": models[area_a].cross_entropy(record.text), "bpc_b": models[area_b].cross_entropy(record.text), "simulated": False})
    result = pd.DataFrame(rows)
    result.to_csv(ROOT / "results/tables/exp7_interdisciplinary.csv", index=False)
    (ROOT / "results/tables/exp7_metadata.json").write_text(json.dumps({"simulated": simulated, "pair": pair}, ensure_ascii=False, indent=2), encoding="utf-8")
    setup_style()
    fig, ax = plt.subplots()
    markers = {"puro A": "o", "puro B": "s", "cross-list": "*", "mistura simulada": "*"}
    for kind, group in result.groupby("kind"):
        ax.scatter(group.bpc_a, group.bpc_b, label=kind, marker=markers[kind], s=90 if "mistura" in kind or kind == "cross-list" else 45, alpha=0.75)
    ax.set(title=f"Textos interdisciplinares ocupam a fronteira entre {area_a} e {area_b}", xlabel=f"bpc sob modelo {area_a}", ylabel=f"bpc sob modelo {area_b}")
    ax.legend()
    save_figure(fig, "exp7_interdisciplinary")

