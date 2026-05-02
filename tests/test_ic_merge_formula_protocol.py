from __future__ import annotations

import pytest

from belief_set import TOP, BeliefSet, World
from belief_set.ic_merge import _distance_to_formula, merge_belief_profile


class UnhashableFormula:
    def __init__(self, required: frozenset[str], atoms: frozenset[str]) -> None:
        self.required = required
        self._atoms = atoms

    def __hash__(self) -> int:
        raise TypeError("unhashable formula")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnhashableFormula) and self.required == other.required

    def evaluate(self, world: World) -> bool:
        return self.required <= world

    def atoms(self) -> frozenset[str]:
        return self._atoms


class MutableFormula:
    def __init__(self, required: frozenset[str], atoms: frozenset[str]) -> None:
        self.required = required
        self._atoms = atoms

    def evaluate(self, world: World) -> bool:
        return self.required <= world

    def atoms(self) -> frozenset[str]:
        return self._atoms


def test_ic_merge_accepts_unhashable_formula_protocol_implementations() -> None:
    formula = UnhashableFormula(
        required=frozenset({"p"}),
        atoms=frozenset({"p"}),
    )

    result = merge_belief_profile(frozenset({"p"}), (formula,), TOP)

    assert result.belief_set == BeliefSet.from_formula(frozenset({"p"}), formula)


def test_ic_merge_does_not_reuse_stale_models_after_formula_semantics_change() -> None:
    signature = frozenset({"p", "q"})
    formula = MutableFormula(
        required=frozenset({"p"}),
        atoms=signature,
    )

    first = merge_belief_profile(signature, (formula,), TOP).belief_set
    formula.required = frozenset({"q"})
    second = merge_belief_profile(signature, (formula,), TOP).belief_set

    assert first == BeliefSet.from_formula(signature, MutableFormula(frozenset({"p"}), signature))
    assert second == BeliefSet.from_formula(signature, MutableFormula(frozenset({"q"}), signature))


def test_distance_to_formula_rejects_atoms_outside_signature() -> None:
    formula = MutableFormula(
        required=frozenset({"p"}),
        atoms=frozenset({"p"}),
    )

    with pytest.raises(ValueError, match="outside signature"):
        _distance_to_formula(frozenset(), formula, frozenset())
