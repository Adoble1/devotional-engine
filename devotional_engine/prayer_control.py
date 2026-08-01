from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .integrated import _is_mock, _list, _text


PRAYER_MODE = "chapter_shaped_corporate"
PRAYER_VOICE = "first_person_plural"
APPROVED_ADDRESSES = {"our father", "father", "abba father"}
PRAYER_FUNCTIONS = {
    "adoration",
    "confession",
    "lament",
    "intercession",
    "petition",
    "dependence",
    "human_response",
    "christological_resolution",
    "assurance",
    "submission",
    "thanksgiving",
    "doxology",
}
PRAYER_ENDINGS = {
    "lament",
    "christological_resolution",
    "assurance",
    "submission",
    "thanksgiving",
    "doxology",
}


class ChapterPrayerError(ValueError):
    """Raised when a production prayer is detached from its chapter."""


@dataclass(frozen=True)
class ChapterPrayerFinding:
    code: str
    field: str
    message: str


def _evidence_ids(grounding: Mapping[str, Any]) -> set[str]:
    return {
        _text(item.get("id"))
        for item in _list(grounding.get("textual_evidence"))
        if isinstance(item, Mapping) and _text(item.get("id"))
    }


def _normalize_address(value: Any) -> dict[str, Any]:
    source = dict(value) if isinstance(value, Mapping) else {}
    return {
        "opening": _text(source.get("opening")),
        "divine_identity": _text(source.get("divine_identity")),
        "evidence_ids": [
            _text(item) for item in _list(source.get("evidence_ids")) if _text(item)
        ],
    }


def _normalize_movements(value: Any) -> list[dict[str, Any]]:
    movements: list[dict[str, Any]] = []
    for item in _list(value):
        if not isinstance(item, Mapping):
            continue
        position_value = item.get("chapter_position")
        try:
            position = int(position_value)
        except (TypeError, ValueError):
            position = 0
        movements.append(
            {
                "function": _text(item.get("function")).lower(),
                "chapter_position": position,
                "chapter_action": _text(item.get("chapter_action")),
                "prayer_transformation": _text(item.get("prayer_transformation")),
                "evidence_ids": [
                    _text(entry)
                    for entry in _list(item.get("evidence_ids"))
                    if _text(entry)
                ],
                "source_refs": [
                    _text(entry)
                    for entry in _list(item.get("source_refs"))
                    if _text(entry)
                ],
            }
        )
    return movements


def _normalize_target_words(value: Any) -> dict[str, int]:
    source = dict(value) if isinstance(value, Mapping) else {}
    try:
        minimum = int(source.get("minimum", 90))
    except (TypeError, ValueError):
        minimum = 0
    try:
        maximum = int(source.get("maximum", 150))
    except (TypeError, ValueError):
        maximum = 0
    return {"minimum": minimum, "maximum": maximum}


