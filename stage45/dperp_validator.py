import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "dperp_state.json"


def load_state():
    with STATE.open(encoding="utf-8") as f:
        return json.load(f)


def validate_state(data):
    required = {
        "state_id",
        "program_id",
        "status",
        "integration_scope",
        "frontier_state",
        "source_basis",
        "formalization",
        "invariants",
        "open_questions",
        "canonical_promotion",
    }
    errors = []
    missing = sorted(required - set(data))
    if missing:
        errors.append(f"missing top-level fields: {missing}")

    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")

    source = data.get("source_basis", {})
    for key in ("repository", "document", "locator", "source_claims"):
        if key not in source:
            errors.append(f"source_basis missing: {key}")

    formal = data.get("formalization", {})
    required_formal = {
        "state", "orthogonality_relation", "continuation_set",
        "exhaustion", "frustration", "resolution_set",
        "P4_condition", "orientation_condition",
    }
    missing_formal = sorted(required_formal - set(formal))
    if missing_formal:
        errors.append(f"formalization missing: {missing_formal}")

    invariant_text = " ".join(data.get("invariants", []))
    for phrase in (
        "P4 is not an arbitrary transition",
        "P4 is not a fourth spatial basis vector",
        "orientation reversal is not yet an algebraic operator",
        "P4 uniqueness is not assumed",
        "orthogonality is not identified with a specific metric",
        "no Clifford algebra is inferred",
    ):
        if phrase not in invariant_text:
            errors.append(f"missing anti-collapse invariant: {phrase}")

    return errors


def main():
    data = load_state()
    errors = validate_state(data)
    print("PASS" if not errors else "FAIL")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
