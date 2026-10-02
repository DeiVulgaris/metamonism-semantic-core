#!/usr/bin/env python3
"""Stage 60: replay a registered reasoning chain from its root invariant."""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any, Mapping, Sequence

VALID_STATUSES = {
    "SOURCE",
    "THEORETICAL_HYPOTHESIS",
    "PROPOSED",
    "UNRESOLVED",
    "BLOCKED",
}
VALID_CLASSES = {
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


def _trace_id(root_id: str, information_id: str) -> str:
    seed = f"{root_id}|{information_id}"
    return "TRACE-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def validate_chain(chain: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    root = _mapping(chain.get("root_invariant"))
    if not _text(root.get("id")) or not _text(root.get("statement")):
        errors.append("root_invariant_missing")
    steps = chain.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("steps_missing")
        return errors
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, Mapping):
            errors.append(f"step_{index}_invalid")
            continue
        for key in ("step_id", "from_id", "to_id", "relation", "statement"):
            if not _text(step.get(key)):
                errors.append(f"step_{index}_{key}_missing")
        status = _text(step.get("status")).upper()
        if status and status not in VALID_STATUSES:
            errors.append(f"step_{index}_invalid_status:{status}")
    return sorted(set(errors))


def _decision(result_class: str) -> tuple[str, str]:
    return {
        "SOLUTION_FOUND": (
            "INFORMATION_CAN_REPLACE_OR_QUALIFY_CURRENT_OPERATION",
            "validate_adapt_or_reuse_candidate_solution",
        ),
        "METHOD_FOUND": (
            "KNOWN_METHOD_AVAILABLE_FOR_REEVALUATION",
            "evaluate_method_against_rooted_chain",
        ),
        "EVIDENCE_FOUND": (
            "NEW_EVIDENCE_AVAILABLE_FOR_DOWNSTREAM_VALIDATION",
            "validate_evidence_against_registered_chain",
        ),
        "CONTRADICTION_FOUND": (
            "DOWNSTREAM_CHAIN_REQUIRES_RECONCILIATION_OR_TEST",
            "locate_first_affected_step_and_reconcile",
        ),
        "INFORMATION_GAP": (
            "DISCRIMINATING_INFORMATION_MISSING",
            "generate_information_producing_operation",
        ),
        "NO_ADEQUATE_INFO": (
            "NO_ADEQUATE_INFORMATION_FOUND",
            "continue_from_invariant_without_claiming_absence",
        ),
        "RETRIEVAL_FAILURE": (
            "INFORMATION_SPACE_UNAVAILABLE_OR_FAILED",
            "preserve_question_and_retry_or_change_provider",
        ),
    }[result_class]


def replay(chain: Mapping[str, Any], classification: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_chain(chain)
    result_class = _text(classification.get("result_class")).upper()
    if result_class not in VALID_CLASSES:
        errors.append("invalid_result_class")
    if not _text(classification.get("classification_id")):
        errors.append("classification_id_missing")
    if errors:
        return {"status": "BLOCKED", "errors": sorted(set(errors)), "trace_id": "", "steps": []}

    root = dict(_mapping(chain["root_invariant"]))
    steps: list[dict[str, Any]] = []
    for position, step in enumerate(chain["steps"], start=1):
        item = dict(step)
        item["position"] = position
        item["derivation_source"] = item.get("provenance", "REGISTERED_CHAIN")
        item["status"] = _text(item.get("status", "UNRESOLVED")).upper()
        steps.append(item)

    consequence, next_action = _decision(result_class)

    affected_positions: list[int] = []
    if result_class == "CONTRADICTION_FOUND":
        affected_positions = [
            step["position"]
            for step in steps
            if step["status"] in {"PROPOSED", "THEORETICAL_HYPOTHESIS", "UNRESOLVED", "BLOCKED"}
        ]
    elif result_class in {"SOLUTION_FOUND", "METHOD_FOUND", "EVIDENCE_FOUND", "INFORMATION_GAP"}:
        affected_positions = [steps[-1]["position"]]

    for step in steps:
        step["information_effect"] = (
            "REQUIRES_RECONCILIATION"
            if step["position"] in affected_positions and result_class == "CONTRADICTION_FOUND"
            else "REQUIRES_VALIDATION"
            if step["position"] in affected_positions
            else "NO_DIRECT_EFFECT"
        )

    information_result = {
        "classification_id": _text(classification["classification_id"]),
        "retrieval_id": _text(classification.get("retrieval_id")),
        "query_id": _text(classification.get("query_id")),
        "result_class": result_class,
    }

    return {
        "status": "REPLAYED",
        "trace_id": _trace_id(_text(root["id"]), information_result["classification_id"]),
        "root_invariant": root,
        "steps": steps,
        "information_result": information_result,
        "consequence": consequence,
        "next_action": next_action,
        "provenance": {
            "stage": "60",
            "mode": "INVARIANT_ROOTED_REPLAY",
            "chain_id": _text(chain.get("chain_id")) or "UNNAMED",
        },
    }


def demo() -> dict[str, Any]:
    chain = {
        "chain_id": "MM-CH2-CHAIN",
        "root_invariant": {
            "id": "mm:core.inv.ban_of_indifference",
            "statement": "Nontrivial actualization excludes the identity/indifference case.",
            "status": "SOURCE",
            "provenance": "Chapter 1",
        },
        "steps": [
            {
                "step_id": "S1",
                "from_id": "mm:core.inv.ban_of_indifference",
                "to_id": "mm:core.prc.dissipation",
                "relation": "consequence",
                "statement": "Continuing actualization is represented as dissipation of identity.",
                "status": "SOURCE",
                "provenance": "Chapter 2",
            },
            {
                "step_id": "S2",
                "from_id": "mm:core.prc.dissipation",
                "to_id": "mm:core.prc.space_time",
                "relation": "consequence",
                "statement": "Continuing differentiation yields processual space/time structure.",
                "status": "SOURCE",
                "provenance": "Chapter 2",
            },
            {
                "step_id": "S3",
                "from_id": "mm:core.prc.space_time",
                "to_id": "mm:core.prc.ray",
                "relation": "geometric_consequence",
                "statement": "Directionality admits the ray as a first geometric image.",
                "status": "SOURCE",
                "provenance": "Chapter 2",
            },
            {
                "step_id": "S4",
                "from_id": "mm:core.prc.ray",
                "to_id": "mm:core.prc.orthogonal_resolution",
                "relation": "continuation_requirement",
                "statement": "Exhausted continuation requires an independent orthogonal resolution.",
                "status": "SOURCE",
                "provenance": "Chapter 2",
            },
        ],
    }
    classification = {
        "classification_id": "CLS-DEMO-01",
        "retrieval_id": "RET-DEMO-01",
        "query_id": "QRY-DEMO-01",
        "result_class": "CONTRADICTION_FOUND",
    }
    result = replay(chain, classification)
    assert result["status"] == "REPLAYED"
    assert result["root_invariant"]["status"] == "SOURCE"
    assert all(step["information_effect"] == "NO_DIRECT_EFFECT" for step in result["steps"])
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
          f"status={result['status']} trace={result['trace_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
