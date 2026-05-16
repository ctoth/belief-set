from __future__ import annotations

from belief_set import Atom, conjunction, disjunction
from belief_set.language import And, Or


def test_conjunction_recursively_flattens_nested_and_nodes() -> None:
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    s = Atom("s")

    formula = conjunction(And((p, q)), And((And((r, s)), p)))

    assert isinstance(formula, And)
    assert formula.formulas == (p, q, r, s, p)


def test_disjunction_recursively_flattens_nested_or_nodes() -> None:
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    s = Atom("s")

    formula = disjunction(Or((p, q)), Or((Or((r, s)), p)))

    assert isinstance(formula, Or)
    assert formula.formulas == (p, q, r, s, p)
