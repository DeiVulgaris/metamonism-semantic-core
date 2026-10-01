"""Validation for the D2 process-composition result."""

def validate_d2(state):
    errors = []

    if state.get("status") not in {"PARTIALLY_RESOLVED", "UNRESOLVED", "BLOCKED"}:
        errors.append("invalid D2 status")

    if state.get("algebra_obtained") is True:
        errors.append("D2 must not claim an algebra before common carrier and algebraic closure are established")

    if state.get("clifford_structure_obtained") is True:
        errors.append("D2 cannot establish Clifford structure")

    composition = state.get("composition", {})
    if not composition.get("rule"):
        errors.append("missing composition rule")

    if state.get("orientation", {}).get("R(n)") != "-n":
        errors.append("orientation rule must preserve source-grounded R(n)=-n")

    if state.get("orientation", {}).get("R_squared") != "UNRESOLVED":
        errors.append("R² must remain unresolved at D2")

    required_forbidden = {
        "transition composition is Clifford multiplication",
        "P_i are algebra generators",
        "R is a gamma matrix"
    }
    actual = set(state.get("forbidden_inferences", []))
    missing = required_forbidden - actual
    if missing:
        errors.append(f"missing anti-collapse rules: {sorted(missing)}")

    return errors
