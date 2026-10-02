#!/usr/bin/env python3
"""Stage 58: construct information-space queries from a semantic frontier."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

VALID_INTENTS = {
    "SOLUTION_DISCOVERY",
    "METHOD_DISCOVERY",
    "EVIDENCE_DISCOVERY",
    "CONTRADICTION_CHECK",
    "INFORMATION_GAP",
    "PRECEDENT_DISCOVERY",
    "SOURCE_VALIDATION",
}


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [text(value)] if text(value) else []
    if not isinstance(value, list):
        return []
    return [text(v) for v in value if text(v)]


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def validate_frontier(frontier: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("frontier_id", "question_id", "formulation", "unresolved_difference"):
        if not text(frontier.get(key)):
            errors.append(f"{key}_missing")
    if not mapping(frontier.get("provenance")):
        errors.append("provenance_missing")
    return errors


def default_intents(frontier: Mapping[str, Any]) -> list[str]:
    if _text := text(frontier.get("query_intents")):
        return [x.strip().upper() for x in _text.split(",") if x.strip()]
    explicit = frontier.get("query_intents")
    if isinstance(explicit, list) and explicit:
        return [text(x).upper() for x in explicit if text(x)]
    return [
        "SOLUTION_DISCOVERY",
        "METHOD_DISCOVERY",
        "EVIDENCE_DISCOVERY",
        "CONTRADICTION_CHECK",
        "INFORMATION_GAP",
    ]


def build_queries(frontier: Mapping[str, Any], intents: Sequence[str]) -> list[dict[str, Any]]:
    formulation = text(frontier["formulation"])
    difference = text(frontier["unresolved_difference"])
    constraints = strings(frontier.get("constraints"))
    failed = strings(frontier.get("failed_paths"))
    exclusion_text = [f"already tried: {path}" for path in failed]

    result: list[dict[str, Any]] = []
    for index, intent in enumerate(intents, start=1):
        if intent not in VALID_INTENTS:
            raise ValueError(f"unsupported query intent: {intent}")

        if intent == "SOLUTION_DISCOVERY":
            query = f"Existing solutions for: {formulation}. Focus on unresolved difference: {difference}."
        elif intent == "METHOD_DISCOVERY":
            query = f"Methods or approaches for resolving: {difference}, within problem: {formulation}."
        elif intent == "EVIDENCE_DISCOVERY":
            query = f"Evidence, observations, measurements, or documented results relevant to: {difference}."
        elif intent == "CONTRADICTION_CHECK":
            query = f"Counterevidence, limitations, failures, or contradictory results concerning: {formulation}."
        elif intent == "INFORMATION_GAP":
            query = f"What information is typically required to resolve or discriminate: {difference}?"
        elif intent == "PRECEDENT_DISCOVERY":
            query = f"Prior cases or precedents structurally similar to: {formulation}."
        else:
            query = f"Primary or authoritative sources relevant to: {difference}."

        if constraints:
            query += " Constraints: " + "; ".join(constraints) + "."

        result.append({
            "query_id": f"QRY-{text(frontier['question_id'])}-{index:02d}",
            "intent": intent,
            "text": query,
            "target_difference": difference,
            "exclusions": exclusion_text,
        })
    return result


def build_query_plan(frontier: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_frontier(frontier)
    intents = default_intents(frontier)
    for intent in intents:
        if intent not in VALID_INTENTS:
            errors.append(f"invalid_query_intent:{intent}")

    if errors:
        return {
            "query_plan_id": f"QPLAN-{text(frontier.get('question_id'))}",
            "frontier_id": text(frontier.get("frontier_id")),
            "question_id": text(frontier.get("question_id")),
            "intents": intents,
            "queries": [],
            "constraints": strings(frontier.get("constraints")),
            "source_classes": strings(frontier.get("source_classes")) or [
                "web", "literature", "code_repository", "dataset", "internal_corpus"
            ],
            "provenance": mapping(frontier.get("provenance")),
            "status": "BLOCKED",
            "errors": sorted(set(errors)),
        }

    return {
        "query_plan_id": f"QPLAN-{text(frontier['question_id'])}",
        "frontier_id": text(frontier["frontier_id"]),
        "question_id": text(frontier["question_id"]),
        "intents": list(dict.fromkeys(intents)),
        "queries": build_queries(frontier, intents),
        "constraints": strings(frontier.get("constraints")),
        "source_classes": strings(frontier.get("source_classes")) or [
            "web", "literature", "code_repository", "dataset", "internal_corpus"
        ],
        "provenance": {
            **dict(mapping(frontier.get("provenance"))),
            "generation_mode": "FORMALIZATION",
            "planner_stage": "58",
        },
        "status": "READY",
        "errors": [],
    }


def demo() -> dict[str, Any]:
    frontier = {
        "frontier_id": "FR-58-001",
        "question_id": "Q-58-001",
        "formulation": "Determine whether an admissible continuation can be constructed.",
        "unresolved_difference": "Current continuation rule identifies no successor.",
        "constraints": ["preserve invariant", "do not import geometry"],
        "failed_paths": ["repeat_current_rule"],
        "provenance": {
            "source_repository": "metamonism-semantic-core",
            "source_reference": "stage57",
            "derivation_mode": "FORMALIZATION",
        },
    }
    plan = build_query_plan(frontier)
    assert plan["status"] == "READY"
    assert len(plan["queries"]) == 5
    assert plan["queries"][0]["intent"] == "SOLUTION_DISCOVERY"
    return plan


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.print_help()
        return 0
    plan = demo()
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.as_json else
          f"status={plan['status']} queries={len(plan['queries'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
