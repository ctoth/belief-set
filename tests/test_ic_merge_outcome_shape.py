from __future__ import annotations

import pytest

from belief_set import Atom, BeliefSet
from belief_set.ic_merge import ICMergeOperator, merge_belief_profile


@pytest.mark.parametrize("operator", (ICMergeOperator.SIGMA, ICMergeOperator.GMAX))
def test_empty_profile_merge_returns_integrity_constraint_models(
    operator: ICMergeOperator,
) -> None:
    alphabet = frozenset({"p", "q"})
    mu = Atom("p")

    result = merge_belief_profile(alphabet, (), mu, operator=operator)

    assert result.belief_set == BeliefSet.from_formula(alphabet, mu)


@pytest.mark.parametrize("operator", (ICMergeOperator.SIGMA, ICMergeOperator.GMAX))
def test_ic_merge_scored_worlds_always_use_tuple_scores(
    operator: ICMergeOperator,
) -> None:
    result = merge_belief_profile(
        frozenset({"p"}),
        (Atom("p"),),
        Atom("p").or_(Atom("q")),
        operator=operator,
    )

    assert result.scored_worlds
    assert all(isinstance(score, tuple) for _, score in result.scored_worlds)
