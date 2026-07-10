from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


REQUIRED_SECTION_PURPOSES = {
    "introduction",
    "reflection",
    "christ_fulfillment",
    "application",
    "prayer",
    "poem",
}

REQUIRED_STRUCTURAL_CONSTRAINTS = {
    "emotion_earned_by_physical_fact",
    "no_unwarranted_deprivation",
}


@dataclass(frozen=True)
class BlueprintFinding:
    code: str
    field: str
    message: str
    severity: str = "error"
    repair_target: str = "blueprint"
    requires_global_regeneration: bool = False


@dataclass
class StoryPlanBlueprint:
    chapter_ref: str
    source_state: dict[str, Any]
    chapter_design_map: dict[str, Any]
    section_purposes: dict[str, str]
    theological_logic: list[str]
    theological_risk_register: list[dict[str, Any]]
    emotional_arc: list[str]
    image_continuity: dict[str, Any]
    christology_pathway: list[str]
    application_target: str
    prayer_arc: list[str]
    poem_arc: list[str]
    voice_constraints: list[str]
    structural_constraints: list[str]
    unresolved_risks: list[dict[str, Any]] = field(default_factory=list)
    continuity_ledger_references: list[str] = field(default_factory=list)
    approved: bool = False


def _as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _poem_arc(poem_plan: Any) -> list[str]:
    if isinstance(poem_plan, dict):
        return [str(item) for item in _as_list(poem_plan.get("arc", poem_plan.get("movement", poem_plan)))]
    return [str(item) for item in _as_list(poem_plan)]


def build_blueprint(ctx: Any) -> StoryPlanBlueprint:
    brief = ctx.brief
    design = ctx.chapter_design_map
    poem_plan = brief.get("poem_plan", {})
    poem_arc = _poem_arc(poem_plan)
    risks = list(ctx.theological_risk_register)
    unresolved = [
        risk
        for risk in risks
        if "status" in risk and str(risk.get("status", "")).lower() not in {"resolved", "accepted"}
    ]
    return StoryPlanBlueprint(
        chapter_ref=ctx.chapter_ref,
        source_state={
            "source_text": ctx.source_text,
            "working_rendering": ctx.working_rendering,
            "source_layer": ctx.source_layer,
            "rendering_layer": ctx.rendering_layer,
        },
        chapter_design_map=design,
        section_purposes={
            "introduction": brief.get("opening_movement", ""),
            "reflection": brief.get("central_thought", ""),
            "christ_fulfillment": brief.get("christology_pathway", ""),
            "application": brief.get("application_target", ""),
            "prayer": brief.get("theological_terminus", ""),
            "poem": str(poem_plan),
        },
        theological_logic=[design.get("central_theological_claim", ""), brief.get("theological_terminus", "")],
        theological_risk_register=risks,
        emotional_arc=[design.get("emotional_movement", ""), brief.get("emotional_charge", ""), brief.get("closing_movement", "")],
        image_continuity={
            "governing_image": brief.get("governing_image", ""),
            "image_lexicon": _as_list(brief.get("image_lexicon", [])),
            "image_head_terms": _as_list(brief.get("image_head_terms", [])),
        },
        christology_pathway=[design.get("christward_fulfillment", ""), brief.get("christology_pathway", "")],
        application_target=brief.get("application_target", ""),
        prayer_arc=[brief.get("application_target", ""), brief.get("theological_terminus", "")],
        poem_arc=poem_arc,
        voice_constraints=[str(item) for item in _as_list(brief.get("negative_constraints", []))]
        + [str(item) for item in _as_list(ctx.art_direction.get("avoid", []))],
        structural_constraints=[
            "blueprint_before_script",
            "source_fields_immutable",
            "bounded_component_repairs",
            "emotion_earned_by_physical_fact",
            "no_unwarranted_deprivation",
        ],
        unresolved_risks=unresolved,
        continuity_ledger_references=[str(entry.get("chapter_ref", "")) for entry in ctx.ledger.get("entries", [])],
    )


