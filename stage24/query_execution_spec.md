# Stage 24 — Semantic Query Execution

Stage 24 turns the registered Stage 18 query vocabulary into an executable, read-only dispatcher.

## Query classes

- Q1 Identity lookup
- Q2 Claim lookup
- Q3 Relation lookup
- Q4 Basis lookup
- Q5 Provenance lookup
- Q6 Formalization lookup
- Q7 Cross-source lookup
- Q8 Status audit
- Q9 Boundary query
- Q10 Operator query

## Result statuses

- RESOLVED — requested registered information is found.
- PARTIAL — some requested information is found, but the query scope is incomplete.
- UNRESOLVED — the source explicitly leaves the matter unresolved.
- EMPTY — no registered record matches.
- PROHIBITED_INFERENCE — answering would require a forbidden inference.

## Execution rule

The query layer reads registered data and returns evidence. It does not modify registries and does not register derived answers.

## Safety boundary

Queries asking whether A/B/C similarly named operators are identical, whether a model proves CORE, or whether missing edges imply independence return PROHIBITED_INFERENCE unless an explicit source relation exists.
