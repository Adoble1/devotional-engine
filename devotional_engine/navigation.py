from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any, Mapping

from .states import State


DEFAULT_ROUTE = (
    "grounding",
    "blueprint",
    "composition",
    "review",
    "validation",
    "emission",
)
DEFAULT_OBJECTIVE_WEIGHTS = {
    "truth": 0.35,
    "alignment": 0.20,
    "literary": 0.15,
    "safety": 0.20,
    "provenance": 0.10,
}
ROLE_CHECKPOINTS = {
    "devotional_grounder": "grounding",
    "devotional_planner": "blueprint",
    "devotional_composer": "composition",
    "devotional_reviewer": "review",
}
PROTECTED_CLAIM_FIELDS = (
    "governing_claim",
    "textual_hinge",
    "divine_action",
    "christological_fulfillment",
)
UNCERTAINTY_STATUSES = {
    "verified",
    "strong_inference",
    "reasonable_inference",
    "speculative",
    "unsupported",
}
SUPPORTED_PROTECTED_STATUSES = {
    "verified",
    "strong_inference",
    "reasonable_inference",
}


class NavigationContractError(ValueError):
    """Raised when the agent leaves the approved route or omits route evidence."""


class CheckpointStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class UncertaintyRecord:
    field: str
    claim: str
    status: str
    evidence_ids: tuple[str, ...] = ()
    source_refs: tuple[str, ...] = ()
    rationale: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "claim": self.claim,
            "status": self.status,
            "evidence_ids": list(self.evidence_ids),
            "source_refs": list(self.source_refs),
            "rationale": self.rationale,
        }


@dataclass
class RouteCheckpoint:
    name: str
    status: CheckpointStatus = CheckpointStatus.PENDING
    attempts: int = 0
    entered_sequence: int | None = None
    completed_sequence: int | None = None
    input_fingerprint: str = ""
    output_fingerprint: str = ""
    findings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "attempts": self.attempts,
            "entered_sequence": self.entered_sequence,
            "completed_sequence": self.completed_sequence,
            "input_fingerprint": self.input_fingerprint,
            "output_fingerprint": self.output_fingerprint,
            "findings": list(self.findings),
        }


