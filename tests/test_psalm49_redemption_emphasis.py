from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine
from tests.test_psalm49_integration import _psalm49_outputs


def _redemption_centered_outputs() -> dict:
    outputs = _psalm49_outputs()

    outputs["chapter_design_mapper"].update(
        {
            "chapter_start": "Death shepherds every social rank toward Sheol, where human wealth cannot ransom a life.",
            "chapter_end": "God receives His servant, and Christ reveals that divine redemption culminates in bodily resurrection.",
            "emotional_movement": "The flock moves beneath death's staff until confidence turns toward the God who ransoms, receives, and raises His own.",
            "divine_action": "God ransoms from Sheol, receives His servant, provides the ransom in Christ, and raises the whole person.",
            "central_theological_claim": "Human beings cannot redeem life from death, but God receives His own and fulfills that hope through Christ's ransom and resurrection.",
            "christward_fulfillment": "Christ gives His life as the God-provided ransom, rises bodily, receives His people through death, and will raise their bodies.",
            "reader_felt_experience": "Death appears as a shepherd gathering every rank, until God's promise to receive His servant interrupts the procession.",
            "chapter_design_summary": "The wisdom poem moves from death's universal shepherding to God's personal act of ransoming and receiving, then toward resurrection in Christ.",
        }
    )

    outputs["art_director"].update(
        {
            "register": "sober wisdom opening in death's procession and widening into resurrection hope",
            "pace": "brief material contrast, sustained Sheol imagery, decisive turn at divine receiving, expansive resurrection close",
            "sentence_music": "grave declarative clauses opening into longer sentences of promise",
            "image_density": "death shepherding, Sheol receiving, God receiving, Christ rising, dust awakened",
            "emotional_color": "mortality faced without evasion and hope stated without sentimentality",
            "opening_mode": "begin with death as shepherd rather than wealth as spectacle",
            "poem_tone": "measured passage from death's flock to the risen Shepherd",
            "ending_resonance": "redemption reaches the body and even the dust",
            "avoid": [
                "letting material wealth dominate the reflection",
                "reducing redemption to financial metaphor",
                "reducing salvation to survival of an immaterial soul",
                "invented funeral scene",
                "direct-quotation overclaim",
            ],
        }
    )

    outputs["creative_divergence_agent"].update(
        {
            "threshold_phrase_candidates": [
                "Death becomes a shepherd.",
                "Another Shepherd receives them.",
                "Sheol does not speak last.",
                "The flock changes hands.",
                "God reaches beyond the grave.",
            ],
            "introduction_opening_candidates": [
                "Death becomes a shepherd. Generation after generation enters its flock.",
                "The wise and foolish move beneath the same staff.",
                "The psalm watches one flock descend toward Sheol, then hears God claim one life as His own.",
            ],
            "governing_image_candidates": [
                "death shepherding every rank toward Sheol",
                "God receiving His servant from death's flock",
                "the risen Shepherd calling dust into life",
            ],
            "christology_framing_candidates": [
                "Christ as the ransom God Himself provides",
                "Christ as the risen Shepherd whose redemption reaches the body",
            ],
            "poem_arc_candidates": [
                "death's flock to divine receiving to bodily resurrection",
                "Sheol's staff to Christ's ransom to awakened dust",
            ],
            "title_candidates": ["Beyond Sheol", "Another Shepherd", "He Will Receive"],
            "epigraph_candidates": [
                "Death gathers the living. God receives His own.",
                "Sheol takes the body; God claims the person.",
                "The ransom reaches even the dust.",
            ],
        }
    )

    outputs["director"].update(
        {
            "chapter_burden": "Use wealth only to expose human inability, then dwell on death's shepherding, God's receiving act, Christ's ransom, and the resurrection of the whole person.",
            "opening_movement": "death becomes a shepherd and gathers every social rank toward Sheol",
            "closing_movement": "God receives His servant in Christ and will raise the body from the dust",
            "central_thought": "Death shepherds every rank toward Sheol, but God receives His own, provides the ransom in Christ, and will raise the whole person.",
            "emotional_charge": "the severe quiet of a universal procession interrupted by divine possession and promise",
            "transcendent_force": "the God whose receiving mercy reaches farther than Sheol and culminates in resurrection",
            "selected_threshold_phrase": "Death becomes a shepherd.",
            "threshold_phrase_rationale": "The phrase comes directly from verse 14 and places the true subject, death's dominion, before the failed instrument of wealth.",
            "governing_image": "death becomes a shepherd",
            "image_lexicon": ["shepherd", "sheep", "staff", "Sheol", "ransom", "receive", "grave", "dust", "rise"],
            "image_head_terms": ["shepherd", "receive"],
            "anchor_terms": ["death shall shepherd", "Sheol", "God will ransom", "He will receive me", "Christ", "resurrection"],
            "chapter_specific_terms": ["rich and poor together", "death shall shepherd them", "power of Sheol", "God will ransom", "He will receive me"],
            "christology_required_echoes": ["ransom", "silver", "gold", "Christ", "resurrection", "body"],
            "christology_pathway": "Psalm 49 is not directly quoted in the New Testament; Christ's self-giving ransom and bodily resurrection disclose how God receives and ultimately raises His people from death.",
            "application_target": "Entrust the whole person to Christ",
            "theological_terminus": "the resurrection of the whole person through union with the crucified and risen Christ",
            "negative_constraints": [
                "material wealth may introduce human inability but must not dominate the devotional",
                "make God will receive me the interpretive hinge",
                "do not deny the human soul",
                "do not reduce Christian hope to an immaterial afterlife",
                "do not claim a direct New Testament quotation",
                "do not invent a funeral or burial scene",
            ],
            "poem_plan": "four stanzas moving from death's flock through divine ransom to bodily resurrection",
            "semantic_proof_chain": ["all peoples", "cannot redeem", "death shall shepherd", "Sheol", "God will ransom", "receive", "Christ", "rise"],
            "historical_meaning": "A wisdom teacher exposes human inability before death and confesses that God can ransom and receive His servant from Sheol.",
            "canonical_trajectory": "The Hebrew Bible's hope that God can receive beyond Sheol develops through Jewish resurrection expectation and reaches Christian fulfillment in Christ's bodily resurrection.",
            "apostolic_interpretation": "No explicit New Testament quotation of Psalm 49 is identified; Mark 10:45, 1 Peter 1:18-19, and 1 Corinthians 15 provide canonical development rather than direct citation.",
            "governing_mystery": "If every human life enters death's flock and no person can pay the ransom, how can God receive the psalmist from Sheol?",
            "governing_revelation": "God provides the ransom in Christ, receives those united to Him through death, and will raise their bodies at His appearing.",
        }
    )

    outputs["composer"] = {
        "title": "Beyond Sheol",
        "epigraph": "Death gathers the living. God receives His own.",
        "focus_bible_verses": (
            "Psalm 49:1-2, 7-8, 14-15 — Hear this, all peoples; listen, all inhabitants of the world, "
            "rich and poor together. No one can redeem another or give God the ransom for a life. "
            "Like sheep they are appointed for Sheol; death shall shepherd them. But God will ransom "
            "my life from the power of Sheol, for He will receive me."
        ),
        "introduction": (
            "Death becomes a shepherd.\n\nGeneration after generation enters its flock. The wise are "
            "there. The foolish are there. The honored and forgotten move beneath the same staff."
        ),
        "reflection": (
            "Death becomes a shepherd. The image is quiet and severe. Like sheep, low and high, rich "
            "and poor move toward Sheol beneath one staff. Wealth appears because it exposes the limit "
            "of human power: a person may preserve a name on land, yet no fortune can cross into death "
            "and purchase the owner's release. No one can redeem another or give God the price of a life. "
            "The contrast is no longer between rich and poor. It is between what humanity cannot do and "
            "what God can do. No man can ransom. God will ransom. Death shepherds toward Sheol. God receives. "
            "Verse 15 is the hinge: God will ransom the psalmist's life from the power of Sheol, for He will "
            "receive him. The psalm does not yet describe the resurrection body or the full order of the world "
            "to come. It does confess that covenant fellowship with God is not cancelled by death. Sheol may "
            "claim mortal life, but it cannot place God's servant beyond God's reach."
        ),
        "christ_fulfillment": (
            "Psalm 49 is not directly quoted in the New Testament. Its unanswered question nevertheless "
            "moves toward Christ. Jesus gives His life as a ransom for many, and Peter says believers were "
            "redeemed not with silver or gold but with the precious blood of Christ. God provides what no "
            "human fortune can supply. Yet Christian hope is not merely the survival of an immaterial soul. "
            "Christ rises bodily. Those united to Him remain His through death, and their bodies await "
            "resurrection. The God who receives the person will redeem the whole person. At Christ's appearing, "
            "what was sown perishable will be raised imperishable, and even the dust will answer the risen Lord."
        ),
        "application": (
            "Entrust the whole person to Christ. Earthly provisions may serve the living, but they cannot carry "
            "you beyond death. Arrange your possessions wisely, yet prepare more deeply by belonging to the One "
            "who receives His people when every possession must be released. Your hope is not merely that some "
            "part of you survives. Your hope is that death cannot sever you from Christ and that He will raise "
            "your body in glory. A will determines who receives your estate. Only God can receive you."
        ),
        "prayer": (
            "Father, You alone hold the power of life and death. No human wealth or strength can ransom us from "
            "Sheol. We praise You for providing the ransom in Jesus Christ, not with silver or gold but through "
            "His precious blood. Receive us as Your own when our earthly lives are finished. Keep us in Christ "
            "through death and raise our bodies in glory at His appearing. Fix our hope upon the resurrection of "
            "the body and the life of the world to come, through Jesus Christ our Lord. Amen."
        ),
        "next_in_sequence": "Psalm 50 - God summons His covenant people and judges worship severed from obedience.",
    }

    outputs["poet"] = {
        "poem": (
            "Death gathers all beneath its staff,\nThe lowly and the great;\nNo silver buys a life from God\nOr bars the grave's dark gate.\n\n"
            "Yet through the silence of Sheol\nA stronger word is given;\nThe God who knows His servant's name\nReceives the life He claims.\n\n"
            "The Son has paid the ransom price,\nNot silver, land, or gold;\nThe risen Shepherd keeps His own\nWhom death could never hold.\n\n"
            "Their bodies rest within the dust,\nBut not beyond His call;\nThe Lord who rose shall raise His saints,\nAnd life shall conquer all."
        )
    }
    outputs["beauty_pass_agent"] = {
        "lingering_lines": ["Death becomes a shepherd.", "A will determines who receives your estate. Only God can receive you."],
        "strongest_turn": "The contrast shifts from rich and poor to human inability and divine receiving, then opens into bodily resurrection.",
        "weakest_artistic_moment": "",
        "mechanical_residue": [],
        "beauty_score": 9,
        "required_beauty_revisions": [],
    }
    outputs["evaluator"]["notes"] = (
        "Psalm 49 now uses material wealth briefly as the failed instrument, makes death's shepherding and God's "
        "receiving act the controlling contrast, accurately treats New Testament ransom texts as canonical "
        "development, and carries redemption through to bodily resurrection."
    )
    return outputs


