from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


CORE_PROSE_SECTIONS = (
    "introduction",
    "reflection",
    "christ_fulfillment",
    "application",
    "prayer",
)
EXPOSITORY_POEM_PATTERNS = (
    r"\bthis (?:means|shows|teaches)\b",
    r"\bthe psalm (?:means|shows|teaches)\b",
    r"\bwe (?:learn|see|must understand)\b",
    r"\bnot because\b.{0,80}\bbut because\b",
    r"\btherefore\b",
    r"\bin conclusion\b",
)


@dataclass(frozen=True)
class LiteraryFinding:
    code: str
    field: str
    message: str
    severity: str = "warning"
    repair_target: str = "draft"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]


def _words(value: Any) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ’'-]+", _text(value))


def _normalize(value: Any) -> str:
    return " ".join(re.findall(r"[a-z0-9']+", _text(value).lower().replace("’", "'")))


def dedupe_boundaries(values: Iterable[Any]) -> list[str]:
    """Keep distinct non-empty terms or instructions in their original order."""

    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = _text(value)
        normalized = _normalize(text)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(text)
    return result


def prune_local_constraints(
    local_constraints: Iterable[Any],
    risks: Iterable[Any],
    unsupported_claims: Iterable[Any],
) -> list[str]:
    """Remove plan instructions already carried by grounding risk boundaries."""

    protected = [
        risk.get("avoidance_rule")
        for risk in risks
        if isinstance(risk, Mapping)
    ]
    protected.extend(unsupported_claims)
    protected_norm = {_normalize(item) for item in protected if _normalize(item)}
    return [
        item
        for item in dedupe_boundaries(local_constraints)
        if _normalize(item) not in protected_norm
    ]


def build_poem_design(plan: Mapping[str, Any], grounding: Mapping[str, Any]) -> dict[str, Any]:
    supplied = plan.get("poem_design")
    supplied = dict(supplied) if isinstance(supplied, Mapping) else {}
    art = plan.get("art_direction")
    art = dict(art) if isinstance(art, Mapping) else {}
    transform = plan.get("reader_transformation")
    transform = dict(transform) if isinstance(transform, Mapping) else {}

    image_field = dedupe_boundaries(_list(supplied.get("image_field")))
    if not image_field:
        image_field = dedupe_boundaries(
            [plan.get("governing_image"), *_list(plan.get("poem_arc"))]
        )

    sensory_palette = dedupe_boundaries(_list(supplied.get("sensory_palette")))
    if not sensory_palette:
        sensory_palette = dedupe_boundaries(
            _list(art.get("image_lexicon") or grounding.get("physical_vocabulary"))
        )

    poem_arc = _list(plan.get("poem_arc"))
    emotional_turn = _text(
        supplied.get("emotional_turn")
        or (poem_arc[-1] if poem_arc else "")
        or transform.get("new_perception")
        or transform.get("to")
    )
    return {
        "image_field": image_field,
        "sensory_palette": sensory_palette,
        "sonic_movement": _text(
            supplied.get("sonic_movement")
            or art.get("sentence_music")
            or art.get("pace")
        ),
        "emotional_turn": emotional_turn,
        "prohibited_exposition": dedupe_boundaries(
            [
                *_list(supplied.get("prohibited_exposition")),
                "do not summarize the reflection",
                "do not explain the theological argument",
                "do not turn prose sentences into line breaks",
            ]
        ),
    }


def composition_packet(ctx: Any, grounding: Mapping[str, Any], blueprint: Any, config: Any) -> dict[str, Any]:
    """Give the composer the load-bearing truth without the research machinery."""

    canonical = grounding.get("canonical_relationship")
    canonical = dict(canonical) if isinstance(canonical, Mapping) else {}
    risk_boundaries = [
        _text(risk.get("avoidance_rule"))
        for risk in _list(grounding.get("risks"))
        if isinstance(risk, Mapping) and _text(risk.get("avoidance_rule"))
    ]
    return {
        "chapter_ref": ctx.chapter_ref,
        "scripture": {
            "focus_text": _text(grounding.get("working_rendering")),
            "provenance": dict(grounding.get("rendering_provenance", {})),
        },
        "passage": {
            "question": blueprint.governing_question,
            "subject": blueprint.governing_subject,
            "human_predicament": blueprint.human_predicament,
            "textual_hinge": blueprint.textual_hinge,
            "divine_answer": blueprint.divine_answer,
        },
        "canonical": {
            "classification": _text(canonical.get("classification")),
            "description": _text(canonical.get("description")),
            "fulfillment": blueprint.canonical_fulfillment,
        },
        "reader_transformation": dict(blueprint.reader_transformation),
        "prose_movements": dict(blueprint.section_burdens),
        "art_direction": dict(blueprint.art_direction),
        "poem_design": dict(blueprint.poem_design),
        "boundaries": dedupe_boundaries(
            [
                *risk_boundaries,
                *_list(grounding.get("unsupported_claims")),
                *blueprint.local_constraints,
            ]
        ),
        "economy": {
            "prose_target_words": int(getattr(config, "integrated_prose_target_words", 850)),
            "poem_target_lines": int(getattr(config, "integrated_poem_target_lines", 16)),
            "principles": [
                "one movement per section",
                "state a necessary distinction once",
                "prefer image and implication to repeated explanation",
                "remove any sentence that only proves the engine was careful",
                "let every paragraph and every line earn its place",
            ],
        },
        "aesthetic_freedom": {
            "free": [
                "title", "opening", "paragraph shape", "imagery", "cadence",
                "silence", "transitions", "poem form",
            ],
            "fixed": [
                "Scripture provenance", "historical meaning", "governing subject",
                "textual hinge", "divine answer", "canonical classification",
                "reader response",
            ],
        },
    }


