"""Paleta, caminhos e componentes compartilhados pelas animações."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from manimlib import *

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
AREA_COLORS = {
    "math": "#0072B2", "astro-ph": "#E69F00", "cond-mat": "#009E73",
    "hep-th": "#CC79A7", "cs": "#56B4E9", "q-bio": "#D55E00",
    "stat": "#F0E442", "econ": "#8C564B", "physics": "#999999", "quant-ph": "#9467BD",
}


def table(name: str, **kwargs) -> pd.DataFrame:
    path = TABLES / name
    if not path.exists():
        raise FileNotFoundError(f"Execute `python -m src.cli all` antes do Manim: {path}")
    return pd.read_csv(path, **kwargs)


def json_data(name: str):
    return json.loads((TABLES / name).read_text(encoding="utf-8"))


def title(text: str) -> Text:
    return Text(text, font_size=44, color=WHITE).to_edge(UP)


def area_label(area: str, font_size: int = 28) -> Text:
    return Text(area, font_size=font_size, color=AREA_COLORS.get(area, WHITE))


def normalized_points(frame: pd.DataFrame, columns: tuple[str, ...], scale: float = 3.0) -> np.ndarray:
    values = frame[list(columns)].to_numpy(float)
    maximum = np.abs(values).max(axis=0)
    maximum[maximum == 0] = 1
    return values / maximum * scale

