"""Stage 35 — Research Trajectory Memory.

The trajectory engine records state transitions without rewriting history.
It is intentionally conservative: it stores transitions and validates
continuity; it does not infer truth from chronology.
"""

from copy import deepcopy


ALLOWED_RELATIONS = {
    "FOLLOWS", "REVISES", "TESTS", "FALSIFIES", "BLOCKS",
    "REOPENS", "BRANCHES", "MERGES", "REFERENCES",
}


def index_states(trajectory):
    return {s["state_id"]: s for s in trajectory["states"]}


def index_transitions(trajectory):
    return {t["transition_id"]: t for t in trajectory["transitions"]}


def validate_trajectory(trajectory):
    states = index_states(trajectory)
    transitions = index_transitions(trajectory)

    assert trajectory["trajectory_id"]
    assert trajectory["program_id"]
    assert trajectory["current_state"] in states

    for t in trajectory["transitions"]:
        assert t["from_state"] in states
        assert t["to_state"] in states
        assert t["status"]
        assert t["provenance"]

    for b in trajectory["branches"]:
        assert b["parent_state"] in states
        assert b["status"] in {
            "ACTIVE", "REJECTED", "FALSIFIED", "SUSPENDED",
            "MERGED", "ABANDONED",
        }
        assert b["provenance"]

    return True


def append_transition(trajectory, transition, new_state):
    """Return a new trajectory with an appended state and transition.

    Existing states and transitions are never mutated.
    """
    validate_trajectory(trajectory)

    old = deepcopy(trajectory)
    state_ids = index_states(old)

    if new_state["state_id"] in state_ids:
        raise ValueError("state already exists; trajectory is append-only")

    if transition["from_state"] != old["current_state"]:
        raise ValueError("transition must start at current_state")

    if transition["to_state"] != new_state["state_id"]:
        raise ValueError("transition target must equal new state")

    old["states"].append(deepcopy(new_state))
    old["transitions"].append(deepcopy(transition))
    old["current_state"] = new_state["state_id"]

    validate_trajectory(old)
    return old


def reopen_question(trajectory, previous_state_id, new_state):
    """Create a new state that reopens an earlier question.

    The earlier state remains untouched.
    """
    states = index_states(trajectory)
    if previous_state_id not in states:
        raise KeyError(previous_state_id)

    transition = {
        "transition_id": f"{trajectory['trajectory_id']}.reopen.{len(trajectory['transitions'])}",
        "from_state": trajectory["current_state"],
        "to_state": new_state["state_id"],
        "action": "REOPEN",
        "trigger": f"Question reopened from {previous_state_id}",
        "evidence": [f"reference:{previous_state_id}"],
        "status": "UNRESOLVED",
        "provenance": new_state["provenance"],
    }
    return append_transition(trajectory, transition, new_state)


def summarize_trajectory(trajectory):
    validate_trajectory(trajectory)
    return {
        "trajectory_id": trajectory["trajectory_id"],
        "program_id": trajectory["program_id"],
        "state_count": len(trajectory["states"]),
        "transition_count": len(trajectory["transitions"]),
        "branch_count": len(trajectory["branches"]),
        "current_state": trajectory["current_state"],
        "continuity_invariants": trajectory["continuity_invariants"],
    }


if __name__ == "__main__":
    import yaml
    from pathlib import Path

    data = yaml.safe_load(
        (Path(__file__).parent / "research_trajectory.yaml").read_text(encoding="utf-8")
    )

    for trajectory in data["trajectories"]:
        print(summarize_trajectory(trajectory))
