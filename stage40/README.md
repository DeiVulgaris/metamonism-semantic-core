# Stage 40 — Research Selection Policy

Selection is the explicit policy layer between generated research tasks and execution.

TASK SET -> SELECTION POLICY -> SELECTION DECISION -> EXECUTION

Selection is procedural, not epistemic. Choosing a task never means that its hypothesis is true, more important in an absolute sense, or canonical.

Supported policies: USER_SELECTED, DEPENDENCY_FIRST, BLOCKER_FIRST, CHEAPEST_TEST_FIRST, INFORMATION_GAIN, PARALLEL_BRANCHING.

External metrics are supplied to the selector; the semantic core never invents cost, information gain, blocker reduction, or dependency depth.

Missing required metrics produce a BLOCKED decision.

The decision records policy, candidates, selected tasks, criteria, metrics and provenance.

PARALLEL_BRANCHING selects explicitly eligible branches without preferring one branch.

Invariant: selected(task) != epistemic_upgrade(task).
