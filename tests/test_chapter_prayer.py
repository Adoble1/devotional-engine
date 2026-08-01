from __future__ import annotations

from copy import deepcopy

import pytest

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter
from devotional_engine.prayer_control import (
    ChapterPrayerAdapter,
    ChapterPrayerError,
    validate_prayer_design,
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
                "reference": "Psalm 68:1-3",
                "claim": "God rises, scatters His enemies, and gives joy to the righteous.",
            },
            {
                "id": "E2",
                "reference": "Psalm 68:5-6",
                "claim": "God is Father of the fatherless, protector of widows, and a home for the lonely.",
            },
            {
                "id": "E3",
                "reference": "Psalm 68:7-10, 19",
                "claim": "God goes before His people, provides for them, and daily bears them up.",
            },
            {
                "id": "E4",
                "reference": "Psalm 68:18; Ephesians 4:8-13",
                "claim": "The victorious ascent is applied to Christ, who gives gifts to His church.",
            },
            {
                "id": "E5",
                "reference": "Psalm 68:32-35",
                "claim": "The kingdoms sing, and God gives power and strength to His people.",
            },
        ],
        "canonical_relationship": {
            "classification": "explicit_interpretation",
            "description": "Ephesians 4 applies Psalm 68:18 to Christ's ascent and gifts.",
        },
    }


def _plan() -> dict:
    return {
        "prayer_design": {
            "mode": "chapter_shaped_corporate",
            "voice": "first_person_plural",
            "address": {
                "opening": "Our Father",
                "divine_identity": "Father of the fatherless and protector of widows",
                "evidence_ids": ["E2"],
            },
            "movements": [
                {
                    "function": "petition",
                    "chapter_position": 1,
                    "chapter_action": "God rises and scatters hostile powers.",
                    "prayer_transformation": "Arise among us and scatter what resists Your righteous rule.",
                    "evidence_ids": ["E1"],
                },
                {
                    "function": "intercession",
                    "chapter_position": 2,
                    "chapter_action": "God protects the vulnerable and gives the lonely a home.",
                    "prayer_transformation": "Make us defenders of the vulnerable and a faithful home for the lonely.",
                    "evidence_ids": ["E2"],
                },
                {
                    "function": "dependence",
                    "chapter_position": 3,
                    "chapter_action": "God goes before and daily bears His people.",
                    "prayer_transformation": "Go before us, provide for us, and bear us up day by day.",
                    "evidence_ids": ["E3"],
                },
                {
                    "function": "human_response",
                    "chapter_position": 4,
                    "chapter_action": "God's people gather in praise and receive strength for service.",
                    "prayer_transformation": "Teach us to carry one another and bring us into Your presence with praise.",
                    "evidence_ids": ["E3", "E5"],
                },
                {
                    "function": "christological_resolution",
                    "chapter_position": 5,
                    "chapter_action": "The victorious ascent is fulfilled in Christ, who gives gifts.",
                    "prayer_transformation": "Through the risen and ascended Christ, strengthen Your church and let all the earth rejoice.",
                    "evidence_ids": ["E4", "E5"],
                    "source_refs": ["Ephesians 4:8-13"],
                },
            ],
            "target_words": {"minimum": 90, "maximum": 150},
        }
    }


def _valid_prayer() -> str:
    return (
        "Our Father, arise among us and scatter what resists Your righteous rule. "
        "Be the Father of the fatherless, the protector of widows, and a faithful home for the lonely. "
        "Teach us to defend the vulnerable and welcome those who stand alone. Go before us, provide for us, "
        "and bear us up day by day. Keep us from trusting our own strength, and teach us to carry one another "
        "in love. Bring us into Your presence with praise. Through the risen and ascended Christ, free us from "
        "bondage and use His gifts to strengthen Your church. Give power to Your people, and let all the earth "
        "rejoice before You. Through Jesus Christ our Lord. Amen."
    )


def _review(score: float = 9.0) -> dict:
    return {
        "verdict": "Pass",
        "hard_findings": [],
        "advisory_findings": [],
        "dimensions": {"chapter_shaped_prayer": score},
    }


