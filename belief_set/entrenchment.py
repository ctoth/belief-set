from __future__ import annotations

from dataclasses import dataclass

from belief_set.agm import MAX_ALPHABET_SIZE, SpohnEpistemicState, extend_state
from belief_set.anytime import enforce_alphabet_budget
from belief_set.core import BeliefSet
from belief_set.language import Formula, negate


@dataclass(frozen=True, slots=True)
class EpistemicEntrenchment:
    """Gärdenfors-Makinson style entrenchment induced by a Spohn ranking."""

    state: SpohnEpistemicState

    @classmethod
    def from_state(cls, state: SpohnEpistemicState) -> EpistemicEntrenchment:
        return cls(state=state)

    def leq(
        self,
        left: Formula,
        right: Formula,
        *,
        max_alphabet_size: int = MAX_ALPHABET_SIZE,
    ) -> bool:
        """Return whether ``left`` is no more entrenched than ``right``."""
        return self._negation_rank(
            left,
            max_alphabet_size=max_alphabet_size,
        ) <= self._negation_rank(
            right,
            max_alphabet_size=max_alphabet_size,
        )

    def _negation_rank(
        self,
        formula: Formula,
        *,
        max_alphabet_size: int,
    ) -> float:
        signature = self.state.alphabet | formula.atoms()
        enforce_alphabet_budget(signature, max_alphabet_size)
        state = self.state
        if signature != state.alphabet:
            state = extend_state(state, signature)
        countermodels = [
            world
            for world in BeliefSet.all_worlds(signature)
            if negate(formula).evaluate(world)
        ]
        if not countermodels:
            return float("inf")
        return float(min(state.ranks[world] for world in countermodels))
