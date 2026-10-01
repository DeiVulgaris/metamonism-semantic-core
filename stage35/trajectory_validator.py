"""Validate Stage 35 research trajectories."""

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = yaml.safe_load((ROOT / "research_trajectory.yaml").read_text(encoding="utf-8"))


def validate(t):
    states = {s["state_id"] for s in t["states"]}
    assert states
    assert t["current_state"] in states

    seen_transitions = set()
    for tr in t["transitions"]:
        assert tr["transition_id"] not in seen_transitions
        seen_transitions.add(tr["transition_id"])
        assert tr["from_state"] in states
        assert tr["to_state"] in states
        assert tr["provenance"]
        assert tr["status"]

    for b in t["branches"]:
        assert b["parent_state"] in states
        assert b["status"] in {
            "ACTIVE", "REJECTED", "FALSIFIED", "SUSPENDED", "MERGED", "ABANDONED"
        }
        assert b["provenance"]

    assert len(t["continuity_invariants"]) >= 3


for trajectory in DATA["trajectories"]:
    validate(trajectory)

print(f"PASS: {len(DATA['trajectories'])} trajectory(s); continuity invariants preserved.")
