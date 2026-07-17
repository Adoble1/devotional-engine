from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .exceptions import ValidationError


PUBLICATION_MODES = {
    "public_domain",
    "licensed",
    "independent_rendering",
    "paraphrase",
}
ALL_MODES = PUBLICATION_MODES | {"test_fixture"}


@dataclass(frozen=True)
class ScriptureProvenance:
    quotation_mode: str
    attribution: str
    translation_id: str = ""
    edition: str = ""
    source_text_id: str = ""
    license_profile: str = ""
    verified_exact_match: bool = False
    human_review_required: bool = False

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ScriptureProvenance":
        return cls(
            quotation_mode=str(value.get("quotation_mode", "")).strip(),
            attribution=str(value.get("attribution", "")).strip(),
            translation_id=str(value.get("translation_id", "")).strip(),
            edition=str(value.get("edition", "")).strip(),
            source_text_id=str(value.get("source_text_id", "")).strip(),
            license_profile=str(value.get("license_profile", "")).strip(),
            verified_exact_match=value.get("verified_exact_match") is True,
            human_review_required=value.get("human_review_required") is True,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_provenance_record(
    value: Mapping[str, Any] | None,
    *,
    allow_test_fixture: bool = False,
) -> list[str]:
    if not isinstance(value, Mapping):
        return ["Scripture provenance must be a dictionary."]

    record = ScriptureProvenance.from_mapping(value)
    failures: list[str] = []

    if record.quotation_mode not in ALL_MODES:
        failures.append(
            "quotation_mode must be public_domain, licensed, independent_rendering, paraphrase, or test_fixture."
        )
        return failures
    if not record.attribution:
        failures.append("attribution is required.")

    if record.quotation_mode == "public_domain":
        if not record.translation_id:
            failures.append("public-domain Scripture requires translation_id.")
        if not record.edition:
            failures.append("public-domain Scripture requires edition.")
        if not record.verified_exact_match:
            failures.append("public-domain quotation must be verified_exact_match.")

    elif record.quotation_mode == "licensed":
        if not record.translation_id:
            failures.append("licensed Scripture requires translation_id.")
        if not record.edition:
            failures.append("licensed Scripture requires edition.")
        if not record.license_profile:
            failures.append("licensed Scripture requires license_profile.")
        if not record.verified_exact_match:
            failures.append("licensed quotation must be verified_exact_match.")

    elif record.quotation_mode == "independent_rendering":
        if not record.source_text_id:
            failures.append("independent rendering requires source_text_id.")
        if not record.human_review_required:
            failures.append("independent rendering must require human review.")

    elif record.quotation_mode == "paraphrase":
        if not (record.source_text_id or record.translation_id):
            failures.append("paraphrase requires source_text_id or translation_id.")
        if not record.human_review_required:
            failures.append("paraphrase must require human review.")

    elif record.quotation_mode == "test_fixture":
        if not allow_test_fixture:
            failures.append("test_fixture provenance is forbidden for production adapters.")
        if not record.human_review_required:
            failures.append("test_fixture material must require human review.")

    return failures


def normalize_provenance_record(value: Mapping[str, Any]) -> dict[str, Any]:
    return ScriptureProvenance.from_mapping(value).to_dict()


def _is_mock_adapter(adapter: Any) -> bool:
    current = adapter
    for _ in range(6):
        if current is None:
            break
        if current.__class__.__name__ == "MockAgentAdapter":
            return True
        current = getattr(current, "delegate", None)
    return False


def _test_fixture_record(role: str) -> dict[str, Any]:
    return ScriptureProvenance(
        quotation_mode="test_fixture",
        attribution="Deterministic mock Scripture fixture; not for publication",
        translation_id="mock-fixture" if role == "source_agent" else "",
        edition="test-only fixture" if role == "source_agent" else "",
        source_text_id="mock-source" if role == "translator" else "",
        verified_exact_match=role == "source_agent",
        human_review_required=True,
    ).to_dict()


def validate_scripture_context(ctx: Any) -> list[str]:
    provenance = getattr(ctx, "scripture_provenance", {}) or {}
    failures: list[str] = []
    for key in ("source", "rendering"):
        record = provenance.get(key)
        for message in validate_provenance_record(record, allow_test_fixture=True):
            failures.append(f"{key}: {message}")
    if not provenance.get("focus"):
        failures.append("focus: Scripture focus text has no selected provenance record.")
    return failures


def scripture_attribution(ctx: Any) -> str:
    provenance = getattr(ctx, "scripture_provenance", {}) or {}
    focus = provenance.get("focus") or provenance.get("rendering") or provenance.get("source") or {}
    return str(focus.get("attribution", "")).strip()


class ScriptureProvenanceAdapter:
    """Adapter decorator that fails closed when biblical wording lacks provenance."""

    def __init__(self, delegate: Any, config: Any):
        self.delegate = delegate
        self.config = config
        self.allow_test_fixture = _is_mock_adapter(delegate)

    def call(self, role: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = self.delegate.call(role, payload)
        if role not in {"source_agent", "translator"} or not isinstance(result, dict):
            return result

        record = result.get("scripture_provenance")
        if record is None and self.allow_test_fixture:
            record = _test_fixture_record(role)
            result["scripture_provenance"] = record

        failures = validate_provenance_record(
            record,
            allow_test_fixture=self.allow_test_fixture,
        )
        if failures and getattr(self.config, "enforce_scripture_provenance", True):
            summary = "; ".join(failures)
            raise ValidationError(f"{role} Scripture provenance invalid: {summary}")

        if not isinstance(record, Mapping):
            return result

        ctx = payload.get("context")
        if ctx is not None:
            normalized = normalize_provenance_record(record)
            slot = "source" if role == "source_agent" else "rendering"
            ctx.scripture_provenance[slot] = normalized
            if slot == "rendering" or "focus" not in ctx.scripture_provenance:
                ctx.scripture_provenance["focus"] = normalized

        return result
