# Architecture

`belief_set` is a finite formal-kernel package. Its runtime boundary is the
propositional model theory needed by reusable belief-revision algorithms.

The package owns in-memory formal objects and deterministic operators over
those objects. Applications that need persistence, provenance, paper
management, command-line workflows, or presentation layers should adapt their
data into package objects at the boundary.

## Runtime Model

- `World` is `frozenset[str]`: the atoms true in one propositional valuation.
- `Formula` is a protocol with `evaluate(world)` and `atoms()`.
- `BeliefSet` is extensional: it stores an alphabet and the worlds that model
  the theory over that alphabet.
- `SpohnEpistemicState` stores one non-negative rank for every world in its
  alphabet, normalizing finite ranks so the minimum finite rank is `0`.
- Operators that combine objects first align or extend alphabets, then run over
  all worlds in the resulting signature.

This architecture favors clarity and testability over scale. It is suitable as
a reference kernel for small finite signatures, not as a SAT/SMT-backed reasoner
for large languages.

## Owned Surface

- propositional formula protocol and finite formula constructors
- finite worlds represented as `frozenset[str]`
- extensional `BeliefSet` values over finite alphabets
- Spohn ordinal conditional functions over complete finite world maps
- AGM revision and full-meet contraction over finite theories
- lexicographic and restrained iterated revision
- epistemic entrenchment induced by Spohn negation ranks
- finite IC merge with sigma and gmax aggregation
- bounded-enumeration failure types used by these algorithms

## Non-Owned Surface

Applications that consume this package own their own:

- persistence and storage
- provenance graphs, witnesses, and audit trails outside `RevisionTrace`
- repository, source, context, claim, stance, sidecar, and worldline concepts
- command-line and presentation behavior
- argumentation-framework adapters
- scalable solver-backed reasoning

Those concerns should remain outside the package unless they become part of a
general formal-kernel abstraction.

## Invariants

- A `BeliefSet` never contains models outside its declared alphabet.
- `BeliefSet.from_formula()` extends the declared alphabet with atoms mentioned
  by the formula.
- `BeliefSet.cn()` is identity because closure is represented extensionally.
- A `SpohnEpistemicState` rank map must cover every world over its alphabet.
- Spohn ranks must be non-negative and must not be `NaN`.
- A contradictory Spohn state is represented by all-infinite ranks.
- Public revision and merge entrypoints enforce `max_alphabet_size` before
  enumerating worlds.
- IC merge profile formulas must be satisfiable over the merged signature.

## Failure Semantics

`AlphabetBudgetExceeded` is a precondition failure. It means the requested
signature exceeds the caller's configured world-enumeration budget.

`EnumerationExceeded` represents an interrupted bounded scan in private
anytime-style distance code. Public merge does not treat it as an approximate
score.

`ICMergeProfileMemberInconsistent` means at least one profile member has no
models over the merged signature. The merge is rejected instead of scoring that
member as a usable finite source.

## Paper Assets

The package keeps processed notes and metadata for papers that specify the
formal algorithms it owns. Source PDFs and rendered page PNGs may be present in
the working tree for local reading, but they are ignored by Git and are not
tracked package artifacts.
