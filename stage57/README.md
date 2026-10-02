# Stage 57 — Problem Decomposition and Task Generation

Stage 57 extends Stage 56 from one executable task candidate to a structured set of related task candidates.

The runtime path becomes:

semantic frontier
  -> root question
  -> task decomposition
  -> derived questions
  -> UFCPS discovery / claim / execution
  -> results
  -> frontier update

## Architectural rule

Decomposition is not free-form task invention.

A child task must be grounded in an explicit continuation-relevant difference supplied by the frontier or by a validated process result.

Supported decomposition bases in this stage are operational categories:

- unresolved_difference
- evidence_gap
- constraint_gap
- hypothesis_candidate
- contradiction
- resource_gap
- external_requirement

These categories are interface vocabulary, not new ontological entities of the semantic core.

## Root task

The root task is the current unresolved problem represented by the semantic frontier.

Root identity is inherited from the frontier question identity.

## Child tasks

Each child task preserves:

- parent question identity;
- source difference or gap;
- formulation;
- required next operation;
- inherited constraints;
- evidence references;
- provenance;
- task type;
- dependency information.

Child tasks are candidates. UFCPS discovery and agent decision remain separate.

## Derived-question bridge

A generated child can be emitted as a UFCPS UQL derived-question record:

parent_question_id -> child_question_id

This directly matches the UQL concept of a derived question without requiring the semantic core to depend on the UFCPS runtime implementation.

## No hidden optimization

Stage 57 does not assign:

- task priority;
- task value;
- a preferred agent;
- a preferred solution;
- a global ranking.

These remain outside the semantic decomposition layer.

## Example

Root:
Determine what information is sufficient to construct the next admissible continuation.

Explicit gaps:
- identify the missing boundary information;
- test whether a candidate distinction changes the admissible successor set;
- validate the resulting successor against the registered constraints.

Generated structure:

Root
|-- investigate missing boundary information
|-- investigate candidate distinction
    |-- validate candidate successor

The hierarchy expresses problem decomposition, not a claim that these tasks will succeed.

## Status

Stage 57 is an executable problem-decomposition layer and integration contract. It does not change the canonical semantic ontology.