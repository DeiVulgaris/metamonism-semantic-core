import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "ricci_surgery_corpus_test.json").read_text(encoding="utf-8"))

assert DATA["comparison"]["relation_type"] == "STRUCTURAL_CORRESPONDENCE"
assert DATA["comparison"]["status"] == "THEORETICAL_HYPOTHESIS"
assert DATA["comparison"]["expected_result"] == "UNRESOLVED"
assert DATA["research_result"]["result_class"] == "INCONCLUSIVE"
assert DATA["research_result"]["canonical_upgrade"] is False
assert DATA["research_result"]["successor_frontier_state"] == "UNRESOLVED"

for item in DATA["source_findings"]:
    assert item["status"] == "SOURCE"
    assert "provenance" in item
    assert "locator" in item["provenance"]

for forbidden in DATA["anti_collapse"]["forbidden_inferences"]:
    assert forbidden

print("STAGE45 RICCI-SURGERY CORPUS TEST PASS")
print("Result: STRUCTURAL_CORRESPONDENCE / THEORETICAL_HYPOTHESIS / UNRESOLVED")
