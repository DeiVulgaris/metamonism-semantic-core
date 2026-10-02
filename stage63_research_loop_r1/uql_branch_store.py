"""
UQL Branch Store — Research Loop R1 (skeleton)

Durable derived questions, branch identity, append-only history.
Does NOT write ontology registries (id/claim/relation_registry).

R0 policy selects transitions; this store persists UQL process objects.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import json
import re


ACTIVE_QUESTION_STATUSES = frozenset(
    {
        "OPEN",
        "BLOCKED",
        "WAITING_INFORMATION",
        "WAITING_VALIDATION",
    }
)

# Status transitions allowed by R1 spec (target sets)
STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "OPEN": frozenset(
        {
            "WAITING_INFORMATION",
            "WAITING_VALIDATION",
            "BLOCKED",
            "SUPERSEDED",
            "RESOLVED_CANDIDATE",
            "CLOSED_TERMINATED",
        }
    ),
    "WAITING_INFORMATION": frozenset({"OPEN", "BLOCKED", "CLOSED_TERMINATED"}),
    "WAITING_VALIDATION": frozenset(
        {"OPEN", "RESOLVED_CANDIDATE", "CLOSED_TERMINATED"}
    ),
    "BLOCKED": frozenset({"OPEN", "CLOSED_TERMINATED"}),
    "RESOLVED_CANDIDATE": frozenset({"OPEN", "CLOSED_TERMINATED"}),
    "SUPERSEDED": frozenset(),
    "CLOSED_TERMINATED": frozenset(),
    "CLOSED_RESOLVED": frozenset(),
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(text: str, max_len: int = 48) -> str:
    s = text.lower().strip()
    s = re.sub(r"^uql:q:", "", s)
    s = re.sub(r"^q:", "", s)
    s = re.sub(r"[^a-z0-9]+", ".", s).strip(".")
    return (s[:max_len] or "q").strip(".")


@dataclass
class UQLBranchStore:
    """In-memory UQL ledger. Optional JSON path for load/save."""

    questions: dict[str, dict[str, Any]] = field(default_factory=dict)
    branches: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    _seq: dict[str, int] = field(default_factory=dict)

    # --- identity ---

    def _next_seq(self, key: str) -> int:
        n = self._seq.get(key, 0)
        self._seq[key] = n + 1
        return n

    def make_root_question_id(self, slug: str) -> str:
        return f"uql:q:{_slug(slug)}"

    def make_derived_question_id(
        self,
        parent_id: str,
        anchor_step: str,
        trigger: str,
        seq: Optional[int] = None,
    ) -> str:
        parent_slug = _slug(parent_id)
        trigger_slug = _slug(trigger, 32)
        if seq is None:
            key = f"dq:{parent_id}:{anchor_step}:{trigger}"
            seq = self._next_seq(key)
        return f"uql:q:{parent_slug}:d:{anchor_step}:{trigger_slug}:{seq}"

    def make_root_branch_id(self, root_question_id: str) -> str:
        return f"uql:br:{_slug(root_question_id)}:main"

    def make_child_branch_id(
        self,
        root_question_id: str,
        parent_branch_id: str,
        anchor_step: str,
        trigger: str,
        seq: Optional[int] = None,
    ) -> str:
        root_slug = _slug(root_question_id)
        parent_short = _slug(parent_branch_id, 24)
        trigger_slug = _slug(trigger, 24)
        if seq is None:
            key = f"br:{root_question_id}:{parent_branch_id}:{anchor_step}:{trigger}"
            seq = self._next_seq(key)
        return f"uql:br:{root_slug}:{parent_short}:{anchor_step}:{trigger_slug}:{seq}"

    def make_entry_id(self, uql_question_id: str, event_type: str) -> str:
        key = f"he:{uql_question_id}:{event_type}"
        seq = self._next_seq(key)
        return f"uql:he:{_slug(uql_question_id, 40)}:{event_type}:{seq}"

    # --- core writes ---

    def register_root(
        self,
        statement: str,
        unresolved_difference: str,
        constraints: Optional[list[str]] = None,
        slug: Optional[str] = None,
        created_from: str = "fixture",
        provenance: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create root question + main branch."""
        qid = self.make_root_question_id(slug or statement)
        if qid in self.questions:
            raise ValueError(f"root already exists: {qid}")
        bid = self.make_root_branch_id(qid)
        prov = {"ontology_write": False, **(provenance or {})}
        question = {
            "uql_question_id": qid,
            "statement": statement,
            "status": "OPEN",
            "branch_id": bid,
            "parent_uql_question_id": None,
            "root_uql_question_id": qid,
            "unresolved_difference": unresolved_difference,
            "constraints": list(constraints or []),
            "created_from": created_from,
            "origin_step_id": None,
            "origin_trigger": None,
            "derivation_basis": None,
            "provenance": prov,
        }
        branch = {
            "branch_id": bid,
            "root_uql_question_id": qid,
            "parent_branch_id": None,
            "origin_step_id": None,
            "origin_trigger": None,
            "status": "ACTIVE",
            "tip_uql_question_id": qid,
        }
        self.questions[qid] = question
        self.branches[bid] = branch
        self.append_history(
            qid,
            bid,
            "NOTE",
            {"event": "root_registered", "statement": statement},
        )
        return deepcopy(question)

    def append_history(
        self,
        uql_question_id: str,
        branch_id: str,
        event_type: str,
        payload: dict[str, Any],
        timestamp: Optional[str] = None,
    ) -> dict[str, Any]:
        if uql_question_id not in self.questions:
            raise KeyError(f"unknown question: {uql_question_id}")
        entry = {
            "entry_id": self.make_entry_id(uql_question_id, event_type),
            "uql_question_id": uql_question_id,
            "branch_id": branch_id,
            "event_type": event_type,
            "timestamp": timestamp or _utc_now(),
            "payload": deepcopy(payload),
        }
        self.history.append(entry)
        return deepcopy(entry)

    def set_status(self, uql_question_id: str, new_status: str) -> dict[str, Any]:
        q = self.questions[uql_question_id]
        old = q["status"]
        if new_status == "CLOSED_RESOLVED":
            raise ValueError(
                "CLOSED_RESOLVED requires external validation gate; not set by R1 store alone"
            )
        allowed = STATUS_TRANSITIONS.get(old, frozenset())
        if new_status not in allowed and new_status != old:
            raise ValueError(f"illegal transition {old} → {new_status}")
        q["status"] = new_status
        self.append_history(
            uql_question_id,
            q["branch_id"],
            "STATUS_CHANGE",
            {"from": old, "to": new_status},
        )
        if new_status == "CLOSED_TERMINATED":
            br = self.branches.get(q["branch_id"])
            if br and not self.list_open_children(uql_question_id):
                # close branch only if this tip is closed and no open children of this node
                pass  # branch lifecycle refined in full implementation
        return deepcopy(q)

    def spawn_derived(self, policy_decision: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Apply R0 policy_decision:
        - always record POLICY_DECISION / OPERATION_SELECTED on active question
        - if derived_question present, spawn child + branch
        - if terminate, close active question only (not siblings)
        Returns child question or None.
        """
        parent_ref = policy_decision.get("uql_question_id") or policy_decision["question_id"]
        parent = self._resolve_question(parent_ref)
        parent_id = parent["uql_question_id"]
        branch_id = parent["branch_id"]

        self.append_history(
            parent_id,
            branch_id,
            "POLICY_DECISION",
            {
                "selected_operation": policy_decision.get("selected_operation"),
                "rationale_codes": policy_decision.get("rationale_codes"),
                "result_class": policy_decision.get("result_class"),
            },
        )
        self.append_history(
            parent_id,
            branch_id,
            "OPERATION_SELECTED",
            {"operation": policy_decision.get("selected_operation")},
        )

        op = policy_decision.get("selected_operation")
        if op == "terminate":
            self.set_status(parent_id, "CLOSED_TERMINATED")
            return None

        derived = policy_decision.get("derived_question")
        if not derived:
            return None

        anchor = (
            derived.get("derived_from_step")
            or policy_decision.get("anchor_step_id")
            or "S?"
        )
        trigger = derived.get("trigger") or policy_decision.get("result_class") or "DERIVED"
        child_id = self.make_derived_question_id(parent_id, str(anchor), str(trigger))
        child_branch = self.make_child_branch_id(
            parent["root_uql_question_id"],
            branch_id,
            str(anchor),
            str(trigger),
        )

        constraints = list(
            derived.get("constraints")
            or parent.get("constraints")
            or []
        )
        statement = derived.get("statement") or derived.get("unresolved_difference") or "derived"
        child = {
            "uql_question_id": child_id,
            "statement": statement,
            "status": "OPEN",
            "branch_id": child_branch,
            "parent_uql_question_id": parent_id,
            "root_uql_question_id": parent["root_uql_question_id"],
            "unresolved_difference": derived.get("unresolved_difference") or statement,
            "constraints": constraints,
            "created_from": "policy_decision",
            "origin_step_id": str(anchor),
            "origin_trigger": str(trigger),
            "derivation_basis": derived.get("derivation_basis"),
            "provenance": {
                "ontology_write": False,
                "parent_question": parent_id,
                "policy_question_id": policy_decision.get("question_id"),
            },
        }
        branch = {
            "branch_id": child_branch,
            "root_uql_question_id": parent["root_uql_question_id"],
            "parent_branch_id": branch_id,
            "origin_step_id": str(anchor),
            "origin_trigger": str(trigger),
            "status": "ACTIVE",
            "tip_uql_question_id": child_id,
        }
        self.questions[child_id] = child
        self.branches[child_branch] = branch

        self.append_history(
            parent_id,
            branch_id,
            "DERIVED_QUESTION_SPAWNED",
            {"child_uql_question_id": child_id, "child_branch_id": child_branch},
        )
        self.append_history(
            child_id,
            child_branch,
            "NOTE",
            {"event": "spawned", "parent": parent_id},
        )
        return deepcopy(child)

    def _resolve_question(self, ref: str) -> dict[str, Any]:
        if ref in self.questions:
            return self.questions[ref]
        # allow external question_id alias via provenance match
        for q in self.questions.values():
            if q.get("provenance", {}).get("policy_question_id") == ref:
                return q
            if q["uql_question_id"] == ref or q["uql_question_id"].endswith(ref):
                return q
        # try slug root registration style uql:q:{slug} from q:...
        candidate = self.make_root_question_id(ref)
        if candidate in self.questions:
            return self.questions[candidate]
        raise KeyError(f"unknown question ref: {ref}")

    # --- queries ---

    def list_active_frontiers(
        self, root_uql_question_id: Optional[str] = None
    ) -> list[dict[str, Any]]:
        out = []
        for q in self.questions.values():
            if q["status"] not in ACTIVE_QUESTION_STATUSES:
                continue
            if root_uql_question_id and q["root_uql_question_id"] != root_uql_question_id:
                continue
            out.append(deepcopy(q))
        return out

    def get_lineage(self, uql_question_id: str) -> list[dict[str, Any]]:
        chain: list[dict[str, Any]] = []
        seen: set[str] = set()
        cur: Optional[str] = uql_question_id
        while cur and cur not in seen:
            seen.add(cur)
            q = self.questions[cur]
            chain.append(deepcopy(q))
            cur = q.get("parent_uql_question_id")
        chain.reverse()
        return chain

    def list_open_children(self, parent_uql_question_id: str) -> list[dict[str, Any]]:
        return [
            deepcopy(q)
            for q in self.questions.values()
            if q.get("parent_uql_question_id") == parent_uql_question_id
            and q["status"] in ACTIVE_QUESTION_STATUSES
        ]

    def get_branch(self, branch_id: str) -> dict[str, Any]:
        return deepcopy(self.branches[branch_id])

    def history_for(self, uql_question_id: str) -> list[dict[str, Any]]:
        return [deepcopy(e) for e in self.history if e["uql_question_id"] == uql_question_id]

    # --- persistence helpers ---

    def to_dict(self) -> dict[str, Any]:
        return {
            "questions": self.questions,
            "branches": self.branches,
            "history": self.history,
            "seq": self._seq,
        }

    def save_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "UQLBranchStore":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        store = cls()
        store.questions = data.get("questions", {})
        store.branches = data.get("branches", {})
        store.history = data.get("history", [])
        store._seq = data.get("seq", {})
        return store


# --- minimal smoke (not full test suite) ---

def _smoke() -> None:
    store = UQLBranchStore()
    root = store.register_root(
        statement="Local Failure ≠ Process Termination",
        unresolved_difference="Can successor P_n+1 be constructed after STUCK?",
        constraints=["Local Failure ≠ Process Termination"],
        slug="continuity.local_failure",
    )
    decision = {
        "question_id": "q:continuity.local_failure_vs_termination.v1",
        "uql_question_id": root["uql_question_id"],
        "selected_operation": "diff",
        "rationale_codes": ["CONTRADICTION_REQUIRES_REDIFFERENTIATION"],
        "result_class": "CONTRADICTION_FOUND",
        "anchor_step_id": "S3",
        "derived_question": {
            "derived_from_step": "S3",
            "trigger": "CONTRADICTION_FOUND",
            "unresolved_difference": "Reconcile handoff contradiction at S3",
            "derivation_basis": "CONTRADICTION_FOUND against S3",
            "constraints": root["constraints"],
        },
    }
    child = store.spawn_derived(decision)
    assert child is not None
    assert child["parent_uql_question_id"] == root["uql_question_id"]
    assert len(store.list_open_children(root["uql_question_id"])) == 1
    assert len(store.get_lineage(child["uql_question_id"])) == 2
    print("smoke OK", child["uql_question_id"])


if __name__ == "__main__":
    _smoke()
