"""Utilitários numéricos compartilhados pelos experimentos."""
from __future__ import annotations

import numpy as np


def classical_mds(distances: np.ndarray, dimensions: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """MDS clássico por autodecomposição da matriz duplamente centrada."""
    n = len(distances)
    centering = np.eye(n) - np.ones((n, n)) / n
    gram = -0.5 * centering @ (distances ** 2) @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    positive = np.maximum(eigenvalues[order[:dimensions]], 0)
    coordinates = eigenvectors[:, order[:dimensions]] * np.sqrt(positive)
    return coordinates, positive


def upper_values(matrix: np.ndarray) -> np.ndarray:
    return matrix[np.triu_indices_from(matrix, k=1)]

