# Stage 55 — Core ↔ UFCPS Task Formation Bridge

## Purpose

Stage 55 defines the bridge between the Metamonism Semantic Core and the
Universal Framework for Complex Problem Solving (UFCPS).

The bridge is not a merge of the two theories. It is an interface contract:

```
SEMANTIC CORE
    ↓
semantic state / frontier
    ↓
TASK FORMATION
    ↓
UFCPS TASK PROSPECT
    ↓
CLAIM / EXECUTION
    ↓
RESULT / DEADLOCK
    ↓
SEMANTIC UPDATE
    ↓
NEXT FRONTIER
```

The semantic core supplies the **meaning and admissibility constraints**.
UFCPS supplies the **procedural machinery for turning an unresolved
difference into an executable cognitive step and preserving its result**.

## Central invariant

> A task is not generated merely because an output is missing.
> A task is generated from a registered unresolved difference together with
> enough continuation-relevant state to define a legitimate next operation.

## Four-layer separation

### 1. Semantic Layer

Authoritative objects:

- entities
- claims
- relations
- provenance
- epistemic status
- registered derivations
- unresolved questions / frontiers

The semantic layer answers:

```
WHAT IS THE CURRENT PROBLEM STATE?
WHAT IS KNOWN?
WHAT IS UNKNOWN?
WHAT IS PROHIBITED?
WHAT IS ACTUALLY DERIVED?
```

### 2. Frontier Layer

A frontier is the current boundary of established knowledge/process.

Minimal abstraction:

```
Frontier =
(current_state,
 unresolved_difference,
 constraints,
 evidence,
 failed_or_exhausted_paths,
 next_question)
```

A frontier is not itself a task.

### 3. Task Formation Layer

Task formation transforms a frontier into a UFCPS-compatible task candidate.

```
TaskFormation(FRONTIER)
        ↓
TASK CANDIDATE
```

The transformation is valid only when:

- the unresolved difference is explicit;
- the attempted/active path is known;
- the relevant constraints are preserved;
- the required next operation is identifiable or discoverable;
- provenance is preserved;
- no source-level status is silently promoted.

### 4. UFCPS Execution Layer

UFCPS handles:

```
Task Prospect
   ↓
Agent Decision
   ↓
Claim
   ↓
Resource Reservation
   ↓
Execution
   ↓
Result / Deadlock
   ↓
State Preservation
   ↓
UQL / Next Discovery
```

## Bidirectional contract

The bridge has two directions.

### Core → UFCPS

```
Semantic Frontier
      ↓
Question Object
      ↓
Task Prospect
      ↓
Agent Claim
      ↓
Execution
```

The bridge copies **references and continuation requirements**, not uncontrolled semantic content.

### UFCPS → Core

```
Execution Result
      ↓
Result Classification
      ↓
Semantic Evidence / Claim Candidate
      ↓
Frontier Update
```

Possible result classes include:

- solution
- partial result
- negative result
- contradiction
- inconclusive result
- anomaly
- deadlock

A negative, contradictory, or inconclusive result is not converted into semantic truth
merely because an execution produced it. It becomes **new process information**
subject to semantic validation.

## Task formation versus task execution

The bridge explicitly separates:

```
QUESTION
≠
TASK CANDIDATE
≠
CLAIM
≠
EXECUTION
≠
RESULT
```

This mirrors UFCPS' existing separation between discovery, claim, acceptance,
resource reservation, and execution.

## Relation to continuation map F

The existing core defines the minimal continuation mechanism:

```
F : R_n → A_{n+1}
```

Stage 55 does not replace it.

Instead:

```
R_n
 ↓
boundary information
 ↓
frontier representation
 ↓
task formation
 ↓
UFCPS execution
 ↓
result
 ↓
candidate A_{n+1}
```

A task is therefore an **operational carrier of a continuation candidate**.

This does not establish that every result defines a unique successor.

## No hidden promotion

The bridge must not silently turn:

- UNRESOLVED → SOURCE
- HYPOTHESIS → FACT
- STRUCTURAL_CORRESPONDENCE → ISOMORPHISM
- MODEL → ONTOLOGY
- NEGATIVE RESULT → PROOF OF IMPOSSIBILITY

All result promotion remains subject to the semantic validation layer.

## Minimal bridge object

See `bridge_contract.schema.json`.

The minimal object carries:

```
bridge_id
source_frontier
question_id
question
unresolved_difference
constraints
evidence_refs
failed_paths
next_required_operation
task_formation_status
provenance
```

## Design objective

The bridge is intended to make the pair of repositories function as a single
stack without collapsing their roles:

```
METAMONISM SEMANTIC CORE
        =
meaning + constraints + semantic admissibility

UFCPS
        =
problem formation + procedural execution + continuity

TOGETHER
        =
semantic-governed continuous problem solving
```

## Status

This stage is an architectural integration proposal and implementation
contract. It does not establish a new theorem of Metamonism or a theorem of
UFCPS.
