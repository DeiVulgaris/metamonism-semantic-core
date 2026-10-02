# Stage 61 — Impact-Localized Frontier Rebuild

Stage 61 determines where a classified information result enters a registered
reasoning chain and rebuilds the next frontier from that point.

The key boundary is explicit attribution:

information result
  -> classified result
  -> explicit impact reference
  -> invariant-rooted replay prefix
  -> localized frontier
  -> next operation

The system does not infer causal impact from free text.

## Impact reference

A classification may carry an optional:

affected_step_id

This field must come from semantic validation or an equally explicit process
that identifies the affected reasoning step.

When it is absent, the engine may use an explicit procedural fallback:
the last step of the registered chain is reopened. The fallback is labelled
as such and is not treated as a causal claim.

## Localized rebuild

Given an affected step:

1. preserve the root invariant;
2. preserve every registered derivation step before the affected step;
3. mark the affected step for validation or reconciliation;
4. mark downstream steps as requiring replay;
5. create the next frontier at the affected step;
6. retain the complete provenance and original trace.

The frontier therefore resumes at the first known point of impact, while the
reasoning prefix still begins at the root invariant.

## No silent invalidation

A downstream step is not deleted or rewritten.

Its state becomes a procedural status such as:

REQUIRES_REPLAY

This preserves historical and semantic integrity.

## Status

Stage 61 is **CLOSED**. The stage is complete and frozen; further work belongs
to a new architectural stage.
