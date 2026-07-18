from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .coherence import audit_prose
from .config import EngineConfig
from .exceptions import ValidationError
from .harness import run_deterministic_harness
from .integrated import (
    INTEGRATED_ROLES,
    PROSE_FIELDS,
    IntegratedFinding,
    _escalate,
    _is_mock,
    _list,
    _missing,
    _review_finding,
    _text,
    _warn,
    adapter_supports_integrated_devotional,
    validate_grounding,
)
from .ledger import update_ledger
from .literary import (
    LiteraryFinding,
    audit_literary_economy,
    build_poem_design,
    composition_packet,
    prune_local_constraints,
)
from .renderer import render_artifact
from .scripture import normalize_provenance_record, validate_scripture_context
from .states import State


PROSE_SECTIONS = ("introduction", "reflection", "christ_fulfillment", "application", "prayer")
TRUTH_REVIEW_DIMENSIONS = (
    "textual_fidelity",
    "theological_accuracy",
    "canonical_warrant",
    "blueprint_alignment",
)
LITERARY_REVIEW_DIMENSIONS = (
    "verbal_economy",
    "literary_quality",
    "poetic_integrity",
    "sensory_presence",
    "read_aloud_flow",
)
REVIEW_DIMENSIONS = (*TRUTH_REVIEW_DIMENSIONS, *LITERARY_REVIEW_DIMENSIONS)


@dataclass
class IntegratedPassageBlueprint:
    chapter_ref: str
    governing_question: str
    governing_subject: str
    human_predicament: str
    textual_hinge: str
    divine_answer: str
    canonical_fulfillment: str
    reader_transformation: dict[str, str]
    section_burdens: dict[str, str]
    art_direction: dict[str, Any]
    poem_design: dict[str, Any]
    supporting_elements: list[str]
    local_constraints: list[str]
    evidence_path: list[str]
    approved: bool = False

    @property
    def governing_image(self) -> str:
        images = self.poem_design.get("image_field", [])
        return _text(images[0]) if images else ""

    @property
    def poem_arc(self) -> list[str]:
        values = list(self.poem_design.get("image_field", []))
        turn = _text(self.poem_design.get("emotional_turn"))
        if turn:
            values.append(turn)
        return [_text(item) for item in values if _text(item)]


def build_blueprint(ctx: Any, grounding: Mapping[str, Any], plan: Mapping[str, Any]) -> IntegratedPassageBlueprint:
    transform = dict(plan.get("reader_transformation", {}))
    evidence_ids = [
        _text(item.get("id"))
        for item in _list(grounding.get("textual_evidence"))
        if isinstance(item, Mapping) and _text(item.get("id"))
    ]
    section_burdens = {
        key: _text(value)
        for key, value in dict(plan.get("section_burdens", {})).items()
        if key in PROSE_SECTIONS and _text(value)
    }
    return IntegratedPassageBlueprint(
        chapter_ref=ctx.chapter_ref,
        governing_question=_text(plan.get("governing_question")),
        governing_subject=_text(grounding.get("governing_claim")),
        human_predicament=_text(plan.get("human_predicament") or grounding.get("reader_felt_experience")),
        textual_hinge=_text(grounding.get("textual_hinge")),
        divine_answer=_text(grounding.get("divine_action")),
        canonical_fulfillment=_text(grounding.get("christological_fulfillment")),
        reader_transformation={
            "initial_assumption": _text(transform.get("initial_assumption") or transform.get("from")),
            "new_perception": _text(transform.get("new_perception") or transform.get("to")),
            "faithful_response": _text(transform.get("faithful_response") or transform.get("response")),
        },
        section_burdens=section_burdens,
        art_direction=dict(plan.get("art_direction", {})),
        poem_design=build_poem_design(plan, grounding),
        supporting_elements=[_text(item) for item in _list(plan.get("supporting_elements")) if _text(item)],
        local_constraints=prune_local_constraints(
            _list(plan.get("local_constraints")),
            _list(grounding.get("risks")),
            _list(grounding.get("unsupported_claims")),
        ),
        evidence_path=[
            *evidence_ids,
            "governing_claim",
            "textual_hinge",
            "divine_answer",
            "canonical_fulfillment",
            "reader_response",
        ],
    )


