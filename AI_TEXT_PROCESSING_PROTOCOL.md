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

### Mandatory evidence provenance

Every extracted entity, claim, and relation MUST carry machine-readable provenance.

At minimum record:

- source repository;
- document path;
- source ref/version/commit when available;
- section, heading, paragraph, or line range;
- optional short source excerpt.

The provenance locator is part of the semantic record, not merely editorial metadata.


### C. Atomic claims
- claim ID;
- subject;
- predicate;
- object;
- evidence;
- status;
- formalization if present;
- `source_claim` — source wording or faithful quotation/paraphrase;
- `source_claim_as_interpreted` — semantic interpretation, if different;
- `derived_from` — mandatory for every non-SOURCE claim.

The distinction between `source_claim` and `source_claim_as_interpreted` prevents an AI interpretation from silently becoming the wording of the source.

For `INFERENCE`, `FORMALIZATION`, `THEORETICAL_HYPOTHESIS`, and `PROPOSAL`, `derived_from` MUST identify the source claims, registered entities, or prior derivations from which the statement was constructed.


### D. Relations
- source;
- relation type;
- target;
- direction;
- status;
- evidence;
- provenance locator;
- `derived_from` when the relation is not SOURCE.

A relation must not be inferred solely from co-occurrence in source prose.

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

### Provenance gate

Registration MUST fail if an atomic source-grounded claim has no provenance locator.

Registration MUST fail if a non-SOURCE claim has no `derived_from` path.

An AI may process a source without enough evidence to register a conclusion, but it must not register an unsupported conclusion as if its provenance were known.

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

## 25. Research Program Layer — Preserve the Process of Thinking

The protocol must distinguish between **processing a completed semantic statement**
and **continuing an unfinished line of reasoning**.

For unresolved research, create a `RESEARCH_PROGRAM` working object instead of
forcing the material into the canonical ontology.

A research program records:

- the open research question;
- source-grounded claims;
- working entities;
- proposed relations;
- candidate formalizations;
- required definitions and blockers;
- tests;
- expected observations;
- falsifiers;
- derivations and hidden assumptions;
- counterexamples;
- competing hypotheses;
- open questions;
- forbidden inferences;
- the next transition required for continuation.

### 25.1 The research state is a valid semantic state

Do not treat:

```text
UNRESOLVED
BLOCKED
HYPOTHESIS
FAILED TEST
COUNTEREXAMPLE
```

as missing data.

They are information about the current state of the reasoning process.

In particular:

> **An unresolved question is not an incomplete record. It is a record of where
> the process currently stands.**

### 25.2 Research lifecycle

A `RESEARCH_PROGRAM` may move through:

```text
OPEN
  ↓
FORMALIZING
  ↓
TESTING
  ├──→ BLOCKED
  ├──→ REJECTED
  ├──→ PARTIALLY_SUPPORTED
  └──→ SUPPORTED
             ↓
         INTEGRATED
```

These are investigation states, not truth labels.

`SUPPORTED` does not authorize canonical integration by itself.

### 25.3 Continuation rule

When a research program reaches an unresolved point, the AI MUST NOT close the
gap by inventing a definition, proof, equivalence, or physical interpretation.

Instead it must create the next explicit transition:

```text
CURRENT STATE
    ↓
BLOCKER / OPEN QUESTION
    ↓
REQUIRED DEFINITION OR TEST
    ↓
EXPECTED OBSERVATION
    ↓
FALSIFIER
    ↓
NEXT STATE
```

Thus the output of reasoning can itself be the **condition for further reasoning**.

### 25.4 Branching is permitted

If several explanations remain viable, preserve them as explicit competing
hypotheses.

Do not select one merely because it is simpler, more elegant, newer, or more
compatible with an existing theory.

Each branch must retain its own:

- provenance;
- assumptions;
- predicted consequences;
- tests;
- falsifiers;
- current status.

### 25.5 Negative results are productive state

A failed derivation, failed test, dimensional inconsistency, or counterexample
must not be erased.

Record:

```text
attempt → failure → reason → consequence → next question
```

A negative result can narrow the research space and therefore preserve a
meaningful continuation path.

### 25.6 Canonical isolation

`RESEARCH_PROGRAM` belongs to the working layer.

It may reference canonical entities, but it must not rewrite them.

Promotion from research program to canonical structure requires the existing
validation, provenance, relation-classification, and registration gates.

The following transitions are forbidden:

```text
hypothesis → canonical fact
analogy → identity
formal candidate → established formalism
failed derivation → silent repair
repeated proposal → SOURCE
AI interpretation → author statement
```

### 25.7 Process continuity as a core objective

The semantic core therefore has two complementary preservation tasks:

1. **semantic fidelity** — preserve what the corpus establishes;
2. **process continuity** — preserve the conditions under which unresolved
   questions can continue to be investigated.

The second is not an optional research-management feature. It is part of the
semantic architecture.

> **The purpose of the core is not to terminate thought at the point where the
> current corpus ends. It is to mark that boundary precisely enough that
> thought can continue from it.**

Stage 33 implements this layer in:

```text
stage33/research_program_schema.yaml
stage33/research_programs.yaml
stage33/research_program_validator.py
stage33/README.md
```


