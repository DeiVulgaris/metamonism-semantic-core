#!/usr/bin/env python3
"""Stage 57: ground task decomposition in explicit semantic differences."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence


VALID_TYPES = {
    "investigation",
    "validation",
    "experiment",
    "formalization",
    "reconciliation",
    "resource",
    "clarification",
    "external_requirement",
}

VALID_OPERATIONS = {
    "diff",
    "fix",
    "diss",
    "unfold",
    "delegate",
    "compose",
    "investigate",
    "experiment",
    "formalize",
    "validate",
    "request_resources",
    "terminate",
}

BASE_KEYS = {
    "unresolved_difference",
    "evidence_gap",
    "constraint_gap",
    "hypothesis_candidate",
    "contradiction",
    "resource_gap",
    "external_requirement",
}


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [text(value)] if text(value) else []
    if not isinstance(value, list):
        return []
    return [text(v) for v in value if text(v)]


def as_map(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def validate_frontier(frontier: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for key in (
        "frontier_id",
        "question_id",
        "state",
        "epistemic_status",
        "formulation",
        "unresolved_difference",
    ):
        if not text(frontier.get(key)):
            blockers.append(f"{key}_missing")

    provenance = as_map(frontier.get("provenance"))
    for key in ("source_repository", "source_reference", "derivation_mode"):
        if not text(provenance.get(key)):
            blockers.append(f"provenance_{key}_missing")

    return blockers


def validate_seed(seed: Mapping[str, Any], known_ids: set[str]) -> list[str]:
    blockers: list[str] = []
    seed_id = text(seed.get("seed_id"))
    if not seed_id:
        blockers.append("seed_id_missing")
    elif seed_id in known_ids:
        blockers.append(f"duplicate_seed_id:{seed_id}")

    source_basis = text(seed.get("source_basis"))
    if source_basis not in BASE_KEYS:
        blockers.append(f"invalid_source_basis:{source_basis or 'missing'}")

    if text(seed.get("task_type")) not in VALID_TYPES:
        blockers.append(f"invalid_task_type:{text(seed.get('task_type')) or 'missing'}")

    if not text(seed.get("formulation")):
        blockers.append(f"formulation_missing:{seed_id or 'unknown'}")
    if not text(seed.get("unresolved_difference")):
        blockers.append(f"unresolved_difference_missing:{seed_id or 'unknown'}")

    operation = text(seed.get("next_required_operation")).lower()
    if operation not in VALID_OPERATIONS:
        blockers.append(f"invalid_operation:{seed_id or 'unknown'}")

    parent = seed.get("parent_seed_id")
    if parent not in (None, "") and text(parent) not in known_ids:
        blockers.append(f"unknown_parent_seed:{seed_id or 'unknown'}")

    return blockers


def detect_cycles(seeds: Sequence[Mapping[str, Any]]) -> list[str]:
    graph = {
        text(seed.get("seed_id")): text(seed.get("parent_seed_id"))
        for seed in seeds
        if text(seed.get("seed_id"))
    }
    errors: list[str] = []
    for start in graph:
        seen: set[str] = set()
        current = start
        while current:
            if current in seen:
                errors.append(f"cycle_detected:{start}")
                break
            seen.add(current)
            current = graph.get(current, "")
    return sorted(set(errors))


def build_task_tree(frontier: Mapping[str, Any]) -> dict[str, Any]:
    blockers = validate_frontier(frontier)
    seeds = frontier.get("decomposition_seeds", [])
    if not isinstance(seeds, list):
        blockers.append("decomposition_seeds_must_be_list")
        seeds = []

    seen: set[str] = set()
    for seed in seeds:
        if not isinstance(seed, Mapping):
            blockers.append("decomposition_seed_not_object")
            continue
        blockers.extend(validate_seed(seed, seen))
        seed_id = text(seed.get("seed_id"))
        if seed_id:
            seen.add(seed_id)

    blockers.extend(detect_cycles([s for s in seeds if isinstance(s, Mapping)]))

    question_id = text(frontier.get("question_id"))
    root_id = f"TASK-{question_id}-ROOT"

    root = {
        "task_id": root_id,
        "question_id": question_id,
        "parent_task_id": None,
        "task_type": "primary",
        "formulation": text(frontier.get("formulation")),
        "unresolved_difference": text(frontier.get("unresolved_difference")),
        "next_required_operation": text(frontier.get("next_required_operation")).lower(),
        "status": "ROOT" if not blockers else "BLOCKED",
        "constraints": string_list(frontier.get("constraints")),
        "evidence_refs": string_list(frontier.get("evidence_refs")),
        "depends_on": [],
        "required_capabilities": string_list(frontier.get("required_capabilities")),
        "required_resources": frontier.get("required_resources", [])
            if isinstance(frontier.get("required_resources", []), list) else [],
        "source_basis": "unresolved_difference",
        "provenance": dict(as_map(frontier.get("provenance"))),
    }

    tasks = [root]
    if blockers:
        return {
            "tree_id": f"TREE-{question_id}",
            "root_task_id": root_id,
            "tasks": tasks,
            "decomposition_status": "BLOCKED",
            "blockers": sorted(set(blockers)),
            "provenance": {
                "stage": "57",
                "mode": "FORMALIZATION",
            },
        }

    seed_to_task: dict[str, dict[str, Any]] = {}
    pending = [s for s in seeds if isinstance(s, Mapping)]

    # Repeatedly materialize seeds whose parent is already materialized.
    remaining = list(pending)
    while remaining:
        progressed = False
        next_remaining: list[Mapping[str, Any]] = []
        for seed in remaining:
            seed_id = text(seed.get("seed_id"))
            parent_seed = text(seed.get("parent_seed_id"))
            if parent_seed and parent_seed not in seed_to_task:
                next_remaining.append(seed)
                continue

            parent_task_id = (
                seed_to_task[parent_seed]["task_id"] if parent_seed
                else root_id
            )
            task_id = f"TASK-{question_id}-{seed_id}"
            task = {
                "task_id": task_id,
                "question_id": f"{question_id}:{seed_id}",
                "parent_task_id": parent_task_id,
                "task_type": text(seed.get("task_type")),
                "formulation": text(seed.get("formulation")),
                "unresolved_difference": text(seed.get("unresolved_difference")),
                "next_required_operation": text(seed.get("next_required_operation")).lower(),
                "status": "CANDIDATE",
                "constraints": string_list(seed.get("constraints")) or string_list(frontier.get("constraints")),
                "evidence_refs": string_list(seed.get("evidence_refs")) or string_list(frontier.get("evidence_refs")),
                "depends_on": [
                    f"TASK-{question_id}-{text(dep)}"
                    for dep in string_list(seed.get("depends_on"))
                ],
                "required_capabilities": string_list(seed.get("required_capabilities")),
                "required_resources": seed.get("required_resources", [])
                    if isinstance(seed.get("required_resources", []), list) else [],
                "source_basis": text(seed.get("source_basis")),
                "provenance": {
                    **dict(as_map(frontier.get("provenance"))),
                    "decomposition_seed": seed_id,
                    "derivation_mode": "FORMALIZATION",
                },
            }
            tasks.append(task)
            seed_to_task[seed_id] = task
            progressed = True

        if not progressed:
            # Should only occur for an invalid dependency graph not caught above.
            remaining_ids = sorted(text(s.get("seed_id")) for s in next_remaining)
            blockers.append(f"unmaterialized_seeds:{','.join(remaining_ids)}")
            break
        remaining = next_remaining

    task_ids = {task["task_id"] for task in tasks}
    for task in tasks[1:]:
        for dep in task["depends_on"]:
            if dep not in task_ids:
                blockers.append(f"unknown_task_dependency:{task['task_id']}:{dep}")

    status = "READY" if not blockers else "BLOCKED"
    return {
        "tree_id": f"TREE-{question_id}",
        "root_task_id": root_id,
        "tasks": tasks,
        "decomposition_status": status,
        "blockers": sorted(set(blockers)),
        "provenance": {
            "stage": "57",
            "mode": "FORMALIZATION",
            "source_repository": text(as_map(frontier.get("provenance")).get("source_repository")),
            "source_reference": text(as_map(frontier.get("provenance")).get("source_reference")),
        },
    }


def emit_ufcps_questions(tree: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Emit question objects suitable for UFCPS UQL/discovery integration."""
    tasks = tree.get("tasks", [])
    if not isinstance(tasks, list):
        return []

    output: list[dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, Mapping):
            continue
        task_id = text(task.get("task_id"))
        question_id = text(task.get("question_id"))
        parent_task_id = text(task.get("parent_task_id"))
        parent_question_id = ""
        if parent_task_id:
            parent = next(
                (candidate for candidate in tasks
                 if isinstance(candidate, Mapping) and text(candidate.get("task_id")) == parent_task_id),
                None,
            )
            parent_question_id = text(parent.get("question_id")) if isinstance(parent, Mapping) else ""

        output.append({
            "question_id": question_id,
            "parent_question_id": parent_question_id or None,
            "formulation": text(task.get("formulation")),
            "status": "unresolved",
            "current_state": "derived task candidate",
            "unresolved_difference": text(task.get("unresolved_difference")),
            "known_constraints": string_list(task.get("constraints")),
            "previous_attempts": [],
            "evidence_references": string_list(task.get("evidence_refs")),
            "required_capabilities": string_list(task.get("required_capabilities")),
            "requirements": {
                "resources": task.get("required_resources", [])
                if isinstance(task.get("required_resources", []), list) else []
            },
            "next_required_operation": text(task.get("next_required_operation")).lower(),
            "task_id": task_id,
            "task_type": text(task.get("task_type")),
            "provenance": dict(as_map(task.get("provenance"))),
        })
    return output