def validate_blueprint(blueprint: IntegratedPassageBlueprint) -> list[IntegratedFinding]:
    required = {
        "governing_question": blueprint.governing_question,
        "governing_subject": blueprint.governing_subject,
        "human_predicament": blueprint.human_predicament,
        "textual_hinge": blueprint.textual_hinge,
        "divine_answer": blueprint.divine_answer,
        "canonical_fulfillment": blueprint.canonical_fulfillment,
    }
    findings = _missing(required, tuple(required), "P01", "blueprint")
    findings.extend(
        IntegratedFinding("P02", f"reader_transformation.{name}", "Reader Transformation Map is incomplete.", repair_target="blueprint")
        for name in ("initial_assumption", "new_perception", "faithful_response")
        if not _text(blueprint.reader_transformation.get(name))
    )

    burden_index: dict[str, list[str]] = {}
    for section in PROSE_SECTIONS:
        burden = _text(blueprint.section_burdens.get(section))
        if not burden:
            findings.append(IntegratedFinding("P03", f"section_burdens.{section}", "One concise prose movement is required.", repair_target="blueprint"))
        else:
            burden_index.setdefault(" ".join(burden.lower().split()), []).append(section)
    for sections in burden_index.values():
        if len(sections) > 1:
            findings.append(IntegratedFinding("P04", "section_burdens", f"Repeated prose movement: {', '.join(sections)}.", repair_target="blueprint"))

    if not blueprint.art_direction:
        findings.append(IntegratedFinding("P05", "art_direction", "Art direction is required.", repair_target="blueprint"))
    for name in ("image_field", "sensory_palette", "sonic_movement", "emotional_turn"):
        if blueprint.poem_design.get(name) in (None, "", [], {}):
            findings.append(IntegratedFinding("P06", f"poem_design.{name}", "Poem design is incomplete.", repair_target="blueprint"))
    if len(blueprint.poem_design.get("sensory_palette", [])) < 2:
        findings.append(IntegratedFinding("P07", "poem_design.sensory_palette", "Poem needs at least two passage-born sensory anchors.", repair_target="blueprint"))
    if len(blueprint.evidence_path) < 6:
        findings.append(IntegratedFinding("P08", "evidence_path", "Evidence path is incomplete.", repair_target="blueprint"))
    blueprint.approved = not findings
    return findings


def _materialize_context(ctx: Any, grounding: Mapping[str, Any], blueprint: IntegratedPassageBlueprint) -> None:
    source = normalize_provenance_record(grounding["source_provenance"])
    rendering = normalize_provenance_record(grounding["rendering_provenance"])
    ctx.source_text = _text(grounding["source_text"])
    ctx.working_rendering = _text(grounding["working_rendering"])
    ctx.source_layer = {"source_text": ctx.source_text, "chapter_verse_count": grounding.get("chapter_verse_count"), "scripture_provenance": source}
    ctx.rendering_layer = {"working_rendering": ctx.working_rendering, "scripture_provenance": rendering}
    ctx.scripture_provenance = {"source": source, "rendering": rendering, "focus": rendering}
    physical = [_text(item) for item in _list(grounding.get("physical_vocabulary")) if _text(item)]
    ctx.chapter_design_map = {
        "chapter_start": _text(grounding.get("chapter_start") or grounding["historical_meaning"]),
        "chapter_end": _text(grounding.get("chapter_end") or blueprint.reader_transformation["new_perception"]),
        "emotional_movement": f"{blueprint.human_predicament} -> {blueprint.reader_transformation['new_perception']}",
        "divine_action": blueprint.divine_answer,
        "physical_vocabulary": physical,
        "central_theological_claim": blueprint.governing_subject,
        "christward_fulfillment": blueprint.canonical_fulfillment,
        "reader_felt_experience": blueprint.human_predicament,
        "chapter_design_summary": _text(grounding["historical_meaning"]),
    }
    ctx.correspondence = dict(grounding["canonical_relationship"])
    ctx.theological_risk_register = [dict(item) for item in _list(grounding["risks"]) if isinstance(item, Mapping)]
    ctx.historical_linguistic = {"historical_meaning": _text(grounding["historical_meaning"]), "literary_mode": _text(grounding["literary_mode"])}
    ctx.commentary_grounding = {"textual_evidence": list(_list(grounding["textual_evidence"])), "unsupported_claims": list(_list(grounding.get("unsupported_claims")))}
    ctx.art_direction = dict(blueprint.art_direction)
    ctx.brief = {
        "selected_threshold_phrase": "",
        "governing_image": blueprint.governing_image,
        "image_lexicon": list(blueprint.poem_design.get("sensory_palette", physical)),
        "chapter_specific_terms": [_text(item.get("reference")) for item in _list(grounding["textual_evidence"]) if isinstance(item, Mapping)],
        "christology_required_echoes": [],
        "christology_pathway": blueprint.canonical_fulfillment,
        "theological_terminus": blueprint.canonical_fulfillment,
        "semantic_proof_chain": list(blueprint.evidence_path),
        "passage_center_map": {
            "governing_subject": blueprint.governing_subject,
            "human_predicament": blueprint.human_predicament,
            "supporting_elements": list(blueprint.supporting_elements),
            "textual_hinge": blueprint.textual_hinge,
            "divine_answer": blueprint.divine_answer,
            "resolution": blueprint.reader_transformation["new_perception"],
            "canonical_fulfillment": blueprint.canonical_fulfillment,
            "reader_response": blueprint.reader_transformation["faithful_response"],
            "section_burdens": dict(blueprint.section_burdens),
            "governing_terms": [word for word in blueprint.governing_subject.lower().split() if len(word) >= 4],
            "supporting_terms": [word for item in blueprint.supporting_elements for word in item.lower().split() if len(word) >= 4],
        },
    }
    ctx.blueprint = blueprint
    ctx.planning_packet = {
        "passage": {"question": blueprint.governing_question, "subject": blueprint.governing_subject, "hinge": blueprint.textual_hinge, "divine_answer": blueprint.divine_answer},
        "poem_design": dict(blueprint.poem_design),
    }


