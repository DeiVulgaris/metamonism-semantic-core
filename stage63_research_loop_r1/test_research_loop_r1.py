"""Tests for Research Loop R1 — UQL branch identity.

Vectors: R1-01 … R1-08 from research_loop_r1.yaml
Requires: uql_branch_store.py (same directory)

Does not write ontology registries.
"""

from __future__ import annotations

import copy
import unittest

from uql_branch_store import UQLBranchStore, STATUS_TRANSITIONS


def make_root(store: UQLBranchStore | None = None) -> tuple[UQLBranchStore, dict]:
    store = store or UQLBranchStore()
    root = store.register_root(
        statement="Local Failure ≠ Process Termination",
        unresolved_difference="Can successor P_n+1 be constructed after STUCK?",
        constraints=["Local Failure ≠ Process Termination"],
        slug="continuity.local_failure",
        created_from="fixture",
    )
    return store, root


def contradiction_decision(parent_id: str) -> dict:
    return {
        "question_id": "q:continuity.local_failure_vs_termination.v1",
        "uql_question_id": parent_id,
        "selected_operation": "diff",
        "rationale_codes": ["CONTRADICTION_REQUIRES_REDIFFERENTIATION"],
        "result_class": "CONTRADICTION_FOUND",
        "anchor_step_id": "S3",
        "derived_question": {
            "derived_from_step": "S3",
            "trigger": "CONTRADICTION_FOUND",
            "unresolved_difference": "Reconcile handoff contradiction at S3",
            "derivation_basis": "CONTRADICTION_FOUND against S3",
            "constraints": ["Local Failure ≠ Process Termination"],
            "statement": "Reconcile handoff contradiction at S3",
        },
    }


