from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .exceptions import ValidationError
from .profiles import WritingMode, compile_rule_ids, get_profile, normalize_mode


@dataclass(frozen=True)
class PlanFinding:
    code: str
    field: str
    message: str
    severity: str = "error"


@dataclass
class PlanningPacket:
    mode: str
    project_ref: str
    governing_question: str
    truth_contract: list[str]
    planning_maps: dict[str, Any]
    compiled_rule_ids: list[str]
    local_constraints: list[str] = field(default_factory=list)
    approved: bool = False


@dataclass
class WritingRequest:
    mode: WritingMode | str
    project_ref: str
    source_material: str
    plan: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfiledRunResult:
    request: WritingRequest
    packet: PlanningPacket
    draft: dict[str, Any]
    evaluation: dict[str, Any]
    revision_count: int = 0


def build_planning_packet(
    mode: WritingMode | str,
    project_ref: str,
    plan: dict[str, Any],
) -> PlanningPacket:
    normalized_mode = normalize_mode(mode)
    candidate_rules = plan.get("candidate_rules", [])
    return PlanningPacket(
        mode=normalized_mode.value,
        project_ref=str(project_ref).strip(),
        governing_question=str(plan.get("governing_question", "")).strip(),
        truth_contract=[str(item).strip() for item in plan.get("truth_contract", []) if str(item).strip()],
        planning_maps=dict(plan.get("planning_maps", {})),
        compiled_rule_ids=list(compile_rule_ids(normalized_mode, candidate_rules)),
        local_constraints=[
            str(item).strip()
            for item in plan.get("local_constraints", [])
            if str(item).strip()
        ],
    )


def validate_planning_packet(packet: PlanningPacket) -> list[PlanFinding]:
    profile = get_profile(packet.mode)
    findings: list[PlanFinding] = []
    if not packet.project_ref:
        findings.append(PlanFinding("P01", "project_ref", "Project reference is required."))
    if not packet.governing_question:
        findings.append(PlanFinding("P02", "governing_question", "One governing question is required."))
    if not packet.truth_contract:
        findings.append(PlanFinding("P03", "truth_contract", "Truth contract is required."))
    missing_maps = [name for name in profile.required_planning_maps if not packet.planning_maps.get(name)]
    for name in missing_maps:
        findings.append(PlanFinding("P04", f"planning_maps.{name}", "Required planning map is missing."))
    missing_rules = [rule for rule in compile_rule_ids(profile.mode) if rule not in packet.compiled_rule_ids]
    for rule in missing_rules:
        findings.append(PlanFinding("P05", f"compiled_rule_ids.{rule}", "Required rule was not compiled."))
    return findings


def approve_planning_packet(packet: PlanningPacket) -> list[PlanFinding]:
    findings = validate_planning_packet(packet)
    packet.approved = not findings
    return findings


def validate_profiled_draft(mode: WritingMode | str, draft: dict[str, Any]) -> list[PlanFinding]:
    profile = get_profile(mode)
    findings: list[PlanFinding] = []
    for field_name in profile.required_output_fields:
        if field_name not in draft or draft[field_name] in (None, "", [], {}):
            findings.append(PlanFinding("D01", f"draft.{field_name}", "Required draft field is missing."))
    return findings


def _validate_evaluation(evaluation: dict[str, Any], mode: WritingMode | str) -> list[PlanFinding]:
    profile = get_profile(mode)
    findings: list[PlanFinding] = []
    verdict = str(evaluation.get("verdict", "")).strip().lower()
    if verdict not in {"pass", "revise", "fail"}:
        findings.append(PlanFinding("E01", "evaluation.verdict", "Verdict must be Pass, Revise, or Fail."))
    dimensions = evaluation.get("dimensions", {})
    if not isinstance(dimensions, dict):
        findings.append(PlanFinding("E02", "evaluation.dimensions", "Evaluation dimensions must be a dictionary."))
        return findings
    for dimension in profile.evaluator_dimensions:
        if dimension not in dimensions:
            findings.append(PlanFinding("E03", f"evaluation.dimensions.{dimension}", "Required evaluator dimension is missing."))
    return findings


def run_profiled_engine(
    request: WritingRequest,
    adapter: Any,
    *,
    max_revisions: int = 1,
) -> ProfiledRunResult:
    """Run the lean shared core for devotional, fiction, or nonfiction work.

    The full devotional state machine remains available as ``run_engine``. This
    runner provides a smaller profile-aware path for fiction/nonfiction and for
    experiments that do not require the entire devotional harness.
    """

    plan = request.plan or adapter.call(
        "profile_planner",
        {
            "mode": normalize_mode(request.mode).value,
            "project_ref": request.project_ref,
            "source_material": request.source_material,
            "metadata": request.metadata,
        },
    )
    packet = build_planning_packet(request.mode, request.project_ref, plan)
    findings = approve_planning_packet(packet)
    if findings:
        fields = ", ".join(item.field for item in findings)
        raise ValidationError(f"Planning packet failed validation: {fields}")

    payload = {
        "request": request,
        "profile": get_profile(request.mode),
        "packet": packet,
    }
    draft = adapter.call("profile_composer", payload)
    draft_findings = validate_profiled_draft(request.mode, draft)
    if draft_findings:
        fields = ", ".join(item.field for item in draft_findings)
        raise ValidationError(f"Draft failed validation: {fields}")

    evaluation = adapter.call("profile_evaluator", {**payload, "draft": draft})
    evaluation_findings = _validate_evaluation(evaluation, request.mode)
    if evaluation_findings:
        fields = ", ".join(item.field for item in evaluation_findings)
        raise ValidationError(f"Evaluation failed validation: {fields}")

    revisions = 0
    while str(evaluation.get("verdict", "")).strip().lower() == "revise" and revisions < max_revisions:
        revisions += 1
        draft = adapter.call(
            "profile_reviser",
            {**payload, "draft": draft, "evaluation": evaluation, "revision": revisions},
        )
        draft_findings = validate_profiled_draft(request.mode, draft)
        if draft_findings:
            fields = ", ".join(item.field for item in draft_findings)
            raise ValidationError(f"Revised draft failed validation: {fields}")
        evaluation = adapter.call("profile_evaluator", {**payload, "draft": draft})
        evaluation_findings = _validate_evaluation(evaluation, request.mode)
        if evaluation_findings:
            fields = ", ".join(item.field for item in evaluation_findings)
            raise ValidationError(f"Revised evaluation failed validation: {fields}")

    if str(evaluation.get("verdict", "")).strip().lower() != "pass":
        raise ValidationError("Profiled writing run did not reach a passing evaluation.")

    return ProfiledRunResult(
        request=request,
        packet=packet,
        draft=draft,
        evaluation=evaluation,
        revision_count=revisions,
    )