def validate_prayer_design(
    plan: Mapping[str, Any],
    grounding: Mapping[str, Any],
    *,
    required: bool = True,
) -> tuple[dict[str, Any], list[ChapterPrayerFinding]]:
    design_value = plan.get("prayer_design")
    design = dict(design_value) if isinstance(design_value, Mapping) else {}
    normalized = {
        "mode": _text(design.get("mode")).lower(),
        "voice": _text(design.get("voice")).lower(),
        "address": _normalize_address(design.get("address")),
        "movements": _normalize_movements(design.get("movements")),
        "target_words": _normalize_target_words(design.get("target_words")),
    }
    findings: list[ChapterPrayerFinding] = []
    known_ids = _evidence_ids(grounding)

    if required and normalized["mode"] != PRAYER_MODE:
        findings.append(ChapterPrayerFinding(
            "CP01",
            "prayer_design.mode",
            f"Production prayer mode must be {PRAYER_MODE}.",
        ))
    if required and normalized["voice"] != PRAYER_VOICE:
        findings.append(ChapterPrayerFinding(
            "CP02",
            "prayer_design.voice",
            f"Production prayer voice must be {PRAYER_VOICE}.",
        ))

    address = normalized["address"]
    if required and address["opening"].lower().rstrip(",") not in APPROVED_ADDRESSES:
        findings.append(ChapterPrayerFinding(
            "CP03",
            "prayer_design.address.opening",
            "Prayer must begin with Our Father, Father, or Abba Father.",
        ))
    if required and not address["divine_identity"]:
        findings.append(ChapterPrayerFinding(
            "CP03",
            "prayer_design.address.divine_identity",
            "The address must name God as the chapter reveals Him.",
        ))
    if required and not address["evidence_ids"]:
        findings.append(ChapterPrayerFinding(
            "CP04",
            "prayer_design.address.evidence_ids",
            "The divine identity in the address must cite chapter evidence.",
        ))
    unknown_address = sorted(set(address["evidence_ids"]) - known_ids)
    if unknown_address:
        findings.append(ChapterPrayerFinding(
            "CP05",
            "prayer_design.address.evidence_ids",
            f"Prayer address cites unknown evidence ids: {', '.join(unknown_address)}.",
        ))

    movements = normalized["movements"]
    if required and len(movements) < 3:
        findings.append(ChapterPrayerFinding(
            "CP06",
            "prayer_design.movements",
            "A chapter-shaped prayer needs at least three distinct movements from the chapter.",
        ))

    previous_position = 0
    functions: list[str] = []
    for index, movement in enumerate(movements):
        prefix = f"prayer_design.movements.{index}"
        functions.append(movement["function"])
        for field in ("function", "chapter_action", "prayer_transformation"):
            if not movement[field]:
                findings.append(ChapterPrayerFinding(
                    "CP07",
                    f"{prefix}.{field}",
                    "Each prayer movement must name its function, chapter action, and first-person-plural transformation.",
                ))
        if movement["function"] and movement["function"] not in PRAYER_FUNCTIONS:
            findings.append(ChapterPrayerFinding(
                "CP08",
                f"{prefix}.function",
                "Unsupported prayer function.",
            ))
        position = movement["chapter_position"]
        if position <= 0 or position <= previous_position:
            findings.append(ChapterPrayerFinding(
                "CP09",
                f"{prefix}.chapter_position",
                "Prayer movements must follow the chapter in strictly increasing order.",
            ))
        previous_position = max(previous_position, position)
        if not movement["evidence_ids"] and not movement["source_refs"]:
            findings.append(ChapterPrayerFinding(
                "CP10",
                f"{prefix}.evidence_ids",
                "Every major prayer movement must cite chapter evidence or a validated canonical source.",
            ))
        unknown = sorted(set(movement["evidence_ids"]) - known_ids)
        if unknown:
            findings.append(ChapterPrayerFinding(
                "CP11",
                f"{prefix}.evidence_ids",
                f"Prayer movement cites unknown evidence ids: {', '.join(unknown)}.",
            ))
        if movement["function"] == "christological_resolution" and not movement["source_refs"]:
            findings.append(ChapterPrayerFinding(
                "CP12",
                f"{prefix}.source_refs",
                "A Christological prayer movement must cite its canonical source reference.",
            ))

    if required and "human_response" not in functions:
        findings.append(ChapterPrayerFinding(
            "CP13",
            "prayer_design.movements",
            "The prayer must include a human-response movement, not petition alone.",
        ))
    if required and movements and movements[-1]["function"] not in PRAYER_ENDINGS:
        findings.append(ChapterPrayerFinding(
            "CP14",
            "prayer_design.movements",
            "The final movement must reach the chapter's own lament, assurance, submission, thanksgiving, Christological resolution, or doxology.",
        ))

    canonical = grounding.get("canonical_relationship")
    canonical = dict(canonical) if isinstance(canonical, Mapping) else {}
    classification = _text(canonical.get("classification")).lower()
    if required and classification and classification != "no_identified_link":
        if "christological_resolution" not in functions:
            findings.append(ChapterPrayerFinding(
                "CP15",
                "prayer_design.movements",
                "A validated canonical pathway requires a Christological resolution in the prayer design.",
            ))

    target = normalized["target_words"]
    if target["minimum"] < 60 or target["maximum"] > 220 or target["minimum"] > target["maximum"]:
        findings.append(ChapterPrayerFinding(
            "CP16",
            "prayer_design.target_words",
            "Prayer target must be a coherent range between 60 and 220 words.",
        ))

    return normalized, findings


