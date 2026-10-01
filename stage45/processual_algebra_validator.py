"""Validation gate for the D1-D5 processual algebra research program."""

REQUIRED_FRONTIER = {
    "frontier_id", "research_program_id", "trajectory_id", "frontier_state",
    "epistemic_status", "subject", "unresolved_difference", "evidence",
    "provenance", "derived_from", "constraints", "blockers",
    "open_questions", "admissible_transitions", "forbidden_inferences",
}

FORBIDDEN = (
    "P1-P4 are already Dirac gamma matrices",
    "four stages imply Clifford algebra",
    "+n->-n proves spin-1/2",
    "orientation reversal is identical to a gamma-matrix sign",
    "Dirac equation follows from the current source",
)

def validate_frontier(frontier):
    errors = []
    missing = REQUIRED_FRONTIER - set(frontier)
    if missing:
        errors.append(f"missing frontier fields: {sorted(missing)}")

    if frontier.get("frontier_state") not in {
        "ESTABLISHED", "PARTIALLY_RESOLVED", "UNRESOLVED",
        "BLOCKED", "CONFLICTING", "UNTESTED", "NEWLY_GENERATED"
    }:
        errors.append("invalid frontier_state")

    if frontier.get("epistemic_status") not in {
        "SOURCE", "INFERENCE", "FORMALIZATION", "THEORETICAL_HYPOTHESIS",
        "PROPOSAL", "UNRESOLVED", "CONFLICT", "USED_BUT_UNDEFINED",
        "PRIOR_THEORETICAL_FORMULATION", "MODEL_SPECIFIC"
    }:
        errors.append("invalid epistemic_status")

    provenance = frontier.get("provenance", {})
    for key in ("repository", "path", "ref", "locator"):
        if not provenance.get(key):
            errors.append(f"missing provenance.{key}")

    if frontier.get("epistemic_status") != "SOURCE" and not frontier.get("derived_from"):
        errors.append("non-SOURCE frontier requires derived_from")

    forbidden = set(frontier.get("forbidden_inferences", []))
    for item in FORBIDDEN:
        if item not in forbidden:
            errors.append(f"missing forbidden inference: {item}")

    return errors


def validate_d1_d5(state):
    """Validate staged D1-D5 without allowing target-theory import."""
    errors = []

    if state.get("d1", {}).get("status") == "PASS" and not state.get("d1", {}).get("carrier"):
        errors.append("D1 PASS requires an explicit carrier")

    if state.get("d2", {}).get("status") == "PASS" and not state.get("d2", {}).get("composition"):
        errors.append("D2 PASS requires an explicit composition law")

    if state.get("d3", {}).get("status") == "PASS" and not state.get("d3", {}).get("bilinear_form"):
        errors.append("D3 PASS requires an explicit bilinear form")

    if state.get("d4", {}).get("status") == "PASS" and not state.get("d4", {}).get("anticommutator"):
        errors.append("D4 PASS requires an explicit anticommutator")

    if state.get("d5", {}).get("status") == "PASS":
        if not state.get("d5", {}).get("relation_verified"):
            errors.append("D5 PASS requires relation_verified=true")
        if state.get("d5", {}).get("relation_stipulated"):
            errors.append("D5 cannot pass when the relation is merely stipulated")

    return errors
