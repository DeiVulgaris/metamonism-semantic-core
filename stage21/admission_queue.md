# Stage 21 — Source Admission Queue

## Admission principle

This queue records source material that is semantically visible but was deliberately not promoted to a new `mm:*` construct during Stages 11–13.

A queue entry is **not** an ontology entity, claim, or relation.

| Candidate | Source status | Admission decision | Reason |
|---|---|---|---|
| Stb | USED_BUT_UNDEFINED | DEFER | Formal symbol not canonized in CORE |
| Sts | USED_BUT_UNDEFINED | DEFER | Formal symbol not canonized in CORE |
| Balance | USED_BUT_UNDEFINED | DEFER | Descriptive/model usage; no formal CORE object |
| Resolution (ontological) | USED_BUT_UNDEFINED | DEFER | CORE absence; UFCPS already has separate procedural construct |
| Global / Local | USED_BUT_UNDEFINED | DEFER | Not formal CORE levels |
| P0–P8 | USED_BUT_UNDEFINED | DEFER | Exists in UFCPS context with different semantics |
| Slice | USED_BUT_UNDEFINED | DEFER | Proposed in joint work; not established in corpus |
| Information / Inf | USED_BUT_UNDEFINED | DEFER | Conceptual usage exists; formal CORE symbol not canonized |

## Rule

No queue item receives an `mm:*` identity merely because it is useful or intuitively compatible.

Admission requires a source-backed construct registration decision in a later dedicated pass.
