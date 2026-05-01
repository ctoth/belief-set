from __future__ import annotations

from datetime import datetime, timezone

from belief_set import Atom, BeliefSet, SpohnEpistemicState, revise


P = Atom("p")
Q = Atom("q")
ALPHABET = frozenset({"p", "q"})


def _state() -> SpohnEpistemicState:
    return SpohnEpistemicState.from_belief_set(
        BeliefSet.from_formula(ALPHABET, P),
    )


def test_revision_trace_records_operator_pre_image_and_real_timestamp() -> None:
    before = datetime.now(timezone.utc)
    result = revise(_state(), Q)
    after = datetime.now(timezone.utc)

    trace = result.trace
    assert trace.operator == "revise"
    assert trace.pre_image_fingerprint == _state().belief_set.fingerprint()
    assert before <= trace.timestamp <= after