def audit_literary_economy(ctx: Any, blueprint: Any, config: Any) -> list[LiteraryFinding]:
    findings: list[LiteraryFinding] = []
    prose = getattr(ctx, "prose", {}) or {}
    body_counts = {
        section: len(_words(prose.get(section, "")))
        for section in CORE_PROSE_SECTIONS
    }
    total = sum(body_counts.values())
    target = max(1, int(getattr(config, "integrated_prose_target_words", 850)))
    if total > target:
        findings.append(LiteraryFinding(
            "LE01", "prose",
            f"Devotional body is {total} words against a {target}-word literary target; compress repeated explanation.",
            repair_target="prose",
        ))

    if total:
        section, count = max(body_counts.items(), key=lambda item: item[1])
        share_limit = float(getattr(config, "integrated_section_share_limit", 0.52))
        if count / total > share_limit:
            findings.append(LiteraryFinding(
                "LE02", section,
                "One section carries too much of the whole argument; cut or redistribute only what is necessary.",
                repair_target=section,
            ))

    poem = _text(getattr(ctx, "poem", ""))
    lines = [line.strip() for line in poem.splitlines() if line.strip()]
    line_target = max(1, int(getattr(config, "integrated_poem_target_lines", 16)))
    if len(lines) > line_target:
        findings.append(LiteraryFinding(
            "LE03", "poem",
            f"Poem has {len(lines)} lines against a {line_target}-line target; remove explanatory or duplicate lines.",
            repair_target="poem",
        ))

    average = 0.0
    if lines:
        average = sum(len(_words(line)) for line in lines) / len(lines)
        max_average = float(getattr(config, "integrated_poem_max_average_line_words", 7.5))
        if average > max_average:
            findings.append(LiteraryFinding(
                "LE04", "poem",
                f"Average line length is {average:.1f} words; the poem is carrying prose syntax instead of lyric pressure.",
                repair_target="poem",
            ))
        punctuated = sum(bool(re.search(r"[.!?;:]$", line)) for line in lines)
        if len(lines) >= 6 and punctuated / len(lines) >= 0.75 and average >= 6:
            findings.append(LiteraryFinding(
                "LE05", "poem",
                "Most lines close like complete prose sentences; vary syntax, breath, and enjambment.",
                repair_target="poem",
            ))

    if any(re.search(pattern, poem.lower(), re.S) for pattern in EXPOSITORY_POEM_PATTERNS):
        findings.append(LiteraryFinding(
            "LE06", "poem",
            "The poem explains or concludes; return to image, sound, pressure, and discovery.",
            repair_target="poem",
        ))

    prose_sentences = {
        _normalize(sentence)
        for section in CORE_PROSE_SECTIONS
        for sentence in re.split(r"(?<=[.!?])\s+", _text(prose.get(section, "")))
        if len(_normalize(sentence).split()) >= 7
    }
    poem_lines = {
        _normalize(line)
        for line in lines
        if len(_normalize(line).split()) >= 7
    }
    if prose_sentences.intersection(poem_lines):
        findings.append(LiteraryFinding(
            "LE07", "poem",
            "A poem line repeats a full prose sentence; the poem must transform rather than summarize.",
            repair_target="poem",
        ))

    palette = [
        _normalize(item)
        for item in _list(getattr(blueprint, "poem_design", {}).get("sensory_palette"))
        if _normalize(item)
    ]
    normalized_poem = _normalize(poem)
    present = {
        item for item in palette
        if re.search(rf"\b{re.escape(item)}\b", normalized_poem)
    }
    minimum = max(1, int(getattr(config, "integrated_poem_min_qualia", 2)))
    if palette and len(present) < min(minimum, len(palette)):
        findings.append(LiteraryFinding(
            "LE08", "poem",
            "The poem lacks enough passage-born sensory presence; embody the movement in concrete qualia.",
            repair_target="poem",
        ))
    return findings
