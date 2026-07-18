from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .config import EngineConfig
from .scripture import validate_provenance_record
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
SOURCE_LANGUAGES = {"hebrew", "aramaic", "greek"}
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


@dataclass(frozen=True)
class IntegratedFinding:
    code: str
    field: str
    message: str
    severity: str = "error"
    repair_target: str = "draft"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]


def _missing(
    mapping: Mapping[str, Any],
    fields: tuple[str, ...],
    code: str,
    target: str,
) -> list[IntegratedFinding]:
    return [
        IntegratedFinding(code, name, "Required field is missing.", repair_target=target)
        for name in fields
        if mapping.get(name) in (None, "", [], {})
    ]


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
    """Real adapters use the integrated core; old mocks use compatibility."""

    current = adapter
    for _ in range(6):
        outputs = getattr(current, "outputs", None)
        if isinstance(outputs, Mapping):
            return all(role in outputs for role in INTEGRATED_ROLES)
        current = getattr(current, "delegate", None)
        if current is None:
            break
    return True


def _validate_lexical_insight(
    packet: Mapping[str, Any],
    *,
    allow_test_fixture: bool,
) -> list[IntegratedFinding]:
    insight = packet.get("lexical_insight")
    if insight in (None, "", {}, []):
        if allow_test_fixture:
            return []
        return [
            IntegratedFinding(
                "G08",
                "lexical_insight",
                "One standard, source-language lexical insight is required for production devotionals.",
                repair_target="grounding",
            )
        ]
    if not isinstance(insight, Mapping):
        return [
            IntegratedFinding(
                "G08",
                "lexical_insight",
                "Lexical insight must be a dictionary.",
                repair_target="grounding",
            )
        ]

    required = ("source_language", "term", "observation", "argument_role")
    findings = [
        IntegratedFinding(
            "G08",
            f"lexical_insight.{name}",
            "Lexical insight field is required.",
            repair_target="grounding",
        )
        for name in required
        if not _text(insight.get(name))
    ]
    language = _text(insight.get("source_language")).lower()
    if language and language not in SOURCE_LANGUAGES:
        findings.append(
            IntegratedFinding(
                "G09",
                "lexical_insight.source_language",
                "Source language must be Hebrew, Aramaic, or Greek.",
                repair_target="grounding",
            )
        )
    return findings


def validate_grounding(
    packet: Mapping[str, Any],
    *,
    allow_test_fixture: bool,
    config: EngineConfig,
) -> list[IntegratedFinding]:
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
        findings.append(
            IntegratedFinding(
                "G02",
                "source_text",
                "Source text is too short.",
                repair_target="grounding",
            )
        )

    for name in ("source_provenance", "rendering_provenance"):
        record = packet.get(name)
        failures = validate_provenance_record(
            record if isinstance(record, Mapping) else None,
            allow_test_fixture=allow_test_fixture,
        )
        findings.extend(
            IntegratedFinding("G03", name, message, repair_target="grounding")
            for message in failures
        )

    ids: set[str] = set()
    for index, item in enumerate(_list(packet.get("textual_evidence"))):
        if not isinstance(item, Mapping) or not all(
            _text(item.get(key)) for key in ("id", "reference", "claim")
        ):
            findings.append(
                IntegratedFinding(
                    "G04",
                    f"textual_evidence.{index}",
                    "Evidence requires id, reference, and claim.",
                    repair_target="grounding",
                )
            )
            continue
        evidence_id = _text(item.get("id"))
        if evidence_id in ids:
            findings.append(
                IntegratedFinding(
                    "G05",
                    f"textual_evidence.{index}.id",
                    "Evidence ids must be unique.",
                    repair_target="grounding",
                )
            )
        ids.add(evidence_id)

    canonical = packet.get("canonical_relationship")
    if isinstance(canonical, Mapping):
        if _text(canonical.get("classification")) not in CANONICAL_RELATIONSHIPS:
            findings.append(
                IntegratedFinding(
                    "G06",
                    "canonical_relationship.classification",
                    "Invalid canonical relationship.",
                    repair_target="grounding",
                )
            )
        if not _text(canonical.get("description")):
            findings.append(
                IntegratedFinding(
                    "G06",
                    "canonical_relationship.description",
                    "Canonical description is required.",
                    repair_target="grounding",
                )
            )

    for index, risk in enumerate(_list(packet.get("risks"))):
        if not isinstance(risk, Mapping) or not all(
            _text(risk.get(key)) for key in ("risk_description", "avoidance_rule")
        ):
            findings.append(
                IntegratedFinding(
                    "G07",
                    f"risks.{index}",
                    "Risk requires description and avoidance rule.",
                    repair_target="grounding",
                )
            )

    findings.extend(
        _validate_lexical_insight(
            packet,
            allow_test_fixture=allow_test_fixture,
        )
    )
    return findings


def _review_finding(item: Any, severity: str) -> IntegratedFinding:
    if isinstance(item, Mapping):
        return IntegratedFinding(
            _text(item.get("code")) or "R01",
            _text(item.get("field")) or "draft",
            _text(item.get("message")) or "Review finding.",
            severity,
            _text(item.get("repair_target")) or "draft",
        )
    return IntegratedFinding(
        "R01",
        "draft",
        _text(item) or "Review finding.",
        severity,
    )


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
