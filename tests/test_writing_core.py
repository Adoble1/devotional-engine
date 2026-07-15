import pytest

from devotional_engine.agents import MockAgentAdapter
from devotional_engine.exceptions import ValidationError
from devotional_engine.writing_core import (
    WritingRequest,
    approve_planning_packet,
    build_planning_packet,
    run_profiled_engine,
)


def fiction_plan():
    return {
        "governing_question": "Will Mara tell the truth before the bridge opens?",
        "truth_contract": ["No one crosses the raised bridge.", "Mara knows the signal code."],
        "local_constraints": ["Keep the scene in Mara's point of view."],
        "planning_maps": {
            "truth_map": {"established": ["night", "raised bridge"]},
            "revelation_map": {"entry": "alarm", "turn": "Mara recognizes the signal"},
            "reader_transformation_map": {"from": "suspicion", "to": "recognition"},
            "art_direction": {"register": "compressed suspense"},
            "world_state": {"bridge": "raised", "weather": "dry"},
            "character_state": {"Mara": {"desire": "protect her brother", "knowledge": "signal code"}},
            "causal_scene_map": {"alarm": "crowd stops", "recognition": "Mara must choose"},
            "continuity_ledger": {"chapter_3": "Mara learned the code"},
        },
    }


def fiction_evaluation(verdict="Pass"):
    return {
        "verdict": verdict,
        "dimensions": {
            "world_coherence": 9,
            "character_coherence": 9,
            "causal_coherence": 9,
            "narrative_tension": 8,
            "prose_quality": 8,
        },
    }


def test_profiled_fiction_run_uses_only_fiction_requirements():
    request = WritingRequest(
        mode="fiction",
        project_ref="Bridge novel / chapter 4",
        source_material="Existing continuity ledger.",
        plan=fiction_plan(),
    )
    adapter = MockAgentAdapter(
        {
            "profile_composer": {
                "title": "The Signal",
                "body": "The bridge stayed raised while Mara counted the bells.",
                "continuity_updates": {"Mara": "revealed knowledge of the code"},
            },
            "profile_evaluator": fiction_evaluation(),
        }
    )
    result = run_profiled_engine(request, adapter)
    assert result.packet.approved
    assert result.revision_count == 0
    assert "canonical_map" not in result.packet.planning_maps


def test_profiled_runner_permits_one_bounded_revision():
    evaluations = iter([fiction_evaluation("Revise"), fiction_evaluation("Pass")])
    adapter = MockAgentAdapter(
        {
            "profile_composer": {
                "title": "The Signal",
                "body": "Mara heard the bells.",
                "continuity_updates": {"Mara": "heard the code"},
            },
            "profile_reviser": {
                "title": "The Signal",
                "body": "The bridge stayed raised. Mara heard the third bell and knew who sent it.",
                "continuity_updates": {"Mara": "recognized the code"},
            },
            "profile_evaluator": lambda payload: next(evaluations),
        }
    )
    result = run_profiled_engine(
        WritingRequest("fiction", "chapter 4", "continuity", fiction_plan()),
        adapter,
    )
    assert result.revision_count == 1
    assert "third bell" in result.draft["body"]


def test_missing_profile_map_fails_closed():
    plan = fiction_plan()
    del plan["planning_maps"]["world_state"]
    packet = build_planning_packet("fiction", "chapter 4", plan)
    findings = approve_planning_packet(packet)
    assert any(item.field == "planning_maps.world_state" for item in findings)
    with pytest.raises(ValidationError):
        run_profiled_engine(
            WritingRequest("fiction", "chapter 4", "continuity", plan),
            MockAgentAdapter({}),
        )


def test_nonfiction_profile_requires_sources_and_evidence_dimensions():
    plan = {
        "governing_question": "What caused the observed change?",
        "truth_contract": ["Separate measured data from interpretation."],
        "planning_maps": {
            "truth_map": {"data": "measured"},
            "revelation_map": {"order": ["finding", "cause", "limits"]},
            "reader_transformation_map": {"from": "correlation", "to": "qualified inference"},
            "art_direction": {"register": "plain analytical prose"},
            "claim_evidence_map": {"claim_1": "dataset row 4"},
            "argument_map": {"premise": "observation", "conclusion": "qualified cause"},
            "uncertainty_ledger": {"sample_size": "small"},
            "source_ledger": {"dataset": "internal study"},
        },
    }
    adapter = MockAgentAdapter(
        {
            "profile_composer": {
                "title": "Measured Change",
                "body": "The data show a change, but the sample does not establish a universal cause.",
                "sources": ["internal study"],
            },
            "profile_evaluator": {
                "verdict": "Pass",
                "dimensions": {
                    "factual_accuracy": 9,
                    "evidence_quality": 8,
                    "argument_coherence": 9,
                    "uncertainty_calibration": 9,
                    "clarity": 9,
                },
            },
        }
    )
    result = run_profiled_engine(
        WritingRequest("nonfiction", "analysis memo", "study data", plan),
        adapter,
    )
    assert result.packet.mode == "nonfiction"
    assert result.draft["sources"] == ["internal study"]
