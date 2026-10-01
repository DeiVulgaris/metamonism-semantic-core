# Stage 25 — Structured Semantic Query Engine

Stage 25 extends the Stage 24 dispatcher with structured access to:

- Q5 provenance
- Q6 formalizations
- Q7 cross-source bridge X1-X21
- Q9 semantic boundaries

## Query contract

Input:
`QUERY_TYPE VALUE`

Output:
- `status`
- `results`
- optional `evidence`
- optional `boundary`

## Q5 Provenance

Returns provenance records whose registered source/subject/basis matches VALUE.

## Q6 Formalization

Returns Stage 17 formalizations matching a claim ID or formalization ID.

## Q7 Cross-source

Returns X1-X21 records matching an X identifier, inventory token, or referenced construct.

## Q9 Boundary

Returns explicit registered boundary statements for:
- operator identity;
- model→CORE;
- hypothesis promotion;
- missing-edge independence;
- cross-inventory inference.

## Boundary rule

A boundary query may return PROHIBITED_INFERENCE when the requested conclusion is not licensed by registered semantics.

No query result is registered as new `mm:*` semantics.
