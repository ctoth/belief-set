# belief_set

`belief_set` is a small pure-Python package for finite propositional
belief-revision kernels. It provides the model-theoretic pieces needed for
AGM revision and contraction, Spohn ranking states, iterated revision,
epistemic entrenchment, and IC belief merging.

The package is intentionally finite-world and explicit. Given an alphabet of
`n` atoms, many operations enumerate up to `2^n` worlds. Treat alphabet size as
the main cost driver and pass `max_alphabet_size` when accepting caller-owned
formulas.

Status: experimental `0.1.0`, Python `>=3.11`, no declared license yet.

## Install

Install the distribution package from a pushed Git commit or tag:

```powershell
uv add "formal-belief-set @ git+https://github.com/ctoth/belief-set@<commit>"
```

Do not pin downstream projects to a local checkout, local path, or editable
local repository URL.

For local development:

```powershell
uv sync
uv run pytest
uv run pyright
```

## Quick Start

```python
from belief_set import Atom, BeliefSet, SpohnEpistemicState, conjunction, negate, revise

p = Atom("p")
q = Atom("q")

initial = BeliefSet.from_formula(
    frozenset({"p", "q"}),
    conjunction(p, negate(q)),
)
state = SpohnEpistemicState.from_belief_set(initial)

outcome = revise(state, q)

assert outcome.belief_set.entails(q)
assert outcome.state.belief_set.equivalent(outcome.belief_set)
assert outcome.trace.operator == "revise"
```

The central representation is extensional: a `BeliefSet` stores an alphabet
and the finite set of worlds that satisfy the theory. Its `cn()` method returns
the object itself because the deductive closure is already represented by those
models over the declared alphabet.

## Mental Model

- A world is a `frozenset[str]` containing exactly the atoms true in that world.
- A formula is any object implementing `evaluate(world)` and `atoms()`.
- `Atom`, `TOP`, `BOTTOM`, `negate`, `conjunction`, and `disjunction` provide a
  minimal formula language.
- Belief sets are compared extensionally after their alphabets are aligned.
- Revision operators return outcomes, not bare belief sets, so callers can keep
  the revised belief set, revised Spohn state, and trace metadata together.
- Contradictory belief sets are preserved as contradictions; they are not
  converted into tautologies.

## Public API

The package root exports the supported public surface:

```python
from belief_set import (
    AlphabetBudgetExceeded,
    Atom,
    BOTTOM,
    BeliefSet,
    EnumerationExceeded,
    EpistemicEntrenchment,
    Formula,
    ICMergeOperator,
    ICMergeOutcome,
    ICMergeProfileMemberInconsistent,
    RevisionOutcome,
    RevisionTrace,
    SpohnEpistemicState,
    TOP,
    World,
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

- `belief_set.language`: formula protocol, atoms, constants, boolean
  connectives, and equivalence checks.
- `belief_set.core`: extensional finite belief sets and model-alignment
  helpers.
- `belief_set.agm`: Spohn epistemic states, AGM-style revision, full-meet
  contraction, and revision traces.
- `belief_set.iterated`: lexicographic and restrained iterated revision.
- `belief_set.entrenchment`: entrenchment comparisons induced by a Spohn state.
- `belief_set.ic_merge`: finite IC merging with sigma and gmax aggregation.
- `belief_set.anytime`: bounded-enumeration failure types.

## Belief Sets

```python
from belief_set import Atom, BeliefSet, conjunction, negate, theory_subset

p = Atom("p")
q = Atom("q")
beliefs = BeliefSet.from_formula(frozenset({"p", "q"}), conjunction(p, q))
weaker = BeliefSet.from_formula(frozenset({"p", "q"}), p)

assert beliefs.is_consistent
assert beliefs.entails(p)
assert not beliefs.entails(negate(p))
assert theory_subset(beliefs, weaker)
```

`BeliefSet.from_formula()` automatically extends the declared alphabet with
any atoms mentioned by the formula. `with_alphabet()` extends an existing
belief set to a larger signature while preserving its old constraints.

## Revision And Contraction

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

`revise()` implements Darwiche-Pearl bullet revision over a finite Spohn
ranking. `full_meet_contract()` uses the Harper identity over the finite
theory. Both return `RevisionOutcome`.

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

Lexicographic revision orders all formula worlds before all non-formula worlds
while preserving the old rank order inside those groups. Restrained revision
promotes the old minimal formula worlds and then preserves old strict order,
splitting same-rank ties in favor of formula worlds.

## Entrenchment

```python
from belief_set import Atom, BeliefSet, EpistemicEntrenchment, SpohnEpistemicState, negate

p = Atom("p")
state = SpohnEpistemicState.from_belief_set(
    BeliefSet.from_formula(frozenset({"p"}), p),
)
entrenchment = EpistemicEntrenchment.from_state(state)

assert entrenchment.leq(negate(p), p)
```

`EpistemicEntrenchment.leq(left, right)` returns whether `left` is no more
entrenched than `right`, using the minimum rank of countermodels in the
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
assert outcome.scored_worlds[0][1] == (0.0,)
```

`merge_belief_profile()` evaluates candidate worlds satisfying the integrity
constraint `mu`, scores them by distance to the profile, and returns the
best-scoring worlds as a belief set. `ICMergeOperator.SIGMA` sums distances.
`ICMergeOperator.GMAX` compares sorted distance vectors lexicographically.
Unsatisfiable profile members raise `ICMergeProfileMemberInconsistent`.

## Bounded Enumeration

```python
import pytest

from belief_set import AlphabetBudgetExceeded, Atom, BeliefSet, SpohnEpistemicState, revise

state = SpohnEpistemicState.from_belief_set(BeliefSet.tautology(frozenset({"p"})))

with pytest.raises(AlphabetBudgetExceeded):
    revise(state, Atom("q"), max_alphabet_size=1)
```

Public operators call the alphabet guard before enumerating worlds.
`AlphabetBudgetExceeded` means the requested signature is larger than the
configured budget. `EnumerationExceeded` is reserved for interrupted
anytime-style distance scans and is not used as an approximation result by the
public merge operator.

## Correctness Coverage

The test suite contains focused and property-based checks grounded in the
processed paper notes under `papers/`:

- Spohn OCF invariants: no `NaN` ranks, read-only normalized rank maps, and
  contradiction represented by all-infinite ranks.
- AGM revision and contraction: success, extensionality, Harper contraction,
  and aligned belief-set/state alphabets.
- Gardenfors-Makinson entrenchment checks over generated small formulas.
- Booth-Meyer restrained revision and Nayak-Spohn lexicographic revision.
- Konieczny-Pino Perez IC merging checks, including sigma/gmax behavior,
  empty-profile semantics, inconsistent profile-member handling, and uniform
  score shapes.

Run the full suite with:

```powershell
uv run pytest
```

Property tests use small alphabets because world enumeration is exponential:

```powershell
uv run pytest -m property
```

## Non-Goals

This package deliberately does not own:

- caller-owned provenance graphs or witness objects
- source, context, claim, stance, sidecar, storage, worldline, repository, CLI,
  or presentation behavior
- argumentation-framework revision adapters
- compatibility imports for older owner-specific module paths
- scalable SAT/SMT-backed reasoning

See [docs/architecture.md](docs/architecture.md) for the runtime boundary.

## Paper Assets

Processed paper notes and metadata belong in `papers/` when they specify
package-owned formal algorithms. Source PDFs and rendered page PNGs may be
present in a local working tree for paper reading, but they are intentionally
ignored by Git and are not tracked package artifacts.
