#!/usr/bin/env python3
"""Stage 61: locate information impact in an invariant-rooted reasoning trace."""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any, Mapping, Sequence


VALID_RESULTS = {
    "SOLUTION_FOUND",
    "METHOD_FOUND",
    "EVIDENCE_FOUND",
    "CONTRADICTION_FOUND",
    "INFORMATION_GAP",
    "NO_ADEQUATE_INFO",
    "RETRIEVAL_FAILURE",
}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _frontier_id(question_id: str, trace_id: str, step_id: str) -> str:
    seed = "|".join([question_id, trace_id, step_id])
    return "FR61-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def _next_action(result_class: str) -> str:
    return {
        "SOLUTION_FOUND": "validate_adapt_or_reuse_candidate_solution",
        "METHOD_FOUND": "evaluate_method_against_rooted_chain",
        "EVIDENCE_FOUND": "validate_evidence_against_registered_chain",
        "CONTRADICTION_FOUND": "reconcile_or_test_affected_step",
        "INFORMATION_GAP": "generate_information_producing_operation",
        "NO_ADEQUATE_INFO": "continue_from_anchor_without_claiming_absence",
        "RETRIEVAL_FAILURE": "retry_or_change_information_provider",
    }[result_class]


def locate_impact(
    reasoning_trace: Mapping[str, Any],
    classification: Mapping[str, Any],
) -> dict[str, Any]:
    trace_id = _text(reasoning_trace.get("trace_id"))
    question_id = _text(reasoning_trace.get("question_id"))
    root = _mapping(reasoning_trace.get("root_invariant"))
    steps = reasoning_trace.get("steps")
    result_class = _text(classification.get("result_class")).upper()

    if not trace_id or not _text(root.get("id")):
        return {"status":"BLOCKED","errors":["trace_or_root_missing"]}
    if not isinstance(steps, list) or not steps:
        return {"status":"BLOCKED","errors":["steps_missing"]}
    if result_class not in VALID_RESULTS:
        return {"status":"BLOCKED","errors":["invalid_result_class"]}

    requested = _text(
        classification.get("affected_step_id")
        or _mapping(classification.get("classification_basis")).get("affected_step_id")
    )

    anchor_index = None
    impact_mode = ""
    if requested:
        for idx, step in enumerate(steps):
            if isinstance(step, Mapping) and _text(step.get("step_id")) == requested:
                anchor_index = idx
                impact_mode = "EXPLICIT_STEP_REFERENCE"
                break
        if anchor_index is None:
            return {
                "status":"BLOCKED",
                "errors":[f"affected_step_not_found:{requested}"],
            }
    else:
        anchor_index = len(steps) - 1
        impact_mode = "TAIL_FALLBACK"

    affected = dict(steps[anchor_index])
    reasoning_prefix = [
        _text(step.get("step_id"))
        for step in steps[:anchor_index + 1]
        if isinstance(step, Mapping) and _text(step.get("step_id"))
    ]
    downstream = []
    for step in steps[anchor_index + 1:]:
        if not isinstance(step, Mapping):
            continue
        item = dict(step)
        item["replay_status"] = "REQUIRES_REPLAY"
        downstream.append(item)

    if result_class == "CONTRADICTION_FOUND":
        affected["information_effect"] = "REQUIRES_RECONCILIATION"
    else:
        affected["information_effect"] = "REQUIRES_VALIDATION"

    information_result = dict(_mapping(reasoning_trace.get("information_result")))
    information_result.update({
        "result_class": result_class,
        "affected_step_id": affected["step_id"],
    })

    return {
        "status":"READY",
        "frontier_id":_frontier_id(question_id or "UNBOUND", trace_id, affected["step_id"]),
        "question_id":question_id or "UNBOUND",
        "root_invariant_id":_text(root["id"]),
        "trace_id":trace_id,
        "anchor_step_id":affected["step_id"],
        "impact_mode":impact_mode,
        "reasoning_prefix":reasoning_prefix,
        "affected_step":affected,
        "downstream_steps":downstream,
        "information_result":information_result,
        "next_required_operation":_next_action(result_class),
        "provenance":{
            **dict(_mapping(reasoning_trace.get("provenance"))),
            "stage":"61",
            "mode":"IMPACT_LOCALIZED_FRONTIER_REBUILD",
        },
    }


def rebuild_frontier(
    reasoning_trace: Mapping[str, Any],
    classification: Mapping[str, Any],
) -> dict[str, Any]:
    return locate_impact(reasoning_trace, classification)


def demo() -> dict[str, Any]:
    trace = {
        "trace_id":"TRACE-DEMO",
        "question_id":"Q-DEMO",
        "root_invariant":{
            "id":"mm:core.inv.ban_of_indifference",
            "statement":"Nontrivial actualization excludes the identity/indifference case.",
        },
        "steps":[
            {"step_id":"S1","from_id":"mm:core.inv.ban_of_indifference","to_id":"dissipation","status":"SOURCE"},
            {"step_id":"S2","from_id":"dissipation","to_id":"space_time","status":"SOURCE"},
            {"step_id":"S3","from_id":"space_time","to_id":"orthogonal_resolution","status":"UNRESOLVED"},
        ],
        "information_result":{"classification_id":"CLS-DEMO"},
        "provenance":{"stage":"60"},
    }
    classification = {
        "classification_id":"CLS-DEMO",
        "result_class":"CONTRADICTION_FOUND",
        "affected_step_id":"S3",
    }
    result = rebuild_frontier(trace, classification)
    assert result["status"] == "READY"
    assert result["impact_mode"] == "EXPLICIT_STEP_REFERENCE"
    assert result["anchor_step_id"] == "S3"
    assert result["reasoning_prefix"] == ["S1","S2","S3"]
    assert result["affected_step"]["information_effect"] == "REQUIRES_RECONCILIATION"
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.print_help()
        return 0
    result = demo()
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else
          f"status={result['status']} anchor={result['anchor_step_id']} mode={result['impact_mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
