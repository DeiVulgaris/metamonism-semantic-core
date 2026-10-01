import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "orthogonal_continuation_state.json"


def validate_state(data):
    errors = []

    required = {
        "state_id",
        "program_id",
        "status",
        "integration_scope",
        "frontier_state",
        "formal_objects",
        "P3_condition",
        "P4_condition",
        "source_basis",
        "anti_collapse",
        "next_research_questions",
        "canonical_promotion",
    }

    missing = sorted(required - set(data))
    if missing:
        errors.append(f"missing top-level fields: {missing}")

    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")

    fo = data.get("formal_objects", {})
    for key in (
        "state",
        "orthogonality_predicate",
        "continuation_predicate",
        "feasible_set",
        "exhaustion",
        "frustration",
        "resolution_set",
    ):
        if key not in fo:
            errors.append(f"formal_objects missing: {key}")

    p3 = data.get("P3_condition", {})
    if p3.get("orthogonal_feasible_set") != "emptyset":
        errors.append("P3 must record old-regime D_perp as emptyset")

    p4 = data.get("P4_condition", {})
    if p4.get("membership") != "P4 in Sol_perp(P3,R_old)":
        errors.append("P4 must be constrained as an element of Sol_perp")

    if p4.get("orientation_before") != "+n" or p4.get("orientation_after") != "-n":
        errors.append("source-grounded orientation pattern missing")

    anti = " ".join(data.get("anti_collapse", []))
    required_rules = [
        "orthogonal resolution is not the same as n and -n being Euclidean-orthogonal",
        "D_perp exhaustion is regime-specific",
        "P4 is not an arbitrary boundary jump",
        "P4 is not a fourth spatial basis vector",
        "no metric is assumed",
        "no operator law for orientation reversal is assumed",
        "no Clifford algebra is inferred",
        "P4 uniqueness is not assumed",
    ]
    for rule in required_rules:
        if rule not in anti:
            errors.append(f"missing anti-collapse rule: {rule}")

    return errors


def main():
    with STATE.open(encoding="utf-8") as fh:
        data = json.load(fh)

    errors = validate_state(data)
    print("PASS" if not errors else "FAIL")
    for item in errors:
        print(f"- {item}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
