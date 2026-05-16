from itertools import combinations

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
