#!/usr/bin/env python3
"""Deterministic Research Loop v0 next-operation policy.

Policy = transition chooser, not meaning author.

The module is intentionally pure: it returns a policy decision and optional
derived question. It does not write ontology files, registries, claims, or
UQL storage.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping

ALLOWED_OPERATIONS = (
    "diff",
    "fix",
    "diss",
    "unfold",
    "delegate",
    "compose",
    "terminate",
)

RESULT_CLASSES = (
    "SOLUTION_FOUND",
    "METHOD_FOUND",
    "EVIDENCE_FOUND",
    "CONTRADICTION_FOUND",
    "INFORMATION_GAP",
    "NO_ADEQUATE_INFO",
    "RETRIEVAL_FAILURE",
)

IMPACT_MODES = ("EXPLICIT_STEP_REFERENCE", "TAIL_FALLBACK")


def _require_nonempty(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"missing required field: {field}")
    return text


def _slug(value: str) -> str:
    value = value.strip()
    if value.startswith("q:"):
        value = value[2:]
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "root"


def _derive_question_id(parent_question: str, anchor_step_id: str, trigger: str) -> str:
    return (
        f"q:derived:{_slug(parent_question)}:"
        f"{_slug(anchor_step_id)}:{_slug(trigger)}"
    )


def _base_provenance(
    question_id: str,
    anchor_step_id: str,
    result_class: str,
    constraints: list[str],
    rule_id: str,
) -> dict[str, Any]:
    return {
        "parent_question": question_id,
        "derived_from_step": anchor_step_id,
        "trigger": result_class,
        "derivation_basis": f"policy_rule:{rule_id}",
        "constraints_inherited": list(constraints),
    }


def _derived_question(
    question_id: str,
    anchor_step_id: str,
    trigger: str,
    unresolved_difference: str,
    derivation_basis: str,
    constraints: list[str],
) -> dict[str, Any]:
    return {
        "question_id": _derive_question_id(question_id, anchor_step_id, trigger),
        "parent_question": question_id,
        "derived_from_step": anchor_step_id,
        "trigger": trigger,
        "unresolved_difference": unresolved_difference,
        "derivation_basis": derivation_basis,
        "constraints": list(constraints),
        "status": "OPEN",
    }


def _validated_input(source: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(source))
    _require_nonempty(result.get("question_id"), "question_id")
    _require_nonempty(result.get("unresolved_difference"), "unresolved_difference")
    _require_nonempty(result.get("anchor_step_id"), "anchor_step_id")

    result_class = _require_nonempty(result.get("result_class"), "result_class")
    if result_class not in RESULT_CLASSES:
        raise ValueError(f"invalid result_class: {result_class}")

    impact_mode = _require_nonempty(result.get("impact_mode"), "impact_mode")
    if impact_mode not in IMPACT_MODES:
        raise ValueError(f"invalid impact_mode: {impact_mode}")

    constraints = result.get("constraints") or []
    if not isinstance(constraints, list) or not all(isinstance(x, str) for x in constraints):
        raise ValueError("constraints must be a list of strings")
    result["constraints"] = list(constraints)

    budget = result.get("budget")
    if budget is not None and not isinstance(budget, Mapping):
        raise ValueError("budget must be an object or null")

    result["budget"] = dict(budget) if isinstance(budget, Mapping) else None
    return result


def build_policy_decision(source: Mapping[str, Any]) -> dict[str, Any]:
    """Build one deterministic policy decision.

    Budget exhaustion is a global guard and therefore outranks classification
    rules, matching the R0-07 contract.
    """
    data = _validated_input(source)

    question_id = str(data["question_id"])
    anchor_step_id = str(data["anchor_step_id"])
    result_class = str(data["result_class"])
    constraints = list(data["constraints"])
    budget = data["budget"] or {}

    if budget.get("exhausted") is True:
        selected_operation = "terminate"
        rationale_codes = ["EXPLICIT_BUDGET_EXHAUSTED"]
        derived_question = None
        rule_id = "R-BUDGET-STOP"
    elif result_class == "CONTRADICTION_FOUND":
        selected_operation = "diff"
        rationale_codes = ["CONTRADICTION_REQUIRES_REDIFFERENTIATION"]
        derived_question = _derived_question(
            question_id,
            anchor_step_id,
            "CONTRADICTION_FOUND",
            (
                f"Reconcile contradiction at step {anchor_step_id}: "
                "registered derivation conflicts with retrieved information_result."
            ),
            f"CONTRADICTION_FOUND against reasoning step {anchor_step_id}",
            constraints,
        )
        rule_id = "R-CONTRACTION"
    elif result_class == "EVIDENCE_FOUND":
        selected_operation = "fix"
        rationale_codes = ["EVIDENCE_PRESERVE_THEN_VALIDATE"]
        derived_question = None
        rule_id = "R-EVIDENCE"
    elif result_class == "METHOD_FOUND":
        selected_operation = "fix"
        rationale_codes = ["METHOD_PRESERVE_AS_PROCESS_INFO"]
        derived_question = None
        rule_id = "R-METHOD"
    elif result_class == "SOLUTION_FOUND":
        selected_operation = "fix"
        rationale_codes = [
            "SOLUTION_CANDIDATE_NOT_CLAIM",
            "REQUIRE_VALIDATION_PATH",
        ]
        derived_question = None
        rule_id = "R-SOLUTION-CANDIDATE"
    elif result_class == "INFORMATION_GAP":
        selected_operation = "diff"
        rationale_codes = ["GAP_IS_UNRESOLVED_DIFFERENCE"]
        derived_question = _derived_question(
            question_id,
            anchor_step_id,
            "INFORMATION_GAP",
            (
                f"Information gap at step {anchor_step_id}: "
                "required evidence or structure absent."
            ),
            f"INFORMATION_GAP on step {anchor_step_id}",
            constraints,
        )
        rule_id = "R-GAP"
    elif result_class == "NO_ADEQUATE_INFO":
        selected_operation = "diff"
        rationale_codes = ["NO_ADEQUATE_INFO_REOPEN_DIFF"]
        derived_question = _derived_question(
            question_id,
            anchor_step_id,
            "NO_ADEQUATE_INFO",
            "No adequate information for current intent; reformulate difference or constraints.",
            f"NO_ADEQUATE_INFO for question {question_id}",
            constraints,
        )
        rule_id = "R-NO-ADEQUATE"
    elif result_class == "RETRIEVAL_FAILURE":
        selected_operation = "delegate"
        rationale_codes = ["PROVIDER_FAILURE_DELEGATE_NOT_TERMINATE"]
        derived_question = None
        rule_id = "R-RETRIEVAL-FAIL"
    else:
        # Defensive fallback: unreachable after input validation.
        selected_operation = "diff"
        rationale_codes = ["DEFAULT_SAFE_DIFF"]
        derived_question = None
        rule_id = "R-DEFAULT"

    provenance = _base_provenance(
        question_id,
        anchor_step_id,
        result_class,
        constraints,
        rule_id,
    )
    if derived_question is not None:
        provenance["derivation_basis"] = str(derived_question["derivation_basis"])

    return {
        "policy_decision": {
            "question_id": question_id,
            "selected_operation": selected_operation,
            "rationale_codes": rationale_codes,
            "derived_question": derived_question,
            "provenance": provenance,
            "rights": {
                "ontology_write": False,
                "claim_elevate": False,
            },
        }
    }


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    decision = build_policy_decision(payload)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