def build_prayer_contract(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "governing_rule": (
            "Convert the chapter's movement into first-person-plural prayer, preserving its order, "
            "emphasis, responsibility, canonical resolution, and emotional destination."
        ),
        "mode": design["mode"],
        "voice": design["voice"],
        "address": deepcopy(design["address"]),
        "movements": deepcopy(design["movements"]),
        "target_words": dict(design["target_words"]),
        "required_elements": [
            "chapter_arc_order",
            "corporate_voice",
            "divine_action",
            "human_response",
            "canonical_warrant",
            "chapter_specific_close",
        ],
        "boundary": (
            "Do not add generic petitions that could move unchanged to another chapter. "
            "Do not quote mechanically when prayerful transformation can preserve the chapter's force."
        ),
    }


def _append_instruction(existing: Any, addition: str) -> str:
    current = _text(existing)
    return f"{current} {addition}".strip()


def audit_prayer_text(prayer: str, contract: Mapping[str, Any]) -> list[ChapterPrayerFinding]:
    text = _text(prayer)
    findings: list[ChapterPrayerFinding] = []
    lowered = text.lower()
    if not any(lowered.startswith(f"{opening},") for opening in APPROVED_ADDRESSES):
        findings.append(ChapterPrayerFinding(
            "CP_D01",
            "prayer",
            "Prayer must begin with Our Father, Father, or Abba Father followed by a comma.",
        ))
    plural_count = len(re.findall(r"\b(?:we|us|our|ours)\b", lowered))
    singular_count = len(re.findall(r"\b(?:i|me|my|mine)\b", lowered))
    if plural_count < 3 or singular_count > plural_count:
        findings.append(ChapterPrayerFinding(
            "CP_D02",
            "prayer",
            "Prayer must remain predominantly first-person plural.",
        ))
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ’'-]+", text)
    target = contract.get("target_words", {})
    target = dict(target) if isinstance(target, Mapping) else {}
    minimum = int(target.get("minimum", 90))
    maximum = int(target.get("maximum", 150))
    if len(words) < minimum or len(words) > maximum:
        findings.append(ChapterPrayerFinding(
            "CP_D03",
            "prayer",
            f"Prayer has {len(words)} words; target range is {minimum}-{maximum}.",
        ))
    if not re.search(r"\bamen\.?$", lowered):
        findings.append(ChapterPrayerFinding(
            "CP_D04",
            "prayer",
            "Prayer must end with Amen.",
        ))
    return findings


