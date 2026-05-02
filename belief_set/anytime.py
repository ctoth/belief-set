from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnumerationExceeded(Exception):
    partial_count: int
    max_candidates: int


@dataclass(frozen=True, slots=True)
class AlphabetBudgetExceeded(ValueError):
    alphabet_size: int
    max_alphabet_size: int


def enforce_alphabet_budget(
    signature: frozenset[str],
    max_alphabet_size: int,
) -> None:
    if max_alphabet_size < 0:
        raise ValueError("max_alphabet_size must be non-negative")
    if len(signature) > max_alphabet_size:
        raise AlphabetBudgetExceeded(
            alphabet_size=len(signature),
            max_alphabet_size=max_alphabet_size,
        )
