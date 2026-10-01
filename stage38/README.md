# Stage 38 — Frontier → Research Task Engine

Stage 38 connects the Research Frontier to explicit, machine-readable research tasks.

The key distinction:
- FRONTIER = what remains unresolved.
- TRANSITION = what operation is structurally admissible.
- RESEARCH_TASK = a concrete research obligation instantiated from that transition.

The engine does not decide truth and does not perform research. It derives candidate tasks while preserving provenance, blockers, epistemic status, and uncertainty.

Architecture:
CANONICAL CORE → RESEARCH PROGRAM → RESEARCH TRAJECTORY → RESEARCH FRONTIER → ADMISSIBLE TRANSITIONS → RESEARCH TASKS → EXTERNAL SELECTION → EXECUTION → RESULT / DEADLOCK / DIFFERENCE → TRAJECTORY + FRONTIER UPDATE

Selection is deliberately separated from generation. The engine may return several admissible tasks; another policy may choose one.

Core invariants:
- A task must originate from a frontier item.
- A task cannot upgrade epistemic status.
- A task cannot silently resolve its own target.
- A blocked frontier cannot generate an automatically executable task.
- Contradiction generates comparison/branching work, not silent reconciliation.
- Negative results remain research information.
- Task identity is not research truth.
- Execution result must return to trajectory/frontier state.
