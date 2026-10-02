import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STATE=ROOT/"minimal_continuation_map_state.json"

def validate(data):
    errors=[]
    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")
    root=data.get("root_invariant",{})
    if root.get("id")!="axiom_ban_of_absolute_identity":
        errors.append("wrong root invariant")
    if root.get("scope")!="ACTUALIZATION_DOMAIN":
        errors.append("wrong root scope")

    c=data.get("constraints",[])
    required=[
        "F(R_n)=(D_{n+1},I_{n+1})",
        "F(R_n) in Dom(P)",
        "P(F(R_n))=R_{n+1}",
        "F introduces no new fundamental invariant",
        "F preserves trajectory continuity",
        "F produces a nontrivial successor",
    ]
    for item in required:
        if item not in c:
            errors.append(f"missing constraint: {item}")

    split=data.get("status_split",{})
    if split.get("source_definition_of_F")!="SOURCE":
        errors.append("source definition of F must remain SOURCE")
    if split.get("explicit_internal_formula")!="UNRESOLVED":
        errors.append("explicit internal formula must remain UNRESOLVED")
    if split.get("geometry")!="DOWNSTREAM":
        errors.append("geometry must remain downstream")

    return errors

if __name__=="__main__":
    with STATE.open(encoding="utf-8") as fh:
        data=json.load(fh)
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    raise SystemExit(0 if not errors else 1)
