#!/usr/bin/env python3
"""Stage 19 read-only integrity validator.

The script validates repository registry files. It never mutates semantic data.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def ids(text):
    return set(re.findall(r"mm:[a-z0-9_-]+(?:\.[a-z0-9_-]+){2,}", text))

def scoped_ids(text, inv):
    return set(re.findall(rf"mm:{inv}\.[a-z0-9_-]+(?:\.[a-z0-9_-]+)*", text))

def check_scope(inv, files, global_ids, global_rels):
    found = set()
    leaks = set()
    missing = set()
    for rel in files:
        for ident in scoped_ids(read(rel), inv):
            found.add(ident)
            if not ident.startswith(f"mm:{inv}."):
                leaks.add(ident)
            if ident not in global_ids and ident not in global_rels:
                missing.add(ident)
    return not leaks and not missing, {"leaks": sorted(leaks), "missing": sorted(missing)}

def main():
    global_ids = ids(read("id_registry.yaml"))
    global_rels = ids(read("relation_registry.yaml"))

    checks = []

    for inv, files in {
        "a": ["stage11/a_entity_registry.yaml","stage11/b_claim_registry.yaml","stage11/c_relation_registry.yaml"],
        "b": ["stage12/b_entity_registry.yaml","stage12/c_claim_registry.yaml","stage12/d_relation_registry.yaml"],
        "c": ["stage13/c_entity_registry.yaml","stage13/d_claim_registry.yaml","stage13/e_relation_registry.yaml"],
    }.items():
        ok, details = check_scope(inv, files, global_ids, global_rels)
        checks.append((f"R01/R02:{inv}", ok, details))

    x = read("stage10/cross_source_edges_x1_x21.yaml").split("edges:",1)[-1]
    xids = re.findall(r"^\s*-\s*\{id:\s*(X\d+)", x, re.M)
    expected = {f"X{i}" for i in range(1,22)}
    checks.append(("R03", len(xids) == 21 and set(xids) == expected, {"count":len(xids)}))

    relation_text = read("relation_registry.yaml")
    forbidden = {"sameAs","identical_to","implements","proves","independent_of","unrelated_to"}
    semantic_tokens = set(re.findall(r"(?:id|predicate|relation):\s*([A-Za-z0-9_.-]+)", relation_text))
    checks.append(("R05/R12", not (forbidden & semantic_tokens), {"found": sorted(forbidden & semantic_tokens)}))

    op_ids = {x for x in global_ids if re.match(r"mm:[abc]\.op\.", x)}
    checks.append(("R06", all(any(x.startswith(f"mm:{i}.op.") for x in op_ids) for i in "abc"), {"operators": sorted(op_ids)}))

    formalizations = re.findall(r"\bid:\s*(f17:[A-Za-z0-9_.-]+)", read("stage17/formalization_registry.yaml"))
    checks.append(("R09", len(formalizations) == 25, {"count": len(formalizations)}))

    queries = re.findall(r"\bid:\s*(q18\.[A-Za-z0-9_.-]+)", read("stage18/query_registry.yaml"))
    checks.append(("R10", len(queries) == 10, {"count": len(queries)}))

    failed = [x for x in checks if not x[1]]
    for name, ok, details in checks:
        print(f"{name}: {'PASS' if ok else 'FAIL'} {details}")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
