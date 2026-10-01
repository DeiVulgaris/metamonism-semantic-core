#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    case = json.loads((ROOT / "stage28" / "monos_logos_case.json").read_text(encoding="utf-8"))
    tests = (ROOT / "stage28" / "test_vectors.yaml").read_text(encoding="utf-8")
    report = (ROOT / "stage28" / "validation_report.md").read_text(encoding="utf-8")

    checks = [
        ("case is Monos / Logos", case["case"] == "monos_logos"),
        ("Monos is SOURCE", case["source_derived"]["monos"]["status"] == "SOURCE"),
        ("Logos is SOURCE", case["source_derived"]["logos"]["status"] == "SOURCE"),
        ("correspondence is SOURCE", case["source_derived"]["relation"]["status"] == "SOURCE"),
        ("isomorphism unresolved", case["source_derived"]["relation"]["formal_isomorphism"] == "UNRESOLVED"),
        ("result is structural correspondence",
         case["cross_inventory_result"]["status"] == "STRUCTURAL_CORRESPONDENCE"),
        ("eight test vectors", tests.count("T28-") == 8),
        ("validation says PASS",
         "PASS — SECOND INDEPENDENT SEMANTIC CASE" in report),
    ]

    for name, ok in checks:
        print(name, "PASS" if ok else "FAIL")

    return 0 if all(ok for _, ok in checks) else 1

if __name__ == "__main__":
    sys.exit(main())
