#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    spec = (ROOT / "stage27" / "benchmark_pattern.md").read_text(encoding="utf-8")
    cases = (ROOT / "stage27" / "benchmark_cases.yaml").read_text(encoding="utf-8")
    tests = (ROOT / "stage27" / "test_vectors.yaml").read_text(encoding="utf-8")
    report = (ROOT / "stage27" / "validation_report.md").read_text(encoding="utf-8")

    checks = [
        ("has case schema", "case_id" in spec and "comparison_axes" in spec),
        ("has anti-collapse rule", "Anti-collapse Rule" in spec),
        ("supports extension result", "EXTENSION" in spec and "mm:rel.extends" in spec),
        ("reference case is SB-001", "SB-001" in cases),
        ("reference result is PARTIAL", "expected_result: PARTIAL" in cases),
        ("six test vectors", tests.count("T27-") == 6),
        ("validation says PASS", "PASS — REUSABLE SEMANTIC BENCHMARK PATTERN" in report),
    ]

    for name, ok in checks:
        print(name, "PASS" if ok else "FAIL")

    return 0 if all(ok for _, ok in checks) else 1

if __name__ == "__main__":
    sys.exit(main())
