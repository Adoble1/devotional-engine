import pytest
from devotional_engine.renderer import HEADINGS, render_artifact, render_flow_artifact, validate_artifact_structure

def test_renders_headings_in_order(context):
    artifact = render_artifact(context)
    assert validate_artifact_structure(artifact)
    assert [artifact.index(h) for h in HEADINGS] == sorted(artifact.index(h) for h in HEADINGS)

def test_missing_epigraph_fails(context):
    del context.prose["epigraph"]
    with pytest.raises(KeyError): render_artifact(context)

def test_renderer_uses_structured_fields_not_loose_body(context):
    context.prose["body"] = "LOOSE BODY"
    assert "LOOSE BODY" not in render_artifact(context)


def test_flow_renderer_places_full_verses_after_opening_without_headings(context):
    context.prose["focus_bible_verses"] = (
        "Psalm 18:1-3 — I love You, LORD, my strength. The LORD is my rock, "
        "my fortress, and my rescuer; my God is my rock where I take refuge, "
        "my shield, the horn of my salvation, and my high place. I call upon "
        "the LORD, who is worthy of praise, and I am saved from my enemies."
    )
    artifact = render_flow_artifact(context)
    assert "## " not in artifact
    assert artifact.index("Love speaks before thunder.") < artifact.index("Psalm 18:1-3")
    assert artifact.index("Psalm 18:1-3") < artifact.index("The Lord comes to rescue.")
    assert artifact.count("Love speaks before thunder.") == 1


def test_flow_renderer_suppresses_title_opening_duplicate(context):
    context.prose["title"] = "Love Speaks Before Thunder"
    context.prose["epigraph"] = "Love speaks before thunder."
    artifact = render_flow_artifact(context)
    assert artifact.count("Love Speaks Before Thunder") == 1
    assert "Love speaks before thunder.\n\nLove speaks before thunder." not in artifact