def demo() -> dict[str, Any]:
    frontier = {
        "frontier_id": "FR-57-001",
        "question_id": "Q-57-001",
        "state": "Current continuation regime reached a boundary.",
        "epistemic_status": "UNRESOLVED",
        "formulation": "Determine what information is sufficient to construct the next admissible continuation.",
        "unresolved_difference": "The current rule does not identify a successor.",
        "constraints": ["preserve invariant", "do not import geometry"],
        "evidence_refs": ["stage52", "stage53", "stage56"],
        "next_required_operation": "investigate",
        "provenance": {
            "source_repository": "Deivulgaris/metamonism-semantic-core",
            "source_reference": "Stage 56 frontier",
            "derivation_mode": "FORMALIZATION",
        },
        "decomposition_seeds": [
            {
                "seed_id": "BOUNDARY",
                "source_basis": "unresolved_difference",
                "task_type": "investigation",
                "formulation": "Identify the missing boundary information.",
                "unresolved_difference": "The content of the continuation boundary is not sufficient.",
                "next_required_operation": "investigate",
            },
            {
                "seed_id": "DISTINCTION",
                "source_basis": "evidence_gap",
                "task_type": "investigation",
                "formulation": "Determine which new distinction changes the successor set.",
                "unresolved_difference": "No discriminating distinction is currently registered.",
                "next_required_operation": "investigate",
            },
            {
                "seed_id": "VALIDATE",
                "parent_seed_id": "DISTINCTION",
                "source_basis": "constraint_gap",
                "task_type": "validation",
                "formulation": "Validate a candidate successor against active constraints.",
                "unresolved_difference": "Candidate successor admissibility is unresolved.",
                "next_required_operation": "validate",
                "depends_on": ["DISTINCTION"],
            },
        ],
    }
    tree = build_task_tree(frontier)
    questions = emit_ufcps_questions(tree)
    assert tree["decomposition_status"] == "READY"
    assert len(tree["tasks"]) == 4
    assert len(questions) == 4
    assert questions[3]["parent_question_id"] == "Q-57-001:DISTINCTION"
    return {"tree": tree, "ufcps_questions": questions}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.print_help()
        return 0
    data = demo()
    if args.as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("Stage 57 task decomposition")
        print("status:", data["tree"]["decomposition_status"])
        print("tasks:", len(data["tree"]["tasks"]))
        print("UFCPS questions:", len(data["ufcps_questions"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