@dataclass
class NavigationState:
    mission: str
    route: tuple[str, ...] = DEFAULT_ROUTE
    objective_weights: dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_OBJECTIVE_WEIGHTS)
    )
    checkpoints: dict[str, RouteCheckpoint] = field(default_factory=dict)
    expected_roles: tuple[str, ...] = ("devotional_grounder",)
    current_checkpoint: str = ""
    sequence: int = 0
    deviations: list[str] = field(default_factory=list)
    uncertainty_register: list[UncertaintyRecord] = field(default_factory=list)
    objective_scores: dict[str, float] = field(default_factory=dict)
    aggregate_score: float | None = None
    terminal_status: str = "running"

    def __post_init__(self) -> None:
        for name in self.route:
            self.checkpoints.setdefault(name, RouteCheckpoint(name=name))

    def enter_role(self, role: str, payload: Mapping[str, Any]) -> None:
        if role not in ROLE_CHECKPOINTS:
            raise NavigationContractError(f"Unknown devotional route role: {role}")
        if role not in self.expected_roles:
            expected = ", ".join(self.expected_roles) or "no further model call"
            message = f"Route deviation: received {role}; expected {expected}."
            self.deviations.append(message)
            raise NavigationContractError(message)
        name = ROLE_CHECKPOINTS[role]
        self.sequence += 1
        checkpoint = self.checkpoints[name]
        checkpoint.status = CheckpointStatus.ACTIVE
        checkpoint.attempts += 1
        checkpoint.entered_sequence = self.sequence
        checkpoint.input_fingerprint = fingerprint(payload)
        self.current_checkpoint = name

    def complete_role(self, role: str, output: Any) -> None:
        name = ROLE_CHECKPOINTS[role]
        self.sequence += 1
        checkpoint = self.checkpoints[name]
        checkpoint.status = CheckpointStatus.PASSED
        checkpoint.completed_sequence = self.sequence
        checkpoint.output_fingerprint = fingerprint(output)
        if role == "devotional_grounder":
            self.expected_roles = ("devotional_planner",)
        elif role == "devotional_planner":
            self.expected_roles = ("devotional_composer",)
        elif role == "devotional_composer":
            self.expected_roles = ("devotional_reviewer",)
        else:
            verdict = str(output.get("verdict", "") if isinstance(output, Mapping) else "").strip().lower()
            self.expected_roles = () if verdict == "fail" else ("devotional_composer",)

    def fail_role(self, role: str, message: str) -> None:
        name = ROLE_CHECKPOINTS.get(role, self.current_checkpoint or "validation")
        checkpoint = self.checkpoints[name]
        checkpoint.status = CheckpointStatus.FAILED
        checkpoint.findings.append(message)
        self.deviations.append(message)
        self.terminal_status = "escalated"

    def mark_system_checkpoint(
        self,
        name: str,
        status: CheckpointStatus,
        *,
        findings: list[str] | None = None,
        output: Any = None,
    ) -> None:
        self.sequence += 1
        checkpoint = self.checkpoints[name]
        if checkpoint.entered_sequence is None:
            checkpoint.entered_sequence = self.sequence
        checkpoint.status = status
        checkpoint.completed_sequence = self.sequence
        if output is not None:
            checkpoint.output_fingerprint = fingerprint(output)
        if findings:
            checkpoint.findings.extend(findings)
        self.current_checkpoint = name

    def as_dict(self) -> dict[str, Any]:
        return {
            "mission": self.mission,
            "route": list(self.route),
            "objective_weights": dict(self.objective_weights),
            "expected_roles": list(self.expected_roles),
            "current_checkpoint": self.current_checkpoint,
            "sequence": self.sequence,
            "deviations": list(self.deviations),
            "uncertainty_register": [item.as_dict() for item in self.uncertainty_register],
            "objective_scores": dict(self.objective_scores),
            "aggregate_score": self.aggregate_score,
            "terminal_status": self.terminal_status,
            "checkpoints": [self.checkpoints[name].as_dict() for name in self.route],
        }


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {
            str(key): _json_safe(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if str(key) != "context"
        }
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def fingerprint(value: Any) -> str:
    encoded = json.dumps(
        _json_safe(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _is_mock(adapter: Any) -> bool:
    current = adapter
    for _ in range(8):
        if current is None:
            return False
        if current.__class__.__name__ == "MockAgentAdapter":
            return True
        current = getattr(current, "delegate", None)
    return False


def _string_tuple(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    values = value if isinstance(value, (list, tuple, set)) else (value,)
    return tuple(str(item).strip() for item in values if str(item).strip())


def validate_uncertainty_register(
    grounding: Mapping[str, Any],
    *,
    required: bool,
) -> tuple[list[UncertaintyRecord], list[str]]:
    raw = grounding.get("uncertainty_register")
    if raw in (None, "", []):
        if required:
            return [], [
                "Production grounding requires an uncertainty_register for protected claims."
            ]
        return [], []
    if not isinstance(raw, (list, tuple)):
        return [], ["uncertainty_register must be a list."]

    evidence_ids = {
        str(item.get("id", "")).strip()
        for item in grounding.get("textual_evidence", [])
        if isinstance(item, Mapping) and str(item.get("id", "")).strip()
    }
    records: list[UncertaintyRecord] = []
    findings: list[str] = []
    seen_fields: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            findings.append(f"uncertainty_register.{index} must be a dictionary.")
            continue
        field_name = str(item.get("field", "")).strip()
        claim = str(item.get("claim", "")).strip()
        status = str(item.get("status", "")).strip().lower()
        record_evidence = _string_tuple(item.get("evidence_ids"))
        source_refs = _string_tuple(item.get("source_refs"))
        rationale = str(item.get("rationale", "")).strip()
        if not field_name or not claim or status not in UNCERTAINTY_STATUSES:
            findings.append(
                f"uncertainty_register.{index} requires field, claim, and a valid status."
            )
            continue
        unknown_ids = sorted(set(record_evidence) - evidence_ids)
        if unknown_ids:
            findings.append(
                f"uncertainty_register.{index} references unknown evidence ids: {', '.join(unknown_ids)}."
            )
        if not record_evidence and not source_refs:
            findings.append(
                f"uncertainty_register.{index} requires evidence_ids or source_refs."
            )
        if status in {"speculative", "unsupported"} and not rationale:
            findings.append(
                f"uncertainty_register.{index} requires a rationale for {status} status."
            )
        if field_name in PROTECTED_CLAIM_FIELDS and status not in SUPPORTED_PROTECTED_STATUSES:
            findings.append(
                f"Protected claim {field_name} cannot advance with status {status}."
            )
        seen_fields.add(field_name)
        records.append(
            UncertaintyRecord(
                field=field_name,
                claim=claim,
                status=status,
                evidence_ids=record_evidence,
                source_refs=source_refs,
                rationale=rationale,
            )
        )

    if required:
        for field_name in PROTECTED_CLAIM_FIELDS:
            if field_name not in seen_fields:
                findings.append(
                    f"uncertainty_register is missing protected claim {field_name}."
                )
    return records, findings


def _normalized_weights(config: Any) -> dict[str, float]:
    configured = getattr(config, "navigation_objective_weights", None)
    source = configured if isinstance(configured, Mapping) else DEFAULT_OBJECTIVE_WEIGHTS
    weights = {
        name: max(0.0, float(source.get(name, DEFAULT_OBJECTIVE_WEIGHTS[name])))
        for name in DEFAULT_OBJECTIVE_WEIGHTS
    }
    total = sum(weights.values())
    if total <= 0:
        return dict(DEFAULT_OBJECTIVE_WEIGHTS)
    return {name: value / total for name, value in weights.items()}


def _mean_dimension(dimensions: Mapping[str, Any], names: tuple[str, ...]) -> float:
    values: list[float] = []
    for name in names:
        if name not in dimensions:
            continue
        try:
            values.append(max(0.0, min(10.0, float(dimensions[name]))) / 10.0)
        except (TypeError, ValueError):
            continue
    return sum(values) / len(values) if values else 0.0


def compute_objective_scores(ctx: Any, config: Any) -> tuple[dict[str, float], float]:
    review = getattr(ctx, "integrated_review", {}) or {}
    dimensions = review.get("dimensions", {}) if isinstance(review, Mapping) else {}
    if not isinstance(dimensions, Mapping):
        dimensions = {}
    scores = {
        "truth": _mean_dimension(
            dimensions,
            (
                "textual_fidelity",
                "theological_accuracy",
                "canonical_warrant",
                "ontological_integrity",
                "affective_truth",
            ),
        ),
        "alignment": _mean_dimension(dimensions, ("blueprint_alignment",)),
        "literary": _mean_dimension(
            dimensions,
            (
                "verbal_economy",
                "literary_quality",
                "poetic_integrity",
                "sensory_presence",
                "read_aloud_flow",
                "historical_diction",
                "source_discipline",
            ),
        ),
        "safety": 1.0
        if not getattr(ctx, "failed_checks", [])
        and not getattr(ctx, "error", "")
        and getattr(ctx, "trace", [])
        and getattr(ctx, "trace", [])[-1] is State.DONE
        else 0.0,
        "provenance": 1.0 if getattr(ctx, "scripture_provenance", {}) else 0.0,
    }
    weights = _normalized_weights(config)
    aggregate = sum(scores[name] * weights[name] for name in weights)
    return scores, aggregate


class NavigationControlAdapter:
    """Observe, constrain, and audit the four-role devotional route."""

    def __init__(self, delegate: Any, ctx: Any, config: Any):
        self.delegate = delegate
        self.ctx = ctx
        self.config = config
        self.is_mock = _is_mock(delegate)
        mission = (
            f"Produce a biblically warranted, Christ-centered, pastorally responsible, "
            f"and literarily alive devotional for {getattr(ctx, 'chapter_ref', '')}."
        )
        self.state = NavigationState(
            mission=mission,
            objective_weights=_normalized_weights(config),
        )
        self._sync_context()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.delegate, name)

    def _contract(self, role: str) -> dict[str, Any]:
        return {
            "mission": self.state.mission,
            "current_checkpoint": ROLE_CHECKPOINTS[role],
            "route": list(self.state.route),
            "completed_checkpoints": [
                name
                for name in self.state.route
                if self.state.checkpoints[name].status is CheckpointStatus.PASSED
            ],
            "objective_weights": dict(self.state.objective_weights),
            "uncertainty_policy": {
                "statuses": sorted(UNCERTAINTY_STATUSES),
                "protected_claims": list(PROTECTED_CLAIM_FIELDS),
                "rule": (
                    "Do not advance a protected claim unless it is verified or a supported inference "
                    "with explicit evidence ids or source references."
                ),
            },
            "replanning_rule": (
                "Repair only the failed checkpoint and dependent fields. Preserve previously "
                "validated evidence, blueprint decisions, and unaffected artistic choices."
            ),
        }

    def _sync_context(self) -> None:
        self.ctx.navigation_state = self.state
        self.ctx.checkpoint_log = [
            self.state.checkpoints[name].as_dict() for name in self.state.route
        ]
        self.ctx.uncertainty_register = [
            item.as_dict() for item in self.state.uncertainty_register
        ]
        self.ctx.objective_scores = dict(self.state.objective_scores)

    def call(self, role: str, payload: dict[str, Any]) -> Any:
        self.state.enter_role(role, payload)
        call_payload = dict(payload)
        if not self.is_mock:
            call_payload["navigation_contract"] = self._contract(role)
        try:
            output = self.delegate.call(role, call_payload)
            if role == "devotional_grounder" and isinstance(output, Mapping):
                required = bool(
                    getattr(
                        self.config,
                        "navigation_require_uncertainty_register",
                        True,
                    )
                ) and not self.is_mock
                records, findings = validate_uncertainty_register(
                    output,
                    required=required,
                )
                if findings:
                    raise NavigationContractError("; ".join(findings))
                self.state.uncertainty_register = records
            self.state.complete_role(role, output)
            self._sync_context()
            return output
        except Exception as exc:
            self.state.fail_role(role, f"{type(exc).__name__}: {exc}")
            self._sync_context()
            raise


def finalize_navigation_state(ctx: Any, config: Any) -> Any:
    state = getattr(ctx, "navigation_state", None)
    if not isinstance(state, NavigationState):
        state = NavigationState(
            mission=(
                f"Produce a biblically warranted, Christ-centered, pastorally responsible, "
                f"and literarily alive devotional for {getattr(ctx, 'chapter_ref', '')}."
            ),
            objective_weights=_normalized_weights(config),
        )
        ctx.navigation_state = state

    trace = getattr(ctx, "trace", [])
    completed = bool(trace and trace[-1] is State.DONE)
    if not completed:
        findings = list(getattr(ctx, "failed_checks", []) or [])
        if not findings and getattr(ctx, "error", ""):
            findings = [str(ctx.error)]
        state.mark_system_checkpoint(
            "validation",
            CheckpointStatus.ESCALATED,
            findings=findings or ["The devotional did not reach DONE."],
        )
        state.terminal_status = "escalated"
        _sync_final_context(ctx, state)
        return ctx

    scores, aggregate = compute_objective_scores(ctx, config)
    state.objective_scores = scores
    state.aggregate_score = aggregate
    minimum = float(getattr(config, "navigation_min_objective_score", 0.85))
    hard_floor = float(getattr(config, "navigation_hard_floor", 0.80))
    failures: list[str] = []
    if aggregate < minimum:
        failures.append(
            f"Navigation objective score {aggregate:.3f} is below required {minimum:.3f}."
        )
    for name in ("truth", "alignment", "safety", "provenance"):
        if scores[name] < hard_floor:
            failures.append(
                f"Navigation objective {name} scored {scores[name]:.3f}, below hard floor {hard_floor:.3f}."
            )

    if failures and bool(getattr(config, "enforce_navigation_control", True)):
        ctx.failed_checks = list(getattr(ctx, "failed_checks", []) or []) + [
            f"[NAVIGATION] {message}" for message in failures
        ]
        ctx.error = "ValidationError: navigation objective gate failed"
        ctx.trace[-1] = State.ESCALATED
        state.mark_system_checkpoint(
            "validation",
            CheckpointStatus.FAILED,
            findings=failures,
            output=scores,
        )
        state.terminal_status = "escalated"
    else:
        state.mark_system_checkpoint(
            "validation",
            CheckpointStatus.PASSED,
            output=scores,
        )
        state.mark_system_checkpoint(
            "emission",
            CheckpointStatus.PASSED,
            output=getattr(ctx, "artifact", ""),
        )
        state.terminal_status = "done"
    _sync_final_context(ctx, state)
    return ctx


def _sync_final_context(ctx: Any, state: NavigationState) -> None:
    ctx.navigation_state = state
    ctx.checkpoint_log = [
        state.checkpoints[name].as_dict() for name in state.route
    ]
    ctx.uncertainty_register = [
        item.as_dict() for item in state.uncertainty_register
    ]
    ctx.objective_scores = {
        **state.objective_scores,
        "aggregate": state.aggregate_score,
    }