def test_psalm49_centers_redemption_from_death() -> None:
    ctx = run_engine(EngineContext(chapter_ref="Psalm 49"), MockAgentAdapter(_redemption_centered_outputs()))

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.blueprint is not None and ctx.blueprint.approved
    assert ctx.prose["title"] == "Beyond Sheol"

    reflection = ctx.prose["reflection"].lower()
    christology = ctx.prose["christ_fulfillment"].lower()
    application = ctx.prose["application"].lower()
    prayer = ctx.prose["prayer"].lower()

    assert reflection.index("death becomes a shepherd") < reflection.index("wealth")
    assert reflection.count("wealth") <= 2
    redemption_weight = sum(reflection.count(term) for term in ("death", "sheol", "ransom", "receive"))
    assert redemption_weight >= 5 * max(reflection.count("wealth"), 1)
    assert "the contrast is no longer between rich and poor" in reflection
    assert "god receives" in reflection

    assert "not merely the survival of an immaterial soul" in christology
    assert "bodies await resurrection" in christology
    assert "redeem the whole person" in christology
    assert "entrust the whole person to christ" in application
    assert "raise your body in glory" in application
    assert "resurrection of the body" in prayer

    assert "# Beyond Sheol" in ctx.artifact
    assert "Death gathers the living. God receives His own." in ctx.artifact
