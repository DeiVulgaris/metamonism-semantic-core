#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def main():
    reg=read("stage24/query_registry.yaml")
    tests=read("stage24/test_vectors.yaml")
    spec=read("stage24/query_execution_spec.md")
    checks=[
      ("Q1-Q10",all(f"  Q{i}:" in reg for i in range(1,11))),
      ("statuses",all(x in spec for x in ["RESOLVED","PARTIAL","UNRESOLVED","EMPTY","PROHIBITED_INFERENCE"])),
      ("tests",len(re.findall(r"T24-\d+",tests))==6),
      ("read_only","does not modify registries" in spec),
      ("no_registration","does not register derived answers" in spec),
    ]
    for n,ok in checks: print(n,"PASS" if ok else "FAIL")
    return 0 if all(ok for _,ok in checks) else 1
if __name__=="__main__": sys.exit(main())
