"""Stage 40 structural validator."""
from selection_policy import POLICIES

def validate_decision(decision):
    assert decision["decision_id"]
    assert decision["policy"] in POLICIES
    assert decision["candidate_task_ids"]
    assert set(decision["selected_task_ids"]) <= set(decision["candidate_task_ids"])
    assert decision["status"] in {"SELECTED","BLOCKED","NO_ELIGIBLE_TASK","INVALID_REQUEST"}
    assert decision["rationale"]
    for key in ("repository","path","ref","locator"):
        assert decision["provenance"].get(key)
    if decision["status"]=="SELECTED":
        assert decision["selected_task_ids"]
    if decision["policy"]=="USER_SELECTED" and decision["status"]=="SELECTED":
        assert decision.get("user_selected_task_id") in decision["selected_task_ids"]
    return True

if __name__=="__main__":
    import json,sys
    validate_decision(json.load(open(sys.argv[1],encoding="utf-8")))
    print("PASS")
