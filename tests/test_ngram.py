import math

import pytest

from src.ngram import CharNGramModel, empirical_entropy


def test_entropia_uniforme():
    text = "abcd" * 1000
    assert empirical_entropy(text) == pytest.approx(math.log2(4), abs=1e-6)


def test_probabilidades_somam_um():
    model = CharNGramModel(4).fit("abracadabra" * 200)
    assert sum(model.probability(char, "abra") for char in model.alphabet) == pytest.approx(1.0, abs=1e-10)


def test_entropia_cruzada_e_kl_nao_negativa():
    p_text = "aaaabbbbccccddddeeee " * 300
    q_text = "aaaaaaaabbbbccdd " * 300
    p = CharNGramModel(2, set(p_text + q_text)).fit(p_text)
    q = CharNGramModel(2, set(p_text + q_text)).fit(q_text)
    h_p = p.cross_entropy(p_text)
    h_pq = q.cross_entropy(p_text)
    assert h_pq + 1e-9 >= h_p
    assert h_pq - h_p >= -1e-9

