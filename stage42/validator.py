"""Validation gate for Stage 42."""

from identity_registry import IdentityMapping, IdentityRegistry

def validate_record(r):
    required = {
        "mapping_id","left_ref","right_ref","relation_type",
        "assertion_status","scope","evidence","provenance"
    }
    assert required <= set(r), "required field missing"
    assert r["relation_type"] in {
        "IDENTITY_EQUIVALENCE","ALIAS","VERSION_CONTINUATION",
        "DERIVATION","FORK","MERGE","UNRESOLVED_IDENTITY"
    }
    assert r["assertion_status"] in {"PROPOSED","ASSERTED","REJECTED","UNRESOLVED"}
    assert r["scope"] in {"RESEARCH_PROGRAM","RESEARCH_TRAJECTORY","RESEARCH_FRONTIER","RESEARCH_TASK"}
    for k in ("repository","path","ref","locator"):
        assert r["provenance"].get(k), "incomplete provenance"
    if r["assertion_status"] == "ASSERTED":
        assert r["evidence"] and r.get("derived_from"), "asserted mapping lacks trace"
    if r["relation_type"] == "UNRESOLVED_IDENTITY":
        assert r["assertion_status"] != "ASSERTED"
    return True

def run():
    vectors = [
        {
            "mapping_id":"ID-001",
            "left_ref":"mm:rp.r1_r4_dirac",
            "right_ref":"RP-r1r4-dirac",
            "relation_type":"ALIAS",
            "assertion_status":"ASSERTED",
            "scope":"RESEARCH_PROGRAM",
            "evidence":["stage41 identifier-continuity finding"],
            "provenance":{"repository":"DeiVulgaris/metamonism-semantic-core","path":"stage41/run_report.json","ref":"24b3211ef548029a4979ea290faa64433ff82a3e","locator":"finding"},
            "derived_from":["stage41 identifier-continuity finding"]
        },
        {
            "mapping_id":"ID-002",
            "left_ref":"RP-a","right_ref":"RP-b",
            "relation_type":"FORK","assertion_status":"ASSERTED",
            "scope":"RESEARCH_PROGRAM",
            "evidence":["explicit fork declaration"],
            "provenance":{"repository":"DeiVulgaris/metamonism-semantic-core","path":"stage42/test_vectors.yaml","ref":"stage42","locator":"fork"},
            "derived_from":["explicit fork declaration"]
        },
        {
            "mapping_id":"ID-003",
            "left_ref":"RP-x","right_ref":"RP-y",
            "relation_type":"UNRESOLVED_IDENTITY","assertion_status":"UNRESOLVED",
            "scope":"RESEARCH_PROGRAM",
            "evidence":["similar labels only"],
            "provenance":{"repository":"DeiVulgaris/metamonism-semantic-core","path":"stage42/test_vectors.yaml","ref":"stage42","locator":"unresolved"},
            "derived_from":["similar labels only"]
        }
    ]
    reg = IdentityRegistry()
    for v in vectors:
        validate_record(v)
        reg.register(IdentityMapping(**v))
    assert len(reg.resolve("mm:rp.r1_r4_dirac")) == 1
    assert reg.resolve("RP-x") == []
    assert reg.unresolved("RP-x")
    print("STAGE42 PASS")

if __name__ == "__main__":
    run()
