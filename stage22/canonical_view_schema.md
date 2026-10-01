# Stage 22 — Canonical View Schema

Top-level fields:

- `schema_version`
- `generated_from`
- `scope`
- `inventories.A/B/C`
- `cross_source.X1_X21`
- `formalizations`
- `provenance`
- `status_policy`

Each inventory contains:
- `entities`
- `claims`
- `relations`

Records are copied from source registries without semantic rewriting.

The canonical view is therefore a projection/aggregation, not a synthesis.
