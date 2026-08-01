from __future__ import annotations

from copy import deepcopy

import pytest

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter
from devotional_engine.poetic_control import (
    PoeticTransformationAdapter,
    PoeticTransformationError,
    validate_poetic_contract,
)


class RecordingAdapter:
    def __init__(self, outputs: dict):
        self.outputs = outputs
        self.calls: list[tuple[str, dict]] = []

    def call(self, role: str, payload: dict):
        self.calls.append((role, deepcopy(payload)))
        value = self.outputs[role]
        return value(payload) if callable(value) else deepcopy(value)


def _grounding() -> dict:
    return {
        "textual_evidence": [
            {
                "id": "E1",
                "reference": "Psalm 68:1-2",
                "claim": "God rises and His enemies scatter like smoke and melting wax.",
            },
            {
                "id": "E2",
                "reference": "Psalm 68:5-6",
                "claim": "God protects the vulnerable, settles the solitary, and leads prisoners out.",
            },
            {
                "id": "E3",
                "reference": "Psalm 68:19",
                "claim": "The Lord daily bears His people up.",
            },
            {
                "id": "E4",
                "reference": "Psalm 68:18; Ephesians 4:8-13",
                "claim": "The victorious ascent is applied canonically to Christ, who gives gifts.",
            },
        ],
        "canonical_relationship": {
            "classification": "explicit_interpretation",
            "description": "Ephesians 4 applies the ascent language to Christ.",
        },
    }


def _plan() -> dict:
    return {
        "art_direction": {"register": "exultant and pastoral"},
        "poem_design": {
            "imagery_mode": "textual",
            "poetic_strategy": {
                "genre_force": "A processional hymn that rises from conflict into praise.",
                "emotional_tone": "Triumphant without hardness; tender toward the vulnerable.",
                "formal_strategy": "Two common-meter stanzas with alternating rhyme.",
                "discovery": "The strength that scatters evil is the strength that carries the weak.",
            },
            "poetic_transformations": [
                {
                    "phrase": "scatter night",
                    "operation": "bounded_implication",
                    "textual_anchor": "God shall arise, his enemies shall be scattered.",
                    "warrant_ids": ["E1"],
                    "rationale": "Night compresses the moral darkness represented by hostile powers without inventing a scene.",
                },
                {
                    "phrase": "captives leave their chains",
                    "operation": "bounded_implication",
                    "textual_anchor": "He leads out the prisoners to prosperity.",
                    "warrant_ids": ["E2"],
                    "rationale": "Chains are a conventional implication of captivity and intensify release without adding an event.",
                },
                {
                    "phrase": "the risen Christ ascends his throne",
                    "operation": "canonical_echo",
                    "textual_anchor": "You ascended on high, leading captives in your train.",
                    "warrant_ids": ["E4"],
                    "source_refs": ["Ephesians 4:8-13"],
                    "rationale": "The New Testament explicitly applies the ascent to Christ and His gifts to the church.",
                },
            ],
        },
    }


def _review(score: float = 9.0) -> dict:
    return {
        "verdict": "Pass",
        "hard_findings": [],
        "advisory_findings": [],
        "dimensions": {
            "textual_fidelity": 9,
            "theological_accuracy": 9,
            "canonical_warrant": 9,
            "blueprint_alignment": 9,
            "verbal_economy": 9,
            "literary_quality": 9,
            "poetic_integrity": 9,
            "sensory_presence": 8,
            "read_aloud_flow": 9,
            "poetic_transformation": score,
        },
    }


def test_warranted_nonliteral_language_is_accepted_and_forwarded() -> None:
    delegate = RecordingAdapter(
        {
            "devotional_planner": _plan(),
            "devotional_composer": {"poem": "placeholder"},
            "devotional_reviewer": _review(),
        }
    )
    ctx = EngineContext(chapter_ref="Psalm 68")
    adapter = PoeticTransformationAdapter(delegate, ctx, EngineConfig())

    plan = adapter.call(
        "devotional_planner",
        {
            "grounding": _grounding(),
            "planning_instruction": "Build the blueprint.",
        },
    )

    planner_payload = delegate.calls[0][1]
    assert "Scripture supplies the world; poetry supplies the music" in planner_payload["planning_instruction"]
    contract = plan["art_direction"]["poetic_transformation_contract"]
    assert contract["strategy"]["formal_strategy"].startswith("Two common-meter")
    assert {item["phrase"] for item in contract["transformations"]} == {
        "scatter night",
        "captives leave their chains",
        "the risen Christ ascends his throne",
    }

    adapter.call(
        "devotional_composer",
        {"composition_packet": {"economy": {"principles": []}}},
    )
    composer_payload = delegate.calls[1][1]
    assert composer_payload["composition_packet"]["poetic_transformation_contract"] == contract
    assert "do more than excerpt or lineate the passage" in composer_payload["composition_packet"]["economy"]["principles"]

    review = adapter.call("devotional_reviewer", {"review_instruction": "Review truth."})
    reviewer_payload = delegate.calls[2][1]
    assert "merely excerpt or lineate" in reviewer_payload["review_instruction"]
    assert review["verdict"] == "Pass"
    assert ctx.scores["poetic_transformation"] == 9.0


def test_unknown_warrant_id_fails_closed() -> None:
    plan = _plan()
    plan["poem_design"]["poetic_transformations"][0]["warrant_ids"] = ["E99"]
    _, _, findings = validate_poetic_contract(plan, _grounding())
    assert any(item.code == "PT05" for item in findings)

    delegate = RecordingAdapter({"devotional_planner": plan})
    adapter = PoeticTransformationAdapter(
        delegate,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(),
    )
    with pytest.raises(PoeticTransformationError):
        adapter.call("devotional_planner", {"grounding": _grounding()})


def test_low_poetic_transformation_score_routes_to_revision() -> None:
    delegate = RecordingAdapter(
        {
            "devotional_planner": _plan(),
            "devotional_reviewer": _review(6.5),
        }
    )
    adapter = PoeticTransformationAdapter(
        delegate,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(integrated_review_min_score=8.0),
    )
    adapter.call("devotional_planner", {"grounding": _grounding()})
    review = adapter.call("devotional_reviewer", {})

    assert review["verdict"] == "Revise"
    assert any(item["code"] == "PT_R02" for item in review["hard_findings"])


def test_missing_positive_poetic_strategy_fails_even_without_an_image_quota() -> None:
    plan = _plan()
    plan["poem_design"].pop("poetic_strategy")
    plan["poem_design"]["poetic_transformations"] = []

    strategy, transformations, findings = validate_poetic_contract(
        plan,
        _grounding(),
    )
    assert strategy["genre_force"] == ""
    assert transformations == []
    assert {item.code for item in findings} == {"PT01"}


def test_mock_payload_shape_remains_unchanged() -> None:
    captured: dict = {}

    def planner(payload: dict) -> dict:
        captured.update(deepcopy(payload))
        return {"fixture": True}

    mock = MockAgentAdapter({"devotional_planner": planner})
    adapter = PoeticTransformationAdapter(
        mock,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(),
    )
    original = {"grounding": {"fixture": True}, "planning_instruction": "unchanged"}
    result = adapter.call("devotional_planner", deepcopy(original))

    assert captured == original
    assert result == {"fixture": True}
