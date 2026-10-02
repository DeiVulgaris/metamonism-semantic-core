# Stage 60 — Information Classification and Invariant-Rooted Reasoning Replay

Stage 60 inserts a reasoning replay after information retrieval.

The retrieval layer may discover a solution, method, evidence, contradiction, or
information gap. None of these classifications is itself a semantic
conclusion.

The classified result is therefore fed back into the reasoning chain, which is
reconstructed from the registered root invariant.

## Canonical path

semantic frontier
  -> query plan
  -> retrieval
  -> result classification
  -> invariant-rooted reasoning replay
  -> updated derivation state
  -> next frontier / task formation

## Classification boundary

The classifier uses operational facts already present in the retrieval
contract:

- retrieval status;
- query intent;
- optional provider-declared result class.

It does not infer truth from snippets or content.

Result classes:

- SOLUTION_FOUND
- METHOD_FOUND
- EVIDENCE_FOUND
- CONTRADICTION_FOUND
- INFORMATION_GAP
- NO_ADEQUATE_INFO
- RETRIEVAL_FAILURE

## Reasoning replay

The replay requires an explicit chain specification:

root invariant
  -> registered derivation steps
  -> information checkpoint
  -> classified result
  -> consequence / required operation
  -> resulting reasoning state

The engine never creates a missing derivation rule. Every step must be supplied
with its relation, premises, status, and provenance.

This makes the replay a reconstruction of an existing reasoning program rather
than free-form inference.

## Meta-Monism core example

The included vectors use the source-grounded sequence already registered in the
project:

Ban of Indifference
  -> Dissipation
  -> Space / Time
  -> Ray
  -> Orthogonal Resolution
  -> Continuation

The engine does not upgrade these steps to stronger logical status. Their
epistemic status remains whatever the chain specification declares.

## Important distinction

A contradiction discovered in information space does not mean that the root
invariant is false.

It means that one or more downstream steps, interpretations, or applications
must be reconciled or tested.

Likewise, failure to retrieve information is not evidence that no information
exists.

## Status

Stage 60 is an executable semantic/process integration layer. It does not add a
new canonical ontology claim.
