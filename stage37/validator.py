#!/usr/bin/env python3
"""Stage 37 structural validator. Does not establish truth or research success."""

import json
import sys

STATES = {"ESTABLISHED","PARTIALLY_RESOLVED","UNRESOLVED","BLOCKED","CONFLICTING","UNTESTED","NEWLY_GENERATED"}
TRANSITIONS = {"AVAILABLE","CONDITIONAL","BLOCKED","PROHIBITED"}
NON_SOURCE = {"INFERENCE","FORMALIZATION","THEORETICAL_HYPOTHESIS","PROPOSAL","UNRESOLVED","CONFLICT","USED_BUT_UNDEFINED","PRIOR_THEORETICAL_FORMULATION","MODEL_SPECIFIC"}

def validate(item):
    errors = []
    required = ["frontier_id","research_program_id","trajectory_id","frontier_state","subject","unresolved_difference","provenance","admissible_transitions"]
    for key in required:
        if key not in item:
            errors.append("missing required field: " + key)
    if item.get("frontier_state") not in STATES:
        errors.append("invalid frontier_state")
    if not isinstance(item.get("subject"), dict) or not item.get("subject", {}).get("ref"):
        errors.append("subject.ref is required")
    prov = item.get("provenance", {})
    for key in ["repository","path","ref","locator"]:
        if not prov.get(key):
            errors.append("provenance." + key + " is required")
    if item.get("epistemic_status") in NON_SOURCE and not item.get("derived_from"):
        errors.append("non-SOURCE epistemic status requires derived_from")
    transitions = item.get("admissible_transitions", [])
    if not isinstance(transitions, list):
        errors.append("admissible_transitions must be an array")
    for i, transition in enumerate(transitions):
        if transition.get("status") not in TRANSITIONS:
            errors.append("transition[%d] invalid status" % i)
        if "prerequisites" not in transition:
            errors.append("transition[%d] missing prerequisites" % i)
    if item.get("frontier_state") == "BLOCKED":
        if not item.get("blockers"):
            errors.append("BLOCKED frontier requires blockers")
        if any(t.get("type") == "TERMINATE" and t.get("status") == "AVAILABLE" for t in transitions):
            errors.append("BLOCKED frontier cannot make TERMINATE automatically AVAILABLE")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validator.py frontier.json")
        raise SystemExit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        item = json.load(f)
    errors = validate(item)
    print("PASS" if not errors else "FAIL")
    for error in errors:
        if error:
            print("- " + error)
    raise SystemExit(0 if not errors else 1)
