from copy import deepcopy

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter, State, run_engine
from devotional_engine.integrated import adapter_supports_integrated_devotional


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
        "physical_vocabulary": ["tongue", "razor", "tent", "root", "olive tree", "house"],
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
        "unsupported_claims": ["Do not invent Doeg's private emotions or David's location while composing the psalm."],
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
            "introduction": "Enter through the speed and consequence of the tongue.",
            "reflection": "Trace destructive speech to its false refuge and divine uprooting.",
            "christ_fulfillment": "Show the truthful King bearing accusation and rising beyond its verdict.",
            "application": "Test the purpose, context, and desired effect of one's speech.",
            "prayer": "Ask for rooted trust and speech governed by covenant love.",
            "poem": "Move from the razor and shallow root to the living olive tree.",
        },
        "art_direction": {
            "register": "compressed moral clarity with organic imagery",
            "pace": "quick opening, patient contrast, quiet rooted ending",
            "image_lexicon": ["razor", "root", "tent", "olive tree", "house"],
            "threshold_phrase": "Destruction cannot make deep roots.",
        },
        "governing_image": "a green olive tree remaining where a violent refuge is uprooted",
        "poem_arc": ["cutting word", "shallow root", "divine uprooting", "olive tree", "truthful praise"],
        "supporting_elements": ["wealth and influence function as false refuges"],
        "local_constraints": [
            "do not invent motives for Doeg",
            "do not condemn necessary reporting of abuse or danger",
            "do not make speech rather than steadfast love the final subject",
        ],
    }


def _draft(application: str | None = None) -> dict:
    return {
        "title": "The Tree That Remains",
        "epigraph": "A razor can cut; it cannot take root.",
        "focus_bible_verses": (
            "Psalm 52:1, 5, 8-9 — Why do you boast in evil? God's steadfast love endures continually. "
            "God will uproot the false refuge, but I am like a flourishing olive tree in His house."
        ),
        "introduction": (
            "The tongue moves first. A report crosses a room, reaches power, and leaves other people "
            "to bear what the speaker set in motion."
        ),
        "reflection": (
            "Psalm 52 joins the sharpened tongue to a deeper trust. The destructive person makes wealth, "
            "influence, and successful harm into a refuge. Yet God's steadfast love endures continually. "
            "The hinge is divine uprooting: power that looked planted is pulled from its tent, while the "
            "faithful person remains like an olive tree in God's house. The final subject is not the razor. "
            "It is the covenant love that keeps life rooted and turns speech toward thanksgiving."
        ),
        "christ_fulfillment": (
            "The New Testament does not identify Psalm 52 as a direct prophecy of Christ. The correspondence "
            "is thematic. Jesus is the truthful King in whose mouth there is no deceit. False witnesses use "
            "words to secure His death, but the Father raises Him beyond their verdict. United to Him, His "
            "people learn to refuse manipulative speech and to remain rooted in God's love."
        ),
        "application": application or (
            "Speak truth without making destruction your refuge. Before repeating a fact, ask whether context "
            "has been preserved, whether protection requires disclosure, and whether your desired outcome is "
            "truth or injury. Report real danger plainly. Refuse the private pleasure of controlling another "
            "person's reputation."
        ),
        "prayer": (
            "Father, root us in Your steadfast love. Forgive the words we have used to control or injure. "
            "Give us courage to report real evil truthfully and without cruelty. Form our speech after Jesus, "
            "in whose mouth there was no deceit. Keep us grateful and faithful through Jesus Christ our Lord."
        ),
        "poem": (
            "A sharpened word may cross the room,\nAnd leave a wound behind;\nBut shallow roots cannot endure\nThe judgment truth will find.\n\n"
            "Within God's house the olive lives,\nIts leaves turned toward the light;\nSteadfast love holds every root,\nAnd teaches speech the right."
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
            "literary_quality": 9,
        },
    }


def test_integrated_runner_uses_four_roles_and_preserves_artistic_freedom() -> None:
    adapter = MockAgentAdapter(
        {
            "devotional_grounder": _grounding(),
            "devotional_planner": _plan(),
            "devotional_composer": _draft(),
            "devotional_reviewer": _review(
                advisory_findings=[
                    {"code": "A1", "field": "poem", "message": "Review final cadence aloud."}
                ]
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
    assert ctx.prose["title"] == "The Tree That Remains"
    assert "INTEGRATED A1" in "\n".join(ctx.warnings)
    assert "Integrated deterministic Scripture fixture" in ctx.artifact

    freedom = adapter.outputs["devotional_composer"]
    assert freedom["title"] == "The Tree That Remains"


def test_integrated_runner_allows_one_targeted_revision_without_replanning() -> None:
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
    assert "preserved" in ctx.prose["application"]


def test_old_mock_roles_use_legacy_compatibility_path() -> None:
    adapter = MockAgentAdapter({"source_agent": {"source_text": "fixture only"}})
    assert not adapter_supports_integrated_devotional(adapter)
    assert EngineConfig().devotional_pipeline == "auto"
