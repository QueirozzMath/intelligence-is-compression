"""Intelligence is Compression: teoria da informação aplicada ao arXiv."""
import os

# O pipeline sempre salva figuras em disco; não deve depender de uma sessão gráfica.
os.environ.setdefault("MPLBACKEND", "Agg")

SEED = 42

