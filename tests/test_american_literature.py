from devotional_engine import (
    AMERICAN_PATTERNS,
    CLASSICAL_HYMNODY_PROFILE,
    CREATIVE_MASTERY_LAYER,
    EngineConfig,
    EngineContext,
    MockAgentAdapter,
    State,
    build_style_brief,
    match_american_patterns,
    public_domain_patterns,
    run_engine,
    validate_style_brief,
)
from devotional_engine.harness import run_deterministic_harness


def test_registry_contains_prose_and_poetry_before_1950():
    genres = {pattern.genre for pattern in AMERICAN_PATTERNS if pattern.publication_year <= 1950}
    assert {"prose", "poetry"} <= genres


def test_public_domain_patterns_exclude_restricted_post_1930_work():
    pattern_ids = {pattern.pattern_id for pattern in public_domain_patterns()}
    assert "steinbeck_dust_mercy" not in pattern_ids
    assert "hughes_blues_resilience" not in pattern_ids


def test_match_patterns_returns_craft_guidance_not_source_text():
    matches = match_american_patterns(["forsaken", "beasts", "death", "praise"])
    brief = build_style_brief(matches)
    assert brief["style_sources"]
    assert "named author pastiche" in brief["avoid"]
    assert brief["creative_mastery"] == CREATIVE_MASTERY_LAYER
    assert brief["classical_hymnody"] == CLASSICAL_HYMNODY_PROFILE
    assert "Maintain image physics unless the biblical chapter itself warrants miracle logic." in brief["creative_mastery"]["principles"]
    assert all("page_content" not in source for source in brief["style_sources"])


def test_classical_hymnody_profile_uses_craft_not_archaism():
    guidance = " ".join(CLASSICAL_HYMNODY_PROFILE["poem_guidance"]).lower()
    avoid = " ".join(CLASSICAL_HYMNODY_PROFILE["avoid"]).lower()
    assert "question and answer" in guidance
    assert "repeat a biblical summons" in guidance
    assert "automatic archaisms" in avoid
    assert "rhyme-driven filler" in avoid


def test_creative_mastery_layer_rejects_unsafe_prompt_material():
    flattened = " ".join(
        item
        for values in CREATIVE_MASTERY_LAYER.values()
        for item in values
    ).lower()
    assert "grok" not in flattened
    assert "uncensored" not in flattened
    assert "imitate any author" not in flattened


def test_style_brief_rejects_restricted_pattern():
    failures = validate_style_brief({"style_sources": [{"pattern_id": "steinbeck_dust_mercy"}]})
    assert failures
    assert "restricted" in failures[0]


def test_harness_rejects_restricted_style_brief(context):
    context.literary_style = {"style_sources": [{"pattern_id": "steinbeck_dust_mercy"}]}
    failures, _ = run_deterministic_harness(context)
    assert any("D21" in failure for failure in failures)


def test_harness_accepts_public_domain_style_brief(context):
    context.literary_style = build_style_brief(match_american_patterns(["praise", "nations", "body"]))
    failures, _ = run_deterministic_harness(context)
    assert not any("D21" in failure for failure in failures)


def test_no_post_1950_pattern_is_enabled():
    enabled_years = [pattern.publication_year for pattern in public_domain_patterns()]
    assert max(enabled_years) <= 1930
    assert all(pattern.publication_year <= 1950 for pattern in AMERICAN_PATTERNS if pattern.usage != "blocked_post_cutoff")


def test_engine_auto_builds_style_brief_before_art_direction():
    calls = []

    def art_director(payload):
        calls.append(payload["context"].literary_style)
        return {
            "register": "grave and lyrical",
            "pace": "measured",
            "sentence_music": "pressure and release",
            "image_density": "moderate",
            "emotional_color": "forsaken ache into praise",
            "opening_mode": "threshold phrase",
            "poem_tone": "compressed witness",
            "ending_resonance": "answered song",
            "avoid": ["pastiche"],
        }

    outputs = {
        "source_agent": {"source_text": "My God, my God, why have you forsaken me? Bulls, dogs, dust, death, and praise."},
        "translator": {"working_rendering": "Forsaken prayer becomes praise among the congregation."},
        "chapter_design_mapper": {
            "chapter_start": "Forsaken cry.",
            "chapter_end": "Praise among the nations.",
            "emotional_movement": "Forsaken death becomes praise.",
            "divine_action": "The LORD hears and answers.",
            "physical_vocabulary": ["forsaken", "dogs", "dust", "death", "praise"],
            "central_theological_claim": "God answers the forsaken one.",
            "christward_fulfillment": "Christ enters abandonment and opens praise.",
            "reader_felt_experience": "terror answered by worship",
            "chapter_design_summary": "Lament turns to congregation praise.",
        },
        "canonist": {},
        "theological_risk_agent": {"risks": [{"risk_id": "R1", "risk_description": "avoid collision", "why_it_matters": "truth", "avoidance_rule": "separate metaphor and history", "evaluator_check": "no physical beasts at cross"}]},
        "historian_linguist": {},
        "commentary_agent": {},
        "art_director": art_director,
    }
    context = run_engine(EngineContext(chapter_ref="Psalm 22"), MockAgentAdapter(outputs), EngineConfig(source_min_chars=10))
    assert calls
    assert calls[0]["style_sources"]
    assert calls[0]["classical_hymnody"]["chapter_movement"] == "Forsaken death becomes praise."
    assert context.trace[-1] is State.ESCALATED
    assert "Missing mock output for role: creative_divergence_agent" in context.error
