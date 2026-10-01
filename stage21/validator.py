#!/usr/bin/env python3
"""Stage 21 source-admission gate: queue only, no semantic promotion."""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def main():
    q=read("undefined_term_registry.yaml")
    a=read("stage21/admission_queue.yaml")
    report=read("stage21/admission_audit.yaml")

    terms=re.findall(r'^\s*- term:\s*"([^"]+)"',q,re.M)
    queued=re.findall(r'^\| ([^|]+) \| USED_BUT_UNDEFINED',a,re.M)

    checks=[
        ("undefined_registry_has_8_terms",len(terms)==8),
        ("all_8_are_queued",len(queued)==8),
        ("zero_admitted", "admitted: 0" in report),
        ("zero_new_entities", "new_entities: 0" in report),
        ("zero_new_claims", "new_claims: 0" in report),
        ("zero_new_relations", "new_relations: 0" in report),
    ]
    for name,ok in checks:
        print(name, "PASS" if ok else "FAIL")
    return 0 if all(ok for _,ok in checks) else 1

if __name__=="__main__":
    sys.exit(main())
