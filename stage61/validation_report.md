# Stage 61 Validation Report

## Checks

- explicit affected step is required for causal localization;
- unknown affected step blocks rather than guessing;
- absent affected step uses only an explicit tail fallback;
- root invariant remains unchanged;
- reasoning prefix begins at the root and ends at the impact anchor;
- affected step receives validation/reconciliation status;
- downstream steps remain present and receive REQUIRES_REPLAY;
- next action is derived from the classified result class;
- provenance and original trace identity are preserved.

## Semantic boundary

Stage 61 identifies a procedural restart point. It does not prove that the
information caused the referenced step to fail.
