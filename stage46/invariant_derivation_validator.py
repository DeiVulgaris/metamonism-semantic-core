import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "invariant_derivation_state.json"

ALLOWED_STATUSES = {
    "SOURCE",
    "SOURCE_SUPPORTED",
    "INFERENCE",
    "FORMALIZATION",
    "THEORETICAL_HYPOTHESIS",
}

def load():
    with STATE.open(encoding="utf-8") as f:
        return json.load(f)

def validate(data):
    errors=[]
    chain=data.get("chain",[])
    ids={n.get("id") for n in chain}

    if data.get("canonical_promotion") is not False:
        errors.append("canonical_promotion must remain false")

    root=data.get("root",{})
    if root.get("id")!="axiom_ban_of_absolute_identity":
        errors.append("root invariant must be axiom_ban_of_absolute_identity")
    if root.get("status")!="SOURCE":
        errors.append("root invariant must be SOURCE")

    if not chain or chain[0].get("type")!="ROOT" or chain[0].get("id")!="I0":
        errors.append("chain must begin at I0 ROOT")

    for node in chain:
        if node.get("status") not in ALLOWED_STATUSES:
            errors.append(f"invalid status for {node.get('id')}")
        if node.get("id")!="I0" and not node.get("derived_from"):
            errors.append(f"{node.get('id')} lacks derived_from")

        for parent in node.get("derived_from",[]):
            if parent not in ids:
                errors.append(f"{node.get('id')} references unknown parent {parent}")

    chain_map={n["id"]:n for n in chain}
    def reaches_root(node_id, seen=None):
        seen=set() if seen is None else seen
        if node_id=="I0":
            return True
        if node_id in seen:
            return False
        seen.add(node_id)
        parents=chain_map.get(node_id,{}).get("derived_from",[])
        return bool(parents) and all(reaches_root(p,seen.copy()) for p in parents)

    for node in chain:
        if not reaches_root(node["id"]):
            errors.append(f"{node['id']} has no valid root path")

    i5=chain_map.get("I5",{})
    if i5.get("status")!="THEORETICAL_HYPOTHESIS":
        errors.append("I5 orthogonality step must remain a theoretical hypothesis")

    i10=chain_map.get("I10",{})
    if not any(p=="I5" for p in i10.get("derived_from",[])):
        errors.append("I10 must depend on the orthogonality derivation node I5")

    if "Orthogonality is not treated as the root axiom." not in data.get("invariants",[]):
        errors.append("missing root/orthogonality separation invariant")

    return errors

def main():
    data=load()
    errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for e in errors:
        print("-",e)
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
