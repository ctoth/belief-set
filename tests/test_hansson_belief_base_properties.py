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
