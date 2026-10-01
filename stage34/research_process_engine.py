"""Stage 34 — Research Process Engine.

The engine does not solve a research program. It computes the next admissible
research action from the program's explicit state.

Design rule:
    state -> blocker/question/test -> admissible transition

No transition may manufacture evidence, definitions, identity, equivalence,
or canonical status.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Transition:
    action: str
    reason: str
    requires: List[str]
    produces: str
    priority: int


def _blocking_definitions(program: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [d for d in program.get("required_definitions", []) if d.get("blocking")]


def _open_tests(program: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [t for t in program.get("tests", []) if t.get("status") in {"OPEN", "READY"}]


def _failed_tests(program: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [t for t in program.get("tests", []) if t.get("status") in {"FAILED", "FALSIFIED"}]


def _open_questions(program: Dict[str, Any]) -> List[str]:
    return list(program.get("open_questions", []))


def propose_next_transitions(program: Dict[str, Any]) -> List[Transition]:
    """Return admissible next actions, ordered by priority.

    The engine deliberately returns actions, not conclusions.
    """
    transitions: List[Transition] = []
    blockers = _blocking_definitions(program)
    tests = _open_tests(program)
    failed = _failed_tests(program)
    questions = _open_questions(program)

    if blockers:
        transitions.append(Transition(
            action="DEFINE_BLOCKER",
            reason="A blocking definition is missing.",
            requires=[d["term"] for d in blockers],
            produces="A candidate definition or an explicit decision to leave the term unresolved.",
            priority=100,
        ))

    if not blockers and tests:
        transitions.append(Transition(
            action="RUN_TEST",
            reason="The program has a test whose prerequisites are not blocked.",
            requires=[t["id"] for t in tests],
            produces="Observed result, preserved as SOURCE/INFERENCE/UNRESOLVED according to evidence.",
            priority=90,
        ))

    if failed:
        transitions.append(Transition(
            action="ANALYZE_FAILURE",
            reason="A previous test failed or was falsified.",
            requires=[t["id"] for t in failed],
            produces="Failure reason, revised constraint, and a possible next test.",
            priority=95,
        ))

    if questions and not blockers:
        transitions.append(Transition(
            action="REFINE_QUESTION",
            reason="Open questions remain after current constraints are explicit.",
            requires=questions,
            produces="A narrower or decomposed research question.",
            priority=70,
        ))

    if not blockers and not tests and questions:
        transitions.append(Transition(
            action="DESIGN_TEST",
            reason="An open question has no registered test.",
            requires=questions,
            produces="A test with expected observation and falsifier.",
            priority=80,
        ))

    if not transitions:
        transitions.append(Transition(
            action="REVIEW_STATE",
            reason="No automatic transition is admissible.",
            requires=[],
            produces="Human/AI review of the research state without promotion.",
            priority=10,
        ))

    return sorted(transitions, key=lambda t: t.priority, reverse=True)


def next_transition(program: Dict[str, Any]) -> Dict[str, Any]:
    candidates = propose_next_transitions(program)
    chosen = candidates[0]
    return {
        "action": chosen.action,
        "reason": chosen.reason,
        "requires": chosen.requires,
        "produces": chosen.produces,
        "priority": chosen.priority,
        "alternatives": [
            {
                "action": t.action,
                "reason": t.reason,
                "priority": t.priority,
            }
            for t in candidates[1:]
        ],
        "canonical_promotion": False,
    }


if __name__ == "__main__":
    import yaml
    from pathlib import Path

    programs = yaml.safe_load(
        (Path(__file__).parent / "research_programs.yaml").read_text(encoding="utf-8")
    )["programs"]

    for program in programs:
        print(program["id"])
        print(next_transition(program))
