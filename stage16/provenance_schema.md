# Stage 16 — Provenance Schema

A provenance record has the conceptual form:

```yaml
provenance:
  object_id: mm:...
  provenance_level: SOURCE_REGISTRATION | CLAIM_DERIVATION | CROSS_SOURCE_BRIDGE | FORMALIZATION | UNRESOLVED_PROVENANCE
  source_inventory: A | B | C | CORE | CROSS_SOURCE
  source_anchor: ...
  basis_claim: mm:...        # optional; required for CLAIM_DERIVATION
  bridge_id: X1              # required for CROSS_SOURCE_BRIDGE
  status: REGISTERED | UNRESOLVED
```

## Resolution rule

An object has **resolved provenance** when its source inventory/source anchor is known and every referenced basis claim or bridge ID resolves.

An object has **unresolved fine-grained provenance** when its source is known but the current registry does not preserve the exact source fragment/location.

This distinction is deliberate:

> known source ≠ known source location.

No finer provenance is inferred from terminology or memory.
