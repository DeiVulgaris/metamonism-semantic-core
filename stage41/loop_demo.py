"""Stage 41: end-to-end demonstrator for the research loop."""

from copy import deepcopy
from stage38.frontier_task_engine import generate_tasks
from stage40.selection_policy import select_tasks
from stage39.result_validator import validate_result

PROV = {
    "repository": "DeiVulgaris/metamonism-semantic-core",
    "path": "stage41/loop_demo.py",
    "ref": "stage41-research-loop-demonstrator",
    "locator": "controlled end-to-end demonstration",
}

def normalize_frontier(raw, program_id, trajectory_id):
    f = deepcopy(raw)
    f["research_program_id"] = program_id
    f["trajectory_id"] = trajectory_id
    return f

def make_result(task, frontier, result_class, state, difference, interpretation, blockers=None):
    successor = {
        "frontier_id": frontier["frontier_id"] + ".next",
        "research_program_id": frontier["research_program_id"],
        "trajectory_id": frontier["trajectory_id"],
        "frontier_state": state,
        "epistemic_status": frontier.get("epistemic_status"),
        "subject": frontier["subject"],
        "unresolved_difference": difference,
        "evidence": ["stage41:controlled-execution"],
        "provenance": PROV,
        "derived_from": ["frontier:" + frontier["frontier_id"], "task:" + task["task_id"]],
        "constraints": frontier.get("constraints", []),
        "blockers": blockers or [],
        "open_questions": frontier.get("open_questions", []),
        "admissible_transitions": [],
    }
    return {
        "result_id": task["task_id"] + ".result",
        "task_id": task["task_id"],
        "frontier_id": frontier["frontier_id"],
        "research_program_id": frontier["research_program_id"],
        "trajectory_id": frontier["trajectory_id"],
        "result_class": result_class,
        "task_state_after": "COMPLETED",
        "epistemic_status": frontier.get("epistemic_status"),
        "observation": interpretation,
        "interpretation": interpretation,
        "unresolved_difference": difference,
        "evidence": ["stage41:controlled-execution"],
        "successor_frontier": successor,
        "provenance": PROV,
        "derived_from": ["task:" + task["task_id"]],
    }

def run_case(name, frontier, policy, metrics, result_spec):
    tasks = generate_tasks(frontier)
    decision = select_tasks(tasks, policy, context=metrics, decision_id="stage41."+name, provenance=PROV)
    assert decision["status"] == "SELECTED", decision
    selected_id = decision["selected_task_ids"][0]
    task = next(t for t in tasks if t["task_id"] == selected_id)

    result = make_result(task, frontier, **result_spec)
    validate_result(result)

    return {
        "case": name,
        "frontier_before": frontier["frontier_id"],
        "task_count": len(tasks),
        "selected_task": selected_id,
        "policy": policy,
        "result_class": result["result_class"],
        "frontier_after": result["successor_frontier"]["frontier_id"],
        "frontier_state_after": result["successor_frontier"]["frontier_state"],
        "epistemic_status_after": result["successor_frontier"].get("epistemic_status"),
        "old_frontier_preserved": True,
        "canonical_upgrade": False,
        "result": result,
    }

def main():
    r1 = {
        "frontier_id":"RF-r1r4-dirac-demo",
        "research_program_id":"RP-r1r4-dirac",
        "trajectory_id":"RT-r1r4-dirac-demo",
        "frontier_state":"UNTESTED",
        "epistemic_status":"THEORETICAL_HYPOTHESIS",
        "subject":{"ref":"mm:research.r1_r4_dirac","label":"R1-R4 / Dirac structural hypothesis"},
        "unresolved_difference":"Can the R1-R4 recursive structure admit a formal correspondence with a Clifford/Dirac algebra?",
        "provenance":PROV,
        "derived_from":["stage32:R1-R4-DIRAC-01"],
        "blockers":["formal representation of R1-R4"],
        "open_questions":["What is the algebraic operation?","What is the metric/signature?","Is there a Clifford representation?"],
        "admissible_transitions":[
            {"type":"DEFINE","status":"AVAILABLE","prerequisites":["algebraic operation"]},
            {"type":"FORMALIZE","status":"CONDITIONAL","prerequisites":["state space","algebraic operation"]},
            {"type":"COMPARE","status":"AVAILABLE","prerequisites":["defined R1-R4 structure"]},
            {"type":"COUNTEREXAMPLE","status":"AVAILABLE","prerequisites":["explicit candidate correspondence"]},
        ],
    }

    ricci = {
        "frontier_id":"RF-ricci-planck-demo",
        "research_program_id":"RP-ricci-planck",
        "trajectory_id":"RT-ricci-planck-demo",
        "frontier_state":"UNTESTED",
        "epistemic_status":"THEORETICAL_HYPOTHESIS",
        "subject":{"ref":"mm:research.ricci_planck","label":"Frustration / Ricci surgery / Planck-scale hypothesis"},
        "unresolved_difference":"Can a mathematically defined frustration-to-surgery transition yield a characteristic scale independently comparable with the Planck scale?",
        "provenance":PROV,
        "derived_from":["stage32:RICCI-SURGERY-PLANCK-02"],
        "blockers":["ontodynamic state space","surgery operator"],
        "open_questions":["Define state space.","Define surgery.","Derive scale independently.","Check dimensions."],
        "admissible_transitions":[
            {"type":"DEFINE","status":"AVAILABLE","prerequisites":["state space"]},
            {"type":"FORMALIZE","status":"CONDITIONAL","prerequisites":["state space","surgery operator"]},
            {"type":"COUNTEREXAMPLE","status":"AVAILABLE","prerequisites":["candidate scale relation"]},
        ],
    }

    cases = [
        run_case(
            "r1_r4_formalization",
            r1,
            "DEPENDENCY_FIRST",
            {
                r1["frontier_id"]+".task.000":{"dependency_depth":0},
                r1["frontier_id"]+".task.002":{"dependency_depth":2},
                r1["frontier_id"]+".task.003":{"dependency_depth":3},
            },
            {
                "result_class":"INCONCLUSIVE",
                "state":"UNRESOLVED",
                "difference":"Does the defined closure operator admit a Clifford-compatible representation?",
                "interpretation":"A candidate formal structure can be specified, but the Clifford-compatible closure relation remains unproved.",
            },
        ),
        run_case(
            "ricci_definition",
            ricci,
            "USER_SELECTED",
            {},
            {
                "result_class":"BLOCKED",
                "state":"BLOCKED",
                "difference":"How should the ontodynamic state space and surgery operator be defined?",
                "interpretation":"Execution cannot proceed until the state space and surgery operator are explicitly defined.",
                "blockers":["missing ontodynamic state space","missing surgery operator"],
            },
        ),
    ]

    return {"stage":41,"status":"PASS","cases":cases}

if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2, ensure_ascii=False))
