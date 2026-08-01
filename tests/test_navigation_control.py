from types import SimpleNamespace

import pytest

from devotional_engine.navigation import (
    CheckpointStatus,
    NavigationContractError,
    NavigationControlAdapter,
    NavigationState,
    finalize_navigation_state,
    validate_uncertainty_register,
)
from devotional_engine.states import State


class RealAdapter:
    def __init__(self, outputs):
        self.outputs = outputs
        self.payloads = {}

    def call(self, role, payload):
        self.payloads[role] = payload
        output = self.outputs[role]
        return output(payload) if callable(output) else output


class MockAgentAdapter:
    def __init__(self, outputs):
        self.outputs = outputs
        self.payloads = {}

    def call(self, role, payload):
        self.payloads[role] = payload
        output = self.outputs[role]
        return output(payload) if callable(output) else output


def config(**overrides):
    values = {
        "navigation_require_uncertainty_register": True,
        "navigation_min_objective_score": 0.85,
        "navigation_hard_floor": 0.80,
        "enforce_navigation_control": True,
        "navigation_objective_weights": {
            "truth": 0.35,
            "alignment": 0.20,
            "literary": 0.15,
            "safety": 0.20,
            "provenance": 0.10,
        },
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def ctx():
    return SimpleNamespace(
        chapter_ref="Psalm 52",
        navigation_state=None,
        checkpoint_log=[],
        uncertainty_register=[],
        objective_scores={},
    )


def grounding():
    return {
        "textual_evidence": [
            {"id": "E1", "reference": "Psalm 52:1-4", "claim": "Speech destroys."},
            {"id": "E2", "reference": "Psalm 52:5", "claim": "God uproots false refuge."},
        ],
        "uncertainty_register": [
            {
                "field": "governing_claim",
                "claim": "Steadfast love outlasts destructive power.",
                "status": "verified",
                "evidence_ids": ["E1", "E2"],
            },
            {
                "field": "textual_hinge",
                "claim": "God uproots false refuge.",
                "status": "verified",
                "evidence_ids": ["E2"],
            },
            {
                "field": "divine_action",
                "claim": "God judges false refuge.",
                "status": "verified",
                "evidence_ids": ["E2"],
            },
            {
                "field": "christological_fulfillment",
                "claim": "Christ bears false accusation and rises.",
                "status": "strong_inference",
                "source_refs": ["1 Peter 2:22-24"],
            },
        ],
    }


def test_real_adapter_receives_route_contract_and_records_route():
    adapter = RealAdapter(
        {
            "devotional_grounder": grounding(),
            "devotional_planner": {"plan": True},
            "devotional_composer": {"draft": True},
            "devotional_reviewer": {"verdict": "Pass"},
        }
    )
    context = ctx()
    controlled = NavigationControlAdapter(adapter, context, config())
    controlled.call("devotional_grounder", {"chapter_ref": "Psalm 52"})
    controlled.call("devotional_planner", {"grounding": {}})
    controlled.call("devotional_composer", {"revision": 0})
    controlled.call("devotional_reviewer", {"draft": {}})

    assert "navigation_contract" in adapter.payloads["devotional_grounder"]
    assert context.navigation_state.checkpoints["review"].status is CheckpointStatus.PASSED
    assert len(context.uncertainty_register) == 4
    assert context.navigation_state.expected_roles == ("devotional_composer",)


def test_mock_payload_shape_is_not_changed():
    adapter = MockAgentAdapter({"devotional_grounder": {"textual_evidence": []}})
    controlled = NavigationControlAdapter(adapter, ctx(), config())
    controlled.call("devotional_grounder", {"chapter_ref": "Psalm 52"})
    assert set(adapter.payloads["devotional_grounder"]) == {"chapter_ref"}


def test_out_of_order_call_is_rejected():
    controlled = NavigationControlAdapter(
        RealAdapter({"devotional_planner": {}}),
        ctx(),
        config(navigation_require_uncertainty_register=False),
    )
    with pytest.raises(NavigationContractError):
        controlled.call("devotional_planner", {})


def test_uncertainty_register_rejects_unsupported_protected_claim():
    packet = grounding()
    packet["uncertainty_register"][0]["status"] = "unsupported"
    packet["uncertainty_register"][0]["rationale"] = "No adequate warrant."
    _, findings = validate_uncertainty_register(packet, required=True)
    assert any("cannot advance" in finding for finding in findings)


def test_final_objective_gate_escalates_low_truth_score():
    context = SimpleNamespace(
        chapter_ref="Psalm 52",
        trace=[State.DONE],
        integrated_review={
            "dimensions": {
                "textual_fidelity": 5,
                "theological_accuracy": 5,
                "canonical_warrant": 5,
                "blueprint_alignment": 9,
                "literary_quality": 9,
            }
        },
        failed_checks=[],
        error="",
        scripture_provenance={"focus": {"quotation_mode": "licensed"}},
        artifact="devotional",
        navigation_state=NavigationState("mission"),
        checkpoint_log=[],
        uncertainty_register=[],
        objective_scores={},
    )
    finalize_navigation_state(context, config())
    assert context.trace[-1] is State.ESCALATED
    assert context.navigation_state.checkpoints["validation"].status is CheckpointStatus.FAILED
    assert any("truth" in item.lower() for item in context.failed_checks)


def test_final_objective_gate_passes_strong_result():
    context = SimpleNamespace(
        chapter_ref="Psalm 52",
        trace=[State.DONE],
        integrated_review={
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
            }
        },
        failed_checks=[],
        error="",
        scripture_provenance={"focus": {"quotation_mode": "licensed"}},
        artifact="devotional",
        navigation_state=NavigationState("mission"),
        checkpoint_log=[],
        uncertainty_register=[],
        objective_scores={},
    )
    finalize_navigation_state(context, config())
    assert context.trace[-1] is State.DONE
    assert context.navigation_state.checkpoints["emission"].status is CheckpointStatus.PASSED
    assert context.objective_scores["aggregate"] >= 0.85
