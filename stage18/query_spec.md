# Stage 18 — Semantic Query Specification

## Purpose

Provide a controlled query vocabulary over the registered semantic core.

Queries retrieve registered information. They do not silently infer identity, truth, equivalence, independence, or causal necessity.

## Query classes

### Q1 — Identity lookup

Input:
`mm:ID`

Returns:
- canonical registration;
- inventory;
- category/type;
- status;
- provenance anchor when available;
- linked claim/relation/formalization records when registered.

### Q2 — Claim lookup

`claims(status=...)`
`claims(inventory=...)`
`claims(category=...)`
`claims(term=...)`

Returns only registered claims matching the explicit filter.

### Q3 — Relation lookup

`relations(subject=...)`
`relations(object=...)`
`relations(predicate=...)`
`relations(status=...)`

Returns registered relation records.

### Q4 — Basis lookup

`basis(relation=mm:...)`

Returns the registered `basis_claim`, if one exists.

No basis claim is inferred when the field is absent.

### Q5 — Provenance lookup

`provenance(mm:ID)`

Returns the strongest provenance level actually registered.

Known source does not imply known line/page location.

### Q6 — Formalization lookup

`formalization(claim=mm:...)`

Returns Stage 17 formalizations explicitly linked to that claim.

### Q7 — Cross-source lookup

`bridge(Xn)`
`bridge(inventory=A|B|C)`

Returns only Stage 10 X1–X21 records.

Stage 8 analogies are not queryable as relations.

### Q8 — Status audit

`audit(status=...)`

Returns claims/relations/formalizations carrying the requested status.

### Q9 — Boundary query

`boundaries(inventory=...)`

Returns registered epistemic-boundary claims and related records.

### Q10 — Operator query

`operator(inventory=A|B|C, name=...)`

Returns the inventory-scoped operator records.

A matching name across inventories is not an identity result.

## Explicitly prohibited query semantics

The query layer must not answer the following by inference:

- "Are A and B identical?"
- "Does missing relation mean independent?"
- "Does model X prove CORE?"
- "Does hypothesis H become true because it has a formalization?"
- "Are similarly named operators isomorphic?"
- "Does relation chain imply an unstated causal law?"

Such questions may return registered evidence and an `UNRESOLVED` result where appropriate.

## Result statuses

- `RESOLVED` — directly answerable from registered data.
- `PARTIAL` — some requested fields are registered, others are absent.
- `UNRESOLVED` — the repository does not contain enough registered information.
- `EMPTY` — no matching registered record.
- `PROHIBITED_INFERENCE` — answering would require an unsupported inference.

## Query principle

> Retrieval is allowed. Silent semantic invention is not.
