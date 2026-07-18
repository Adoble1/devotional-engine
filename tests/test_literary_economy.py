from types import SimpleNamespace

from devotional_engine import EngineConfig, EngineContext
from devotional_engine.literary import (
    audit_literary_economy,
    build_poem_design,
    dedupe_boundaries,
    prune_local_constraints,
)


def test_short_qualia_survive_deduplication() -> None:
    assert dedupe_boundaries(["razor", "root", "razor", "oil"]) == [
        "razor",
        "root",
        "oil",
    ]


def test_grounded_risk_rules_are_not_repeated_as_local_constraints() -> None:
    rule = "Do not invent motives for Doeg."
    assert prune_local_constraints(
        [rule, "Keep the olive image quiet."],
        [{"avoidance_rule": rule}],
        [],
    ) == ["Keep the olive image quiet."]


def test_poem_design_is_separate_from_prose_burdens() -> None:
    design = build_poem_design(
        {
            "poem_design": {
                "image_field": ["razor", "olive tree"],
                "sensory_palette": ["steel", "root", "oil"],
                "sonic_movement": "hard opening, long-vowel close",
                "emotional_turn": "from flash to rooted quiet",
            }
        },
        {},
    )
    assert design["image_field"] == ["razor", "olive tree"]
    assert "do not summarize the reflection" in design["prohibited_exposition"]


def test_audit_flags_exposition_and_missing_qualia_without_hard_coding_form() -> None:
    ctx = EngineContext(chapter_ref="Psalm 52")
    ctx.prose = {
        "introduction": "Brief opening.",
        "reflection": "Brief reflection.",
        "christ_fulfillment": "Brief fulfillment.",
        "application": "Brief application.",
        "prayer": "Brief prayer.",
    }
    ctx.poem = (
        "This means the speaker cannot remain secure forever.\n"
        "The psalm teaches that divine judgment exposes false refuge.\n"
        "We learn that truthful speech must replace manipulation.\n"
        "Therefore the believer should trust God instead of wealth.\n"
        "In conclusion, careful speech is the proper response.\n"
        "The final lesson is obedience and gratitude before God."
    )
    blueprint = SimpleNamespace(
        poem_design={"sensory_palette": ["razor", "root", "olive leaf"]}
    )
    codes = {
        finding.code
        for finding in audit_literary_economy(ctx, blueprint, EngineConfig())
    }
    assert "LE06" in codes
    assert "LE08" in codes
