# Stage 42 — Identity & Continuity Registry

Stage 41 exposed a concrete integration problem: the same intended research process can appear under different machine identifiers across stages or versions.

## Principle

> Process identity is not the same thing as an identifier string.

A changed identifier does not automatically create a new research program. Similar labels do not establish identity.

## Identity relations

- `IDENTITY_EQUIVALENCE`
- `ALIAS`
- `VERSION_CONTINUATION`
- `DERIVATION`
- `FORK`
- `MERGE`
- `UNRESOLVED_IDENTITY`

These are process-identity relations, not semantic relations.

## Assertion status

- `PROPOSED`
- `ASSERTED`
- `REJECTED`
- `UNRESOLVED`

An unresolved/proposed mapping cannot be consumed as established identity.

## Invariants

1. No silent identifier merge.
2. Asserted mappings require provenance and evidence.
3. Identity resolution never deletes original references.
4. Forks remain distinct research identities.
5. Version continuation preserves prior history.
6. Derivation creates a distinct identity.
7. Merge requires explicit evidence.
8. Ambiguous identity remains unresolved.
9. Identity mapping does not upgrade epistemic status.
10. Identity mapping does not establish theoretical equivalence.
11. Research identity is independent of AI/session/carrier identity.
12. Historical identifiers remain retrievable.

## Stage 41 continuity case

The following references occurred in different stages:

- `mm:rp.r1_r4_dirac`
- `RP-r1r4-dirac`

Stage 41 deliberately refused to merge them silently. Stage 42 records the continuity relation explicitly, with provenance and evidence.

## Operational rule

When an unknown identifier is encountered:

1. look up the registry;
2. use an asserted mapping if one exists;
3. preserve uncertainty for proposed/unresolved mappings;
4. create an unresolved identity observation when no mapping exists;
5. never guess a canonical identifier.

The registry controls identity continuity only. It does not establish truth, theoretical equivalence, formal isomorphism, or canonical promotion.
