from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .integrated import _is_mock, _list, _text


POETIC_OPERATIONS = {
    "compression",
    "metrical_paraphrase",
    "bounded_implication",
    "personification",
    "contrast",
    "refrain",
    "canonical_echo",
}
POETIC_STRATEGY_FIELDS = (
    "genre_force",
    "emotional_tone",
    "formal_strategy",
    "discovery",
)


class PoeticTransformationError(ValueError):
    """Raised when poetic freedom is detached from textual warrant."""


@dataclass(frozen=True)
class PoeticTransformationFinding:
    code: str
    field: str
    message: str


def _evidence_ids(grounding: Mapping[str, Any]) -> set[str]:
    return {
        _text(item.get("id"))
        for item in _list(grounding.get("textual_evidence"))
        if isinstance(item, Mapping) and _text(item.get("id"))
    }


def _normalize_transformations(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in _list(value):
        if not isinstance(item, Mapping):
            continue
        records.append(
            {
                "phrase": _text(item.get("phrase")),
                "operation": _text(item.get("operation")).lower(),
                "textual_anchor": _text(item.get("textual_anchor")),
                "warrant_ids": [
                    _text(entry)
                    for entry in _list(item.get("warrant_ids"))
                    if _text(entry)
                ],
                "source_refs": [
                    _text(entry)
                    for entry in _list(item.get("source_refs"))
                    if _text(entry)
                ],
                "rationale": _text(item.get("rationale")),
            }
        )
    return records


def validate_poetic_contract(
    plan: Mapping[str, Any],
    grounding: Mapping[str, Any],
    *,
    required: bool = True,
) -> tuple[dict[str, str], list[dict[str, Any]], list[PoeticTransformationFinding]]:
    """Validate positive poetic craft without turning it into an image quota.

    A planner may supply no transformations when exact diction, refrain, or silence
    is sufficient. When it does transform passage language, each transformation
    must identify the operation and its textual or canonical warrant.
    """

    poem_design = plan.get("poem_design")
    poem_design = dict(poem_design) if isinstance(poem_design, Mapping) else {}
    strategy_value = poem_design.get("poetic_strategy")
    strategy_value = (
        dict(strategy_value) if isinstance(strategy_value, Mapping) else {}
    )
    strategy = {
        field: _text(strategy_value.get(field)) for field in POETIC_STRATEGY_FIELDS
    }
    transformations = _normalize_transformations(
        poem_design.get("poetic_transformations")
    )
    findings: list[PoeticTransformationFinding] = []

    if required:
        for field in POETIC_STRATEGY_FIELDS:
            if not strategy[field]:
                findings.append(
                    PoeticTransformationFinding(
                        "PT01",
                        f"poem_design.poetic_strategy.{field}",
                        "Production poem design must state its genre force, emotional tone, formal strategy, and discovery.",
                    )
                )

    known_ids = _evidence_ids(grounding)
    for index, record in enumerate(transformations):
        prefix = f"poem_design.poetic_transformations.{index}"
        for field in ("phrase", "operation", "textual_anchor", "rationale"):
            if not record[field]:
                findings.append(
                    PoeticTransformationFinding(
                        "PT02",
                        f"{prefix}.{field}",
                        "Every poetic transformation must name its phrase, operation, textual anchor, and rationale.",
                    )
                )
        if record["operation"] and record["operation"] not in POETIC_OPERATIONS:
            findings.append(
                PoeticTransformationFinding(
                    "PT03",
                    f"{prefix}.operation",
                    "Unsupported poetic operation. Use compression, metrical paraphrase, bounded implication, personification, contrast, refrain, or canonical echo.",
                )
            )
        if not record["warrant_ids"] and not record["source_refs"]:
            findings.append(
                PoeticTransformationFinding(
                    "PT04",
                    f"{prefix}.warrant_ids",
                    "A poetic transformation must cite grounding evidence ids or canonical source references.",
                )
            )
        unknown = sorted(set(record["warrant_ids"]) - known_ids)
        if unknown:
            findings.append(
                PoeticTransformationFinding(
                    "PT05",
                    f"{prefix}.warrant_ids",
                    f"Poetic transformation cites unknown evidence ids: {', '.join(unknown)}.",
                )
            )
        if record["operation"] == "canonical_echo" and not record["source_refs"]:
            findings.append(
                PoeticTransformationFinding(
                    "PT06",
                    f"{prefix}.source_refs",
                    "A canonical echo must identify its canonical source reference.",
                )
            )

    return strategy, transformations, findings


def build_poetic_contract(
    strategy: Mapping[str, str],
    transformations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "governing_rule": "Scripture supplies the world; poetry supplies the music.",
        "positive_standard": (
            "Transform warranted language through compression, implication, personification, "
            "contrast, refrain, meter, rhyme, and sound so the poem discovers rather than merely excerpts."
        ),
        "boundary": (
            "A bounded transformation may deepen what the passage entails, but it may not introduce "
            "a new scene, event, actor, historical claim, or doctrine."
        ),
        "strategy": dict(strategy),
        "transformations": deepcopy(transformations),
    }


def _append_instruction(existing: Any, addition: str) -> str:
    current = _text(existing)
    return f"{current} {addition}".strip()


class PoeticTransformationAdapter:
    """Add a positive, warranted poetry contract to the integrated route.

    The adapter leaves deterministic mock payloads unchanged. Real production
    adapters receive a planner contract, a composer craft brief, and a reviewer
    dimension that distinguishes faithful poetic development from foreign
    world-building and from merely lineated quotation.
    """

    def __init__(self, delegate: Any, ctx: Any, config: Any):
        self.delegate = delegate
        self.ctx = ctx
        self.config = config
        self.is_mock = _is_mock(delegate)
        self.grounding: dict[str, Any] = {}
        self.contract: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        return getattr(self.delegate, name)

    def _planner_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        addition = (
            "Poetic fidelity does not require exact reuse of every biblical noun. Scripture supplies "
            "the world; poetry supplies the music. Add poem_design.poetic_strategy with genre_force, "
            "emotional_tone, formal_strategy, and discovery. Record every nonliteral development in "
            "poem_design.poetic_transformations with phrase, operation, textual_anchor, warrant_ids or "
            "canonical source_refs, and rationale. Bounded implication, compression, personification, "
            "contrast, refrain, meter, and rhyme are welcome when they deepen a warranted action or image. "
            "Do not create a new scene, event, actor, historical claim, or doctrine. No minimum number of "
            "transformations is required."
        )
        enriched["planning_instruction"] = _append_instruction(
            enriched.get("planning_instruction"), addition
        )
        return enriched

    def _composer_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        packet = dict(enriched.get("composition_packet", {}))
        packet["poetic_transformation_contract"] = deepcopy(self.contract)
        economy = dict(packet.get("economy", {}))
        principles = list(_list(economy.get("principles")))
        for principle in (
            "Scripture supplies the world; poetry supplies the music",
            "poetic faithfulness permits bounded implication and formal transformation",
            "do more than excerpt or lineate the passage",
            "preserve the passage's genre force and emotional temperature",
            "do not introduce a new scene, event, actor, historical claim, or doctrine",
        ):
            if principle not in principles:
                principles.append(principle)
        economy["principles"] = principles
        packet["economy"] = economy
        enriched["composition_packet"] = packet
        return enriched

    def _reviewer_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        enriched = deepcopy(dict(payload))
        enriched["poetic_transformation_contract"] = deepcopy(self.contract)
        addition = (
            "Score dimensions.poetic_transformation from 0 to 10. A strong poem must transform rather "
            "than merely excerpt or lineate the passage, preserve the passage's genre force and emotional "
            "temperature, and keep every nonliteral development within the supplied warrant. Do not reject "
            "a phrase merely because it is not an exact biblical noun; reject it when it creates a foreign "
            "world, event, actor, claim, or doctrine."
        )
        enriched["review_instruction"] = _append_instruction(
            enriched.get("review_instruction"), addition
        )
        return enriched

    def _enforce_review_dimension(self, review: Mapping[str, Any]) -> dict[str, Any]:
        normalized = deepcopy(dict(review))
        dimensions_value = normalized.get("dimensions")
        dimensions = (
            dict(dimensions_value) if isinstance(dimensions_value, Mapping) else {}
        )
        hard = [
            dict(item) if isinstance(item, Mapping) else {"message": _text(item)}
            for item in _list(normalized.get("hard_findings"))
        ]
        verdict = _text(normalized.get("verdict")).lower()
        minimum = float(getattr(self.config, "integrated_review_min_score", 8.0))
        score_value = dimensions.get("poetic_transformation")
        score: float | None
        try:
            score = float(score_value)
        except (TypeError, ValueError):
            score = None

        if score is None:
            hard.append(
                {
                    "code": "PT_R01",
                    "field": "dimensions.poetic_transformation",
                    "message": "Reviewer must score warranted poetic transformation.",
                    "repair_target": "poem",
                }
            )
        elif verdict == "pass" and score < minimum:
            hard.append(
                {
                    "code": "PT_R02",
                    "field": "dimensions.poetic_transformation",
                    "message": (
                        f"Poetic transformation score {score:g} is below the configured minimum {minimum:g}; "
                        "revise the poem without changing its textual world."
                    ),
                    "repair_target": "poem",
                }
            )

        if hard and verdict == "pass":
            normalized["verdict"] = "Revise"
        normalized["hard_findings"] = hard
        if self.ctx is not None:
            scores = getattr(self.ctx, "scores", None)
            if isinstance(scores, dict):
                scores["poetic_transformation"] = score
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
            enriched = self._planner_payload(payload)
            output = self.delegate.call(role, enriched)
            if not isinstance(output, Mapping):
                return output
            grounding = payload.get("grounding")
            grounding = dict(grounding) if isinstance(grounding, Mapping) else self.grounding
            strategy, transformations, findings = validate_poetic_contract(
                output,
                grounding,
                required=True,
            )
            if findings:
                raise PoeticTransformationError(
                    "; ".join(f"{item.field}: {item.message}" for item in findings)
                )
            normalized = deepcopy(dict(output))
            self.contract = build_poetic_contract(strategy, transformations)
            art_value = normalized.get("art_direction")
            art = dict(art_value) if isinstance(art_value, Mapping) else {}
            art["poetic_transformation_contract"] = deepcopy(self.contract)
            normalized["art_direction"] = art
            if self.ctx is not None:
                setattr(
                    self.ctx,
                    "poetic_transformation_contract",
                    deepcopy(self.contract),
                )
            return normalized

        if role == "devotional_composer":
            return self.delegate.call(role, self._composer_payload(payload))

        if role == "devotional_reviewer":
            output = self.delegate.call(role, self._reviewer_payload(payload))
            if isinstance(output, Mapping):
                return self._enforce_review_dimension(output)
            return output

        return self.delegate.call(role, payload)