def test_psalm_68_prayer_design_is_validated_forwarded_and_audited() -> None:
    delegate = RecordingAdapter(
        {
            "devotional_planner": _plan(),
            "devotional_composer": {"prayer": _valid_prayer()},
            "devotional_reviewer": _review(),
        }
    )
    ctx = EngineContext(chapter_ref="Psalm 68")
    adapter = ChapterPrayerAdapter(delegate, ctx, EngineConfig())

    plan = adapter.call(
        "devotional_planner",
        {"grounding": _grounding(), "planning_instruction": "Build the blueprint."},
    )
    planner_payload = delegate.calls[0][1]
    assert "chapter_shaped_corporate" in planner_payload["planning_instruction"]
    assert plan["prayer_design"]["movements"][0]["chapter_position"] == 1
    assert ctx.chapter_prayer_contract["voice"] == "first_person_plural"

    adapter.call("devotional_composer", {"composition_packet": {}})
    composer_payload = delegate.calls[1][1]
    assert composer_payload["composition_packet"]["chapter_prayer_contract"] == ctx.chapter_prayer_contract
    assert "first-person-plural" in composer_payload["composition_packet"]["prayer_instruction"]
    assert adapter.draft_findings == []

    review = adapter.call("devotional_reviewer", {"review_instruction": "Review truth."})
    reviewer_payload = delegate.calls[2][1]
    assert "could move unchanged" in reviewer_payload["review_instruction"]
    assert review["verdict"] == "Pass"
    assert ctx.scores["chapter_shaped_prayer"] == 9.0


def test_unknown_prayer_evidence_id_fails_closed() -> None:
    plan = _plan()
    plan["prayer_design"]["movements"][0]["evidence_ids"] = ["E99"]
    _, findings = validate_prayer_design(plan, _grounding())
    assert any(item.code == "CP11" for item in findings)

    delegate = RecordingAdapter({"devotional_planner": plan})
    adapter = ChapterPrayerAdapter(
        delegate,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(),
    )
    with pytest.raises(ChapterPrayerError):
        adapter.call("devotional_planner", {"grounding": _grounding()})


def test_prayer_requires_human_response_and_chapter_order() -> None:
    plan = _plan()
    plan["prayer_design"]["movements"][3]["function"] = "petition"
    plan["prayer_design"]["movements"][2]["chapter_position"] = 1

    _, findings = validate_prayer_design(plan, _grounding())
    codes = {item.code for item in findings}
    assert "CP09" in codes
    assert "CP13" in codes


def test_generic_singular_prayer_routes_to_targeted_revision() -> None:
    delegate = RecordingAdapter(
        {
            "devotional_planner": _plan(),
            "devotional_composer": {"prayer": "Father, help me today. Amen."},
            "devotional_reviewer": _review(),
        }
    )
    adapter = ChapterPrayerAdapter(
        delegate,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(),
    )
    adapter.call("devotional_planner", {"grounding": _grounding()})
    adapter.call("devotional_composer", {"composition_packet": {}})
    review = adapter.call("devotional_reviewer", {})

    assert review["verdict"] == "Revise"
    codes = {item["code"] for item in review["hard_findings"]}
    assert {"CP_D02", "CP_D03"}.issubset(codes)


def test_low_chapter_prayer_score_routes_to_revision() -> None:
    delegate = RecordingAdapter(
        {
            "devotional_planner": _plan(),
            "devotional_composer": {"prayer": _valid_prayer()},
            "devotional_reviewer": _review(6.0),
        }
    )
    adapter = ChapterPrayerAdapter(
        delegate,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(integrated_review_min_score=8.0),
    )
    adapter.call("devotional_planner", {"grounding": _grounding()})
    adapter.call("devotional_composer", {"composition_packet": {}})
    review = adapter.call("devotional_reviewer", {})

    assert review["verdict"] == "Revise"
    assert any(item["code"] == "CP_R02" for item in review["hard_findings"])


def test_mock_payload_shape_remains_unchanged() -> None:
    captured: dict = {}

    def planner(payload: dict) -> dict:
        captured.update(deepcopy(payload))
        return {"fixture": True}

    mock = MockAgentAdapter({"devotional_planner": planner})
    adapter = ChapterPrayerAdapter(
        mock,
        EngineContext(chapter_ref="Psalm 68"),
        EngineConfig(),
    )
    original = {"grounding": {"fixture": True}, "planning_instruction": "unchanged"}
    result = adapter.call("devotional_planner", deepcopy(original))

    assert captured == original
    assert result == {"fixture": True}
