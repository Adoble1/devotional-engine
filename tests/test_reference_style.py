from devotional_engine import EngineConfig
from devotional_engine import EngineContext, MockAgentAdapter, State, render_flow_artifact, run_engine
from devotional_engine.harness import run_deterministic_harness
import json
from pathlib import Path


FULL_FOCUS = (
    "Psalm 18:1-3 — I love You, LORD, my strength. The LORD is my rock, "
    "my fortress, and my rescuer; my God is my rock where I take refuge, "
    "my shield, the horn of my salvation, and my high place. I call upon "
    "the LORD, who is worthy of praise, and I am saved from my enemies."
)


def test_repeated_same_chapter_reference_fails_when_enforced(context):
    context.prose["focus_bible_verses"] = FULL_FOCUS
    context.prose["introduction"] = "Love speaks before thunder.\n\nPsalm 18 begins with love."
    failures, _ = run_deterministic_harness(
        context,
        EngineConfig(enforce_same_chapter_reference_style=True, require_full_focus_verses=True),
    )
    assert any("D22" in failure for failure in failures)


def test_the_psalm_reference_passes_when_enforced(context):
    context.prose["focus_bible_verses"] = FULL_FOCUS
    context.prose["introduction"] = "Love speaks before thunder.\n\nThe psalm begins with love."
    failures, _ = run_deterministic_harness(
        context,
        EngineConfig(enforce_same_chapter_reference_style=True, require_full_focus_verses=True),
    )
    assert not any("D22" in failure for failure in failures)
    assert not any("D23" in failure for failure in failures)


def test_citation_only_focus_verses_fail_when_full_text_required(context):
    context.prose["focus_bible_verses"] = "Psalm 18:1-3"
    failures, _ = run_deterministic_harness(context, EngineConfig(require_full_focus_verses=True))
    assert any("D23" in failure for failure in failures)


def test_kjv_archaisms_fail_when_full_text_required(context):
    context.prose["focus_bible_verses"] = (
        "Psalm 18:1-3 — I will love thee, O LORD, my strength. The LORD is my "
        "rock and my fortress and my deliverer; my God, my strength, in whom "
        "I will trust; my buckler, and the horn of my salvation, and my high tower."
    )
    failures, _ = run_deterministic_harness(context, EngineConfig(require_full_focus_verses=True))
    assert any("KJV-style archaisms" in failure for failure in failures)


def test_whole_chapter_focus_fails_when_key_selection_required(context):
    context.source_layer["chapter_verse_count"] = 3
    context.prose["focus_bible_verses"] = FULL_FOCUS
    failures, _ = run_deterministic_harness(
        context,
        EngineConfig(require_full_focus_verses=True, require_key_verse_selection=True),
    )
    assert any("whole chapter" in failure for failure in failures)


def test_selected_key_verses_pass_when_key_selection_required(context):
    context.source_layer["chapter_verse_count"] = 50
    context.prose["focus_bible_verses"] = FULL_FOCUS
    failures, _ = run_deterministic_harness(
        context,
        EngineConfig(require_full_focus_verses=True, require_key_verse_selection=True),
    )
    assert not any("D23" in failure for failure in failures)


def test_key_verse_selection_fails_without_chapter_count(context):
    context.prose["focus_bible_verses"] = FULL_FOCUS
    failures, _ = run_deterministic_harness(context, EngineConfig(require_key_verse_selection=True))
    assert any("chapter verse count unavailable" in failure for failure in failures)


def test_unnecessary_adverbs_warn_when_enabled(context):
    context.prose["reflection"] = "The valley is literally dark, but the Shepherd is truly near."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_unnecessary_adverbs=True))
    assert any("D24" in warning and "literally" in warning for warning in warnings)


def test_image_physics_warns_on_false_poetic_illustration(context):
    context.poem = "Grass bends under the Shepherd's hand."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_image_physics=True))
    assert any("D25" in warning for warning in warnings)


def test_abstract_cleverness_warns_as_image_physics_issue(context):
    context.poem = "There the Shepherd is nearer than grammar."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_image_physics=True))
    assert any("abstract cleverness" in warning for warning in warnings)


