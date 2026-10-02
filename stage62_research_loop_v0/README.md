# Research Loop v0 — Next-Operation Policy + Derived Question

## Status

**DRAFT → IMPLEMENTED v0.1.0**

This stage adds the first operational autonomy layer on top of the frozen
Stage 55–61 continuity contour.

The policy chooses a process transition. It does not author semantic meaning.

> **Policy = transition chooser, not meaning author.**

## Boundary

Input:

`frontier state = UQL + impact + classification`

Output:

`next_operation ∈ allowed enum`  
`± derived_question` with provenance

The module does **not**:

- write ontology registries;
- write `claim_registry`;
- elevate `SOLUTION_FOUND` into a validated claim;
- infer `affected_step_id` from free text;
- erase or rewrite reasoning history;
- terminate because retrieval failed once.

The policy implementation is pure. A future UQL adapter may persist its output,
but persistence is deliberately outside this policy module.

## Allowed operations

- `diff`
- `fix`
- `diss`
- `unfold`
- `delegate`
- `compose`
- `terminate`

R0 currently selects only `diff`, `fix`, `delegate`, or `terminate`.
The remaining operations are part of the allowed vocabulary and become
relevant when later policy rules are introduced.

## Deterministic policy

Priority begins with an explicit budget guard.

| Rule | Result class | Operation | Derived question |
|---|---|---|---|
| R-BUDGET-STOP | `budget.exhausted=true` | `terminate` | no |
| R-CONTRACTION | `CONTRADICTION_FOUND` | `diff` | yes |
| R-EVIDENCE | `EVIDENCE_FOUND` | `fix` | no |
| R-METHOD | `METHOD_FOUND` | `fix` | no |
| R-SOLUTION-CANDIDATE | `SOLUTION_FOUND` | `fix` | no |
| R-GAP | `INFORMATION_GAP` | `diff` | yes |
| R-NO-ADEQUATE | `NO_ADEQUATE_INFO` | `diff` | yes |
| R-RETRIEVAL-FAIL | `RETRIEVAL_FAILURE` | `delegate` | no |
| R-DEFAULT | other | `diff` | no |

The budget guard is evaluated before result classification. This is required by
test vector R0-07 and prevents the ordering ambiguity in the draft contract.

The Stage 61 `next_required_operation_hint` remains advisory and cannot
override the deterministic table.

## Derived question

When emitted, the derived question remains an open process object:

`parent question → affected step → trigger → unresolved difference
→ derivation basis → inherited constraints`

The generated identifier is deterministic:

`q:derived:{parent_slug}:{anchor_step_id}:{trigger_slug}`

The key invariant is:

> **Emitting a derived question does not assert truth of the parent hypothesis
> or of the information result.**

## Test suite

R0-01…R0-07 are aligned with E2E-01…E2E-06 plus the explicit budget-stop case.

The suite checks:

- operation belongs to allowed vocabulary;
- `question_id` is preserved;
- ontology and registry files remain byte-identical;
- `ontology_write=false`;
- `claim_elevate=false`;
- `SOLUTION_FOUND` is never elevated by policy alone;
- `RETRIEVAL_FAILURE` does not terminate unless budget exhaustion is explicit;
- derived questions contain provenance and remain `OPEN`;
- identical input produces identical output.

Run:

`python stage62_research_loop_v0/test_research_loop_v0.py`

Expected:

`RESEARCH LOOP V0: PASS`

## Autonomy ladder

`E2E 61` — continue the process  
`R0` — select admissible next operation (+ optional derived question)  
`R1` — multi-step derived questions + UQL branch identity  
`R2` — branching frontier / compose  
Later — general research agent? **not claimed**  
AGI — **UNRESOLVED by design**

## No ontology expansion

No ontology identifier, operator merge, `sameAs`, `implements`, or registry
entry is added by this stage.
