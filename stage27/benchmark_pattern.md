# Stage 27 — Semantic Benchmark Pattern

## Purpose

Stage 26 demonstrated one substantive cross-inventory semantic case. Stage 27 generalizes that case into a reusable benchmark pattern without introducing new semantic claims.

The benchmark evaluates whether the semantic core can:

1. retrieve source-grounded claims from multiple inventories;
2. preserve layer and epistemic status;
3. compare meanings without collapsing them into identity;
4. block unsupported transfer of proof across layers;
5. distinguish established correspondence from unresolved equivalence;
6. produce an explicit result when the comparison is partial.

## Canonical Case Schema

A semantic benchmark case consists of:

- `case_id`
- `question`
- `inventories`
- `source_bindings`
- `comparison_axes`
- `forbidden_inferences`
- `expected_result`
- `validation_requirements`

## Comparison Axes

| Axis | Question |
|---|---|
| lexical identity | Is the same term used? |
| semantic role | What does the term/operator do in its layer? |
| process position | Where does it occur in the process structure? |
| formalization | What formal representation is actually registered? |
| epistemic status | Is the statement SOURCE, hypothesis, model-specific, etc.? |
| cross-layer relation | Is the relation identity, correspondence, mapping, specialization, or unresolved? |

## Result Vocabulary

```text
SAME_CONTENT
EQUIVALENT_FORMULATION
STRUCTURAL_CORRESPONDENCE
PARTIAL
UNRESOLVED
PROHIBITED_INFERENCE
```

These are result classes, not semantic identities to be inserted into the corpus automatically.

## Anti-collapse Rule

A benchmark MUST NOT infer identity merely because:

- the same lexical label occurs;
- two descriptions share a processual pattern;
- formal expressions look similar;
- one layer provides a physical interpretation of another;
- two operators occur in analogous positions.

## Dissipation Benchmark

Stage 26 is retained as the reference implementation:

```text
A: structural closure → mandatory dissipation
B: diff → fix → diss → unfold; diss releases carrier dependence
C: redistribution into degrees of freedom; orthogonal dissipation is layer-canonical
```

Expected cross-inventory result:

```text
PARTIAL
```

Identity and mathematical isomorphism remain unestablished.

## Benchmark Contract

A future case can be admitted only when its expected result can be stated without silently changing source status.

> **Compare registered meanings; do not manufacture a shared meaning merely to make the comparison complete.**
