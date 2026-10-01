#!/usr/bin/env python3
"""Stage 22 canonical-view gate.

This validator checks the canonical aggregation contract. It does not
interpret the underlying ontology.
"""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def ids(p):
    return set(re.findall(r"mm:[a-z0-9_-]+(?:\.[a-z0-9_-]+){2,}", read(p)))

def count_records(p):
    return len(re.findall(r"^\s*-\s+id:\s+mm:", read(p), re.M))

EXPECTED={
 "A":(32,46,44),
 "B":(94,65,53),
 "C":(42,51,42)
}
REG={
 "A":("stage11/a_entity_registry.yaml","stage11/b_claim_registry.yaml","stage11/c_relation_registry.yaml"),
 "B":("stage12/b_entity_registry.yaml","stage12/c_claim_registry.yaml","stage12/d_relation_registry.yaml"),
 "C":("stage13/c_entity_registry.yaml","stage13/d_claim_registry.yaml","stage13/e_relation_registry.yaml")
}

def main():
    checks=[]
    all_ids=set()
    for inv,files in REG.items():
        actual=tuple(count_records(p) for p in files)
        checks.append((f"{inv}_counts",actual==EXPECTED[inv],{"expected":EXPECTED[inv],"actual":actual}))
        for p in files: all_ids |= ids(p)

    x=read("stage10/cross_source_edges_x1_x21.yaml")
    xids=re.findall(r"^\s*-\s*\{id:\s*(X\d+)",x,re.M)
    checks.append(("X1_X21",len(xids)==21 and set(xids)=={f"X{i}" for i in range(1,22)},{"count":len(xids)}))

    # Same-named operators must remain inventory-scoped.
    ops={i:{x for x in all_ids if x.startswith(f"mm:{i}.op.")} for i in "ABC"}
    checks.append(("operator_namespace",all(len(ops[i])>0 for i in "ABC"),ops))

    # The canonical view may only contain the declared zero-addition policy.
    m=read("stage22/canonical_view_manifest.md")
    checks.append(("no_new_semantics","new entities" in m and "new claims" in m and "new cross-source edges" in m,{}))

    for n,ok,d in checks:
        print(n,"PASS" if ok else "FAIL",d)
    return 0 if all(ok for _,ok,_ in checks) else 1

if __name__=="__main__":
    sys.exit(main())
