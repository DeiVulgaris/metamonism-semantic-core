#!/usr/bin/env python3
"""Stage 55 — semantic-frontier to UFCPS task formation.

This module creates a UFCPS-compatible task candidate from a structured
semantic frontier. It deliberately stops before claim, scheduling, resource
reservation, or execution.

The engine is conservative:
- an explicit unresolved difference is required;
- continuation-relevant state is preserved;
- result classifications do not become semantic truth automatically;
- provenance is mandatory;
- the engine can report BLOCKED when the frontier is insufficient.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Mapping, Sequence


OPERATIONS = {
    "diff", "fix", "diss", "unfold", "delegate", "compose",
    "investigate", "experiment", "formalize", "validate",
    "request_resources", "terminate",
}

TERMINAL_FORMATION_STATES = {"INVALID", "BLOCKED"}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return [_text(x) for x in value if _text(x)]


def assess_frontier(frontier: Mapping[str, Any]) -> tuple[str, list[str]]:
    blockers: list[str] = []

    if not _text(frontier.get("frontier_id")):
        blockers.append("frontier_id_missing")
    if not _text(frontier.get("state")):
        blockers.append("state_missing")
    if not _text(frontier.get("epistemic_status")):
        blockers.append("epistemic_status_missing")
    if not _text(frontier.get("question")):
        blockers.append("question_missing")
    if not _text(frontier.get("unresolved_difference")):
        blockers.append("unresolved_difference_missing")

    operation = _text(frontier.get("next_required_operation")).lower()
    if operation not in OPERATIONS:
        blockers.append("next_required_operation_missing_or_invalid")

    provenance = frontier.get("provenance")
    if not isinstance(provenance, Mapping):
        blockers.append("provenance_missing")
    else:
        for key in ("source_repository", "source_reference", "derivation_mode"):
            if not _text(provenance.get(key)):
                blockers.append(f"provenance_{key}_missing")

    status = "READY" if not blockers else "BLOCKED"
    return status, blockers


def build_task_candidate(frontier: Mapping[str, Any], *, bridge_id: str | None = None) -> dict[str, Any]:
    status, blockers = assess_frontier(frontier)
    result = {
        "bridge_id": bridge_id or f"BR-{_text(frontier.get('frontier_id')) or 'UNNAMED'}",
        "source_frontier": {
            "frontier_id": _text(frontier.get("frontier_id")),
            "state": _text(frontier.get("state")),
            "epistemic_status": _text(frontier.get("epistemic_status")),
        },
        "question": _text(frontier.get("question")),
        "unresolved_difference": _text(frontier.get("unresolved_difference")),
        "constraints": _list(frontier.get("constraints")),
        "evidence_refs": _list(frontier.get("evidence_refs")),
        "failed_paths": _list(frontier.get("failed_paths")),
        "next_required_operation": _text(frontier.get("next_required_operation")).lower(),
        "task_formation_status": status,
        "provenance": dict(frontier.get("provenance", {})) if isinstance(frontier.get("provenance"), Mapping) else {},
    }
    if "new_data" in frontier:
        result["new_data"] = frontier["new_data"]
    if blockers:
        result["blockers"] = blockers
    return result


def demo() -> dict[str, Any]:
    ready_frontier = {
        "frontier_id": "FRONTIER-001",
        "state": "Current derivation reached an unresolved boundary.",
        "epistemic_status": "UNRESOLVED",
        "question": "What additional distinction permits the next admissible continuation?",
        "unresolved_difference": "Current continuation rule yields no admissible successor under active constraints.",
        "constraints": ["preserve registered invariant", "do not import geometry"],
        "evidence_refs": ["semantic-core:stage52", "semantic-core:stage53"],
        "failed_paths": ["repeat_current_mode"],
        "next_required_operation": "investigate",
        "provenance": {
            "source_repository": "Deivulgaris/metamonism-semantic-core",
            "source_reference": "stage55 architecture",
            "derivation_mode": "FORMALIZATION",
        },
    }
    blocked_frontier = dict(ready_frontier)
    blocked_frontier["unresolved_difference"] = ""
    ready = build_task_candidate(ready_frontier)
    blocked = build_task_candidate(blocked_frontier)
    assert ready["task_formation_status"] == "READY"
    assert blocked["task_formation_status"] == "BLOCKED"
    assert "unresolved_difference_missing" in blocked["blockers"]
    return {"ready": ready, "blocked": blocked}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.print_help()
        return 0
    data = demo()
    if args.as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("Stage 55 task formation demo")
        print("READY:", data["ready"]["task_formation_status"])
        print("BLOCKED:", data["blocked"]["task_formation_status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
