import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STATE=ROOT/"actualization_domain_scope_state.json"

def validate(data):
    errors=[]
    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")
    roots=data.get("roots",[])
    ids={r.get("id") for r in roots}
    if ids != {"R0","R1"}:
        errors.append("both phenomenological and actualization roots are required")

    r1=next((r for r in roots if r.get("id")=="R1"),{})
    if r1.get("scope")!="ACTUALIZATION_DOMAIN":
        errors.append("R1 must be scoped to ACTUALIZATION_DOMAIN")

    chain=data.get("active_chain",[])
    if not chain or chain[0].get("id")!="A0":
        errors.append("active chain must begin at A0")

    for node in chain:
        if not node.get("scope"):
            errors.append(f"{node.get('id')} missing scope")
        for parent in node.get("from",[]):
            if parent not in ids and parent not in {x.get("id") for x in chain}:
                errors.append(f"{node.get('id')} references unknown parent {parent}")

    a8=next((x for x in chain if x.get("id")=="A8"),{})
    if a8.get("status")!="SOURCE":
        errors.append("Chapter 2 orthogonal resolution must be SOURCE at processual level")

    anti=" ".join(data.get("anti_inflation",[]))
    required=[
        "The invariant constrains actualization, not the total possibility space.",
        "A possible configuration is not automatically an actualized state.",
        "Chapter 2 consequences are scoped to continuing actualization.",
        "D_perp is local to an actualized state and regime."
    ]
    for item in required:
        if item not in anti:
            errors.append(f"missing anti-inflation rule: {item}")

    return errors

if __name__=="__main__":
    with STATE.open(encoding="utf-8") as fh:
        data=json.load(fh)
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    raise SystemExit(0 if not errors else 1)
