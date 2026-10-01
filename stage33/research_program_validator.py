"""Stage 33 validator: research programs preserve open-ended reasoning without
promoting working hypotheses into canonical claims.
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "research_program_schema.yaml"
PROGRAMS = ROOT / "research_programs.yaml"

ALLOWED_STATUS = {
    "SOURCE", "INFERENCE", "FORMALIZATION", "THEORETICAL_HYPOTHESIS",
    "PROPOSAL", "UNRESOLVED", "CONFLICT", "USED_BUT_UNDEFINED",
    "PRIOR_THEORETICAL_FORMULATION", "MODEL_SPECIFIC",
}

REQUIRED = {
    "id", "title", "question", "status", "lifecycle", "provenance",
    "source_claims", "working_entities", "proposed_relations",
    "required_definitions", "tests", "open_questions",
    "forbidden_inferences", "next_transition",
}

def fail(msg):
    raise AssertionError(msg)

def provenance_ok(p):
    return all(p.get(k) for k in ("repository", "path", "ref", "locator"))

def main():
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    data = yaml.safe_load(PROGRAMS.read_text(encoding="utf-8"))

    assert schema["object_type"] == "RESEARCH_PROGRAM"
    programs = data["programs"]
    assert programs, "no research programs"

    ids = set()

    for p in programs:
        missing = REQUIRED - set(p)
        assert not missing, f"{p.get('id')}: missing {sorted(missing)}"
        assert p["id"].startswith("mm:rp.")
        assert p["id"] not in ids, f"duplicate program id: {p['id']}"
        ids.add(p["id"])
        assert p["status"] in ALLOWED_STATUS
        assert provenance_ok(p["provenance"]), f"{p['id']}: bad program provenance"

        for c in p["source_claims"]:
            assert c["id"] and c["source_claim"]
            assert c["status"] in ALLOWED_STATUS
            assert provenance_ok(c["provenance"]), f"{c['id']}: bad provenance"
            if c["status"] != "SOURCE":
                assert c.get("derived_from"), f"{c['id']}: missing derived_from"

        for e in p["working_entities"]:
            assert e["id"] and e["label"] and e["kind"]
            assert e["status"] in ALLOWED_STATUS
            assert provenance_ok(e["provenance"]), f"{e['id']}: bad provenance"

        for r in p["proposed_relations"]:
            assert r["source"] and r["relation"] and r["target"]
            assert r["status"] in ALLOWED_STATUS
            assert provenance_ok(r["provenance"]), f"{r['relation']}: bad provenance"
            if r["status"] != "SOURCE":
                assert r.get("derived_from"), (
                    f"{r['source']}->{r['target']}: missing derived_from"
                )
            assert r["relation"] not in {
                "IDENTITY", "FORMAL_ISOMORPHISM"
            } or r["status"] == "SOURCE", (
                f"{p['id']}: working relation cannot self-promote to {r['relation']}"
            )

        for f in p.get("candidate_formalizations", []):
            assert f["expression"] and f["role"] and f["status"]
            if f["status"] != "SOURCE":
                assert f.get("validation") is not None

        for d in p["required_definitions"]:
            assert d["term"] and d["question"]
            assert isinstance(d["blocking"], bool)

        for t in p["tests"]:
            for key in ("id", "test", "expected_observation", "falsifier", "status"):
                assert t.get(key) is not None, f"{p['id']}: incomplete test"

        assert p["question"].strip().endswith("?"), (
            f"{p['id']}: research question must remain explicitly open"
        )

        nxt = p["next_transition"]
        for key in ("trigger", "action", "evidence_required"):
            assert nxt.get(key), f"{p['id']}: missing next transition field"

        # A research program with a non-SOURCE top-level status must remain
        # outside the canonical layer.
        if p["status"] != "SOURCE":
            assert p.get("integration_scope") != "CANONICAL", (
                f"{p['id']}: non-SOURCE program cannot be CANONICAL"
            )

    print(f"PASS: {len(programs)} research programs; invariants preserved.")

if __name__ == "__main__":
    main()
