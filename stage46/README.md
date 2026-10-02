# Stage 46 — Invariant-Rooted Derivation

Stage 46 changes the reasoning architecture from locally initiated derivations to explicit derivation chains rooted in a registered invariant.

## Core rule

> No derived object may be used as a premise until its path from a registered invariant has been made explicit.

For the current Chapter 3 program:

`ban of absolute identity
→ necessary differentiation
→ necessary continuation
→ preservation of non-identity
→ non-redundant continuation
→ orthogonality constraint
→ D_perp
→ old-regime exhaustion
→ frustration
→ orthogonal resolution
→ P4
→ +n → -n`

The central edge

`non-redundant continuation → orthogonality`

remains a theoretical hypothesis and is deliberately exposed as the main research frontier.

## Files

- `invariant_rooted_derivation.md` — normative specification
- `invariant_derivation_state.json` — machine-readable derivation chain
- `invariant_derivation_test_vectors.yaml` — anti-collapse tests
- `invariant_derivation_validator.py` — validation logic
- `invariant_derivation_validation_report.md` — validation result

The global `AI_TEXT_PROCESSING_PROTOCOL.md` is also updated so rooted derivation applies to future research stages.

Canonical promotion remains false.
