# D3 Revision — Exhaustion of Available External Degrees of Freedom

## Purpose

The earlier D3 treated `+n -> -n` as an ordinary linear reversal on a fixed vector space. Chapter 3 indicates a different causal order: after the available external orthogonal directions are exhausted, continuation by the previous method becomes impossible, producing frustration and a regime transition.

The earlier D3 is preserved as historical work; this revision changes the primary research direction.

## Source-grounded basis

Chapter 3 states that after three external orthogonal directions, further external orthogonal unfolding is exhausted. Continuation nevertheless remains necessary. The source defines frustration as necessity of continuation plus impossibility of completion by the previous method. It also states that P4 is not a fourth spatial dimension and that the transition includes `+n -> -n`.

## Minimal formalization

Define the admissible external continuation set:

`D_ext(P) = { d | d is an admissible external orthogonal continuation from P under the current regime }`

The source-grounded condition is formalized as:

`D_ext(P3) = empty_set`

Define exhaustion:

`Exh(P) := D_ext(P) = empty_set`

and frustration:

`Fr(P) := NeedContinue(P) AND Exh(P)`

These formulas are formalizations of source content, not quotations of source notation.

## Working rank model

If `D_ext(P)` later receives a vector-space structure, one may define `r_ext(P) = dim D_ext(P)`. A minimal working model is:

`r_ext(P0)=3, r_ext(P1)=2, r_ext(P2)=1, r_ext(P3)=0`

This numerical assignment is a proposal, not a source theorem. The source supports exhaustion after three external orthogonal directions but does not provide this rank function.

P4 is not assigned a negative rank. It belongs to a new continuation regime.

## Regime transition

Introduce a transition rather than an already-defined linear operator:

`J : (P3, Fr, Regime_old) -> (P4, Regime_new)`

with orientation update:

`n_new = -n_old`

At this stage `J^2` is undefined. Neither `J^2=+I` nor `J^2=-I` may be imported from analogy.

## Revised D3 order

`external continuation structure -> exhaustion -> frustration -> regime transition -> orientation reversal -> candidate state-space structure -> bilinear form -> operator algebra`

This preserves the causal order stated by the source and prevents a metric from being imposed before the process that motivates the reversal has been formalized.

## Consequence for the Dirac/Clifford program

P1-P4 cannot currently be identified with four independent Clifford generators. P4 is produced by exhaustion and regime transition rather than by adding an independent fourth external direction.

A weaker research question remains admissible: can the algebra of processual transitions, including exhaustion and regime-change operators, admit a representation containing a Clifford/Dirac sector? This remains a theoretical hypothesis and is not a derivation of Clifford algebra or Dirac matrices.

## Status

- Source basis: `SOURCE`
- Exhaustion formalization: `FORMALIZATION`
- Rank model: `PROPOSAL`
- Regime transition J: `PROPOSAL`
- Clifford/Dirac connection: `THEORETICAL_HYPOTHESIS`
- Canonical promotion: `FALSE`

## Provenance

Myshko, A. (2026), *МЕТАМОНИЗМ: Глава 3. Процессуальная онтодинамика*, Zenodo, DOI `10.5281/zenodo.22730697`, user-supplied source text, lines 34-90 and 93-120.