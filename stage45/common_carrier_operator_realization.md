# Common Carrier W — Operator Realization of Continuation and Regime Change

## Research question

Can the processual transition system be represented on one mathematical carrier without identifying the old and new regimes?

The purpose is not to prove that such a carrier is physically real. It is to test whether a mathematically coherent representation exists.

## 1. Minimal free carrier

Introduce a free vector space:

W = Span_F { |P_i,R> }

where each basis state retains both:

- processual position P_i;
- continuation regime R.

The regime label is therefore part of the basis identity.

This prevents the construction from silently identifying P3 in the old regime with P3 in another regime.

No metric is imposed on W.

No inner product is imposed.

No physical interpretation of W is assumed.

## 2. Ordinary continuation operators

For an admissible transition:

P_i --T_i--> P_{i+1}

define an operator on basis states:

T_i |P_i,R> = |P_{i+1},R>

when the transition is admissible.

Outside its explicitly defined domain, T_i is not yet assigned a value.

Thus T_i is naturally a partial linear operator.

## 3. Regime transition operator

For the exhaustion boundary:

P3 --J_R--> P4

define:

J_R |P3,R> = |P4,R'>

where R' is the new continuation regime.

The regime label is deliberately retained.

Therefore J_R is not an identification:

|P4,R'> = |P4,R>

unless an independent equivalence is later established.

## 4. What has been achieved

A common carrier W can represent both old-regime continuation and regime-changing transition without collapsing their distinction.

This answers the existence question positively at the level of a formal free construction.

It does NOT show that W is the natural physical state space.

## 5. Composition

Ordinary continuation composes when domains match:

T_2 T_1 |P1,R> = |P3,R>

and:

T_3 T_2 T_1 |P1,R> = |P4,R>

only if T_3 is an admissible continuation in the same regime.

But Chapter 3 says that the old external continuation is exhausted at P3.

Therefore the transition from P3 to P4 is represented by J_R, not by another old-regime T_3.

Hence the faithful composition is:

J_R T_2 T_1 |P1,R> = |P4,R'>

where defined.

The operator sequence itself records the change of regime.

## 6. J squared: the crucial distinction

The canonical object is a partial operator:

J_R : W_R^dom -> W_{R'}

with domain containing |P3,R>.

After one application:

J_R |P3,R> = |P4,R'>

A second application requires:

|P4,R'> ∈ dom(J_R)

The source does not establish this.

Therefore:

J_R^2 is **undefined**, not zero, not +I, and not -I.

## 7. Zero-extension is not a processual result

For computational purposes one may define an arbitrary total extension:

J_0 |x> = 0

outside dom(J).

Then J_0^2 may become zero on some states.

But this is an imposed extension convention.

It must never be interpreted as:

J^2 = 0

for the processual transition.

The semantic core therefore distinguishes:

- partial processual operator J;
- optional mathematical extension J_0.

Only the first is source-relevant.

## 8. Possible continuation after P4

To determine J^2 one would need a successor structure in the new regime.

For example, if a later transition gives:

P4 --J'--> P5

then the composition:

J' J_R |P3,R> = |P5,R''>

can be studied.

This is not the same operator square unless:

J' and J_R are independently identified.

That identification is currently unavailable.

## 9. Orientation transformation

The source gives:

+n -> -n

during the P3 -> P4 transition.

In the carrier representation this becomes a label transformation attached to J:

J_R : (P3,R,+n) -> (P4,R',-n)

The sign reversal is therefore encoded as part of the transition data.

It is not yet represented by multiplication by -1 on W.

That distinction is essential.

## 10. Operator algebra: current result

The formal carrier W supports composition of compatible partial operators.

However, the following are not yet derived:

- a closed algebra of all transitions;
- a multiplicative identity distinct from process-state identities;
- an involution;
- a bilinear form;
- anticommutation relations;
- Clifford relations.

The current structure is therefore an operator category / partial transition algebra candidate, not a Clifford algebra.

## 11. Minimal matrix representation

Once a finite subspace is selected, partial operators may be represented by matrices after a basis convention is fixed.

For example, on:

W_4 = Span{|P1,R>, |P2,R>, |P3,R>, |P4,R'>}

one can represent:

T_1 |P1,R> = |P2,R>
T_2 |P2,R> = |P3,R>
J_R |P3,R> = |P4,R'>

The resulting matrices are sparse transition matrices.

But their matrix form depends on the chosen basis and extension convention.

Matrix representation therefore does not add physical content by itself.

## 12. Consequence for Clifford research

The common carrier exists as a formal construction, but it does not yet generate a Clifford algebra.

The important object is now the distinction between:

1. same-regime continuation T;
2. exhaustion-boundary transition J;
3. subsequent transition J' in the new regime.

A possible algebraic structure must therefore be derived from relations among these operators.

The first nontrivial test is not:

"Does J look like a gamma matrix?"

It is:

"Do the processually required compositions and regime changes impose relations on the operators that cannot be removed by a basis change?"

## 13. Next tests

W-1: Define the smallest carrier containing P1-P4 with regime labels.

W-2: Build partial operators T1,T2,J.

W-3: Compute all domain-compatible compositions.

W-4: Determine whether any relation such as J'T = ±TJ follows from process constraints.

W-5: Introduce a bilinear form only if a process-derived reason exists.

W-6: Test whether any resulting operator relations imply a Clifford-type anticommutator.

## Status

Common carrier W: FORMALIZATION
Partial continuation operators T: FORMALIZATION
Regime transition J: FORMALIZATION
Zero extension J_0: MODELING CONVENTION
J²: UNRESOLVED / UNDEFINED
Clifford connection: THEORETICAL_HYPOTHESIS
Canonical promotion: FALSE

## Provenance

Primary source: Myshko, A. (2026), *МЕТАМОНИЗМ: Глава 3. Процессуальная онтодинамика*, Zenodo DOI 10.5281/zenodo.22730697, user-supplied source text, especially lines 34–90 and 93–120.
