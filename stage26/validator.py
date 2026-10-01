#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def main():
    c=json.loads(read("stage26/dissipation_case.json"))
    t=read("stage26/test_vectors.yaml")
    checks=[
      ("case has A/B/C",all(x in c["source_derived"] for x in ["A","B","C"])),
      ("cross-source status is PARTIAL",c["cross_inventory_result"]["status"]=="PARTIAL"),
      ("identity is not established","A/B/C dissipation are identical." in c["cross_inventory_result"]["not_established"]),
      ("isomorphism is not established","A/B/C dissipation are mathematically isomorphic." in c["cross_inventory_result"]["not_established"]),
      ("six tests",t.count("T26-") == 6),
    ]
    for n,ok in checks: print(n,"PASS" if ok else "FAIL")
    return 0 if all(ok for _,ok in checks) else 1
if __name__=="__main__": sys.exit(main())
