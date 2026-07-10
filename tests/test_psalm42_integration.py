import json
from pathlib import Path

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def _psalm42_outputs() -> dict:
    fixture = Path(__file__).resolve().parents[1] / "examples" / "psalm24_mock_outputs.json"
    outputs = json.loads(fixture.read_text())

    outputs["source_agent"] = {
        "source_text": (
            "Psalm 42 source text: As a deer longs for channels of water, so my living self longs for You, God. "
            "My living self thirsts for God, for the living God. My tears have been my food day and night while they say, "
            "Where is your God? I remember going with the crowd to the house of God. Why are you bowed down, my living self? "
            "Wait for God, for I shall yet praise Him. Deep calls to deep at the sound of Your waterfalls; all Your breakers and "
            "waves have passed over me. By day the LORD commands His covenant love, and at night His song is with me."
        ),
        "chapter_verse_count": 11,
    }
    outputs["translator"] = {
        "working_rendering": (
            "As a deer longs for channels of water, so my living self longs for You, God. My living self thirsts for God, "
            "for the living God. My tears have become my food day and night. Why are you bowed down, my living self? "
            "Wait for God, for I shall yet praise Him, the saving presence of my God. Deep calls to deep beneath the sound "
            "of Your waterfalls; all Your breakers and waves have passed over me."
        )
    }
    outputs["chapter_design_mapper"] = {
        "chapter_start": "A thirsty deer embodies the worshiper's longing for the living God.",
        "chapter_end": "The bowed-down self is addressed again with a summons to wait for God.",
        "emotional_movement": "Thirst and remembered worship descend into tears and overwhelming waters, then turn toward disciplined hope.",
        "divine_action": "God remains living, commands covenant love by day, gives song by night, and remains the object of future praise.",
        "physical_vocabulary": ["deer", "water", "thirst", "tears", "food", "waterfalls", "breakers", "waves", "face"],
        "central_theological_claim": "Faithful longing and emotional heaviness can coexist because hope rests in the living God rather than present feeling.",
        "christward_fulfillment": "Jesus gives living water and secures access to the Father by the Spirit without denying the reality of sorrow.",
        "reader_felt_experience": "A worshiper remembers former joy while bodily exhaustion, tears, and distance make God's presence difficult to feel.",
        "chapter_design_summary": "Psalm 42 moves from thirst, to memory, to submersion, to repeated self-address and future praise.",
    }
    outputs["canonist"] = {
        "pathway": "Psalm 42 is not directly cited as prophecy. John 7:37-39 supplies a strong thematic echo: Christ calls the thirsty to Himself and gives the Spirit as living water."
    }
    outputs["theological_risk_agent"] = {
        "risks": [
            {
                "risk_id": "R1",
                "risk_description": "Treat emotional heaviness as proof of unbelief.",
                "why_it_matters": "The psalmist remains faithful while bowed down and distressed.",
                "avoidance_rule": "Distinguish suffering from apostasy and avoid promising immediate emotional relief.",
                "evaluator_check": "Verify that hope does not erase sorrow or impose a diagnosis.",
            },
            {
                "risk_id": "R2",
                "risk_description": "Present Psalm 42 as a direct prediction of Christ.",
                "why_it_matters": "The New Testament does not directly cite the psalm as prophecy.",
                "avoidance_rule": "Name the connection as a thematic echo centered on living water and access to God.",
                "evaluator_check": "Verify that correspondence strength is stated honestly.",
            },
        ]
    }
    outputs["historian_linguist"] = {
        "notes": "The Hebrew nephesh can designate the living self or whole breathing life, not merely an immaterial compartment."
    }
    outputs["commentary_agent"] = {
        "notes": "The refrain does not deny distress; it contests distress as the final interpretation of God."
    }
    outputs["art_director"] = {
        "register": "restrained lament with bodily and hydrological detail",
        "pace": "slow thirst, compressed memory, overwhelming middle, quiet hope",
        "sentence_music": "plain clauses interrupted by brief questions and rests",
        "image_density": "one water system deepened across thirst, tears, waterfalls, and future streams",
        "emotional_color": "honest heaviness without sentimental closure",
        "opening_mode": "sensory scene",
        "poem_tone": "common meter lament turning toward hope",
        "ending_resonance": "water first absent, then promised without being possessed on demand",
        "avoid": ["clinical diagnosis", "forced prophecy", "instant emotional resolution"],
    }
    outputs["creative_divergence_agent"] = {
        "threshold_phrase_candidates": [
            "Thirst can remember where water was.",
            "The soul can thirst without abandoning God.",
            "Hope speaks from inside the roar.",
            "Memory can deepen thirst.",
            "The living God meets a living self.",
        ],
        "introduction_opening_candidates": [
            "A deer lowers its head over an empty channel.",
            "The stones are smooth, but no water moves.",
            "Psalm 42 begins with a body that needs water.",
        ],
        "governing_image_candidates": ["a deer at an empty water channel", "tears eaten as daily food", "waterfalls becoming overwhelming waves"],
        "christology_framing_candidates": ["Christ as giver of living water", "Christ securing access to the Father by the Spirit"],
        "poem_arc_candidates": ["dry channel to roaring deep to promised water", "thirst to submersion to patient praise"],
        "title_candidates": ["Water Beyond the Deer’s Reach", "Inside the Roar", "The Living Self Thirsts"],
        "epigraph_candidates": ["The soul can remember God faithfully while still feeling His absence.", "Hope speaks from inside the roar.", "Memory can deepen thirst."],
    }
    outputs["director"] = {
        "chapter_burden": "The psalm gives faithful language for longing, emotional heaviness, remembered worship, and hope that does not pretend relief has already arrived.",
        "opening_movement": "a thirsty deer reaches an empty channel",
        "closing_movement": "the living self waits for future praise without denying present heaviness",
        "central_thought": "The living God remains trustworthy when the whole living self feels thirst, distance, and inward collapse.",
        "emotional_charge": "thirst sharpened by memory and held within disciplined hope",
        "transcendent_force": "the living God whose covenant love and song remain present inside the roar",
        "selected_threshold_phrase": "The soul can remember God faithfully while still feeling His absence.",
        "threshold_phrase_rationale": "The line preserves both fidelity and phenomenological absence without equating feeling with divine reality.",
        "governing_image": "a deer at an empty water channel",
        "image_lexicon": ["deer", "channel", "water", "thirst", "tears", "deep", "waterfalls", "waves", "song"],
        "image_head_terms": ["deer", "water"],
        "anchor_terms": ["living God", "living self", "thirst", "hope", "Christ"],
        "chapter_specific_terms": ["deer", "living God", "tears as food", "deep calls to deep", "bowed down", "wait for God"],
        "christology_required_echoes": ["living water", "Christ", "Father", "Spirit"],
        "christology_pathway": "A strong thematic echo links the psalm's thirst for the living God with Christ's invitation to the thirsty and His gift of the Spirit as living water.",
        "application_target": "Name sorrow without diagnosis, refuse false certainty, remain in worship, and seek bodily and relational care while waiting for God.",
        "theological_terminus": "communion with the living God secured through Christ and sustained by the Spirit",
        "negative_constraints": ["do not diagnose the psalmist", "do not promise immediate relief", "do not call the psalm direct prophecy"],
        "poem_plan": "common meter moving from dry channel to roaring deep and ending with water received as promise rather than payment",
        "semantic_proof_chain": ["deer", "thirst", "living God", "tears", "remember", "deep", "waves", "song", "bowed down", "wait", "praise"],
    }
    outputs["composer"] = {
        "title": "Water Beyond the Deer’s Reach",
        "epigraph": "The soul can remember God faithfully while still feeling His absence.",
        "focus_bible_verses": "Psalm 42:1-2, 5, 7-8, 11 — As a deer longs for channels of water, so my living self longs for You, God. Why are you bowed down, my living self? Wait for God, for I shall yet praise Him. Deep calls to deep beneath the sound of Your waterfalls. By day the LORD commands His covenant love, and at night His song is with me.",
        "introduction": "A deer reaches an empty water channel and lowers its head. The stones are smooth, but no water moves between them. Dust clings to its mouth. Psalm 42 begins there, with a body that needs what it cannot reach.",
        "reflection": "The Hebrew word nephesh can name the living self, the whole breathing life of a person. The psalmist's memory, body, speech, appetite, and hope thirst together. He remembers the worshiping crowd, but memory sharpens the distance. Tears become food. Then water changes form. What was desired as relief arrives as waterfalls, breakers, and waves. The thirsty man feels submerged. The psalm does not diagnose him. It shows a faithful worshiper bent under loss and distance. He questions his bowed-down self without calling the pain imaginary. His feeling is truthful evidence of suffering, but it is not the whole account of God. By day covenant love remains. At night a song remains. Hope speaks from inside the roar.",
        "christ_fulfillment": "Psalm 42 is not directly cited as a prophecy of Christ. Its strongest New Testament correspondence is a thematic echo. Jesus calls the thirsty to come to Him and drink, and John explains this living water as the Spirit. Christ brings the worshiper to the Father. He does not promise that believers will never feel bowed down. He secures communion with God more firmly than our present ability to feel it.",
        "application": "Name what has bent your inner life without inventing certainty or assigning yourself a diagnosis. Read the psalm aloud. Remain among God's people when former intensity is absent. Tell one trusted person the truth. Eat, rest, and seek competent care when the body carries more than devotion alone can address. Waiting is not payment for relief. It is the posture of one who has nowhere truer to turn.",
        "prayer": "Living God, hear us when our living selves are bowed down. Keep us from mistaking felt absence for abandonment. Give us honest words for sorrow and hope without pretense. Bring us to Christ, the giver of living water, and sustain us by Your Spirit until praise rises again, through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 43 - Send out Your light and truth.",
    }
    outputs["voice_keeper"] = {"approved": True}
    outputs["poet"] = {
        "poem": "As deer seek streams in summer heat,\nMy soul cries out for Thee;\nYet hope still walks on weary feet\nToward waters I shall see.\n\nDeep answers deep beneath the roar,\nThe floods pass over me;\nYet through the night I praise once more\nThe God who carries me.\n\nWhen thirst has dried my failing tongue,\nChrist calls the thirsty near;\nHe leads me where clear waters run,\nAnd hope outlives my fear."
    }
    outputs["beauty_pass_agent"] = {
        "lingering_lines": ["Psalm 42 begins there.", "Hope speaks from inside the roar."],
        "strongest_turn": "Desired water becomes overwhelming water before hope speaks from within it.",
        "weakest_artistic_moment": "",
        "mechanical_residue": [],
        "beauty_score": 9,
        "required_beauty_revisions": [],
    }
    outputs["evaluator"] = {
        "textual_fidelity": 9,
        "theological_accuracy": 9,
        "christology_from_chapter_logic": 9,
        "chapter_design_fidelity": 9,
        "emotional_charged_phrase": 9,
        "introduction_strength": 9,
        "ancient_image_discipline": 9,
        "register": 9,
        "read_aloud_quality": 9,
        "application_concreteness": 9,
        "prayer": 9,
        "poem_form": 9,
        "poetic_vitality": 9,
        "artful_design": 9,
        "artifact_integrity": 9,
        "fault_target": "none",
        "notes": "Psalm 42 preserves textual restraint, psychological plausibility, and an honestly labeled thematic Christological echo.",
    }
    outputs["contradiction_editor"] = {
        "verdict": "Pass",
        "major_conflicts": [],
        "minor_conflicts": [],
        "theological_risks": [],
        "literary_risks": [],
        "harness_risks": [],
        "required_revisions": [],
        "notes": "No conflicts.",
    }
    outputs["editorial_smoother"] = {"prose": {}}
    return outputs


def test_psalm42_runs_full_v64_pipeline() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 42"), MockAgentAdapter(_psalm42_outputs()))

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert State.STORY_PLAN_BLUEPRINT in ctx.trace
    assert State.BLUEPRINT_VALIDATION in ctx.trace
    assert ctx.trace.index(State.STORY_PLAN_BLUEPRINT) < ctx.trace.index(State.COMPOSE_PROSE)
    assert ctx.trace.index(State.BLUEPRINT_VALIDATION) < ctx.trace.index(State.COMPOSE_PROSE)
    assert "thematic echo" in ctx.prose["christ_fulfillment"].lower()
    assert "does not diagnose" in ctx.prose["reflection"].lower()
    assert "Water Beyond the Deer" in ctx.artifact