## 26. Research Process Engine

The `RESEARCH_PROGRAM` layer records an unfinished line of reasoning.
Stage 34 adds a process engine that determines the **next admissible research
action** from that state.

The engine MUST NOT answer the research question.

Its function is:

```text
CURRENT STATE
    ↓
BLOCKERS / OPEN QUESTIONS / TESTS / FAILURES
    ↓
ADMISSIBLE TRANSITIONS
    ↓
NEXT RESEARCH ACTION
```

The engine therefore operates on process state, not truth value.

### 26.1 Allowed transition types

```text
DEFINE_BLOCKER
ANALYZE_FAILURE
RUN_TEST
DESIGN_TEST
REFINE_QUESTION
REVIEW_STATE
```

#### DEFINE_BLOCKER

Used when a missing definition prevents safe continuation.

The AI may propose candidate definitions, but must preserve their status and
must not silently register them as SOURCE.

#### ANALYZE_FAILURE

Used when a test failed or a falsifier was encountered.

The failure must be retained. The AI should extract the reason, consequence,
new constraint, and possible next test.

#### RUN_TEST

Used when prerequisites are sufficiently defined.

Running a test does not imply a positive result.

#### DESIGN_TEST

Used when an open question has no registered falsifiable test.

A valid test must specify:

- target question;
- expected observation;
- falsifier;
- required definitions;
- provenance of the hypothesis being tested.

#### REFINE_QUESTION

Used when a question remains too broad or decomposable.

Refinement must narrow the question without answering it by assumption.

#### REVIEW_STATE

Used when no safe automatic transition exists.

### 26.2 Transition generation is not theory generation

The process engine may answer:

> What can be done next?

It may not answer:

> What is true?

Therefore:

```text
PROCESS ENGINE OUTPUT
        ≠
CANONICAL SEMANTIC CONCLUSION
```

### 26.3 Priority is operational, not epistemic

Transition priority indicates which blocker or research action should normally
be addressed first.

It MUST NOT be interpreted as:

- probability of truth;
- theoretical importance;
- preference for one hypothesis;
- evidence strength;
- prediction of research success.

### 26.4 Process continuity invariant

A valid processing run must leave the system in a state from which another
valid processing step can be identified, unless the program is explicitly
closed, rejected, integrated, or blocked.

Thus the preferred terminal state for an unresolved program is not an empty
result.

It is:

```text
KNOWN STATE + EXPLICIT LIMIT + NEXT POSSIBLE TRANSITION
```

This is the **process-continuity invariant**.

Stage 34 implements the engine in:

```text
stage34/research_process_engine.py
stage34/process_state_schema.yaml
stage34/test_vectors.yaml
stage34/README.md
```


## 27. Research Trajectory Memory

A research program must preserve not only its current state but also the path
by which that state was reached.

Stage 35 introduces `RESEARCH_TRAJECTORY`.

A trajectory records:

- ordered research states;
- transitions between states;
- branching hypotheses;
- tests and failures;
- revisions;
- rejected and falsified branches;
- reopening of earlier questions;
- provenance for every transition.

### 27.1 History is semantic information

The same proposition can have different research meaning depending on whether
it is:

- newly proposed;
- repeatedly tested;
- weakened by counterexample;
- retained after failed alternatives;
- reopened after a later discovery.

Therefore history must not be discarded as editorial detail.

### 27.2 Append-only rule

Previous states MUST NOT be rewritten.

If a later interpretation changes the understanding of an earlier state, create a
new state linked by an explicit relation such as `REVISES` or `REFERENCES`.

Do not retroactively rewrite the earlier state.

### 27.3 Failed branches are retained

A rejected or falsified hypothesis remains part of the trajectory.

It may encode a constraint:

```text
hypothesis
    ↓
test
    ↓
failure
    ↓
constraint on future search
```

Deleting the failed branch destroys information about the search space.

### 27.4 Research is non-linear

A previous question may become relevant again.

When that occurs, create a new state linked to the earlier state with
`REOPENS`.

The earlier state remains unchanged.

Thus:

```text
state₄
   ...
state₁₁
   ↓
REOPENS
   ↓
state₁₂
```

is valid research history.

### 27.5 Chronology is not evidence

Later states do not automatically have higher epistemic status.

The following inference is forbidden:

```text
later formulation
      ↓
therefore more true
```

Temporal order is provenance information, not proof.

### 27.6 Three-dimensional research memory

The system should preserve:

```text
SEMANTIC STATE
    what is known

RESEARCH STATE
    what is being investigated

TRAJECTORY
    how we arrived here
```

Together with the Stage 34 process engine:

```text
TRAJECTORY
    ↓
CURRENT STATE
    ↓
NEXT ADMISSIBLE ACTION
    ↓
NEW STATE
    ↓
TRAJECTORY
```

This creates a closed operational loop for continuing research while keeping
canonical ontology isolated from unfinished reasoning.

Stage 35 implements this layer in:

```text
stage35/research_trajectory_schema.yaml
stage35/research_trajectory.yaml
stage35/trajectory_engine.py
stage35/test_vectors.yaml
stage35/README.md
```
