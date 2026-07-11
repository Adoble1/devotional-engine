import json
from pathlib import Path

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def _psalm45_outputs() -> dict:
    path = Path(__file__).resolve().parents[1] / "examples" / "psalm24_mock_outputs.json"
    outputs = json.loads(path.read_text())
    outputs["source_agent"] = {"source_text": "Psalm 45: My heart overflows concerning the king. Grace is poured upon your lips. Your throne, O God, is forever and ever. God, your God, has anointed you with the oil of gladness. The queen stands at your right hand in gold.", "chapter_verse_count": 17}
    outputs["translator"] = {"working_rendering": "My heart overflows with a good word concerning the king. Grace is poured upon your lips. Your throne, O God, is forever and ever. You love righteousness and hate wickedness; therefore God, your God, has anointed you with the oil of joy."}
    outputs["chapter_design_mapper"] = {
        "chapter_start": "A court poet's heart overflows as he addresses a royal bridegroom.",
        "chapter_end": "The bride enters the king's enduring praise.",
        "emotional_movement": "Overflowing admiration moves through royal majesty into covenantal union and public joy.",
        "divine_action": "God establishes the king's throne, anoints him, and gathers a bride into royal fellowship.",
        "physical_vocabulary": ["heart", "tongue", "lips", "sword", "throne", "scepter", "oil", "robes", "palace", "gold"],
        "central_theological_claim": "The righteous royal bridegroom bears a throne beyond ordinary kingship and gathers a bride into his enduring kingdom.",
        "christward_fulfillment": "Hebrews 1 explicitly applies Psalm 45:6-7 to the Son, revealing Christ whose throne is forever.",
        "reader_felt_experience": "A listener moves from admiration of royal splendor into allegiance to the king.",
        "chapter_design_summary": "Psalm 45 celebrates a royal wedding while its language exceeds the merely human king and opens toward the eternal Son and His bride.",
    }
    outputs["canonist"] = {"pathway": "Hebrews 1:8-9 explicitly quotes Psalm 45:6-7 and addresses the words to the Son. Ephesians 5 and Revelation 19 develop the bridegroom-and-bride pattern."}
    outputs["theological_risk_agent"] = {"risks": [
        {"risk_id": "R1", "risk_description": "Erase the historical royal wedding.", "why_it_matters": "The psalm first functions as a royal wedding song in Israel.", "avoidance_rule": "Preserve the historical king and bride before following Hebrews to the Son.", "evaluator_check": "Verify continuity and escalation."},
        {"risk_id": "R2", "risk_description": "Reduce the bride imagery to private romance.", "why_it_matters": "The canonical trajectory concerns the covenant people.", "avoidance_rule": "Keep ecclesial application primary.", "evaluator_check": "Verify Christ and His people remain central."},
    ]}
    outputs["historian_linguist"] = {"notes": "The psalm is a royal wedding song, and Hebrews 1 explicitly applies its divine throne language to the Son."}
    outputs["commentary_agent"] = {"notes": "The language honors an Israelite king while straining beyond him toward an everlasting righteous throne."}
    outputs["art_director"] = {
        "register": "royal radiance with covenantal gravity", "pace": "overflow, procession, throne, bridal summons",
        "sentence_music": "ceremonial lines interrupted by throne declarations", "image_density": "lips, sword, throne, scepter, oil, robes, gold",
        "emotional_color": "wonder deepening into allegiance", "opening_mode": "embodied overflow", "poem_tone": "common meter royal hymn",
        "ending_resonance": "the bride crossing toward the eternal King", "avoid": ["forced allegory", "generic romance", "living-author imitation"],
    }
    outputs["creative_divergence_agent"] = {
        "threshold_phrase_candidates": ["The song exceeds the wedding.", "The throne outlives the palace.", "The bridegroom is more than a king.", "Grace speaks before the sword moves.", "Joy rests upon a righteous throne."],
        "introduction_opening_candidates": ["The poet cannot keep the song inside his chest.", "Grace is heard before the sword appears.", "The wedding song reaches a throne no dynasty can hold."],
        "governing_image_candidates": ["oil of joy on the king's robes", "a throne standing beyond the palace", "the bride crossing toward the king"],
        "christology_framing_candidates": ["Hebrews addressing the psalm to the Son", "the royal bridegroom gathering His covenant bride"],
        "poem_arc_candidates": ["overflowing heart to eternal throne to bride", "gracious lips to righteous scepter to wedding joy"],
        "title_candidates": ["The Throne Beyond the Wedding", "The King Above His Companions", "When the Song Reaches the Son"],
        "epigraph_candidates": ["The song exceeds the wedding.", "The throne outlives the palace.", "The bridegroom is more than a king."],
    }
    outputs["director"] = {
        "chapter_burden": "The royal wedding is historically real, yet Hebrews identifies its everlasting throne language with the Son.",
        "opening_movement": "the poet's body strains with a song too full to remain unspoken",
        "closing_movement": "the bride crosses from former allegiance into the joy of the everlasting King",
        "central_thought": "A historical wedding becomes a canonical mystery when the king is addressed with an eternal divine throne, and Hebrews reveals the fullest referent as the Son.",
        "emotional_charge": "wonder becoming allegiance", "transcendent_force": "the Son whose righteous throne endures forever",
        "selected_threshold_phrase": "The song exceeds the wedding.", "threshold_phrase_rationale": "It preserves the ceremony while signaling canonical escalation.",
        "governing_image": "a throne standing beyond the palace", "image_lexicon": ["heart", "lips", "sword", "throne", "scepter", "oil", "palace", "bride"],
        "image_head_terms": ["throne", "palace"], "anchor_terms": ["king", "throne", "righteousness", "Son", "bride"],
        "chapter_specific_terms": ["grace upon your lips", "oil of gladness", "your throne O God"],
        "christology_required_echoes": ["Hebrews", "Son", "throne", "forever", "bride"],
        "christology_pathway": "Hebrews 1 explicitly quotes Psalm 45:6-7 and addresses the words to the Son; the wedding moves from mystery to revelation in Christ the eternal Bridegroom.",
        "application_target": "Receive Christ's righteous rule, leave rival loyalties, and enter the worshiping life of His covenant people.",
        "theological_terminus": "the eternal Son reigning in righteousness and gathering His bride into joy",
        "negative_constraints": ["preserve the historical wedding", "explicit quotation outranks thematic echoes", "do not imitate a living author", "discover before explaining"],
        "poem_plan": "common meter moving from overflowing heart to eternal throne and the bride entering joy",
        "semantic_proof_chain": ["heart overflows", "grace", "throne", "God", "anointed", "oil of joy", "bride", "king"],
        "historical_meaning": "A royal wedding song honoring an Israelite king and bride.",
        "canonical_trajectory": "The everlasting throne and bridegroom pattern move through Hebrews 1, Ephesians 5, and Revelation 19.",
        "apostolic_interpretation": "Hebrews 1:8-9 explicitly quotes Psalm 45:6-7 and says these words are spoken of the Son.",
        "governing_mystery": "How can an Israelite king be addressed with a divine everlasting throne?",
        "governing_revelation": "The New Testament reveals the fullest referent as the Son, the eternal righteous King and Bridegroom.",
    }
    outputs["composer"] = {
        "title": "The Throne Beyond the Wedding", "epigraph": "The song exceeds the wedding.",
        "focus_bible_verses": "Psalm 45:1-7 — My heart overflows. Grace is poured upon your lips. Your throne, O God, is forever and ever.",
        "introduction": "The song exceeds the wedding. The poet cannot keep it inside his chest. His heart overflows; his tongue moves like a ready stylus. The procession reaches the throne, and the language rises beyond any palace built by men.",
        "reflection": "Psalm 45 first belongs to a royal wedding in Israel. Yet the poem says more than court ceremony can contain: Your throne, O God, is forever and ever. The mystery is preserved until the canon reveals the King to whom this language finally belongs.",
        "christ_fulfillment": "Hebrews does not merely echo Psalm 45. It quotes verses 6 and 7 and introduces them with the words, 'Of the Son he says.' The apostolic interpretation governs the fulfillment and reveals the mystery. Jesus Christ is the Son whose throne is forever and whose scepter is righteousness. Ephesians and Revelation widen the bridal pattern: the righteous King prepares a people as His bride.",
        "application": "Receive Christ's righteous rule, leave rival loyalties, and enter the worshiping life of His covenant people. Let His gracious word govern your speech and His righteous scepter correct your loves.",
        "prayer": "Father, open our ears to the song You have spoken concerning Your Son. Free us from rival loyalties and bring us gladly under His righteous rule. Gather us with Your people as the bride of the everlasting King, through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 46 - The city that does not fall because God is within her.",
    }
    outputs["voice_keeper"] = {"approved": True}
    outputs["poet"] = {"poem": "My heart pours forth a royal song,\nThe King stands clothed in light;\nHis throne remains when halls are gone,\nHis scepter judges right.\n\nGrace rests upon His holy lips,\nJoy crowns His righteous reign;\nThe bride leaves every lesser house\nTo bear His glorious name.\n\nThe apostle names the hidden King:\nThe Son forever crowned;\nIn Him the wedding mystery\nHas found its deepest sound."}
    outputs["beauty_pass_agent"] = {"lingering_lines": ["The song exceeds the wedding."], "strongest_turn": "Hebrews names the eternal Son.", "weakest_artistic_moment": "", "mechanical_residue": [], "beauty_score": 9, "required_beauty_revisions": []}
    outputs["evaluator"] = {key: 9 for key in ["textual_fidelity", "theological_accuracy", "christology_from_chapter_logic", "chapter_design_fidelity", "emotional_charged_phrase", "introduction_strength", "ancient_image_discipline", "register", "read_aloud_quality", "application_concreteness", "prayer", "poem_form", "poetic_vitality", "artful_design", "artifact_integrity"]}
    outputs["evaluator"].update({"fault_target": "none", "notes": "Psalm 45 preserves the wedding, gives Hebrews apostolic priority, and avoids derivative phrasing."})
    outputs["contradiction_editor"] = {"verdict": "Pass", "major_conflicts": [], "minor_conflicts": [], "theological_risks": [], "literary_risks": [], "harness_risks": [], "required_revisions": [], "notes": "No conflicts."}
    outputs["editorial_smoother"] = {"prose": {}}
    return outputs


def test_psalm45_runs_global_canonical_pipeline() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 45"), MockAgentAdapter(_psalm45_outputs()))
    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert ctx.trace.index(State.STORY_PLAN_BLUEPRINT) < ctx.trace.index(State.COMPOSE_PROSE)
    assert "Hebrews 1:8-9" in ctx.blueprint.canonical_view["apostolic_interpretation"]
    assert "mystery" in ctx.prose["christ_fulfillment"].lower()
    assert "Of the Son" in ctx.prose["christ_fulfillment"]
    assert "The Throne Beyond the Wedding" in ctx.artifact
    assert "reject_distinctive_unattributed_overlap" in ctx.blueprint.originality_rules
