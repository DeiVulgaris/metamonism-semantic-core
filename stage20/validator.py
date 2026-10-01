#!/usr/bin/env python3
"""Stage 20 controlled-expansion gate.

This gate is intentionally conservative: Stage 20 adds no semantic assertions.
It checks that the expansion package is registry-only and that baseline counts
declared by the project remain unchanged.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "A": (32,46,44),
    "B": (94,65,53),
    "C": (42,51,42),
}

def text(p):
    return (ROOT/p).read_text(encoding="utf-8")

def record_count(p):
    s=text(p)
    return len(re.findall(r"^\s*-\s+id:\s+mm:", s, re.M))

def main():
    checks=[]
    for inv, paths in {
        "A":("stage11/a_entity_registry.yaml","stage11/b_claim_registry.yaml","stage11/c_relation_registry.yaml"),
        "B":("stage12/b_entity_registry.yaml","stage12/c_claim_registry.yaml","stage12/d_relation_registry.yaml"),
        "C":("stage13/c_entity_registry.yaml","stage13/d_claim_registry.yaml","stage13/e_relation_registry.yaml"),
    }.items():
        actual=tuple(record_count(p) for p in paths)
        checks.append((inv, actual == EXPECTED[inv], {"expected":EXPECTED[inv],"actual":actual}))

    manifest=text("stage20/expansion_manifest.yaml")
    zero_all=all(x in manifest for x in [
        "new_mm_entities: 0","new_mm_claims: 0",
        "new_mm_relations: 0","new_cross_source_relations: 0"
    ])
    checks.append(("registry_only_admission",zero_all,{}))

    failed=[x for x in checks if not x[1]]
    for name,ok,details in checks:
        print(name, "PASS" if ok else "FAIL", details)
    return 1 if failed else 0

if __name__=="__main__":
    sys.exit(main())
