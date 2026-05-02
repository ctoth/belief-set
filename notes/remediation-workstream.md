# belief_set Remediation Workstream

This plan is based on the processed paper notes and claims already present in
`./papers`. I did not reread source PDFs or page images for this planning pass.

## Paper-Backed Ground Truth

- Spohn 1988: an OCF has kappa(empty)=Omega, kappa(W)=0, and
  kappa(A)=min{kappa(w) | w in A} for non-empty propositions. In this package,
  `math.inf` is the finite implementation of Omega.
- Spohn 1988: OCF conditionalization must stay inside the class of OCFs. No
  revision path may create NaN, lose the zero-minimum property, or turn
  contradiction into tautology.
- AGM 1985 and Gardenfors-Makinson 1988: contraction is constrained by
  inclusion, success for non-tautologies, extensionality, recovery, and the
  Harper identity K-A = K intersect K*not-A.
- Gardenfors-Makinson 1988: epistemic entrenchment must satisfy EE1-EE5, and
  contraction/revision behavior must be recoverable from the entrenchment view.
- Booth-Meyer 2006: restrained revision preserves old strict ordering outside
  the minimal alpha-worlds and only splits equal alpha/not-alpha levels as much
  as needed for admissibility. Lexicographic revision is the high-authority
  extreme; restrained revision is the conservative admissible extreme.
- Konieczny-Pino Perez 2002: IC merging is over finite propositional
  interpretations; Sigma is sum-distance majority merging, GMax is sorted-vector
  lexicographic arbitration, and IC0-IC8 are the correctness envelope.

## Execution Rules

- Each slice starts by adding a failing focused or Hypothesis test that names the
  paper-backed invariant it protects.
- Production code is changed only after the failing test demonstrates the bug.
- Each kept slice ends with targeted tests, then full `uv run pytest`, then
  `uv run pyright`.
- Each edited file is committed atomically before moving to the next slice.
- This file is ordered topologically. Validate with:
  `uv run scripts/check_workstream_order.py notes/remediation-workstream.md`.

## Workstream

### WF-1 Paper invariant ledger
**Depends on:** none

Create this workstream and pin every remediation target to a paper invariant.
This prevents implementation cleanup from drifting away from the formal
contract.

### TDD-1 OCF contradiction preservation tests
**Depends on:** WF-1

Add Hypothesis and focused examples showing that
`SpohnEpistemicState.from_belief_set(BeliefSet.contradiction(alphabet))`
produces all-infinite ranks and an inconsistent belief set, never tautology.
Also generate inconsistent/all-infinite states and revise them by satisfiable
and unsatisfiable formulas; assert no NaN ranks and no contradiction laundering.

### FIX-1 OCF contradiction preservation
**Depends on:** TDD-1

Change `from_belief_set` and revision over all-infinite states so Spohn's
kappa(empty)=Omega and kappa(W)=0 invariants are preserved. Target behavior:
contradictory prior plus ordinary revision remains contradictory unless a
paper-backed operator explicitly reconstructs a finite OCF from new evidence;
no path emits NaN.

### TDD-2 Harper contraction alphabet tests
**Depends on:** FIX-1

Add tests for `full_meet_contract` when the contraction formula introduces new
atoms, including tautological formulas over a larger alphabet. Assert
`outcome.belief_set.alphabet == outcome.state.alphabet`, no `KeyError`, and
the belief set equals `K intersect K*not-A` over the shared signature.

### FIX-2 Harper contraction over extended signatures
**Depends on:** TDD-2

Make contraction compute prior and revised ranks over one aligned signature
before applying the Harper min construction. The returned belief set and state
must share that signature.

### TDD-3 State immutability and OCF validity tests
**Depends on:** FIX-2

Add tests that generated `SpohnEpistemicState` objects expose ranks read-only,
reject missing worlds, reject invalid finite ranks, and preserve a finite
minimum of zero whenever the state is not all-infinite.

### FIX-3 Read-only Spohn state surface
**Depends on:** TDD-3

Store normalized ranks behind a read-only mapping and type the public field as
`Mapping[World, int | float]`. Keep construction through `from_ranks` as the
single normalization boundary.

### TDD-4 Formula equivalence boundary tests
**Depends on:** FIX-3

