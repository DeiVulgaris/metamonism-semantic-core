## Runtime handoff

The query plan is intended to be consumed by an information-space provider.

The provider returns retrieval envelopes.

The envelopes are then converted into evidence candidates and passed to the
semantic validation layer.

No external provider is hard-coded into the core.
