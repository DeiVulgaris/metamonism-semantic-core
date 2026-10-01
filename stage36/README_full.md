# Stage 36 — UFCPS Integration Decision

UFCPS has been analyzed as a companion architecture.

## Decision

**Selective integration.**

Reuse the process mechanisms that strengthen continuation of inquiry:

```text
UQL
Structured Deadlock
Question Evolution
Negative Results
Branching
Composition
Autonomous Research Loop
Append-oriented History
Carrier-independent Continuation
```

Keep runtime and material mechanisms outside semantic core:

```text
Swarm Runtime
Carrier Selection
Resource Accounting
Economic Settlement
Blockchain
Physical Infrastructure
```

## Resulting Architecture

```text
CANONICAL CORE
       ↓
RESEARCH PROGRAM
       ↓
RESEARCH TRAJECTORY
       ↓
RESEARCH FRONTIER
       ↓
PROCESS ENGINE
       ↓
NEXT ADMISSIBLE TRANSITION
       ↓
optional external UFCPS runtime
```

## Key finding

UFCPS already contains the conceptual distinction between an unresolved question,
its investigation state, and the continuing process. This strengthens Stage 33–35
without requiring wholesale import of UFCPS.

## Next architectural target

Implement `RESEARCH_FRONTIER` as the explicit boundary between established,
partially resolved, unresolved, blocked, conflicting, untested, and newly generated
research states.
