import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "dirac_frontier.json").read_text(encoding="utf-8"))

assert DATA["frontier_state"] == "UNRESOLVED"
assert DATA["epistemic_status"] == "THEORETICAL_HYPOTHESIS"
assert DATA["result"]["relation_type"] == "STRUCTURAL_CORRESPONDENCE"
assert DATA["result"]["canonical_upgrade"] is False

required_blockers = {
    "carrier undefined",
    "composition law undefined",
    "algebraic identity undefined",
    "metric/bilinear form undefined",
    "anticommutator undefined",
    "matrix representation undefined",
}
assert required_blockers.issubset(set(DATA["blockers"]))

for forbidden in DATA["forbidden_inferences"]:
    assert forbidden

print("STAGE45 DIRAC CORRESPONDENCE TEST PASS")
print("Result: STRUCTURAL_CORRESPONDENCE / THEORETICAL_HYPOTHESIS / UNRESOLVED")
