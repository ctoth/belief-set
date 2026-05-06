---
title: "New operators for theory change"
authors: ["Sven Ove Hansson"]
year: 1989
venue: "Theoria"
doi_url: "https://doi.org/10.1111/j.1755-2567.1989.tb00725.x"
pages: "114-132"
---

# New operators for theory change

## One-Sentence Summary
Hansson argues that AGM contraction and revision over closed theories are too narrow for many epistemic and normative changes, then defines generalized set-contraction operators and new minimal-contraction operators that preserve useful non-closed information. *(pp.114-132)*

## Problem Addressed
AGM-style theory change assumes changes to deductively closed theories by a single sentence, but Hansson argues this loses important distinctions between different bases with the same closure and cannot represent changes by sets of propositions. The paper targets belief systems, norm systems, and descriptive models where source-level expressions matter independently of their logical closure. *(pp.114-119)*

## Key Contributions
- Shows why revision/contraction of closed theories cannot distinguish bases such as `{a, a v b}` and `{a}` when revising by `not a`, even though the first should retain `a v b`. *(pp.117-118)*
- Generalizes contraction from single sentences to sets of expressions and from closed theories to arbitrary sets of expressions. *(pp.119-123)*
- Defines simple full meet, simple partial meet, composite full meet, and composite partial meet contractions for set contraction. *(pp.120-123)*
- Extends Gardenfors' six contraction postulates to contractions by sets and proves a representation theorem for finite contractions of theories. *(pp.122-124, 127-130)*
- Introduces full minimal contraction and partial minimal contraction to preserve disjunctive information from the original base without adding redundant disjunctions. *(pp.124-126)*

## Study Design

## Methodology
The paper is a formal theory-construction and representation-theorem paper. It first reviews AGM contraction, partial meet contraction, and safe contraction, then motivates a broader setting with examples from belief bases and norm systems. It defines a monotonic, idempotent consequence operation `Cn`, assumes compact classical propositional behavior, and develops contraction operators over arbitrary subsets of the language. *(pp.114-120)*

## Key Equations / Statistical Models

AGM Levi identity:

$$
A +' a = Cn((A \div \neg a) \cup \{a\})
$$

Revision can be defined by first contracting away the negation of the input and then expanding by the input. *(p.115)*

Full meet contraction for a single sentence:

$$
A \div x = \bigcap(A \perp x)
$$

`A perp x` is the set of inclusion-maximal subsets of `A` that do not imply `x`. *(p.115)*

Partial meet contraction:

$$
A \div x = \bigcap \gamma(A \perp x)
$$

The selection function `gamma` chooses some of the maximal non-`x`-implying subsets before intersection. *(pp.115-116)*

Generalized remainder sets:

