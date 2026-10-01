"""Validation for D3 bilinear/quadratic formalization."""

def validate_d3(state):
    errors = []

    if state.get("status") not in {"PARTIALLY_RESOLVED", "UNRESOLVED", "BLOCKED"}:
        errors.append("invalid D3 status")

    form = state.get("bilinear_form", {})
    if form.get("matrix_form") != "diag(a1,a2,a3)":
        errors.append("D3 must preserve the unresolved diagonal form")

    if form.get("signature") != "UNRESOLVED":
        errors.append("signature must remain unresolved")

    if state.get("lorentzian_signature_derived") is True:
        errors.append("D3 must not claim Lorentzian signature derived from source")

    if state.get("clifford_product_defined") is True:
        errors.append("D3 must not define Clifford product")

    forbidden = set(state.get("forbidden_inferences", []))
    required = {
        "+n->-n is a Lorentzian metric sign",
        "P4 is a fourth spatial basis vector",
        "orthogonality implies Clifford multiplication"
    }
    missing = required - forbidden
    if missing:
        errors.append(f"missing anti-collapse rules: {sorted(missing)}")

    return errors
