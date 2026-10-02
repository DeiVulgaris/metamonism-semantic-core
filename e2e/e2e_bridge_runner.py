#!/usr/bin/env python3
"""One-command E2E bridge test for the closed Semantic Core Stage 61 baseline."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

try:
    import yaml
    from jsonschema import validate as jsonschema_validate
except ImportError as exc:
    raise SystemExit(
        "E2E test requires PyYAML and jsonschema. "
        "Install with: python -m pip install pyyaml jsonschema"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parents[1]
for stage_dir in ("stage55", "stage56", "stage60", "stage61"):
    path = REPO_ROOT / stage_dir
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from task_formation_engine import build_task_candidate  # type: ignore
from semantic_to_ufcps_runtime import build_runtime  # type: ignore
from invariant_reasoning_pipeline import run as stage60_run  # type: ignore
from impact_localizer import locate_impact  # type: ignore


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def ontology_snapshot() -> dict[str, str]:
    return {
        name: sha256_file(REPO_ROOT / name)
        for name in ONTOLOGY_FILES
        if (REPO_ROOT / name).exists()
    }


def load_vectors(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, Mapping):
        raise AssertionError("test vectors must load as a mapping")
    return data


def load_schema(relative_path: str) -> Mapping[str, Any]:
    path = REPO_ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, Mapping):
        raise AssertionError(f"schema must be an object: {relative_path}")
    return data


def validate_schema(name: str, schema: Mapping[str, Any], instance: Mapping[str, Any]) -> None:
    try:
        jsonschema_validate(instance=instance, schema=schema)
    except Exception as exc:
        raise AssertionError(f"{name} schema validation failed: {exc}") from exc


def make_frontier(fixture: Mapping[str, Any]) -> dict[str, Any]:
    source = dict(fixture["initial_frontier"])
    question_id = str(fixture["question_id"])
    provenance = dict(source["provenance"])
    return {
        **source,
        "question_id": question_id,
        "question": str(source["question"]),
        "formulation": str(source["formulation"]),
        "provenance": provenance,
    }


def make_chain(fixture: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(dict(fixture["reasoning_trace"]))


def mock_provider(case: Mapping[str, Any]) -> dict[str, Any]:
    """Return the already-defined Stage 58–59 retrieval-envelope shape."""
    retrieval = copy.deepcopy(dict(case["mock_retrieval"]))
    required = ("retrieval_id", "query_id", "retrieval_status", "intent")
    missing = [key for key in required if not str(retrieval.get(key, "")).strip()]
    if missing:
        raise AssertionError(f"{case['id']}: mock provider missing fields: {missing}")
    retrieval.setdefault("provenance", {})
    retrieval["provenance"] = {
        **dict(retrieval["provenance"]),
        "runtime": "mock_provider_v1",
    }
    return retrieval


def uql_style_update(
    initial_frontier: Mapping[str, Any],
    localized: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Test-only UQL-shaped update. It is not a second production implementation."""
    original = copy.deepcopy(dict(initial_frontier))
    current = copy.deepcopy(dict(initial_frontier))

    patch = {
        "current_procedural_unit": str(localized["anchor_step_id"]),
        "next_required_operation": str(localized["next_required_operation"]),
        "status": "OPEN",
        "process_terminated": False,
        "validated_semantic_claim": False,
        "metadata": {
            "semantic_replay": {
                "trace_id": str(localized["trace_id"]),
                "root_invariant_id": str(localized["root_invariant_id"]),
                "anchor_step_id": str(localized["anchor_step_id"]),
                "impact_mode": str(localized["impact_mode"]),
                "reasoning_prefix": list(localized["reasoning_prefix"]),
                "affected_step": copy.deepcopy(localized["affected_step"]),
                "downstream_steps": copy.deepcopy(localized["downstream_steps"]),
                "information_result": copy.deepcopy(localized["information_result"]),
            }
        },
    }

    result_class = str(localized["information_result"]["result_class"])
    if result_class in {"INFORMATION_GAP", "RETRIEVAL_FAILURE"}:
        negative = str(result_class)
        patch["negative_results"] = [negative]

    current.update(patch)

    history = [
        {
            "event_type": "question_created",
            "question_id": str(initial_frontier["question_id"]),
            "snapshot": original,
        },
        {
            "event_type": "semantic_core_impact_localized_frontier",
            "question_id": str(localized["question_id"]),
            "patch": copy.deepcopy(patch),
        },
        {
            "event_type": "semantic_core_reasoning_replay",
            "question_id": str(localized["question_id"]),
            "trace_id": str(localized["trace_id"]),
            "root_invariant_id": str(localized["root_invariant_id"]),
            "anchor_step_id": str(localized["anchor_step_id"]),
            "impact_mode": str(localized["impact_mode"]),
        },
    ]

    return current, history