$$
A \perp B = \{C \subseteq A : B \cap Cn(C) = \varnothing \text{ and no larger } C' \subseteq A \text{ avoids } B\}
$$

This generalizes remainder sets from avoiding one sentence to avoiding every non-tautological member of a set `B`. *(p.120)*

Simple full meet contraction:

$$
A \sim B = \bigcap(A \perp B)
$$

When `A perp B` is empty, Hansson defines the result as the empty set. *(p.121)*

Composite partial meet contraction:

$$
A \simeq_\gamma B = \bigcap \gamma(A \parallel B)
$$

`A parallel B` is the union of `A perp C` for subsets `C` of `B`; `gamma` must select a `B`-covering subfamily when such a covering exists. *(pp.121-122)*

Usefulness of exclusion:

$$
a \in A \text{ and } a \notin A \div B
$$

requires some `C subseteq A` such that adding `C` back remains compatible with avoiding `B`, but adding `a` with `C` reintroduces an element of `B`. This separates simple partial meet contraction from the broader composite class. *(pp.123-124)*

Minimal contraction setup:

$$
V_n A
$$

is the set of disjunctions of at most `n` distinct elements of `A`, and `VA = V_1A \cup V_2A \cup ...`. *(p.125)*

Full minimal contraction:

$$
D_n = (V_n A) \sim B,\quad E_1 = D_1,\quad E_{n+1} = E_n \cup (D_{n+1} \setminus Cn(E_n))
$$

`A - B` is the union of the `E_n` sequence, preserving as much original and useful disjunctive material as possible while avoiding redundant disjunctions. *(p.125)*

Partial minimal contraction:

$$
D_n = (V_n A) \sim_\gamma B,\quad E_1 = D_1,\quad E_{n+1} = E_n \cup (D_{n+1} \setminus Cn(E_n))
$$

This inserts selection-function priorities into the minimal-contraction construction. *(p.126)*

## Parameters

| Name | Symbol | Units | Default | Range | Page | Notes |
|------|--------|-------|---------|-------|------|-------|
| Language | `L` | - | all expressions under consideration | arbitrary propositional language | 119 | Operators are defined over `P(L) x P(L)`. |
| Consequence operation | `Cn` | - | inclusion, iteration, monotony | includes classical propositional logic, deduction, compactness | 119 | Used to define consistency, theories, and implication by bases. |
| Theory | `A = Cn(A)` | - | deductively closed set | subset of `L` | 120 | AGM theory-change operators are a special case. |
| Set contraction input | `B` | - | set of expressions to avoid | any subset of `L` | 120 | Allows multi-sentence contraction. |
| Remainder family | `A perp B` | - | maximal subsets of `A` avoiding `B` | empty or nonempty family | 120 | Basis for simple meet contraction. |
| Composite family | `A parallel B` | - | union of `A perp C` for `C subseteq B` | must be checked for covering | 121 | Basis for composite meet contraction. |
| Selection function | `gamma` | - | chosen subfamily of remainders | nonempty when input family nonempty | 116, 121 | Encodes priority among alternative contractions. |
| Disjunction expansion | `V_n A` | - | disjunctions of at most `n` members of `A` | `n >= 1` | 125 | Used by minimal contraction to preserve base-level disjunctions. |
| Priority relation | `<` | - | safe-contraction ordering | strict relation over base elements | 116, 126 | Compared with selection functions in worked examples. |

## Effect Sizes / Key Quantitative Results

## Methods & Implementation Details
- Closure hides representation-relevant structure: the bases `{a, a v b}` and `{a}` have the same closure, but after new information `not a` the first can reasonably retain `a v b` and infer `b`, while the second cannot. *(pp.117-118)*
- Norm systems have the same issue: if norm `n2` is entailed by `n1` but also independently grounded, retracting `n1` should not force retraction of `n2`. *(p.118)*
- Set inputs are not reducible to conjunctions: adding `{a,b}` to the empty set differs from adding `a & b`, and contracting `{b,c}` differs from contracting `b & c`. *(pp.118-119)*
- Iterating single-sentence changes is order-dependent; adding `{a, not a}` one element at a time can leave either `a` or `not a` depending on order. *(p.119)*
- Definition 3.5 constrains contraction output: if `A = B div C`, then `Cn(A) subseteq Cn(B)` and `Cn(A) cap C subseteq Cn(empty)`. *(p.120)*
- Theorem 3.10: every simple partial meet contraction is a composite partial meet contraction, but not every composite partial meet contraction is simple. *(p.122)*
- Theorem 3.12: finite contractions of theories satisfy the extended Gardenfors postulates EG1-EG6 iff they are composite partial meet contractions. *(pp.123, 127-130)*
- Theorem 3.14: finite theory contractions satisfying EG1-EG6 plus usefulness of exclusion are exactly the simple partial meet contractions. *(pp.123-124, 130-131)*
- Full and partial minimal contraction satisfy five of six extended Gardenfors postulates, but replace inclusion EG2 with logical inclusion `Cn(A - B) subseteq Cn(A)`. *(p.126)*
- In the comparison example contracting `{x, y, z}` by `x & y & z`, different operators produce different retained information: full meet gives empty, full minimal keeps pairwise disjunctions, partial meet and safe contraction keep `{x}`, and partial minimal keeps `{x, y v z}`. *(p.126)*

## Figures of Interest
No figures.

## Results Summary
Hansson broadens theory change from AGM's closed-theory, single-sentence operators to a family of operators over arbitrary expression sets and set-valued change inputs. The meet-style generalizations recover AGM-like postulates for finite contractions of theories, while minimal contraction is designed for belief bases because it can retain useful disjunctive information from the original base without collapsing everything to closure. *(pp.119-126)*

## Limitations
- Full and partial minimal contraction fail ordinary inclusion EG2/G2; they only guarantee logical inclusion. *(p.126)*
- The minimal-contraction construction can introduce disjunctions not explicitly present in the original base, though it is designed to avoid redundant disjunctions where possible. *(p.125)*
- The representation theorems are stated for finite contractions of theories, so direct implementation over arbitrary infinite bases needs an explicit finitary representation strategy. *(pp.123-124)*
- The paper introduces diversity of operators rather than a single mandated choice; selecting an operator is application-dependent. *(p.127)*

## Arguments Against Prior Work
- AGM's closed-theory setting cannot preserve distinctions between different belief bases with the same closure. *(pp.117-118)*
- Restricting change to one proposition is too narrow because changes by sets are not reducible to conjunctions or order-insensitive iteration. *(pp.118-119)*
- Meet contractions are not fully suitable for non-closed bases because they can throw away useful disjunctive information. *(p.124)*
- Consequence-extended meet contraction, applying meet contraction to `Cn(A)`, can produce too much material for base-level contraction and can introduce inappropriate tautological closure effects. *(p.124)*

## Design Rationale
- Model belief sets, norm systems, and factual models uniformly as sets of expressions rather than only closed theories. *(pp.114, 117-119)*
- Keep `Cn` explicit so implementations can distinguish stored base items from derived closure. *(pp.119-120)*
- Use selection functions when priorities among alternative contractions matter, matching the role selection functions already play in partial meet contraction. *(pp.116, 121-122, 126)*
- Use minimal contraction when the implementation must preserve non-closed source information such as disjunctions supported by the original base. *(pp.124-126)*

## Testable Properties
- A set contraction result must not imply any non-tautological member of the contracted-away set. *(p.120)*
- A simple partial meet contraction must be the intersection of a selected nonempty subfamily of `A perp B` when remainders exist. *(p.121)*
- A composite partial meet contraction must select from `A parallel B` and satisfy the `B`-covering condition when such covering is possible. *(pp.121-122)*
- Finite theory contractions satisfying EG1-EG6 should be representable as composite partial meet contractions. *(pp.123, 127-130)*
- Adding usefulness of exclusion should force the contraction into the simple partial meet subclass. *(pp.123-124, 130-131)*
- Minimal contraction should satisfy EG1, EG3, EG4, EG5, EG6 and logical inclusion, but not ordinary inclusion. *(p.126)*

## Relevance to Project
This paper is the strongest support in the collection for treating `belief-set` as a belief-base system rather than only as a closed AGM theory system. It recommends keeping explicit base expressions, derived closure, and contraction/revision policy separate, with full AGM available as a theory-level specialization and Hansson-style base contraction available when source representation matters.

## Open Questions
- [ ] Should `belief-set` expose set-valued contraction inputs directly instead of encoding them as conjunctions?
- [ ] Should the implementation include a minimal-contraction policy for preserving base-level disjunctions, or reserve that for a later belief-base layer?
- [ ] What finite representation of `Cn` and `V_n A` is tractable enough for practical minimal contraction?
- [ ] How should usefulness of exclusion be tested for finite bases and selected consequence fragments?

## Related Work Worth Reading
- Alchourron, Gardenfors, and Makinson 1985, "On the Logic of Theory Change: Partial Meet Contraction and Revision Functions" - baseline AGM contraction and revision framework. *(pp.115, 131)*
- Alchourron and Makinson 1985, "On the Logic of Theory Change: Safe Contraction" - source of safe contraction and priority relations. *(pp.116, 131)*
- Gardenfors 1988, *Knowledge in Flux* - broader theory-change framework and Gardenfors postulates. *(pp.122-123, 131-132)*
- Segerberg 1986, "On the Logic of Small Changes in Theories I/II" - small-change logic related to Hansson's generalized operators. *(pp.118, 132)*

## Collection Cross-References

### Already in Collection
- [On the logic of theory change: Partial meet contraction and revision functions](../Alchourron_1985_TheoryChange/notes.md) - provides the AGM partial-meet framework that Hansson generalizes. *(pp.115, 131)*
- [Revisions of Knowledge Systems Using Epistemic Entrenchment](../Gärdenfors_1988_RevisionsKnowledgeSystemsEpistemic/notes.md) - shares the Gardenfors postulate background and the concern with rational theory change. *(pp.122-123, 131-132)*

### New Leads (Not Yet in Collection)
- Alchourron and Makinson (1981) - "Hierarchies of Regulations and Their Logic" - relevant for the norm-system examples and legal/normative contraction setting. *(p.131)*
- Alchourron and Makinson (1985) - "On the Logic of Theory Change: Safe Contraction" - directly needed for safe-contraction details and priority relations. *(pp.116, 131)*
- Alchourron and Makinson (1986) - "Maps Between Some Different Kinds of Contraction Function: The Finite Case" - likely relevant for finite implementation mappings. *(p.131)*
- Segerberg (1986) - "On the Logic of Small Changes in Theories I" and "II" - related to small-change operators. *(pp.118, 132)*
- Makinson (1987) - "On the Status of the Postulate of Recovery in the Logic of Theory Change" - relevant to recovery and its limits. *(p.132)*

### Supersedes or Recontextualizes
- Hansson does not replace AGM for closed theories; it recontextualizes AGM as a special case and argues that belief-base and set-input changes need additional operators. *(pp.117-126)*

### Cited By (in Collection)
- No already-read collection paper was verified as citing Hansson 1989 during this pass.

### Conceptual Links (not citation-based)
- [Two modellings for theory change](../Grove_1988_TwoModellingsTheoryChange/notes.md) - Grove supplies semantic models for AGM revision, while Hansson explains why implementations over belief bases need richer operators than closed-theory AGM alone.
- [Ordinal Conditional Functions: A Dynamic Theory of Epistemic States](../Spohn_1988_OrdinalConditionalFunctionsDynamic/notes.md) - Spohn gives ranked epistemic states for iterated belief change; Hansson gives base-sensitive contraction operators for non-closed representations.
- [Merging Information Under Constraints: A Logical Framework](../Konieczny_2002_MergingInformationUnderConstraints/notes.md) - both broaden AGM-style postulate-and-representation methods beyond single closed theories, though Konieczny and Pino Perez focus on multi-source merging.
