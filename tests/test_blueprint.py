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
        structural_constraints=["blueprint_before_script"],
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
