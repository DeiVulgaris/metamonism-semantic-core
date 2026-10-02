# Stage 56 — Semantic ↔ UFCPS Runtime

Stage 56 turns the Stage 55 bridge into an executable deterministic adapter.

Core to UFCPS:
semantic frontier -> question -> task prospect -> procedural state -> execution

UFCPS to Core:
result/deadlock -> candidate semantic update -> next frontier -> next task

Responsibility split:
- Semantic Core provides meaning, provenance, epistemic status, constraints and unresolved differences.
- UFCPS provides discovery, claim, resource binding, execution and process continuity.
- The adapter performs representation and state-transition work only.

Core invariant:
A task is formed from a registered unresolved difference plus enough continuation-relevant state to define a legitimate next operation.

Important separations:
question != task prospect != claim != execution != result
result != truth
negative result != termination
deadlock != termination
solution candidate != validated semantic claim

Stage 56 does not modify the canonical ontology. It is an integration/runtime layer.

See:
semantic_to_ufcps_runtime.py
ufcps_result_to_frontier.py
runtime_contract.schema.json
test_vectors.yaml
validation_report.md