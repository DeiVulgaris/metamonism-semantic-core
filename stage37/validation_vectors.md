# Stage 37 Validation Vectors

V1 Established source — PASS: SOURCE + ESTABLISHED + complete provenance.

V2 Untested hypothesis — PASS: THEORETICAL_HYPOTHESIS + UNTESTED + derived_from.

V3 Blocked question — PASS: BLOCKED + non-empty blockers + no automatic termination.

V4 Conflict — PASS: CONFLICTING + explicit relations and preserved provenance.

V5 Missing provenance — FAIL: source-grounded item lacks repository/path/ref/locator.

V6 Missing derivation path — FAIL: non-SOURCE status without derived_from.

V7 Unresolved is allowed — PASS: UNRESOLVED remains a valid frontier state.

V8 Blocked is not terminated — PASS: BLOCKED cannot automatically make TERMINATE AVAILABLE.

V9 R1-R4 / Dirac — PASS: structural correspondence remains a hypothesis; formal isomorphism remains unresolved.

V10 Ricci / Planck — PASS: structural correspondence remains a hypothesis; Planck-scale relation remains unresolved and dimensional correction is retained as validation information.