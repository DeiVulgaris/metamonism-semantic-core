"""Stage 39 — Research Result Engine.

Records execution results and constructs an append-only trajectory successor.
It validates continuity but deliberately does not infer scientific truth.
"""

from copy import deepcopy
from typing import Any, Dict

try:
    from stage35.trajectory_engine import append_transition
except ImportError:
    append_transition = None

def _result_action(result_class):
    return {
        "CONFIRMING":"RECORD_RESULT",
        "DISCONFIRMING":"RECORD_RESULT",
        "PARTIALLY_CONFIRMING":"RECORD_RESULT",
        "INCONCLUSIVE":"RECORD_RESULT",
        "ANOMALOUS":"RECORD_RESULT",
        "INVALID":"RECORD_RESULT",
        "UNREPRODUCIBLE":"RECORD_RESULT",
        "BLOCKED":"RECORD_RESULT",
    }[result_class]

def build_successor_state(result: Dict[str, Any], predecessor_state_id: str) -> Dict[str, Any]:
    frontier = result["successor_frontier"]
    return {
        "state_id": frontier["frontier_id"],
        "timestamp_or_version": result["result_id"],
        "lifecycle": frontier["frontier_state"],
        "epistemic_status": frontier.get("epistemic_status", result.get("epistemic_status","UNRESOLVED")),
        "summary": result["interpretation"],
        "evidence": [
            {"claim": result["observation"], "status": result["result_class"], "provenance": result["provenance"]}
        ] + [
            {"claim": e, "status": "EVIDENCE", "provenance": result["provenance"]}
            for e in result.get("evidence", [])
        ],
        "open_questions": frontier.get("open_questions", []),
        "blockers": frontier.get("blockers", []),
        "provenance": frontier["provenance"],
    }

def apply_result(trajectory: Dict[str, Any], result: Dict[str, Any], predecessor_state_id: str) -> Dict[str, Any]:
    """Return a new trajectory with result recorded; never mutate the input."""
    if append_transition is None:
        raise ImportError("stage35.trajectory_engine is required")
    from_state = trajectory["current_state"]
    if from_state != predecessor_state_id:
        raise ValueError("predecessor_state_id must equal trajectory current_state")
    if result["trajectory_id"] != trajectory["trajectory_id"]:
        raise ValueError("result trajectory mismatch")
    successor = result["successor_frontier"]
    if successor["research_program_id"] != trajectory["program_id"]:
        raise ValueError("result research program mismatch")

    new_state = build_successor_state(result, predecessor_state_id)
    transition = {
        "transition_id": f"{trajectory['trajectory_id']}.result.{result['result_id']}",
        "from_state": predecessor_state_id,
        "to_state": new_state["state_id"],
        "action": _result_action(result["result_class"]),
        "trigger": f"Task {result['task_id']} executed",
        "evidence": [result["result_id"], *result.get("evidence", [])],
        "status": result.get("epistemic_status","UNRESOLVED"),
        "provenance": result["provenance"],
    }
    return append_transition(trajectory, transition, new_state)

def record_result(trajectory, result, predecessor_state_id):
    """Validate and apply a result. Execution itself remains external."""
    from stage39.result_validator import validate_result
    validate_result(result)
    return apply_result(trajectory, deepcopy(result), predecessor_state_id)
