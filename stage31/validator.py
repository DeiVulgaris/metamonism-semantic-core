#!/usr/bin/env python3
"""Stage 31 validator for the AI Text Processing Protocol benchmark."""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("FAIL")
    print("- PyYAML is required to validate the benchmark YAML")
    raise SystemExit(1)

CASE_FILE = Path(__file__).with_name("test_cases.yaml")

REQUIRED_PROVENANCE = {"repository", "path", "ref", "locator"}
NON_SOURCE = {
    "INFERENCE", "FORMALIZATION", "THEORETICAL_HYPOTHESIS", "PROPOSAL",
    "UNRESOLVED", "CONFLICT", "PRIOR_THEORETICAL_FORMULATION",
    "USED_BUT_UNDEFINED",
}

def fail(errors):
    print("FAIL")
    for e in errors:
        print(f"- {e}")
    return 1

def main():
    data = yaml.safe_load(CASE_FILE.read_text(encoding="utf-8"))
    errors = []

    cases = data.get("cases", [])
    expected_ids = {"PHILOSOPHICAL-CORE-01", "FORMAL-AXIOM-02", "PHYSICAL-MODEL-03"}
    actual_ids = {c.get("case_id") for c in cases}
    missing = expected_ids - actual_ids
    if missing:
        errors.append(f"missing benchmark cases: {sorted(missing)}")

    for case in cases:
        source = case.get("source", {})
        for key in ("repository", "path", "ref", "locator"):
            if not source.get(key):
                errors.append(f"{case.get('case_id')}: source missing {key}")

        for record in case.get("expected_records", []):
            rid = record.get("id", "<missing-id>")
            for key in ("id", "kind", "status", "provenance"):
                if key not in record:
                    errors.append(f"{case.get('case_id')}/{rid}: missing {key}")

            provenance = record.get("provenance", {})
            missing_prov = REQUIRED_PROVENANCE - set(provenance)
            if missing_prov:
                errors.append(
                    f"{case.get('case_id')}/{rid}: missing provenance {sorted(missing_prov)}"
                )

            if record.get("status") != "SOURCE" and not record.get("derived_from"):
                errors.append(
                    f"{case.get('case_id')}/{rid}: non-SOURCE record lacks derived_from"
                )

            if record.get("kind") in {"claim", "formalization"}:
                if not record.get("source_claim"):
                    errors.append(f"{case.get('case_id')}/{rid}: missing source_claim")
                if not record.get("source_claim_as_interpreted"):
                    errors.append(
                        f"{case.get('case_id')}/{rid}: missing source_claim_as_interpreted"
                    )

            if record.get("kind") == "relation" and not record.get("relation_type"):
                errors.append(f"{case.get('case_id')}/{rid}: relation lacks relation_type")

        forbidden = case.get("forbidden_inferences", [])
        if not forbidden:
            errors.append(f"{case.get('case_id')}: no forbidden-inference tests")

    # Explicit anti-collapse tests required by Stage 30.
    text = CASE_FILE.read_text(encoding="utf-8")
    for phrase in (
        "MODEL_SPECIFIC prediction becomes empirical fact",
        "Formal expression is automatically a formally proven theorem",
        "Monos = Logos",
        "Contradicts relation becomes proof",
    ):
        if phrase not in text:
            errors.append(f"missing anti-collapse test: {phrase}")

    if errors:
        return fail(errors)

    print("PASS")
    print(f"{len(cases)} heterogeneous corpus cases validated")
    print("all records contain machine-readable provenance")
    print("all non-SOURCE records contain derived_from")
    print("claim/formalization records preserve source_claim and interpretation")
    print("relation records are typed")
    print("anti-collapse tests present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
