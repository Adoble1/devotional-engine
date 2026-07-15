from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class WritingMode(str, Enum):
    DEVOTIONAL = "devotional"
    FICTION = "fiction"
    NONFICTION = "nonfiction"


@dataclass(frozen=True)
class GoverningLaw:
    rule_id: str
    name: str
    purpose: str


@dataclass(frozen=True)
class WritingProfile:
    mode: WritingMode
    required_planning_maps: tuple[str, ...]
    required_output_fields: tuple[str, ...]
    profile_rule_ids: tuple[str, ...]
    evaluator_dimensions: tuple[str, ...]


CORE_LAWS: tuple[GoverningLaw, ...] = (
    GoverningLaw(
        "source_truth",
        "Source Truth",
        "Claims, scenes, and images may not outrun the governing source, evidence, or established story world.",
    ),
    GoverningLaw(
        "reality_and_genre",
        "Reality and Genre Fidelity",
        "Preserve ordinary causality, declared miracles or speculative premises, and the literary mode of the work.",
    ),
    GoverningLaw(
        "continuity",
        "Continuity",
        "Preserve theological, factual, character, world, and argument state across the work.",
    ),
    GoverningLaw(
        "revelatory_pacing",
        "Revelatory Pacing",
        "Let understanding arrive in the order warranted by the source, scene, or argument instead of explaining too early.",
    ),
    GoverningLaw(
        "human_truth",
        "Human Truth",
        "Earn emotion and judgment through perception, action, consequence, memory, and desire rather than labels alone.",
    ),
    GoverningLaw(
        "aesthetic_freedom",
        "Protected Aesthetic Freedom",
        "Permit formal and stylistic variation inside truth, continuity, rights, and safety boundaries.",
    ),
)

CORE_LAW_IDS: tuple[str, ...] = tuple(law.rule_id for law in CORE_LAWS)

_SHARED_MAPS = (
    "truth_map",
    "revelation_map",
    "reader_transformation_map",
    "art_direction",
)

PROFILE_REGISTRY: dict[WritingMode, WritingProfile] = {
    WritingMode.DEVOTIONAL: WritingProfile(
        mode=WritingMode.DEVOTIONAL,
        required_planning_maps=_SHARED_MAPS + ("canonical_map", "theological_risk_map"),
        required_output_fields=("title", "body", "scripture_references"),
        profile_rule_ids=(
            "text_sovereignty",
            "ordinary_physics_unless_revelation",
            "literary_mode_preservation",
            "apostolic_priority",
            "israel_church_continuity",
            "christological_fulfillment_without_replacement",
        ),
        evaluator_dimensions=(
            "textual_fidelity",
            "theological_accuracy",
            "canonical_warrant",
            "earned_emotion",
            "literary_quality",
        ),
    ),
    WritingMode.FICTION: WritingProfile(
        mode=WritingMode.FICTION,
        required_planning_maps=_SHARED_MAPS
        + ("world_state", "character_state", "causal_scene_map", "continuity_ledger"),
        required_output_fields=("title", "body", "continuity_updates"),
        profile_rule_ids=(
            "declared_world_physics",
            "character_desire_and_causality",
            "point_of_view_consistency",
            "scene_turn_and_consequence",
            "earned_emotion",
            "no_unearned_fact",
        ),
        evaluator_dimensions=(
            "world_coherence",
            "character_coherence",
            "causal_coherence",
            "narrative_tension",
            "prose_quality",
        ),
    ),
    WritingMode.NONFICTION: WritingProfile(
        mode=WritingMode.NONFICTION,
        required_planning_maps=_SHARED_MAPS
        + ("claim_evidence_map", "argument_map", "uncertainty_ledger", "source_ledger"),
        required_output_fields=("title", "body", "sources"),
        profile_rule_ids=(
            "claim_evidence_traceability",
            "source_attribution",
            "fact_inference_opinion_separation",
            "uncertainty_disclosure",
            "argument_coherence",
            "no_fabricated_sources",
        ),
        evaluator_dimensions=(
            "factual_accuracy",
            "evidence_quality",
            "argument_coherence",
            "uncertainty_calibration",
            "clarity",
        ),
    ),
}

# Compatibility aliases translate older local rules into the smaller law set.
# They are accepted as inputs but are not re-emitted as independent governing laws.
LEGACY_RULE_ALIASES: dict[str, str] = {
    "emotion_earned_by_physical_fact": "human_truth",
    "no_unwarranted_deprivation": "source_truth",
    "global_canonical_view": "continuity",
    "apostolic_priority": "continuity",
    "mystery_to_revelation": "revelatory_pacing",
    "discovery_before_explanation": "revelatory_pacing",
    "originality_check": "aesthetic_freedom",
    "physics_consistency": "reality_and_genre",
    "genre_preservation": "reality_and_genre",
    "immediate_immersion": "revelatory_pacing",
}


def normalize_mode(mode: WritingMode | str | None) -> WritingMode:
    if isinstance(mode, WritingMode):
        return mode
    value = str(mode or WritingMode.DEVOTIONAL.value).strip().lower().replace("-", "_")
    aliases = {
        "devotion": WritingMode.DEVOTIONAL,
        "devotional": WritingMode.DEVOTIONAL,
        "fiction": WritingMode.FICTION,
        "non_fiction": WritingMode.NONFICTION,
        "nonfiction": WritingMode.NONFICTION,
    }
    try:
        return aliases[value]
    except KeyError as exc:
        allowed = ", ".join(item.value for item in WritingMode)
        raise ValueError(f"Unknown writing mode {mode!r}; expected one of: {allowed}") from exc


def get_profile(mode: WritingMode | str | None) -> WritingProfile:
    return PROFILE_REGISTRY[normalize_mode(mode)]


def compile_rule_ids(
    mode: WritingMode | str | None,
    candidate_rules: Iterable[str] = (),
) -> tuple[str, ...]:
    """Compile a minimal, deterministic rule set for one writing mode.

    Candidate and legacy rules are deduplicated. Legacy aliases collapse into the
    six governing laws instead of creating additional global rules.
    """

    profile = get_profile(mode)
    compiled: list[str] = list(CORE_LAW_IDS) + list(profile.profile_rule_ids)
    allowed_profile_rules = set(profile.profile_rule_ids)
    allowed_core_rules = set(CORE_LAW_IDS)
    for raw_rule in candidate_rules:
        rule = str(raw_rule).strip()
        if not rule:
            continue
        normalized = LEGACY_RULE_ALIASES.get(rule, rule)
        if normalized not in allowed_profile_rules and normalized not in allowed_core_rules:
            # Passage- or project-specific constraints remain local notes. They do
            # not become global engine rules merely because one draft needed them.
            continue
        if normalized not in compiled:
            compiled.append(normalized)
    return tuple(compiled)
