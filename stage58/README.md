# Stage 58 — Information Space Bridge and Query Formation

Stage 58 inserts an information-retrieval layer before task decomposition/execution.

The canonical path becomes:

semantic frontier
  -> information need
  -> query plan
  -> information-space request
  -> retrieval
  -> evidence candidates
  -> semantic validation
  -> updated frontier
  -> task generation / execution

## Why this layer exists

An unresolved task must first be checked against the accessible information space.

The system should ask:

- Does a documented solution already exist?
- Does a method exist that addresses the unresolved difference?
- What evidence is already available?
- What contradictory evidence exists?
- What information is missing?
- What source would discriminate between remaining alternatives?

Only after this check should the system decide that a new task, experiment, or derivation is required.

## Information space

The information space is an abstract set of externally or internally accessible sources:

- web documents;
- scientific literature;
- books and archives;
- code repositories;
- datasets;
- standards and technical documentation;
- internal semantic corpora;
- domain databases.

The bridge is provider-neutral.

## Query intents

A query plan may contain one or more intents:

- SOLUTION_DISCOVERY
- METHOD_DISCOVERY
- EVIDENCE_DISCOVERY
- CONTRADICTION_CHECK
- INFORMATION_GAP
- PRECEDENT_DISCOVERY
- SOURCE_VALIDATION

These are operational query intents, not semantic entities of the ontology.

## Query formation

A query is derived from a structured frontier, not from the raw wording alone.

The planner uses:

current problem formulation
+ unresolved difference
+ constraints
+ known failed paths
+ evidence context
+ requested query intents

to produce a bounded set of queries.

## Information before action

The system therefore prefers:

frontier
  -> search existing knowledge
  -> classify what was found
  -> decide whether new execution is necessary

rather than:

frontier
  -> immediately generate a new task

## Evidence boundary

Retrieved material is not semantic truth.

The retrieval layer produces:

RETRIEVAL RESULT
    ->
EVIDENCE CANDIDATE
    ->
SEMANTIC VALIDATION
    ->
CLAIM / UPDATE

A source may be relevant without being correct. A search result may be weak,
conflicting, incomplete, or irrelevant.

## Query provenance

Each query preserves:

- source frontier;
- query intent;
- generated text;
- constraints;
- source classes;
- exclusions;
- generation mode.

Each retrieval result preserves:

- query identity;
- source identity;
- locator/reference;
- retrieved content or content reference;
- retrieval timestamp;
- source metadata.

## Design rule

> Search first when existing information may change the task definition.

This does not prohibit action when external information is unavailable or when
the task explicitly requires new observation/experiment.

## Status

Stage 58 is an executable query-planning and information-ingestion layer.
It does not change the canonical ontology or promote retrieved material to truth.
