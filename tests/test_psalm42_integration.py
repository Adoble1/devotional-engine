import json
from pathlib import Path

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def _psalm42_outputs() -> dict:
    path = Path(__file__).resolve().parents[1] / "examples" / "psalm24_mock_outputs.json"
    o = json.loads(path.read_text())

    o["source_agent"] = {
        "source_text": "Psalm 42: As a deer longs for water, so my living self longs for You, God. My living self thirsts for the living God. My tears are my food day and night. Why are you bowed down, my living self? Wait for God, for I shall yet praise Him. Deep calls to deep beneath Your waterfalls. By day the LORD commands covenant love, and at night His song is with me.",
        "chapter_verse_count": 11,
    }
    o["translator"] = {"working_rendering": "As a deer longs for channels of water, so my living self longs for You, God. My living self thirsts for the living God. My tears have become my food day and night. Why are you bowed down, my living self? Wait for God, for I shall yet praise Him. Deep calls to deep beneath the sound of Your waterfalls."}
    o["chapter_design_mapper"] = {
        "chapter_start": "A panting deer embodies urgent longing for the living God.",
        "chapter_end": "The bowed-down living self waits for future praise.",
        "emotional_movement": "Bodily thirst and memory descend into tears and overwhelming waters, then turn toward disciplined hope.",
        "divine_action": "God remains living, commands covenant love, gives song by night, and remains the object of future praise.",
        "physical_vocabulary": ["deer", "water", "panting", "thirst", "tears", "food", "waterfalls", "waves", "face"],
        "central_theological_claim": "Faithful longing and emotional heaviness can coexist because hope rests in the living God rather than present feeling.",
        "christward_fulfillment": "Jesus gives living water and secures access to the Father by the Spirit without denying sorrow.",
        "reader_felt_experience": "A worshiper remembers former joy while tears, distance, and bodily exhaustion make God's presence difficult to feel.",
        "chapter_design_summary": "The psalm moves from thirst to memory, submersion, self-address, and future praise.",
    }
    o["canonist"] = {"pathway": "Psalm 42 is not directly cited as prophecy. John 7:37-39 supplies a strong thematic echo through Christ's invitation to the thirsty and the gift of the Spirit as living water."}
    o["theological_risk_agent"] = {"risks": [
        {"risk_id": "R1", "risk_description": "Treat heaviness as proof of unbelief.", "why_it_matters": "The psalmist remains faithful while bowed down.", "avoidance_rule": "Do not diagnose or promise immediate relief.", "evaluator_check": "Hope must not erase sorrow."},
        {"risk_id": "R2", "risk_description": "Invent a dry stream or unavailable water.", "why_it_matters": "The text establishes intense desire, not deprivation of access.", "avoidance_rule": "Let panting, drinking, and bodily urgency earn the longing.", "evaluator_check": "No unwarranted drought, pursuit, or absence."},
    ]}
    o["historian_linguist"] = {"notes": "The Hebrew nephesh can designate the living self or whole breathing life."}
    o["commentary_agent"] = {"notes": "The refrain contests distress as the final interpretation of God without denying the distress."}
    o["art_director"] = {
        "register": "restrained lament with bodily and water detail",
        "pace": "urgent thirst, compressed memory, overwhelming middle, quiet hope",
        "sentence_music": "plain clauses with brief questions and rests",
        "image_density": "one water system across thirst, drinking, tears, waterfalls, and future praise",
        "emotional_color": "honest heaviness without sentimental closure",
        "opening_mode": "threshold phrase followed by embodied action",
        "poem_tone": "common meter lament turning toward hope",
        "ending_resonance": "longing remains directed toward the living God",
        "avoid": ["clinical diagnosis", "forced prophecy", "dry-stream invention", "instant relief"],
    }
    o["creative_divergence_agent"] = {
        "threshold_phrase_candidates": ["Hope speaks from inside the roar.", "Memory can deepen thirst.", "The living self still waits."],
        "introduction_opening_candidates": ["The deer comes panting toward the stream.", "Its flanks pull hard beneath the hide.", "It drinks, lifts to breathe, and bends again."],
        "governing_image_candidates": ["a panting deer drinking at the stream", "tears eaten as food", "waterfalls becoming overwhelming waves"],
        "christology_framing_candidates": ["Christ as giver of living water", "Christ securing access to the Father by the Spirit"],
        "poem_arc_candidates": ["panting thirst to roaring deep to patient praise"],
        "title_candidates": ["The Deer at the Stream", "Inside the Roar"],
        "epigraph_candidates": ["Hope speaks from inside the roar.", "Memory can deepen thirst."],
    }
    o["director"] = {
        "chapter_burden": "The psalm gives faithful language for longing, heaviness, remembered worship, and hope without pretending relief has arrived.",
        "opening_movement": "a panting deer reaches the stream and drinks with bodily urgency",
        "closing_movement": "the living self waits for future praise",
        "central_thought": "The panting deer at the stream becomes the bowed-down living self whose urgent longing remains directed toward the living God and future praise.",
        "emotional_charge": "thirst earned through breath and bodily urgency, then sharpened by memory",
        "transcendent_force": "the living God whose covenant love and song remain present inside the roar",
        "selected_threshold_phrase": "Hope speaks from inside the roar.",
        "threshold_phrase_rationale": "The line states the psalm's turn without denying distress.",
        "governing_image": "a panting deer drinking at the stream",
        "image_lexicon": ["deer", "stream", "water", "panting", "drink", "breath", "thirst", "tears", "deep", "waterfalls", "waves", "song"],
        "image_head_terms": ["deer", "water"],
        "anchor_terms": ["living God", "living self", "thirst", "hope", "Christ"],
        "chapter_specific_terms": ["deer", "living God", "tears as food", "deep calls to deep", "bowed down", "wait for God"],
        "christology_required_echoes": ["living water", "Christ", "Father", "Spirit"],
        "christology_pathway": "A strong thematic echo links thirst for the living God with Christ's invitation to the thirsty and His gift of the Spirit as living water.",
        "application_target": "Name sorrow without diagnosis, remain in worship, and seek bodily and relational care while waiting for God.",
        "theological_terminus": "communion with the living God secured through Christ and sustained by the Spirit",
        "negative_constraints": ["emotion_earned_by_physical_fact", "no_unwarranted_deprivation", "do not diagnose", "do not promise immediate relief", "do not call the psalm direct prophecy"],
        "poem_plan": "common meter moving from panting thirst to roaring deep and future praise",
        "semantic_proof_chain": ["deer", "thirst", "living God", "tears", "deep", "waves", "song", "bowed down", "wait", "praise"],
    }
    o["composer"] = {
        "title": "The Deer at the Stream",
        "epigraph": "Hope speaks from inside the roar.",
        "focus_bible_verses": "Psalm 42:1-2, 5, 7-8, 11 — As a deer longs for channels of water, so my living self longs for You, God. Why are you bowed down, my living self? Wait for God, for I shall yet praise Him. Deep calls to deep beneath Your waterfalls.",
        "introduction": "Hope speaks from inside the roar.\n\nThe deer comes panting toward the stream. Its flanks pull hard beneath the hide. It lowers its head and drinks fast, lifting only long enough to breathe before bending again to the water. Psalm 42 begins with that kind of longing.",
        "reflection": "The Hebrew word nephesh can name the living self, the whole breathing life of a person. Memory, body, speech, appetite, and hope thirst together. Tears become food. Then water changes form. What was desired as relief arrives as waterfalls and waves. The thirsty man feels submerged. The psalm does not diagnose him. It shows a faithful worshiper bent under loss and distance. His feeling is truthful evidence of suffering, but it is not the whole account of God. By day covenant love remains. At night a song remains. Hope speaks from inside the roar.",
        "christ_fulfillment": "Psalm 42 is not directly cited as a prophecy of Christ. Its strongest New Testament correspondence is a thematic echo. Jesus calls the thirsty to come to Him and drink, and John explains this living water as the Spirit. Christ brings the worshiper to the Father. He secures communion with God more firmly than our present ability to feel it.",
        "application": "Name sorrow without diagnosis, remain in worship, and seek bodily and relational care while waiting for God. Read the psalm aloud. Tell one trusted person the truth. Eat, rest, and seek competent care when the body carries more than devotion alone can address. Waiting is not payment for relief.",
        "prayer": "Father, who hears us when our living selves are bowed down, keep us from mistaking felt absence for abandonment. Give us honest words for sorrow and hope without pretense. Bring us to Christ, the giver of living water, and sustain us by Your Spirit until praise rises again, through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 43 - Send out Your light and truth.",
    }
    o["voice_keeper"] = {"approved": True}
    o["poet"] = {"poem": "As deer drink deep with urgent breath,\nMy soul cries out for Thee;\nYet hope still walks on weary feet\nToward praise I shall yet see.\n\nDeep answers deep beneath the roar,\nThe floods pass over me;\nYet through the night I praise once more\nThe God who carries me.\n\nWhen thirst has seized my living frame,\nChrist calls the thirsty near;\nHe gives the Spirit's living stream,\nAnd hope outlives my fear."}
    o["beauty_pass_agent"] = {"lingering_lines": ["The deer comes panting toward the stream.", "Hope speaks from inside the roar."], "strongest_turn": "Bodily thirst becomes spiritual longing before desired water becomes overwhelming water.", "weakest_artistic_moment": "", "mechanical_residue": [], "beauty_score": 9, "required_beauty_revisions": []}
    o["evaluator"] = {
        "textual_fidelity": 9, "theological_accuracy": 9, "christology_from_chapter_logic": 9,
        "chapter_design_fidelity": 9, "emotional_charged_phrase": 9, "introduction_strength": 9,
        "ancient_image_discipline": 9, "register": 9, "read_aloud_quality": 9,
        "application_concreteness": 9, "prayer": 9, "poem_form": 9, "poetic_vitality": 9,
        "artful_design": 9, "artifact_integrity": 9, "fault_target": "none",
        "notes": "Psalm 42 earns emotion through physical action, avoids invented deprivation, and preserves a thematic Christological echo.",
    }
    o["contradiction_editor"] = {"verdict": "Pass", "major_conflicts": [], "minor_conflicts": [], "theological_risks": [], "literary_risks": [], "harness_risks": [], "required_revisions": [], "notes": "No conflicts."}
    o["editorial_smoother"] = {"prose": {}}
    return o


def test_psalm42_runs_full_v64_pipeline_separately() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 42"), MockAgentAdapter(_psalm42_outputs()))
    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert ctx.trace.index(State.STORY_PLAN_BLUEPRINT) < ctx.trace.index(State.COMPOSE_PROSE)
    assert ctx.trace.index(State.BLUEPRINT_VALIDATION) < ctx.trace.index(State.COMPOSE_PROSE)
    assert "thematic echo" in ctx.prose["christ_fulfillment"].lower()
    assert "does not diagnose" in ctx.prose["reflection"].lower()
    assert "panting toward the stream" in ctx.prose["introduction"].lower()
    assert "empty" not in ctx.prose["introduction"].lower()
    assert "The Deer at the Stream" in ctx.artifact
