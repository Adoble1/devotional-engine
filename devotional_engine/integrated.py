from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .coherence import audit_prose, build_passage_center_map
from .config import EngineConfig
from .exceptions import ValidationError
from .harness import run_deterministic_harness
from .ledger import update_ledger
from .renderer import render_artifact
from .scripture import normalize_provenance_record, validate_provenance_record, validate_scripture_context
from .states import State


INTEGRATED_ROLES = (
    "devotional_grounder",
    "devotional_planner",
    "devotional_composer",
    "devotional_reviewer",
)
CANONICAL_RELATIONSHIPS = {
    "explicit_quotation",
    "explicit_interpretation",
    "typology",
    "thematic_correspondence",
    "canonical_development",
    "no_identified_link",
}
SECTIONS = ("introduction", "reflection", "christ_fulfillment", "application", "prayer", "poem")
PROSE_FIELDS = (
    "title",
    "epigraph",
    "focus_bible_verses",
    "introduction",
    "reflection",
    "christ_fulfillment",
    "application",
    "prayer",
    "next_in_sequence",
)
REVIEW_DIMENSIONS = (
    "textual_fidelity",
    "theological_accuracy",
    "canonical_warrant",
    "blueprint_alignment",
    "literary_quality",
)


@dataclass(frozen=True)
class IntegratedFinding:
    code: str
    field: str
    message: str
    severity: str = "error"
    repair_target: str = "draft"


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
    governing_image: str
    poem_arc: list[str]
    supporting_elements: list[str]
    local_constraints: list[str]
    evidence_path: list[str]
    approved: bool = False


def _text(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]


def _finding(code: str, field: str, message: str, target: str = "draft", severity: str = "error") -> IntegratedFinding:
    return IntegratedFinding(code, field, message, severity, target)


def _is_mock(adapter: Any) -> bool:
    current = adapter
    for _ in range(6):
        if current is None:
            return False
        if current.__class__.__name__ == "MockAgentAdapter":
            return True
        current = getattr(current, "delegate", None)
    return False


def adapter_supports_integrated_devotional(adapter: Any) -> bool:
    """Real adapters use the four-role core; old mocks use the compatibility path."""

    current = adapter
    for _ in range(6):
        outputs = getattr(current, "outputs", None)
        if isinstance(outputs, Mapping):
            return all(role in outputs for role in INTEGRATED_ROLES)
        current = getattr(current, "delegate", None)
        if current is None:
            break
    return True


def _missing(mapping: Mapping[str, Any], fields: tuple[str, ...], code: str, target: str) -> list[IntegratedFinding]:
    return [
        _finding(code, name, "Required field is missing.", target)
        for name in fields
        if mapping.get(name) in (None, "", [], {})
    ]


def validate_grounding(packet: Mapping[str, Any], *, allow_test_fixture: bool, config: EngineConfig) -> list[IntegratedFinding]:
    required = (
        "source_text",
        "working_rendering",
        "source_provenance",
        "rendering_provenance",
        "historical_meaning",
        "literary_mode",
        "textual_evidence",
        "governing_claim",
        "textual_hinge",
        "divine_action",
        "canonical_relationship",
        "christological_fulfillment",
        "reader_felt_experience",
        "risks",
    )
    findings = _missing(packet, required, "G01", "grounding")
    if len(_text(packet.get("source_text"))) < config.source_min_chars:
        findings.append(_finding("G02", "source_text", "Source text is too short.", "grounding"))

    for name in ("source_provenance", "rendering_provenance"):
        record = packet.get(name)
        findings.extend(
            _finding("G03", name, message, "grounding")
            for message in validate_provenance_record(
                record if isinstance(record, Mapping) else None,
                allow_test_fixture=allow_test_fixture,
            )
        )

    ids: set[str] = set()
    for index, item in enumerate(_list(packet.get("textual_evidence"))):
        if not isinstance(item, Mapping) or not all(_text(item.get(key)) for key in ("id", "reference", "claim")):
            findings.append(_finding("G04", f"textual_evidence.{index}", "Evidence requires id, reference, and claim.", "grounding"))
            continue
        evidence_id = _text(item["id"])
        if evidence_id in ids:
            findings.append(_finding("G05", f"textual_evidence.{index}.id", "Evidence ids must be unique.", "grounding"))
        ids.add(evidence_id)

    canonical = packet.get("canonical_relationship")
    if isinstance(canonical, Mapping):
        if _text(canonical.get("classification")) not in CANONICAL_RELATIONSHIPS:
            findings.append(_finding("G06", "canonical_relationship.classification", "Invalid canonical relationship.", "grounding"))
        if not _text(canonical.get("description")):
            findings.append(_finding("G06", "canonical_relationship.description", "Canonical description is required.", "grounding"))

    for index, risk in enumerate(_list(packet.get("risks"))):
        if not isinstance(risk, Mapping) or not all(_text(risk.get(key)) for key in ("risk_description", "avoidance_rule")):
            findings.append(_finding("G07", f"risks.{index}", "Risk requires description and avoidance rule.", "grounding"))
    return findings


