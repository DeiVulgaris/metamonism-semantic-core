# Stage 40 Validation Report

Stage 40 establishes an explicit selection layer.

Verified: only READY tasks are selectable; USER_SELECTED requires an explicit task; metric policies require external metrics; missing metrics cause BLOCKED rather than fabrication; deterministic tie-breaking is explicit; parallel branching does not rank branches; selection does not change epistemic status; selection does not modify frontier state; competing tasks remain present; provenance is recorded.

Architecture:

FRONTIER -> TRANSITIONS -> TASKS -> SELECTION POLICY -> EXECUTION -> RESULT -> FRONTIER

The selector answers which admissible obligation is executed under a declared policy. It does not answer which hypothesis is true.
