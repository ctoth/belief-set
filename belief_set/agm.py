from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType

from belief_set.anytime import enforce_alphabet_budget
from belief_set.core import BeliefSet, expand
from belief_set.language import Formula, World, negate


MAX_ALPHABET_SIZE = 16


@dataclass(frozen=True, slots=True)
class RevisionTrace:
    operator: str
    pre_image_fingerprint: str
    timestamp: datetime = field(compare=False)


@dataclass(frozen=True, slots=True)
class RevisionOutcome:
    belief_set: BeliefSet
    state: SpohnEpistemicState
    trace: RevisionTrace


@dataclass(frozen=True, slots=True)
class SpohnEpistemicState:
    """Finite ordinal conditional function over propositional worlds."""

    alphabet: frozenset[str]
    ranks: Mapping[World, int | float]

    def __post_init__(self) -> None:
        signature = frozenset(self.alphabet)
        worlds = BeliefSet.all_worlds(signature)
        input_ranks = {frozenset(world): rank for world, rank in self.ranks.items()}
        if set(input_ranks) != set(worlds):
            raise ValueError("SpohnEpistemicState ranks must cover every world in the alphabet")
        _raise_for_invalid_ranks(input_ranks)
        if all(math.isinf(float(rank)) for rank in input_ranks.values()):
            normalized_ranks = {world: math.inf for world in input_ranks}
            object.__setattr__(self, "ranks", MappingProxyType(normalized_ranks))
            object.__setattr__(self, "alphabet", signature)
            return

        finite_ranks = [
            float(rank)
            for rank in input_ranks.values()
            if not math.isinf(float(rank))
        ]
        min_rank = min(finite_ranks, default=0.0)
        normalized_ranks = {
            world: _normalize_rank(rank, min_rank)
            for world, rank in input_ranks.items()
        }
        object.__setattr__(
            self,
            "ranks",
            MappingProxyType(normalized_ranks),
        )
        object.__setattr__(self, "alphabet", signature)

    @classmethod
    def from_ranks(
        cls,
        alphabet: frozenset[str],
        ranks: Mapping[World, int | float],
    ) -> SpohnEpistemicState:
        return cls(alphabet=frozenset(alphabet), ranks=dict(ranks))

    @classmethod
    def from_belief_set(cls, belief_set: BeliefSet) -> SpohnEpistemicState:
        worlds = BeliefSet.all_worlds(belief_set.alphabet)
        if not belief_set.models:
            return cls(
                alphabet=belief_set.alphabet,
                ranks={world: math.inf for world in worlds},
            )
        return cls(
            alphabet=belief_set.alphabet,
            ranks={
                world: 0 if world in belief_set.models else 1
                for world in worlds
            },
        )

    @property
    def belief_set(self) -> BeliefSet:
        min_rank = min(self.ranks.values(), default=0)
        if math.isinf(float(min_rank)):
            return BeliefSet.contradiction(self.alphabet)
        return BeliefSet(
            self.alphabet,
            frozenset(world for world, rank in self.ranks.items() if rank == min_rank),
        )

    def rank(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> int | float:
        """Return Spohn's proposition rank: the minimum rank of its worlds."""
        signature = self.alphabet | formula.atoms()
        enforce_alphabet_budget(signature, max_alphabet_size)
        state = extend_state(self, signature)
        formula_ranks = tuple(
            rank for world, rank in state.ranks.items() if formula.evaluate(world)
        )
        if not formula_ranks:
            return math.inf
        return min(formula_ranks)

    def minimal_worlds(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> frozenset[World]:
        """Return the minimal formula-worlds selected by the ranking."""
        signature = self.alphabet | formula.atoms()
        enforce_alphabet_budget(signature, max_alphabet_size)
        state = extend_state(self, signature)
        best_rank = state.rank(formula, max_alphabet_size=max_alphabet_size)
        if math.isinf(float(best_rank)):
            return frozenset()
        return frozenset(
            world
            for world, rank in state.ranks.items()
            if rank == best_rank and formula.evaluate(world)
        )

    def firmness(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> int | float:
        """Return Spohn's signed firmness of belief for a formula."""
        formula_rank = self.rank(formula, max_alphabet_size=max_alphabet_size)
        if formula_rank == 0:
            return self.rank(negate(formula), max_alphabet_size=max_alphabet_size)
        return -formula_rank

    def is_believed(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> bool:
        """Return whether the formula is in the OCF's believed content."""
        return self.rank(negate(formula), max_alphabet_size=max_alphabet_size) > 0

    def is_disbelieved(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> bool:
        """Return whether the formula is disbelieved in the OCF."""
        return self.firmness(formula, max_alphabet_size=max_alphabet_size) < 0

    def is_neutral(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> bool:
        """Return whether the OCF is neutral toward the formula."""
        return self.firmness(formula, max_alphabet_size=max_alphabet_size) == 0

    def conditionalize(
        self,
        formula: Formula,
        *,
        firmness: int | float,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> SpohnEpistemicState:
        """Return Spohn's finite A,alpha-conditionalization of this OCF."""
        firmness_value = _checked_firmness(firmness)
        signature = self.alphabet | formula.atoms()
        enforce_alphabet_budget(signature, max_alphabet_size)
        state = extend_state(self, signature)
        worlds = BeliefSet.all_worlds(signature)
        formula_worlds = frozenset(world for world in worlds if formula.evaluate(world))
        counter_worlds = worlds - formula_worlds
        if not formula_worlds or not counter_worlds:
            raise ValueError("conditionalization formula must be satisfiable and non-tautological")
        formula_rank = state.rank(formula, max_alphabet_size=max_alphabet_size)
        counter_rank = state.rank(negate(formula), max_alphabet_size=max_alphabet_size)
        if math.isinf(float(formula_rank)) or math.isinf(float(counter_rank)):
            raise ValueError("conditionalization parts must have finite ranks")

        ranks: dict[World, int | float] = {}
        for world in worlds:
            current_rank = state.ranks[world]
            if formula.evaluate(world):
                ranks[world] = current_rank - formula_rank
            else:
                ranks[world] = firmness_value + current_rank - counter_rank
        return SpohnEpistemicState.from_ranks(signature, ranks)


def revise(
    state: SpohnEpistemicState,
    formula: Formula,
    *,
    max_alphabet_size: int = MAX_ALPHABET_SIZE,
) -> RevisionOutcome:
    """Darwiche-Pearl 1997 bullet revision over a Spohn ranking."""
    signature = state.alphabet | formula.atoms()
    enforce_alphabet_budget(signature, max_alphabet_size)
    working_state = extend_state(state, signature)
    worlds = BeliefSet.all_worlds(signature)
    satisfying = tuple(world for world in worlds if formula.evaluate(world))
    if _all_ranks_infinite(working_state):
        result_state = SpohnEpistemicState.from_ranks(
            signature,
            {world: math.inf for world in worlds},
        )
    elif not satisfying:
        result_state = SpohnEpistemicState.from_ranks(
            signature,
            {world: math.inf for world in worlds},
        )
    else:
        min_formula_rank = min(working_state.ranks[world] for world in satisfying)
        if math.isinf(float(min_formula_rank)):
            result_state = SpohnEpistemicState.from_belief_set(
                BeliefSet(signature, frozenset(satisfying)),
            )
        else:
            revised_ranks: dict[World, int | float] = {}
            for world in worlds:
                current_rank = working_state.ranks[world]
                if formula.evaluate(world):
                    revised_ranks[world] = current_rank - min_formula_rank
                else:
                    revised_ranks[world] = current_rank + 1
            result_state = SpohnEpistemicState.from_ranks(signature, revised_ranks)
    return RevisionOutcome(
        belief_set=result_state.belief_set,
        state=result_state,
        trace=revision_trace("revise", state.belief_set),
    )


def full_meet_contract(
    state: SpohnEpistemicState,
    formula: Formula,
    *,
    max_alphabet_size: int = MAX_ALPHABET_SIZE,
) -> RevisionOutcome:
    """AGM contraction using the Harper identity over the finite theory."""
    signature = state.alphabet | formula.atoms()
    enforce_alphabet_budget(signature, max_alphabet_size)
    working_state = extend_state(state, signature)
    if not working_state.belief_set.entails(formula):
        return RevisionOutcome(
            belief_set=working_state.belief_set,
            state=working_state,
            trace=revision_trace("contract", state.belief_set),
        )
    revised_by_negation = revise(
        working_state,
        negate(formula),
        max_alphabet_size=max_alphabet_size,
    )
    contracted = working_state.belief_set.intersection_theory(revised_by_negation.belief_set)
    contracted_ranks = {
        world: min(working_state.ranks[world], revised_by_negation.state.ranks[world])
        for world in BeliefSet.all_worlds(signature)
    }
    return RevisionOutcome(
        belief_set=contracted,
        state=SpohnEpistemicState.from_ranks(signature, contracted_ranks),
        trace=revision_trace("contract", state.belief_set),
    )


def levi_revise(
    state: SpohnEpistemicState,
    formula: Formula,
    *,
    max_alphabet_size: int = MAX_ALPHABET_SIZE,
) -> RevisionOutcome:
    """AGM revision via Levi identity: contract not-formula, then expand."""
    contracted = full_meet_contract(
        state,
        negate(formula),
        max_alphabet_size=max_alphabet_size,
    )
    belief_set = expand(contracted.belief_set, formula)
    revised_state = SpohnEpistemicState.from_belief_set(belief_set)
    return RevisionOutcome(
        belief_set=belief_set,
        state=revised_state,
        trace=revision_trace("levi_revise", state.belief_set),
    )


def extend_state(state: SpohnEpistemicState, alphabet: frozenset[str]) -> SpohnEpistemicState:
    if alphabet == state.alphabet:
        return state
    extras = tuple(sorted(alphabet - state.alphabet))
    ranks: dict[World, int | float] = {}
    for world, rank in state.ranks.items():
        for extension in BeliefSet.all_worlds(frozenset(extras)):
            ranks[frozenset(set(world) | set(extension))] = rank
    return SpohnEpistemicState.from_ranks(alphabet, ranks)


def _normalize_rank(rank: int | float, min_rank: float) -> int | float:
    rank_value = float(rank)
    if math.isinf(rank_value):
        return math.inf
    normalized = max(0.0, rank_value - min_rank)
    if normalized.is_integer():
        return int(normalized)
    return normalized


def _raise_for_invalid_ranks(ranks: Mapping[World, int | float]) -> None:
    for rank in ranks.values():
        rank_value = float(rank)
        if math.isnan(rank_value):
            raise ValueError("SpohnEpistemicState ranks must not be NaN")
        if rank_value < 0:
            raise ValueError("SpohnEpistemicState ranks must be non-negative")


def _checked_firmness(firmness: int | float) -> int | float:
    firmness_value = float(firmness)
    if math.isnan(firmness_value):
        raise ValueError("conditionalization firmness must not be NaN")
    if firmness_value < 0:
        raise ValueError("conditionalization firmness must be non-negative")
    if firmness_value.is_integer():
        return int(firmness_value)
    return firmness_value


def _all_ranks_infinite(state: SpohnEpistemicState) -> bool:
    return all(math.isinf(float(rank)) for rank in state.ranks.values())


def _trace_timestamp() -> datetime:
    return datetime.now(timezone.utc)


def revision_trace(
    operator: str,
    pre_image: BeliefSet,
) -> RevisionTrace:
    timestamp = _trace_timestamp()
    return RevisionTrace(
        operator=operator,
        pre_image_fingerprint=pre_image.fingerprint(),
        timestamp=timestamp,
    )
