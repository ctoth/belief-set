---
title: "Two modellings for theory change"
authors: ["Adam J. Grove"]
year: 1988
venue: "Journal of Philosophical Logic"
doi_url: "https://doi.org/10.1007/BF00247909"
pages: "157-170"
---

# Two modellings for theory change

## One-Sentence Summary
Grove gives representation theorems showing that AGM-style revision can be modeled either by systems of spheres over maximal consistent extensions or by orderings over sentences, and then relates those models back to partial-meet contraction. *(pp.157-170)*

## Problem Addressed
Gardenfors' postulates for theory change need concrete semantic models that are plausible and natural, not just abstract representation results. Grove says the Alchourron-Gardenfors-Makinson representation is useful but not entirely satisfactory because, following Segerberg, we still need models that explain all and only the revision functions satisfying the postulates. *(p.157)*

## Key Contributions
- Defines systems of spheres centered on arbitrary sets of maximal consistent extensions, rather than only on single worlds as in Lewis' counterfactual semantics. *(pp.158-160)*
- Proves that every sphere system centered on `|T|` generates a revision function satisfying Gardenfors' postulates `(+2)` through `(+8)`. *(pp.161-162)*
- Proves the converse: every revision function satisfying `(+2)` through `(+8)` can be represented by a sphere system centered on `|T|`. *(pp.162-163)*
- Defines an alternative sentence-ordering model and proves its equivalence to the sphere model for revision. *(pp.163-167)*
- Shows the duality between sphere/order semantics for revision and the AGM partial-meet contraction representation. *(pp.167-170)*

## Study Design

## Methodology
The paper is a formal representation-theorem paper. It starts from a compact propositional logic with Boolean connectives and modus ponens closure, defines theories as deductively closed sets between the logical theses `L` and the full language `F`, represents theories by sets of maximal consistent extensions, then gives semantic constructions whose induced revision operators satisfy the Gardenfors postulates. *(pp.157-158)*

## Key Equations / Statistical Models

AGM-style revision postulates retained from Gardenfors:

$$
A \in T + A
$$

This is postulate `(+2)`: successful revision accepts the input sentence. *(p.158)*

$$
T + A = T / A \quad \text{if } \neg A \notin T
$$

This is postulate `(+3)`: if the input is consistent with the current theory, revision is expansion. *(p.158)*

$$
T + A \text{ is consistent, if } \neg A \notin L
$$

This is postulate `(+4)`: revision by a logically consistent sentence yields a consistent theory. *(p.158)*

$$
T + A = T + B \quad \text{if } A \leftrightarrow B \in L
$$

This is postulate `(+5)`: logically equivalent inputs produce the same revision. *(p.158)*

$$
T + A \wedge B \subseteq (T + A) / B
$$

This is postulate `(+7)`, one side of conjunctive revision coherence. *(p.158)*

$$
(T + A) / B \subseteq T + A \wedge B \quad \text{if } \neg B \notin T + A
$$

This is postulate `(+8)`, the converse conjunctive coherence condition under consistency. *(p.158)*

Theory-to-model-set and model-set-to-theory maps:

$$
|T| = \{m \in M_L : T \subseteq m\}
$$

`M_L` is the set of all maximal consistent extensions of `L`; `|T|` is empty when `T` is inconsistent. *(p.158)*

$$
t(S) = \bigcap\{x : x \in S\}
$$

For `S subseteq M_L`, `t(S)` is the theory true in every member of `S`; if `S` is empty, `t(S)` is the inconsistent theory `F`. *(p.158)*

Sphere-derived revision:

$$
T + A = t(f_S(A))
$$

`S` is a system of spheres centered on `|T|`; `f_S(A) = |A| \cap c(A)` selects the closest `A`-worlds in the smallest sphere intersecting `|A|`. *(pp.159-161)*

Sphere-to-order relation:

$$
A \le_S B \quad \text{iff} \quad c(A) \subseteq c(B)
$$

Strict order is `A <_S B` when `c(A)` is properly contained in `c(B)`. This sentence ordering can define revision directly. *(p.164)*

Sentence-ordering revision:

$$
T + A = \{B \in F : (A \wedge B) < (A \wedge \neg B)\}
$$

Read as: after accepting `A`, include `B` exactly when `B` in the presence of `A` is better, more possible, or more entrenched than `not B` in the presence of `A`. *(pp.164-167)*

Partial-meet contraction from AGM:

$$
T - A = \bigcap\{t : t \in g(M(T,A))\}
$$

`M(T,A)` is the family of maximal subsets of `T` that do not imply `A`; `g` is a selection function over such families. *(p.168)*

## Parameters

