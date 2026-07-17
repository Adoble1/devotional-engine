from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from .exceptions import ValidationError


_LIST_FIELDS = (
    "image_lexicon",
    "image_head_terms",
    "anchor_terms",
    "chapter_specific_terms",
    "christology_required_echoes",
    "negative_constraints",
    "semantic_proof_chain",
    "supporting_elements",
    "supporting_contrasts",
)

_CORE_SECTIONS = (
    "introduction",
    "reflection",
    "christ_fulfillment",
    "application",
    "prayer",
)

_REQUIRED_CENTER_FIELDS = (
    "governing_subject",
    "human_predicament",
    "textual_hinge",
    "divine_answer",
    "canonical_fulfillment",
    "reader_response",
)

_NEGATIVE_PREFIXES = (
    "do not ",
    "don't ",
    "never ",
    "avoid ",
    "exclude ",
    "omit ",
)

_POSITIVE_PREFIXES = (
    "must ",
    "require ",
    "include ",
    "use ",
    "preserve ",
    "keep ",
    "make ",
    "state ",
    "show ",
)

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "he",
    "her",
    "him",
    "his",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "their",
    "them",
    "they",
    "this",
    "through",
    "to",
    "was",
    "we",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "you",
    "your",
}


@dataclass(frozen=True)
class CoherenceFinding:
    code: str
    field: str
    message: str
    severity: str = "error"


def _as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def normalize_instruction(value: Any) -> str:
    text = str(value or "").lower().replace("’", "'")
    return " ".join(re.findall(r"[a-z0-9']+", text))