def validate_review(review: Mapping[str, Any], config: EngineConfig | None = None) -> tuple[list[IntegratedFinding], list[IntegratedFinding]]:
    config = config or EngineConfig()
    verdict = _text(review.get("verdict")).lower()
    hard = [_review_finding(item, "error") for item in _list(review.get("hard_findings"))]
    advisory = [_review_finding(item, "warning") for item in _list(review.get("advisory_findings"))]
    if verdict not in {"pass", "revise", "fail"}:
        hard.append(IntegratedFinding("R00", "verdict", "Verdict must be Pass, Revise, or Fail.", repair_target="review"))
    dimensions = review.get("dimensions")
    if not isinstance(dimensions, Mapping):
        hard.append(IntegratedFinding("R02", "dimensions", "Review dimensions are required.", repair_target="review"))
    else:
        minimum = float(getattr(config, "integrated_review_min_score", 8.0))
        for name in REVIEW_DIMENSIONS:
            if name not in dimensions:
                hard.append(IntegratedFinding("R03", f"dimensions.{name}", "Review dimension is required.", repair_target="review"))
                continue
            try:
                score = float(dimensions[name])
            except (TypeError, ValueError):
                hard.append(IntegratedFinding("R04", f"dimensions.{name}", "Review dimension must be numeric.", repair_target="review"))
                continue
            if verdict == "pass" and score < minimum:
                hard.append(IntegratedFinding("R05", f"dimensions.{name}", f"Passing score {score:g} is below the configured minimum {minimum:g}.", repair_target="review"))
    if verdict == "pass" and hard:
        hard.append(IntegratedFinding("R06", "verdict", "Passing review contains unresolved hard findings.", repair_target="review"))
    return hard, advisory


def _apply_draft(ctx: Any, draft: Mapping[str, Any]) -> list[IntegratedFinding]:
    findings = _missing(draft, (*PROSE_FIELDS, "poem"), "D01", "draft")
    if findings:
        return findings
    ctx.prose = {name: _text(draft[name]) for name in PROSE_FIELDS}
    ctx.poem = _text(draft["poem"])
    return []


def _as_integrated(item: LiteraryFinding) -> IntegratedFinding:
    return IntegratedFinding(item.code, item.field, item.message, item.severity, item.repair_target)


