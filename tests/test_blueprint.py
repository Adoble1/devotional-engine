from devotional_engine.blueprint import StoryPlanBlueprint, approve_blueprint, validate_script_alignment
from devotional_engine.profiles import CORE_LAW_IDS, compile_rule_ids


def valid_blueprint():
    canonical_view = {
        "historical_meaning": "David praises the Lord as deliverer.",
        "canonical_trajectory": "The anointed king pattern moves toward Christ.",
        "apostolic_interpretation": "No explicit quotation controls this fixture.",
        "christological_fulfillment": "Christ is the greater anointed King and Deliverer.",
        "governing_mystery": "How does the king's deliverance serve the covenant people?",
        "governing_revelation": "The greater King delivers His people fully.",
    }
    return StoryPlanBlueprint(
        chapter_ref="Psalm 18",
        source_state={"source_text": "source", "working_rendering": "rendering"},
        chapter_design_map={"central_theological_claim": "The Lord delivers."},
        section_purposes={
            "introduction": "enter distress",
            "reflection": "trace deliverance",
            "christ_fulfillment": "show the greater Deliverer",
            "application": "trust the Lord",
            "prayer": "ask for steadfast faith",
            "poem": "move from distress to praise",
        },
        theological_logic=["The Lord delivers.", "Faith answers deliverance with praise."],
        theological_risk_register=[],
        emotional_arc=["distress", "rescue", "praise"],
        image_continuity={"governing_image": "rock", "image_lexicon": ["fortress"], "image_head_terms": ["rock"]},
        christology_pathway=["the anointed king", "Christ the greater King"],
        application_target="trust the Lord",
        prayer_arc=["need", "petition", "praise"],
        poem_arc=["distress", "deliverance", "praise"],
        voice_constraints=["no sentimentality"],
        structural_constraints=["blueprint_before_script", "source_fields_immutable", "bounded_component_repairs"],
        governing_laws=list(CORE_LAW_IDS),
        profile_rules=list(compile_rule_ids("devotional")),
        planning_maps={
            "truth_map": {"text_establishes": ["deliverance"]},
            "revelation_map": {"entry": "distress", "final_recognition": "praise"},
            "reader_transformation_map": {"from": "fear", "to": "trust"},
            "art_direction": {"register": "restrained praise"},
            "canonical_map": canonical_view,
            "theological_risk_map": {"status": "no unresolved high risk"},
        },
        canonical_view=canonical_view,
        originality_rules=[
            "protect_scripture_and_standard_doctrine",
            "reject_distinctive_unattributed_overlap",
            "reject_living_author_imitation",
            "flag_generic_ai_cadence",
        ],
    )


def test_blueprint_approval_is_deterministic():
    blueprint = valid_blueprint()
    assert approve_blueprint(blueprint) == []
    assert blueprint.approved is True


def test_blueprint_rejects_missing_section_purpose():
    blueprint = valid_blueprint()
    blueprint.section_purposes["application"] = ""
    findings = approve_blueprint(blueprint)
    assert blueprint.approved is False
    assert any(item.field == "section_purposes.application" for item in findings)


def test_blueprint_rejects_missing_core_law():
    blueprint = valid_blueprint()
    blueprint.governing_laws.remove("source_truth")
    findings = approve_blueprint(blueprint)
    assert any(item.code == "B10" and "source_truth" in item.field for item in findings)


def test_blueprint_rejects_missing_mode_specific_rule():
    blueprint = valid_blueprint()
    blueprint.profile_rules.remove("apostolic_priority")
    findings = approve_blueprint(blueprint)
    assert any(item.code == "B11" and "apostolic_priority" in item.field for item in findings)


def test_blueprint_rejects_missing_planning_map():
    blueprint = valid_blueprint()
    del blueprint.planning_maps["reader_transformation_map"]
    findings = approve_blueprint(blueprint)
    assert any(item.code == "B12" and "reader_transformation_map" in item.field for item in findings)


def test_script_alignment_returns_structured_field_findings():
    blueprint = valid_blueprint()
    approve_blueprint(blueprint)
    findings = validate_script_alignment(
        blueprint,
        {
            "application": "trust the Lord in the dark",
            "christ_fulfillment": "Christ the greater King stands as our rock",
            "reflection": "The rock does not move.",
        },
        "Upon the rock I sing.",
    )
    assert findings == []
