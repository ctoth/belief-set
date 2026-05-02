# belief_set

`belief_set` is a small pure-Python package for finite propositional belief
sets and belief-revision kernels. It provides model-theoretic machinery for
AGM-style revision and contraction, Spohn ranking states, iterated revision,
epistemic entrenchment, and IC belief merging.

This is a finite-world reference implementation. Given an alphabet of `n`
atoms, operators enumerate up to `2^n` worlds, so the alphabet is the primary
cost dimension. Public enumeration entrypoints expose a `max_alphabet_size`
guard and raise `AlphabetBudgetExceeded` when a caller asks for more worlds
than the configured budget permits.

Status: experimental `0.1.0`, Python `>=3.11`, installed from Git commits.
No license is declared in this repository yet.

## Install

Install from an immutable pushed commit or tag:

```powershell
uv add "formal-belief-set @ git+https://github.com/ctoth/belief-set@<commit>"
```

Do not pin consumers to a local checkout, local path, or editable local
repository URL.

## Public Surface

```python
from belief_set import (
    AlphabetBudgetExceeded,
    Atom,
    BeliefSet,
    EpistemicEntrenchment,
    ICMergeOperator,
    SpohnEpistemicState,
    conjunction,
    disjunction,
    equivalent,
    expand,
    full_meet_contract,
    lexicographic_revise,
    merge_belief_profile,
    negate,
    restrained_revise,
    revise,
    theory_subset,
)
```

Module map:

- `language`: formula protocol, atoms, boolean connectives, equivalence checks.
- `core`: extensional finite belief sets represented by their model worlds.
- `agm`: Spohn epistemic states, AGM-style revision, Harper contraction traces.
- `iterated`: lexicographic and restrained iterated revision operators.
- `entrenchment`: epistemic entrenchment comparisons induced by a Spohn state.
- `ic_merge`: Konieczny-Pino Perez style sigma and gmax IC merging.
- `anytime`: bounded enumeration exceptions and alphabet-budget checks.

## Basic Belief Sets

```python
from belief_set import Atom, BeliefSet, conjunction, negate

p = Atom("p")
q = Atom("q")
alphabet = frozenset({"p", "q"})

beliefs = BeliefSet.from_formula(alphabet, conjunction(p, q))

assert beliefs.entails(p)
assert not beliefs.entails(negate(p))
assert beliefs.cn() is beliefs
```

`BeliefSet` is extensional: it stores a finite alphabet and the worlds that
model the theory. `cn()` is therefore the identity operation, because the
object already represents the deductive closure over the declared finite
alphabet.

## AGM Revision And Contraction

```python
from belief_set import Atom, BeliefSet, SpohnEpistemicState, full_meet_contract, revise

p = Atom("p")
initial = BeliefSet.from_formula(frozenset({"p"}), p)
state = SpohnEpistemicState.from_belief_set(initial)

revision = revise(state, p)
contraction = full_meet_contract(revision.state, p)

assert revision.belief_set.entails(p)
assert contraction.belief_set.alphabet == contraction.state.alphabet
```

Revision and contraction return `RevisionOutcome` objects containing the
resulting belief set, resulting Spohn state, and package-local trace metadata.
Contradictory belief sets are represented by all-infinite Spohn ranks and are
not silently laundered into tautologies.

## Iterated Revision

```python
from belief_set import Atom, BeliefSet, SpohnEpistemicState, lexicographic_revise, restrained_revise

p = Atom("p")
state = SpohnEpistemicState.from_belief_set(BeliefSet.tautology(frozenset({"p"})))

lexicographic = lexicographic_revise(state, p)
restrained = restrained_revise(state, p)

assert lexicographic.belief_set.entails(p)
assert restrained.belief_set.entails(p)
```

The iterated operators preserve the finite Spohn-ranking representation and
return the same `RevisionOutcome` shape as AGM revision.

## Entrenchment

```python
from belief_set import Atom, BeliefSet, EpistemicEntrenchment, SpohnEpistemicState, negate

p = Atom("p")
state = SpohnEpistemicState.from_belief_set(BeliefSet.from_formula(frozenset({"p"}), p))
entrenchment = EpistemicEntrenchment.from_state(state)

assert entrenchment.leq(negate(p), p)
```

Entrenchment comparisons are induced by the rank of countermodels in the
underlying Spohn state.

## IC Merge

```python
from belief_set import Atom, ICMergeOperator, conjunction, merge_belief_profile

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
`ICMergeOutcome.scored_worlds` uses a uniform tuple score representation for
both operators.

## Bounded Enumeration

```python
import pytest

from belief_set import AlphabetBudgetExceeded, Atom, BeliefSet, SpohnEpistemicState, revise

state = SpohnEpistemicState.from_belief_set(BeliefSet.tautology(frozenset({"p"})))

with pytest.raises(AlphabetBudgetExceeded):
    revise(state, Atom("q"), max_alphabet_size=1)
```

`AlphabetBudgetExceeded` is a hard precondition failure for public operators.
`EnumerationExceeded` is reserved for interrupted anytime-style private
distance scans.

## Correctness Coverage

The test suite contains focused and property-based checks grounded in the
processed paper notes under `papers/`:

- Spohn OCF invariants: no `NaN` ranks, read-only normalized rank maps,
  contradiction as all-infinite ranks.
- AGM revision and contraction: success, extensionality, Harper contraction,
  and aligned belief-set/state alphabets.
- Gardenfors-Makinson entrenchment checks over generated small formulas.
- Booth-Meyer restrained revision and lexicographic iterated revision checks.
- Konieczny-Pino Perez IC merging checks, including sigma/gmax behavior,
  empty-profile semantics, and score-shape normalization.

## Development

```powershell
uv sync
uv run pytest
uv run pytest -m property
uv run pyright
```

The property tests intentionally use small alphabets because world enumeration
is exponential.

## Non-Goals

This package deliberately does not own:

- caller-owned provenance graphs or witness objects
- source, context, claim, stance, sidecar, storage, worldline, repository, or
  CLI behavior
- argumentation-framework revision adapters
- compatibility imports for older owner-specific module paths
- scalable SAT/SMT-backed reasoning

## Paper Assets

Processed paper notes and metadata belong in `papers/` when they specify
package-owned formal algorithms. Source PDFs and rendered page PNGs may be
present in a local working tree for paper reading, but they are intentionally
ignored by Git and are not tracked package artifacts.
