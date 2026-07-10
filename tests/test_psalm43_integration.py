from copy import deepcopy

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine
from tests.test_psalm42_integration import _psalm42_outputs


def _psalm43_outputs() -> dict:
    outputs = deepcopy(_psalm42_outputs())
    outputs["source_agent"] = {
        "source_text": (
            "Psalm 43 source text: Judge me, God, and plead my cause against an ungodly nation. "
            "Deliver me from the deceitful and unjust man. You are the God of my refuge; why have You rejected me? "
            "Why do I walk about mourning because of the oppression of the enemy? Send out Your light and Your truth; "
            "let them lead me. Let them bring me to Your holy mountain and to Your dwelling places. Then I will go to the altar of God, "
            "to God my exceeding joy, and I will praise You with the lyre, God, my God. Why are you bowed down, my living self? "
            "Wait for God, for I shall yet praise Him, the saving presence of my God."
        ),
        "chapter_verse_count": 5,
    }
    outputs["translator"] = {
        "working_rendering": (
            "Vindicate me, God, and contend for my cause against an unfaithful nation. Rescue me from the deceitful and unjust man. "
            "For You are the God of my refuge. Why have You cast me off? Why must I walk in mourning under an enemy's oppression? "
            "Send Your light and Your truth; let them lead me. Let them bring me to Your holy mountain and Your dwelling. "
            "Then I will come to God's altar, to God, my exceeding joy, and praise You with the lyre. Why are you bowed down, my living self? "
            "Wait for God, for I shall yet praise Him, the saving presence of my God."
        )
    }
    outputs["chapter_design_mapper"] = {
        "chapter_start": "A worshiper asks God to judge his cause and rescue him from deceit and oppression.",
        "chapter_end": "The bowed-down self is summoned again to wait for future praise.",
        "emotional_movement": "Public injustice and felt rejection move through petition for guidance toward altar, joy, and future praise.",
        "divine_action": "God vindicates, rescues, sends light and truth, leads to His dwelling, and remains the ground of future praise.",
        "physical_vocabulary": ["walk", "light", "truth", "lead", "mountain", "dwelling", "altar", "lyre", "face"],
        "central_theological_claim": "The God who seems distant remains the worshiper's refuge and can lead the oppressed from mourning into truthful worship.",
        "christward_fulfillment": "Jesus is the true light and truth who brings His people to the Father and secures access to God's presence.",
        "reader_felt_experience": "A person under false accusation keeps walking under pressure while asking God for a path back to worship.",
        "chapter_design_summary": "Psalm 43 moves from vindication, to felt rejection, to light-guided pilgrimage, to altar joy, and finally to the refrain of hope.",
    }
    outputs["canonist"] = {
        "pathway": "Psalm 43 is not directly cited as prophecy. John 8:12 and John 14:6 provide a thematic correspondence: Christ is the light and the truth who brings His people to the Father."
    }
    outputs["theological_risk_agent"] = {
        "risks": [
            {
                "risk_id": "R1",
                "risk_description": "Turn vindication into personal vengeance.",
                "why_it_matters": "The psalm entrusts judgment to God rather than authorizing retaliation.",
                "avoidance_rule": "Keep vindication judicial and covenantal, not vindictive.",
                "evaluator_check": "Verify that application rejects revenge.",
            },
            {
                "risk_id": "R2",
                "risk_description": "Treat light and truth as vague inner feelings.",
                "why_it_matters": "They are God's agents of guidance toward His mountain, dwelling, altar, and praise.",
                "avoidance_rule": "Keep the imagery directional and worship-centered.",
                "evaluator_check": "Verify that guidance leads toward God rather than self-expression.",
            },
        ]
    }
    outputs["historian_linguist"] = {"notes": "The paired imperatives ask God to send light and truth as guides toward His holy dwelling."}
    outputs["commentary_agent"] = {"notes": "Psalm 43 continues the emotional and liturgical movement of Psalm 42 but has its own burden: vindication and guidance back to worship."}
    outputs["art_director"] = {
        "register": "restrained petition under public pressure",
        "pace": "judicial opening, slow mourning, then directional movement toward worship",
        "sentence_music": "firm pleas opening into forward-moving clauses",
        "image_density": "light, path, mountain, dwelling, altar, lyre",
        "emotional_color": "oppression becoming guided hope without premature triumph",
        "opening_mode": "embodied movement",
        "poem_tone": "common meter pilgrimage prayer",
        "ending_resonance": "the road toward the altar remains lit by promise",
        "avoid": ["revenge", "vague illumination", "instant emotional resolution"],
    }
    outputs["creative_divergence_agent"] = {
        "threshold_phrase_candidates": ["Send light for the next step.", "Truth must lead somewhere.", "The road bends toward the altar."],
        "introduction_opening_candidates": ["The worshiper is still walking.", "Oppression has changed his pace, not his direction.", "He asks for light because the road is not clear."],
        "governing_image_candidates": ["light falling across a pilgrim road", "truth leading uphill", "the altar heard before it is reached"],
        "christology_framing_candidates": ["Christ as the light and truth who brings us to the Father"],
        "poem_arc_candidates": ["dark road to holy mountain to altar song"],
        "title_candidates": ["Light for the Road", "Led Toward the Altar"],
        "epigraph_candidates": ["Truth must lead somewhere.", "The road bends toward the altar."],
    }
    outputs["director"] = {
        "chapter_burden": "The oppressed worshiper entrusts vindication to God and asks for light and truth to lead him back into God's presence.",
        "opening_movement": "a mourning worshiper keeps walking under oppression",
        "closing_movement": "light and truth lead toward altar, joy, and future praise",
        "central_thought": "The God of refuge answers oppression not by licensing revenge but by sending light and truth that lead the bowed-down worshiper toward His altar and future praise.",
        "emotional_charge": "measured grief carried in the body of a person still walking",
        "transcendent_force": "God's light and truth moving as guides toward His holy dwelling",
        "selected_threshold_phrase": "Truth must lead somewhere.",
        "threshold_phrase_rationale": "The line preserves the psalm's directional logic: truth is sent to guide the worshiper toward God.",
        "governing_image": "light falling across a pilgrim road",
        "image_lexicon": ["walk", "road", "light", "truth", "lead", "mountain", "dwelling", "altar", "lyre"],
        "image_head_terms": ["light", "road"],
        "anchor_terms": ["refuge", "light", "truth", "joy", "Christ"],
        "chapter_specific_terms": ["vindicate", "oppression", "light", "truth", "holy mountain", "altar", "exceeding joy"],
        "christology_required_echoes": ["light", "truth", "Christ", "Father"],
        "christology_pathway": "A thematic correspondence links God's sent light and truth with Christ, who is the light of the world and the truth who brings His people to the Father.",
        "application_target": "Entrust judgment to God, refuse revenge, ask for truthful guidance, and take the next faithful step toward worship.",
        "theological_terminus": "access to the Father through Christ, the true light and truth",
        "negative_constraints": ["do not endorse revenge", "do not reduce light to mood", "do not impose instant resolution"],
        "poem_plan": "common meter moving from dark road to holy mountain and ending at the altar with future praise",
        "semantic_proof_chain": ["vindicate", "refuge", "mourning", "light", "truth", "lead", "mountain", "altar", "joy", "praise"],
    }
    outputs["composer"] = {
        "title": "Light for the Road",
        "epigraph": "Truth must lead somewhere.",
        "focus_bible_verses": "Psalm 43:1-5 — Vindicate me, God. Send Your light and Your truth; let them lead me. Let them bring me to Your holy mountain and Your dwelling. Then I will go to God's altar, to God, my exceeding joy.",
        "introduction": "The worshiper is still walking. Oppression has changed his pace, but not his direction. He asks God to judge his cause because he will not seize the judge's seat for himself.",
        "reflection": "Psalm 43 does not confuse vindication with revenge. The speaker names deceit, injustice, oppression, and the ache of feeling cast off, then places the case before God. His mourning has a gait: he walks under it. The body earns the sorrow before the psalm explains it. Then the prayer turns. Send Your light and Your truth. These are not decorative ideas or private moods. They are guides. They move ahead of the worshiper and bring him toward the mountain, the dwelling, the altar, and finally praise. The answer is not yet arrival. It is a trustworthy direction.",
        "christ_fulfillment": "Psalm 43 is not directly cited as a prophecy of Christ. Its strongest New Testament correspondence is thematic. Jesus names Himself the light of the world and the truth who brings His people to the Father. In Him, guidance is not detached information. Christ Himself becomes the way into God's presence. He does not authorize revenge against false accusers. He entrusts judgment to the Father and carries His people toward worship.",
        "application": "Place the case before God before rehearsing retaliation. Name the falsehood without becoming false. Ask what light Scripture gives for the next step and what truth must govern your speech. Then take one faithful step toward worship, counsel, reconciliation where possible, or lawful protection where necessary. Guidance is not always a full map. Often it is enough light to keep walking toward God.",
        "prayer": "Father, judge with righteousness where deceit and oppression have distorted what is true. Keep us from revenge and from becoming like those who wound us. Send Your light and Your truth to guide our next faithful step. Bring us through Christ to Your presence, restore truthful worship, and teach our bowed-down souls to wait for future praise, through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 44 - Faith remembers while defeat remains unexplained.",
    }
    outputs["poet"] = {"poem": "Send light upon the road I tread,\nAnd truth to walk before;\nLead on toward Your holy hill,\nAnd bring me to Your door.\n\nI will not take the judge's chair\nNor answer wrong with wrong;\nYour altar waits beyond the dark,\nMy exceeding joy and song.\n\nThough sorrow slows my weary feet,\nYour promise still shall be\nA lamp that leads through Christ the Truth\nTo praise yet waiting me."}
    outputs["beauty_pass_agent"] = {
        "lingering_lines": ["The worshiper is still walking.", "The answer is not yet arrival. It is a trustworthy direction."],
        "strongest_turn": "Light and truth become guides rather than abstractions.",
        "weakest_artistic_moment": "",
        "mechanical_residue": [],
        "beauty_score": 9,
        "required_beauty_revisions": [],
    }
    outputs["evaluator"] = {key: 9 for key in [
        "textual_fidelity", "theological_accuracy", "christology_from_chapter_logic", "chapter_design_fidelity",
        "emotional_charged_phrase", "introduction_strength", "ancient_image_discipline", "register",
        "read_aloud_quality", "application_concreteness", "prayer", "poem_form", "poetic_vitality",
        "artful_design", "artifact_integrity"
    ]}
    outputs["evaluator"].update({"fault_target": "none", "notes": "Psalm 43 preserves vindication without revenge and keeps light and truth directional."})
    outputs["contradiction_editor"] = {"verdict": "Pass", "major_conflicts": [], "minor_conflicts": [], "theological_risks": [], "literary_risks": [], "harness_risks": [], "required_revisions": [], "notes": "No conflicts."}
    return outputs


def test_psalm43_runs_full_v64_pipeline_separately() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 43"), MockAgentAdapter(_psalm43_outputs()))

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert ctx.trace.index(State.STORY_PLAN_BLUEPRINT) < ctx.trace.index(State.COMPOSE_PROSE)
    assert "revenge" in ctx.prose["reflection"].lower()
    assert "thematic" in ctx.prose["christ_fulfillment"].lower()
    assert "Light for the Road" in ctx.artifact
