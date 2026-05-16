from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Iterable

from belief_set.core import BeliefSet
from belief_set.language import Formula, conjunction


@dataclass(frozen=True, slots=True)
class BeliefBase:
    """Finite belief base that preserves explicit source formulas."""

    alphabet: frozenset[str]
    formulas: tuple[Formula, ...]

    def __post_init__(self) -> None:
        formulas = _dedupe_formulas(self.formulas)
        signature = frozenset(self.alphabet)
        for formula in formulas:
            signature |= formula.atoms()
        object.__setattr__(self, "alphabet", signature)
        object.__setattr__(self, "formulas", formulas)

    def closure(self) -> BeliefSet:
        return BeliefSet.from_formula(self.alphabet, conjunction(*self.formulas))

    @property
    def is_consistent(self) -> bool:
        return self.closure().is_consistent

    def entails(self, formula: Formula) -> bool:
        return self.closure().entails(formula)

    def remainder_sets(
        self,
        forbidden: Iterable[Formula],
    ) -> tuple[tuple[Formula, ...], ...]:
        """Return Hansson remainder sets A perp B over this finite base."""
        forbidden_formulas = _dedupe_formulas(tuple(forbidden))
        candidates = tuple(
            subset
            for subset in _subsets(self.formulas)
            if _avoids_all(self.alphabet, subset, forbidden_formulas)
        )
        return tuple(
            candidate
            for candidate in candidates
            if not any(
                _proper_formula_subset(candidate, other)
                for other in candidates
            )
        )

    def simple_full_meet_contract(
        self,
        forbidden: Iterable[Formula],
    ) -> BeliefBase:
        """Return Hansson's simple full meet contraction A ~ B."""
        remainders = self.remainder_sets(forbidden)
        if not remainders:
            return BeliefBase(self.alphabet, ())
        kept = tuple(
            formula
            for formula in self.formulas
            if all(formula in remainder for remainder in remainders)
        )
        return BeliefBase(self.alphabet, kept)

    def parallel_sets(
        self,
        forbidden: Iterable[Formula],
    ) -> tuple[tuple[Formula, ...], ...]:
        """Return Hansson's composite family A parallel B."""
        forbidden_formulas = _dedupe_formulas(tuple(forbidden))
        parallel: list[tuple[Formula, ...]] = []
        for subset in _subsets(forbidden_formulas):
            for remainder in self.remainder_sets(subset):
                if remainder not in parallel:
                    parallel.append(remainder)
        return tuple(parallel)

    def simple_partial_meet_contract(
        self,
        forbidden: Iterable[Formula],
        selector: Callable[
            [tuple[tuple[Formula, ...], ...]],
            Iterable[tuple[Formula, ...]],
        ],
    ) -> BeliefBase:
        """Return Hansson's simple partial meet contraction via gamma."""
        remainders = self.remainder_sets(forbidden)
        if not remainders:
            return BeliefBase(self.alphabet, self.formulas)
        selected = tuple(tuple(remainder) for remainder in selector(remainders))
        if not selected:
            raise ValueError("selection function must choose at least one remainder")
        if any(remainder not in remainders for remainder in selected):
            raise ValueError("selection function must choose only remainder sets")
        kept = tuple(
            formula
            for formula in self.formulas
            if all(formula in remainder for remainder in selected)
        )
        return BeliefBase(self.alphabet, kept)


def _dedupe_formulas(formulas: tuple[Formula, ...]) -> tuple[Formula, ...]:
    deduped: list[Formula] = []
    for formula in formulas:
        if formula not in deduped:
            deduped.append(formula)
    return tuple(deduped)


def _subsets(formulas: tuple[Formula, ...]) -> tuple[tuple[Formula, ...], ...]:
    return tuple(
        tuple(subset)
        for size in range(len(formulas) + 1)
        for subset in combinations(formulas, size)
    )


def _avoids_all(
    alphabet: frozenset[str],
    formulas: tuple[Formula, ...],
    forbidden: tuple[Formula, ...],
) -> bool:
    base = BeliefBase(alphabet, formulas)
    return all(not base.entails(formula) for formula in forbidden)


def _proper_formula_subset(
    left: tuple[Formula, ...],
    right: tuple[Formula, ...],
) -> bool:
    return all(formula in right for formula in left) and any(
        formula not in left for formula in right
    )
