import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STATE=ROOT/"actualization_operator_continuation_state.json"

def validate(data):
    errors=[]
    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")

    root=data.get("root_invariant",{})
    if root.get("role")!="FOUNDATIONAL_ROOT":
        errors.append("root role invalid")
    if root.get("scope")!="ACTUALIZATION_DOMAIN":
        errors.append("root scope must be ACTUALIZATION_DOMAIN")

    objects=data.get("objects",{})
    required={"global_invariant","local_argument","result","continuation","domain"}
    missing=required-set(objects)
    if missing:
        errors.append(f"missing objects: {sorted(missing)}")

    seq=data.get("sequence",[])
    pairs={(x.get("from"),x.get("to")) for x in seq}
    for pair in [("A_n","R_n"),("R_n","A_{n+1}"),("A_{n+1}","R_{n+1}")]:
        if pair not in pairs:
            errors.append(f"missing sequence edge: {pair}")

    scope_rules=" ".join(data.get("scope_rules",[]))
    for rule in [
        "D is possibility space, not actualization trajectory",
        "Dom(P) constrains actualization arguments",
        "R_n is actualized result",
        "A_{n+1} is the next actualization argument state",
        "I_* is foundational invariant and I_n is local argument condition",
        "orthogonal resolution is downstream of continuation",
    ]:
        if rule not in data.get("scope_rules",[]):
            errors.append(f"missing scope rule: {rule}")

    if data.get("frontier",{}).get("state")!="UNRESOLVED":
        errors.append("frontier must remain UNRESOLVED")

    return errors

if __name__=="__main__":
    with STATE.open(encoding="utf-8") as fh:
        data=json.load(fh)
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    raise SystemExit(0 if not errors else 1)
