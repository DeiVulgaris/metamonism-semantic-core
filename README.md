# Metamonism Semantic Core

**Machine-readable semantic core of Meta-Monism, derived from the source corpus and structured as a traceable semantic representation.**

---

## Purpose

This repository contains the **machine-readable semantic core of Meta-Monism**.

Its purpose is not to rewrite, improve, axiomatize, or reinterpret the theory, but to extract and formalize its existing semantic structure:

* entities
* claims
* relations
* formalizations
* identities
* ambiguities
* conflicts
* undefined terms
* historical formulations
* derivations

The central methodological principle is:

> **The architecture must be extracted from the corpus, not invented on top of it.**

The semantic layer preserves the distinction between what is explicitly present in the source corpus, what follows as an inference, what is merely a formalization, what remains unresolved, and what belongs to historical or theoretical formulations.

---

## Source Repositories

The semantic core is derived from the analysis of the following source repositories:

* **[Ontological-core-of-AGI](https://github.com/DeiVulgaris66/Ontological-core-of-AGI)** — ontological core and foundational concepts
* **[metamonism-analysis](https://github.com/DeiVulgaris66/metamonism-analysis)** — analytical reconstruction of Meta-Monism
* **[Wayward-Metamonism](https://github.com/DeiVulgaris66/Wayward-Metamonism)** — development and exploration of Meta-Monist concepts
* **[Metamonism](https://github.com/DeiVulgaris66/Metamonism)** — primary Meta-Monism corpus
* **[EECP](https://github.com/DeiVulgaris/EECP)** — Extended Evolutionary Causal Processing
* **[Universal-Framework-for-Complex-Problem-Solving](https://github.com/DeiVulgaris/Universal-Framework-for-Complex-Problem-Solving)** — UFCPS framework

These repositories constitute the source corpus from which the machine-readable semantic structures are extracted.

The present repository does not replace or rewrite the source material. It provides a structured semantic representation of it.

---

## Semantic Reconstruction Pipeline

The semantic extraction follows the pipeline:

```text
SOURCE
   ↓
SEMANTIC RECONSTRUCTION
   ↓
ATOMIC CLAIMS
   ↓
RELATION TO EXISTING
   ↓
TYPE
   ↓
STATUS
   ↓
FORMALIZATION
   ↓
CANONICAL NAME
   ↓
STABLE ID
   ↓
GRAPH
```

The ordering is deliberate:

> **First semantics → then type → then formalization → then identity.**

IDs are therefore not assigned before semantic identity has been established.

---

## Core Principles

### Source fidelity

The semantic layer does not silently:

* correct the author
* resolve theoretical contradictions
* remove inconvenient formulations
* replace terminology
* turn hypotheses into established facts
* turn analogies into isomorphisms
* turn physical models into fundamental ontology
* turn geometry into process
* turn process into object
* turn descriptions into proofs

Uncertainty and historical development are preserved explicitly.

### Entity, Claim, Relation

The semantic layer distinguishes three different levels:

**Entity** — a semantic object, process, operator, state, model, or other identifiable element.

**Claim** — an assertion about an entity or entities.

**Relation** — a typed connection between entities.

For example:

```text
Entity:
mm:core.op.diff

Claim:
diff produces distinction / non-identity

Relation:
diff → dissipate
```

This prevents properties of an entity from being confused with the entity itself.

---

## Status Taxonomy

The semantic layer uses explicit semantic status categories:

| Status                          | Meaning                                                              |
| ------------------------------- | -------------------------------------------------------------------- |
| `SOURCE`                        | Directly confirmed by the corpus                                     |
| `INFERENCE`                     | Follows from source material without a new fundamental assumption    |
| `FORMALIZATION`                 | Formal representation of existing semantic content                   |
| `THEORETICAL_HYPOTHESIS`        | Current theoretical hypothesis not yet established                   |
| `PROPOSAL`                      | New proposed construction                                            |
| `UNRESOLVED`                    | Cannot currently be established from the corpus                      |
| `CONFLICT`                      | Source-level conflict                                                |
| `USED_BUT_UNDEFINED`            | Used in the corpus but insufficiently defined                        |
| `PRIOR_THEORETICAL_FORMULATION` | Historical formulation superseded by the current working formulation |
| `MODEL_SPECIFIC`                | Specific to a particular model or hypothesis                         |

Origin and status are kept separate.

Possible origins include:

* `CORPUS`
* `PRIOR_THEORETICAL_FORMULATION`
* `JOINT_THEORETICAL_WORK`
* `AI_FORMALIZATION`
* `AI_RECONSTRUCTION`

Thus, a formalization can be AI-generated without becoming a source claim.

---

## Semantic Collapseability

Semantically similar terms are not automatically merged.

The central test is:

> **Can A be deleted and its full semantic content reconstructed from B without information loss?**

Possible relationships include:

```text
same_content
equivalent_formulation
formalization_of
specialization_of
generalization_of
consequence_of
distinct_principle
distinct_but_dependent
distinct_but_related
unresolved
```

This prevents semantic compression from destroying distinctions that may become important in later theoretical development.

---

# Repository Structure

The repository currently consists of **11 core files**.

### 1. `semantic_inventory.yaml`

**Status:** Complete

The inventory of the semantic entities extracted from the corpus.

Approximately **40 entities** are currently represented.

Entities include conceptual objects, processes, operators, states, models, and other semantically identifiable structures.

---

### 2. `claim_registry.yaml`

**Status:** Complete

Registry of atomic semantic claims.

Approximately **25 claims** are currently represented.

Claims are separated from the entities to which they refer, allowing individual assertions to carry their own status, origin, evidence, and formalization.

---

### 3. `relation_registry.yaml`

**Status:** Complete

Registry of typed semantic relations.

Currently contains approximately **20 relations**.

Relations are explicitly defined rather than inferred merely from graph structure.

Examples include:

```text
triggers
triggered_by
derives
derives_from
extends
maps_to
unfold
structurally_corresponds_to
isomorphic_to
```

Where appropriate, inverse relations are explicitly registered.

---

### 4. `semantic_graph.jsonld`

**Status:** Complete

Machine-readable JSON-LD representation of the semantic graph.

Currently contains approximately **14 graph nodes** representing the validated core structure.

The graph is not intended to encode every theoretical implication. It represents relations that have sufficient semantic justification at the current stage.

---

### 5. `id_registry.yaml`

**Status:** Complete

Registry of stable semantic identifiers.

Approximately **60 IDs** are currently registered.

The registry provides identity continuity across the semantic inventory, claims, relations, graph, and future extensions.

---

### 6. `ambiguity_registry.yaml`

**Status:** Complete

Registry of semantic ambiguities identified during reconstruction.

Currently contains approximately **7 ambiguities**.

Ambiguities are preserved rather than silently resolved.

---

### 7. `conflict_registry.yaml`

**Status:** Complete

Registry of conflicts between formulations or source positions.

Currently contains approximately **3 conflicts**.

A conflict is not automatically treated as an error. It may represent theoretical development, different abstraction levels, or genuinely unresolved incompatibility.

---

### 8. `undefined_term_registry.yaml`

**Status:** Complete

Registry of terms that are used by the corpus but are not sufficiently defined for unambiguous formalization.

Currently contains approximately **8 terms**.

This prevents undefined terminology from being silently promoted to formally established concepts.

---

### 9. `historical_formulation_registry.yaml`

**Status:** Complete

Registry of earlier theoretical formulations.

Currently contains approximately **4 historical formulations**.

Historical formulations are preserved because the evolution of a concept is itself semantically relevant.

A superseded formulation is not silently erased from the semantic history.

---

### 10. `derivation_registry.yaml`

**Status:** Complete

Registry of explicitly identified derivational relationships.

Currently contains approximately **5 derivations**.

The registry distinguishes actual derivations from relations that merely appear intuitively connected.

In particular:

> **An unestablished relation is not the same thing as the absence of a relation.**

and:

> **An unestablished necessity is not an independent fundamental principle.**

---

### 11. `validation_report.md`

**Status:** Complete

Final semantic and graph consistency report.

The current validation state is:

```text
READY_FOR_EXPANSION
```

The graph is internally consistent at the current semantic level, while theoretical questions and unresolved derivations remain explicitly marked.

---

# Key Semantic Distinctions

## Fundamental Invariant and Dissipation of Identity

The current working hierarchy distinguishes:

> **The prohibition of indifference is the fundamental principle.**

from:

> **Dissipation of identity is its processual consequence.**

The historical formulation in which dissipation of identity was treated as a fundamental invariant is preserved separately as a prior theoretical formulation.

The semantic layer does not encode the transition

```text
Ban → Dissipation
```

as a proven derivation unless the corpus establishes its necessity.

---

## Monos and Logos

The current formulation distinguishes:

> **Monos — process.**

> **Logos — the space of distinctions of the process.**

> **Model — a concrete framework for distinguishing the process.**

The proposed genesis of Logos is represented as:

```text
process
   ↓
difference
   ↓
recursion
   ↓
stability
   ↓
recognition
   ↓
identity / distinction
   ↓
Logos
```

This sequence remains subject to the status assigned to each individual claim.

---

## Actualization, Movement and Dissipation

Actualization, movement, and dissipation are treated as different semantic slices of a continuous process rather than necessarily as sequential temporal stages.

Thus:

> **The order is not fundamental; these are different slices of one continuous process.**

---

## Stability and Stasis

The semantic layer explicitly distinguishes:

```text
Stb = stabilization
Sts = stasis
```

with:

> **Stability ≠ immobility.**

A stable configuration may persist while the underlying process continues.

Therefore:

> **Stability is preservation of configuration during movement/dissipation.**

---

## Balance

Balance is not represented as static equalization.

The current formulation is:

> **Balance is a stable relation between processes realized through movement and dissipation.**

Thus:

```text
Interaction
     ↓
Balance
     ↓
Movement + Dissipation
     ↓
Stable Regime
```

---

## Geometry and Movement

Movement is treated as a processual class whose spatial manifestations may take different forms:

```text
Motion
├── Linear
├── Orbital
├── Shell
├── Helical
├── Toroidal
├── Möbius
└── other
```

These forms are not assumed to be sequential stages.

Geometry describes spatial realization.

Topology describes connectivity and invariant structural relations.

Model-specific geometric interpretations remain explicitly marked as such.

---

## Isomorphism and Structural Correspondence

The semantic layer distinguishes:

```text
isomorphic_to
homomorphic_to
mapped_to
projected_to
structurally_corresponds_to
analogous_to
```

A corpus-level structural correspondence does not automatically constitute a mathematical isomorphism.

Therefore, where an explicit mapping and preserved structure have not been established:

```text
structurally_corresponds_to = SOURCE
isomorphic_to = UNRESOLVED
```

---

## CMI

The semantic structure distinguishes two related constructions:

### CMI

```text
Conflict → Moment → Impulse
```

This is treated as the foundational CMI triad.

### CMI Chain — Extended

```text
Prohibition
    ↓
Momentum
    ↓
Force
    ↓
Energy
    ↓
Dissipation
    ↓
Arrow of Time
```

The extended chain is represented separately and linked to CMI through an explicit extension relation.

This prevents the six-element chain from being incorrectly identified with the original three-element CMI structure.

---

# Graph Consistency

The final graph consistency audit identified and resolved several structural issues:

1. Missing inverse relation `triggered_by`
2. Missing inverse relation `derives`
3. Entity–Claim separation for operator properties
4. Distinction between `maps_to` and `unfold`
5. Separation of `isomorphic_to` from corpus-level structural correspondence
6. Separation of CMI from the extended CMI Chain
7. Separation of source claims from unresolved logical derivations
8. Distinction between Absolute Identity and fundamental Indifference

The result is a semantically consistent graph representation without artificially closing unresolved theoretical questions.

---

# Current Status

```text
SEMANTIC CORE
        ↓
AUDITED
        ↓
GRAPH CONSISTENCY PASSED
        ↓
THEORETICAL QUESTIONS PRESERVED
        ↓
READY FOR EXPANSION
```

The semantic core should therefore be understood as **structurally validated, but not theoretically closed**.

Its purpose is to provide a stable semantic foundation on which further formal and computational layers can be built.

---

# Next Expansion

The next stage is the expansion of the semantic architecture into:

```text
METAMONISM
     ↓
ONTODYNAMICS
     ↓
UFCPS
     ↓
EECP
```

The same semantic reconstruction methodology will be applied to the subsequent layers.

The existing semantic core is intended to provide the stable reference layer for these expansions.

---

# Methodological Principle

The repository follows one central rule:

> **Semantics first. Type second. Formalization third. Identity fourth.**

And one architectural principle:

> **The architecture must be extracted from the corpus, not invented on top of it.**

The objective is not to make Meta-Monism appear more complete than it is.

The objective is to make its existing semantic structure **explicit, traceable, machine-readable, and extensible**.

