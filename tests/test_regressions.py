import json
from pathlib import Path

from devotional_engine.evaluator import EVALUATOR_SCORE_FIELDS, run_beauty_pass, validate_evaluation
from devotional_engine.engine import route_after_failure
from devotional_engine.harness import chapter_arc_gate, check_stanza_count, run_deterministic_harness
from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter, run_engine
from devotional_engine.renderer import render_artifact, validate_artifact_structure
from devotional_engine.states import State


def _psalm19_outputs():
    path = Path(__file__).parents[1] / "examples" / "psalm19_mock_outputs.json"
    return json.loads(path.read_text())

def test_generic_opening_detected(context):
    context.prose["introduction"] = "There is a kind of sorrow."
    assert run_beauty_pass(context)["mechanical_residue"]

def test_arc_detachment_rejected(context):
    context.brief["central_thought"] = "unrelated stones vanish"
    assert chapter_arc_gate(context)

def test_six_stanzas_not_accepted(context):
    context.poem = "\n\n".join(context.poem.split("\n\n") + context.poem.split("\n\n")[:2])
    assert check_stanza_count(context, EngineConfig(poem_form="common_meter"))[0]

def test_both_not_routed_to_poet(): assert route_after_failure(["[BOTH] defect"]) is State.COMPOSE_PROSE

def test_italics_preserved(context):
    context.prose["reflection"] = "Keep *meaningful emphasis* intact."
    assert "*meaningful emphasis*" in render_artifact(context)

def test_unvalidated_prose_cannot_render(context):
    del context.prose["title"]
    try: render_artifact(context)
    except KeyError: pass
    else: raise AssertionError("unvalidated prose rendered")


def test_repeated_poem_stanzas_fail_harness(context):
    first = context.poem.split("\n\n")[0]
    context.poem = "\n\n".join([first] * 4)
    failures, _ = run_deterministic_harness(context)
    assert any("D11" in failure for failure in failures)


def test_empty_source_cannot_reach_done():
    outputs = _psalm19_outputs()
    outputs["source_agent"] = {}
    outputs["translator"] = {}
    ctx = run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(outputs))
    assert ctx.trace[-1] is State.ESCALATED
    assert any("[SOURCE]" in failure for failure in ctx.failed_checks)


def test_voice_review_loop_terminates():
    outputs = _psalm19_outputs()
    outputs["voice_keeper"] = {"approved": False}
    ctx = run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(outputs))
    assert ctx.trace[-1] is State.ESCALATED
    assert any("[VOICE]" in failure for failure in ctx.failed_checks)


def test_checker_loop_respects_configured_limit():
    outputs = _psalm19_outputs()
    outputs["composer"]["prayer"] = "Lord God, amen."
    ctx = run_engine(
        EngineContext(chapter_ref="Psalm 19"),
        MockAgentAdapter(outputs),
        EngineConfig(max_checker_loops=0),
    )
    assert ctx.trace[-1] is State.ESCALATED
    assert ctx.checker_loops == 1
    assert any("D8" in failure for failure in ctx.failed_checks)


def test_gate_loop_respects_configured_limit():
    outputs = _psalm19_outputs()
    outputs["director"]["selected_threshold_phrase"] = "Sometimes life feels hard."
    ctx = run_engine(
        EngineContext(chapter_ref="Psalm 19"),
        MockAgentAdapter(outputs),
        EngineConfig(max_gate_revisions=0),
    )
    assert ctx.trace[-1] is State.ESCALATED
    assert ctx.gate_revisions == 1
    assert any("V4" in failure for failure in ctx.failed_checks)


def test_beauty_loop_terminates():
    outputs = _psalm19_outputs()
    outputs["beauty_pass_agent"]["beauty_score"] = 5
    ctx = run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(outputs))
    assert ctx.trace[-1] is State.ESCALATED
    assert any("beauty" in failure for failure in ctx.failed_checks)


