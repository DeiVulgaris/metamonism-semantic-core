# Stage 38 — Frontier → Research Task Engine Specification

## 1. New object

A RESEARCH_TASK is an instantiated obligation generated from:
1. a current RESEARCH_FRONTIER;
2. one admissible transition;
3. the unresolved difference and prerequisites attached to that frontier.

RESEARCH_TASK = instantiate(FRONTIER, ADMISSIBLE_TRANSITION)

## 2. Three distinct objects

Frontier answers: What is currently unresolved?
Transition answers: What kind of operation is structurally admissible now?
Task answers: What concrete research obligation follows from that operation?

## 3. Lifecycle

PROPOSED → READY → IN_PROGRESS → COMPLETED / FAILED / REJECTED

BLOCKED and PROHIBITED are non-executable states.

A CONDITIONAL transition produces PROPOSED, not READY.

## 4. No hidden selection

The engine generates admissible tasks. It does not decide which task is scientifically most important. A later selection policy may consider prerequisites, resources, dependency order, user choice, cost, or urgency, but must not encode such a choice as truth.

## 5. Provenance

Every task inherits frontier provenance and derived_from where present. A generated task is a process artifact, never a source-authored claim.

## 6. Anti-collapse

Completing a task does not imply hypothesis confirmation, identity, formal isomorphism, changed source claims, or canonical registration.

## 7. Example

For R1–R4 ↔ Dirac with unresolved state space and composition law:
- DEFINE can produce a ready task;
- FORMALIZE can remain conditional;
- COMPARE can be admissible if prerequisites permit;
- COUNTEREXAMPLE can be admissible.

None is a conclusion.

## 8. Process loop

RESULT → UPDATE TRAJECTORY → UPDATE FRONTIER → GENERATE TRANSITIONS → INSTANTIATE TASKS → EXTERNAL SELECTION → EXECUTION → RESULT / DEADLOCK / DIFFERENCE

This is the first explicit operational loop in which research tasks emerge from the structure of unresolved knowledge itself.
