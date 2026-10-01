#!/usr/bin/env python3
"""Stage 24 — read-only semantic query dispatcher.

This implementation deliberately uses a small deterministic registry reader.
It is a retrieval layer, not an inference engine.
"""
from pathlib import Path
import re, sys, json

ROOT=Path(__file__).resolve().parents[1]

REG_FILES=[
"stage11/a_entity_registry.yaml","stage11/b_claim_registry.yaml","stage11/c_relation_registry.yaml",
"stage12/b_entity_registry.yaml","stage12/c_claim_registry.yaml","stage12/d_relation_registry.yaml",
"stage13/c_entity_registry.yaml","stage13/d_claim_registry.yaml","stage13/e_relation_registry.yaml",
]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def all_text():
    return "\n".join(read(p) for p in REG_FILES)

def mm_ids():
    return sorted(set(re.findall(r"mm:[a-z0-9_-]+(?:\.[a-z0-9_-]+){2,}", all_text())))

def relations():
    out=[]
    for p in REG_FILES:
        for line in read(p).splitlines():
            if "id: mm:" in line and "subject:" in line and "predicate:" in line and "object:" in line:
                out.append(line.strip())
    return out

def query(qtype, value):
    t=all_text()
    if qtype=="Q1":
        hits=[x for x in mm_ids() if value in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype=="Q2":
        hits=[x for x in t.splitlines() if value in x and "clm." in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype=="Q3":
        hits=[x for x in relations() if value in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype=="Q4":
        hits=[x for x in t.splitlines() if "basis_claim:" in x and value in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype=="Q8":
        hits=[x for x in t.splitlines() if "status:" in x and value in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype=="Q10":
        hits=[x for x in mm_ids() if ".op." in x and value in x]
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}
    if qtype in {"Q5","Q6","Q7","Q9"}:
        return {"status":"PARTIAL","results":[],"note":"Query class is registered; this minimal dispatcher requires a narrower structured implementation."}
    return {"status":"EMPTY","results":[]}

def main():
    if len(sys.argv)!=3:
        print("usage: dispatcher.py Q1 value")
        return 2
    print(json.dumps(query(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