def build_blueprint(ctx: Any, grounding: Mapping[str, Any], plan: Mapping[str, Any]) -> IntegratedPassageBlueprint:
    transform = dict(plan.get("reader_transformation", {}))
    evidence_ids = [
        _text(item.get("id"))
        for item in _list(grounding.get("textual_evidence"))
        if isinstance(item, Mapping) and _text(item.get("id"))
    ]
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
        section_burdens={key: _text(value) for key, value in dict(plan.get("section_burdens", {})).items()},
        art_direction=dict(plan.get("art_direction", {})),
        governing_image=_text(plan.get("governing_image")),
        poem_arc=[_text(item) for item in _list(plan.get("poem_arc")) if _text(item)],
        supporting_elements=[_text(item) for item in _list(plan.get("supporting_elements")) if _text(item)],
        local_constraints=[_text(item) for item in _list(plan.get("local_constraints")) if _text(item)],
        evidence_path=[*evidence_ids, "governing_claim", "textual_hinge", "divine_answer", "canonical_fulfillment", "reader_response"],
    )


def validate_blueprint(blueprint: IntegratedPassageBlueprint) -> list[IntegratedFinding]:
    values = {
        "governing_question": blueprint.governing_question,
        "governing_subject": blueprint.governing_subject,
        "human_predicament": blueprint.human_predicament,
        "textual_hinge": blueprint.textual_hinge,
        "divine_answer": blueprint.divine_answer,
        "canonical_fulfillment": blueprint.canonical_fulfillment,
        "governing_image": blueprint.governing_image,
    }
    findings = _missing(values, tuple(values), "P01", "blueprint")
    findings.extend(
        _finding("P02", f"reader_transformation.{name}", "Reader Transformation Map is incomplete.", "blueprint")
        for name in ("initial_assumption", "new_perception", "faithful_response")
        if not _text(blueprint.reader_transformation.get(name))
    )

    burden_index: dict[str, list[str]] = {}
    for section in SECTIONS:
        burden = _text(blueprint.section_burdens.get(section))
        if not burden:
            findings.append(_finding("P03", f"section_burdens.{section}", "Section burden is required.", "blueprint"))
        else:
            burden_index.setdefault(" ".join(burden.lower().split()), []).append(section)
    for sections in burden_index.values():
        if len(sections) > 1:
            findings.append(_finding("P04", "section_burdens", f"Repeated burden: {', '.join(sections)}.", "blueprint"))

    if not blueprint.art_direction:
        findings.append(_finding("P05", "art_direction", "Art direction is required.", "blueprint"))
    if not blueprint.poem_arc:
        findings.append(_finding("P06", "poem_arc", "Poem arc is required.", "blueprint"))
    if len(blueprint.evidence_path) < 6:
        findings.append(_finding("P07", "evidence_path", "Evidence path is incomplete.", "blueprint"))
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
    ctx.chapter_design_map = {
        "chapter_start": _text(grounding.get("chapter_start") or grounding["historical_meaning"]),
        "chapter_end": _text(grounding.get("chapter_end") or blueprint.reader_transformation["new_perception"]),
        "emotional_movement": f"{blueprint.human_predicament} -> {blueprint.reader_transformation['new_perception']}",
        "divine_action": blueprint.divine_answer,
        "physical_vocabulary": [_text(item) for item in _list(grounding.get("physical_vocabulary")) if _text(item)],
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
        "chapter_burden": blueprint.governing_subject,
        "opening_movement": blueprint.section_burdens["introduction"],
        "closing_movement": blueprint.reader_transformation["new_perception"],
        "central_thought": blueprint.governing_subject,
        "emotional_charge": blueprint.human_predicament,
        "transcendent_force": blueprint.textual_hinge,
        "selected_threshold_phrase": "",
        "threshold_phrase_rationale": "",
        "governing_image": blueprint.governing_image,
        "image_lexicon": list(_list(blueprint.art_direction.get("image_lexicon") or grounding.get("physical_vocabulary"))),
        "image_head_terms": [],
        "anchor_terms": [],
        "chapter_specific_terms": [_text(item.get("reference")) for item in _list(grounding["textual_evidence"]) if isinstance(item, Mapping)],
        "christology_required_echoes": [],
        "christology_pathway": blueprint.canonical_fulfillment,
        "application_target": blueprint.reader_transformation["faithful_response"],
        "theological_terminus": blueprint.canonical_fulfillment,
        "negative_constraints": list(blueprint.local_constraints),
        "poem_plan": list(blueprint.poem_arc),
        "semantic_proof_chain": list(blueprint.evidence_path),
        "supporting_elements": list(blueprint.supporting_elements),
        "textual_hinge": blueprint.textual_hinge,
        "divine_answer": blueprint.divine_answer,
        "canonical_fulfillment": blueprint.canonical_fulfillment,
        "reader_response": blueprint.reader_transformation["faithful_response"],
    }
    ctx.brief["passage_center_map"] = build_passage_center_map(ctx, ctx.brief)
    ctx.blueprint = blueprint
    ctx.planning_packet = {"grounding": dict(grounding), "blueprint": blueprint}


