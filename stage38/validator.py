#!/usr/bin/env python3
"""Stage 38 validator: Research Task structural integrity."""

import json
import sys

TRANSITIONS={"DEFINE","FORMALIZE","TEST","COMPARE","DERIVE","COUNTEREXAMPLE","REPLICATE","BRANCH","COMPOSE","DELEGATE","REFRAME","TERMINATE"}
TRANSITION_STATUS={"AVAILABLE","CONDITIONAL","BLOCKED","PROHIBITED"}
TASK_STATES={"PROPOSED","READY","BLOCKED","PROHIBITED","IN_PROGRESS","COMPLETED","FAILED","REJECTED"}
NON_SOURCE={"INFERENCE","FORMALIZATION","THEORETICAL_HYPOTHESIS","PROPOSAL","UNRESOLVED","CONFLICT","USED_BUT_UNDEFINED","PRIOR_THEORETICAL_FORMULATION","MODEL_SPECIFIC"}

def validate(task):
    errors=[]
    required=["task_id","frontier_id","research_program_id","trajectory_id","transition_type","task_state","objective","why_now","prerequisites","expected_output","provenance"]
    for k in required:
        if k not in task: errors.append(f"missing required field: {k}")
    if task.get("transition_type") not in TRANSITIONS: errors.append("invalid transition_type")
    if task.get("task_state") not in TASK_STATES: errors.append("invalid task_state")
    if task.get("transition_status") not in TRANSITION_STATUS: errors.append("invalid transition_status")
    for k in ("repository","path","ref","locator"):
        if not task.get("provenance",{}).get(k): errors.append(f"provenance.{k} is required")
    if task.get("epistemic_status") in NON_SOURCE and not task.get("derived_from"):
        errors.append("non-SOURCE task requires derived_from")
    expected={"AVAILABLE":"READY","CONDITIONAL":"PROPOSED","BLOCKED":"BLOCKED","PROHIBITED":"PROHIBITED"}
    status=task.get("transition_status")
    if status in expected and task.get("task_state") != expected[status]:
        errors.append(f"transition_status {status} incompatible with task_state {task.get('task_state')}")
    if task.get("task_state")=="READY" and status!="AVAILABLE":
        errors.append("READY task must originate from AVAILABLE transition")
    if task.get("task_state") in {"COMPLETED","FAILED","REJECTED"} and not task.get("result_frontier_ids"):
        errors.append("completed/failed/rejected task requires result_frontier_ids")
    if task.get("transition_type")=="TERMINATE" and task.get("task_state")=="READY":
        errors.append("TERMINATE cannot be automatically READY at task generation stage")
    return errors

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: validator.py task.json")
    item=json.load(open(sys.argv[1],encoding="utf-8"))
    errors=validate(item)
    print("PASS" if not errors else "FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(0 if not errors else 1)
