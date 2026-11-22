import numpy as np

from src.experiments.utils import classical_mds


def test_mds_tem_formato_e_distancias_finitas():
    distances = np.array([[0.0, 1.0, 1.2], [1.0, 0.0, 0.8], [1.2, 0.8, 0.0]])
    coordinates, eigenvalues = classical_mds(distances, 3)
    assert coordinates.shape == (3, 3)
    assert np.isfinite(coordinates).all()
    assert (eigenvalues >= 0).all()

