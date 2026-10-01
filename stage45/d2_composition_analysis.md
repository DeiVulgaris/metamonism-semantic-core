# D2 — Composition Analysis

## Result

The most conservative composition supplied by the processual sequence is **composition of transitions**, not multiplication of processual states.

Write:

P0 --T0--> P1 --T1--> P2 --T2--> P3 --T3--> P4.

Then:

T1 ∘ T0 : P0 -> P2
T2 ∘ T1 : P1 -> P3
T3 ∘ T2 : P2 -> P4

and, where domains/codomains match,

T2 ∘ T1 ∘ T0 : P0 -> P3.

This composition is defined by succession of compatible transitions.

## Important distinction

The relation P_i -> P_{i+1} does not itself provide a binary product P_i P_j.

Therefore no Clifford-like multiplication is obtained at D2.

The natural structure at this stage is a **path/transition composition structure**.

If transitions are represented as partial maps, ordinary composition is associative whenever defined. This associativity comes from composition of maps, not from Clifford algebra.

## Orientation reversal

Introduce R only as a transformation acting on the relevant orientation datum:

R(n) = -n.

The source does not establish that R maps a processual state P_i to another processual state by ordinary multiplication.

Thus the safe distinction is:

- T_i: processual transition;
- R: orientation transformation;
- P_i: processual state;
- n: directional/orientation datum.

The expression R ∘ T3 is meaningful only after a common carrier and compatible domains are defined.

## What D2 establishes

D2 establishes a candidate composition mechanism:

Hom(P_i,P_j) × Hom(P_j,P_k) -> Hom(P_i,P_k).

This is categorical/path-like structure.

It does **not** yet establish an algebra because we do not have:

1. a common carrier for all transitions;
2. a closed binary operation on a single set of elements;
3. a scalar field or additive structure;
4. an identity element in the required algebraic sense;
5. a bilinear product.

## Consequence for the Dirac hypothesis

The first natural formalization therefore changes the target question.

Instead of asking:

"Do P1-P4 multiply like gamma matrices?"

ask:

"Can the transition/orientation structure be represented by operators on one common carrier, and if so, does the resulting operator algebra contain a Clifford substructure?"

This preserves the source distinction between processual states and algebraic operations.

## D2 status

PARTIALLY_RESOLVED

Resolved:

- a source-faithful composition notion exists;
- composition is sequential transition composition;
- associativity can be inherited from map composition.

Unresolved:

- common carrier;
- total versus partial operators;
- identity operator;
- additive/scalar structure;
- composition law involving R;
- whether an algebraic closure exists.

## Next dependency

D3 should not begin by choosing a Minkowski metric.

The next task is to determine whether the processual structure itself supplies enough information to construct a bilinear/quadratic relation on the common carrier.

If not, the metric must be explicitly marked as an external modelling assumption.
