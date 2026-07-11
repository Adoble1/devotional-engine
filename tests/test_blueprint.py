from devotional_engine.blueprint import StoryPlanBlueprint, approve_blueprint, validate_script_alignment


def valid_blueprint():
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
        structural_constraints=[
            "blueprint_before_script",
            "emotion_earned_by_physical_fact",
            "no_unwarranted_deprivation",
            "global_canonical_view",
            "apostolic_priority",
            "mystery_to_revelation",
            "discovery_before_explanation",
            "originality_check",
        ],
        canonical_view={
            "historical_meaning": "David praises the Lord as deliverer.",
            "canonical_trajectory": "The anointed king pattern moves toward Christ.",
            "apostolic_interpretation": "No explicit quotation controls this fixture.",
            "christological_fulfillment": "Christ is the greater anointed King and Deliverer.",
            "governing_mystery": "How does the king's deliverance serve the covenant people?",
            "governing_revelation": "The greater King delivers His people fully.",
        },
        originality_rules=[
            "protect_scripture_and_standard_doctrine",
            "reject_distinctive_unattributed_overlap",
            "reject_living_author_imitation",
            "flag_generic_ai_cadence",
            "prefer_discovery_before_explanation",
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


def test_blueprint_rejects_missing_earned_emotion_constraint():
    blueprint = valid_blueprint()
    blueprint.structural_constraints.remove("emotion_earned_by_physical_fact")
    findings = approve_blueprint(blueprint)
    assert blueprint.approved is False
    assert any(item.code == "B09" and "emotion_earned_by_physical_fact" in item.field for item in findings)


def test_blueprint_rejects_unwarranted_deprivation_constraint_gap():
    blueprint = valid_blueprint()
    blueprint.structural_constraints.remove("no_unwarranted_deprivation")
    findings = approve_blueprint(blueprint)
    assert blueprint.approved is False
    assert any(item.code == "B09" and "no_unwarranted_deprivation" in item.field for item in findings)


def test_blueprint_rejects_incomplete_global_canonical_view():
    blueprint = valid_blueprint()
    blueprint.canonical_view["apostolic_interpretation"] = ""
    findings = approve_blueprint(blueprint)
    assert blueprint.approved is False
    assert any(item.code == "B10" and "apostolic_interpretation" in item.field for item in findings)


def test_blueprint_rejects_missing_originality_rule():
    blueprint = valid_blueprint()
    blueprint.originality_rules.remove("reject_distinctive_unattributed_overlap")
    findings = approve_blueprint(blueprint)
    assert blueprint.approved is False
    assert any(item.code == "B11" and "reject_distinctive_unattributed_overlap" in item.field for item in findings)


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
