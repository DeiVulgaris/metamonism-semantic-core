# Stage 59 — Information Provider Runtime Contract

Stage 59 formalizes the runtime boundary between Semantic Core query planning
and the external information space.

Stage 58 forms provider-neutral queries. Stage 59 defines how those queries are
dispatched, how provider results are normalized, and how the results return to
the Semantic Core/UFCPS boundary.

## Canonical runtime path

semantic frontier
  -> query plan
  -> provider request
  -> provider
  -> raw result
  -> normalized retrieval envelope
  -> semantic validation
  -> frontier update
  -> task formation / execution

## Provider neutrality

The Semantic Core does not contain a vendor-specific search API.

A provider is selected by source class, for example:

- web;
- literature;
- code_repository;
- dataset;
- internal_corpus.

The provider implementation is an integration concern. The semantic contract
only requires that request identity, source provenance, locator, retrieval
status, and content/reference information survive the round trip.

## Runtime rules

1. Every prepared query has a stable query identity.
2. Every provider result retains the originating query identity.
3. Missing providers are explicit runtime errors, not silent omissions.
4. Provider exceptions become ERROR retrievals rather than process termination.
5. An empty successful search becomes NOT_FOUND.
6. Only FOUND/PARTIAL retrievals may become evidence references through the
   existing ingestion boundary.
7. Retrieval does not establish semantic truth.
8. Repeated retrievals are deduplicated by query/provider/locator identity.
9. Provider timestamps and provenance are retained as runtime metadata.
10. No agent assignment or task completion decision occurs in this layer.

## Stage boundary

Stage 59 therefore closes the previously abstract gap:

query plan
  -> dispatch
  -> retrieval
  -> ingestion

The contract remains reusable whether the provider is a local corpus, a
literature service, a repository index, or an HTTP API.

## Status

Stage 59 is an executable integration/runtime contract. It does not change the
canonical ontology.
