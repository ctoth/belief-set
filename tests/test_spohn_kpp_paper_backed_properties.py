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
    ICMergeOperator,
    SpohnEpistemicState,
    conjunction,
    disjunction,
    merge_belief_profile,
    negate,
)


pytestmark = pytest.mark.property

ALPHABET = frozenset({"p", "q", "r"})
P = Atom("p")
Q = Atom("q")
R = Atom("r")

FORMULAS: tuple[Formula, ...] = (
    TOP,
    BOTTOM,
    P,
    Q,
    R,
    negate(P),
    negate(Q),
    negate(R),
    conjunction(P, Q),
    conjunction(P, negate(Q)),
    conjunction(Q, R),
    disjunction(P, Q),
    disjunction(negate(P), R),
    disjunction(conjunction(P, Q), R),
)

st_formula = st.sampled_from(FORMULAS)
st_merge_operator = st.sampled_from(
    (ICMergeOperator.SIGMA, ICMergeOperator.MAX, ICMergeOperator.GMAX)
)


@st.composite
def st_finite_ocf(draw) -> SpohnEpistemicState:
    return SpohnEpistemicState.from_ranks(
        ALPHABET,
        {
            world: draw(st.integers(min_value=0, max_value=7))
            for world in BeliefSet.all_worlds(ALPHABET)
        },
    )


@st.composite
def st_profile(draw) -> tuple[Formula, ...]:
    return tuple(draw(st.lists(st_formula, min_size=1, max_size=4)))


def _belief(formula: Formula) -> BeliefSet:
    return BeliefSet.from_formula(ALPHABET, formula)


@given(st_finite_ocf(), st_formula)
@settings(deadline=None)
def test_spohn_1988_formula_rank_is_minimum_rank_of_formula_worlds(
    state: SpohnEpistemicState,
    formula: Formula,
) -> None:
    """Spohn 1988, Definition 4: kappa(A) is min kappa(w) over A-worlds."""

    formula_worlds = tuple(
        world for world in BeliefSet.all_worlds(ALPHABET) if formula.evaluate(world)
    )
    expected = (
        math.inf
        if not formula_worlds
        else min(state.ranks[world] for world in formula_worlds)
    )

    assert state.rank(formula) == expected


@given(st_finite_ocf(), st_formula)
@settings(deadline=None)
def test_grove_1988_revision_selects_minimal_formula_worlds(
    state: SpohnEpistemicState,
    formula: Formula,
) -> None:
    """Grove 1988: revision selects the closest worlds satisfying the input."""

    assume(_belief(formula).is_consistent)
    best_rank = state.rank(formula)
    expected = frozenset(
        world
        for world in BeliefSet.all_worlds(ALPHABET)
        if formula.evaluate(world) and state.ranks[world] == best_rank
    )

    assert state.minimal_worlds(formula) == expected


@given(st_finite_ocf(), st_formula, st.integers(min_value=0, max_value=5))
@settings(deadline=None)
def test_spohn_1988_conditionalization_sets_formula_firmness(
    state: SpohnEpistemicState,
    formula: Formula,
    firmness: int,
) -> None:
    """Spohn 1988, Definition 6: kappa_A,alpha(A)=0 and kappa_A,alpha(not A)=alpha."""

    assume(_belief(formula).is_consistent)
    assume(_belief(negate(formula)).is_consistent)

    conditioned = state.conditionalize(formula, firmness=firmness)

    assert conditioned.rank(formula) == 0
    assert conditioned.rank(negate(formula)) == firmness


@given(st_finite_ocf(), st_formula, st.integers(min_value=0, max_value=5))
@settings(deadline=None)
def test_spohn_1988_conditionalization_preserves_grading_inside_each_part(
    state: SpohnEpistemicState,
    formula: Formula,
    firmness: int,
) -> None:
    """Spohn 1988, Definition 6: A- and not-A-parts are shifted, not reordered."""

    assume(_belief(formula).is_consistent)
    assume(_belief(negate(formula)).is_consistent)

    conditioned = state.conditionalize(formula, firmness=firmness)
    worlds = tuple(BeliefSet.all_worlds(ALPHABET))

    for expected_truth in (True, False):
        part_worlds = tuple(world for world in worlds if formula.evaluate(world) is expected_truth)
        for left in part_worlds:
            for right in part_worlds:
                assert conditioned.ranks[left] - conditioned.ranks[right] == (
                    state.ranks[left] - state.ranks[right]
                )


@given(st_profile(), st_formula)
@settings(deadline=None)
def test_konieczny_pino_perez_2002_gmax_refines_max(
    profile: tuple[Formula, ...],
    mu: Formula,
) -> None:
    """KPP 2002, Remark 4.10: GMax refines Max over the same profile."""

    assume(_belief(mu).is_consistent)
    assume(all(_belief(formula).is_consistent for formula in profile))

    max_result = merge_belief_profile(
        ALPHABET,
        profile,
        mu,
        operator=ICMergeOperator.MAX,
    ).belief_set
    gmax_result = merge_belief_profile(
        ALPHABET,
        profile,
        mu,
        operator=ICMergeOperator.GMAX,
    ).belief_set

    assert gmax_result.models <= max_result.models


@given(st_profile(), st_formula, st_merge_operator)
@settings(deadline=None)
def test_konieczny_pino_perez_2002_outcome_exposes_selected_minimal_worlds(
    profile: tuple[Formula, ...],
    mu: Formula,
    operator: ICMergeOperator,
) -> None:
    """KPP 2002: merge result is min(mod(mu), <=_Psi)."""

    assume(_belief(mu).is_consistent)
    assume(all(_belief(formula).is_consistent for formula in profile))

    outcome = merge_belief_profile(ALPHABET, profile, mu, operator=operator)
    expected_score = outcome.scored_worlds[0][1]
    expected_winners = frozenset(
        world for world, score in outcome.scored_worlds if score == expected_score
    )

    assert outcome.best_score == expected_score
    assert outcome.winning_worlds == expected_winners
    assert outcome.belief_set.models == outcome.winning_worlds
