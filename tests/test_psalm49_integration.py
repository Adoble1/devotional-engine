import json
from pathlib import Path

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def _psalm49_outputs() -> dict:
    path = Path(__file__).resolve().parents[1] / "examples" / "psalm24_mock_outputs.json"
    outputs = json.loads(path.read_text())

    outputs["source_agent"] = {
        "source_text": (
            "Psalm 49: Hear this, all peoples; give ear, all inhabitants of the world, "
            "both low and high, rich and poor together. Why should I fear in days of evil, "
            "when the iniquity of those who trust in wealth surrounds me? No one can redeem "
            "a brother or give God the ransom for his life, for the redemption price of a life "
            "is costly and can never suffice. The wise die; the fool and the senseless perish "
            "and leave their wealth to others. Their inward thought is that their houses will "
            "last forever, and they call lands by their own names. A person in honor does not "
            "remain; he is like the beasts that perish. Like sheep they are appointed for Sheol; "
            "death shall shepherd them. But God will ransom my life from the power of Sheol, "
            "for He will receive me. A person in honor without understanding is like the beasts "
            "that perish."
        ),
        "chapter_verse_count": 20,
    }
    outputs["translator"] = {
        "working_rendering": (
            "Hear this, all peoples; listen, all inhabitants of the world, low and high, rich and "
            "poor together. No one can redeem another or give God the ransom for a life, because "
            "the redemption price of life is costly and never sufficient. The wise die, and the "
            "foolish perish and leave their wealth to others. A person in honor does not remain; "
            "he resembles the beasts that perish. Like sheep they are appointed for Sheol; death "
            "shepherds them. But God will ransom my life from the power of Sheol, for He will receive me."
        )
    }
    outputs["chapter_design_mapper"] = {
        "chapter_start": "A universal wisdom summons places rich and poor beneath the same question.",
        "chapter_end": "Human wealth cannot redeem life, but the psalmist trusts God to ransom and receive him.",
        "emotional_movement": "Fear before wealthy oppressors gives way to sober recognition of death and confidence in God's receiving mercy.",
        "divine_action": "God fixes the value of life beyond human purchase, ransoms from Sheol, and receives His servant.",
        "physical_vocabulary": ["wealth", "houses", "lands", "grave", "sheep", "Sheol", "ransom", "receive"],
        "central_theological_claim": "Wealth cannot purchase life from death; hope rests in the God who alone can ransom and receive His people.",
        "christward_fulfillment": "Christ gives His life as the ransom human wealth cannot provide and rises beyond death's claim.",
        "reader_felt_experience": "The apparent permanence of wealth is exposed by the body that dies and the estate left behind.",
        "chapter_design_summary": "The wisdom poem moves from the intimidation of wealth, through death's equalizing limit, to God's power to ransom and receive.",
    }
    outputs["canonist"] = {
        "pathway": (
            "Psalm 49 is not directly quoted in the New Testament. Mark 10:45 and 1 Peter 1:18-19 "
            "provide strong canonical development: Christ gives His life as ransom, not with silver "
            "or gold, while His resurrection discloses the reach of God's victory over death."
        )
    }
    outputs["theological_risk_agent"] = {
        "risks": [
            {
                "risk_id": "R1",
                "risk_description": "Treat the comparison with beasts as a denial of the human soul or of life beyond death.",
                "why_it_matters": "The comparison concerns mortal inability and honor without understanding, while verse 15 confesses that God will ransom and receive the psalmist.",
                "avoidance_rule": "State that the comparison strips pomp of power over mortality; do not make it an anthropology of annihilation.",
                "evaluator_check": "The reflection must preserve verse 15 and avoid claiming that human beings cease to exist like animals.",
                "status": "resolved",
                "severity": "high",
            },
            {
                "risk_id": "R2",
                "risk_description": "Condemn possessions rather than misplaced trust in them.",
                "why_it_matters": "The psalm condemns confidence and boasting in wealth, not responsible possession itself.",
                "avoidance_rule": "Distinguish faithful use of wealth from trusting wealth to redeem or secure life.",
                "evaluator_check": "Application must not present poverty as meritorious or possessions as inherently evil.",
                "status": "resolved",
                "severity": "medium",
            },
            {
                "risk_id": "R3",
                "risk_description": "Present New Testament ransom texts as direct quotations of Psalm 49.",
                "why_it_matters": "The canonical relationship is strong development, not explicit apostolic citation.",
                "avoidance_rule": "Say that no direct New Testament quotation is identified and distinguish development from citation.",
                "evaluator_check": "Christological section must label the relationship accurately.",
                "status": "resolved",
                "severity": "high",
            },
            {
                "risk_id": "R4",
                "risk_description": "Invent a historical deathbed, funeral, estate dispute, or burial scene.",
                "why_it_matters": "Psalm 49 is wisdom poetry addressing all peoples, not a report of one observed death.",
                "avoidance_rule": "Enter the psalm's universal contrast without historicizing it.",
                "evaluator_check": "No invented names, mourners, rooms, weather, burial, or witnessed event.",
                "status": "resolved",
                "severity": "medium",
            },
        ]
    }
    outputs["historian_linguist"] = {
        "notes": (
            "The psalm is wisdom instruction addressed universally. Its ransom vocabulary concerns "
            "a payment no human can render to God, while Sheol names the realm or power of death."
        )
    }
    outputs["commentary_agent"] = {
        "notes": (
            "Verses 12 and 20 compare honored humanity without understanding to perishing beasts; "
            "verse 15 prevents that comparison from being read as a denial of God's power to receive "
            "and ransom the faithful beyond death."
        )
    }
    outputs["art_director"] = {
        "register": "compressed wisdom with financial and mortality imagery",
        "pace": "five-sentence opening, measured comparison, sharp turn at verse 15, restrained hope",
        "sentence_music": "plain declarations followed by longer interpretive sentences",
        "image_density": "one system of price, estate, ransom, shepherding death, and divine receiving",
        "emotional_color": "sober clarity rather than fearmongering or sentimental consolation",
        "opening_mode": "text-derived contradiction without an invented funeral scene",
        "poem_tone": "measured wisdom moving from false security to costly redemption",
        "ending_resonance": "the grave cannot retain what God receives",
        "avoid": [
            "invented funeral scene",
            "wealth-is-evil moralism",
            "annihilation claim",
            "direct-quotation overclaim",
            "prematurely solved title",
        ],
    }
    outputs["creative_divergence_agent"] = {
        "threshold_phrase_candidates": [
            "The estate keeps his name.",
            "The price remains beyond him.",
            "Death accepts no fortune.",
            "The owner leaves first.",
            "The account cannot be settled."
        ],
        "introduction_opening_candidates": [
            "The rich man dies. His estate keeps his name. He does not keep the estate.",
            "The land retains the name its owner gave it. The owner is gone.",
            "Rich and poor stand beneath the same command to listen."
        ],
        "governing_image_candidates": [
            "an estate retaining a dead owner's name",
            "a ransom price no fortune reaches",
            "death shepherding sheep toward Sheol"
        ],
        "christology_framing_candidates": [
            "Christ gives His life as the ransom God provides",
            "the risen Christ reveals that death does not own those God receives"
        ],
        "poem_arc_candidates": [
            "estate to grave to ransom to receiving",
            "boast to death's shepherding to Christ's costly gift"
        ],
        "title_candidates": ["The Price", "After the Estate", "What Wealth Leaves"],
        "epigraph_candidates": [
            "A fortune reaches the grave and stops.",
            "The owner leaves before the name fades.",
            "Only God can pay what wealth cannot."
        ],
    }
    outputs["director"] = {
        "chapter_burden": "Expose wealth's inability to ransom life without condemning faithful possession, then rest hope in God's power to receive and redeem.",
        "opening_movement": "the rich person dies while the named estate remains behind",
        "closing_movement": "God receives the person whom wealth could not preserve",
        "central_thought": "The estate outlives its owner, but neither estate nor honor can ransom life; God alone can receive and redeem from Sheol.",
        "emotional_charge": "the quiet humiliation of leaving behind what seemed permanent",
        "transcendent_force": "God's authority over the value, death, ransom, and reception of human life",
        "selected_threshold_phrase": "The estate keeps his name.",
        "threshold_phrase_rationale": "The phrase arises from the psalm's named lands and creates the question of what the owner truly kept.",
        "governing_image": "an estate retaining a dead owner's name",
        "image_lexicon": ["estate", "name", "wealth", "price", "ransom", "sheep", "Sheol", "receive"],
        "image_head_terms": ["estate", "ransom"],
        "anchor_terms": ["all peoples", "wealth", "ransom", "Sheol", "receive", "Christ"],
        "chapter_specific_terms": ["rich and poor together", "houses forever", "lands by their own names", "death shall shepherd", "God will ransom", "He will receive me"],
        "christology_required_echoes": ["ransom", "silver", "gold", "Christ", "resurrection"],
        "christology_pathway": "No direct New Testament quotation is identified; Christ's self-giving ransom and resurrection are the strongest canonical developments of the psalm's God-provided redemption.",
        "application_target": "Use wealth without trusting it to redeem, secure, or define your life.",
        "theological_terminus": "God's costly redemption and receiving mercy fulfilled in the crucified and risen Christ",
        "negative_constraints": [
            "do not invent a funeral or burial scene",
            "do not deny the human soul",
            "do not call wealth inherently evil",
            "do not claim a direct New Testament quotation",
            "distinguish poetic comparison from systematic anthropology"
        ],
        "poem_plan": "four stanzas moving from estate and grave to ransom and resurrection",
        "semantic_proof_chain": ["all peoples", "wealth", "die", "leave", "beasts", "Sheol", "ransom", "receive"],
        "historical_meaning": "A wisdom teacher addresses all social ranks and exposes the inability of wealth and honor to prevent death or redeem a life before God.",
        "canonical_trajectory": "God's promise to ransom and receive develops through Christ's self-giving ransom and resurrection, without requiring a direct quotation of the psalm.",
        "apostolic_interpretation": "No explicit New Testament quotation of Psalm 49 is identified; Mark 10:45 and 1 Peter 1:18-19 are ranked as strong canonical developments.",
        "governing_mystery": "If no person can pay the ransom for a life, how can the psalmist expect release from Sheol?",
        "governing_revelation": "God Himself provides the ransom in Christ and demonstrates its victory through resurrection.",
    }
    outputs["composer"] = {
        "title": "The Price",
        "epigraph": "A fortune reaches the grave and stops.",
        "focus_bible_verses": (
            "Psalm 49:1-2, 7-9, 12, 15, 20 — Hear this, all peoples; listen, all inhabitants "
            "of the world, rich and poor together. No one can redeem another or give God the ransom "
            "for a life. A person in honor does not remain; he resembles the beasts that perish. "
            "But God will ransom my life from the power of Sheol, for He will receive me."
        ),
        "introduction": (
            "The rich man dies.\n\nHis estate keeps his name. He does not keep the estate. "
            "Psalm 49 places wealth beside the grave and asks what money can do there. "
            "It cannot ransom a life."
        ),
        "reflection": (
            "The song calls all peoples to listen, low and high, rich and poor together. Its wisdom "
            "is universal because death ignores rank. The wealthy trust abundance and name lands "
            "after themselves, yet the wise and foolish die alike and leave their wealth to others. "
            "The comparison with beasts does not deny the human soul. It strips human honor of its "
            "imagined power over mortality. A person in pomp without understanding cannot use status "
            "to escape the end shared by mortal creatures. No one can redeem another or give God the "
            "price of a life. Human wealth fails not because the owner offered too little, but because "
            "no fortune can purchase life from God. Then death becomes a shepherd, driving those who "
            "trusted themselves toward Sheol. The riddle turns at verse 15. God will ransom the "
            "psalmist's life from the power of Sheol and receive him. The psalm does not explain the "
            "full manner or timing of that hope. It confesses that the God whom wealth cannot bargain "
            "with can ransom and receive His servant."
        ),
        "christ_fulfillment": (
            "Psalm 49 is not directly quoted in the New Testament. Its question nevertheless develops "
            "toward Christ. Jesus says that the Son of Man gives His life as a ransom for many. Peter "
            "says believers were redeemed not with perishable silver or gold but with the precious blood "
            "of Christ. God does not discover a human fortune large enough to meet the price; He provides "
            "the ransom in His Son. Christ enters death and rises, disclosing the reach of the psalm's "
            "confidence that God can ransom from Sheol. Those united to Him still die, but death does not "
            "own them. Their lives belong to the risen Lord, and their bodies await resurrection."
        ),
        "application": (
            "Use wealth without trusting it to redeem, secure, or define your life. Receive possessions "
            "as stewardship, not proof that you are beyond danger. Make plans without asking plans to "
            "guarantee tomorrow. Let property carry your name without expecting the name to make you last. "
            "Then look to Christ, whose ransom was not drawn from an estate and whose risen life cannot be "
            "held by the grave."
        ),
        "prayer": (
            "Father, every life belongs to You. Forgive us for trusting wealth, status, or memory to do "
            "what only Your mercy can do. Teach us to use possessions faithfully without asking them to "
            "redeem or define us. We praise You for the ransom given in Jesus Christ and for the resurrection "
            "hope secured in Him. Receive us as Your own and keep us faithful through Jesus Christ our Lord. Amen."
        ),
        "next_in_sequence": "Psalm 50 - God summons His covenant people before His judgment seat.",
    }
    outputs["voice_keeper"] = {"approved": True}
    outputs["poet"] = {
        "poem": (
            "The house retains the owner's name,\nBut not the owner's breath;\nNo field or fortune pays the price\nDemanded at his death.\n\n"
            "Like sheep the generations pass\nWhere death would have them go;\nThe guarded wealth they leave behind\nCannot redeem from Sheol.\n\n"
            "No silver reaches high enough,\nNo gold can purchase breath;\nThe Son of Man gives up His life\nAnd enters human death.\n\n"
            "The risen Christ has left the grave;\nIts claim shall not endure.\nThe God who ransoms and receives\nWill keep His people sure."
        )
    }
    outputs["beauty_pass_agent"] = {
        "lingering_lines": ["His estate keeps his name. He does not keep the estate.", "A fortune reaches the grave and stops."],
        "strongest_turn": "The text moves from the impossible human ransom to God's promise to ransom and receive.",
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
        "notes": (
            "Psalm 49 remains wisdom poetry, distinguishes human mortality from denial of the soul, "
            "treats wealth as a false refuge rather than an inherent evil, and labels New Testament "
            "ransom texts as canonical development rather than direct quotation."
        ),
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


def test_psalm49_runs_full_v65_devotional_pipeline() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 49"), MockAgentAdapter(_psalm49_outputs()))

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert ctx.trace.index(State.STORY_PLAN_BLUEPRINT) < ctx.trace.index(State.COMPOSE_PROSE)
    assert ctx.trace.index(State.BLUEPRINT_VALIDATION) < ctx.trace.index(State.COMPOSE_PROSE)

    assert ctx.prose["title"] == "The Price"
    first_five = [
        "The rich man dies.",
        "His estate keeps his name.",
        "He does not keep the estate.",
        "Psalm 49 places wealth beside the grave and asks what money can do there.",
        "It cannot ransom a life.",
    ]
    introduction = ctx.prose["introduction"]
    positions = [introduction.index(sentence) for sentence in first_five]
    assert positions == sorted(positions)

    reflection = ctx.prose["reflection"].lower()
    christology = ctx.prose["christ_fulfillment"].lower()
    application = ctx.prose["application"].lower()

    assert "does not deny the human soul" in reflection
    assert "god will ransom" in reflection
    assert "not directly quoted" in christology
    assert "silver or gold" in christology
    assert "their bodies await resurrection" in christology
    assert "use wealth without trusting it" in application

    forbidden_inventions = ["funeral", "mourners", "coffin", "burial room", "widow watched"]
    artifact_lower = ctx.artifact.lower()
    assert not any(term in artifact_lower for term in forbidden_inventions)
    assert "# The Price" in ctx.artifact
