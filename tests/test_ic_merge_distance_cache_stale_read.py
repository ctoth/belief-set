from __future__ import annotations

import belief_set.ic_merge as ic_merge
from belief_set import TOP, Atom, conjunction
from belief_set.ic_merge import merge_belief_profile


def test_ic_merge_uses_per_call_distance_entries_for_equivalent_formulas() -> None:
    formula_a = conjunction(Atom("p"), Atom("q"))
    formula_b = conjunction(Atom("p"), Atom("q"))
    signature = frozenset({"p", "q"})

    assert formula_a == formula_b
    assert formula_a is not formula_b
    assert not hasattr(ic_merge, "_DISTANCE_FORMULA_CACHE")

    left = merge_belief_profile(signature, (formula_a,), TOP).belief_set
    right = merge_belief_profile(signature, (formula_b,), TOP).belief_set

    assert left == right
