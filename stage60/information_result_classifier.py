#!/usr/bin/env python3
"""Stage 60: classify information-space retrievals without semantic truth claims."""

from __future__ import annotations

import argparse
import hashlib
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
VALID_RETRIEVAL = {"FOUND", "NOT_FOUND", "PARTIAL", "ERROR"}
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


def _classification_id(retrieval_id: str, result_class: str) -> str:
    seed = f"{retrieval_id}|{result_class}"
    return "CLS-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def classify_retrieval(
    retrieval: Mapping[str, Any],
    *,
    query_intent: str | None = None,
) -> dict[str, Any]:
    retrieval_id = _text(retrieval.get("retrieval_id"))
    query_id = _text(retrieval.get("query_id"))
    status = _text(retrieval.get("retrieval_status")).upper()
    intent = _text(query_intent or retrieval.get("intent")).upper()

    if not retrieval_id or not query_id:
        raise ValueError("retrieval_id and query_id are required")
    if status not in VALID_RETRIEVAL:
        raise ValueError(f"unsupported retrieval status: {status}")
    if intent and intent not in VALID_INTENTS:
        raise ValueError(f"unsupported query intent: {intent}")

    provider_class = _text(
        _mapping(retrieval.get("metadata")).get("result_class")
        or _mapping(retrieval.get("source")).get("result_class")
    ).upper()

    if status == "ERROR":
        result_class = "RETRIEVAL_FAILURE"
        basis = "RETRIEVAL_STATUS"
    elif provider_class in VALID_CLASSES:
        result_class = provider_class
        basis = "PROVIDER_DECLARED_RESULT_CLASS"
    elif status == "NOT_FOUND":
        result_class = "RETRIEVAL_FAILURE"
        basis = "RETRIEVAL_STATUS"
    elif intent == "SOLUTION_DISCOVERY":
        result_class = "SOLUTION_FOUND"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    elif intent == "METHOD_DISCOVERY":
        result_class = "METHOD_FOUND"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    elif intent == "EVIDENCE_DISCOVERY":
        result_class = "EVIDENCE_FOUND"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    elif intent == "CONTRADICTION_CHECK":
        result_class = "CONTRADICTION_FOUND"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    elif intent == "INFORMATION_GAP":
        result_class = "INFORMATION_GAP"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    elif intent in {"PRECEDENT_DISCOVERY", "SOURCE_VALIDATION"}:
        result_class = "EVIDENCE_FOUND"
        basis = "RETRIEVAL_STATUS_AND_QUERY_INTENT"
    else:
        result_class = "NO_ADEQUATE_INFO"
        basis = "NO_QUERY_INTENT"

    return {
        "classification_id": _classification_id(retrieval_id, result_class),
        "retrieval_id": retrieval_id,
        "query_id": query_id,
        "result_class": result_class,
        "classification_basis": {
            "basis": basis,
            "retrieval_status": status,
            "query_intent": intent,
        },
        "provenance": {
            **dict(_mapping(retrieval.get("provenance"))),
            "stage": "60",
            "classification": "OPERATIONAL_ONLY",
        },
    }


def classify_many(
    retrievals: Sequence[Mapping[str, Any]],
    *,
    query_intents: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for retrieval in retrievals:
        query_id = _text(retrieval.get("query_id"))
        intent = query_intents.get(query_id) if query_intents else None
        results.append(classify_retrieval(retrieval, query_intent=intent))
    return results


def demo() -> dict[str, Any]:
    retrieval = {
        "retrieval_id": "RET-DEMO-01",
        "query_id": "QRY-DEMO-01",
        "retrieval_status": "FOUND",
        "relevance": "HIGH",
        "provenance": {"provider": "demo"},
    }
    result = classify_retrieval(retrieval, query_intent="SOLUTION_DISCOVERY")
    assert result["result_class"] == "SOLUTION_FOUND"
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
          f"classification={result['result_class']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
