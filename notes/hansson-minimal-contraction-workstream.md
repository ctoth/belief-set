# Hansson Minimal Contraction Workstream

This workstream covers the next belief-base slice after composite meet
contraction: Hansson 1989 full and partial minimal contraction on finite belief
bases.

I used the processed Hansson notes for this planning pass, especially the
sections for pp.124-126. I did not reread the full PDF or page images for this
planning pass.

## Paper-Backed Target

- Hansson p.125: `V_n A` is the set of disjunctions of at most `n` distinct
  members of `A`; `VA = V_1 A union V_2 A ...`.
- Hansson p.125: full minimal contraction computes
  `D_n = (V_n A) ~ B`, then `E_1 = D_1` and
  `E_{n+1} = E_n union (D_{n+1} \ Cn(E_n))`.
- Hansson p.126: partial minimal contraction replaces full meet in the
  `D_n` construction with simple partial meet selected by `gamma`.
- Hansson p.126: minimal contraction preserves useful disjunctive information
  but satisfies logical inclusion rather than ordinary inclusion.
- Hansson p.126 comparison example: contracting `{x, y, z}` by `x & y & z`
  distinguishes full meet, full minimal, partial meet, safe contraction, and
  partial minimal outputs.

## Execution Rules

- Add failing focused tests first, then implementation.
- Keep each production change small and path-owned.
- After every edited file, commit atomically before moving to the next slice.
- Validate this workstream order with:
  `uv run scripts/check_workstream_order.py notes/hansson-minimal-contraction-workstream.md`.

## Workstream

### WF-1 Minimal contraction invariant ledger
**Depends on:** none

Record the p.125-126 invariants as the active control surface for this slice.
The target API is `BeliefBase.disjunction_expansion`,
`BeliefBase.full_minimal_contract`, and
`BeliefBase.partial_minimal_contract`.

### TDD-1 Disjunction expansion property
**Depends on:** WF-1

Add red focused tests for `V_n A`: for a finite base, `disjunction_expansion(n)`
contains every original formula for `n = 1`, contains every disjunction of up
to `n` distinct base formulas, preserves deterministic source order, and
rejects `n < 1`.

### FIX-1 Disjunction expansion implementation
**Depends on:** TDD-1

Implement `BeliefBase.disjunction_expansion(max_size)`. Use existing formula
constructors, preserve stable order by combination size and source order, and
dedupe formulas without collapsing source-level distinction beyond formula
object equality.

### TDD-2 Full minimal recurrence property
**Depends on:** FIX-1

Add red tests for the p.125 recurrence:
`D_n = (V_n A) ~ B`, `E_1 = D_1`, and
`E_{n+1} = E_n union (D_{n+1} \ Cn(E_n))`. The tests should assert that a
candidate from `D_{n+1}` is kept exactly when it is not already entailed by the
current `E_n` base.

### FIX-2 Full minimal recurrence implementation
**Depends on:** TDD-2

Implement a small private recurrence helper that builds `E_n` from a supplied
`D_n` producer, then implement `BeliefBase.full_minimal_contract(forbidden)`.
The finite implementation may iterate `n = 1..len(base.formulas)` because no
new disjunctions beyond the full base size are needed for finite source bases.

### TDD-3 Full minimal contraction example
**Depends on:** FIX-2

Add the Hansson p.126 comparison example for full minimal contraction:
contracting `{x, y, z}` by `x & y & z` should retain the pairwise disjunctions
`x or y`, `x or z`, and `y or z`, while avoiding the contracted conjunction.

### FIX-3 Full minimal example conformance
**Depends on:** TDD-3

Fix any gap between the recurrence implementation and the p.126 full minimal
example without adding special-case logic. The example must fall out of the
general `V_n A` and recurrence machinery.

### TDD-4 Partial minimal recurrence property
**Depends on:** FIX-3

Add red tests for p.126 partial minimal contraction:
`D_n = (V_n A) ~_gamma B`, then the same `E_n` recurrence. Include a selector
that chooses one prioritized remainder at each `D_n` level.

### FIX-4 Partial minimal contraction implementation
**Depends on:** TDD-4

Implement `BeliefBase.partial_minimal_contract(forbidden, selector)` by
reusing the recurrence helper and using `simple_partial_meet_contract` over
each `V_n A` base.

### TDD-5 Logical inclusion and non-inclusion properties
**Depends on:** FIX-4

Add tests showing minimal contraction satisfies logical inclusion:
`Cn(A - B) subseteq Cn(A)`, while allowing formulas not literally present in
the original base. Also assert the result avoids the non-tautological
contracted-away inputs.

### FIX-5 Minimal contraction postulate cleanup
**Depends on:** TDD-5

Adjust full and partial minimal contraction so they satisfy logical inclusion
and avoidance for the finite extensional implementation. Keep failure modes
explicit for invalid selectors or impossible recurrence states.

### DOC-1 Public documentation
**Depends on:** FIX-5

Update the README belief-base section to name `disjunction_expansion`,
`full_minimal_contract`, and `partial_minimal_contract`, and explain that these
operators can introduce useful disjunctions while guaranteeing logical
inclusion rather than ordinary source-formula inclusion.

## Definition of Done

- `uv run scripts/check_workstream_order.py notes/hansson-minimal-contraction-workstream.md`
  passes.
- Focused Hansson belief-base tests pass.
- `uv run pytest -q` passes.
- `uv run pyright` passes.
- The new minimal-contraction APIs are documented and exported only if they are
  intended as public package surface.