def run_integrated_devotional(ctx: Any, adapter: Any, config: EngineConfig | None = None) -> Any:
    """Run dense grounding, spare blueprint, liberated composition, and one review."""

    config = config or EngineConfig()
    ctx.pipeline_mode = "integrated"
    try:
        ctx.trace.append(State.TEXT_GROUNDING)
        grounding = adapter.call("devotional_grounder", {"chapter_ref": ctx.chapter_ref, "source_text": ctx.source_text, "context": ctx})
        if not isinstance(grounding, Mapping):
            raise ValidationError("devotional_grounder output must be a dictionary")
        findings = validate_grounding(grounding, allow_test_fixture=_is_mock(adapter), config=config)
        if findings:
            raise ValidationError("; ".join(f"{item.field}: {item.message}" for item in findings))
        ctx.grounding_packet = dict(grounding)

        ctx.trace.append(State.PASSAGE_BLUEPRINT)
        plan = adapter.call(
            "devotional_planner",
            {
                "chapter_ref": ctx.chapter_ref,
                "grounding": dict(grounding),
                "protected_facts": {
                    "governing_claim": grounding["governing_claim"],
                    "textual_hinge": grounding["textual_hinge"],
                    "divine_action": grounding["divine_action"],
                    "canonical_relationship": grounding["canonical_relationship"],
                    "christological_fulfillment": grounding["christological_fulfillment"],
                },
                "planning_instruction": "Build a spare blueprint: one movement per prose section and a separate poem design of image field, sensory palette, sonic movement, and emotional turn.",
                "context": ctx,
            },
        )
        if not isinstance(plan, Mapping):
            raise ValidationError("devotional_planner output must be a dictionary")
        blueprint = build_blueprint(ctx, grounding, plan)
        findings = validate_blueprint(blueprint)
        ctx.blueprint_findings = findings
        if findings:
            raise ValidationError("; ".join(f"{item.field}: {item.message}" for item in findings))
        _materialize_context(ctx, grounding, blueprint)
        scripture_failures = validate_scripture_context(ctx)
        if scripture_failures:
            raise ValidationError("; ".join(scripture_failures))

        packet = composition_packet(ctx, grounding, blueprint, config)
        max_revisions = max(0, int(getattr(config, "integrated_max_revisions", 1)))
        revision = 0
        revision_brief: dict[str, Any] = {}
        while True:
            ctx.trace.append(State.INTEGRATED_COMPOSITION if revision == 0 else State.TARGETED_REVISION)
            draft = adapter.call("devotional_composer", {"composition_packet": packet, "revision": revision, "revision_brief": revision_brief})
            if not isinstance(draft, Mapping):
                raise ValidationError("devotional_composer output must be a dictionary")
            findings = _apply_draft(ctx, draft)
            if findings:
                raise ValidationError("; ".join(f"{item.field}: {item.message}" for item in findings))
            ctx.draft_log.append({"revision": revision, "prose": dict(ctx.prose), "poem": ctx.poem})

            harness_failures, harness_warnings = run_deterministic_harness(ctx, config)
            for warning in harness_warnings:
                if warning not in ctx.warnings:
                    ctx.warnings.append(warning)
            coherence = audit_prose(ctx, ctx.prose, config)
            coherence_hard = [IntegratedFinding(f"COHERENCE_{item.code}", item.field, item.message, "error", item.field) for item in coherence if item.severity == "error"]
            coherence_advisory = [IntegratedFinding(f"COHERENCE_{item.code}", item.field, item.message, "warning", item.field) for item in coherence if item.severity != "error"]
            literary = [_as_integrated(item) for item in audit_literary_economy(ctx, blueprint, config)]

            ctx.trace.append(State.INTEGRATED_REVIEW)
            review = adapter.call(
                "devotional_reviewer",
                {
                    "chapter_ref": ctx.chapter_ref,
                    "protected": {"passage": packet["passage"], "canonical": packet["canonical"], "reader_transformation": packet["reader_transformation"], "boundaries": packet["boundaries"]},
                    "draft": {**ctx.prose, "poem": ctx.poem},
                    "deterministic_failures": list(harness_failures),
                    "coherence_findings": [item.__dict__ for item in coherence_hard + coherence_advisory],
                    "literary_findings": [item.__dict__ for item in literary],
                    "review_instruction": "Truth failures are hard. Test whether each sentence and line earns its place, whether prose trusts implication, and whether the poem has image, qualia, music, breath, and an emotional turn without summarizing the devotional.",
                    "revision": revision,
                },
            )
            if not isinstance(review, Mapping):
                raise ValidationError("devotional_reviewer output must be a dictionary")
            review_hard, review_advisory = validate_review(review, config)
            ctx.integrated_review = dict(review)
            ctx.scores["integrated_review"] = dict(review)
            hard = [*[IntegratedFinding("HARNESS", "draft", message) for message in harness_failures], *coherence_hard, *review_hard]
            advisory = [*coherence_advisory, *literary, *review_advisory]
            _warn(ctx, advisory)
            verdict = _text(review.get("verdict")).lower()

            if verdict == "pass" and not hard:
                ctx.trace.append(State.LEDGER_UPDATE)
                update_ledger(ctx)
                ctx.trace.append(State.EMIT_ARTIFACT)
                ctx.artifact = render_artifact(ctx)
                ctx.failed_checks = []
                ctx.error = ""
                ctx.trace.append(State.DONE)
                return ctx
            if verdict == "fail" or revision >= max_revisions:
                return _escalate(ctx, hard)
            revision += 1
            revision_brief = {
                "hard_findings": [item.__dict__ for item in hard],
                "literary_findings": [item.__dict__ for item in literary],
                "advisory_findings": [item.__dict__ for item in advisory],
                "instruction": "Repair only identified fields. Preserve Scripture, grounding, blueprint, and unaffected artistic choices. Cut before adding.",
            }
    except Exception as exc:
        ctx.error = f"{type(exc).__name__}: {exc}"
        ctx.failed_checks = ctx.failed_checks or [f"[BOTH] integrated devotional exception: {exc}"]
        if not ctx.trace or ctx.trace[-1] is not State.ESCALATED:
            ctx.trace.append(State.ESCALATED)
        return ctx
