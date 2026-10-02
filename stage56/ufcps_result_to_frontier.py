#!/usr/bin/env python3
"""Stage 56: convert a UFCPS result into a candidate semantic frontier patch."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

RESULT_CLASSES = {
    "solution", "partial", "negative", "contradiction",
    "inconclusive", "anomaly", "deadlock",
}


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [text(value)] if text(value) else []
    if not isinstance(value, list):
        return []
    return [text(v) for v in value if text(v)]


def classify(result: Mapping[str, Any]) -> str:
    kind = text(result.get("result_class")).lower()
    if kind not in RESULT_CLASSES:
        raise ValueError(f"unsupported result class: {kind}")
    return kind


def build_frontier_patch(result: Mapping[str, Any]) -> dict[str, Any]:
    kind = classify(result)
    unresolved = text(result.get("unresolved_difference"))
    next_operation = text(result.get("next_required_operation")).lower()
    failed_paths = string_list(result.get("failed_paths"))
    evidence = string_list(result.get("evidence_refs"))

    patch = {
        "result_class": kind,
        "result_content": text(result.get("result_content")),
        "evidence_refs": evidence,
        "provenance": dict(result.get("provenance", {}))
        if isinstance(result.get("provenance", {}), Mapping) else {},
        "semantic_promotion_required": True,
    }

    if kind == "solution":
        patch.update({
            "status_candidate": "resolved_candidate",
            "resolution_candidate": text(result.get("result_content")),
        })
    elif kind == "partial":
        patch.update({
            "status_candidate": "unresolved",
            "unresolved_difference": unresolved,
        })
    elif kind == "negative":
        method = text(result.get("method", "unspecified_method"))
        patch.update({
            "status_candidate": "unresolved",
            "negative_result": text(result.get("result_content")),
            "failed_paths": sorted(set(failed_paths + [method])),
            "unresolved_difference": unresolved,
            "next_required_operation": next_operation or "investigate",
        })
    elif kind == "contradiction":
        patch.update({
            "status_candidate": "unresolved",
            "contradiction": text(result.get("result_content")),
            "unresolved_difference": unresolved or "branch results are incompatible",
            "next_required_operation": next_operation or "investigate",
        })
    elif kind == "inconclusive":
        patch.update({
            "status_candidate": "unresolved",
            "uncertainty": text(result.get("result_content")),
            "unresolved_difference": unresolved or "additional discriminating information is required",
            "next_required_operation": next_operation or "investigate",
        })
    elif kind == "anomaly":
        patch.update({
            "status_candidate": "unresolved",
            "anomaly": text(result.get("result_content")),
            "unresolved_difference": unresolved or "anomaly requires differentiation",
            "next_required_operation": next_operation or "investigate",
        })
    elif kind == "deadlock":
        patch.update({
            "status_candidate": "blocked",
            "deadlock": text(result.get("result_content")),
            "unresolved_difference": unresolved or "current method cannot continue",
            "next_required_operation": next_operation or "investigate",
        })
    return patch


def demo() -> dict[str, Any]:
    cases = {
        "negative": {
            "result_class": "negative",
            "result_content": "Current rule yields no admissible successor.",
            "method": "repeat_current_rule",
            "unresolved_difference": "Which distinction changes the successor set?",
            "evidence_refs": ["run-56-001"],
            "provenance": {"source": "ufcps-execution", "status": "UNRESOLVED"},
        },
        "contradiction": {
            "result_class": "contradiction",
            "result_content": "Independent branches produce incompatible constraints.",
            "unresolved_difference": "Which constraint explains the divergence?",
            "evidence_refs": ["branch-a", "branch-b"],
            "provenance": {"source": "ufcps-execution", "status": "CONFLICT"},
        },
        "solution": {
            "result_class": "solution",
            "result_content": "Candidate solution obtained.",
            "evidence_refs": ["run-56-002"],
            "provenance": {"source": "ufcps-execution", "status": "CANDIDATE"},
        },
    }
    output = {name: build_frontier_patch(value) for name, value in cases.items()}
    assert output["negative"]["status_candidate"] == "unresolved"
    assert output["contradiction"]["status_candidate"] == "unresolved"
    assert output["solution"]["status_candidate"] == "resolved_candidate"
    assert output["solution"]["semantic_promotion_required"] is True
    return output


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
          "negative -> unresolved; contradiction -> unresolved; solution -> resolved_candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
