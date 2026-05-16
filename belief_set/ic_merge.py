from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
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
    distance_vectors: Mapping[World, tuple[float, ...]]

    @property
    def best_score(self) -> tuple[float, ...] | None:
        if not self.scored_worlds:
            return None
        return self.scored_worlds[0][1]

    @property
    def winning_worlds(self) -> frozenset[World]:
        best_score = self.best_score
        if best_score is None:
            return frozenset()
        return frozenset(
            world for world, score in self.scored_worlds if score == best_score
        )

    @property
    def candidate_worlds(self) -> frozenset[World]:
        return frozenset(world for world, _score in self.scored_worlds)


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
    max_candidates: int | None = None,
) -> ICMergeOutcome:
    """Konieczny-Pino Pérez style finite model-theoretic IC merge."""
    if max_candidates is not None and max_candidates < 0:
        raise ValueError("max_candidates must be non-negative")
    signature = frozenset(alphabet) | mu.atoms()
    for formula in profile:
        signature |= formula.atoms()
    enforce_alphabet_budget(signature, max_alphabet_size)
    distance_entries = _distance_entries(
        profile,
        signature,
        max_candidates=max_candidates,
    )
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
            distance_vectors=MappingProxyType({}),
        )
    distance_vectors = {
        world: _distance_vector(world, distance_entries)
        for world in candidates
    }
    scored = tuple(
        sorted(
            (
                (world, _score_distances(distance_vectors[world], operator))
                for world in candidates
            ),
            key=lambda item: (_score_key(item[1]), tuple(sorted(item[0]))),
        )
    )
    best_score = scored[0][1]
    winners = frozenset(world for world, score in scored if score == best_score)
    return ICMergeOutcome(
        belief_set=BeliefSet(signature, winners),
        scored_worlds=scored,
        distance_vectors=MappingProxyType(distance_vectors),
    )


def _distance_vector(
    world: World,
    distance_entries: tuple[_DistanceFormulaEntry, ...],
) -> tuple[float, ...]:
    return tuple(_distance_from_entry(world, entry) for entry in distance_entries)


def _score_distances(
    distances: tuple[float, ...],
    operator: ICMergeOperator,
) -> tuple[float, ...]:
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
    *,
    max_candidates: int | None = None,
) -> tuple[_DistanceFormulaEntry, ...]:
    return tuple(
        _DistanceFormulaEntry(
            formula=formula,
            models=_models_for_formula(
                formula,
                signature,
                max_candidates=max_candidates,
            ),
            distances={},
        )
        for formula in profile
    )


def _models_for_formula(
    formula: Formula,
    signature: frozenset[str],
    *,
    max_candidates: int | None = None,
) -> tuple[World, ...]:
    _raise_if_formula_atoms_outside_signature(formula, signature)
    models: list[World] = []
    examined = 0
    for candidate in BeliefSet.all_worlds(signature):
        if max_candidates is not None and examined >= max_candidates:
            raise EnumerationExceeded(
                partial_count=examined,
                max_candidates=max_candidates,
            )
        examined += 1
        if formula.evaluate(candidate):
            models.append(candidate)
    return tuple(models)


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
