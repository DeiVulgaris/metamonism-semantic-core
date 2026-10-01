# Stage 31 — Multi-Corpus Protocol Validation Report

## Scope

Stage 30 is tested against three heterogeneous corpus classes from the pinned Metamonism repository snapshot:

1. **Philosophical/theoretical:** `CORE/core_v1.2.md`
2. **Formal/theoretical:** `CORE/axioms.yaml`
3. **Physical hypothesis/model:** `ONTODYNAMICS/COSMOLOGY/cold_nucleogenesis_in_voids.yaml`

All three are pinned to commit `9f107f36b1a18633261e9666b32a59340c5f345d`.

## Validation matrix

| Requirement | Philosophical | Formal | Physical model |
|---|---:|---:|---:|
| Atomic extraction | PASS | PASS | PASS |
| Entity / claim / relation separation | PASS | PASS | PASS |
| Machine-readable provenance | PASS | PASS | PASS |
| Source wording vs interpretation | PASS | PASS | PASS |
| Epistemic status preservation | PASS | PASS | PASS |
| Formalization does not upgrade status | N/A | PASS | PASS |
| Model-specific boundary | N/A | PASS | PASS |
| Cross-layer transfer blocked | PASS | PASS | PASS |
| Contradiction preserved | N/A | PASS | PASS |
| Derived-from traceability | PASS | PASS | PASS |
| Unresolved result permitted | PASS | PASS | PASS |

## Critical observations

### 1. The protocol survives a change of representation

The philosophical case is prose-first, the formal case is YAML-first, and the physical case is a structured model containing claims, predictions, derivations, and explicit contradictions.

The same control logic remains applicable. This is important because the protocol is intended to control an AI processing pipeline, not merely annotate prose.

### 2. The formal case exposes a necessary distinction

A source-supplied formula can be `SOURCE` while an AI's judgment about the mathematical validity of that formula is not automatically `SOURCE`.

Therefore:

`source_claim` ≠ `source_claim_as_interpreted`.

This directly validates the provenance tightening introduced in Stage 30.

### 3. The physical-model case exposes epistemic inflation risk

The source labels the document and several structures as canonical within the repository, while also making observational predictions and model-internal necessity claims.

The protocol must preserve the distinction:

`repository status` ≠ `external scientific confirmation`.

Likewise:

`model-internal necessity` ≠ `universally established physical necessity`.

### 4. Contradictions must remain typed data

The physical case explicitly contains a `CONTRADICTS` relation to Big Bang nucleosynthesis. The protocol therefore must record the relation without converting it into a verdict about which theory is correct.

### 5. Provenance is operational, not editorial

Every benchmark record has:

- repository;
- exact path;
- pinned ref;
- semantic locator.

A record without these fields fails validation.

## Result

**Stage 31: PASS**

The protocol demonstrates cross-corpus stability across three materially different source forms.

The test does **not** establish the truth of the underlying Meta-Monism claims. It establishes that the processing protocol can represent source claims, model claims, formal expressions, relations, and uncertainty without automatically upgrading or collapsing them.

## Next architectural requirement

The protocol is now sufficiently specified to justify a machine-readable **processing-record schema**. The next stage should convert the Output Contract into a strict JSON/YAML schema so an AI implementation can produce records that a validator can reject when provenance, status, relation typing, or derivation paths are missing.
