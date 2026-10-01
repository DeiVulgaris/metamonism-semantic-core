"""Stage 38 — Research Frontier -> Research Task Engine.

Instantiates research obligations from admissible frontier transitions.
It does not solve research, select truth, or manufacture evidence.
Selection policy is outside this module.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

@dataclass
class ResearchTask:
    task_id: str
    frontier_id: str
    research_program_id: str
    trajectory_id: str
    transition_type: str
    task_state: str
    objective: str
    why_now: str
    prerequisites: List[str]
    expected_output: str
    provenance: Dict[str, str]
    transition_status: str = "AVAILABLE"
    epistemic_status: str = ""
    unresolved_difference: str = ""
    constraints: List[str] = None
    forbidden_outcomes: List[str] = None
    derived_from: List[str] = None

    def to_dict(self):
        d = asdict(self)
        d["constraints"] = d["constraints"] or []
        d["forbidden_outcomes"] = d["forbidden_outcomes"] or []
        d["derived_from"] = d["derived_from"] or []
        return d

def _task_state(status):
    return {"AVAILABLE":"READY","CONDITIONAL":"PROPOSED","BLOCKED":"BLOCKED","PROHIBITED":"PROHIBITED"}[status]

def _objective(frontier, transition_type):
    diff = frontier["unresolved_difference"]
    return {
        "DEFINE": f"Define the missing structure required to resolve: {diff}",
        "FORMALIZE": f"Construct a formal representation addressing: {diff}",
        "TEST": f"Design or execute a test capable of discriminating the unresolved difference: {diff}",
        "COMPARE": f"Compare the relevant structures without collapsing semantic status: {diff}",
        "DERIVE": f"Attempt a traceable derivation concerning: {diff}",
        "COUNTEREXAMPLE": f"Search for a counterexample to the working hypothesis concerning: {diff}",
        "REPLICATE": f"Replicate the relevant result while preserving provenance: {diff}",
        "BRANCH": f"Instantiate an explicit alternative hypothesis for: {diff}",
        "COMPOSE": f"Test controlled composition of the relevant structures for: {diff}",
        "DELEGATE": f"Prepare a carrier-independent research handoff for: {diff}",
        "REFRAME": f"Reframe or decompose the unresolved difference without resolving it by assumption: {diff}",
        "TERMINATE": f"Document a justified termination decision for: {diff}",
    }[transition_type]

def generate_tasks(frontier: Dict[str, Any]) -> List[Dict[str, Any]]:
    required = ["frontier_id","research_program_id","trajectory_id","frontier_state","unresolved_difference","provenance","admissible_transitions"]
    missing = [k for k in required if k not in frontier]
    if missing:
        raise ValueError(f"frontier missing required fields: {missing}")
    tasks = []
    for index, transition in enumerate(frontier["admissible_transitions"]):
        status = transition["status"]
        task = ResearchTask(
            task_id=f"{frontier['frontier_id']}.task.{index:03d}",
            frontier_id=frontier["frontier_id"],
            research_program_id=frontier["research_program_id"],
            trajectory_id=frontier["trajectory_id"],
            transition_type=transition["type"],
            transition_status=status,
            task_state=_task_state(status),
            objective=_objective(frontier, transition["type"]),
            why_now=transition.get("reason") or f"Transition {transition['type']} is admissible at the current frontier.",
            unresolved_difference=frontier["unresolved_difference"],
            prerequisites=transition.get("prerequisites", []),
            constraints=frontier.get("constraints", []) + frontier.get("blockers", []),
            expected_output="New evidence, definition, comparison, derivation, counterexample, branch, or explicit unresolved state relevant to the frontier.",
            forbidden_outcomes=[
                "Do not upgrade epistemic status merely by completing the task.",
                "Do not infer identity or formal isomorphism from structural similarity.",
                "Do not erase prior frontier state or provenance."
            ],
            provenance=frontier["provenance"],
            epistemic_status=frontier.get("epistemic_status", ""),
            derived_from=frontier.get("derived_from", []),
        )
        tasks.append(task.to_dict())
    return tasks

def ready_tasks(frontier):
    return [t for t in generate_tasks(frontier) if t["task_state"] == "READY"]

def next_task(frontier):
    ready = ready_tasks(frontier)
    if not ready:
        return {"selected":False,"reason":"No READY research task exists at the current frontier.","alternatives":generate_tasks(frontier)}
    return {
        "selected":False,
        "reason":"Selection policy is external; this is only a candidate.",
        "candidate":ready[0],
        "alternatives":ready[1:],
    }

if __name__ == "__main__":
    import json, sys
    frontier = json.load(open(sys.argv[1], encoding="utf-8"))
    print(json.dumps(generate_tasks(frontier), indent=2, ensure_ascii=False))
