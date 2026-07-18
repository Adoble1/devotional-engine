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
REDUNDANT_INTENSIFIERS = (
    "literally",
    "actually",
    "truly",
    "really",
    "very",
    "deeply",
)
REVERSAL_PATTERNS = (
    r"\bnot\s+[^.!?]{1,100}\.\s+(?:it|this|that)\s+is\b",
    r"\bnot\s+because\b[^.!?]{1,140}\bbut\s+because\b",
    r"\bnot\s+[^,.;:]{1,100},\s+but\b",
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


def _image_candidates(plan: Mapping[str, Any]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for item in _list(plan.get("governing_image_candidates")):
        if isinstance(item, Mapping):
            record = {
                "image": _text(item.get("image")),
                "warrant": _text(item.get("warrant")),
                "sensory_grain": _text(item.get("sensory_grain")),
                "transformation": _text(item.get("transformation")),
                "ledger_novelty": _text(item.get("ledger_novelty")),
            }
        else:
            record = {
                "image": _text(item),
                "warrant": "",
                "sensory_grain": "",
                "transformation": "",
                "ledger_novelty": "",
            }
        if record["image"]:
            candidates.append(record)
    return candidates


def build_narrative_design(
    plan: Mapping[str, Any],
    grounding: Mapping[str, Any],
) -> dict[str, Any]:
    supplied = plan.get("narrative_design")
    supplied = dict(supplied) if isinstance(supplied, Mapping) else {}
    level = supplied.get("level", 1)
    try:
        level = int(level)
    except (TypeError, ValueError):
        level = 0
    return {
        "level": level,
        "warrant": _text(
            supplied.get("warrant")
            or grounding.get("literary_mode")
            or grounding.get("historical_meaning")
        ),
        "scope": _text(
            supplied.get("scope")
            or "Dramatize only the speaker and situation established by the text."
        ),
        "source_basis": _text(
            supplied.get("source_basis")
            or grounding.get("historical_meaning")
        ),
        "bounded_scene": _text(supplied.get("bounded_scene")),
    }


def build_poem_design(plan: Mapping[str, Any], grounding: Mapping[str, Any]) -> dict[str, Any]:
    supplied = plan.get("poem_design")
    supplied = dict(supplied) if isinstance(supplied, Mapping) else {}
    art = plan.get("art_direction")
    art = dict(art) if isinstance(art, Mapping) else {}
    transform = plan.get("reader_transformation")
    transform = dict(transform) if isinstance(transform, Mapping) else {}

    candidates = _image_candidates(plan)
    selected = _text(
        plan.get("selected_governing_image")
        or supplied.get("selected_governing_image")
        or (candidates[0]["image"] if candidates else "")
        or plan.get("governing_image")
    )

    image_field = dedupe_boundaries(_list(supplied.get("image_field")))
    if not image_field:
        image_field = dedupe_boundaries(
            [selected, plan.get("governing_image"), *_list(plan.get("poem_arc"))]
        )
    elif selected:
        image_field = dedupe_boundaries([selected, *image_field])

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
        "form": _text(supplied.get("form")),
        "meter": _text(supplied.get("meter")),
        "rhyme_scheme": _text(supplied.get("rhyme_scheme")),
        "selected_governing_image": selected,
        "governing_image_candidates": candidates,
        "selection_rationale": _text(
            plan.get("image_selection_rationale")
            or supplied.get("selection_rationale")
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
    lexical = grounding.get("lexical_insight")
    lexical = dict(lexical) if isinstance(lexical, Mapping) else {}
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
            "lexical_insight": lexical,
        },
        "canonical": {
            "classification": _text(canonical.get("classification")),
            "description": _text(canonical.get("description")),
            "fulfillment": blueprint.canonical_fulfillment,
        },
        "reader_transformation": dict(blueprint.reader_transformation),
        "prose_movements": dict(blueprint.section_burdens),
        "art_direction": dict(blueprint.art_direction),
        "narrative_design": dict(getattr(blueprint, "narrative_design", {})),
        "poem_design": dict(blueprint.poem_design),
        "series_continuity": {
            "selected_image": blueprint.governing_image,
            "selection_rationale": _text(
                blueprint.poem_design.get("selection_rationale")
            ),
            "candidate_count": len(
                _list(blueprint.poem_design.get("governing_image_candidates"))
            ),
        },
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
                "use the lexical insight only where it advances the argument",
                "make the epigraph's implied mechanism true to the passage",
                "after a strong image, allow a plain sentence to carry weight",
                "reserve balanced reversal for the strongest turn",
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
                "reader response", "narrative warrant",
            ],
        },
    }


def _cadence_findings(prose: Mapping[str, Any], poem: str) -> list[LiteraryFinding]:
    findings: list[LiteraryFinding] = []
    prose_text = "\n".join(_text(prose.get(section, "")) for section in CORE_PROSE_SECTIONS)
    full_text = f"{prose_text}\n{poem}"

    if "—" in full_text or "–" in full_text:
        findings.append(
            LiteraryFinding(
                "LE09",
                "draft",
                "Dash punctuation is carrying sentence structure; prefer commas, colons, or separate sentences when the ear improves.",
                repair_target="draft",
            )
        )

    found = sorted(
        term
        for term in REDUNDANT_INTENSIFIERS
        if re.search(rf"\b{re.escape(term)}\b", prose_text.lower())
    )
    if found:
        findings.append(
            LiteraryFinding(
                "LE10",
                "prose",
                f"Redundant intensifier language appears: {', '.join(found)}.",
                repair_target="prose",
            )
        )

    reversals = sum(
        len(re.findall(pattern, prose_text.lower(), re.S))
        for pattern in REVERSAL_PATTERNS
    )
    if reversals > 1:
        findings.append(
            LiteraryFinding(
                "LE11",
                "prose",
                f"Balanced reversal appears {reversals} times; reserve it for one decisive turn.",
                repair_target="prose",
            )
        )

    for section in CORE_PROSE_SECTIONS:
        text = _text(prose.get(section, ""))
        sentences = [
            item.strip()
            for item in re.split(r"(?<=[.!?])\s+", text)
            if item.strip()
        ]
        lengths = [len(_words(item)) for item in sentences]
        if len(lengths) >= 4 and max(lengths) - min(lengths) < 8:
            findings.append(
                LiteraryFinding(
                    "LE12",
                    section,
                    "Sentence lengths are unusually even; vary breath and pressure within the section.",
                    repair_target=section,
                )
            )

        paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
        openings = [
            tuple(_normalize(item).split()[:2])
            for item in paragraphs
            if _normalize(item)
        ]
        if any(
            openings[index] == openings[index - 1]
            for index in range(1, len(openings))
            if len(openings[index]) == 2
        ):
            findings.append(
                LiteraryFinding(
                    "LE13",
                    section,
                    "Consecutive paragraphs open with the same syntactic footprint.",
                    repair_target=section,
                )
            )
    return findings


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

    findings.extend(_cadence_findings(prose, poem))
    return findings