def validate_blueprint(blueprint: StoryPlanBlueprint) -> list[BlueprintFinding]:
    findings: list[BlueprintFinding] = []
    missing_sections = REQUIRED_SECTION_PURPOSES - set(blueprint.section_purposes)
    empty_sections = {key for key, value in blueprint.section_purposes.items() if not str(value).strip()}
    for key in sorted(missing_sections | empty_sections):
        findings.append(BlueprintFinding("B01", f"section_purposes.{key}", "Section purpose is missing."))
    if not all(str(item).strip() for item in blueprint.theological_logic):
        findings.append(BlueprintFinding("B02", "theological_logic", "Theological logic contains an unsupported or empty claim."))
    if not all(str(item).strip() for item in blueprint.christology_pathway):
        findings.append(BlueprintFinding("B03", "christology_pathway", "Christological pathway is discontinuous."))
    if len([item for item in blueprint.emotional_arc if str(item).strip()]) < 2:
        findings.append(BlueprintFinding("B04", "emotional_arc", "Emotional arc lacks a meaningful movement."))
    if not str(blueprint.image_continuity.get("governing_image", "")).strip():
        findings.append(BlueprintFinding("B05", "image_continuity.governing_image", "Governing image is missing."))
    if not blueprint.application_target.strip():
        findings.append(BlueprintFinding("B06", "application_target", "Application does not arise from the chapter plan."))
    if not any(str(item).strip() for item in blueprint.poem_arc):
        findings.append(BlueprintFinding("B07", "poem_arc", "Poem arc is disconnected from the prose plan."))
    high_risks = [risk for risk in blueprint.unresolved_risks if str(risk.get("severity", "high")).lower() in {"high", "critical"}]
    if high_risks:
        findings.append(BlueprintFinding("B08", "unresolved_risks", "High-severity theological risks remain unresolved."))
    missing_constraints = REQUIRED_STRUCTURAL_CONSTRAINTS - set(blueprint.structural_constraints)
    for constraint in sorted(missing_constraints):
        findings.append(
            BlueprintFinding(
                "B09",
                f"structural_constraints.{constraint}",
                "The blueprint must earn emotion through warranted physical fact and may not invent deprivation to intensify desire.",
            )
        )
    return findings


def approve_blueprint(blueprint: StoryPlanBlueprint) -> list[BlueprintFinding]:
    findings = validate_blueprint(blueprint)
    blueprint.approved = not findings
    return findings


def validate_script_alignment(blueprint: StoryPlanBlueprint, prose: dict[str, Any], poem: str) -> list[BlueprintFinding]:
    findings: list[BlueprintFinding] = []
    if not blueprint.approved:
        findings.append(BlueprintFinding("A00", "approved", "Script cannot be evaluated against an unapproved blueprint."))
        return findings
    if blueprint.application_target.lower() not in str(prose.get("application", "")).lower():
        findings.append(BlueprintFinding("A01", "application_target", "Application diverges from the approved target.", repair_target="application"))
    governing_image = str(blueprint.image_continuity.get("governing_image", "")).lower()
    combined = " ".join(str(value) for value in prose.values()).lower() + " " + poem.lower()
    if governing_image and governing_image not in combined:
        findings.append(BlueprintFinding("A02", "image_continuity.governing_image", "The governing image is absent from the script.", repair_target="prose_and_poem"))
    christ_terms = [term.lower() for term in blueprint.christology_pathway if term]
    if christ_terms and not any(term in str(prose.get("christ_fulfillment", "")).lower() for term in christ_terms):
        findings.append(BlueprintFinding("A03", "christology_pathway", "Christological fulfillment diverges from the blueprint.", repair_target="christ_fulfillment"))
    if not poem.strip():
        findings.append(BlueprintFinding("A04", "poem_arc", "Poem is missing.", repair_target="poem"))
    return findings
