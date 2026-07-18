from copy import deepcopy

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter, State, run_engine
from devotional_engine.integrated_v67 import adapter_supports_integrated_devotional


def _grounding() -> dict:
    provenance = {
        "quotation_mode": "test_fixture",
        "attribution": "Integrated deterministic Scripture fixture; not for publication",
        "human_review_required": True,
    }
    return {
        "source_text": (
            "Psalm 52: Why do you boast in evil? God's steadfast love endures all day. "
            "Your tongue plans destruction like a sharp razor. God will uproot you. "
            "But I am like a green olive tree in the house of God."
        ),
        "working_rendering": (
            "Why do you boast in evil? The steadfast love of God endures continually. "
            "Your tongue devises destruction like a sharpened razor. God will uproot you, "
            "but I am like a flourishing olive tree in God's house."
        ),
        "source_provenance": deepcopy(provenance),
        "rendering_provenance": deepcopy(provenance),
        "chapter_verse_count": 9,
        "historical_meaning": (
            "A wisdom-shaped denunciation addresses destructive speech and false refuge, "
            "then contrasts uprooting with trust in God's enduring covenant love."
        ),
        "literary_mode": "individual thanksgiving and wisdom denunciation",
        "textual_evidence": [
            {"id": "E1", "reference": "Psalm 52:1-4", "claim": "The destructive tongue serves evil and deceit."},
            {"id": "E2", "reference": "Psalm 52:5", "claim": "God answers false security by uprooting it."},
            {"id": "E3", "reference": "Psalm 52:8-9", "claim": "The faithful person trusts steadfast love and gives thanks."},
        ],
        "governing_claim": "God's steadfast love outlasts destructive power and roots truthful trust.",
        "textual_hinge": "God uproots the person who made destruction a refuge.",
        "divine_action": "God judges false refuge and preserves the one who trusts His steadfast love.",
        "canonical_relationship": {
            "classification": "thematic_correspondence",
            "description": "Christ is the truthful King who bears slander, rises, and reforms the speech of His people.",
        },
        "christological_fulfillment": (
            "Jesus, in whose mouth there was no deceit, bears destructive accusation, rises, "
            "and roots His people in God's love."
        ),
        "reader_felt_experience": "Words and influence can appear powerful enough to make harm permanent.",
        "physical_vocabulary": ["tongue", "razor", "tent", "root", "olive leaf", "oil", "wind"],
        "risks": [
            {
                "risk_description": "Treat every report of wrongdoing as destructive speech.",
                "avoidance_rule": "Distinguish truthful protection from selective speech intended to injure.",
            },
            {
                "risk_description": "Turn Doeg's superscription into invented motives or scenes.",
                "avoidance_rule": "Use only details established by Scripture and the psalm's poetic claims.",
            },
        ],
        "unsupported_claims": ["Do not invent Doeg's private emotions or David's location."],
    }


def _plan() -> dict:
    return {
        "governing_question": "Can destructive power make itself secure?",
        "human_predicament": "People use truthful fragments, influence, and speech as instruments of control.",
        "reader_transformation": {
            "initial_assumption": "The damaging speaker appears rooted because the damage succeeds.",
            "new_perception": "Destructive power is uprooted while trust in steadfast love remains alive.",
            "faithful_response": "Speak truth without making destruction your refuge.",
        },
        "section_burdens": {
            "introduction": "Enter through the sudden cut of a word.",
            "reflection": "Move from destructive speech to the false refuge beneath it.",
            "christ_fulfillment": "Let resurrection overturn the verdict of destructive speech.",
            "application": "Examine the refuge and purpose beneath one's words.",
            "prayer": "Ask for rooted trust and truthful speech.",
        },
        "art_direction": {
            "register": "compressed, lucid, contemplative",
            "pace": "a quick cut followed by slower rooted breath",
            "image_lexicon": ["razor", "root", "olive leaf", "oil", "wind"],
        },
        "poem_design": {
            "image_field": ["razor", "olive tree"],
            "sensory_palette": ["razor", "root", "olive leaf", "oil", "wind"],
            "sonic_movement": "hard consonants opening into long vowels and quieter breath",
            "emotional_turn": "from the flash of injury to life held underground",
            "prohibited_exposition": ["do not name the lesson"],
        },
        "supporting_elements": ["wealth and influence function as false refuges"],
        "local_constraints": [
            "do not condemn necessary reporting of abuse or danger",
            "do not make speech rather than steadfast love the final subject",
        ],
    }


def _draft(application: str | None = None, poem: str | None = None) -> dict:
    return {
        "title": "Under the Olive",
        "epigraph": "The blade flashes. The root keeps its dark counsel.",
        "focus_bible_verses": (
            "Psalm 52:1, 5, 8-9 — Why do you boast in evil? God's steadfast love endures continually. "
            "God will uproot the false refuge, but I am like a flourishing olive tree in His house."
        ),
        "introduction": "A word can cross a room before mercy has risen from its chair.",
        "reflection": (
            "Psalm 52 follows the cut to its hidden root. The destructive tongue trusts wealth, access, "
            "and the thrill of successful harm. God answers not by admiring the blade but by pulling up "
            "the refuge beneath it. What remains is the olive tree: life held by steadfast love, its mouth "
            "turned at last toward thanks."
        ),
        "christ_fulfillment": (
            "The correspondence is thematic, not a direct New Testament quotation. False witnesses sharpen "
            "words against Jesus, yet the Father raises Him beyond their verdict. In Him, the uprooted are "
            "given a life no accusation can finally sever."
        ),
        "application": application or (
            "Before speaking, ask what shelter the sentence is building. Tell the truth needed for protection "
            "or justice; refuse the extra turn of the blade that only feeds control."
        ),
        "prayer": (
            "Father, root us in Your steadfast love. Forgive the words we have used to control or injure. "
            "Give us courage to tell necessary truth without cruelty. Shape our speech after Jesus. "
            "Keep us faithful through Jesus Christ our Lord."
        ),
        "poem": poem or (
            "Razor-light—\nthen the room goes still.\n\nUnder stone,\na root drinks darkness.\n\nOne olive leaf\nturns in the wind,\nits small green silence\noiled with dawn."
        ),
        "next_in_sequence": "Psalm 53 - Human corruption is exposed and salvation is awaited from Zion.",
    }


