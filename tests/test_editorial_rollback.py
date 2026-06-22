from devotional_engine.agents import MockAgentAdapter
from devotional_engine.engine import apply_editorial_smoothing

def test_rolls_back_invalid_edit(context):
    original = context.prose.copy()
    adapter = MockAgentAdapter({"editorial_smoother": {"prose": {"prayer": "Lord God, amen.", "poem": "changed", "focus_bible_verses": "changed"}}})
    assert not apply_editorial_smoothing(context, adapter)
    assert context.prose == original
    assert "EDITORIAL_ROLLBACK: deterministic failure" in context.warnings

def test_editor_cannot_change_immutable_fields(context):
    poem = context.poem; verses = context.prose["focus_bible_verses"]
    adapter = MockAgentAdapter({"editorial_smoother": {"prose": {"reflection": "Smoothed.", "poem": "changed", "focus_bible_verses": "changed", "christ_fulfillment": "changed"}}})
    assert apply_editorial_smoothing(context, adapter)
    assert context.poem == poem and context.prose["focus_bible_verses"] == verses
    assert context.prose["christ_fulfillment"] == "Christ enters death and rises."
