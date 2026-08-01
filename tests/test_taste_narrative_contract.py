from copy import deepcopy
from types import SimpleNamespace

from devotional_engine import EngineConfig, EngineContext
from devotional_engine.integrated import validate_grounding
from devotional_engine.integrated_v67 import build_blueprint, validate_blueprint
from devotional_engine.literary import audit_literary_economy, composition_packet
from tests.test_integrated_devotional import _grounding, _plan


def _lexical_insight() -> dict:
    return {
        "source_language": "Hebrew",
        "term": "hesed",
        "observation": "The covenant-love term governs the contrast with destructive power.",
        "argument_role": "It moves the devotional from speech as instrument to refuge as the deeper issue.",
    }


def _taste_plan() -> dict:
    plan = deepcopy(_plan())
    plan.update(
        {
            "imagery_mode": "textual",
            "governing_image_candidates": [
                {
                    "image": "a sharpened razor",
                    "textual_anchor": "Your tongue plots destruction, like a sharp razor.",
                    "warrant": "Psalm 52:2 directly compares the destructive tongue to a razor.",
                    "warrant_ids": ["E1"],
                    "sensory_grain": "cold edge and sudden cut",
                    "transformation": "the blade loses authority when the false refuge is uprooted",
                    "ledger_novelty": "not used in the supplied series ledger",
                },
                {
                    "image": "an uprooted refuge",
                    "textual_anchor": "God will break you down forever; he will snatch and tear you from your tent; he will uproot you.",
                    "warrant": "Psalm 52:5 joins removal from the tent with uprooting.",
                    "warrant_ids": ["E2"],
                    "sensory_grain": "removal, tearing, and loosened ground",
                    "transformation": "false security gives way to exposed ground",
                    "ledger_novelty": "not used in the supplied series ledger",
                },
                {
                    "image": "a flourishing olive tree",
                    "textual_anchor": "But I am like a green olive tree in the house of God.",
                    "warrant": "Psalm 52:8 gives the faithful speaker this comparison.",
                    "warrant_ids": ["E3"],
                    "sensory_grain": "root and living leaf",
                    "transformation": "the threatened life becomes rooted praise",
                    "ledger_novelty": "distinct from recent stone and water imagery",
                },
            ],
            "selected_governing_image": "a flourishing olive tree",
            "image_selection_rationale": (
                "The olive tree has direct warrant and carries the psalm's movement from threatened life "
                "to enduring trust without importing a separate scene."
            ),
            "narrative_design": {
                "level": 2,
                "warrant": "The superscription and 1 Samuel 21-22 identify Doeg's report and its consequence.",
                "scope": "One bounded scene, followed by reflection on the psalm's language.",
                "source_basis": "Psalm 52 superscription and 1 Samuel 21-22.",
                "bounded_scene": "Doeg reports to Saul; no motives, weather, or private emotion are invented.",
            },
        }
    )
    plan["poem_design"]["imagery_mode"] = "textual"
    return plan


def test_real_grounding_requires_one_usable_lexical_insight() -> None:
    grounding = _grounding()
    findings = validate_grounding(
        grounding,
        allow_test_fixture=False,
        config=EngineConfig(),
    )
    assert any(item.code == "G08" for item in findings)

    grounding["lexical_insight"] = _lexical_insight()
    findings = validate_grounding(
        grounding,
        allow_test_fixture=False,
        config=EngineConfig(),
    )
    assert not any(item.code in {"G08", "G09"} for item in findings)


def test_production_taste_design_accepts_passage_warranted_candidates() -> None:
    grounding = _grounding()
    grounding["lexical_insight"] = _lexical_insight()
    blueprint = build_blueprint(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        _taste_plan(),
    )

    assert validate_blueprint(blueprint, require_taste_design=True) == []
    assert blueprint.governing_image == "a flourishing olive tree"
    assert blueprint.narrative_design["level"] == 2

    packet = composition_packet(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        blueprint,
        EngineConfig(),
    )
    assert packet["passage"]["lexical_insight"]["term"] == "hesed"
    assert packet["series_continuity"]["candidate_count"] == 3
    assert packet["series_continuity"]["imagery_mode"] == "textual"
    assert packet["narrative_design"]["bounded_scene"]


def test_one_passage_born_candidate_is_enough() -> None:
    grounding = _grounding()
    grounding["lexical_insight"] = _lexical_insight()
    plan = _taste_plan()
    plan["governing_image_candidates"] = [plan["governing_image_candidates"][2]]
    blueprint = build_blueprint(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        plan,
    )

    assert validate_blueprint(blueprint, require_taste_design=True) == []
    assert len(blueprint.poem_design["governing_image_candidates"]) == 1


def test_restrained_mode_does_not_require_images_or_sensory_palette() -> None:
    grounding = _grounding()
    grounding["lexical_insight"] = _lexical_insight()
    plan = deepcopy(_plan())
    plan["imagery_mode"] = "restrained"
    plan["governing_image_candidates"] = []
    plan["selected_governing_image"] = ""
    plan["poem_design"] = {
        "imagery_mode": "restrained",
        "image_field": [],
        "sensory_palette": [],
        "sonic_movement": "communal refrain widening into praise",
        "emotional_turn": "from received mercy to shared praise",
        "prohibited_exposition": ["do not invent a scene"],
    }
    blueprint = build_blueprint(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        plan,
    )

    assert validate_blueprint(blueprint, require_taste_design=True) == []
    assert blueprint.governing_image == ""
    assert blueprint.poem_design["sensory_palette"] == []


def test_unknown_image_warrant_id_fails_closed() -> None:
    grounding = _grounding()
    grounding["lexical_insight"] = _lexical_insight()
    plan = _taste_plan()
    plan["governing_image_candidates"][0]["warrant_ids"] = ["E99"]
    blueprint = build_blueprint(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        plan,
    )

    findings = validate_blueprint(blueprint, require_taste_design=True)
    assert any(item.code == "P10" and "unknown evidence ids" in item.message for item in findings)


def test_deep_narrative_layer_fails_without_a_bounded_scene() -> None:
    grounding = _grounding()
    grounding["lexical_insight"] = _lexical_insight()
    plan = _taste_plan()
    plan["narrative_design"]["bounded_scene"] = ""
    blueprint = build_blueprint(
        EngineContext(chapter_ref="Psalm 52"),
        grounding,
        plan,
    )

    findings = validate_blueprint(blueprint, require_taste_design=True)
    assert any(item.code == "P14" and "bounded_scene" in item.field for item in findings)


def test_human_cadence_checks_are_advisory_not_a_new_hard_style_stack() -> None:
    ctx = EngineContext(chapter_ref="Psalm 52")
    ctx.prose = {
        "introduction": "The blade flashes—really close. The room stays still. The witness looks down. The ruler leans in.",
        "reflection": "Trust is not control. It is surrender. Hope is not denial. It is endurance.",
        "christ_fulfillment": "Christ bears the accusation and rises.",
        "application": "Speak necessary truth without the extra cut.",
        "prayer": "Father, keep our speech truthful through Jesus Christ our Lord.",
    }
    ctx.poem = "Root under earth\nLeaf in the wind"
    blueprint = SimpleNamespace(poem_design={"imagery_mode": "restrained", "sensory_palette": []})

    findings = audit_literary_economy(ctx, blueprint, EngineConfig())
    codes = {item.code for item in findings}
    assert {"LE09", "LE10", "LE11", "LE12"}.issubset(codes)
    assert all(item.severity == "warning" for item in findings if item.code.startswith("LE1"))
