from devotional_engine import EngineConfig, EngineContext
from devotional_engine.coherence import (
    audit_director_output,
    audit_prose,
    dedupe_instructions,
    prepare_director_output,
)


def _context() -> EngineContext:
    ctx = EngineContext(chapter_ref="Psalm 50")
    ctx.chapter_design_map = {
        "central_theological_claim": "True worship joins gratitude and obedience.",
        "reader_felt_experience": "Religious activity can conceal resistance to correction.",
        "divine_action": "God summons His people, exposes false worship, and promises salvation.",
        "christward_fulfillment": "Christ offers Himself once for all and forms truthful worshipers.",
    }
    ctx.art_direction = {
        "avoid": [
            "avoid anti-sacrifice language",
            "avoid anti-sacrifice language",
            "do not let ritual become the governing subject",
        ]
    }
    return ctx


def _director_output() -> dict:
    return {
        "chapter_burden": "Expose worship separated from life and recover thanksgiving joined to obedience.",
        "opening_movement": "God summons His covenant people and examines their worship.",
        "closing_movement": "The grateful worshiper receives salvation and orders the way rightly.",
        "central_thought": "True worship joins gratitude and obedience.",
        "emotional_charge": "The life behind the offering is brought into the light.",
        "transcendent_force": "God speaks as owner, judge, and deliverer.",
        "selected_threshold_phrase": "God examines the offering.",
        "threshold_phrase_rationale": "The phrase opens the covenant lawsuit without solving it too early.",
        "governing_image": "God examining the life behind the offering",
        "image_lexicon": ["altar", "offering", "thanksgiving", "altar"],
        "image_head_terms": ["offering", "thanksgiving"],
        "anchor_terms": ["sacrifice", "thanksgiving", "obedience", "thanksgiving"],
        "chapter_specific_terms": ["cattle on a thousand hills", "call upon Me"],
        "christology_required_echoes": ["Christ", "once for all", "obedience"],
        "christology_pathway": "Christ provides the final sacrifice and creates worshipers in spirit and truth.",
        "application_target": "Let the life agree with the worship offered.",
        "theological_terminus": "Grateful obedience flowing from Christ's finished sacrifice.",
        "negative_constraints": [
            "do not reject sacrifice as though God never commanded it",
            "do not reject sacrifice as though God never commanded it",
        ],
        "poem_plan": "Two stanzas moving from divine ownership to grateful obedience in Christ.",
        "semantic_proof_chain": ["God summons", "God owns", "God calls", "God saves"],
        "supporting_elements": ["the cattle and offerings expose that God lacks nothing"],
        "textual_hinge": "Offer to God a sacrifice of thanksgiving.",
        "divine_answer": "God calls for thanksgiving, trust, and an ordered way.",
    }


def test_instruction_compilation_deduplicates_without_promoting_new_rules():
    prepared = prepare_director_output(_context(), _director_output())

    assert prepared["image_lexicon"] == ["altar", "offering", "thanksgiving"]
    assert prepared["negative_constraints"] == [
        "do not reject sacrifice as though God never commanded it"
    ]
    assert len(prepared["effective_constraints"]) == 3
    assert prepared["passage_center_map"]["governing_subject"] == (
        "True worship joins gratitude and obedience."
    )
    assert audit_director_output(_context(), prepared) == []


def test_conflicting_directives_fail_the_coherence_contract():
    ctx = _context()
    output = _director_output()
    output["negative_constraints"] = [
        "avoid invented weather",
        "include invented weather",
    ]

    prepared = prepare_director_output(ctx, output)
    findings = audit_director_output(ctx, prepared)

    assert any(item.code == "C04" for item in findings)


def test_duplicate_section_burdens_are_detected_before_composition():
    ctx = _context()
    output = _director_output()
    output["application_target"] = output["central_thought"]

    prepared = prepare_director_output(ctx, output)
    findings = audit_director_output(ctx, prepared)

    assert any(item.code == "C03" for item in findings)


def test_title_and_opening_distinction_is_a_local_editorial_option():
    ctx = _context()
    ctx.brief = {"passage_center_map": prepare_director_output(ctx, _director_output())["passage_center_map"]}
    prose = {
        "title": "Thanksgiving Over Ritual",
        "epigraph": "God examines the life behind the offering.",
        "introduction": "Thanksgiving Over Ritual. God summons His covenant people.",
        "reflection": "True worship joins gratitude and obedience before the God who owns all things.",
        "christ_fulfillment": "Christ offers Himself once for all.",
        "application": "Let the life agree with the worship offered.",
        "prayer": "Father, teach us grateful obedience through Jesus Christ our Lord. Amen.",
    }

    default_findings = audit_prose(ctx, prose, EngineConfig())
    local_findings = audit_prose(
        ctx,
        prose,
        EngineConfig(enforce_title_opening_distinction=True),
    )

    assert not any(item.code == "C10" for item in default_findings)
    assert any(item.code == "C10" and item.severity == "error" for item in local_findings)


def test_repetition_and_theme_displacement_are_warnings_not_global_style_rules():
    ctx = _context()
    ctx.brief = {
        "passage_center_map": {
            "governing_terms": ["worship", "obedience", "thanksgiving"],
            "supporting_terms": ["altar", "sacrifice"],
        }
    }
    repeated = "The altar cannot turn resistance into faithful worship before God."
    prose = {
        "title": "Thanksgiving Over Ritual",
        "epigraph": "God examines the life behind the offering.",
        "introduction": "God summons His covenant people.",
        "reflection": (
            f"{repeated} The altar and sacrifice remain visible. "
            "The altar receives sacrifice, and sacrifice returns to the altar."
        ),
        "christ_fulfillment": repeated,
        "application": "Receive correction and walk in obedience.",
        "prayer": "Father, form truthful worship in us through Jesus Christ our Lord. Amen.",
    }

    findings = audit_prose(ctx, prose, EngineConfig())

    assert any(item.code == "C12" and item.severity == "warning" for item in findings)
    assert any(item.code == "C14" and item.severity == "warning" for item in findings)


def test_dedupe_instructions_preserves_first_wording_and_order():
    assert dedupe_instructions(["Keep the image concrete.", "keep the image concrete", "Move forward."]) == [
        "Keep the image concrete.",
        "Move forward.",
    ]
