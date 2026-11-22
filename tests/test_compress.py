import os

from src.compress import ncd


def test_ncd_identidade_e_aleatorio():
    text = ("information theory finds repeated structure in scientific language. " * 500).encode()
    random = os.urandom(len(text))
    assert ncd(text, text, "lzma") < 0.1
    assert ncd(text, random, "lzma") > 0.7

