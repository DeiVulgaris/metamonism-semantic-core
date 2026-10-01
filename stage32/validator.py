#!/usr/bin/env python3
"""Stage 32 validator: research hypotheses must remain hypotheses."""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("FAIL")
    print("- PyYAML is required")
    raise SystemExit(1)

p = Path(__file__).with_name("test_cases.yaml")
d = yaml.safe_load(p.read_text(encoding="utf-8"))
errors = []

cases = {c["case_id"]: c for c in d.get("cases", [])}
for required in ("R1-R4-DIRAC-01", "RICCI-SURGERY-PLANCK-02"):
    if required not in cases:
        errors.append(f"missing case: {required}")

for case in cases.values():
    if case.get("integration_decision") != "NEW_WORKING_HYPOTHESIS":
        errors.append(f'{case["case_id"]}: hypothesis entered wrong integration scope')

    for r in case.get("expected_records", []):
        if "provenance" not in r:
            errors.append(f'{case["case_id"]}/{r.get("id")}: missing provenance')
        if r.get("status") != "SOURCE" and not r.get("derived_from"):
            errors.append(f'{case["case_id"]}/{r.get("id")}: missing derived_from')

for phrase in (
    "R1-R4 already implement the Dirac algebra",
    "Planck length follows from the current model",
    "Ricci-flow surgery and ontodynamic surgery are mathematically identical",
    "The supplied Planck-length expression is accepted without dimensional validation",
):
    if phrase not in p.read_text(encoding="utf-8"):
        errors.append(f"missing forbidden inference: {phrase}")

planck = next(
    (r for r in cases["RICCI-SURGERY-PLANCK-02"]["expected_records"]
     if r["id"] == "s6"),
    None,
)
if not planck or planck.get("validation") != "CORRECTION_REQUIRED":
    errors.append("Planck formula must be marked CORRECTION_REQUIRED")

if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    raise SystemExit(1)

print("PASS")
print("2 research-hypothesis cases validated")
print("canonical-core contamination blocked")
print("structural analogy kept distinct from isomorphism")
print("Planck expression flagged for dimensional correction")
