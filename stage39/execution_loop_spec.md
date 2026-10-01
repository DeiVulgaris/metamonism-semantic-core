# Research Execution Loop Specification

## 1. Purpose

RESEARCH_RESULT is the process object produced after a research task is executed.

It connects the task layer to trajectory memory and the next research frontier.

## 2. Required distinctions

### Task state

A task may be READY, IN_PROGRESS, COMPLETED, FAILED or REJECTED.

### Result class

A recorded execution may be CONFIRMING, DISCONFIRMING, PARTIALLY_CONFIRMING, INCONCLUSIVE, ANOMALOUS, INVALID, UNREPRODUCIBLE or BLOCKED.

### Epistemic status

The result may contain an epistemic status inherited from the research context, but result recording must never upgrade it automatically.

### Frontier state

The successor frontier explicitly records the new process state.

These four dimensions must not be collapsed.

## 3. Result contract

Required:

- result_id
- task_id
- frontier_id
- research_program_id
- trajectory_id
- result_class
- observation
- interpretation
- unresolved_difference
- evidence
- successor_frontier
- provenance

The successor frontier is an explicit object, not an inferred conclusion.

## 4. Conservative update rule

The engine accepts a successor frontier only when:

- it points to the same research program;
- it points to the same trajectory;
- its provenance is present;
- non-SOURCE material carries derived_from;
- it has a valid frontier state;
- it does not erase the predecessor.

The engine does not determine whether a result scientifically establishes a proposition.

## 5. Result semantics

| Result class | Meaning |
|---|---|
| CONFIRMING | execution supports the working expectation |
| DISCONFIRMING | execution conflicts with the working expectation |
| PARTIALLY_CONFIRMING | only part of the expected structure is supported |
| INCONCLUSIVE | execution does not discriminate sufficiently |
| ANOMALOUS | observation does not fit the current expected structure |
| INVALID | execution cannot support the intended inference |
| UNREPRODUCIBLE | result cannot currently be reproduced |
| BLOCKED | execution could not proceed because of an explicit blocker |

These meanings describe the execution, not the truth of the hypothesis.

## 6. Continuity

The trajectory transition should record:

- task as trigger;
- result as evidence;
- predecessor state;
- successor state;
- provenance.

A failed or negative result remains part of the trajectory.

## 7. Forbidden transformations

Never:

- convert CONFIRMING into SOURCE automatically;
- convert DISCONFIRMING into deletion;
- convert INCONCLUSIVE into absence of information;
- convert BLOCKED into TERMINATED;
- rewrite the predecessor state;
- erase the executed task;
- infer formal isomorphism from a successful comparison;
- promote a structural correspondence to identity.

## 8. Closed-loop contract

After result recording, Stage 38 can instantiate new tasks from the successor frontier.

No additional semantic layer is required between RESULT and FRONTIER.
