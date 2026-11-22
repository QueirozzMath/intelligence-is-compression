"""Leitura e resolução da configuração do projeto."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_config(quick: bool = False) -> dict[str, Any]:
    """Carrega o YAML e aplica as substituições do modo rápido."""
    with (ROOT / "config.yaml").open(encoding="utf-8") as handle:
        config: dict[str, Any] = yaml.safe_load(handle)
    overrides = config.pop("quick", {})
    if quick:
        config.update(overrides)
    config["quick"] = quick
    return config


def ensure_directories() -> None:
    """Cria somente diretórios de saída previstos pelo projeto."""
    for relative in ("data/raw", "data/processed", "results/tables", "results/figures", "results/animations"):
        (ROOT / relative).mkdir(parents=True, exist_ok=True)

