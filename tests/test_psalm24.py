import json
from pathlib import Path

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter, State, render_flow_artifact, run_engine
from devotional_engine.harness import run_deterministic_harness


def _outputs():
    path = Path(__file__).parents[1] / "examples" / "psalm24_mock_outputs.json"
    return json.loads(path.read_text())


def _strict_config():
    return EngineConfig(
        require_full_focus_verses=True,
        require_key_verse_selection=True,
        enforce_same_chapter_reference_style=True,
        warn_unnecessary_adverbs=True,
        warn_image_physics=True,
        warn_explanatory_poem=True,
        warn_grounded_qualia=True,
        warn_poem_music=True,
        strict_beauty_warnings=True,
    )


def test_psalm24_state_machine_reaches_done():
    context = run_engine(EngineContext(chapter_ref="Psalm 24"), MockAgentAdapter(_outputs()))
    assert context.trace[-1] is State.DONE
    assert context.artifact.startswith("# The Gates Remember")
    assert context.ledger["entries"][-1]["chapter"] == "Psalm 24"
    assert context.failed_checks == []


def test_psalm24_strict_flow_passes_truth_and_beauty_checks():
    config = _strict_config()
    context = run_engine(EngineContext(chapter_ref="Psalm 24"), MockAgentAdapter(_outputs()), config)
    failures, warnings = run_deterministic_harness(context, config)
    artifact = render_flow_artifact(context)

    assert context.trace[-1] is State.DONE
    assert failures == []
    assert not any(warning.startswith(("D24", "D25", "D26", "D27", "D28")) for warning in warnings)
    assert "Psalm 24:3-5, 7-8" in artifact
    assert "Psalm 24:1-10" not in artifact
    assert "The psalm begins wider" in artifact
    assert "Psalm 24 begins" not in artifact
    assert artifact.count("The Gates Remember") == 1
    assert "Again the cry moves through the stone" in artifact
    assert "and the whole house opens." in artifact


def test_psalm24_preserves_holiness_and_saving_vindication():
    context = run_engine(EngineContext(chapter_ref="Psalm 24"), MockAgentAdapter(_outputs()), _strict_config())
    combined = " ".join(
        [
            context.prose["reflection"],
            context.prose["christ_fulfillment"],
            context.prose["application"],
        ]
    )
    assert "vindication comes from the God who saves" in combined
    assert "Jesus Christ alone comes with wholly clean hands" in combined
    assert "self-salvation" not in combined
