"""Modelos de caracteres e palavras implementados sem modelos prontos."""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Iterable

import numpy as np


def empirical_entropy(text: str, order: int = 0) -> float:
    """Entropia condicional empírica H(X_t | contexto) em bits/caractere."""
    if not text:
        return 0.0
    if order == 0:
        counts = Counter(text)
        n = len(text)
        return -sum((c / n) * math.log2(c / n) for c in counts.values())
    groups: dict[str, Counter[str]] = defaultdict(Counter)
    for index in range(order, len(text)):
        groups[text[index - order:index]][text[index]] += 1
    total = sum(sum(values.values()) for values in groups.values())
    if not total:
        return 0.0
    return sum((sum(values.values()) / total) * empirical_entropy_from_counts(values) for values in groups.values())


def empirical_entropy_from_counts(counts: Counter[str]) -> float:
    total = sum(counts.values())
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


class CharNGramModel:
    """N-grama de caracteres com interpolação recursiva de Witten–Bell."""

    def __init__(self, order: int = 4, alphabet: Iterable[str] | None = None) -> None:
        if order < 1:
            raise ValueError("A ordem deve ser positiva")
        self.order = order
        self.alphabet = set(alphabet or [])
        self.counts: list[dict[str, Counter[str]]] = [defaultdict(Counter) for _ in range(order)]

    def fit(self, text: str) -> "CharNGramModel":
        self.alphabet.update(text)
        for index, char in enumerate(text):
            for context_size in range(self.order):
                context = text[max(0, index - context_size):index]
                self.counts[context_size][context][char] += 1
        return self

    def probability(self, char: str, context: str = "") -> float:
        """Probabilidade interpolada; o nível zero termina numa uniforme."""
        vocabulary = max(1, len(self.alphabet))
        probability = 1.0 / vocabulary
        for context_size in range(min(len(context), self.order - 1) + 1):
            suffix = context[-context_size:] if context_size else ""
            values = self.counts[context_size].get(suffix, Counter())
            total, distinct = sum(values.values()), len(values)
            if total:
                probability = (values.get(char, 0) + distinct * probability) / (total + distinct)
        return max(probability, np.finfo(float).tiny)

    def distribution(self, context: str = "") -> dict[str, float]:
        raw = {char: self.probability(char, context) for char in sorted(self.alphabet)}
        total = sum(raw.values())
        return {char: value / total for char, value in raw.items()}

    def cross_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        bits = 0.0
        for index, char in enumerate(text):
            context = text[max(0, index - self.order + 1):index]
            bits -= math.log2(self.probability(char, context))
        return bits / len(text)


class WordUnigramModel:
    """Unigrama de palavras com suavização aditiva configurável."""

    def __init__(self, alpha: float = 0.5) -> None:
        self.alpha = alpha
        self.counts: Counter[str] = Counter()

    def fit(self, words: Iterable[str]) -> "WordUnigramModel":
        self.counts.update(words)
        return self

    def probability(self, word: str, vocabulary: set[str]) -> float:
        denominator = sum(self.counts.values()) + self.alpha * len(vocabulary)
        return (self.counts.get(word, 0) + self.alpha) / max(denominator, self.alpha)


def kl_word_contributions(a: WordUnigramModel, b: WordUnigramModel) -> dict[str, float]:
    vocabulary = set(a.counts) | set(b.counts)
    return {
        word: a.probability(word, vocabulary) * math.log2(a.probability(word, vocabulary) / b.probability(word, vocabulary))
        for word in vocabulary
    }

