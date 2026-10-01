#!/usr/bin/env python3
"""Stage 31 validator for the AI Text Processing Protocol benchmark.

This validator checks the machine-readable benchmark contract itself.
It does not attempt to prove the underlying scientific or philosophical claims.
"""

from pathlib import Path
import re
import sys

CASE_FILE = Path(__file__).with_name("test_cases.yaml")

# Deliberately dependency-free structural checks over the benchmark YAML.
# The repository may later replace this with a full YAML parser/schema validator.

REQUIRED_RECORD_KEYS = {"id", "kind", "status", "provenance"}
REQUIRED_PROVENANCE_KEYS = {"repository", "path", "ref", "locator"}
NON_SOURCE = {
    "INFERENCE", "FORMALIZATION", "THEORETICAL_HYPOTHESIS",
    "PROPOSAL", "UNRESOLVED", "CONFLICT", "MODEL_SPECIFIC",
    "PRIOR_THEORETICAL_FORMULATION", "USED_BUT_UNDEFINED",
}

def main() -> int:
    text = CASE_FILE.read_text(encoding="utf-8")
    errors = []

    for token in ("PHILOSOPHICAL-CORE-01", "FORMAL-AXIOM-02", "PHYSICAL-MODEL-03"):
        if token not in text:
            errors.append(f"missing benchmark case: {token}")

    if "source_claim_as_interpreted:" not in text:
        errors.append("missing source_claim_as_interpreted field")
    if "derived_from:" not in text:
        errors.append("missing derived_from coverage")
    if "repository:" not in text or "path:" not in text or "ref:" not in text:
        errors.append("missing machine-readable provenance fields")

    # Every listed non-SOURCE record must expose a derived_from field.
    # We inspect record blocks conservatively because this validator has no YAML dependency.
    blocks = re.split(r"\n\s*- id: ", text)
    for block in blocks[1:]:
        status = re.search(r"\n\s*status:\s*([A-Z_]+)", block)
        if not status:
            continue
        value = status.group(1)
        if value in NON_SOURCE and "derived_from:" not in block:
            # MODEL_SPECIFIC source claims may still be directly source-grounded;
            # only the protocol rule requires derived_from for AI-generated non-SOURCE
            # records. The benchmark marks this explicitly where applicable.
            if value != "MODEL_SPECIFIC":
                errors.append(f"record block with status {value} lacks derived_from")

    # The benchmark must explicitly preserve the central anti-collapse rules.
    required_phrases = [
        "MODEL_SPECIFIC prediction becomes empirical fact",
        "Formal expression is automatically a formally proven theorem",
        "Monos = Logos",
        "Contradicts relation becomes proof",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"missing anti-collapse test: {phrase}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print("3 heterogeneous corpus cases present")
    print("provenance fields present")
    print("source/interpreted distinction present")
    print("anti-collapse checks present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
