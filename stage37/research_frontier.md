# Stage 37 — Research Frontier

## Purpose

`RESEARCH_FRONTIER` is the machine-readable representation of the current boundary between what a research process has established and what remains open.

It is not a task queue, a conclusion registry, or a second canonical ontology.

Core principle:
> The research frontier is where the current process meets the unknown.

## Architectural position

```text
CANONICAL CORE
      ↓
RESEARCH PROGRAM
      ↓
TRAJECTORY
      ↓
RESEARCH FRONTIER
      ↓
PROCESS ENGINE
      ↓
NEXT ADMISSIBLE TRANSITION
```

## Frontier states

- ESTABLISHED — supported by appropriate evidence and validation.
- PARTIALLY_RESOLVED — some dimensions are established, others remain open.
- UNRESOLVED — no validated resolution yet.
- BLOCKED — continuation requires a missing definition, capability, resource, observation, or operation.
- CONFLICTING — source-grounded or derived states currently cannot be reconciled.
- UNTESTED — hypothesis or proposed mechanism has not received its required test.
- NEWLY_GENERATED — a new question or difference emerged from a prior state.

These are **research-process states**, not epistemic statuses.

## Epistemic status vs frontier state

The distinction is mandatory.

```yaml
status: SOURCE
frontier_state: ESTABLISHED
```

or:

```yaml
status: THEORETICAL_HYPOTHESIS
frontier_state: UNTESTED
```

A SOURCE claim can therefore be conflicting with another SOURCE claim. A theoretical hypothesis can be well formulated but untested.

## UQL integration

UFCPS contributes the distinction:

```text
Question → Investigation State → Resolution
```

The semantic-core mapping is:

```text
UQL Question
      ↓
RESEARCH_PROGRAM
      ↓
RESEARCH_TRAJECTORY
      ↓
RESEARCH_FRONTIER
```

The frontier does not replace UQL. It is the current structured view of the active inquiry boundary.

## Trajectory integration

```text
TRAJECTORY_n
     ↓
RESULT / DEADLOCK / DIFFERENCE
     ↓
FRONTIER_n
     ↓
TRANSITION
     ↓
TRAJECTORY_n+1
```

History remains append-oriented. The current frontier may change; historical trajectory records are not silently rewritten.

## Deadlock

A UFCPS structural deadlock maps to:

```text
STATE
CONSTRAINT
BOUNDARY
UNRESOLVED DIFFERENCE
```

A deadlock becomes a structured frontier item, normally BLOCKED, but does not automatically mean TERMINATED.

Possible continuation includes a new question, alternative transition, required definition, capability requirement, branch, experiment, or explicit safe termination.

## Contradiction

Contradiction is first-class:

```text
Claim A + Claim B
       ↓
CONFLICTING FRONTIER ITEM
       ↓
NEW DIFFERENCE
       ↓
possible successor questions
```

Both states, their provenance, conditions, epistemic status, and conflict must remain visible. No preference is assigned merely because one formulation is newer or simpler.

## Partial resolution

Partial resolution is first-class. For example:

```text
R1-R4 ↔ Dirac structure

structural correspondence = registered
formal isomorphism = unresolved
representation = undefined
empirical consequence = untested
```

## Admissible transitions

The frontier enumerates operations that are structurally admissible; it does not issue commands.

Candidate transitions:

```text
DEFINE
FORMALIZE
TEST
COMPARE
DERIVE
COUNTEREXAMPLE
REPLICATE
BRANCH
COMPOSE
DELEGATE
REFRAME
TERMINATE
```

An AVAILABLE transition means the prerequisites are present. CONDITIONAL means prerequisites remain. BLOCKED means a known blocker prevents it. PROHIBITED means protocol rules forbid it.

## Frontier evolution

```text
FRONTIER_n
    ↓
PROCESS TRANSITION
    ↓
NEW EVIDENCE / RESULT / DEADLOCK
    ↓
FRONTIER_n+1
```

Evolution may close, split, merge, conflict, partially resolve, unblock, or generate new frontier items.

## Canonical-core boundary

The frontier must never silently promote working research into canonical ontology.

```text
working hypothesis
      ↓
frontier item
      ↓
test
      ↓
validated result
      ↓
candidate canonical registration
```

Canonical registration remains governed by provenance and validation gates.

## Semantic-collapse boundary

Frontier construction uses the existing collapseability test. Similarity does not authorize identity.

Relations remain typed as appropriate:

IDENTITY, EQUIVALENT_FORMULATION, STRUCTURAL_CORRESPONDENCE, EXTENSION, SPECIALIZATION, GENERALIZATION, UNRESOLVED, CONFLICT.

## Machine contract

A minimal record contains:

```yaml
frontier_id: RF-...
research_program_id: RP-...
trajectory_id: RT-...
frontier_state: UNRESOLVED
epistemic_status: THEORETICAL_HYPOTHESIS

subject:
  ref: mm:...

unresolved_difference: ...

evidence: [...]

provenance:
  repository: ...
  path: ...
  ref: ...
  locator: ...

derived_from: [...]
constraints: [...]
blockers: [...]
open_questions: [...]

admissible_transitions:
  - type: FORMALIZE
    status: CONDITIONAL
    prerequisites: [...]
```

## Validation requirements

A frontier validator must reject missing identity, missing provenance, non-SOURCE records without derived_from, invalid states, invalid transition statuses, and silent contradiction collapse.

It must allow unresolved items, conflicts, blocked states, failed branches, negative results, untested hypotheses, and incomplete formalizations.

## Core invariants

```text
Frontier != Truth
Frontier != Task Queue
Unresolved != Empty
Blocked != Terminated
Contradiction != Deletion
Negative Result != No Information
Research Identity != Carrier Identity
History != Mutable Frontier
Epistemic Status != Frontier State
```

## Relation to UFCPS

Borrow UQL, structured deadlock, question evolution, negative-result preservation, branch preservation, composition, and research continuity.

Keep economic infrastructure, blockchain assumptions, swarm implementation requirements, and carrier-selection algorithms outside the semantic core.

## Relation to AI Text Processing Protocol

```text
SOURCE TEXT
   ↓
ATOMIC EXTRACTION
   ↓
SEMANTIC RECORDS
   ↓
RESEARCH PROGRAM
   ↓
TRAJECTORY
   ↓
FRONTIER UPDATE
```

The AI must keep a source claim, a frontier item, an AI-derived hypothesis, and a proposed next transition as separate typed and traceable objects.

## Final principle

> A good research system does not merely store what it knows. It stores the exact shape of what it does not yet know.

> The frontier is the machine-readable boundary at which semantic knowledge becomes research.