def test_later_resurrection_language_does_not_silence_unrelated_physics_warning(context):
    context.prose["christ_fulfillment"] = "Christ rose from the dead."
    context.poem = "Grass bends under the Shepherd's hand."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_image_physics=True))
    assert any("D25" in warning for warning in warnings)


def test_source_miracle_context_allows_physics_exception(context):
    context.source_text = "The sea split before the people."
    context.poem = "Water quiets its silver tongue."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_image_physics=True))
    assert not any("D25" in warning for warning in warnings)


def test_explanatory_poem_language_warns_when_enabled(context):
    context.poem = "The flock breathes again,\nnot because the hills are harmless,\nbut because the path has a Keeper."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_explanatory_poem=True))
    assert any("D26" in warning for warning in warnings)


def test_grounded_qualia_warns_on_emotional_padding(context):
    context.source_text = "The shepherd leads by water, shadow, table, oil, cup, and house."
    context.working_rendering = context.source_text
    context.chapter_design_map["physical_vocabulary"] = ["water", "shadow", "table", "oil", "cup", "house"]
    context.prose["introduction"] = "The experience is aching, tender, lonely, sorrowful, beautiful, and deeply emotional."
    context.prose["reflection"] = "The soul feels anguish and longing in a wonderful comforting way."
    context.poem = "Aching sorrow gathers.\nTender longing stays.\nBeautiful grief answers.\nLonely wonder remains."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_grounded_qualia=True))
    assert any("D27" in warning for warning in warnings)


def test_grounded_qualia_passes_with_chapter_born_detail(context):
    context.source_text = "The shepherd leads by water, shadow, table, oil, cup, and house."
    context.working_rendering = context.source_text
    context.chapter_design_map["physical_vocabulary"] = ["water", "shadow", "table", "oil", "cup", "house"]
    context.prose["introduction"] = "The road lowers into shadow, but the staff stays near."
    context.prose["reflection"] = "Bread waits on the table, oil darkens the lifted head, and the cup brims."
    context.poem = "Still water holds the sky.\nThe table waits in shadow.\nOil darkens the head.\nThe cup keeps its brim."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_grounded_qualia=True))
    assert not any("D27" in warning for warning in warnings)


def test_psalm23_flow_uses_full_verses_and_same_chapter_style():
    path = Path(__file__).parents[1] / "examples" / "psalm23_mock_outputs.json"
    config = EngineConfig(
        require_full_focus_verses=True,
        enforce_same_chapter_reference_style=True,
        warn_unnecessary_adverbs=True,
        warn_image_physics=True,
        warn_explanatory_poem=True,
        warn_grounded_qualia=True,
    )
    context = run_engine(EngineContext(chapter_ref="Psalm 23"), MockAgentAdapter(json.loads(path.read_text())), config)
    assert context.trace[-1] is State.DONE
    artifact = render_flow_artifact(context)
    assert "## " not in artifact
    assert "Psalm 23:1-6" in artifact
    assert "The psalm does not begin" in artifact
    assert "Psalm 23 begins" not in artifact
    assert artifact.count("Mercy Learns the Road") == 1
    assert "Mercy learns the road.\n\nMercy learns the road." not in artifact
    assert "nearer than grammar" not in artifact
    assert "old grammar" not in artifact
    assert "Grass bends under the Shepherd's hand" not in artifact
    _, warnings = run_deterministic_harness(context, config)
    assert not any("D26" in warning for warning in warnings)
    assert not any("D27" in warning for warning in warnings)


def test_strict_beauty_warnings_stop_psalm23_explanatory_poem():
    path = Path(__file__).parents[1] / "examples" / "psalm23_mock_outputs.json"
    outputs = json.loads(path.read_text())
    outputs["poet"]["poem"] += "\nnot because the valley is harmless"
    context = run_engine(
        EngineContext(chapter_ref="Psalm 23"),
        MockAgentAdapter(outputs),
        EngineConfig(
            require_full_focus_verses=True,
            enforce_same_chapter_reference_style=True,
            warn_explanatory_poem=True,
            strict_beauty_warnings=True,
            max_beauty_loops=0,
        ),
    )
    assert context.trace[-1] is State.ESCALATED
    assert context.beauty_loops == 1
    assert any("D26" in revision for revision in context.scores["required_beauty_revisions"])
