# Stage 51 — Logical Continuation Core

## Purpose
Semantic extraction records what the source states. This stage adds the minimal logical layer needed to determine what follows from registered premises under registered rules.

> Semantics tells the system what the source gives it. Logic tells the system what may be concluded from what it has been given.

## 1. Atomic propositions
Represent a proposition as Atom(predicate, arguments). Examples:
- Actualized(A_n)
- InDomain(P,A_n)
- NonIdentity(D_n,I_n)
- NeedContinue(A_n)
- CurrentModeExhausted(A_n)
- OrthogonalResolutionRequired(A_n)
- NextArgument(F(R_n),A_{n+1})

Names do not make propositions true. A proposition enters a proof only as source evidence or as the conclusion of a registered rule.

## 2. Rule object
A logical rule is:
Rule = (rule_id, premises, conclusion, provenance, status)

Rules are explicit. The engine never invents missing premises.

## 3. Chapter 1 rules
### L1 — Domain non-identity
NonIdentity(D,I) -> InDomain(P,(D,I))

### L2 — Nontrivial actualization
InDomain(P,A) -> NonTrivialResult(P,A)

These are formalizations of the Chapter 1 operator/domain construction.

## 4. Chapter 2 continuation rules
### L3 — Result to next argument
Actualized(R_n) AND Continue(R_n) -> ExistsNextArgument(A_{n+1})

Chapter 2 explicitly describes the sequence:
(D_n,I_n) -> R_n -> (D_{n+1},I_{n+1}) -> R_{n+1}.

### L4 — Continuation re-enters the domain
ExistsNextArgument(A_{n+1}) -> InDomain(P,A_{n+1})

Together L3 and L4 express the requirement that a continuing nontrivial trajectory produce a new argument state from which the operator can act again.

### L5 — Exhaustion triggers orthogonal resolution
CurrentModeExhausted(A_n) AND NeedContinue(A_n) -> OrthogonalResolutionRequired(A_n)

This is a source-grounded Chapter 2 process rule. It is not replaced by an arbitrary transition rule.

## 5. Operator-first sequence
The minimal continuing sequence is:

A_n
  -> P
R_n
  -> F
A_{n+1}
  -> P
R_{n+1}

The logic layer controls the arrows; it does not redefine the semantic objects.

## 6. Proof objects
Every derived proposition must preserve:
- conclusion;
- premises;
- rule_id;
- rule status;
- rule provenance;
- ancestor path to the root when the proposition belongs to a rooted derivation.

Proof status vocabulary:
- PROVED_WITH_REGISTERED_RULES
- CONDITIONALLY_DERIVED
- BLOCKED
- UNRESOLVED

PROVED_WITH_REGISTERED_RULES means that the registered rule system derives the proposition. It does not mean physical truth or empirical confirmation.

## 7. Scope
The engine reasons over registered actualization propositions and trajectories.
It does not globalize a local domain condition.

Invalid:
A_n outside Dom(P) -> every configuration in D is impossible.

Valid:
A_n outside Dom(P) -> the current argument cannot produce a nontrivial result through P.

## 8. Downstream geometry
Geometry is not a primitive input to this logical layer.
The dependency remains:

root invariant
-> actualization-domain condition
-> actualization
-> continuation
-> distinguishable successor
-> directionality
-> current-mode exhaustion
-> orthogonal resolution
-> geometry
-> operator representation
-> algebra.

D_perp is therefore downstream of the actualization/continuation chain.

## 9. Anti-inflation rules
Reject:
- deriving orthogonal resolution directly from the root without the registered intermediate chain;
- inserting a metric to manufacture orthogonality;
- treating P as a geometric or physical force without evidence;
- treating F as a new fundamental invariant;
- equating result R_n with next argument A_{n+1};
- treating logical derivability as empirical truth;
- treating a semantic record as a proof.

## 10. Current frontier
The open mathematical question is:

What is the minimal formal structure of F such that repeated applications of P remain nontrivial and inside Dom(P), without introducing a new foundational invariant or pre-imposing geometry?

Canonical promotion: FALSE.