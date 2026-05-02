# belief_set

`belief_set` is a small Python package for finite formal belief sets and
belief-revision kernels. It owns the reusable model-theoretic machinery for
finite propositional belief sets, AGM-style revision and contraction, iterated
revision, epistemic entrenchment, and IC belief merging.

The package uses a flat layout:

```text
belief_set/
tests/
```

## Install

Install from a pushed Git commit:

```powershell
uv add "formal-belief-set @ git+https://github.com/ctoth/belief-set@<commit>"
```

Use an immutable pushed commit or tag. Do not pin consumers to a local checkout.

## Public Imports

```python
from belief_set import (
    Atom,
    BeliefSet,
    EpistemicEntrenchment,
    ICMergeOperator,
    SpohnEpistemicState,
    conjunction,
    full_meet_contract,
    lexicographic_revise,
    merge_belief_profile,
    restrained_revise,
    revise,
)
```

## Formula And Belief-Set Examples

```python
from belief_set import Atom, BeliefSet, conjunction, negate

p = Atom("p")
q = Atom("q")
alphabet = frozenset({"p", "q"})

beliefs = BeliefSet.from_formula(alphabet, conjunction(p, q))
assert beliefs.entails(p)
assert not beliefs.entails(negate(p))
```

`BeliefSet` is extensional: it stores the finite alphabet and the worlds that
model the theory.

## AGM Revision And Contraction

```python
from belief_set import Atom, BeliefSet, SpohnEpistemicState, full_meet_contract, revise

p = Atom("p")
initial = BeliefSet.from_formula(frozenset({"p"}), p)
state = SpohnEpistemicState.from_belief_set(initial)

revision = revise(state, p)
contraction = full_meet_contract(revision.state, p)
```

Revision returns a `RevisionOutcome` with the revised belief set, resulting
Spohn state, and package-local trace metadata.

## Iterated Revision

```python
from belief_set import Atom, BeliefSet, SpohnEpistemicState, lexicographic_revise, restrained_revise

p = Atom("p")
state = SpohnEpistemicState.from_belief_set(BeliefSet.tautology(frozenset({"p"})))

lexicographic = lexicographic_revise(state, p)
restrained = restrained_revise(state, p)
```

The iterated operators preserve the finite Spohn-ranking representation and
return the same `RevisionOutcome` shape as AGM revision.

## IC Merge

```python
from belief_set import Atom, BOTTOM, ICMergeOperator, conjunction, merge_belief_profile

p = Atom("p")
q = Atom("q")

outcome = merge_belief_profile(
    frozenset({"p", "q"}),
    profile=(p, q),
    mu=conjunction(p, q),
    operator=ICMergeOperator.SIGMA,
)
assert outcome.belief_set.is_consistent
```

`merge_belief_profile` implements finite model-theoretic IC merging over a
profile, an integrity constraint, and either sigma or gmax aggregation.

## Non-Goals

This package deliberately does not own:

- caller-owned provenance graphs or witness objects
- source, context, claim, stance, sidecar, storage, worldline, repository, or
  CLI behavior
- argumentation-framework revision adapters
- compatibility imports for older owner-specific module paths

## Paper Assets

Processed paper notes and metadata belong in `papers/` when they specify
package-owned formal algorithms. Source PDFs and rendered page PNGs may be
present in the working tree for local paper reading, but they are intentionally
ignored by Git and are not tracked package artifacts.
