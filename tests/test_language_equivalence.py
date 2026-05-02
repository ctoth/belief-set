from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from belief_set import BOTTOM, Atom, equivalent


def test_equivalent_honors_explicit_empty_alphabet() -> None:
    assert equivalent(Atom("p"), BOTTOM, alphabet=frozenset())


def test_equivalent_default_alphabet_includes_formula_atoms() -> None:
    assert not equivalent(Atom("p"), BOTTOM)


@pytest.mark.property
@given(st.sets(st.sampled_from(("q", "r")), max_size=2))
@settings(deadline=None)
def test_equivalent_uses_exact_explicit_alphabet(atoms: set[str]) -> None:
    assert equivalent(Atom("p"), BOTTOM, alphabet=frozenset(atoms))
