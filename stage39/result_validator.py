"""Stage 39 — structural validation for RESEARCH_RESULT."""

RESULT_CLASSES = {
    "CONFIRMING","DISCONFIRMING","PARTIALLY_CONFIRMING","INCONCLUSIVE",
    "ANOMALOUS","INVALID","UNREPRODUCIBLE","BLOCKED",
}
FRONTIER_STATES = {
    "ESTABLISHED","PARTIALLY_RESOLVED","UNRESOLVED","BLOCKED",
    "CONFLICTING","UNTESTED","NEWLY_GENERATED",
}
EPISTEMIC_STATUSES = {
    "SOURCE","INFERENCE","FORMALIZATION","THEORETICAL_HYPOTHESIS",
    "PROPOSAL","UNRESOLVED","CONFLICT","USED_BUT_UNDEFINED",
    "PRIOR_THEORETICAL_FORMULATION","MODEL_SPECIFIC",
}

def _provenance(p):
    assert isinstance(p, dict)
    for k in ("repository","path","ref","locator"):
        assert p.get(k)

def validate_result(result):
    for k in ("result_id","task_id","frontier_id","research_program_id","trajectory_id",
              "result_class","observation","interpretation","unresolved_difference",
              "evidence","successor_frontier","provenance"):
        assert k in result, f"missing {k}"
    assert result["result_class"] in RESULT_CLASSES
    _provenance(result["provenance"])

    successor = result["successor_frontier"]
    assert successor["frontier_state"] in FRONTIER_STATES
    assert successor["frontier_id"]
    assert successor["research_program_id"] == result["research_program_id"]
    assert successor["trajectory_id"] == result["trajectory_id"]
    assert successor["unresolved_difference"]
    assert successor["subject"]["ref"]
    _provenance(successor["provenance"])

    if result.get("epistemic_status"):
        assert result["epistemic_status"] in EPISTEMIC_STATUSES

    if successor.get("epistemic_status"):
        assert successor["epistemic_status"] in EPISTEMIC_STATUSES

    # A non-SOURCE successor cannot silently become canonical.
    if successor.get("epistemic_status") != "SOURCE":
        assert successor.get("derived_from"), "non-SOURCE successor requires derived_from"

    # A blocked execution must preserve an explicit blocker.
    if result["result_class"] == "BLOCKED":
        assert result.get("blockers"), "BLOCKED result requires blockers"

    # BLOCKED is never equivalent to termination.
    if successor["frontier_state"] == "BLOCKED":
        assert successor.get("blockers"), "BLOCKED frontier requires blockers"

    # Result recording never upgrades a working hypothesis by itself.
    if result["result_class"] == "CONFIRMING":
        assert successor.get("epistemic_status") != "SOURCE" or successor.get("derived_from"),             "confirmation cannot create SOURCE status without explicit provenance"

    return True

if __name__ == "__main__":
    import json, sys
    validate_result(json.load(open(sys.argv[1], encoding="utf-8")))
    print("PASS")
