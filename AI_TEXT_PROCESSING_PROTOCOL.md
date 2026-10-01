# AI Text Processing Protocol for Meta-Monism

## 1. Purpose

This repository is an operational semantic instruction set for AI systems processing Meta-Monism texts.

The primary task is not to summarize Meta-Monism, improve it, defend it, criticize it, or complete it.

> Given a Meta-Monism source text, reconstruct its semantic content faithfully, atomically, traceably, and without semantic collapse.

The semantic core is therefore a working memory and control layer for an AI text-processing pipeline.

## 2. Golden Rule

> Never make the text mean more than the source establishes.

The AI must not silently:

- strengthen or weaken a claim;
- resolve an ambiguity;
- repair a contradiction;
- promote a hypothesis to SOURCE;
- turn an analogy into an isomorphism;
- turn structural correspondence into identity;
- turn extension into equivalence;
- turn formalization into a source statement;
- turn a model into ontology;
- turn a physical interpretation into a logical proof.

If the source does not establish something, record that fact explicitly.

## 3. Processing Pipeline

~~~text
SOURCE TEXT
    ↓
SEGMENTATION
    ↓
ATOMIC SEMANTIC EXTRACTION
    ↓
ENTITY / CLAIM / RELATION SEPARATION
    ↓
SOURCE STATUS ASSIGNMENT
    ↓
EXISTING-CORE MATCHING
    ↓
COLLAPSEABILITY TEST
    ↓
RELATION CLASSIFICATION
    ↓
FORMALIZATION
    ↓
CONFLICT / AMBIGUITY / UNDEFINED CHECK
    ↓
DERIVATION CHECK
    ↓
STABLE ID DECISION
    ↓
TRACEABLE REGISTRATION
    ↓
VALIDATION
~~~

The order is deliberate:

> Semantics → type → status → relation → formalization → identity.

Do not jump directly from prose to canonical IDs.

## 4. Atomic Extraction

Split source text into semantically meaningful statements. Do not treat a paragraph as one claim if it contains several independent assertions.

For example, a sentence saying that differentiation prevents identity, generates motion, and produces dissipation contains at least three claims.

Claims occurring in one sentence do not automatically have identical logical status.

## 5. Entity / Claim / Relation

Entity = identifiable semantic element: concept, process, operator, state, domain, model, invariant, formulation, mathematical object, or physical interpretation.

Claim = assertion about one or more entities.

Relation = typed connection between semantic elements.

Never encode a claim as an entity. Never infer a relation merely because two entities occur in the same sentence.

## 6. Status Assignment

Use the repository status taxonomy:

| Status | Meaning |
|---|---|
| SOURCE | Explicitly confirmed by the source corpus |
| INFERENCE | Follows from registered source material without a new fundamental assumption |
| FORMALIZATION | Formal representation of existing semantic content |
| THEORETICAL_HYPOTHESIS | Theoretical proposition not established as source fact |
| PROPOSAL | New construction proposed during analysis |
| UNRESOLVED | Cannot currently be established |
| CONFLICT | Source-level conflict |
| USED_BUT_UNDEFINED | Used but insufficiently defined |
| PRIOR_THEORETICAL_FORMULATION | Earlier formulation preserved as historical data |
| MODEL_SPECIFIC | Valid only inside a particular model or hypothesis |

> Origin is not status.

An AI-generated reconstruction can be FORMALIZATION. An AI-generated proposal remains PROPOSAL. A source text may itself contain a THEORETICAL_HYPOTHESIS.

## 7. Existing-Core Matching

Before creating a new semantic ID, search the existing core:

- canonical names;
- aliases;
- definitions;
- claims;
- relations;
- historical formulations;
- ambiguity registry;
- conflict registry;
- undefined-term registry.

The first question is not what the element should be called.

> The first question is whether this semantic object already exists.

## 8. Semantic Collapseability

For candidate concepts A and B ask:

> If A were deleted, could the complete semantic content of A be reconstructed from B without information loss?

If yes, investigate same content, equivalent formulation, or formalization.

If no, preserve the distinction.

Never merge merely because terminology is similar, definitions overlap, operators are similar, diagrams resemble one another, or two concepts occupy analogous positions.

Semantic similarity is not semantic identity.

## 9. Relation Discipline

Distinguish explicitly:

- identity;
- equivalent formulation;
- structural correspondence;
- extension;
- specialization / generalization;
- formal isomorphism;
- unresolved relation.

Structural correspondence is not formal isomorphism.

Extension is not identity.

Similarity is not equivalence.

For extension:

~~~text
B extends A
~~~

does not imply A = B and does not imply formal isomorphism.

## 10. Formalization

Formalization is a representation layer.

If the source says that absolute identity is impossible and the AI writes a symbolic expression representing that statement, the expression is FORMALIZATION unless the source itself explicitly presents the expression as part of its formal theory.

Mathematical precision does not upgrade epistemic status.

## 11. Derivation Discipline

For every apparent derivation ask:

1. Are the premises explicitly present?
2. Is the inference valid under registered assumptions?
3. Are hidden assumptions required?
4. Does the corpus itself state the derivation?
5. Is the result source material or AI reconstruction?

Use the derivation registry.

A derivation may be SOURCE, INFERENCE, THEORETICAL_HYPOTHESIS, or UNRESOLVED.

> An unestablished relation is not the same thing as absence of a relation.

> An unestablished necessity is not an independent fundamental principle.

## 12. Contradictions and History

When two formulations conflict, do not choose the one that looks newer or more elegant.

Preserve both formulations, their evidence, status, and theoretical or historical relation.

A contradiction may represent genuine conflict, terminology change, abstraction-level change, historical development, or unresolved tension.

