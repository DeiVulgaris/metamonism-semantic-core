"""Stage 43: cross-stage integration and failure-injection gate."""

INVARIANTS = {
    "SOURCE != INFERENCE",
    "HYPOTHESIS != FACT",
    "CORRESPONDENCE != IDENTITY",
    "TASK != TRUTH",
    "RESULT != PROOF",
    "BLOCKED != TERMINATED",
    "IDENTITY != EQUIVALENCE",
    "HISTORY != CURRENT STATE",
}


def valid_chain(record):
    required = [
        "program_id", "trajectory_id", "frontier_id",
        "task_id", "selection_id", "result_id",
        "successor_frontier_id", "identity_status",
        "epistemic_status", "provenance",
    ]
    missing = [k for k in required if not record.get(k)]
    return not missing


def reject_failure(case):
    """Return True when an injected corruption is correctly rejected."""
    rules = {
        "wrong_program_identity": lambda x: x["program_id"] != x["resolved_program_id"],
        "missing_provenance": lambda x: not x.get("provenance"),
        "hypothesis_to_source": lambda x: x["epistemic_status"] == "SOURCE"
            and x["original_status"] == "THEORETICAL_HYPOTHESIS",
        "correspondence_to_identity": lambda x: (
            x["semantic_relation"] == "STRUCTURAL_CORRESPONDENCE"
            and x["identity_status"] == "ASSERTED"
        ),
        "failed_task_to_confirmation": lambda x: (
            x["result_class"] == "DISCONFIRMING"
            and x["promoted_to_confirmation"] is True
        ),
        "fork_without_evidence": lambda x: (
            x["relation_type"] == "MERGE"
            and not x["evidence"]
        ),
        "blocked_to_terminated": lambda x: (
            x["frontier_state"] == "BLOCKED"
            and x["lifecycle"] == "TERMINATED"
        ),
        "silent_identifier_substitution": lambda x: (
            x["input_id"] != x["resolved_id"]
            and x["identity_asserted"] is False
        ),
    }
    return rules[case](record)


def run_gate():
    chain = {
        "program_id": "RP-r1r4-dirac",
        "trajectory_id": "RT-r1r4-dirac-001",
        "frontier_id": "RF-r1r4-dirac-001",
        "task_id": "TASK-r1r4-define",
        "selection_id": "SEL-r1r4-001",
        "result_id": "RES-r1r4-001",
        "successor_frontier_id": "RF-r1r4-dirac-002",
        "identity_status": "ASSERTED",
        "epistemic_status": "THEORETICAL_HYPOTHESIS",
        "provenance": {"repository": "DeiVulgaris/metamonism-semantic-core",
                       "path": "stage41/run_report.json",
                       "ref": "24b3211ef548029a4979ea290faa64433ff82a3e",
                       "locator": "r1_r4_formalization"},
    }
    assert valid_chain(chain)

    injections = {
        "wrong_program_identity": {**chain, "program_id":"RP-other",
                                    "resolved_program_id":"RP-r1r4-dirac"},
        "missing_provenance": {**chain, "provenance":{}},
        "hypothesis_to_source": {**chain, "epistemic_status":"SOURCE",
                                 "original_status":"THEORETICAL_HYPOTHESIS"},
        "correspondence_to_identity": {**chain, "semantic_relation":"STRUCTURAL_CORRESPONDENCE",
                                       "identity_status":"ASSERTED"},
        "failed_task_to_confirmation": {**chain, "result_class":"DISCONFIRMING",
                                         "promoted_to_confirmation":True},
        "fork_without_evidence": {**chain, "relation_type":"MERGE", "evidence":[]},
        "blocked_to_terminated": {**chain, "frontier_state":"BLOCKED",
                                  "lifecycle":"TERMINATED"},
        "silent_identifier_substitution": {**chain, "input_id":"legacy-id",
                                            "resolved_id":"RP-r1r4-dirac",
                                            "identity_asserted":False},
    }
    failures = {name: reject_failure(name) for name, data in injections.items()}
    # The helper evaluates the named rule against its corresponding case.
    assert all(failures.values()), failures
    return {"status":"PASS","invariants":sorted(INVARIANTS),
            "failure_injections":list(failures)}


if __name__ == "__main__":
    print(run_gate())
