#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def main():
    reg=read("stage25/query_registry.yaml")
    tests=read("stage25/test_vectors.yaml")
    checks=[
      ("Q5 executable","Q5:" in reg and "EXECUTABLE" in reg),
      ("Q6 executable","Q6:" in reg and "EXECUTABLE" in reg),
      ("Q7 executable","Q7:" in reg and "EXECUTABLE" in reg),
      ("Q9 executable","Q9:" in reg and "EXECUTABLE" in reg),
      ("9 test vectors",len(re.findall(r"T25-\d+",tests))==9),
      ("prohibited boundary vectors",all(x in tests for x in ["identity","model_core","hypothesis","independence"])),
    ]
    for n,ok in checks: print(n,"PASS" if ok else "FAIL")
    return 0 if all(ok for _,ok in checks) else 1
if __name__=="__main__": sys.exit(main())
