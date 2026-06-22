import math
from .config import EngineConfig

MECHANICAL_PATTERNS = [
    "This Psalm speaks to", "The Psalm reminds us", "The heart grows",
    "There is a kind of", "There are moments when", "Sometimes",
    "In our lives today", "We are called to", "This does not mean",
]
EVALUATOR_SCORE_FIELDS = {
    "textual_fidelity", "theological_accuracy", "christology_from_chapter_logic",
    "chapter_design_fidelity", "emotional_charged_phrase", "introduction_strength",
    "ancient_image_discipline", "register", "read_aloud_quality",
    "application_concreteness", "prayer", "poem_form", "poetic_vitality",
    "artful_design", "artifact_integrity",
}
EVALUATOR_FAULT_TARGETS = {"none", "prose", "poem", "both"}


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _warning_id(warning: str) -> str:
    return str(warning).split(" ", 1)[0]


def _beauty_fault_target(warnings: list[str]) -> str:
    ids = {_warning_id(warning) for warning in warnings}
    if ids and ids <= {"D26"}:
        return "poem"
    if ids and ids <= {"D24"}:
        return "prose"
    return "both"


def _promoted_beauty_warnings(warnings, config):
    if not config.strict_beauty_warnings:
        return []
    promoted_ids = set(config.beauty_warning_ids)
    return [warning for warning in _as_list(warnings) if _warning_id(warning) in promoted_ids]


def run_beauty_pass(ctx, output=None, warnings=None, config=None) -> dict:
    config = config or EngineConfig()
    text = "\n".join(str(v) for v in ctx.prose.values()) + "\n" + ctx.poem
    residue = [pattern for pattern in MECHANICAL_PATTERNS if pattern.lower() in text.lower()]
    promoted_warnings = _promoted_beauty_warnings(warnings, config)
    default = {
        "lingering_lines": [], "strongest_turn": "", "weakest_artistic_moment": "",
        "mechanical_residue": residue + promoted_warnings,
        "beauty_score": 8 if not residue and not promoted_warnings else 6,
        "required_beauty_revisions": residue + promoted_warnings,
    }
    if promoted_warnings:
        default["fault_target"] = _beauty_fault_target(promoted_warnings)
        default["weakest_artistic_moment"] = "Deterministic beauty warnings require revision."
    deterministic_score = default["beauty_score"]
    if output:
        score = output.get("beauty_score", default["beauty_score"])
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score):
            score = 0
        output_residue = _as_list(output.get("mechanical_residue"))
        output_revisions = _as_list(output.get("required_beauty_revisions"))
        default.update(output)
        combined_residue = list(dict.fromkeys(residue + output_residue))
        combined_residue = list(dict.fromkeys(combined_residue + promoted_warnings))
        combined_revisions = list(dict.fromkeys(residue + output_revisions + promoted_warnings))
        default["mechanical_residue"] = combined_residue
        default["required_beauty_revisions"] = combined_revisions
        default["beauty_score"] = min(max(score, 0), deterministic_score)
        if promoted_warnings:
            default["fault_target"] = _beauty_fault_target(promoted_warnings)
    return default


def validate_evaluation(result: dict) -> list[str]:
    if not isinstance(result, dict):
        return ["[BOTH] evaluator output must be a dictionary"]
    missing = EVALUATOR_SCORE_FIELDS - result.keys()
    if missing:
        return [f"[BOTH] evaluator missing: {', '.join(sorted(missing))}"]
    target = str(result.get("fault_target", "both")).lower()
    if target not in EVALUATOR_FAULT_TARGETS:
        return ["[BOTH] evaluator fault_target invalid"]
    for key in EVALUATOR_SCORE_FIELDS:
        score = result[key]
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score) or not 0 <= score <= 10:
            return [f"[BOTH] evaluator score invalid for {key}"]
        if score < 8:
            routed_target = "both" if target == "none" else target
            return [f"[{routed_target.upper()}] evaluator score below 8"]
    return []
