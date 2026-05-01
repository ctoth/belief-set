from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnumerationExceeded(Exception):
    partial_count: int
    max_candidates: int
