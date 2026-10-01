#!/usr/bin/env python3
"""Stage 23 reasoning gate: verifies rule/output boundaries."""
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def main():
    spec=read("stage23/reasoning_spec.md")
    rules=read("stage23/reasoning_rules.yaml")
    data=json.loads(read("stage23/reasoning_examples.json"))
    checks=[
      ("rules_present", all(x in rules for x in ["R1","R2","R3","R4","R5"])),
      ("forbidden_boundaries_present", all(x in spec for x in ["No causal inference","No mathematical equivalence","hypothesis → SOURCE","model → CORE"])),
      ("examples_present", len(data["outputs"])==4),
      ("blocked_identity", any(x["result"].get("status")=="PROHIBITED_INFERENCE" for x in data["outputs"])),
      ("blocked_model_core", any(x["result"].get("reason")=="MODEL_TO_CORE_ELEVATION" for x in data["outputs"])),
      ("no_mm_derivation_ids", not re.search(r'"id"\s*:\s*"mm:', read("stage23/reasoning_examples.json"))),
    ]
    for n,ok in checks: print(n,"PASS" if ok else "FAIL")
    return 0 if all(ok for _,ok in checks) else 1

if __name__=="__main__": sys.exit(main())
