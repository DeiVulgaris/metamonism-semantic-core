# Stage 19 — Automated Integrity Specification

The validator checks structured registry data, not prose descriptions of rules.

Forbidden tokens mentioned in documentation as examples are not semantic relations.

Structured checks operate on relation IDs, relation subject/object/predicate/status/basis fields, registered IDs, X1-X21 records, f17 formalizations, and q18 query classes.

The validator is read-only and reports failures; it never repairs semantic data automatically.

A gate passes only when every ERROR rule passes.
