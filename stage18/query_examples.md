# Stage 18 — Query Examples

- `claims(inventory=B, status=RESEARCH_HYPOTHESIS)` → seven registered B research hypotheses.
- `formalization(claim=mm:b.clm.continuity_is_valid_transition)` → `f17:b.continuity_transition`.
- `bridge(X12)` → registered B/CORE bridge, status RESEARCH_HYPOTHESIS.
- `basis(relation=mm:b.rel.continuity_not_same_carrier)` → `mm:b.clm.process_continuity_not_same_carrier`.
- `provenance(mm:b.clm.continuity_is_valid_transition)` → source B known; finer-grained location unresolved.
- Comparing `diff` across A/B is PROHIBITED_INFERENCE for identity/isomorphism; return separate scoped records.

The query layer retrieves registered evidence and does not infer identity, independence, truth, proof, or causal necessity.