def _apply_draft(ctx: Any, draft: Mapping[str, Any]) -> list[IntegratedFinding]:
    findings = _missing(draft, (*PROSE_FIELDS, "poem"), "D01", "draft")
    if findings:
        return findings
    ctx.prose = {name: _text(draft[name]) for name in PROSE_FIELDS}
    ctx.poem = _text(draft["poem"])
    return []


def _review_finding(item: Any, severity: str) -> IntegratedFinding:
    if isinstance(item, Mapping):
        return IntegratedFinding(
            _text(item.get("code")) or "R01",
            _text(item.get("field")) or "draft",
            _text(item.get("message")) or "Review finding.",
            severity,
            _text(item.get("repair_target")) or "draft",
        )
    return IntegratedFinding("R01", "draft", _text(item) or "Review finding.", severity)


def validate_review(review: Mapping[str, Any]) -> tuple[list[IntegratedFinding], list[IntegratedFinding]]:
    verdict = _text(review.get("verdict")).lower()
    hard = [_review_finding(item, "error") for item in _list(review.get("hard_findings"))]
    advisory = [_review_finding(item, "warning") for item in _list(review.get("advisory_findings"))]
    if verdict not in {"pass", "revise", "fail"}:
        hard.append(_finding("R00", "verdict", "Verdict must be Pass, Revise, or Fail.", "review"))
    dimensions = review.get("dimensions")
    if not isinstance(dimensions, Mapping):
        hard.append(_finding("R02", "dimensions", "Review dimensions are required.", "review"))
    else:
        hard.extend(
            _finding("R03", f"dimensions.{name}", "Review dimension is required.", "review")
            for name in REVIEW_DIMENSIONS
            if name not in dimensions
        )
    if verdict == "pass" and hard:
        hard.append(_finding("R04", "verdict", "Passing review contains hard findings.", "review"))
    return hard, advisory


