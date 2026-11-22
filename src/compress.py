"""Compressores clássicos e distância de compressão normalizada."""
from __future__ import annotations

import bz2
import gzip
import lzma
from collections.abc import Callable

Compressor = Callable[[bytes], bytes]

COMPRESSORS: dict[str, Compressor] = {
    "gzip": lambda value: gzip.compress(value, compresslevel=9, mtime=0),
    "bz2": lambda value: bz2.compress(value, compresslevel=9),
    "lzma": lambda value: lzma.compress(value, preset=9),
}


def compressed_size(value: bytes | str, compressor: str = "lzma") -> int:
    """Retorna o tamanho comprimido em bytes."""
    raw = value.encode("utf-8") if isinstance(value, str) else value
    try:
        return len(COMPRESSORS[compressor](raw))
    except KeyError as exc:
        raise ValueError(f"Compressor desconhecido: {compressor}") from exc


def ncd(x: bytes | str, y: bytes | str, compressor: str = "lzma") -> float:
    """Calcula NCD usando a média das duas ordens de concatenação."""
    xb = x.encode("utf-8") if isinstance(x, str) else x
    yb = y.encode("utf-8") if isinstance(y, str) else y
    cx, cy = compressed_size(xb, compressor), compressed_size(yb, compressor)
    cxy = (compressed_size(xb + yb, compressor) + compressed_size(yb + xb, compressor)) / 2
    return max(0.0, (cxy - min(cx, cy)) / max(cx, cy))


def bits_per_character(text: str, compressor: str) -> float:
    """Mede bytes comprimidos como bits por caractere Unicode."""
    return 8.0 * compressed_size(text, compressor) / max(1, len(text))

