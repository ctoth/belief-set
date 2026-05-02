from __future__ import annotations

import math

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from belief_set import (
    Atom,
    BOTTOM,
    BeliefSet,
    EpistemicEntrenchment,
    Formula,
    ICMergeOperator,
    SpohnEpistemicState,
    TOP,
    conjunction,
    disjunction,
    expand,
    full_meet_contract,
    lexicographic_revise,
    merge_belief_profile,
    negate,
    restrained_revise,
    revise,
    theory_subset,
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
st_operator = st.sampled_from((ICMergeOperator.SIGMA, ICMergeOperator.GMAX))


@st.composite
def st_ocf(draw) -> SpohnEpistemicState:
    ranks = {
        world: draw(st.one_of(st.integers(min_value=0, max_value=4), st.just(math.inf)))
        for world in BeliefSet.all_worlds(ALPHABET)
    }
    assume(any(not math.isinf(float(rank)) for rank in ranks.values()))
    return SpohnEpistemicState.from_ranks(ALPHABET, ranks)


@st.composite
def st_formula_impossible_state(draw) -> tuple[SpohnEpistemicState, Formula]:
    formula = draw(st_formula)
    formula_models = tuple(world for world in BeliefSet.all_worlds(ALPHABET) if formula.evaluate(world))
    countermodels = tuple(world for world in BeliefSet.all_worlds(ALPHABET) if not formula.evaluate(world))
    assume(formula_models)
    assume(countermodels)

    ranks = {
        world: math.inf if formula.evaluate(world) else draw(st.integers(min_value=0, max_value=4))
        for world in BeliefSet.all_worlds(ALPHABET)
    }
    return SpohnEpistemicState.from_ranks(ALPHABET, ranks), formula


@st.composite
def st_finite_ocf(draw) -> SpohnEpistemicState:
    return SpohnEpistemicState.from_ranks(
        ALPHABET,
        {
            world: draw(st.integers(min_value=0, max_value=4))
            for world in BeliefSet.all_worlds(ALPHABET)
        },
    )


@st.composite
def st_profile(draw) -> tuple[Formula, ...]:
    return tuple(draw(st.lists(st_formula, min_size=1, max_size=3)))


def _belief(formula: Formula) -> BeliefSet:
    return BeliefSet.from_formula(ALPHABET, formula)


def _is_tautology(formula: Formula) -> bool:
    return _belief(formula).models == BeliefSet.all_worlds(ALPHABET)


def _assert_valid_ocf(state: SpohnEpistemicState) -> None:
    ranks = tuple(float(rank) for rank in state.ranks.values())
    assert all(not math.isnan(rank) for rank in ranks)
    if not all(math.isinf(rank) for rank in ranks):
        assert min(ranks) == 0.0


@given(st_formula_impossible_state())
@settings(deadline=None)
def test_spohn_1988_agm_revision_by_satisfiable_formula_stays_ocf_and_succeeds(
    case: tuple[SpohnEpistemicState, Formula],
) -> None:
    state, formula = case

    outcome = revise(state, formula)

    _assert_valid_ocf(outcome.state)
    assert outcome.belief_set.is_consistent
    assert outcome.belief_set.entails(formula)


@given(st_ocf(), st_formula)
@settings(deadline=None)
def test_spohn_1988_iterated_revision_operators_preserve_ocf_invariants(
    state: SpohnEpistemicState,
    formula: Formula,
) -> None:
    assume(_belief(formula).is_consistent)

    for operator in (lexicographic_revise, restrained_revise):
        outcome = operator(state, formula)
        _assert_valid_ocf(outcome.state)
        assert outcome.belief_set.entails(formula)


@given(st_ocf(), st_formula, st_formula)
@settings(deadline=None)
def test_agm_1985_revision_and_harper_contraction_postulates_remain_extensional(
    state: SpohnEpistemicState,
    alpha: Formula,
    beta: Formula,
) -> None:
    revision = revise(state, alpha)
    contraction = full_meet_contract(state, alpha)

    if _belief(alpha).is_consistent and state.belief_set.is_consistent:
        assert revision.belief_set.entails(alpha)
    assert revision.belief_set.alphabet == revision.state.alphabet
    assert contraction.belief_set.alphabet == contraction.state.alphabet

    harper = state.belief_set.intersection_theory(revise(state, negate(alpha)).belief_set)
    assert contraction.belief_set.equivalent(harper)

    conjunctive_revision = revise(state, conjunction(alpha, beta)).belief_set
    revise_then_expand = expand(revision.belief_set, beta)
    assert theory_subset(conjunctive_revision, revise_then_expand)


@given(st_finite_ocf(), st_formula, st_formula, st_formula)
@settings(deadline=None)
def test_gardenfors_makinson_1988_ee1_ee5_generated_sweep(
    state: SpohnEpistemicState,
    alpha: Formula,
    beta: Formula,
    gamma: Formula,
) -> None:
    assume(state.belief_set.is_consistent)
    entrenchment = EpistemicEntrenchment.from_state(state)

    if entrenchment.leq(alpha, beta) and entrenchment.leq(beta, gamma):
        assert entrenchment.leq(alpha, gamma)
    if _belief(alpha).entails(beta):
        assert entrenchment.leq(alpha, beta)
    assert entrenchment.leq(alpha, conjunction(alpha, beta)) or entrenchment.leq(
        beta,
        conjunction(alpha, beta),
    )
    if not state.belief_set.entails(alpha):
        assert all(entrenchment.leq(alpha, candidate) for candidate in FORMULAS)
    if all(entrenchment.leq(candidate, alpha) for candidate in FORMULAS):
        assert _is_tautology(alpha)


@given(st_profile(), st_profile(), st_formula, st_operator)
@settings(deadline=None)
def test_konieczny_pino_perez_2002_ic0_ic8_generated_sweep(
    left: tuple[Formula, ...],
    right: tuple[Formula, ...],
    mu: Formula,
    operator: ICMergeOperator,
) -> None:
    profile = left + right
    assume(_belief(mu).is_consistent)
    assume(all(_belief(item).is_consistent for item in profile))

    result = merge_belief_profile(ALPHABET, profile, mu, operator=operator).belief_set
    assert result.is_consistent
    assert result.entails(mu)

    profile_conjunction = conjunction(*profile)
    if _belief(conjunction(profile_conjunction, mu)).is_consistent:
        assert result.equivalent(_belief(conjunction(profile_conjunction, mu)))

    syntactic_variant = tuple(conjunction(item, disjunction(P, negate(P))) for item in profile)
    assert result.equivalent(
        merge_belief_profile(ALPHABET, syntactic_variant, mu, operator=operator).belief_set
    )

    if left and right:
        left_result = merge_belief_profile(ALPHABET, left, mu, operator=operator).belief_set
        right_result = merge_belief_profile(ALPHABET, right, mu, operator=operator).belief_set
        intersection = BeliefSet(
            ALPHABET,
            left_result.models & right_result.models,
        )
        assert theory_subset(result, intersection)
        if intersection.is_consistent:
            assert theory_subset(intersection, result)
