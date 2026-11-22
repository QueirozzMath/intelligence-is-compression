"""Orquestra os experimentos na ordem de suas dependências."""
from __future__ import annotations

from importlib import import_module

EXPERIMENTS = [
    "exp0_languages", "exp1_compressibility", "exp2_ncd", "exp3_window",
    "exp4_cross_entropy", "exp5_words", "exp6_classification",
    "exp7_interdisciplinary", "exp8_robustness", "export_for_manim",
]


def run_all(config: dict) -> None:
    for name in EXPERIMENTS:
        print(f"[experimento] {name}", flush=True)
        import_module(f"src.experiments.{name}").run(config)

