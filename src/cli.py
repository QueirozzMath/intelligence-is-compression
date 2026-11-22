"""Interface de linha de comando do pipeline."""
from __future__ import annotations

import argparse

from src.config import ensure_directories, load_config
from src.data import prepare_data
from src.experiments.runner import run_all
from src.reporting import verify_outputs, write_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Compressão é inteligência")
    parser.add_argument("command", choices=["data", "experiments", "figures", "all", "verify"])
    parser.add_argument("--quick", action="store_true", help="Executa a mesma lógica com amostras menores")
    parser.add_argument("--download", action="store_true", help="Tenta a API oficial quando não há dump")
    arguments = parser.parse_args()
    config = load_config(arguments.quick)
    ensure_directories()
    if arguments.command in {"data", "all"}:
        prepare_data(config, arguments.download)
    if arguments.command in {"experiments", "figures", "all"}:
        run_all(config)
        write_summary()
    if arguments.command in {"verify", "all"}:
        missing = verify_outputs()
        if missing:
            raise SystemExit("Entregáveis ausentes:\n- " + "\n- ".join(missing))
        print("Todos os entregáveis tabulares obrigatórios foram gerados.")


if __name__ == "__main__":
    main()
