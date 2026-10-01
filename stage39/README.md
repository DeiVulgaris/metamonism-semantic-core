# Stage 39 — Research Execution Loop

Stage 39 closes the operational research loop.

```
RESEARCH_TASK
    ↓
EXECUTION (external)
    ↓
RESEARCH_RESULT
    ↓
TRAJECTORY UPDATE
    ↓
FRONTIER UPDATE
    ↓
ADMISSIBLE TRANSITIONS
    ↓
RESEARCH_TASKS
```

## Core rule

A task being completed means that an execution produced a recorded result. It does **not** mean that the research question was solved.

A result is process information, not an automatic epistemic upgrade.

## Result classes

- CONFIRMING
- DISCONFIRMING
- PARTIALLY_CONFIRMING
- INCONCLUSIVE
- ANOMALOUS
- INVALID
- UNREPRODUCIBLE
- BLOCKED

These are process-result classes, not epistemic statuses.

## Observation / interpretation separation

The result object keeps:

1. observation — what execution produced;
2. interpretation — what the researcher currently infers from that observation;
3. result class — procedural characterization;
4. unresolved difference — what remains open.

An interpretation never silently becomes a source claim.

## Frontier update

The executor supplies an explicit successor frontier. The engine validates continuity but does not invent scientific conclusions from the result class.

Thus:

- CONFIRMING does not automatically create CANONICAL knowledge;
- DISCONFIRMING does not delete the hypothesis;
- INCONCLUSIVE does not mean no information;
- BLOCKED does not mean TERMINATED;
- ANOMALOUS preserves the anomaly as information.

## Append-only trajectory

The previous trajectory state and frontier are immutable. A result creates a new state linked by a transition.

## External execution

Stage 39 records and validates execution results. It does not execute experiments, select truth, rank hypotheses, or decide scientific priority.

## Main invariant

`TASK → RESULT` is not `TASK → TRUTH`.

The closed research loop is:

`UNKNOWN → ADMISSIBLE OPERATION → TASK → RESULT → NEW FRONTIER → NEW TASK`.
