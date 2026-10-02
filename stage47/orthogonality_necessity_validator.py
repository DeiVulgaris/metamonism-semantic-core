import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "orthogonality_necessity_state.json"

def validate(data):
    errors=[]
    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")
    root=data.get("root",{})
    if root.get("id")!="axiom_ban_of_absolute_identity":
        errors.append("wrong root")
    if root.get("status")!="SOURCE":
        errors.append("root must be SOURCE")

    results={x.get("id"):x for x in data.get("results",[])}
    if results.get("R0",{}).get("status")!="INFERENCE":
        errors.append("R0 must record the negative result as INFERENCE")
    if results.get("R3",{}).get("claim","").endswith("orthogonality.") :
        errors.append("non-redundancy must not be equated with orthogonality")

    unique=data.get("uniqueness_targets",{})
    if unique.get("unique_principle")=="PROVEN":
        errors.append("unique resolution principle cannot be PROVEN here")

    if data.get("frontier",{}).get("state")!="UNRESOLVED":
        errors.append("frontier must remain UNRESOLVED")

    return errors

def main():
    with STATE.open(encoding="utf-8") as fh:
        data=json.load(fh)
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
