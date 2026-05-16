from itertools import combinations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from belief_set import Atom, Formula, conjunction, disjunction, negate
from belief_set.base import BeliefBase


ALPHABET = frozenset({"p", "q", "r"})
P = Atom("p")
Q = Atom("q")
R = Atom("r")

BASE_FORMULAS: tuple[Formula, ...] = (
    P,
    Q,
    R,
    negate(P),
    negate(Q),
    negate(R),
    disjunction(P, Q),
    disjunction(P, R),
    conjunction(P, Q),
    conjunction(Q, R),
)

st_base_formulas = st.lists(
    st.sampled_from(BASE_FORMULAS),
    min_size=1,
    max_size=4,
    unique_by=repr,
).map(tuple)
st_forbidden = st.lists(
    st.sampled_from(BASE_FORMULAS),
    min_size=1,
    max_size=2,
    unique_by=repr,
).map(tuple)


def test_hansson_1989_base_contraction_preserves_source_disjunction() -> None:
    """Hansson 1989, pp.117-118: bases with same closure can contract differently."""

    richer_base = BeliefBase(ALPHABET, (P, disjunction(P, Q)))
    closed_equivalent_base = BeliefBase(ALPHABET, (P,))

    assert richer_base.simple_full_meet_contract((P,)).formulas == (disjunction(P, Q),)
    assert closed_equivalent_base.simple_full_meet_contract((P,)).formulas == ()


def test_hansson_1989_disjunction_expansion_contains_up_to_n_member_disjunctions() -> None:
    """Hansson 1989, p.125: V_n A contains disjunctions of at most n base members."""

    base = BeliefBase(ALPHABET, (P, Q, R))

    assert base.disjunction_expansion(1).formulas == (P, Q, R)
    assert base.disjunction_expansion(2).formulas == (
        P,
        Q,
        R,
        disjunction(P, Q),
        disjunction(P, R),
        disjunction(Q, R),
    )


def test_hansson_1989_disjunction_expansion_rejects_non_positive_size() -> None:
    """Hansson 1989, p.125: V_n A is defined for n >= 1."""

    base = BeliefBase(ALPHABET, (P, Q, R))

    with pytest.raises(ValueError, match="positive"):
        base.disjunction_expansion(0)


def test_hansson_1989_simple_partial_meet_intersects_selected_remainders() -> None:
    """Hansson 1989, Definition 3.7: simple partial meet intersects gamma(A perp B)."""

    base = BeliefBase(ALPHABET, (P, Q, disjunction(P, Q)))
    remainders = base.remainder_sets((P,))
    selected = (remainders[0],)

    contracted = base.simple_partial_meet_contract((P,), lambda _: selected)

    assert contracted.formulas == selected[0]


@given(st_base_formulas, st_forbidden)
@settings(deadline=None)
def test_hansson_1989_parallel_sets_union_remainders_over_forbidden_subsets(
    base_formulas: tuple[Formula, ...],
    forbidden: tuple[Formula, ...],
) -> None:
    """Hansson 1989, Definition 3.8: A || B is union of A perp C for C subseteq B."""

    base = BeliefBase(ALPHABET, base_formulas)
    expected: list[tuple[Formula, ...]] = []
    for subset in _subsets(forbidden):
        for remainder in base.remainder_sets(subset):
            if remainder not in expected:
                expected.append(remainder)

    assert base.parallel_sets(forbidden) == tuple(expected)


def test_hansson_1989_covering_selection_meets_each_forbidden_input() -> None:
    """Hansson 1989, Definition 3.8: D is B-covering only when every b in B is covered."""

    base = BeliefBase(ALPHABET, (P, Q, disjunction(P, Q)))
    covers_p = base.remainder_sets((P,))[0]
    covers_q = base.remainder_sets((Q,))[0]

    assert base.is_covering_selection((P, Q), (covers_p, covers_q))
    assert not base.is_covering_selection((P, Q), (base.formulas,))


def test_hansson_1989_covering_selection_rejects_non_parallel_members() -> None:
    """Hansson 1989, Definition 3.8: D must be a subfamily of A || B."""

    base = BeliefBase(ALPHABET, (P, Q, disjunction(P, Q)))

    with pytest.raises(ValueError, match="parallel"):
        base.is_covering_selection((P, Q), ((P, Q),))


def test_hansson_1989_composite_partial_meet_intersects_covering_selection() -> None:
    """Hansson 1989, Definition 3.9: composite partial meet intersects gamma(A || B)."""

    base = BeliefBase(ALPHABET, (P, Q, disjunction(P, Q)))
    covers_p = base.remainder_sets((P,))[0]
    covers_q = base.remainder_sets((Q,))[0]
    selected = (covers_p, covers_q)

    contracted = base.composite_partial_meet_contract((P, Q), lambda _: selected)

    assert contracted.formulas == (disjunction(P, Q),)
    with pytest.raises(ValueError, match="remainder"):
        base.simple_partial_meet_contract((P, Q), lambda _: selected)


def test_hansson_1989_composite_partial_meet_requires_covering_when_possible() -> None:
    """Hansson 1989, Definition 3.9: gamma must select a B-covering subfamily when possible."""

    base = BeliefBase(ALPHABET, (P, Q, disjunction(P, Q)))

    with pytest.raises(ValueError, match="covering"):
        base.composite_partial_meet_contract((P, Q), lambda _: (base.formulas,))


@given(st_base_formulas, st_forbidden)
@settings(deadline=None)
def test_hansson_1989_remainder_sets_are_maximal_subsets_avoiding_inputs(
    base_formulas: tuple[Formula, ...],
    forbidden: tuple[Formula, ...],
) -> None:
    """Hansson 1989, Definition 3.4: remainders are maximal B-avoiding subsets."""

    base = BeliefBase(ALPHABET, base_formulas)

    for remainder in base.remainder_sets(forbidden):
        remainder_base = BeliefBase(ALPHABET, remainder)
        assert all(not remainder_base.entails(formula) for formula in forbidden)

        for formula in base.formulas:
            if formula not in remainder:
                expanded = BeliefBase(ALPHABET, (*remainder, formula))
                assert any(expanded.entails(forbidden_formula) for forbidden_formula in forbidden)


def _subsets(formulas: tuple[Formula, ...]) -> tuple[tuple[Formula, ...], ...]:
    return tuple(
        tuple(subset)
        for size in range(len(formulas) + 1)
        for subset in combinations(formulas, size)
    )
