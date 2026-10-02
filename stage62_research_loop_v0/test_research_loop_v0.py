#!/usr/bin/env python3
"""Tests for deterministic Research Loop v0."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import validate

from research_loop_policy import build_policy_decision


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "stage62_research_loop_v0" / "research_loop_v0.schema.json").read_text(
        encoding="utf-8"
    )
)
INPUT_SCHEMA = json.loads(
    (
        ROOT
        / "stage62_research_loop_v0"
        / "research_loop_v0_input.schema.json"
    ).read_text(encoding="utf-8")
)
VECTORS = yaml.safe_load(
    (ROOT / "stage62_research_loop_v0" / "test_vectors.yaml").read_text(
        encoding="utf-8"
    )
)


ONTOLOGY_FILES = (
    "id_registry.yaml",
    "claim_registry.yaml",
    "relation_registry.yaml",
    "derivation_registry.yaml",
    "ambiguity_registry.yaml",
    "conflict_registry.yaml",
    "undefined_term_registry.yaml",
    "historical_formulation_registry.yaml",
    "semantic_inventory.yaml",
    "semantic_graph.jsonld",
)


def snapshot_ontology() -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for name in ONTOLOGY_FILES:
        path = ROOT / name
        if path.exists():
            snapshot[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def test_vectors() -> None:
    before = snapshot_ontology()

    for case in VECTORS["cases"]:
        source = copy.deepcopy(case["input"])
        validate(source, INPUT_SCHEMA)

        result = build_policy_decision(source)
        validate(result, SCHEMA)

        decision = result["policy_decision"]
        expected = case["expected"]

        assert decision["question_id"] == VECTORS["question_id"]
        assert decision["selected_operation"] == expected["selected_operation"]
        assert decision["rationale_codes"] == expected["rationale_codes"]
        assert decision["rights"]["ontology_write"] is False
        assert decision["rights"]["claim_elevate"] is False

        derived = decision["derived_question"]
        assert (derived is not None) is bool(expected["derived_question_emitted"])

        if derived is not None:
            expected_derived = expected["derived_question"]
            assert derived["parent_question"] == expected_derived["parent_question"]
            assert derived["derived_from_step"] == expected_derived["derived_from_step"]
            assert derived["trigger"] == expected_derived["trigger"]
            assert derived["status"] == expected_derived["status"]
            assert derived["derivation_basis"]
            assert "constraints" in derived
            assert "truth" not in derived["derivation_basis"].lower()

            provenance = decision["provenance"]
            assert provenance["parent_question"] == decision["question_id"]
            assert provenance["derived_from_step"] == derived["derived_from_step"]
            assert provenance["trigger"] == derived["trigger"]
            assert provenance["constraints_inherited"] == derived["constraints"]

        if case["id"] == "R0-05":
            assert decision["selected_operation"] != "terminate"

        if case["id"] == "R0-06":
            assert decision["selected_operation"] == "fix"
            assert decision["rights"]["claim_elevate"] is False

        if case["id"] == "R0-07":
            assert decision["selected_operation"] == "terminate"
            assert decision["rationale_codes"] == ["EXPLICIT_BUDGET_EXHAUSTED"]
            assert decision["derived_question"] is None

    after = snapshot_ontology()
    assert before == after


def test_policy_is_pure_for_same_input() -> None:
    source = copy.deepcopy(VECTORS["cases"][0]["input"])
    first = build_policy_decision(source)
    second = build_policy_decision(source)
    assert first == second


if __name__ == "__main__":
    test_vectors()
    test_policy_is_pure_for_same_input()
    print("RESEARCH LOOP V0: PASS")