| Name | Symbol | Units | Default | Range | Page | Notes |
|------|--------|-------|---------|-------|------|-------|
| Logical theses | `L` | - | compact propositional logic closed under modus ponens | includes Boolean connectives | 157 | Base logic used for all theories. |
| Sentences | `F` | - | all sentences in the language | - | 157 | A theory is any `T` such that `L subseteq T subseteq F`. |
| Maximal consistent extensions | `M_L` | - | all maximal consistent extensions of `L` | - | 158 | Semantic worlds for both sphere and ordering models. |
| Current theory model set | `|T|` | - | `{m in M_L : T subseteq m}` | empty if `T` inconsistent | 158 | Center of the sphere system for revision of `T`. |
| Theory induced by worlds | `t(S)` | - | intersection of all worlds in `S` | `F` if `S` empty | 158 | Converts selected worlds back to a theory. |
| Smallest `A`-intersecting sphere | `c(A)` | - | smallest sphere intersecting `|A|` | `M_L` if no sphere intersects `|A|` | 159 | Exists by sphere condition S4. |
| Selection from a sphere system | `f_S(A)` | - | `|A| cap c(A)` | empty if `|A|` empty | 159 | Selects closest `A` worlds. |
| Sentence-order relation | `<=` | - | connected, transitive relation on `F` | constrained by conditions `<=1` to `<=5` | 163 | Alternative representation for revision. |
| Partial meet selector | `g` | - | selection from `M(T,A)` | `g(M(T,A)) subseteq M(T,A)` | 168 | AGM contraction selector related to sphere semantics. |

## Effect Sizes / Key Quantitative Results

## Methods & Implementation Details
- A system of spheres `S` centered on `X subseteq M_L` must be totally ordered by subset inclusion, have `X` as its minimum, include `M_L` as largest element, and have a smallest sphere intersecting any nonempty proposition `|A|`. *(p.159)*
- Grove's sphere model differs from Lewis' counterfactual spheres by centering spheres on arbitrary subsets of `M_L`, not individual worlds; this is necessary because theories correspond to sets of worlds. *(p.159)*
- The relational version of a sphere system uses a connected, transitive relation on worlds plus the condition that the `<=`-minimal worlds are exactly the current center `X`. *(p.160)*
- Condition S4, the existence of a smallest sphere intersecting a proposition, is difficult to justify intuitively but essential for the representation theorem. *(pp.160-161)*
- Theorem 1 proves soundness of the sphere construction against postulates `(+2)` to `(+8)`, with proof cases for success, expansion under consistency, consistency preservation, equivalence invariance, and the two conjunctive postulates. *(pp.161-162)*
- Theorem 2 proves completeness: any revision function satisfying `(+2)` to `(+8)` determines a sphere system, though the representing system is not unique. *(pp.162-163)*
- The alternative ordering model requires connectedness, transitivity, a disjunctive condition `A -> B v C in L` implies `B <= A` or `C <= A`, minimality exactly for negations already in `T`, and maximality exactly for logically consistent sentences. *(p.163)*
- Theorems 3 and 4 establish equivalence between the sentence-ordering model and the sphere model, using cuts and co-spheres to build the equivalent sphere system. *(pp.164-167)*
- In the conclusion, maxichoice contraction corresponds to the finest possible spheres, full meet contraction to the coarsest possible two-sphere system, and partial meet contraction to intermediate sphere systems. *(p.168)*
- The apparent forms are dual: sphere semantics emphasize subsets of `M_L`, whereas AGM's partial-meet construction emphasizes actual theories/subsets of `T`. *(pp.169-170)*

## Figures of Interest
No figures.

## Results Summary
The paper establishes two equivalent semantic characterizations of theory revision satisfying the Gardenfors postulates. Systems of spheres around `|T|` give a closest-world semantics for revision, and sentence orderings give a relative-importance semantics in which a proposition survives revision by `A` when `A and B` is better than `A and not B`. Both constructions are tied back to AGM partial-meet contraction by showing that maxichoice, full meet, and partial meet contractions correspond to progressively coarser or intermediate sphere systems. *(pp.161-170)*

## Limitations
- The sphere representation is not unique: multiple sphere systems may generate the same addition/revision function. *(p.163)*
- There need not be any relation between the sphere systems centered on different theories `T` and `T'`, so the representation is pointwise in the current theory unless extra constraints are added. *(p.163)*
- Gardenfors' monotonicity condition for addition is not necessarily satisfied by arbitrary AGM revision functions, and Gardenfors showed monotonicity is incompatible with `(+2)` through `(+8)`. *(p.163)*
- Condition S4 is acknowledged as troublesome from the intended interpretation, though it is formally necessary for the sphere representation. *(pp.160-161)*

## Arguments Against Prior Work
- The AGM/AGM-style representation of Alchourron, Gardenfors, and Makinson is not by itself a sufficiently natural model of revision; Grove wants concrete semantic constructions that make the postulates intelligible. *(p.157)*
- Lewis' single-world-centered spheres are inappropriate for theory change because a theory corresponds to a set of possible worlds, not one world. *(p.159)*
- Maxichoice contraction and full meet contraction are both described as unsatisfactory extremes; partial meet contraction is the intermediate case corresponding to richer sphere systems. *(p.168)*

