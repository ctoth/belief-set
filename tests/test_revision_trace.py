from __future__ import annotations

from datetime import datetime, timedelta, timezone

from belief_set import Atom, BeliefSet, RevisionOutcome, RevisionTrace, SpohnEpistemicState, revise


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


def test_revision_outcome_semantic_equality_ignores_trace_timestamp() -> None:
    result = revise(_state(), Q)
    same_semantics_later_trace = RevisionOutcome(
        belief_set=result.belief_set,
        state=result.state,
        trace=RevisionTrace(
            operator=result.trace.operator,
            pre_image_fingerprint=result.trace.pre_image_fingerprint,
            timestamp=result.trace.timestamp + timedelta(seconds=1),
        ),
    )

    assert result.trace.timestamp != same_semantics_later_trace.trace.timestamp
    assert result == same_semantics_later_trace
