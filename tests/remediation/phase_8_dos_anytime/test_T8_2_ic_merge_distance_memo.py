from __future__ import annotations

import pytest

from belief_set import TOP
from belief_set.anytime import EnumerationExceeded
from belief_set.core import BeliefSet
from belief_set.ic_merge import merge_belief_profile
from belief_set.language import World


class CountingConjunctionFormula:
    def __init__(self, atoms: frozenset[str]) -> None:
        self._atoms = atoms
        self.evaluations = 0

    def evaluate(self, world: World) -> bool:
        self.evaluations += 1
        return self._atoms <= world

    def atoms(self) -> frozenset[str]:
        return self._atoms


def test_merge_distance_oracle_scans_each_profile_formula_once_per_call() -> None:
    signature = frozenset({"a", "b", "c", "d", "e", "f"})
    worlds = tuple(BeliefSet.all_worlds(signature))
    formula = CountingConjunctionFormula(signature)

    merge_belief_profile(signature, (formula,), TOP)

    assert formula.evaluations == len(worlds)

    after_first_pass = formula.evaluations
    merge_belief_profile(signature, (formula,), TOP)

    assert formula.evaluations == after_first_pass + len(worlds)


def test_merge_profile_honors_candidate_budget_during_distance_entry_build() -> None:
    signature = frozenset({"a", "b", "c"})
    formula = CountingConjunctionFormula(signature)

    with pytest.raises(EnumerationExceeded):
        merge_belief_profile(signature, (formula,), TOP, max_candidates=0)

    assert formula.evaluations == 0
