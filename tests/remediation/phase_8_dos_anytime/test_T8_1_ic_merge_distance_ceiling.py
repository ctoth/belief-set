from __future__ import annotations

from belief_set import Atom
from belief_set.ic_merge import _distance_to_formula
from belief_set.anytime import EnumerationExceeded


def test_distance_to_formula_returns_enumeration_exceeded_past_ceiling() -> None:
    result = _distance_to_formula(
        frozenset(),
        Atom("p"),
        frozenset({"p", "q", "r"}),
        max_candidates=1,
    )

    assert isinstance(result, EnumerationExceeded)
    assert result.partial_count == 1
    assert result.max_candidates == 1
