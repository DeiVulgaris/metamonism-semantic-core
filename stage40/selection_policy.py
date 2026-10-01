"""Stage 40: explicit procedural selection of research tasks."""

POLICIES = {"USER_SELECTED","DEPENDENCY_FIRST","BLOCKER_FIRST","CHEAPEST_TEST_FIRST","INFORMATION_GAIN","PARALLEL_BRANCHING"}

def _ready(tasks):
    return [t for t in tasks if t.get("task_state") == "READY"]

def _metric(context, task_id, name):
    return context.get(task_id, {}).get(name)

def select_tasks(tasks, policy, context=None, user_selected_task_id=None,
                 decision_id="selection.001", provenance=None):
    context = context or {}
    provenance = provenance or {}
    candidates = _ready(tasks)
    decision = {
        "decision_id":decision_id, "policy":policy,
        "candidate_task_ids":[t["task_id"] for t in candidates],
        "selected_task_ids":[],
        "status":"NO_ELIGIBLE_TASK" if not candidates else "BLOCKED",
        "criteria":[],"rationale":"","metrics_used":{},"provenance":provenance
    }
    if policy not in POLICIES:
        decision["status"]="INVALID_REQUEST"; decision["rationale"]="Unknown selection policy."; return decision
    if not candidates:
        decision["rationale"]="No READY task exists."; return decision
    by_id={t["task_id"]:t for t in candidates}

    if policy=="USER_SELECTED":
        if user_selected_task_id not in by_id:
            decision["rationale"]="An explicit READY task ID is required."; return decision
        decision["selected_task_ids"]=[user_selected_task_id]
        decision["status"]="SELECTED"
        decision["criteria"]=["explicit user selection"]
        decision["rationale"]="User explicitly selected an admissible READY task."
        decision["user_selected_task_id"]=user_selected_task_id
        return decision

    if policy=="PARALLEL_BRANCHING":
        eligible=[t for t in candidates if context.get(t["task_id"],{}).get("eligible_for_parallel_branching") is True]
        if not eligible:
            decision["rationale"]="No READY task is explicitly eligible for parallel branching."; return decision
        eligible.sort(key=lambda t:t["task_id"])
        decision["selected_task_ids"]=[t["task_id"] for t in eligible]
        decision["status"]="SELECTED"
        decision["criteria"]=["explicit parallel-branch eligibility","task-id tie-break"]
        decision["rationale"]="All explicitly eligible branches are selected; no branch is preferred."
        return decision

    metric_name={"DEPENDENCY_FIRST":"dependency_depth","BLOCKER_FIRST":"blocker_reduction",
                 "CHEAPEST_TEST_FIRST":"estimated_cost","INFORMATION_GAIN":"expected_information_gain"}[policy]
    pool=candidates
    if policy=="CHEAPEST_TEST_FIRST":
        pool=[t for t in candidates if t.get("transition_type")=="TEST"]
        if not pool:
            decision["rationale"]="No READY TEST task exists."; return decision
    missing=[t["task_id"] for t in pool if _metric(context,t["task_id"],metric_name) is None]
    if missing:
        decision["rationale"]="Required external metric is missing: "+str(missing)
        decision["selection_notes"]=["No metric was fabricated."]
        return decision
    reverse=policy in {"BLOCKER_FIRST","INFORMATION_GAIN"}
    pool.sort(key=lambda t:((-_metric(context,t["task_id"],metric_name)) if reverse else _metric(context,t["task_id"],metric_name),t["task_id"]))
    chosen=pool[0]
    decision["selected_task_ids"]=[chosen["task_id"]]
    decision["status"]="SELECTED"
    decision["criteria"]=["external metric: "+metric_name,"task-id tie-break"]
    decision["metrics_used"]={t["task_id"]:{metric_name:_metric(context,t["task_id"],metric_name)} for t in pool}
    decision["rationale"]="Selected by declared procedural policy using external metrics."
    return decision
