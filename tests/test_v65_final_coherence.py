from devotional_engine import EngineConfig, EngineContext, State
from devotional_engine.v65 import _record_final_coherence


def test_final_coherence_rejects_post_edit_title_opening_drift() -> None:
    ctx = EngineContext(chapter_ref="Psalm 50")
    ctx.brief = {"passage_center_map": {"governing_terms": ["worship", "obedience"]}}
    ctx.prose = {
        "title": "Thanksgiving Over Ritual",
        "epigraph": "God examines the life behind the offering.",
        "introduction": "Thanksgiving Over Ritual. God summons His covenant people.",
        "reflection": "True worship joins gratitude and obedience.",
        "christ_fulfillment": "Christ offers Himself once for all.",
        "application": "Let the life agree with the worship offered.",
        "prayer": "Father, form truthful worship through Jesus Christ our Lord. Amen.",
    }
    ctx.trace = [State.DONE]

    _record_final_coherence(
        ctx,
        EngineConfig(enforce_title_opening_distinction=True),
    )

    assert ctx.trace[-1] is State.ESCALATED
    assert any("COHERENCE C10" in failure for failure in ctx.failed_checks)
    assert "final devotional coherence failed" in ctx.error


def test_final_coherence_deduplicates_advisory_warnings() -> None:
    ctx = EngineContext(chapter_ref="Psalm 50")
    ctx.brief = {
        "passage_center_map": {
            "governing_terms": ["worship", "obedience"],
            "supporting_terms": [],
        }
    }
    repeated = "The life behind the offering must come into the light before God."
    ctx.prose = {
        "title": "Thanksgiving Over Ritual",
        "epigraph": "God examines the life behind the offering.",
        "introduction": "God summons His covenant people.",
        "reflection": repeated,
        "christ_fulfillment": repeated,
        "application": "Receive correction and walk in obedience.",
        "prayer": "Father, form truthful worship through Jesus Christ our Lord. Amen.",
    }
    ctx.trace = [State.DONE]

    _record_final_coherence(ctx, EngineConfig())
    _record_final_coherence(ctx, EngineConfig())

    repeated_warnings = [warning for warning in ctx.warnings if "COHERENCE C12" in warning]
    assert len(repeated_warnings) == 1
    assert ctx.trace[-1] is State.DONE