class ChapterPrayerAdapter:
    """Require production prayers to emerge from the chapter's own arc."""

    def __init__(self, delegate: Any, ctx: Any, config: Any):
        self.delegate = delegate
        self.ctx = ctx
        self.config = config
        self.is_mock = _is_mock(delegate)
        self.grounding: dict[str, Any] = {}
        self.contract: dict[str, Any] = {}
        self.draft_findings: list[ChapterPrayerFinding] = []

    def __getattr__(self, name: str) -> Any:
        return getattr(self.delegate, name)

    def _planner_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        addition = (
            "Add prayer_design with mode chapter_shaped_corporate, voice first_person_plural, a chapter-warranted "
            "address, ordered movements, and a 90-150 word target unless the chapter requires a nearby adjustment. "
            "Each movement must include function, chapter_position, chapter_action, prayer_transformation, and "
            "evidence_ids or canonical source_refs. Follow the chapter's rhetorical or narrative order. Include "
            "dependence on God and a human-response movement. Use the validated canonical pathway for Christ, then "
            "end where the chapter ends emotionally and theologically. Do not add generic petitions that could be "
            "moved unchanged to another chapter."
        )
        enriched["planning_instruction"] = _append_instruction(
            enriched.get("planning_instruction"), addition
        )
        return enriched

    def _composer_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        packet = dict(enriched.get("composition_packet", {}))
        packet["chapter_prayer_contract"] = deepcopy(self.contract)
        packet["prayer_instruction"] = (
            "Write the prayer from the chapter_prayer_contract. Begin with the approved address. Convert each "
            "major chapter action into concise first-person-plural prayer in the supplied order. Preserve both "
            "God's sovereign action and the worshiper's faithful response. Include Christ only through the "
            "validated canonical pathway. Reach the chapter's own destination and close with Amen."
        )
        enriched["composition_packet"] = packet
        return enriched

    def _reviewer_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        enriched["chapter_prayer_contract"] = deepcopy(self.contract)
        enriched["chapter_prayer_findings"] = [item.__dict__ for item in self.draft_findings]
        addition = (
            "Score dimensions.chapter_shaped_prayer from 0 to 10. Confirm that the prayer is predominantly "
            "first-person plural, follows the chapter's movement in order, transforms rather than merely quotes "
            "its major actions, includes both dependence and faithful response, uses the validated canonical "
            "pathway, remains concise, and ends at the chapter's own theological and emotional destination. "
            "A prayer that could move unchanged to many chapters must not pass."
        )
        enriched["review_instruction"] = _append_instruction(
            enriched.get("review_instruction"), addition
        )
        return enriched

    def _enforce_review_dimension(self, review: Mapping[str, Any]) -> dict[str, Any]:
        normalized = deepcopy(dict(review))
        dimensions_value = normalized.get("dimensions")
        dimensions = dict(dimensions_value) if isinstance(dimensions_value, Mapping) else {}
        hard = [
            dict(item) if isinstance(item, Mapping) else {"message": _text(item)}
            for item in _list(normalized.get("hard_findings"))
        ]
        hard.extend(
            {
                "code": item.code,
                "field": item.field,
                "message": item.message,
                "repair_target": "prayer",
            }
            for item in self.draft_findings
        )
        verdict = _text(normalized.get("verdict")).lower()
        minimum = float(getattr(self.config, "integrated_review_min_score", 8.0))
        score_value = dimensions.get("chapter_shaped_prayer")
        try:
            score: float | None = float(score_value)
        except (TypeError, ValueError):
            score = None

        if score is None:
            hard.append({
                "code": "CP_R01",
                "field": "dimensions.chapter_shaped_prayer",
                "message": "Reviewer must score chapter-shaped prayer.",
                "repair_target": "prayer",
            })
        elif verdict == "pass" and score < minimum:
            hard.append({
                "code": "CP_R02",
                "field": "dimensions.chapter_shaped_prayer",
                "message": (
                    f"Chapter-shaped prayer score {score:g} is below the configured minimum {minimum:g}; "
                    "revise the prayer without changing approved grounding or prose."
                ),
                "repair_target": "prayer",
            })

        if hard and verdict == "pass":
            normalized["verdict"] = "Revise"
        normalized["hard_findings"] = hard
        if self.ctx is not None:
            scores = getattr(self.ctx, "scores", None)
            if isinstance(scores, dict):
                scores["chapter_shaped_prayer"] = score
        return normalized

    def call(self, role: str, payload: dict[str, Any]) -> Any:
        if self.is_mock:
            return self.delegate.call(role, payload)

        if role == "devotional_grounder":
            output = self.delegate.call(role, payload)
            if isinstance(output, Mapping):
                self.grounding = dict(output)
            return output

        if role == "devotional_planner":
            output = self.delegate.call(role, self._planner_payload(payload))
            if not isinstance(output, Mapping):
                return output
            grounding_value = payload.get("grounding")
            grounding = (
                dict(grounding_value)
                if isinstance(grounding_value, Mapping)
                else self.grounding
            )
            design, findings = validate_prayer_design(output, grounding, required=True)
            if findings:
                raise ChapterPrayerError(
                    "; ".join(f"{item.field}: {item.message}" for item in findings)
                )
            normalized = deepcopy(dict(output))
            normalized["prayer_design"] = design
            self.contract = build_prayer_contract(design)
            if self.ctx is not None:
                setattr(self.ctx, "chapter_prayer_contract", deepcopy(self.contract))
            return normalized

        if role == "devotional_composer":
            output = self.delegate.call(role, self._composer_payload(payload))
            if isinstance(output, Mapping):
                self.draft_findings = audit_prayer_text(
                    _text(output.get("prayer")),
                    self.contract,
                )
            return output

        if role == "devotional_reviewer":
            output = self.delegate.call(role, self._reviewer_payload(payload))
            if isinstance(output, Mapping):
                return self._enforce_review_dimension(output)
            return output

        return self.delegate.call(role, payload)
