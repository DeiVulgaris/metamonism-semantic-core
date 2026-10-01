#!/usr/bin/env python3
"""Stage 25 — deterministic structured semantic query engine."""
from pathlib import Path
import re, sys, json

ROOT=Path(__file__).resolve().parents[1]

FILES={
 "registries":[
  "stage11/a_entity_registry.yaml","stage11/b_claim_registry.yaml","stage11/c_relation_registry.yaml",
  "stage12/b_entity_registry.yaml","stage12/c_claim_registry.yaml","stage12/d_relation_registry.yaml",
  "stage13/c_entity_registry.yaml","stage13/d_claim_registry.yaml","stage13/e_relation_registry.yaml"],
 "provenance":"stage16/provenance_registry.yaml",
 "formalization":"stage17/formalization_registry.yaml",
 "cross_source":"stage10/cross_source_edges_x1_x21.yaml",
 "ambiguity":"ambiguity_registry.yaml",
 "conflict":"conflict_registry.yaml",
}

def read(p): return (ROOT/p).read_text(encoding="utf-8")
def registry_text(): return "\n".join(read(p) for p in FILES["registries"])

def records_with(text, pattern):
    return [x.strip() for x in text.splitlines() if re.search(pattern,x,re.I)]

def query(qtype, value):
    if qtype=="Q5":
        t=read(FILES["provenance"])
        hits=records_with(t, re.escape(value))
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}

    if qtype=="Q6":
        t=read(FILES["formalization"])
        hits=records_with(t, re.escape(value))
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}

    if qtype=="Q7":
        t=read(FILES["cross_source"])
        hits=records_with(t, re.escape(value))
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}

    if qtype=="Q9":
        forbidden={
          "identity":{"status":"PROHIBITED_INFERENCE","boundary":"No A/B/C operator identity without explicit identity relation."},
          "model_core":{"status":"PROHIBITED_INFERENCE","boundary":"MODEL does not become CORE by query chaining."},
          "hypothesis":{"status":"PROHIBITED_INFERENCE","boundary":"Hypothesis status cannot be promoted by retrieval or formalization."},
          "independence":{"status":"PROHIBITED_INFERENCE","boundary":"Missing relation does not imply independence."},
          "causality":{"status":"PROHIBITED_INFERENCE","boundary":"Relation path does not establish causality."},
        }
        for key,result in forbidden.items():
            if key in value.lower():
                return result
        a=read(FILES["ambiguity"])
        c=read(FILES["conflict"])
        hits=records_with(a,re.escape(value))+records_with(c,re.escape(value))
        return {"status":"RESOLVED" if hits else "EMPTY","results":hits}

    return {"status":"UNRESOLVED","results":[]}

def main():
    if len(sys.argv)!=3:
        print("usage: structured_query.py Q5 VALUE")
        return 2
    print(json.dumps(query(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
