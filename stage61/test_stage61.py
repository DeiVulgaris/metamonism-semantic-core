#!/usr/bin/env python3
"""Stage 61 executable test matrix."""

from impact_localizer import locate_impact


def trace():
    return {
        "trace_id": "TRACE-61",
        "question_id": "Q-61",
        "root_invariant": {"id": "ROOT", "statement": "root"},
        "steps": [
            {"step_id": "S1", "from_id": "ROOT", "to_id": "A", "status": "SOURCE"},
            {"step_id": "S2", "from_id": "A", "to_id": "B", "status": "SOURCE"},
            {"step_id": "S3", "from_id": "B", "to_id": "C", "status": "UNRESOLVED"},
            {"step_id": "S4", "from_id": "C", "to_id": "D", "status": "BLOCKED"},
        ],
        "information_result": {"classification_id": "CLS-61"},
        "provenance": {"stage": "60"},
    }


def classification(result_class, affected=None):
    result = {"classification_id": f"CLS-{result_class}", "result_class": result_class}
    if affected:
        result["affected_step_id"] = affected
    return result


def main():
    explicit = locate_impact(trace(), classification("CONTRADICTION_FOUND", "S3"))
    assert explicit["status"] == "READY"
    assert explicit["impact_mode"] == "EXPLICIT_STEP_REFERENCE"
    assert explicit["anchor_step_id"] == "S3"
    assert explicit["reasoning_prefix"] == ["S1", "S2", "S3"]
    assert explicit["affected_step"]["information_effect"] == "REQUIRES_RECONCILIATION"
    assert [s["step_id"] for s in explicit["downstream_steps"]] == ["S4"]
    assert explicit["downstream_steps"][0]["replay_status"] == "REQUIRES_REPLAY"

    fallback = locate_impact(trace(), classification("EVIDENCE_FOUND"))
    assert fallback["status"] == "READY"
    assert fallback["impact_mode"] == "TAIL_FALLBACK"
    assert fallback["anchor_step_id"] == "S4"
    assert fallback["reasoning_prefix"] == ["S1", "S2", "S3", "S4"]

    missing = locate_impact(trace(), classification("CONTRADICTION_FOUND", "NOPE"))
    assert missing["status"] == "BLOCKED"
    assert "affected_step_not_found:NOPE" in missing["errors"]

    print("Stage 61 tests: PASS")


if __name__ == "__main__":
    main()
