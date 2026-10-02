# BRIDGE_RUNTIME_CONTRACT

Status: Active baseline after Stage 61 closeout

## Purpose

This page freezes the division of responsibility for the single E2E continuity contour.

The contract is deliberately operational. It does not introduce ontology and does not create a new Stage.

## One working contour

frontier
→ task formation (55)
→ runtime prospect (56)
→ mock retrieval/provider envelope (58–59)
→ classification (60)
→ invariant-rooted replay (60)
→ impact localization (61)
→ localized frontier
→ UQL-style update
→ next operation

## Layer responsibilities

| Layer | Does | Does not |
|---|---|---|
| Semantic Core | preserve meaning, status, provenance, reasoning trace and frontier | silently create claims or change ontology |
| Stage 55 | turn an explicit unresolved frontier into a task candidate and preserve question identity | assign execution or promote a result to truth |
| Stage 56 | construct UFCPS-shaped question, task prospect and procedural runtime state | establish that a successor actually exists |
| Stage 58–59 | represent/serve provider-neutral retrieval and explicit provider errors | decide semantic truth |
| Stage 60 | classify retrieval and replay the registered chain from its root invariant | invent missing derivations or rewrite the root |
| Stage 61 | localize explicit impact and rebuild the affected frontier | infer causal impact from free text |
| UQL-style update | reopen the frontier at the affected step while preserving history | delete prior history or terminate from classification alone |

## Required invariants

1. question_id is stable end-to-end.
2. result classification is operational information, not a validated semantic claim.
3. negative, gap, contradiction and retrieval failure do not imply process termination.
4. impact is explicit through affected_step_id, or a labelled TAIL_FALLBACK is used.
5. downstream reasoning is retained as REQUIRES_REPLAY, not deleted.
6. history is append-only in the E2E harness.
7. ontology registry files are unchanged by the E2E run.
8. no automatic claim-registry write follows SOLUTION_FOUND.

## Root and chain

The E2E fixture uses a stable synthetic root identifier:

ufcps:scp.inv.local_failure_not_process_termination.v1

The identifier belongs to the test fixture chain and is sourced conceptually from UFCPS Step Continuity Protocol. It is not added to Semantic Core ontology registries.

The chain under test contains four procedural steps:

S1 — deadlock as structured information  
S2 — state handoff  
S3 — continuation through preserved state  
S4 — unfold / next procedural unit

## Impact rules

Explicit reference:

affected_step_id = S3
→ EXPLICIT_STEP_REFERENCE
→ S3 is reopened
→ later steps receive REQUIRES_REPLAY

No explicit reference:

no affected_step_id
→ TAIL_FALLBACK
→ last step only
→ fallback_label = procedural_tail_fallback_not_causal_attribution

The fallback is a procedural convenience, not a causal inference.

## Claim boundary

The following transitions are prohibited by this contract:

retrieval result → validated semantic claim  
retrieval failure → process termination  
contradiction → root invalidation  
free-text similarity → affected_step_id  
missing information → falsehood  
successful runtime object → proof of successor existence

## E2E command

From the repository root:

python -m pip install pyyaml jsonschema
python e2e/e2e_bridge_runner.py

The runner executes all six fixture cases and prints operational metrics.

## Completion condition

The priority is complete when one command reproducibly demonstrates:

question_id preservation  
→ task formation  
→ runtime prospect  
→ mock retrieval  
→ classification  
→ invariant-rooted replay  
→ impact localization  
→ localized frontier  
→ UQL-style update  
→ next operation

with ontology files unchanged.

No intelligence score is part of this gate.
