from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from belief_set import BOTTOM, Atom, BeliefSet, SpohnEpistemicState, revise


def test_revise_by_inconsistent_formula_returns_inconsistent_theory() -> None:
    """Class A - must fail today: agm.py short-circuits K*2 for bottom."""

    p = Atom("p")
    alphabet = frozenset({"p"})
    state = SpohnEpistemicState.from_ranks(
        alphabet,
        {
            frozenset({"p"}): 0,
            frozenset(): 1,
        },
    )

    result = revise(state, BOTTOM)

    assert result.belief_set == BeliefSet.contradiction(alphabet)
    assert result.state.belief_set == BeliefSet.contradiction(alphabet)
    assert all(math.isinf(rank) for rank in result.state.ranks.values())
    assert result.trace.pre_image_fingerprint == state.belief_set.fingerprint()
    assert state.belief_set.entails(p)


def test_from_contradictory_belief_set_preserves_inconsistency() -> None:
    alphabet = frozenset({"p", "q"})

    state = SpohnEpistemicState.from_belief_set(BeliefSet.contradiction(alphabet))

    assert state.belief_set == BeliefSet.contradiction(alphabet)
    assert all(math.isinf(rank) for rank in state.ranks.values())


@pytest.mark.property
@given(st.sets(st.sampled_from(("p", "q", "r")), max_size=3))
@settings(deadline=None)
def test_revising_all_infinite_spohn_state_keeps_ocf_ranks_non_nan(
    atoms: set[str],
) -> None:
    alphabet = frozenset(atoms | {"p"})
    state = SpohnEpistemicState.from_ranks(
        alphabet,
        {world: math.inf for world in BeliefSet.all_worlds(alphabet)},
    )

    result = revise(state, Atom("p"))

    assert result.belief_set == BeliefSet.contradiction(alphabet)
    assert all(math.isinf(rank) for rank in result.state.ranks.values())
    assert not any(math.isnan(float(rank)) for rank in result.state.ranks.values())