def dedupe_instructions(values: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        normalized = normalize_instruction(text)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(text)
    return result


def _directive_signature(value: Any) -> tuple[str, str]:
    normalized = normalize_instruction(value)
    for prefix in _NEGATIVE_PREFIXES:
        if normalized.startswith(prefix):
            return "negative", normalized[len(prefix) :].strip()
    for prefix in _POSITIVE_PREFIXES:
        if normalized.startswith(prefix):
            return "positive", normalized[len(prefix) :].strip()
    return "neutral", normalized


def find_instruction_conflicts(values: Iterable[Any]) -> list[tuple[str, str]]:
    positive: dict[str, str] = {}
    negative: dict[str, str] = {}
    for value in values:
        text = str(value or "").strip()
        polarity, core = _directive_signature(text)
        if len(core.split()) < 2:
            continue
        if polarity == "positive":
            positive.setdefault(core, text)
        elif polarity == "negative":
            negative.setdefault(core, text)
    return [(negative[core], positive[core]) for core in sorted(set(negative) & set(positive))]


def _content_terms(*values: Any) -> list[str]:
    terms: list[str] = []
    for value in values:
        for word in re.findall(r"[a-z]+", str(value or "").lower()):
            if len(word) >= 4 and word not in _STOPWORDS and word not in terms:
                terms.append(word)
    return terms


def _first_sentence(text: Any) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    match = re.search(r".+?[.!?](?:\s|$)", value, re.S)
    return match.group(0).strip() if match else value.splitlines()[0].strip()


def _sentences(text: Any) -> list[str]:
    value = str(text or "").strip()
    if not value:
        return []
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", value) if item.strip()]


def build_passage_center_map(ctx: Any, director_output: dict[str, Any]) -> dict[str, Any]:
    design = getattr(ctx, "chapter_design_map", {}) or {}
    supporting = _as_list(
        director_output.get("supporting_elements", director_output.get("supporting_contrasts", []))
    )
    governing_subject = str(
        director_output.get("governing_theme")
        or design.get("central_theological_claim")
        or director_output.get("central_thought", "")
    ).strip()
    human_predicament = str(
        director_output.get("human_predicament")
        or design.get("reader_felt_experience")
        or director_output.get("opening_movement", "")
    ).strip()
    textual_hinge = str(
        director_output.get("textual_hinge")
        or director_output.get("transcendent_force")
        or design.get("divine_action", "")
    ).strip()
    divine_answer = str(
        director_output.get("divine_answer")
        or design.get("divine_action")
        or director_output.get("closing_movement", "")
    ).strip()
    canonical_fulfillment = str(
        director_output.get("canonical_fulfillment")
        or director_output.get("christology_pathway")
        or design.get("christward_fulfillment", "")
    ).strip()
    reader_response = str(
        director_output.get("reader_response") or director_output.get("application_target", "")
    ).strip()
    resolution = str(
        director_output.get("resolution") or director_output.get("closing_movement", "")
    ).strip()

    section_burdens = {
        "introduction": str(director_output.get("opening_movement", "")).strip(),
        "reflection": governing_subject,
        "christ_fulfillment": canonical_fulfillment,
        "application": reader_response,
        "prayer": str(director_output.get("theological_terminus", "")).strip(),
        "poem": str(director_output.get("poem_plan", "")).strip(),
    }

    governing_terms = _content_terms(governing_subject, textual_hinge, divine_answer, resolution)
    supporting_terms = _content_terms(*supporting)

    return {
        "governing_subject": governing_subject,
        "human_predicament": human_predicament,
        "supporting_elements": dedupe_instructions(supporting),
        "textual_hinge": textual_hinge,
        "divine_answer": divine_answer,
        "resolution": resolution,
        "canonical_fulfillment": canonical_fulfillment,
        "reader_response": reader_response,
        "section_burdens": section_burdens,
        "governing_terms": governing_terms,
        "supporting_terms": supporting_terms,
    }


def prepare_art_direction(output: dict[str, Any]) -> dict[str, Any]:
    prepared = dict(output)
    prepared["avoid"] = dedupe_instructions(_as_list(prepared.get("avoid", [])))
    return prepared


def prepare_director_output(ctx: Any, output: dict[str, Any]) -> dict[str, Any]:
    prepared = dict(output)
    for field_name in _LIST_FIELDS:
        if field_name in prepared:
            prepared[field_name] = dedupe_instructions(_as_list(prepared[field_name]))

    art_avoid = _as_list((getattr(ctx, "art_direction", {}) or {}).get("avoid", []))
    local_constraints = _as_list(prepared.get("negative_constraints", []))
    prepared["effective_constraints"] = dedupe_instructions([*local_constraints, *art_avoid])
    prepared["passage_center_map"] = build_passage_center_map(ctx, prepared)
    return prepared


def audit_director_output(ctx: Any, output: dict[str, Any]) -> list[CoherenceFinding]:
    findings: list[CoherenceFinding] = []
    center_map = output.get("passage_center_map") or build_passage_center_map(ctx, output)

    for field_name in _REQUIRED_CENTER_FIELDS:
        if not str(center_map.get(field_name, "")).strip():
            findings.append(
                CoherenceFinding(
                    "C01",
                    f"passage_center_map.{field_name}",
                    "Passage center is incomplete before composition.",
                )
            )

    governing = normalize_instruction(center_map.get("governing_subject", ""))
    for item in _as_list(center_map.get("supporting_elements", [])):
        if governing and normalize_instruction(item) == governing:
            findings.append(
                CoherenceFinding(
                    "C02",
                    "passage_center_map.supporting_elements",
                    "A supporting element duplicates the governing subject instead of serving it.",
                )
            )

    burdens = center_map.get("section_burdens", {})
    burden_index: dict[str, list[str]] = defaultdict(list)
    if isinstance(burdens, dict):
        for section, burden in burdens.items():
            normalized = normalize_instruction(burden)
            if len(normalized.split()) >= 4:
                burden_index[normalized].append(str(section))
    for sections in burden_index.values():
        if len(sections) > 1:
            findings.append(
                CoherenceFinding(
                    "C03",
                    "passage_center_map.section_burdens",
                    f"Sections repeat the same burden: {', '.join(sections)}.",
                )
            )

    constraints = _as_list(output.get("effective_constraints", []))
    for negative, positive in find_instruction_conflicts(constraints):
        findings.append(
            CoherenceFinding(
                "C04",
                "effective_constraints",
                f"Contradictory instructions: {negative!r} conflicts with {positive!r}.",
            )
        )

    normalized_constraints = [normalize_instruction(item) for item in constraints]
    if len(normalized_constraints) != len(set(normalized_constraints)):
        findings.append(
            CoherenceFinding(
                "C05",
                "effective_constraints",
                "Duplicate instructions remain after compilation.",
            )
        )
    return findings


def audit_prose(ctx: Any, prose: dict[str, Any], config: Any) -> list[CoherenceFinding]:
    findings: list[CoherenceFinding] = []
    title = normalize_instruction(prose.get("title", ""))
    epigraph = normalize_instruction(prose.get("epigraph", ""))
    opening = normalize_instruction(_first_sentence(prose.get("introduction", "")))

    if getattr(config, "enforce_title_opening_distinction", True) and title and opening:
        if title == opening:
            findings.append(
                CoherenceFinding(
                    "C10",
                    "introduction",
                    "The title and opening sentence must perform different work.",
                )
            )
    if getattr(config, "enforce_title_opening_distinction", True) and title and epigraph:
        if title == epigraph:
            findings.append(
                CoherenceFinding(
                    "C11",
                    "epigraph",
                    "The title and epigraph must not duplicate one another.",
                )
            )

    if getattr(config, "warn_cross_section_repetition", True):
        source = normalize_instruction(
            f"{getattr(ctx, 'source_text', '')} {getattr(ctx, 'working_rendering', '')}"
        )
        sentence_locations: dict[str, list[str]] = defaultdict(list)
        for section in _CORE_SECTIONS:
            for sentence in _sentences(prose.get(section, "")):
                normalized = normalize_instruction(sentence)
                if len(normalized.split()) < 7:
                    continue
                if normalized and normalized in source:
                    continue
                sentence_locations[normalized].append(section)
        repeated = [locations for locations in sentence_locations.values() if len(set(locations)) > 1]
        if repeated:
            locations = sorted(set(repeated[0]))
            findings.append(
                CoherenceFinding(
                    "C12",
                    "prose",
                    f"A full sentence is repeated across sections: {', '.join(locations)}.",
                    severity="warning",
                )
            )

    center_map = (getattr(ctx, "brief", {}) or {}).get("passage_center_map", {})
    reflection = str(prose.get("reflection", "")).lower()
    governing_terms = [str(term).lower() for term in _as_list(center_map.get("governing_terms", []))]
    supporting_terms = [str(term).lower() for term in _as_list(center_map.get("supporting_terms", []))]

    if governing_terms:
        covered = sum(1 for term in governing_terms if re.search(rf"\b{re.escape(term)}\b", reflection))
        required = 1 if len(governing_terms) == 1 else 2
        if covered < required:
            findings.append(
                CoherenceFinding(
                    "C13",
                    "reflection",
                    "The reflection does not carry enough of the approved passage center.",
                    severity="warning",
                )
            )

    if getattr(config, "warn_theme_displacement", True) and governing_terms and supporting_terms:
        governing_mentions = sum(len(re.findall(rf"\b{re.escape(term)}\b", reflection)) for term in governing_terms)
        supporting_mentions = sum(len(re.findall(rf"\b{re.escape(term)}\b", reflection)) for term in supporting_terms)
        if supporting_mentions > max(governing_mentions * 2, 4):
            findings.append(
                CoherenceFinding(
                    "C14",
                    "reflection",
                    "Supporting material appears to displace the governing subject.",
                    severity="warning",
                )
            )
    return findings


class CoherenceGateAdapter:
    """v6.5 adapter decorator that compiles and enforces one coherence contract."""

    def __init__(self, delegate: Any, config: Any):
        self.delegate = delegate
        self.config = config

    def _record_or_raise(self, ctx: Any, findings: list[CoherenceFinding]) -> None:
        errors = [finding for finding in findings if finding.severity == "error"]
        warnings = [finding for finding in findings if finding.severity != "error"]
        if ctx is not None:
            ctx.warnings.extend(
                f"COHERENCE {finding.code}: {finding.field}: {finding.message}" for finding in warnings
            )
        if errors and getattr(self.config, "enforce_instruction_coherence", True):
            summary = "; ".join(f"{item.code} {item.field}: {item.message}" for item in errors)
            raise ValidationError(summary)

    def call(self, role: str, payload: dict[str, Any]) -> dict[str, Any]:
        ctx = payload.get("context")
        result = self.delegate.call(role, payload)

        if role == "art_director" and isinstance(result, dict):
            return prepare_art_direction(result)

        if role == "director" and isinstance(result, dict):
            prepared = prepare_director_output(ctx, result)
            self._record_or_raise(ctx, audit_director_output(ctx, prepared))
            return prepared

        if role == "composer" and isinstance(result, dict):
            self._record_or_raise(ctx, audit_prose(ctx, result, self.config))
            return result

        return result
