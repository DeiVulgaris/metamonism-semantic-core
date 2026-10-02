#!/usr/bin/env python3
"""Stage 56: convert a semantic frontier into UFCPS runtime objects."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

VALID_OPERATIONS = {
    "diff", "fix", "diss", "unfold", "delegate", "compose",
    "investigate", "experiment", "formalize", "validate",
    "request_resources", "terminate",
}


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [text(value)] if text(value) else []
    if not isinstance(value, list):
        return []
    return [text(v) for v in value if text(v)]


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def validate_frontier(frontier: Mapping[str, Any]) -> list[str]:
    blockers = []
    for key in (
        "frontier_id", "question_id", "state",
        "epistemic_status", "formulation", "unresolved_difference"
    ):
        if not text(frontier.get(key)):
            blockers.append(f"{key}_missing")

    operation = text(frontier.get("next_required_operation")).lower()
    if operation not in VALID_OPERATIONS:
        blockers.append("next_required_operation_invalid")

    provenance = mapping(frontier.get("provenance"))
    for key in ("source_repository", "source_reference", "derivation_mode"):
        if not text(provenance.get(key)):
            blockers.append(f"provenance_{key}_missing")

    return blockers


def build_question(frontier: Mapping[str, Any]) -> dict[str, Any]:
    operation = text(frontier["next_required_operation"]).lower()
    return {
        "question_id": text(frontier["question_id"]),
        "formulation": text(frontier["formulation"]),
        "status": "unresolved",
        "current_state": text(frontier["state"]),
        "current_frontier": text(frontier["state"]),
        "unresolved_difference": text(frontier["unresolved_difference"]),
        "known_constraints": string_list(frontier.get("constraints")),
        "previous_attempts": string_list(frontier.get("failed_paths")),
        "attempted_operations": string_list(frontier.get("attempted_operations")),
        "next_required_operation": operation,
        "evidence_references": string_list(frontier.get("evidence_refs")),
        "required_capabilities": string_list(frontier.get("required_capabilities")),
        "requirements": {
            "resources": list(frontier.get("required_resources", []))
            if isinstance(frontier.get("required_resources", []), list) else []
        },
        "available_budget_rc": frontier.get("available_budget_rc", 0),
        "prospect_signals": dict(frontier.get("prospect_signals", {}))
        if isinstance(frontier.get("prospect_signals", {}), Mapping) else {},
        "continuation": {
            "required": True,
            "unresolved_difference": text(frontier["unresolved_difference"]),
            "next_required_operation": operation,
        },
        "provenance": dict(mapping(frontier.get("provenance"))),
    }


def build_procedural_state(
    frontier: Mapping[str, Any], carrier_id: str = "unassigned"
) -> dict[str, Any]:
    constraints = string_list(frontier.get("constraints"))
    failed_paths = string_list(frontier.get("failed_paths"))
    difference = text(frontier["unresolved_difference"])
    operation = text(frontier["next_required_operation"]).lower()
    step_index = int(frontier.get("step_index", 0))
    boundary = text(frontier.get("boundary"))
    deadlock_present = bool(failed_paths or boundary)

    preserved_repr = {
        "frontier_id": text(frontier["frontier_id"]),
        "epistemic_status": text(frontier["epistemic_status"]),
        "constraints": constraints,
        "evidence_refs": string_list(frontier.get("evidence_refs")),
        "failed_paths": failed_paths,
    }

    return {
        "procedural_unit": {
            "step_index": step_index,
            "unit_id": f"PU-{text(frontier['frontier_id'])}",
            "carrier": {
                "carrier_id": carrier_id,
                "carrier_type": "ufcps-adapter",
                "role": "task-carrier",
            },
            "session_status": "active",
        },
        "task_state": {
            "task": text(frontier["formulation"]),
            "current_state": text(frontier["state"]),
            "local_result": text(frontier.get("local_result")),
            "result_status": text(frontier.get("result_status", "none")) or "none",
        },
        "structural_difference": {
            "identified": True,
            "description": difference,
            "source": text(frontier.get("difference_source", "boundary")) or "boundary",
            "relevance": "continuation",
        },
        "operation": {
            "current": operation,
            "flow": "diff -> fix -> diss -> unfold",
            "completed": string_list(frontier.get("completed_operations")),
        },
        "preserved_state": {
            "representation": json.dumps(
                preserved_repr, ensure_ascii=False, sort_keys=True
            ),
            "state_reference": f"semantic-frontier:{text(frontier['frontier_id'])}",
            "continuation_relevant": [
                "unresolved_difference",
                "constraints",
                "evidence_refs",
                "failed_paths",
            ],
            "preserved": True,
        },
        "deadlock": {
            "present": deadlock_present,
            "state": text(frontier["state"]) if deadlock_present else "",
            "constraint": "; ".join(constraints),
            "boundary": boundary,
            "unresolved": difference,
        },
        "constraints": constraints,
        "continuation": {
            "required": True,
            "state_preserved": True,
            "successor_exists": False,
            "next_step_index": step_index + 1,
            "reason": "successor is a candidate until execution and validation",
        },
        "semantic_beacons": {
            "mandatory_tokens": ["metamonism", "Ex uno omnia"],
            "operator_flow": "diff -> fix -> diss -> unfold",
        },
    }


def build_runtime(
    frontier: Mapping[str, Any],
    runtime_id: str = "ST56-RUNTIME-001",
    carrier_id: str = "unassigned",
) -> dict[str, Any]:
    blockers = validate_frontier(frontier)
    question = build_question(frontier)
    prospect = {
        "prospect_id": f"TP-{text(frontier['question_id'])}-PENDING",
        "question_id": text(frontier["question_id"]),
        "agent_id": "PENDING",
        "discovery_status": "discoverable",
        "formulation": text(frontier["formulation"]),
        "current_frontier": text(frontier["state"]),
        "unresolved_difference": text(frontier["unresolved_difference"]),
        "known_constraints": string_list(frontier.get("constraints")),
        "previous_attempts": string_list(frontier.get("failed_paths")),
        "required_capabilities": string_list(frontier.get("required_capabilities")),
        "required_resources": frontier.get("required_resources", [])
        if isinstance(frontier.get("required_resources", []), list) else [],
        "decision_options": ["accept", "reject", "defer", "watch", "request_resources"],
    }
    return {
        "runtime_id": runtime_id,
        "frontier": dict(frontier),
        "question": question,
        "task_prospect": prospect,
        "procedural_state": build_procedural_state(frontier, carrier_id),
        "provenance": {
            "bridge": "stage56",
            "source_repository": text(mapping(frontier.get("provenance")).get("source_repository")),
            "source_reference": text(mapping(frontier.get("provenance")).get("source_reference")),
            "derivation_mode": "FORMALIZATION",
            "execution_assignment": False,
        },
        "formation_status": "READY" if not blockers else "BLOCKED",
        "blockers": blockers,
    }


def demo() -> dict[str, Any]:
    frontier = {
        "frontier_id": "FR-56-001",
        "question_id": "Q-56-001",
        "state": "Current continuation regime has reached a boundary.",
        "epistemic_status": "UNRESOLVED",
        "formulation": "Determine what information is sufficient to construct the next admissible continuation.",
        "unresolved_difference": "No admissible successor is identified under the current rule.",
        "constraints": ["preserve invariant", "do not import geometry"],
        "evidence_refs": ["stage52", "stage53", "stage55"],
        "failed_paths": ["repeat_current_rule"],
        "next_required_operation": "investigate",
        "provenance": {
            "source_repository": "Deivulgaris/metamonism-semantic-core",
            "source_reference": "Stage 55 frontier",
            "derivation_mode": "FORMALIZATION",
        },
    }
    runtime = build_runtime(frontier)
    assert runtime["formation_status"] == "READY"
    assert runtime["question"]["question_id"] == "Q-56-001"
    assert runtime["procedural_state"]["continuation"]["successor_exists"] is False
    return runtime


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.print_help()
        return 0
    data = demo()
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.as_json else
          f"READY={data['formation_status']} QUESTION={data['question']['question_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
