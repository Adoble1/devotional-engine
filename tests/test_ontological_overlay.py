from copy import deepcopy

import pytest

from devotional_engine import EngineConfig, EngineContext
from devotional_engine.exceptions import ValidationError
from devotional_engine.ontology import (
    ONTOLOGY_REVIEW_DIMENSIONS,
    OntologicalOverlayAdapter,
    audit_ontology_surface,
    build_ontological_overlay,
    public_domain_source_catalog,
    validate_ontological_overlay,
)


def _grounding() -> dict:
    return {
        "historical_meaning": "A threatened singer moves from fear to trust because God remembers and preserves him.",
        "literary_mode": "individual lament and trust psalm",
        "textual_evidence": [
            {"id": "E1", "reference": "Psalm 56:3-4", "claim": "Fear is answered by trust in God's word."},
            {"id": "E2", "reference": "Psalm 56:8-13", "claim": "God remembers tears and keeps the faithful from falling."},
        ],
        "governing_claim": "God's remembered care turns fear toward trusting obedience.",
        "textual_hinge": "The threatened singer knows that God is for him.",
        "divine_action": "God remembers tears, answers prayer, and preserves life.",
        "reader_felt_experience": "Fear narrows the future until threat appears to govern every step.",
        "physical_vocabulary": ["tear", "skin-bottle", "step", "fall", "light"],
    }


def _plan() -> dict:
    return {
        "reader_transformation": {
            "initial_assumption": "Fear has the final word.",
            "new_perception": "God remembers and preserves the fearful person.",
            "faithful_response": "Trust God's word and take the next faithful step.",
        },
        "ontological_overlay": {
            "nodes": [
                {
                    "id": "god",
                    "kind": "divine",
                    "name": "God",
                    "truth": "The sovereign keeper who remembers tears and preserves life.",
                    "warrant_ids": ["E2"],
                },
                {
                    "id": "speaker",
                    "kind": "human",
                    "name": "the threatened singer",
                    "truth": "A dependent creature who fears and learns trust.",
                    "warrant_ids": ["E1", "E2"],
                },
            ],
            "relations": [
                {
                    "source": "god",
                    "relation": "remembers and preserves",
                    "target": "speaker",
                    "warrant_ids": ["E2"],
                },
                {
                    "source": "speaker",
                    "relation": "trusts and praises",
                    "target": "god",
                    "warrant_ids": ["E1"],
                },
            ],
            "order": {
                "true_order": "God governs; the singer depends upon His word.",
                "disorder": "Fear treats mortal threat as final authority.",
                "divine_action": "God remembers, answers, and keeps the singer's feet.",
                "restored_posture": "The singer trusts and walks before God.",
            },
            "affective_path": {
                "pressure": "Fear closes around the singer.",
                "embodied_evidence": ["tear", "wandering feet", "falling"],
                "turn": "God has counted every wandering and remembered every tear.",
                "settled_posture": "Trust walks forward in the light of life.",
            },
            "diction": {
                "period_end_year": 1949,
                "source_document_ids": [
                    "macdonald_unspoken_sermons_1867",
                    "stevenson_vailima_prayers_1916",
                ],
                "selected_vocabulary": ["trust", "sorrow", "courage", "rest", "mercy"],
            },
        },
    }


def test_catalog_is_public_domain_and_before_1950() -> None:
    catalog = public_domain_source_catalog(1949)
    assert catalog
    assert all(item["publication_year"] <= 1930 for item in catalog)
    assert all("public domain in the USA" in item["public_domain_basis"] for item in catalog)


def test_explicit_overlay_validates_against_grounding() -> None:
    overlay = build_ontological_overlay(_plan(), _grounding())
    findings = validate_ontological_overlay(
        overlay,
        evidence_ids={"E1", "E2"},
        required=True,
    )
    assert findings == []
    assert overlay["order"]["divine_action"].startswith("God remembers")
    assert overlay["diction"]["selected_vocabulary"] == [
        "trust", "sorrow", "courage", "rest", "mercy"
    ]


