from __future__ import annotations

import math

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from belief_set import (
    Atom,
    BOTTOM,
    TOP,
    BeliefSet,
    Formula,
    SpohnEpistemicState,
    conjunction,
    disjunction,
    expand,
    full_meet_contract,
    levi_revise,
    negate,
    revise,
)


pytestmark = pytest.mark.property

ALPHABET = frozenset({"p", "q"})
P = Atom("p")
Q = Atom("q")
FORMULAS: tuple[Formula, ...] = (
    TOP,
    BOTTOM,
    P,
    Q,
    negate(P),
    negate(Q),
    conjunction(P, Q),
    disjunction(P, Q),
    disjunction(P, negate(Q)),
)
st_formula = st.sampled_from(FORMULAS)


@st.composite
def st_ocf(draw) -> SpohnEpistemicState:
    ranks = {
        world: draw(st.one_of(st.integers(min_value=0, max_value=5), st.just(math.inf)))
        for world in BeliefSet.all_worlds(ALPHABET)
    }
    assume(any(not math.isinf(float(rank)) for rank in ranks.values()))
    return SpohnEpistemicState.from_ranks(ALPHABET, ranks)


@given(st_ocf(), st_formula)
@settings(deadline=None)
def test_agm_1985_levi_revision_contracts_negation_then_expands(
    state: SpohnEpistemicState,
    formula: Formula,
) -> None:
    """AGM 1985 / Gärdenfors 1988: K*A = (K- not A)+A."""

    expected = expand(full_meet_contract(state, negate(formula)).belief_set, formula)

    assert levi_revise(state, formula).belief_set.equivalent(expected)


@given(st_ocf(), st_formula)
@settings(deadline=None)
def test_agm_1985_levi_revision_matches_direct_revision_belief_set(
    state: SpohnEpistemicState,
    formula: Formula,
) -> None:
    """The finite Spohn direct revision and Levi construction select the same theory."""

    assert levi_revise(state, formula).belief_set.equivalent(revise(state, formula).belief_set)