def _review(verdict: str = "Pass", hard_findings=None, advisory_findings=None) -> dict:
    return {
        "verdict": verdict,
        "hard_findings": hard_findings or [],
        "advisory_findings": advisory_findings or [],
        "dimensions": {
            "textual_fidelity": 9,
            "theological_accuracy": 9,
            "canonical_warrant": 9,
            "blueprint_alignment": 9,
            "verbal_economy": 9,
            "literary_quality": 9,
            "poetic_integrity": 9,
            "sensory_presence": 9,
            "read_aloud_flow": 9,
        },
    }


def test_integrated_runner_uses_lean_packet_and_preserves_artistic_freedom() -> None:
    captured = {}

    def compose(payload):
        captured.update(payload)
        return _draft()

    adapter = MockAgentAdapter(
        {
            "devotional_grounder": _grounding(),
            "devotional_planner": _plan(),
            "devotional_composer": compose,
            "devotional_reviewer": _review(
                advisory_findings=[{"code": "A1", "field": "poem", "message": "Keep the final vowel open."}]
            ),
        }
    )
    ctx = run_engine(EngineContext(chapter_ref="Psalm 52"), adapter)

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.pipeline_mode == "integrated"
    assert State.TEXT_GROUNDING in ctx.trace
    assert State.PASSAGE_BLUEPRINT in ctx.trace
    assert State.INTEGRATED_COMPOSITION in ctx.trace
    assert State.INTEGRATED_REVIEW in ctx.trace
    assert State.CANONICAL_CORRESPONDENCE not in ctx.trace
    assert ctx.blueprint.approved
    assert ctx.prose["title"] == "Under the Olive"
    assert "INTEGRATED A1" in "\n".join(ctx.warnings)
    assert "Integrated deterministic Scripture fixture" in ctx.artifact

    assert set(captured) == {"composition_packet", "revision", "revision_brief"}
    packet = captured["composition_packet"]
    assert "grounding" not in packet
    assert "context" not in packet
    assert packet["poem_design"]["sensory_palette"][:2] == ["razor", "root"]
    assert "poem" not in packet["prose_movements"]


def test_literary_findings_can_trigger_one_targeted_poem_revision() -> None:
    prose_poem = (
        "This means the destructive speaker cannot remain secure forever.\n"
        "The psalm teaches that divine judgment will expose every false refuge.\n"
        "We learn that truthful speech must replace manipulative speech in our lives.\n"
        "Therefore we should trust God instead of wealth and human influence.\n"
        "The final lesson is that steadfast love will preserve faithful people.\n"
        "In conclusion, the believer should speak carefully and obey God."
    )

    def compose(payload):
        if payload["revision"] == 0:
            return _draft(poem=prose_poem)
        codes = {item["code"] for item in payload["revision_brief"]["literary_findings"]}
        assert {"LE04", "LE06", "LE08"}.intersection(codes)
        return _draft()

    def review(payload):
        if payload["revision"] == 0:
            assert payload["literary_findings"]
            return _review("Revise")
        return _review("Pass")

    adapter = MockAgentAdapter(
        {
            "devotional_grounder": _grounding(),
            "devotional_planner": _plan(),
            "devotional_composer": compose,
            "devotional_reviewer": review,
        }
    )
    ctx = run_engine(EngineContext(chapter_ref="Psalm 52"), adapter)

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.trace.count(State.PASSAGE_BLUEPRINT) == 1
    assert State.TARGETED_REVISION in ctx.trace
    assert len(ctx.draft_log) == 2
    assert "olive leaf" in ctx.poem.lower()


def test_integrated_runner_allows_one_truth_targeted_revision_without_replanning() -> None:
    def compose(payload):
        if payload["revision"] == 0:
            return _draft("Be careful with your speech.")
        assert payload["revision_brief"]["hard_findings"]
        return _draft()

    def review(payload):
        if payload["revision"] == 0:
            return _review(
                "Revise",
                hard_findings=[
                    {
                        "code": "R10",
                        "field": "application",
                        "message": "Application is not yet derived concretely from the approved response.",
                        "repair_target": "application",
                    }
                ],
            )
        return _review("Pass")

    adapter = MockAgentAdapter(
        {
            "devotional_grounder": _grounding(),
            "devotional_planner": _plan(),
            "devotional_composer": compose,
            "devotional_reviewer": review,
        }
    )
    ctx = run_engine(EngineContext(chapter_ref="Psalm 52"), adapter)

    assert ctx.trace[-1] is State.DONE, ctx.error or ctx.failed_checks
    assert ctx.trace.count(State.PASSAGE_BLUEPRINT) == 1
    assert State.TARGETED_REVISION in ctx.trace
    assert len(ctx.draft_log) == 2
    assert "protection" in ctx.prose["application"]


def test_old_mock_roles_use_legacy_compatibility_path() -> None:
    adapter = MockAgentAdapter({"source_agent": {"source_text": "fixture only"}})
    assert not adapter_supports_integrated_devotional(adapter)
    assert EngineConfig().devotional_pipeline == "auto"
