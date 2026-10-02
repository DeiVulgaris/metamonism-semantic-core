#!/usr/bin/env python3
"""Minimal in-memory UQL-compatible branch store for Research Loop R1.

This is a skeleton, not a replacement for the existing UFCPS UQLStore.

Responsibilities:
- durable-shaped question objects;
- explicit branch lineage;
- append-only history;
- active frontier index;
- spawning a derived question from an R0 policy decision.

Non-responsibilities:
- ontology writes;
- claim elevation;
- semantic rewriting;
- automatic branch merge;
- autonomous policy selection;
- execution.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping


QUESTION_STATUSES = {"OPEN", "CLOSED"}
BRANCH_STATUSES = {"ACTIVE", "CLOSED"}


class UQLBranchStoreError(ValueError):
    """Base store error."""


class UQLNotFound(UQLBranchStoreError):
    """Requested UQL object does not exist."""


class UQLBranchStore:
    """In-memory UQL-shaped ledger with explicit append-only history."""

    def __init__(self) -> None:
        self.questions: dict[str, dict[str, Any]] = {}
        self.branches: dict[str, dict[str, Any]] = {}
        self.history: list[dict[str, Any]] = []
        self.frontier: dict[str, list[str]] = {
            "active_branch_ids": [],
            "active_tip_question_ids": [],
        }

    # ------------------------------------------------------------------
    # Root registration
    # ------------------------------------------------------------------
    def register_root(
        self,
        *,
        uql_question_id: str,
        question: str,
        unresolved_difference: str,
        constraints: list[str] | None = None,
        source: str | None = None,
        branch_id: str | None = None,
    ) -> dict[str, Any]:
        if uql_question_id in self.questions:
            raise UQLBranchStoreError(
                f"question already exists: {uql_question_id}"
            )
        root_branch_id = branch_id or f"br:{uql_question_id}"
        if root_branch_id in self.branches:
            raise UQLBranchStoreError(
                f"branch already exists: {root_branch_id}"
            )

        now = self._now()
        question_obj = {
            "uql_question_id": uql_question_id,
            "status": "OPEN",
            "branch_id": root_branch_id,
            "root_question_id": uql_question_id,
            "parent_question_id": None,
            "question": question,
            "unresolved_difference": unresolved_difference,
            "constraints": list(constraints or []),
            "provenance": {
                "parent_question": None,
                "derived_from_step": None,
                "trigger": None,
                "derivation_basis": "ROOT_REGISTRATION",
                "source": source,
                "ontology_write": False,
                "claim_elevate": False,
            },
        }
        branch_obj = {
            "branch_id": root_branch_id,
            "root_question_id": uql_question_id,
            "parent_branch_id": None,
            "origin_step_id": None,
            "origin_trigger": None,
            "tip_question_id": uql_question_id,
            "status": "ACTIVE",
            "lineage": [root_branch_id],
        }

        self.questions[uql_question_id] = question_obj
        self.branches[root_branch_id] = branch_obj
        self._history(
            event_type="ROOT_REGISTERED",
            uql_question_id=uql_question_id,
            branch_id=root_branch_id,
            payload={"source": source},
        )
        self._refresh_frontier()
        return deepcopy(question_obj)

    # ------------------------------------------------------------------
    # Derived-question spawn
    # ------------------------------------------------------------------
    def spawn_derived(
        self,
        policy_decision: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Persist an R0 derived question as a new branch.

        The method accepts only an R0-shaped decision and never creates an
        ontology or claim write. A null derived_question is a no-op.
        """
        decision = policy_decision.get("policy_decision", policy_decision)
        if not isinstance(decision, Mapping):
            raise UQLBranchStoreError("policy_decision must be an object")

        derived = decision.get("derived_question")
        if derived is None:
            return {
                "spawned": False,
                "reason": "NO_DERIVED_QUESTION",
                "question": None,
            }
        if not isinstance(derived, Mapping):
            raise UQLBranchStoreError("derived_question must be an object")

        parent_question_id = self._require(
            decision.get("question_id"),
            "policy_decision.question_id",
        )
        derived_id = self._require(
            derived.get("question_id"),
            "derived_question.question_id",
        )
        if parent_question_id not in self.questions:
            raise UQLNotFound(f"parent question not found: {parent_question_id}")
        if derived_id in self.questions:
            raise UQLBranchStoreError(f"question already exists: {derived_id}")

        parent = self.questions[parent_question_id]
        parent_branch_id = str(parent["branch_id"])
        parent_branch = self.branches[parent_branch_id]

        derived_from_step = self._require(
            derived.get("derived_from_step"),
            "derived_question.derived_from_step",
        )
        trigger = self._require(
            derived.get("trigger"),
            "derived_question.trigger",
        )
        status = self._require(derived.get("status"), "derived_question.status")
        if status != "OPEN":
            raise UQLBranchStoreError(
                "R1 spawn accepts only OPEN derived questions"
            )

        branch_id = f"br:{derived_id}"
        if branch_id in self.branches:
            raise UQLBranchStoreError(f"branch already exists: {branch_id}")

        inherited_constraints = list(
            derived.get("constraints")
            or parent.get("constraints")
            or []
        )

        question_obj = {
            "uql_question_id": derived_id,
            "status": "OPEN",
            "branch_id": branch_id,
            "root_question_id": str(parent["root_question_id"]),
            "parent_question_id": parent_question_id,
            "question": (
                str(derived.get("unresolved_difference"))
                if derived.get("unresolved_difference")
                else str(derived_id)
            ),
            "unresolved_difference": self._require(
                derived.get("unresolved_difference"),
                "derived_question.unresolved_difference",
            ),
            "constraints": inherited_constraints,
            "provenance": {
                "parent_question": parent_question_id,
                "derived_from_step": derived_from_step,
                "trigger": trigger,
                "derivation_basis": self._require(
                    derived.get("derivation_basis"),
                    "derived_question.derivation_basis",
                ),
                "source": None,
                "ontology_write": False,
                "claim_elevate": False,
            },
        }

        branch_obj = {
            "branch_id": branch_id,
            "root_question_id": str(parent["root_question_id"]),
            "parent_branch_id": parent_branch_id,
            "origin_step_id": derived_from_step,
            "origin_trigger": trigger,
            "tip_question_id": derived_id,
            "status": "ACTIVE",
            "lineage": list(parent_branch["lineage"]) + [branch_id],
        }

        self.questions[derived_id] = question_obj
        self.branches[branch_id] = branch_obj

        self._history(
            event_type="DERIVED_QUESTION_SPAWNED",
            uql_question_id=derived_id,
            branch_id=branch_id,
            payload={
                "parent_question_id": parent_question_id,
                "parent_branch_id": parent_branch_id,
                "origin_step_id": derived_from_step,
                "trigger": trigger,
            },
        )
        self._refresh_frontier()

        return {
            "spawned": True,
            "question": deepcopy(question_obj),
            "branch": deepcopy(branch_obj),
        }

    # ------------------------------------------------------------------
    # Append-only history
    # ------------------------------------------------------------------
    def append_history(
        self,
        *,
        event_type: str,
        uql_question_id: str,
        branch_id: str,
        payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._ensure_question_branch(uql_question_id, branch_id)
        return self._history(
            event_type=event_type,
            uql_question_id=uql_question_id,
            branch_id=branch_id,
            payload=payload or {},
        )

    def _history(
        self,
        *,
        event_type: str,
        uql_question_id: str,
        branch_id: str,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        event_id = f"ev:{len(self.history) + 1:06d}"
        previous_event_id = (
            self.history[-1]["event_id"] if self.history else None
        )
        entry = {
            "event_id": event_id,
            "event_type": event_type,
            "occurred_on": self._now(),
            "uql_question_id": uql_question_id,
            "branch_id": branch_id,
            "payload": deepcopy(dict(payload)),
            "previous_event_id": previous_event_id,
            "sequence": len(self.history),
        }
        self.history.append(entry)
        return deepcopy(entry)

    # ------------------------------------------------------------------
    # Status / lineage / frontier
    # ------------------------------------------------------------------
    def set_question_status(self, uql_question_id: str, status: str) -> dict[str, Any]:
        question = self._question(uql_question_id)
        if status not in QUESTION_STATUSES:
            raise UQLBranchStoreError(f"invalid question status: {status}")
        if question["status"] == status:
            return deepcopy(question)

        previous = question["status"]
        question["status"] = status
        self._history(
            event_type="QUESTION_STATUS_CHANGED",
            uql_question_id=uql_question_id,
            branch_id=str(question["branch_id"]),
            payload={"from": previous, "to": status},
        )
        self._refresh_frontier()
        return deepcopy(question)

    def set_branch_status(self, branch_id: str, status: str) -> dict[str, Any]:
        branch = self._branch(branch_id)
        if status not in BRANCH_STATUSES:
            raise UQLBranchStoreError(f"invalid branch status: {status}")
        if branch["status"] == status:
            return deepcopy(branch)

        previous = branch["status"]
        branch["status"] = status
        self._history(
            event_type="BRANCH_STATUS_CHANGED",
            uql_question_id=str(branch["tip_question_id"]),
            branch_id=branch_id,
            payload={"from": previous, "to": status},
        )
        self._refresh_frontier()
        return deepcopy(branch)

    def get_lineage(self, uql_question_id: str) -> list[dict[str, Any]]:
        question = self._question(uql_question_id)
        branch_id = str(question["branch_id"])
        branch = self._branch(branch_id)
        result: list[dict[str, Any]] = []

        for lineage_branch_id in branch["lineage"]:
            lineage_branch = self._branch(lineage_branch_id)
            tip_id = lineage_branch["tip_question_id"]
            result.append(self._question(str(tip_id)))
        return result

    def list_active_frontier(self) -> dict[str, Any]:
        return {
            "active_branch_ids": list(self.frontier["active_branch_ids"]),
            "active_tip_question_ids": list(self.frontier["active_tip_question_ids"]),
        }

    # ------------------------------------------------------------------
    # Inspection / persistence
    # ------------------------------------------------------------------
    def snapshot(self) -> dict[str, Any]:
        return {
            "questions": deepcopy(self.questions),
            "branches": deepcopy(self.branches),
            "history": deepcopy(self.history),
            "frontier": deepcopy(self.frontier),
        }

    def save_json(self, path: str | Path) -> None:
        target = Path(path)
        target.write_text(
            json.dumps(self.snapshot(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_json(cls, path: str | Path) -> "UQLBranchStore":
        target = Path(path)
        data = json.loads(target.read_text(encoding="utf-8"))
        store = cls()
        store.questions = dict(data.get("questions", {}))
        store.branches = dict(data.get("branches", {}))
        store.history = list(data.get("history", []))
        store.frontier = {
            "active_branch_ids": list(
                data.get("frontier", {}).get("active_branch_ids", [])
            ),
            "active_tip_question_ids": list(
                data.get("frontier", {}).get("active_tip_question_ids", [])
            ),
        }
        return store

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _require(value: Any, field: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise UQLBranchStoreError(f"missing required field: {field}")
        return text

    def _question(self, uql_question_id: str) -> dict[str, Any]:
        try:
            return self.questions[uql_question_id]
        except KeyError as exc:
            raise UQLNotFound(
                f"question not found: {uql_question_id}"
            ) from exc

    def _branch(self, branch_id: str) -> dict[str, Any]:
        try:
            return self.branches[branch_id]
        except KeyError as exc:
            raise UQLNotFound(f"branch not found: {branch_id}") from exc

    def _ensure_question_branch(
        self,
        uql_question_id: str,
        branch_id: str,
    ) -> None:
        question = self._question(uql_question_id)
        branch = self._branch(branch_id)
        if str(question["branch_id"]) != branch_id:
            raise UQLBranchStoreError(
                "question does not belong to supplied branch"
            )
        if str(branch["branch_id"]) != branch_id:
            raise UQLBranchStoreError(
                "branch identifier mismatch"
            )

    def _refresh_frontier(self) -> None:
        active_branches = [
            branch_id
            for branch_id, branch in self.branches.items()
            if branch.get("status") == "ACTIVE"
        ]
        active_tips = [
            str(self.branches[branch_id]["tip_question_id"])
            for branch_id in active_branches
            if self.branches[branch_id].get("tip_question_id")
            and self.questions.get(
                str(self.branches[branch_id]["tip_question_id"]),
                {},
            ).get("status") == "OPEN"
        ]
        self.frontier = {
            "active_branch_ids": active_branches,
            "active_tip_question_ids": active_tips,
        }


__all__ = [
    "UQLBranchStore",
    "UQLBranchStoreError",
    "UQLNotFound",
]
