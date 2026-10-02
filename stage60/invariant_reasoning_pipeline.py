#!/usr/bin/env python3
"""Stage 60: classify a retrieval and immediately replay the registered chain from its invariant."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

from information_result_classifier import classify_retrieval
from invariant_reasoning_replay import replay


def run(
    retrieval: Mapping[str, Any],
    chain: Mapping[str, Any],
    *,
    query_intent: str | None = None,
    affected_step_id: str | None = None,
) -> dict[str, Any]:
    """Classify information, then re-run the explicit reasoning chain from its root invariant."""
    classification = classify_retrieval(retrieval, query_intent=query_intent)
    if affected_step_id:
        classification["affected_step_id"] = str(affected_step_id).strip()
        classification["classification_basis"] = {
            **dict(classification.get("classification_basis", {})),
            "impact_reference_basis": "SEMANTIC_VALIDATION",
        }
    trace = replay(chain, classification)
    return {
        "status": trace.get("status", "BLOCKED"),
        "classification": classification,
        "reasoning_trace": trace,
        "next_action": trace.get("next_action", ""),
    }


def demo() -> dict[str, Any]:
    retrieval = {
        "retrieval_id": "RET-PIPE-01",
        "query_id": "QRY-PIPE-01",
        "retrieval_status": "FOUND",
        "provenance": {"provider": "demo"},
    }
    chain = {
        "chain_id": "MM-CH2-CHAIN",
        "question_id": "Q-MM-CH2-DEMO",
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
    result = run(retrieval, chain, query_intent="EVIDENCE_DISCOVERY")
    assert result["status"] == "REPLAYED"
    assert result["classification"]["result_class"] == "EVIDENCE_FOUND"
    assert result["reasoning_trace"]["root_invariant"]["id"] == "mm:core.inv.ban_of_indifference"
    assert result["reasoning_trace"]["steps"][0]["from_id"] == "mm:core.inv.ban_of_indifference"
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
          f"status={result['status']} class={result['classification']['result_class']} "
          f"next_action={result['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
