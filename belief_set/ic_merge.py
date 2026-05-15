from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import overload

from belief_set.agm import MAX_ALPHABET_SIZE
from belief_set.anytime import EnumerationExceeded, enforce_alphabet_budget
from belief_set.core import BeliefSet
from belief_set.language import Formula, World


class ICMergeOperator(StrEnum):
    SIGMA = "sigma"
    MAX = "max"
    GMAX = "gmax"


class ICMergeProfileMemberInconsistent(ValueError):
    """Raised when an IC profile contains an unsatisfiable formula."""

    def __init__(self, formula: Formula) -> None:
        self.formula = formula
        super().__init__("IC merge profile member has no models")

    def __str__(self) -> str:
        return "IC merge profile member has no models"


@dataclass(frozen=True, slots=True)
class ICMergeOutcome:
    belief_set: BeliefSet
    scored_worlds: tuple[tuple[World, tuple[float, ...]], ...]


@dataclass(slots=True)
class _DistanceFormulaEntry:
    formula: Formula
    models: tuple[World, ...]
    distances: dict[World, float]


def merge_belief_profile(
    alphabet: frozenset[str],
    profile: tuple[Formula, ...],
    mu: Formula,
    *,
    operator: ICMergeOperator = ICMergeOperator.SIGMA,
    max_alphabet_size: int = MAX_ALPHABET_SIZE,
) -> ICMergeOutcome:
    """Konieczny-Pino Pérez style finite model-theoretic IC merge."""
    signature = frozenset(alphabet) | mu.atoms()
    for formula in profile:
        signature |= formula.atoms()
    enforce_alphabet_budget(signature, max_alphabet_size)
    distance_entries = _distance_entries(profile, signature)
    _raise_for_unsatisfiable_profile_members(distance_entries)
    candidates = tuple(
        world
        for world in BeliefSet.all_worlds(signature)
        if mu.evaluate(world)
    )
    if not candidates:
        return ICMergeOutcome(
            belief_set=BeliefSet.contradiction(signature),
            scored_worlds=(),
        )
    scored = tuple(
        sorted(
            ((world, _score_world(world, distance_entries, operator)) for world in candidates),
            key=lambda item: (_score_key(item[1]), tuple(sorted(item[0]))),
        )
    )
    best_score = scored[0][1]
    winners = frozenset(world for world, score in scored if score == best_score)
    return ICMergeOutcome(
        belief_set=BeliefSet(signature, winners),
        scored_worlds=scored,
    )


def _score_world(
    world: World,
    distance_entries: tuple[_DistanceFormulaEntry, ...],
    operator: ICMergeOperator,
) -> tuple[float, ...]:
    distances = tuple(_distance_from_entry(world, entry) for entry in distance_entries)
    if operator == ICMergeOperator.SIGMA:
        return (float(sum(distances)),)
    if operator == ICMergeOperator.MAX:
        return (float(max(distances, default=0.0)),)
    if operator == ICMergeOperator.GMAX:
        return tuple(sorted(distances, reverse=True))
    raise ValueError(f"Unsupported IC merge operator: {operator}")


@overload
def _distance_to_formula(world: World, formula: Formula, signature: frozenset[str]) -> float: ...


@overload
def _distance_to_formula(
    world: World,
    formula: Formula,
    signature: frozenset[str],
    *,
    max_candidates: None,
) -> float: ...


@overload
def _distance_to_formula(
    world: World,
    formula: Formula,
    signature: frozenset[str],
    *,
    max_candidates: int,
) -> float | EnumerationExceeded: ...


def _distance_to_formula(
    world: World,
    formula: Formula,
    signature: frozenset[str],
    *,
    max_candidates: int | None = None,
) -> float | EnumerationExceeded:
    """Return finite Hamming distance with an anytime candidate ceiling.

    Zilberstein 1996 frames bounded exact search as an anytime computation:
    if the candidate-world scan is interrupted before exactness is proven, the
    unvisited model space is reported as vacuous rather than approximated.

    Konieczny and Pino Pérez 2002 IC merging repeatedly evaluates distances to
    the same profile formulas across candidate worlds; uncapped exact calls
    therefore memoize each formula's model set and per-world distances.
    """

    if max_candidates is not None and max_candidates < 0:
        raise ValueError("max_candidates must be non-negative")
    _raise_if_formula_atoms_outside_signature(formula, signature)

    if max_candidates is None:
        models = _models_for_formula(formula, signature)
        if not models:
            return math.inf
        return float(min(_hamming(world, model) for model in models))

    best_distance: int | None = None
    examined = 0
    for candidate in BeliefSet.all_worlds(signature):
        if examined >= max_candidates:
            return EnumerationExceeded(
                partial_count=examined,
                max_candidates=max_candidates,
            )
        examined += 1
        if not formula.evaluate(candidate):
            continue
        distance = _hamming(world, candidate)
        if best_distance is None or distance < best_distance:
            best_distance = distance
            if best_distance == 0:
                return 0.0
    if best_distance is None:
        return math.inf
    return float(best_distance)


def _distance_entries(
    profile: tuple[Formula, ...],
    signature: frozenset[str],
) -> tuple[_DistanceFormulaEntry, ...]:
    return tuple(
        _DistanceFormulaEntry(
            formula=formula,
            models=_models_for_formula(formula, signature),
            distances={},
        )
        for formula in profile
    )


def _models_for_formula(
    formula: Formula,
    signature: frozenset[str],
) -> tuple[World, ...]:
    _raise_if_formula_atoms_outside_signature(formula, signature)
    return tuple(
        candidate
        for candidate in BeliefSet.all_worlds(signature)
        if formula.evaluate(candidate)
    )


def _distance_from_entry(world: World, entry: _DistanceFormulaEntry) -> float:
    cached_distance = entry.distances.get(world)
    if cached_distance is not None:
        return cached_distance
    if not entry.models:
        entry.distances[world] = math.inf
        return math.inf
    distance = float(min(_hamming(world, model) for model in entry.models))
    entry.distances[world] = distance
    return distance


def _raise_for_unsatisfiable_profile_members(
    distance_entries: tuple[_DistanceFormulaEntry, ...],
) -> None:
    for entry in distance_entries:
        if not entry.models:
            raise ICMergeProfileMemberInconsistent(entry.formula)


def _raise_if_formula_atoms_outside_signature(
    formula: Formula,
    signature: frozenset[str],
) -> None:
    extra_atoms = formula.atoms() - signature
    if extra_atoms:
        raise ValueError("formula atoms outside signature")


def _hamming(left: World, right: World) -> int:
    return len(left.symmetric_difference(right))


def _score_key(score: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(float(item) for item in score)