class TestR1UQLBranchStore(unittest.TestCase):
    def test_R1_01_spawn_child_on_contradiction(self):
        store, root = make_root()
        child = store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        self.assertIsNotNone(child)
        assert child is not None
        self.assertEqual(child["status"], "OPEN")
        self.assertEqual(child["parent_uql_question_id"], root["uql_question_id"])
        self.assertEqual(child["root_uql_question_id"], root["uql_question_id"])
        self.assertNotEqual(child["branch_id"], root["branch_id"])
        self.assertIn(child["branch_id"], store.branches)
        parent_hist = store.history_for(root["uql_question_id"])
        types = [e["event_type"] for e in parent_hist]
        self.assertIn("DERIVED_QUESTION_SPAWNED", types)
        self.assertIn("POLICY_DECISION", types)
        self.assertFalse(child["provenance"].get("ontology_write", True))

    def test_R1_02_no_spawn_on_evidence(self):
        store, root = make_root()
        decision = {
            "question_id": "q:continuity.local_failure_vs_termination.v1",
            "uql_question_id": root["uql_question_id"],
            "selected_operation": "fix",
            "rationale_codes": ["EVIDENCE_PRESERVE_THEN_VALIDATE"],
            "result_class": "EVIDENCE_FOUND",
            "anchor_step_id": "S3",
            "derived_question": None,
        }
        child = store.spawn_derived(decision)
        self.assertIsNone(child)
        self.assertEqual(len(store.list_open_children(root["uql_question_id"])), 0)
        types = [e["event_type"] for e in store.history_for(root["uql_question_id"])]
        self.assertIn("POLICY_DECISION", types)
        self.assertIn("OPERATION_SELECTED", types)
        self.assertNotIn("DERIVED_QUESTION_SPAWNED", types)

    def test_R1_03_retrieval_failure_no_terminate_branch(self):
        store, root = make_root()
        decision = {
            "question_id": "q:continuity.local_failure_vs_termination.v1",
            "uql_question_id": root["uql_question_id"],
            "selected_operation": "delegate",
            "rationale_codes": ["PROVIDER_FAILURE_DELEGATE_NOT_TERMINATE"],
            "result_class": "RETRIEVAL_FAILURE",
            "anchor_step_id": "S4",
            "derived_question": None,
        }
        child = store.spawn_derived(decision)
        self.assertIsNone(child)
        self.assertEqual(store.questions[root["uql_question_id"]]["status"], "OPEN")

    def test_R1_04_budget_terminate_closes_active_not_siblings(self):
        store, root = make_root()
        child = store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        self.assertIsNotNone(child)
        assert child is not None
        child_id = child["uql_question_id"]

        term = {
            "question_id": "q:derived-child",
            "uql_question_id": child_id,
            "selected_operation": "terminate",
            "rationale_codes": ["EXPLICIT_BUDGET_EXHAUSTED"],
            "derived_question": None,
        }
        out = store.spawn_derived(term)
        self.assertIsNone(out)
        self.assertEqual(store.questions[child_id]["status"], "CLOSED_TERMINATED")
        self.assertEqual(store.questions[root["uql_question_id"]]["status"], "OPEN")
        self.assertNotEqual(
            store.questions[child_id]["branch_id"],
            root["branch_id"],
        )

    def test_R1_05_lineage_query(self):
        store, root = make_root()
        child = store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        assert child is not None
        lineage = store.get_lineage(child["uql_question_id"])
        self.assertEqual(len(lineage), 2)
        self.assertEqual(lineage[0]["uql_question_id"], root["uql_question_id"])
        self.assertEqual(lineage[1]["uql_question_id"], child["uql_question_id"])
        open_children = store.list_open_children(root["uql_question_id"])
        self.assertEqual(len(open_children), 1)
        self.assertEqual(open_children[0]["uql_question_id"], child["uql_question_id"])

    def test_R1_06_solution_found_not_closed_resolved(self):
        store, root = make_root()
        decision = {
            "question_id": "q:continuity.local_failure_vs_termination.v1",
            "uql_question_id": root["uql_question_id"],
            "selected_operation": "fix",
            "rationale_codes": ["SOLUTION_CANDIDATE_NOT_CLAIM"],
            "result_class": "SOLUTION_FOUND",
            "anchor_step_id": "S4",
            "derived_question": None,
        }
        store.spawn_derived(decision)
        self.assertNotEqual(
            store.questions[root["uql_question_id"]]["status"],
            "CLOSED_RESOLVED",
        )
        with self.assertRaises(ValueError):
            store.set_status(root["uql_question_id"], "CLOSED_RESOLVED")
        q = store.set_status(root["uql_question_id"], "RESOLVED_CANDIDATE")
        self.assertEqual(q["status"], "RESOLVED_CANDIDATE")

    def test_R1_07_append_only_history(self):
        store, root = make_root()
        n0 = len(store.history)
        first = copy.deepcopy(store.history)
        store.append_history(
            root["uql_question_id"],
            root["branch_id"],
            "NOTE",
            {"k": 1},
        )
        self.assertEqual(len(store.history), n0 + 1)
        for i, e in enumerate(first):
            self.assertEqual(store.history[i], e)
        store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        self.assertGreater(len(store.history), n0 + 1)
        for i, e in enumerate(first):
            self.assertEqual(store.history[i], e)

    def test_R1_08_deterministic_ids(self):
        store_a, root_a = make_root()
        store_b, root_b = make_root()
        self.assertEqual(root_a["uql_question_id"], root_b["uql_question_id"])
        self.assertEqual(root_a["branch_id"], root_b["branch_id"])

        id1 = store_a.make_derived_question_id(
            root_a["uql_question_id"], "S3", "CONTRADICTION_FOUND", seq=0
        )
        id2 = store_b.make_derived_question_id(
            root_b["uql_question_id"], "S3", "CONTRADICTION_FOUND", seq=0
        )
        self.assertEqual(id1, id2)

        br1 = store_a.make_child_branch_id(
            root_a["uql_question_id"],
            root_a["branch_id"],
            "S3",
            "CONTRADICTION_FOUND",
            seq=0,
        )
        br2 = store_b.make_child_branch_id(
            root_b["uql_question_id"],
            root_b["branch_id"],
            "S3",
            "CONTRADICTION_FOUND",
            seq=0,
        )
        self.assertEqual(br1, br2)

        c1 = store_a.spawn_derived(contradiction_decision(root_a["uql_question_id"]))
        c2 = store_b.spawn_derived(contradiction_decision(root_b["uql_question_id"]))
        assert c1 is not None and c2 is not None
        self.assertEqual(c1["uql_question_id"], c2["uql_question_id"])
        self.assertEqual(c1["branch_id"], c2["branch_id"])

    def test_active_frontiers_and_provenance_flag(self):
        store, root = make_root()
        tips = store.list_active_frontiers()
        self.assertEqual(len(tips), 1)
        child = store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        assert child is not None
        tips = store.list_active_frontiers(root["uql_question_id"])
        ids = {t["uql_question_id"] for t in tips}
        self.assertIn(root["uql_question_id"], ids)
        self.assertIn(child["uql_question_id"], ids)

    def test_illegal_status_transition(self):
        store, root = make_root()
        with self.assertRaises(ValueError):
            store.set_status(root["uql_question_id"], "CLOSED_RESOLVED")
        store.set_status(root["uql_question_id"], "SUPERSEDED")
        with self.assertRaises(ValueError):
            store.set_status(root["uql_question_id"], "OPEN")

    def test_json_roundtrip(self):
        import os
        import tempfile

        store, root = make_root()
        store.spawn_derived(contradiction_decision(root["uql_question_id"]))
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "uql.json")
            store.save_json(path)
            loaded = UQLBranchStore.load_json(path)
        self.assertEqual(len(loaded.questions), len(store.questions))
        self.assertEqual(len(loaded.history), len(store.history))
        self.assertEqual(
            loaded.list_open_children(root["uql_question_id"])[0]["uql_question_id"],
            store.list_open_children(root["uql_question_id"])[0]["uql_question_id"],
        )


class TestR1StatusMachineSpec(unittest.TestCase):
    """Sanity: CLOSED_RESOLVED never reachable from transitions map alone."""

    def test_closed_resolved_not_in_any_target(self):
        for src, targets in STATUS_TRANSITIONS.items():
            self.assertNotIn(
                "CLOSED_RESOLVED",
                targets,
                msg=f"{src} must not transition to CLOSED_RESOLVED via R1",
            )


if __name__ == "__main__":
    unittest.main()
