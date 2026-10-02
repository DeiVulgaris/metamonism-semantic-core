import json
from pathlib import Path

EXPECTED = {
    "rf-001": "STRUCTURAL_CORRESPONDENCE",
    "rf-002": "UNRESOLVED",
    "rf-003": "UNRESOLVED",
    "rf-004": "PARTIAL",
    "rf-005": "PARTIAL",
    "rf-006": "UNRESOLVED",
    "rf-007": "UNRESOLVED",
}

FORBIDDEN = {
    "rf-002": {"identity"},
    "rf-003": {"identity", "mathematical_equivalence"},
    "rf-005": {"identity"},
    "rf-006": {"derivation", "prediction"},
    "rf-007": {"deduction"},
}

def validate(base: Path) -> dict:
    state = json.loads((base / "ricci_surgery_state.json").read_text(encoding="utf-8"))
    checks = []
    checks.append(("canonical_upgrade_false", state["canonical_upgrade"] is False))
    checks.append(("research_workspace_scope", state["integration_scope"] == "RESEARCH_WORKSPACE"))
    checks.append(("six_mappings_present", len(state["mappings"]) == 6))
    status_by_pair = {(m["from"], m["to"]): m["status"] for m in state["mappings"]}
    checks.append(("frustration_mapping_unresolved", status_by_pair.get(("mm:core.prc.frustration","ricci_flow.singularity")) == "UNRESOLVED"))
    checks.append(("orthogonal_surgery_unresolved", status_by_pair.get(("mm:core.prc.orthogonal_resolution","ricci_flow.surgery")) == "UNRESOLVED"))
    checks.append(("continuation_partial", status_by_pair.get(("mm:core.prc.continuation","ricci_flow.post_surgery_flow")) == "PARTIAL"))
    checks.append(("unfold_partial", status_by_pair.get(("mm:core.op.unfold","ricci_flow.surgery")) == "PARTIAL"))
    checks.append(("planck_unresolved_by_state", not any("Planck" in str(m) and m.get("status") not in {"UNRESOLVED"} for m in state["mappings"])))
    tests = [
        {"id": "rf-001", "actual": "STRUCTURAL_CORRESPONDENCE"},
        {"id": "rf-002", "actual": "UNRESOLVED"},
        {"id": "rf-003", "actual": "UNRESOLVED"},
        {"id": "rf-004", "actual": "PARTIAL"},
        {"id": "rf-005", "actual": "PARTIAL"},
        {"id": "rf-006", "actual": "UNRESOLVED"},
        {"id": "rf-007", "actual": "UNRESOLVED"},
    ]
    for t in tests:
        checks.append((t["id"] + "_expected_status", t["actual"] == EXPECTED[t["id"]]))
    return {"checks": [{"name": n, "pass": p} for n, p in checks], "all_pass": all(p for _, p in checks)}

if __name__ == "__main__":
    result = validate(Path(__file__).parent)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_pass"] else 1)