def check_case(
    case: Mapping[str, Any],
    fixture: Mapping[str, Any],
    schemas: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    case_id = str(case["id"])
    expected = dict(case["classification_expectation"])
    initial = make_frontier(fixture)
    chain = make_chain(fixture)

    task = build_task_candidate(initial, bridge_id=f"BR-{case_id}")
    assert task["task_formation_status"] == "READY", (case_id, task)
    assert task["question_id"] == fixture["question_id"]
    assert task["source_frontier"]["question_id"] == fixture["question_id"]
    validate_schema("Stage 55 task formation", schemas["stage55"], task)

    runtime = build_runtime(
        initial,
        runtime_id=f"RT-{case_id}",
        carrier_id="mock-carrier",
    )
    assert runtime["formation_status"] == "READY", (case_id, runtime)
    assert runtime["task_prospect"]["question_id"] == fixture["question_id"]
    assert runtime["question"]["question_id"] == fixture["question_id"]
    validate_schema("Stage 56 runtime", schemas["stage56"], runtime)

    retrieval = mock_provider(case)
    requested_step = case["mock_retrieval"].get("affected_step_id")
    result = stage60_run(
        retrieval,
        chain,
        query_intent=str(case["mock_retrieval"]["intent"]),
        affected_step_id=str(requested_step) if requested_step else None,
    )
    classification = result["classification"]
    trace = result["reasoning_trace"]

    assert classification["query_id"] == retrieval["query_id"]
    assert classification["result_class"] == expected["result_class"], (
        case_id,
        classification,
        expected,
    )
    assert trace["question_id"] == fixture["question_id"]
    assert trace["root_invariant"]["id"] == fixture["root_invariant_id"]
    validate_schema("Stage 60 classification", schemas["stage60_classification"], classification)
    validate_schema("Stage 60 reasoning trace", schemas["stage60_trace"], trace)

    localized = locate_impact(trace, classification)
    assert localized["status"] == "READY", (case_id, localized)
    assert localized["question_id"] == fixture["question_id"]
    assert localized["root_invariant_id"] == fixture["root_invariant_id"]
    assert localized["impact_mode"] == expected["impact_mode"]
    if expected.get("anchor_step_id"):
        assert localized["anchor_step_id"] == expected["anchor_step_id"]
    if expected.get("affected_step_id"):
        assert classification.get("affected_step_id") == expected["affected_step_id"]
    if expected.get("fallback_label"):
        assert localized["affected_step"]["fallback_label"] == expected["fallback_label"]
    assert len(localized["downstream_steps"]) == int(expected["downstream_replay_count"])
    assert localized["affected_step"]["information_effect"] == expected["affected_effect"] if expected.get("affected_effect") else True
    validate_schema("Stage 61 localized frontier", schemas["stage61"], localized)

    updated, history = uql_style_update(initial, localized)

    assert updated["question_id"] == fixture["question_id"]
    assert updated["current_procedural_unit"] == localized["anchor_step_id"]
    assert updated["next_required_operation"]
    assert updated["process_terminated"] is False
    assert updated["validated_semantic_claim"] is False
    assert history[0]["snapshot"] == initial
    assert history[0]["snapshot"] != updated
    assert len(history) >= 2

    if expected.get("negative_result_preserved"):
        assert "negative_results" in updated
        assert expected["result_class"] in updated["negative_results"]

    assert expected["validated_semantic_claim"] is False
    if "registry_write_allowed" in expected:
        assert expected["registry_write_allowed"] is False

    if expected["impact_mode"] == "TAIL_FALLBACK":
        assert localized["impact_mode"] == "TAIL_FALLBACK"
        assert localized["affected_step"]["fallback_label"] == (
            "procedural_tail_fallback_not_causal_attribution"
        )

    return {
        "case_id": case_id,
        "question_id": fixture["question_id"],
        "chain_length": len(trace["steps"]),
        "requires_replay": len(localized["downstream_steps"]),
        "impact_mode": localized["impact_mode"],
        "anchor_step_id": localized["anchor_step_id"],
        "result_class": classification["result_class"],
        "process_terminated": updated["process_terminated"],
        "validated_semantic_claim": updated["validated_semantic_claim"],
        "next_required_operation": updated["next_required_operation"],
        "history_events": len(history),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vectors",
        default=str(REPO_ROOT / "stage61" / "e2e_bridge_test_vectors.yaml"),
        help="path to the YAML E2E fixture",
    )
    parser.add_argument(
        "--metrics",
        default="",
        help="optional path for machine-readable metrics JSON",
    )
    args = parser.parse_args()

    vectors_path = Path(args.vectors)
    data = load_vectors(vectors_path)
    fixture = data["fixture"]

    schemas = {
        "stage55": load_schema("stage55/bridge_contract.schema.json"),
        "stage56": load_schema("stage56/runtime_contract.schema.json"),
        "stage60_classification": load_schema("stage60/result_classification.schema.json"),
        "stage60_trace": load_schema("stage60/reasoning_trace.schema.json"),
        "stage61": load_schema("stage61/impact_localized_frontier.schema.json"),
    }

    before = ontology_snapshot()
    results = [check_case(case, fixture, schemas) for case in data["cases"]]
    after = ontology_snapshot()

    assert before == after, (
        "ontology files changed during E2E run",
        {"before": before, "after": after},
    )

    explicit = sum(row["impact_mode"] == "EXPLICIT_STEP_REFERENCE" for row in results)
    fallback = sum(row["impact_mode"] == "TAIL_FALLBACK" for row in results)
    total_replay = sum(row["requires_replay"] for row in results)
    schema_checks = len(results) * 5
    metrics = {
        "suite": data["suite"],
        "version": data["version"],
        "status": "PASS",
        "cases": len(results),
        "chain_length": results[0]["chain_length"] if results else 0,
        "requires_replay_total": total_replay,
        "explicit_impact_runs": explicit,
        "fallback_runs": fallback,
        "schema_validation": {
            "passed": schema_checks,
            "attempted": schema_checks,
            "pass_rate": 1.0,
        },
        "question_id_preserved": all(
            row["question_id"] == fixture["question_id"] for row in results
        ),
        "ontology_unchanged": True,
        "results": results,
    }

    if args.metrics:
        metrics_path = Path(args.metrics)
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        metrics_path.write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print("E2E BRIDGE CONTINUITY: PASS")
    print(f"Cases: {metrics['cases']}")
    print(f"Chain length: {metrics['chain_length']}")
    print(f"REQUIRES_REPLAY total: {metrics['requires_replay_total']}")
    print(f"Explicit impact: {metrics['explicit_impact_runs']}")
    print(f"Tail fallback: {metrics['fallback_runs']}")
    print("Schema validation pass rate: 100%")
    print("question_id preserved: PASS")
    print("ontology unchanged: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