Do not decide which explanation applies without evidence.

## 13. Layer Discipline

At minimum distinguish:

~~~text
ONTOLOGICAL
PROCESSUAL
EPISTEMIC
FORMAL
PHYSICAL
COGNITIVE
MODEL-SPECIFIC
HISTORICAL
~~~

A statement valid in one layer must not automatically be transferred to another.

Forbidden patterns include physical analogy → ontological identity, mathematical similarity → physical equivalence, cognitive model → fundamental ontology, and formal mapping → empirical truth.

## 14. Process Before Object

Meta-Monism is strongly processual.

When a source describes movement, differentiation, stabilization, dissipation, actualization, unfolding, or recursion, do not automatically convert the process into a static entity.

> Stability ≠ stasis.

A stable configuration may persist while the underlying process continues.

Geometry describes spatial realization. Topology describes connectivity and invariant structural relations. Neither automatically replaces process with static structure.

## 15. Monos / Logos

Current registered formulation:

~~~text
Monos = continuous processual differentiation
Logos = epistemic space of models, theories and fixed representations
~~~

The registered relation is STRUCTURAL_CORRESPONDENCE, not automatic identity or formal isomorphism.

Do not silently rewrite Monos = Logos or Logos is merely a representation of Monos unless a source explicitly establishes that stronger relation.

## 16. CMI / CMI Chain

Treat these as distinct registered structures.

CMI:

~~~text
Prohibition / Conflict
        ↓
Momentum / Moment-Impulse
        ↓
Force
~~~

CMI Chain:

~~~text
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
~~~

The registered relation is CMI Chain extends CMI.

Therefore the benchmark result is EXTENSION, not identity.

The additional stages must not be discarded during normalization.

## 17. Dissipation

Do not assume every occurrence of dissipation has identical semantics.

The benchmark distinguishes at least ontological dissipation, UFCPS operational dissipation, and ONTODYNAMICS/model-specific dissipation.

When comparing them, preserve layer, role, process position, formalization, epistemic status, and cross-layer relation.

A comparison may legitimately return PARTIAL rather than forcing a unified definition.

## 18. Output Contract

Every processed source should produce, where applicable:

### A. Source metadata
- source;
- location;
- date/version;
- author;
- document context.

### B. Extracted entities
- temporary ID;
- proposed canonical name;
- type;
- definition;
- aliases;
- evidence;
- status.

### C. Atomic claims
- claim ID;
- subject;
- predicate;
- object;
- evidence;
- status;
- formalization if present.

### D. Relations
- source;
- relation type;
- target;
- direction;
- status;
- evidence.

### E. Derivations
- premises;
- conclusion;
- relation type;
- hidden assumptions;
- status.

### F. Uncertainty
- unresolved terms;
- ambiguities;
- conflicts;
- competing interpretations;
- missing definitions.

### G. Integration decision

Each candidate addition should be classified as one of:

~~~text
NEW
EXISTING
EQUIVALENT
EXTENSION
SPECIALIZATION
HISTORICAL
MODEL_SPECIFIC
UNRESOLVED
CONFLICT
~~~

Never silently modify the canonical core during extraction.

## 19. Canonical Core vs Working Reconstruction

Maintain a strict boundary.

Canonical semantic core contains only registered structures with traceable evidence.

Working reconstruction may contain candidate mappings, AI formalizations, unresolved hypotheses, and tentative relationships.

A working reconstruction must never silently become canonical.

## 20. Validation Gate

Before registering an element ask:

- What exactly does it mean?
- Where is it established?
- What is its epistemic status?
- Does it already exist?
- Can it be merged without information loss?
- What exact relation does it have to existing structures?
- At what theoretical layer does it operate?
- Is it asserted, inferred, or hypothesized?
- Does it conflict with an existing formulation?
- Can another AI reconstruct why this entry exists?

If any answer is unknown, preserve the uncertainty instead of guessing.

## 21. Forbidden AI Behaviors

Hard prohibitions:

- semantic beautification;
- theory completion;
- semantic unification;
- retroactive proof;
- cross-layer promotion;
- mathematical inflation;
- historical erasure;
- masking AI authorship as source authorship.

## 22. Minimal Decision Tree

~~~text
Is it explicitly in the source?
        │
   YES  │  NO
        │
     SOURCE       Can it be derived?
                       │
                  YES  │  NO
                       │
                   INFERENCE     UNRESOLVED
~~~

Then:

~~~text
Does it match an existing semantic object?
        │
   YES  │  NO
        │
  compare meaning     candidate NEW
        │
        ↓
Can one be removed without semantic loss?
        │
   YES  │  NO
        │
same/equivalent       preserve distinction
                      │
                      ↓
             relation classification
~~~

Never skip from lexical similarity to identity.

## 23. AI Role

The AI is not the author of the ontology during processing.

~~~text
READER
  ↓
EXTRACTOR
  ↓
SEMANTIC ANALYST
  ↓
TRACEABILITY BUILDER
  ↓
VALIDATOR
~~~

Only after these stages may it act as a formalizer.

The AI may propose interpretations, but proposals must remain visibly proposals.

## 24. Final Principle

The repository exists to make Meta-Monism machine-processable without making it machine-rewritten.

> Semantic fidelity under transformation is the primary quality criterion.

A successful processing run allows a later reader to move from source text to semantic extraction, registered entity/claim/relation, status, formalization, and graph — and back again without losing the distinction between what the author said, what follows from it, what was formalized, what was hypothesized, what remains unresolved, and what the AI itself proposed.

> **The semantic core is not the answer. It is the control system that keeps an AI from corrupting the answer while processing the corpus.**