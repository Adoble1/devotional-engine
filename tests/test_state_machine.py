import json
from pathlib import Path
from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def test_psalm18_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm18_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 18"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# Love Before Thunder")
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 18"


def test_psalm19_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm19_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# The Speech of Heaven")
    assert "Creation speaks without a sound." in ctx.artifact
    assert ctx.failed_checks == []
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 19"


def test_psalm20_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm20_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 20"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# The Naked Trust")
    assert "Trouble teaches the true name." in ctx.artifact
    assert "The iron breaks beneath the weight" in ctx.artifact
    assert ctx.failed_checks == []
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 20"


def test_psalm21_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm21_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 21"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# The Crown Is Mercy")
    assert "The crown is mercy." in ctx.artifact
    assert "We will sing until the crown becomes praise." in ctx.artifact
    assert ctx.failed_checks == []
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 21"


def test_psalm22_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm22_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 22"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# The Circle Opens")
    assert "The circle opens into song." in ctx.artifact
    assert "Anchor our chests to the reality" in ctx.artifact
    assert ctx.failed_checks == []
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 22"


def test_psalm23_state_machine_reaches_done():
    path = Path(__file__).parents[1] / "examples" / "psalm23_mock_outputs.json"
    ctx = run_engine(EngineContext(chapter_ref="Psalm 23"), MockAgentAdapter(json.loads(path.read_text())))
    assert ctx.trace[-1] is State.DONE
    assert ctx.artifact.startswith("# Mercy Learns the Road")
    assert "Mercy learns the road." in ctx.artifact
    assert "Jesus Christ is the Shepherd" in ctx.artifact
    assert ctx.failed_checks == []
    assert ctx.ledger["entries"][-1]["chapter"] == "Psalm 23"
