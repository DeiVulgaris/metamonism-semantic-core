from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parent
CASE = ROOT / "cmi_chain_case.json"
VECTORS = ROOT / "test_vectors.yaml"

ALLOWED_RESULTS = {
    "SAME_CONTENT",
    "EQUIVALENT_FORMULATION",
    "STRUCTURAL_CORRESPONDENCE",
    "EXTENSION",
    "PARTIAL",
    "UNRESOLVED",
    "PROHIBITED_INFERENCE",
}

def main():
    case = json.loads(CASE.read_text(encoding="utf-8"))
    vectors = yaml.safe_load(VECTORS.read_text(encoding="utf-8"))

    assert case["cross_inventory_result"]["result"] == "EXTENSION"
    assert case["source_derived"]["cmi"]["status"] == "SOURCE"
    assert case["source_derived"]["cmi_chain"]["status"] == "SOURCE"

    relation = case["source_derived"]["relation"]
    assert relation["relation_id"] == "mm:rel.extends"
    assert relation["source"] == "mm:core.prc.cmi_chain"
    assert relation["target"] == "mm:core.prc.cmi"
    assert relation["status"] == "SOURCE"
    assert relation["identity"] == "NOT_ESTABLISHED"

    assert "CMI and CMI Chain are identical." in case["not_established"]
    assert "CMI Chain is merely an equivalent reformulation of CMI." in case["not_established"]

    assert "EXTENSION" in ALLOWED_RESULTS
    assert len(vectors["vectors"]) == 10

    forbidden = [v for v in vectors["vectors"] if v["expected"] == "PROHIBITED_INFERENCE"]
    assert len(forbidden) == 5

    print("PASS: Stage 29 CMI/CMI Chain extension benchmark")

if __name__ == "__main__":
    main()