def test_overlay_rejects_unknown_sources_and_unattested_vocabulary() -> None:
    plan = deepcopy(_plan())
    plan["ontological_overlay"]["diction"]["source_document_ids"] = [
        "unknown_postwar_source",
        "stevenson_vailima_prayers_1916",
    ]
    plan["ontological_overlay"]["diction"]["selected_vocabulary"] = ["bandwidth"]
    overlay = build_ontological_overlay(plan, _grounding())
    codes = {
        item.code
        for item in validate_ontological_overlay(
            overlay,
            evidence_ids={"E1", "E2"},
            required=True,
        )
    }
    assert {"O08", "O09"}.issubset(codes)


def test_surface_audit_blocks_kjv_language_and_postwar_jargon() -> None:
    overlay = build_ontological_overlay(_plan(), _grounding())
    findings = audit_ontology_surface(
        {
            "reflection": "Thou art near when I feel triggered. Thy mercy creates a safe space.",
            "poem": "",
        },
        overlay,
        enforce=True,
    )
    codes = {item.code for item in findings}
    assert "O10" in codes
    assert "O11" in codes


class RecordingAdapter:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, role: str, payload: dict):
        self.calls.append((role, payload))
        if role == "devotional_planner":
            return _plan()
        if role == "devotional_composer":
            return {
                "title": "Remembered Tears",
                "epigraph": "Fear rises; remembered mercy steadies the step.",
                "focus_bible_verses": "Psalm 56",
                "introduction": "A tear falls before courage returns.",
                "reflection": "God remembers sorrow and teaches trust.",
                "christ_fulfillment": "Christ enters fear and brings life.",
                "application": "Take the next faithful step.",
                "prayer": "God of mercy, give us courage and rest.",
                "poem": "One tear\nheld in mercy.",
                "next_in_sequence": "Psalm 57",
            }
        if role == "devotional_reviewer":
            return {
                "verdict": "Pass",
                "hard_findings": [],
                "advisory_findings": [],
                "dimensions": {name: 9 for name in ONTOLOGY_REVIEW_DIMENSIONS},
            }
        raise AssertionError(role)


def test_adapter_injects_overlay_without_source_prose() -> None:
    delegate = RecordingAdapter()
    adapter = OntologicalOverlayAdapter(delegate, EngineConfig())
    ctx = EngineContext(chapter_ref="Psalm 56")
    plan = adapter.call(
        "devotional_planner",
        {"grounding": _grounding(), "context": ctx, "planning_instruction": "Plan."},
    )
    assert plan["ontological_overlay"]["origin"] == "supplied"
    assert ctx.ontological_overlay["nodes"][0]["id"] == "god"

    adapter.call(
        "devotional_composer",
        {"composition_packet": {"economy": {"principles": []}}},
    )
    payload = delegate.calls[-1][1]["composition_packet"]["ontological_overlay"]
    assert payload["diction"]["selected_vocabulary"]
    assert "available_vocabulary" not in payload["diction"]
    assert all("vocabulary" not in source for source in payload["diction"]["source_documents"])


def test_production_review_requires_ontology_dimensions() -> None:
    delegate = RecordingAdapter()
    adapter = OntologicalOverlayAdapter(delegate, EngineConfig())
    adapter.call(
        "devotional_planner",
        {"grounding": _grounding(), "context": EngineContext(chapter_ref="Psalm 56")},
    )

    class MissingDimensionsAdapter(RecordingAdapter):
        def call(self, role: str, payload: dict):
            if role == "devotional_reviewer":
                return {
                    "verdict": "Pass",
                    "hard_findings": [],
                    "advisory_findings": [],
                    "dimensions": {},
                }
            return super().call(role, payload)

    missing = MissingDimensionsAdapter()
    wrapper = OntologicalOverlayAdapter(missing, EngineConfig())
    wrapper.overlay = adapter.overlay
    review = wrapper.call(
        "devotional_reviewer",
        {"protected": {}, "review_instruction": "Review.", "revision": 1},
    )
    assert review["verdict"] == "Fail"
    assert {item["field"] for item in review["hard_findings"]} == {
        f"dimensions.{name}" for name in ONTOLOGY_REVIEW_DIMENSIONS
    }


def test_production_planner_fails_closed_without_overlay() -> None:
    class EmptyPlanner:
        def call(self, role: str, payload: dict):
            return {"reader_transformation": {}}

    adapter = OntologicalOverlayAdapter(EmptyPlanner(), EngineConfig())
    with pytest.raises(ValidationError):
        adapter.call(
            "devotional_planner",
            {"grounding": _grounding(), "context": EngineContext(chapter_ref="Psalm 56")},
        )