def test_contradiction_revision_loop_terminates():
    outputs = _psalm19_outputs()
    outputs["contradiction_editor"] = {"verdict": "Pass with revisions", "required_revisions": ["[PROSE] revise"]}
    ctx = run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(outputs))
    assert ctx.trace[-1] is State.ESCALATED
    assert any("contradiction" in failure for failure in ctx.failed_checks)


def test_mechanical_residue_cannot_be_overridden_by_model(context):
    context.prose["introduction"] = "Sometimes the heart explains itself."
    result = run_beauty_pass(context, {"beauty_score": 9, "mechanical_residue": []})
    assert result["beauty_score"] < 8
    assert result["mechanical_residue"]


def test_strict_beauty_warning_caps_model_score(context):
    result = run_beauty_pass(
        context,
        {"beauty_score": 9, "mechanical_residue": []},
        ["D24 unnecessary adverbs: literally"],
        EngineConfig(strict_beauty_warnings=True),
    )
    assert result["beauty_score"] < 8
    assert result["fault_target"] == "prose"
    assert any("D24" in revision for revision in result["required_beauty_revisions"])


def test_strict_explanatory_poem_warning_routes_to_poet(context):
    result = run_beauty_pass(
        context,
        {"beauty_score": 9, "mechanical_residue": [], "fault_target": "none"},
        ["D26 explanatory poem language detected"],
        EngineConfig(strict_beauty_warnings=True),
    )
    assert result["beauty_score"] < 8
    assert result["fault_target"] == "poem"


def test_strict_image_physics_warning_routes_to_both(context):
    result = run_beauty_pass(
        context,
        {"beauty_score": 9, "mechanical_residue": []},
        ["D25 image physics issue: abstract cleverness displaces concrete poetic image"],
        EngineConfig(strict_beauty_warnings=True),
    )
    assert result["beauty_score"] < 8
    assert result["fault_target"] == "both"


def test_strict_grounded_qualia_warning_caps_model_score(context):
    result = run_beauty_pass(
        context,
        {"beauty_score": 9, "mechanical_residue": []},
        ["D27 grounded qualia weak: use embodied detail"],
        EngineConfig(strict_beauty_warnings=True),
    )
    assert result["beauty_score"] < 8
    assert result["fault_target"] == "both"
    assert any("D27" in revision for revision in result["required_beauty_revisions"])


def test_duplicate_artifact_heading_rejected(context):
    artifact = render_artifact(context) + "\n## Prayer\n\nDuplicate\n"
    assert not validate_artifact_structure(artifact)


def test_missing_christology_anchor_fails(context):
    context.brief["christology_required_echoes"] = ["anointed", "nations"]
    context.prose["christ_fulfillment"] = "Christ rises."
    failures, _ = run_deterministic_harness(context)
    assert any("D12a" in failure for failure in failures)


def test_unverified_long_quote_fails(context):
    context.source_text = "The Lord is my rock."
    context.working_rendering = "The Lord is my rock."
    context.prose["reflection"] = "David says, “This sentence is not in the source.”"
    failures, _ = run_deterministic_harness(context)
    assert any("D9" in failure for failure in failures)


def test_historical_metaphor_collision_rejected(context):
    context.prose["christ_fulfillment"] = "On the cross, the bulls gored Christ and the wild dogs tore His flesh."
    failures, _ = run_deterministic_harness(context)
    assert any("D20" in failure for failure in failures)


def test_historical_metaphor_distinction_allowed(context):
    context.prose["christ_fulfillment"] = (
        "Jesus Christ was physically nailed to Roman wood, while spiritually He stepped into "
        "the center of the roaring beasts."
    )
    failures, _ = run_deterministic_harness(context)
    assert not any("D20" in failure for failure in failures)


def test_invalid_evaluator_output_fails_closed():
    result = {key: 9 for key in EVALUATOR_SCORE_FIELDS}
    result["fault_target"] = "mystery"
    assert validate_evaluation(result)
