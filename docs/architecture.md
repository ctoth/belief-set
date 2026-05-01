# Architecture

`belief_set` is a finite formal-kernel package. Its runtime boundary is the
propositional model theory needed by reusable belief-revision algorithms.

## Owned Surface

- propositional formula protocol and finite formula constructors
- finite worlds represented as `frozenset[str]`
- extensional `BeliefSet` values over finite alphabets
- Spohn ordinal conditional functions
- AGM revision and contraction over finite theories
- lexicographic and restrained iterated revision
- epistemic entrenchment induced by Spohn negation ranks
- finite IC merge with sigma and gmax aggregation
- bounded-enumeration failure types used by these algorithms

## Caller Surface

Applications that consume this package own their own persistence, provenance,
repository, source, context, claim, stance, worldline, command-line, and
presentation concerns. Those concerns should adapt into package objects at the
boundary instead of becoming package dependencies.

## Paper Assets

The package keeps processed notes and metadata for papers that specify the
formal algorithms it owns. Source PDFs and rendered page PNGs may be present in
the working tree for local reading, but they are ignored by Git.
