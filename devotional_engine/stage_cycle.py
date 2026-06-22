from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StageName(str, Enum):
    PLANNING = "planning"
    TOOL_USE = "tool_use"
    VERIFICATION = "verification"
    REFLECTION = "reflection"


@dataclass(frozen=True)
class StageArtifact:
    artifact_id: str
    stage: StageName
    content: Any
    claims: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class StageReport:
    stage: StageName
    artifacts: tuple[StageArtifact, ...] = ()
    notes: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()


@dataclass(frozen=True)
class RejectedArtifact:
    artifact: StageArtifact
    reason: str


@dataclass(frozen=True)
class VerificationReport:
    accepted: tuple[StageArtifact, ...] = ()
    rejected: tuple[RejectedArtifact, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return not self.rejected


@dataclass(frozen=True)
class ReflectionReport:
    retained: tuple[StageArtifact, ...] = ()
    discarded: tuple[RejectedArtifact, ...] = ()
    lessons: tuple[str, ...] = ()
    improved_version: dict = field(default_factory=dict)


StageCheck = Callable[[StageArtifact], bool | tuple[bool, str]]


def _as_tuple(values: Iterable[str] | None) -> tuple[str, ...]:
    return tuple(str(value) for value in values or () if str(value).strip())


def _artifact_from_mapping(raw: Mapping[str, Any], index: int, stage: StageName) -> StageArtifact:
    content = raw.get("content", raw)
    return StageArtifact(
        artifact_id=str(raw.get("artifact_id") or raw.get("id") or f"{stage.value}_{index}"),
        stage=stage,
        content=content,
        claims=_as_tuple(raw.get("claims")),
        evidence=_as_tuple(raw.get("evidence")),
        tags=_as_tuple(raw.get("tags")),
    )


def _normalize_artifacts(values: Iterable[Any], stage: StageName) -> tuple[StageArtifact, ...]:
    artifacts = []
    for index, value in enumerate(values, 1):
        if isinstance(value, StageArtifact):
            artifacts.append(value)
        elif isinstance(value, Mapping):
            artifacts.append(_artifact_from_mapping(value, index, stage))
        else:
            artifacts.append(StageArtifact(f"{stage.value}_{index}", stage, value))
    return tuple(artifacts)


def planning_stage(task: str, objectives: Iterable[str] = (), constraints: Iterable[str] = ()) -> StageReport:
    task = task.strip()
    if not task:
        return StageReport(StageName.PLANNING, failures=("planning task is empty",))
    plan = {
        "task": task,
        "objectives": _as_tuple(objectives),
        "constraints": _as_tuple(constraints),
        "stages": tuple(stage.value for stage in StageName),
        "principle": "separate, test, discard failures, recombine verified parts",
    }
    return StageReport(
        StageName.PLANNING,
        artifacts=(StageArtifact("plan", StageName.PLANNING, plan, tags=("plan",)),),
        notes=("Plan created with explicit verification and reflection boundaries.",),
    )


def tool_use_stage(plan: StageReport, outputs: Iterable[Any], notes: Iterable[str] = ()) -> StageReport:
    if plan.failures:
        return StageReport(StageName.TOOL_USE, failures=("tool-use skipped because planning failed",))
    artifacts = _normalize_artifacts(outputs, StageName.TOOL_USE)
    if not artifacts:
        return StageReport(StageName.TOOL_USE, failures=("tool-use produced no artifacts",))
    return StageReport(StageName.TOOL_USE, artifacts=artifacts, notes=_as_tuple(notes))


def _run_check(check: StageCheck, artifact: StageArtifact) -> tuple[bool, str]:
    result = check(artifact)
    if isinstance(result, tuple):
        passed, reason = result
        return bool(passed), str(reason)
    return bool(result), getattr(check, "__name__", "check failed")


def verification_stage(reports: Sequence[StageReport], checks: Mapping[str, StageCheck] | None = None) -> VerificationReport:
    checks = checks or {}
    candidates = tuple(artifact for report in reports for artifact in report.artifacts if report.stage is not StageName.PLANNING)
    accepted, rejected = [], []
    for artifact in candidates:
        reasons = []
        if artifact.content in (None, ""):
            reasons.append("empty artifact content")
        for check_name, check in checks.items():
            passed, reason = _run_check(check, artifact)
            if not passed:
                reasons.append(reason or check_name)
        if reasons:
            rejected.append(RejectedArtifact(artifact, "; ".join(reasons)))
        else:
            accepted.append(artifact)
    return VerificationReport(tuple(accepted), tuple(rejected), notes=("Verified artifacts independently from generation.",))


def reflection_stage(task: str, verification: VerificationReport) -> ReflectionReport:
    retained = verification.accepted
    discarded = verification.rejected
    lessons = []
    if retained:
        lessons.append(f"Retained {len(retained)} verified artifact(s).")
    if discarded:
        lessons.append(f"Discarded {len(discarded)} failed artifact(s).")
    improved_version = {
        "task": task,
        "retained_artifact_ids": tuple(artifact.artifact_id for artifact in retained),
        "discarded_artifact_ids": tuple(item.artifact.artifact_id for item in discarded),
        "content": tuple(artifact.content for artifact in retained),
        "discard_reasons": tuple(item.reason for item in discarded),
    }
    return ReflectionReport(retained, discarded, tuple(lessons), improved_version)


def run_stage_cycle(
    task: str,
    outputs: Iterable[Any],
    checks: Mapping[str, StageCheck] | None = None,
    objectives: Iterable[str] = (),
    constraints: Iterable[str] = (),
) -> tuple[StageReport, StageReport, VerificationReport, ReflectionReport]:
    plan = planning_stage(task, objectives, constraints)
    tool_report = tool_use_stage(plan, outputs)
    verification = verification_stage((plan, tool_report), checks)
    reflection = reflection_stage(task, verification)
    return plan, tool_report, verification, reflection