## Design Rationale
- Use maximal consistent extensions as worlds because they make each theory correspond to a set of possible states compatible with current belief. *(pp.158-160)*
- Center spheres on `|T|` because revision of a theory should be governed by worlds most compatible with the current theory. *(pp.159-160)*
- Introduce sentence orderings because they are arguably more appealing than spheres for implementation: `T + A` can be decided by comparing `A and B` against `A and not B`. *(pp.163-167)*
- Preserve S4 despite interpretive discomfort because it guarantees a smallest best `A`-region and is essential to the representation theorem. *(pp.160-161)*

## Testable Properties
- A sphere representation for revision must include `M_L` as the largest sphere and the current model set `|T|` as the smallest sphere. *(p.159)*
- For every satisfiable input `A`, `c(A)` must be the smallest sphere intersecting `|A|`. *(p.159)*
- A sphere-derived operator must satisfy postulates `(+2)` through `(+8)`. *(pp.161-162)*
- For every operator satisfying `(+2)` through `(+8)` and fixed theory `T`, there must exist at least one representing sphere system centered on `|T|`. *(pp.162-163)*
- A sentence-order representation must satisfy connectedness and transitivity, and must make `A` minimal iff `not A in T` and maximal iff `not A` is logically inconsistent. *(p.163)*
- Sentence-order revision includes `B` in `T + A` iff `(A and B) < (A and not B)`. *(pp.164-167)*

## Relevance to Project
This is the canonical semantic bridge for implementing AGM revision over finite model sets or rankings in `belief-set`. It supports a target architecture with explicit possible-world/model-set semantics, a sphere or preorder state object, and revision as selection of minimal `A` worlds followed by deductive closure. It also clarifies how partial-meet contraction can be treated as the contraction-side dual of sphere-based revision.

## Open Questions
- [ ] Which finite representation should `belief-set` expose first: sphere layers, total preorders over valuations, or sentence-order comparisons?
- [ ] Should the implementation preserve the pointwise nature of Grove's theorem, or add iterated-revision constraints tying sphere systems for different theories together?
- [ ] How should S4 be enforced for finite inconsistent or unsatisfiable inputs?

## Related Work Worth Reading
- Alchourron, Gardenfors, and Makinson 1985, "On the logic of theory change: Partial meet contraction and revision functions" - source of partial-meet contraction and the representation Grove relates to spheres. *(p.170)*
- Lewis 1973, "Counterfactuals" - source of sphere semantics adapted here from counterfactual logic to theory change. *(pp.159, 170)*
- Gardenfors 1986, "Belief revisions and the Ramsey test for conditionals" - discusses monotonicity and conditionals in the theory-change setting. *(pp.163, 170)*
- Segerberg, "On the logic of small changes to theories I" - cited as motivating the need for plausible and natural models. *(pp.157, 170)*

## Collection Cross-References

### Already in Collection
- [On the logic of theory change: Partial meet contraction and revision functions](../Alchourron_1985_TheoryChange/notes.md) - cited as the AGM/partial-meet representation theorem that Grove reinterprets through systems of spheres. *(p.170)*

### New Leads (Not Yet in Collection)
- Lewis (1973) - *Counterfactuals* - source of sphere semantics; useful for validating the formal lineage of Grove's closest-world construction. *(pp.159, 170)*
- Gardenfors (1986) - "Belief revisions and the Ramsey test for conditionals" - relevant for the monotonicity condition Grove discusses. *(pp.163, 170)*
- Segerberg (forthcoming at the time) - "On the logic of small changes to theories I" - cited as the motivation for requiring natural models of small theory changes. *(pp.157, 170)*

### Supersedes or Recontextualizes
- Grove does not supersede AGM 1985; it recontextualizes AGM partial-meet contraction by showing how maxichoice, full meet, and partial meet contraction correspond to fine, coarse, and intermediate systems of spheres. *(pp.167-170)*

### Cited By (in Collection)
- [Revisions of Knowledge Systems Using Epistemic Entrenchment](../Gärdenfors_1988_RevisionsKnowledgeSystemsEpistemic/notes.md) - cites Grove as an alternative formal model of theory change.
- [Admissible and Restrained Revision](../Booth_2006_AdmissibleRestrainedRevision/notes.md) - cites Grove in its iterated-revision literature background.

### Conceptual Links (not citation-based)
- [Ordinal Conditional Functions: A Dynamic Theory of Epistemic States](../Spohn_1988_OrdinalConditionalFunctionsDynamic/notes.md) - both provide ranked/similarity-style semantic structure beyond bare belief sets; Grove uses spheres over maximal consistent extensions, while Spohn uses ordinal disbelief grades for iterated epistemic states.
- [Merging Information Under Constraints: A Logical Framework](../Konieczny_2002_MergingInformationUnderConstraints/notes.md) - both are representation-theorem papers connecting rationality postulates to semantic constructions over interpretations; Grove covers single-agent revision, while Konieczny and Pino Perez generalize the style to multi-source merging under integrity constraints.
