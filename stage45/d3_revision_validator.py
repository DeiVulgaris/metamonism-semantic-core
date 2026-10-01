import json
from pathlib import Path
import yaml

ROOT = Path(__file__).parent

def main():
    state = json.loads((ROOT / "d3_revision_state.json").read_text(encoding="utf-8"))
    vectors = yaml.safe_load((ROOT / "d3_revision_test_vectors.yaml").read_text(encoding="utf-8"))
    required = ["revision_id","revision_of","status","epistemic_status","source_basis","source_claims","formalization","not_established","next_tests","canonical_promotion"]
    missing = [k for k in required if k not in state]
    assert not missing, f"missing fields: {missing}"
    assert state["revision_of"] == "stage45/d3_state.json"
    assert state["canonical_promotion"] is False
    assert state["epistemic_status"] == "FORMALIZATION"
    for k in ["continuation_set","exhaustion","frustration","regime_transition","orientation_update"]:
        assert k in state["formalization"]
    assert vectors["suite"] == "D3R_EXHAUSTION_REVISION"
    assert len(vectors["cases"]) == 8
    assert sum(c.get("expected_result") == "REJECT" for c in vectors["cases"]) >= 6
    print("D3R VALIDATION: PASS")

if __name__ == "__main__":
    main()
