from devotional_engine.profiles import CORE_LAW_IDS, WritingMode, compile_rule_ids, get_profile


def test_profiles_share_six_core_laws_but_keep_domain_rules_separate():
    devotional = compile_rule_ids(WritingMode.DEVOTIONAL)
    fiction = compile_rule_ids(WritingMode.FICTION)
    nonfiction = compile_rule_ids(WritingMode.NONFICTION)

    assert devotional[: len(CORE_LAW_IDS)] == CORE_LAW_IDS
    assert fiction[: len(CORE_LAW_IDS)] == CORE_LAW_IDS
    assert nonfiction[: len(CORE_LAW_IDS)] == CORE_LAW_IDS
    assert "apostolic_priority" in devotional
    assert "apostolic_priority" not in fiction
    assert "claim_evidence_traceability" in nonfiction
    assert "point_of_view_consistency" not in devotional


def test_legacy_rules_collapse_into_governing_laws_instead_of_accumulating():
    compiled = compile_rule_ids(
        "devotional",
        [
            "emotion_earned_by_physical_fact",
            "no_unwarranted_deprivation",
            "discovery_before_explanation",
            "one_passage_only_note",
        ],
    )
    assert compiled.count("human_truth") == 1
    assert compiled.count("source_truth") == 1
    assert compiled.count("revelatory_pacing") == 1
    assert "one_passage_only_note" not in compiled


def test_profile_required_maps_are_mode_specific():
    assert "canonical_map" in get_profile("devotional").required_planning_maps
    assert "world_state" in get_profile("fiction").required_planning_maps
    assert "claim_evidence_map" in get_profile("nonfiction").required_planning_maps