def _warn(ctx: Any, findings: list[IntegratedFinding]) -> None:
    for item in findings:
        warning = f"INTEGRATED {item.code}: {item.field}: {item.message}"
        if warning not in ctx.warnings:
            ctx.warnings.append(warning)


def _escalate(ctx: Any, findings: list[IntegratedFinding]) -> Any:
    ctx.failed_checks = [
        f"[PROSE] INTEGRATED {item.code}: {item.field}: {item.message}"
        for item in findings
    ] or ["[PROSE] integrated reviewer did not approve the draft"]
    ctx.error = "ValidationError: integrated devotional did not reach a passing review"
    ctx.trace.append(State.ESCALATED)
    return ctx


def run_integrated_devotional(ctx: Any, adapter: Any, config: EngineConfig | None = None) -> Any:
    """Run Text Grounding -> Passage Blueprint -> Composition -> Integrated Review."""

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
                    "christological_fulfillment": grounding["christological_fulfillment"],
                },
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

        max_revisions = max(0, int(getattr(config, "integrated_max_revisions", 1)))
        revision = 0
        revision_brief: dict[str, Any] = {}

        while True:
            ctx.trace.append(State.INTEGRATED_COMPOSITION if revision == 0 else State.TARGETED_REVISION)
            draft = adapter.call(
                "devotional_composer",
                {
                    "chapter_ref": ctx.chapter_ref,
                    "grounding": dict(grounding),
                    "blueprint": blueprint,
                    "aesthetic_freedom": {
                        "free": ["title", "opening", "paragraph shape", "imagery", "cadence", "transitions", "poem form"],
                        "fixed": ["provenance", "historical meaning", "governing subject", "textual hinge", "divine answer", "canonical classification", "reader response"],
                    },
                    "revision": revision,
                    "revision_brief": revision_brief,
                    "context": ctx,
                },
            )
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
            coherence_hard = [
                IntegratedFinding(f"COHERENCE_{item.code}", item.field, item.message, "error", item.field)
                for item in coherence
                if item.severity == "error"
            ]
            coherence_advisory = [
                IntegratedFinding(f"COHERENCE_{item.code}", item.field, item.message, "warning", item.field)
                for item in coherence
                if item.severity != "error"
            ]

            ctx.trace.append(State.INTEGRATED_REVIEW)
            review = adapter.call(
                "devotional_reviewer",
                {
                    "chapter_ref": ctx.chapter_ref,
                    "grounding": dict(grounding),
                    "blueprint": blueprint,
                    "draft": {**ctx.prose, "poem": ctx.poem},
                    "deterministic_failures": list(harness_failures),
                    "coherence_findings": [item.__dict__ for item in coherence_hard + coherence_advisory],
                    "revision": revision,
                    "context": ctx,
                },
            )
            if not isinstance(review, Mapping):
                raise ValidationError("devotional_reviewer output must be a dictionary")
            review_hard, review_advisory = validate_review(review)
            ctx.integrated_review = dict(review)
            ctx.scores["integrated_review"] = dict(review)

            hard = [
                *[IntegratedFinding("HARNESS", "draft", message) for message in harness_failures],
                *coherence_hard,
                *review_hard,
            ]
            advisory = [*coherence_advisory, *review_advisory]
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
                "advisory_findings": [item.__dict__ for item in advisory],
                "instruction": "Repair only identified fields; preserve grounding, blueprint, Scripture wording, and unaffected literary choices.",
            }
    except Exception as exc:
        ctx.error = f"{type(exc).__name__}: {exc}"
        ctx.failed_checks = ctx.failed_checks or [f"[BOTH] integrated devotional exception: {exc}"]
        if not ctx.trace or ctx.trace[-1] is not State.ESCALATED:
            ctx.trace.append(State.ESCALATED)
        return ctx
