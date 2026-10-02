# Stage 60 Test Matrix

The minimum runtime test matrix is:

1. classify FOUND by query intent;
2. classify NOT_FOUND as INFORMATION_GAP only for the information-gap query,
   otherwise as NO_ADEQUATE_INFO;
3. classify ERROR as RETRIEVAL_FAILURE even if provider metadata contains a
   contradictory declared class;
4. reject an unrooted reasoning chain;
5. reject a disconnected reasoning chain;
6. replay a valid chain from the explicit root invariant;
7. pass the classified result into the replay without rewriting the invariant.

The important invariant is:

information result
  -> classification
  -> replay from registered root invariant
  -> consequence / next operation

not:

information result
  -> replace reasoning root
