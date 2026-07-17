import pytest

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter
from devotional_engine.exceptions import ValidationError
from devotional_engine.renderer import render_artifact
from devotional_engine.scripture import (
    ScriptureProvenanceAdapter,
    validate_provenance_record,
    validate_scripture_context,
)


def test_public_domain_source_requires_named_verified_edition() -> None:
    valid = {
        "quotation_mode": "public_domain",
        "translation_id": "WEB",
        "edition": "World English Bible",
        "attribution": "World English Bible (Public Domain)",
        "verified_exact_match": True,
        "human_review_required": False,
    }
    assert validate_provenance_record(valid) == []

    invalid = dict(valid, edition="", verified_exact_match=False)
    failures = validate_provenance_record(invalid)
    assert any("edition" in item for item in failures)
    assert any("verified_exact_match" in item for item in failures)


def test_licensed_source_requires_license_profile() -> None:
    failures = validate_provenance_record(
        {
            "quotation_mode": "licensed",
            "translation_id": "Example Translation",
            "edition": "2026 edition",
            "attribution": "Example Translation",
            "verified_exact_match": True,
        }
    )
    assert failures == ["licensed Scripture requires license_profile."]


def test_independent_rendering_records_source_and_human_review() -> None:
    valid = {
        "quotation_mode": "independent_rendering",
        "source_text_id": "Masoretic Text / Psalm 52",
        "attribution": "Independent rendering from the Hebrew",
        "verified_exact_match": False,
        "human_review_required": True,
    }
    assert validate_provenance_record(valid) == []


def test_test_fixture_cannot_pass_as_publication_source() -> None:
    fixture = {
        "quotation_mode": "test_fixture",
        "attribution": "Deterministic fixture; not for publication",
        "human_review_required": True,
    }
    assert validate_provenance_record(fixture, allow_test_fixture=True) == []
    assert "forbidden for production adapters" in validate_provenance_record(fixture)[0]


def test_real_adapter_fails_closed_when_provenance_is_missing() -> None:
    class RealAdapter:
        def call(self, role, payload):
            if role == "source_agent":
                return {"source_text": "A sufficiently long Scripture source text."}
            return {"working_rendering": "A sufficiently long rendering."}

    adapter = ScriptureProvenanceAdapter(RealAdapter(), EngineConfig())
    with pytest.raises(ValidationError, match="Scripture provenance invalid"):
        adapter.call("source_agent", {"context": EngineContext(chapter_ref="Psalm 52")})


def test_mock_fixture_is_labeled_and_rendered_as_non_publication() -> None:
    ctx = EngineContext(chapter_ref="Psalm 52")
    adapter = ScriptureProvenanceAdapter(
        MockAgentAdapter(
            {
                "source_agent": {"source_text": "A sufficiently long mock source text."},
                "translator": {"working_rendering": "A sufficiently long mock rendering."},
            }
        ),
        EngineConfig(),
    )

    adapter.call("source_agent", {"context": ctx})
    adapter.call("translator", {"context": ctx})

    assert validate_scripture_context(ctx) == []
    assert ctx.scripture_provenance["focus"]["quotation_mode"] == "test_fixture"

    ctx.prose = {
        "title": "The Rooted Tree",
        "epigraph": "Boasting falls; steadfast love remains.",
        "focus_bible_verses": "Psalm 52:8 — I am like a green olive tree in the house of God.",
        "introduction": "The boast is loud.",
        "reflection": "God uproots destructive falsehood and preserves those who trust His steadfast love.",
        "christ_fulfillment": "Christ is the faithful King whose truthful word gives life.",
        "application": "Trust the steadfast love of God rather than the power of harm.",
        "prayer": "Father, root us in Your steadfast love through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 53",
    }
    ctx.poem = "The boast will fall.\nThe rooted tree remains."

    artifact = render_artifact(ctx)
    assert "Scripture source: Deterministic mock Scripture fixture; not for publication." in artifact
