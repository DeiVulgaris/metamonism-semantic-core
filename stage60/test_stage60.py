#!/usr/bin/env python3
"""Stage 60 executable test matrix."""

from information_result_classifier import classify_retrieval
from invariant_reasoning_pipeline import run
from invariant_reasoning_replay import replay, validate_chain


def chain(status="SOURCE", broken=False):
    first_from = "wrong-root" if broken else "mm:core.inv.ban_of_indifference"
    return {
        "chain_id": "TEST-CHAIN",
        "root_invariant": {
            "id": "mm:core.inv.ban_of_indifference",
            "statement": "Nontrivial actualization excludes the identity/indifference case.",
            "status": "SOURCE",
        },
        "steps": [
            {
                "step_id": "S1",
                "from_id": first_from,
                "to_id": "dissipation",
                "relation": "consequence",
                "statement": "Dissipation follows in the registered chain.",
                "status": status,
            },
            {
                "step_id": "S2",
                "from_id": "dissipation",
                "to_id": "continuation",
                "relation": "consequence",
                "statement": "Continuation follows in the registered chain.",
                "status": status,
            },
        ],
    }


def main():
    assert classify_retrieval(
        {
            "retrieval_id": "RET-1",
            "query_id": "Q-1",
            "retrieval_status": "FOUND",
        },
        query_intent="SOLUTION_DISCOVERY",
    )["result_class"] == "SOLUTION_FOUND"

    assert classify_retrieval(
        {
            "retrieval_id": "RET-2",
            "query_id": "Q-2",
            "retrieval_status": "NOT_FOUND",
        },
        query_intent="INFORMATION_GAP",
    )["result_class"] == "INFORMATION_GAP"

    assert classify_retrieval(
        {
            "retrieval_id": "RET-3",
            "query_id": "Q-3",
            "retrieval_status": "NOT_FOUND",
        },
        query_intent="SOLUTION_DISCOVERY",
    )["result_class"] == "NO_ADEQUATE_INFO"

    assert classify_retrieval(
        {
            "retrieval_id": "RET-4",
            "query_id": "Q-4",
            "retrieval_status": "ERROR",
            "metadata": {"result_class": "SOLUTION_FOUND"},
        },
        query_intent="SOLUTION_DISCOVERY",
    )["result_class"] == "RETRIEVAL_FAILURE"

    errors = validate_chain(chain(broken=True))
    assert "first_step_not_rooted_in_invariant" in errors

    errors = validate_chain(
        {
            **chain(),
            "steps": [chain()["steps"][0], {
                "step_id": "S2",
                "from_id": "unrelated",
                "to_id": "continuation",
                "relation": "consequence",
                "statement": "Broken link.",
                "status": "SOURCE",
            }],
        }
    )
    assert "step_2_not_connected_to_previous" in errors

    classification = classify_retrieval(
        {
            "retrieval_id": "RET-5",
            "query_id": "Q-5",
            "retrieval_status": "FOUND",
        },
        query_intent="CONTRADICTION_CHECK",
    )
    result = run(
        {
            "retrieval_id": "RET-5",
            "query_id": "Q-5",
            "retrieval_status": "FOUND",
        },
        chain(status="UNRESOLVED"),
        query_intent="CONTRADICTION_CHECK",
    )
    assert result["status"] == "REPLAYED"
    assert result["classification"]["result_class"] == "CONTRADICTION_FOUND"
    assert result["reasoning_trace"]["root_invariant"]["status"] == "SOURCE"
    assert result["reasoning_trace"]["chain_path"][0] == "mm:core.inv.ban_of_indifference"
    assert result["reasoning_trace"]["chain_path"][1] == "dissipation"
    assert result["reasoning_trace"]["steps"][0]["position"] == 1
    assert all(
        step["information_effect"] == "REQUIRES_RECONCILIATION"
        for step in result["reasoning_trace"]["steps"]
    )

    assert classification["classification_id"]

    print("Stage 60 tests: PASS")


if __name__ == "__main__":
    main()