Add focused tests for `equivalent(left, right, alphabet=frozenset())` and
Hypothesis tests over explicit alphabets, including empty alphabets, to prove
the caller-supplied alphabet is honored exactly.

### FIX-4 Honor explicit empty alphabets
**Depends on:** TDD-4

Replace truthiness checks on optional alphabets with `is None` checks. Audit for
the same bug pattern in public constructors.

### TDD-5 Enumeration budget tests
**Depends on:** FIX-4

Add Hypothesis tests that every public operator that enumerates worlds enforces
a caller-visible alphabet budget: `revise`, `full_meet_contract`,
`lexicographic_revise`, `restrained_revise`, entrenchment comparison, and
`merge_belief_profile`.

### FIX-5 Public alphabet budget surface
**Depends on:** TDD-5

Introduce one hard-precondition exception for alphabet-budget violations and
reserve `EnumerationExceeded` for interrupted anytime search. Thread
`max_alphabet_size` through every public enumeration entrypoint.

### TDD-6 IC merge cache and formula protocol tests
**Depends on:** FIX-5

Add tests with unhashable formula implementations, mutable formula
implementations, and formulas whose `atoms()` exceed a supplied signature.
Assert public merge is deterministic across repeated calls and cannot reuse
stale model sets across changed formula semantics.

### FIX-6 Local IC distance oracle
**Depends on:** TDD-6

Delete the module-global distance cache. Build a per-merge distance oracle that
uses the current call's formulas and signature only. Keep private distance
helpers simple and make unsupported formula/signature combinations fail at the
boundary instead of silently treating absent atoms as false.

### TDD-7 IC empty profile and score-shape tests
**Depends on:** FIX-6

Add tests documenting empty-profile semantics as exactly the integrity
constraint models, and tests that `ICMergeOutcome.scored_worlds` has one
uniform score representation for Sigma and GMax.

### FIX-7 IC outcome normalization
**Depends on:** TDD-7

Represent all IC scores as tuples. For Sigma, use a one-element tuple. For GMax,
use the sorted distance tuple. Document and implement empty-profile merge as
returning the belief set induced by `mu`.

### TDD-8 Deterministic semantic equality tests
**Depends on:** FIX-7

Add tests showing two semantically identical revision outcomes compare equal
even though their trace timestamps differ, while trace metadata remains
available for audit.

### FIX-8 Trace timestamp comparison cleanup
**Depends on:** TDD-8

Mark `RevisionTrace.timestamp` as non-comparing data or split audit metadata
from semantic outcome equality. Keep timestamp assertions for trace freshness.

### TDD-9 Public surface and dead-stub tests
**Depends on:** FIX-8

Add import tests for the intended public package surface, including
entrenchment and IC merge symbols if they remain public APIs. Add a test that
either removes `BeliefSet.cn()` from the public contract or proves its role as
the extensional closure identity.

### FIX-9 Public API cleanup
**Depends on:** TDD-9

Make `__all__` match the documented public surface. Delete dead stubs or
document them as formal identities. Collapse duplicate `extend_state`
implementation into one canonical function.

### TDD-10 Paper postulate property sweep
**Depends on:** FIX-9

Broaden existing property tests with generated small alphabets and formula
families for Spohn OCF invariants, AGM K* and K- postulates, EE1-EE5,
Booth-Meyer restrained-revision conditions, and KPP IC0-IC8 plus Maj/Arb.

### FIX-10 Final conformance pass
**Depends on:** TDD-10

Fix any remaining failures from the property sweep without adding compatibility
bridges. The final state is one target architecture: finite propositional
belief-set kernels with bounded enumeration, read-only OCF states, paper-backed
AGM/iterated/entrenchment/IC behavior, and no old production path left alive.

## Definition of Done

- `uv run scripts/check_workstream_order.py notes/remediation-workstream.md`
  passes.
- `uv run pytest` passes.
- `uv run pyright` passes.
- No production path can turn contradiction into tautology, create NaN ranks, or
  return outcome objects whose belief set and epistemic state disagree on
  alphabet.
- Public enumeration entrypoints all expose the same budget semantics.
- All workstream items are either complete or explicitly deferred by the user.
