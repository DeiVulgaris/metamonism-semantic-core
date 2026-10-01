# Stage 23 — Controlled Semantic Reasoning

## Purpose

Permit bounded derivation from already registered semantic records.

This stage does **not** create new ontology. It creates explicitly marked derived answers.

## Allowed inference

A derived statement may be emitted only when:
1. all premises are registered records;
2. the relation predicates are explicitly registered;
3. the inference rule is declared in this stage;
4. no epistemic status is upgraded;
5. the conclusion is not an identity/equivalence claim unless that identity is itself registered.

## Initial rule set

### R1 — Relation chaining

If:
- A --r1--> B
- B --r2--> C

then emit:
- A --path(r1,r2)--> C

Status: DERIVED.

This is a path statement, not a new direct semantic relation.

### R2 — Basis propagation

If relation R has basis claim C, a query may return C as supporting provenance.

Status: DERIVED_FROM_SOURCE.

### R3 — Status preservation

Derived output inherits the strongest epistemic limitation of its premises.

It may never become stronger than its weakest premise.

### R4 — Namespace preservation

A/B/C scoped entities remain scoped after reasoning.

### R5 — No semantic collapse

No inference may convert:
- distinct_from → unrelated_to;
- similar operator names → identity;
- derived_from → proves;
- missing relation → independence;
- hypothesis → SOURCE;
- model → CORE.

## Explicitly forbidden

Transitive closure of arbitrary predicates is forbidden unless the predicate is explicitly declared transitive.

No causal inference from mere relation chaining.

No truth inference from formalization.

No mathematical equivalence from structural correspondence.
