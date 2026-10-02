import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "chapter2_rooted_chain_state.json"

def validate(data):
    errors=[]
    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")

    root=data.get("root",{})
    if root.get("id")!="axiom_ban_of_absolute_identity":
        errors.append("wrong root")
    if root.get("source_status")!="SOURCE":
        errors.append("root must be SOURCE")

    chain=data.get("active_chain",[])
    if not chain:
        errors.append("active chain missing")
    expected_prefix=["C0","C1","C2","C3","C4","C5","C6","C7","C8","C9","C10"]
    ids=[x.get("id") for x in chain]
    if ids[:len(expected_prefix)]!=expected_prefix:
        errors.append("active chain order is invalid")

    c9=next((x for x in chain if x.get("id")=="C9"),{})
    if c9.get("status")!="SOURCE":
        errors.append("C9 orthogonal-resolution necessity must be SOURCE at corpus level")

    corrections=data.get("status_corrections",{})
    if corrections.get("stage47_negative_result")!="retained_as_historical":
        errors.append("stage47 historical result must be retained")
    if corrections.get("current_source_level_orthogonality")!="SOURCE":
        errors.append("source-level orthogonality must now be SOURCE")
    if corrections.get("current_mathematical_orthogonality")!="UNRESOLVED":
        errors.append("mathematical realization must remain unresolved")

    return errors

if __name__=="__main__":
    with STATE.open(encoding="utf-8") as fh:
        data=json.load(fh)
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    raise SystemExit(0 if not errors else 1)
