from __future__ import annotations

import pytest

from belief_set import Atom, BeliefSet, SpohnEpistemicState, conjunction, full_meet_contract, revise
from belief_set.anytime import AlphabetBudgetExceeded
from belief_set.entrenchment import EpistemicEntrenchment
from belief_set.ic_merge import merge_belief_profile
from belief_set.iterated import lexicographic_revise, restrained_revise


def _state() -> SpohnEpistemicState:
    return SpohnEpistemicState.from_belief_set(
        BeliefSet.tautology(frozenset({"p"})),
    )


def test_revise_raises_hard_alphabet_budget_exception() -> None:
    with pytest.raises(AlphabetBudgetExceeded):
        revise(_state(), conjunction(Atom("p"), Atom("q")), max_alphabet_size=1)


def test_contract_raises_hard_alphabet_budget_exception() -> None:
    with pytest.raises(AlphabetBudgetExceeded):
        full_meet_contract(_state(), conjunction(Atom("p"), Atom("q")), max_alphabet_size=1)


def test_lexicographic_revise_raises_hard_alphabet_budget_exception() -> None:
    with pytest.raises(AlphabetBudgetExceeded):
        lexicographic_revise(_state(), conjunction(Atom("p"), Atom("q")), max_alphabet_size=1)


def test_restrained_revise_raises_hard_alphabet_budget_exception() -> None:
    with pytest.raises(AlphabetBudgetExceeded):
        restrained_revise(_state(), conjunction(Atom("p"), Atom("q")), max_alphabet_size=1)


def test_entrenchment_raises_hard_alphabet_budget_exception() -> None:
    entrenchment = EpistemicEntrenchment.from_state(_state())

    with pytest.raises(AlphabetBudgetExceeded):
        entrenchment.leq(Atom("p"), Atom("q"), max_alphabet_size=1)


def test_ic_merge_raises_hard_alphabet_budget_exception() -> None:
    with pytest.raises(AlphabetBudgetExceeded):
        merge_belief_profile(
            frozenset({"p"}),
            (Atom("q"),),
            Atom("p"),
            max_alphabet_size=1,
        )
