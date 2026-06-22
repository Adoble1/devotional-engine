import re
from .american_literature import validate_style_brief
from .config import EngineConfig
from .renderer import render_artifact, validate_artifact_structure
from .text_utils import breath_overruns, count_syllables, split_stanzas, tongue_trip_spans
from .poetic_music import analyze_euphony, has_midline_caesura

PROSE_FIELDS = {"title", "epigraph", "focus_bible_verses", "introduction", "reflection", "christ_fulfillment", "application", "prayer", "next_in_sequence"}
BANNED_OPENING_PATTERNS = ["there is a kind", "there is a type", "there are moments", "sometimes", "the heart grows", "life feels", "god is always", "faith wins", "hope rises"]
KNOWN_RHYMES = {frozenset(x) for x in [("sea", "me"), ("night", "light"), ("word", "heard"), ("grace", "place"), ("fire", "desire"), ("way", "day"), ("song", "strong"), ("down", "crown"), ("stone", "known"), ("name", "flame")]}
FORBIDDEN_LABELS = [
    "threshold phrase", "chapter arc", "semantic proof chain", "christology pathway",
    "application target", "beauty pass", "deterministic harness", "theological risk register",
]
MECHANICAL_IMAGE_LABELS = ["governing image", "image head term", "image lexicon"]
METAPHOR_COLLISION_PATTERNS = [
    r"\b(bulls?|dogs?|lions?)\b.{0,60}\b(gored|tore|pierced|nailed|crucified)\b.{0,60}\b(christ|jesus)\b",
    r"\b(christ|jesus)\b.{0,60}\b(was|is|being)\b.{0,30}\b(gored|torn|pierced)\b.{0,60}\b(bulls?|dogs?|lions?)\b",
    r"\b(literal|physical)\b.{0,30}\b(bulls?|dogs?|lions?)\b.{0,60}\b(cross|crucifixion|calvary|roman wood)\b",
]
KJV_ARCHAISMS = [
    "thou", "thee", "thy", "thine", "ye", "hath", "doth", "art", "wilt",
    "shalt", "unto", "wherefore",
]
UNNECESSARY_ADVERBS = ["literally", "actually", "simply", "really", "very"]
SENSORY_QUALIA_TERMS = {
    "air", "ash", "blood", "bone", "bread", "breath", "brim", "cup", "dark",
    "door", "dust", "field", "fire", "flame", "flesh", "foot", "footfalls",
    "grass", "green", "hand", "head", "hill", "house", "lamp", "light",
    "mouth", "oil", "path", "road", "rock", "shadow", "sky", "sound",
    "stone", "table", "thirst", "thorn", "voice", "water", "wind",
}
EMOTION_ONLY_TERMS = {
    "abandoned", "ache", "aching", "anguish", "anxious", "beautiful",
    "comforting", "dread", "emotional", "fearful", "frightened", "grief",
    "heartbroken", "joyful", "lonely", "longing", "peaceful", "sad",
    "sorrow", "terrified", "tender", "wonderful",
}
EXPLANATORY_POEM_PATTERNS = [
    r"\bnot\s+because\b",
    r"\bbut\s+because\b",
    r"\bthis\s+means\b",
    r"\bthat\s+is\s+why\b",
    r"\bwe\s+learn\b",
    r"\bthe\s+psalm\s+(teaches|shows|means)\b",
]
IMAGE_PHYSICS_MISMATCHES = [
    (r"\bgrass\s+bends\s+under\s+the\s+shepherd'?s\s+hand\b", "grass bends under foot, wind, or grazing, not a shepherd's hand"),
    (r"\bwater\s+quiets\s+its\s+silver\s+tongue\b", "water does not quiet itself; prefer still water or the Shepherd's leading"),
    (r"\bnearer\s+than\s+grammar\b", "abstract cleverness displaces concrete poetic image"),
]


def _structured_text(ctx):
    return "\n".join(str(ctx.prose.get(key, "")) for key in sorted(PROSE_FIELDS)) + "\n" + ctx.poem


def _devotional_body_text(ctx):
    keys = ["introduction", "reflection", "christ_fulfillment", "application", "prayer"]
    return "\n".join(str(ctx.prose.get(key, "")) for key in keys) + "\n" + ctx.poem


def _normalize_words(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _word_tokens(text):
    return re.findall(r"[a-z]+", str(text).lower())


def _chapter_grounding_terms(ctx):
    sources = [
        ctx.source_text,
        ctx.working_rendering,
        " ".join(str(item) for item in ctx.chapter_design_map.get("physical_vocabulary", [])),
        " ".join(str(item) for item in ctx.brief.get("image_lexicon", [])),
        " ".join(str(item) for item in ctx.brief.get("chapter_specific_terms", [])),
    ]
    source_words = set(_word_tokens(" ".join(sources)))
    explicit_image_words = set(_word_tokens(" ".join(str(item) for item in ctx.chapter_design_map.get("physical_vocabulary", []))))
    explicit_image_words.update(_word_tokens(" ".join(str(item) for item in ctx.brief.get("image_lexicon", []))))
    explicit_image_words.update(_word_tokens(" ".join(str(item) for item in ctx.brief.get("chapter_specific_terms", []))))
    return explicit_image_words | (source_words & SENSORY_QUALIA_TERMS)


def _selected_reference_verses(focus: str, chapter_ref: str) -> set[int]:
    match = re.search(rf"\b{re.escape(chapter_ref)}:(?P<spec>[0-9,\-\s]+)", focus, re.I)
    if not match:
        return set()
    selected = set()
    for part in match.group("spec").split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            if not start_text.strip().isdigit() or not end_text.strip().isdigit():
                return set()
            start, end = int(start_text), int(end_text)
            if start > end:
                return set()
            selected.update(range(start, end + 1))
        elif part.isdigit():
            selected.add(int(part))
        else:
            return set()
    return selected


def validate_threshold_phrase(phrase: str, config=None) -> bool:
    config = config or EngineConfig()
    words = re.findall(r"[A-Za-z’'-]+", phrase)
    low = phrase.strip().lower()
    return config.threshold_min_words <= len(words) <= config.threshold_max_words and not any(low.startswith(p) for p in BANNED_OPENING_PATTERNS)


def chapter_arc_gate(ctx, config=None) -> list[str]:
    b = ctx.brief
    failures = [f"[ARC] missing {k}" for k in ("opening_movement", "closing_movement", "central_thought", "emotional_charge", "selected_threshold_phrase", "threshold_phrase_rationale") if not b.get(k)]
    if b.get("selected_threshold_phrase") and not validate_threshold_phrase(b["selected_threshold_phrase"], config): failures.append("V4 [ARC] invalid threshold phrase")
    central = str(b.get("central_thought", "")).lower()
    opening = set(re.findall(r"[a-z]+", str(b.get("opening_movement", "")).lower())) - {"the", "and", "to", "of", "a"}
    closing = set(re.findall(r"[a-z]+", str(b.get("closing_movement", "")).lower())) - {"the", "and", "to", "of", "a"}
    if central and opening and closing and (not opening.intersection(central.split()) or not closing.intersection(central.split())):
        failures.append("[ARC] central thought does not connect opening and closing movement")
    return failures


def _last_word(line):
    words = re.findall(r"[a-z]+", line.lower()); return words[-1] if words else ""


def _rhyme_kind(a, b):
    if not a or not b: return "fail"
    if a == b or frozenset((a, b)) in KNOWN_RHYMES: return "pass"
    if len(a) >= 3 and len(b) >= 3 and a[-3:] == b[-3:]: return "pass"
    if len(a) >= 2 and len(b) >= 2 and a[-2:] == b[-2:]: return "slant"
    return "fail"


def check_required_fields(ctx, config):
    missing = [k for k in PROSE_FIELDS if not str(ctx.prose.get(k, "")).strip()]
    return ([f"D0 [PROSE] missing fields: {', '.join(sorted(missing))}"] if missing else [], [])


def check_syllable_pattern(ctx, config):
    if config.poem_form != "common_meter":
        return [], []
    bad = []
    for si, stanza in enumerate(split_stanzas(ctx.poem), 1):
        if len(stanza) == 4:
            actual = [count_syllables(x) for x in stanza]
            if actual != [8, 6, 8, 6]: bad.append(f"stanza {si}: {actual}")
    return (["D1 [POEM] meter mismatch: " + "; ".join(bad)] if bad else [], [])


def check_rhyme(ctx, config):
    if config.poem_form != "common_meter":
        return [], []
    failures, warnings = [], []
    for i, stanza in enumerate(split_stanzas(ctx.poem), 1):
        if len(stanza) == 4:
            kind = _rhyme_kind(_last_word(stanza[1]), _last_word(stanza[3]))
            if kind == "fail": failures.append(f"D2 [POEM] stanza {i} B-lines do not rhyme")
            elif kind == "slant": warnings.append(f"D2w stanza {i} uses slant rhyme")
    return failures, warnings


def check_stanza_count(ctx, config):
    stanzas = split_stanzas(ctx.poem); n = len(stanzas)
    failures = []
    if config.poem_form == "common_meter":
        if n not in config.poem_stanza_counts: failures.append(f"D3 [POEM] stanza count {n} not allowed")
        if any(len(s) != 4 for s in stanzas): failures.append("D3 [POEM] every stanza must have four lines")
    else:
        line_count = sum(len(stanza) for stanza in stanzas)
        if not config.open_poem_min_lines <= line_count <= config.open_poem_max_lines:
            failures.append(f"D3 [POEM] open poem line count {line_count} not allowed")
    return failures, []


def check_repeated_stanzas(ctx, config):
    stanzas = ["\n".join(stanza).strip().lower() for stanza in split_stanzas(ctx.poem)]
    if len(stanzas) > 1 and len(set(stanzas)) < len(stanzas):
        return ["D11 [POEM] repeated stanza construction"], []
    return [], []


def check_image_head_term_exposure(ctx, config):
    text = _structured_text(ctx).lower()
    failures = [label for label in MECHANICAL_IMAGE_LABELS if label in text]
    return ([f"D5 [PROSE] mechanical image label exposed: {', '.join(failures)}"] if failures else [], [])


def check_forbidden_labels(ctx, config):
    text = _structured_text(ctx).lower()
    failures = [label for label in FORBIDDEN_LABELS if label in text]
    return ([f"D6 [PROSE] forbidden engine label exposed: {', '.join(failures)}"] if failures else [], [])


def check_historical_metaphor_collision(ctx, config):
    text = _structured_text(ctx).lower()
    for pattern in METAPHOR_COLLISION_PATTERNS:
        if re.search(pattern, text, re.S):
            return ["D20 [CHRISTOLOGY] historical metaphor collision detected"], []
    return [], []


def check_prayer_address_and_close(ctx, config):
    prayer = ctx.prose.get("prayer", "").strip()
    begins = re.match(r"^(Father|Our Father|Abba Father)\b", prayer, re.I)
    closes = re.search(r"\b(through Jesus Christ(?: our Lord)?|through Christ(?: our Lord)?|in Jesus Christ)\b", prayer, re.I)
    fails = [] if begins and closes else ["D8 [PROSE] prayer address or Christ-mediated close invalid"]
    sentences = len(re.findall(r"[.!?](?:\s|$)", prayer))
    return fails, ([] if 5 <= sentences <= 8 else [f"D7 prayer sentence count is {sentences}; prefer 5-8"])


def check_tongue_trips(ctx, config):
    trips = tongue_trip_spans(" ".join(str(v) for v in ctx.prose.values()))
    return [], (["D13 tongue-trip spans: " + ", ".join(trips)] if trips else [])


def check_breath_overruns(ctx, config):
    overruns = breath_overruns(" ".join(str(v) for v in ctx.prose.values()), config.breath_word_limit)
    return [], ([f"D14 breath overruns in {len(overruns)} sentence(s)"] if overruns else [])


def check_artifact_heading_order(ctx, config):
    try: artifact = render_artifact(ctx)
    except (KeyError, TypeError): return ["D17 [PROSE] artifact cannot be rendered"], []
    return ([] if validate_artifact_structure(artifact) else ["D17 [PROSE] artifact heading order invalid"], [])


def check_next_sequence(ctx, config):
    return ([] if str(ctx.prose.get("next_in_sequence", "")).strip() else ["D18 [PROSE] next in sequence missing"], [])


def check_threshold_phrase(ctx, config):
    return ([] if validate_threshold_phrase(ctx.brief.get("selected_threshold_phrase", ""), config) else ["V4 [ARC] threshold phrase invalid"], [])


def check_long_quotations(ctx, config):
    text = _structured_text(ctx)
    quotes = re.findall(r"[\"“](.*?)[\"”]", text)
    if not any(len(_normalize_words(quote).split()) >= 4 for quote in quotes):
        return [], []
    source = _normalize_words(ctx.source_text + " " + ctx.working_rendering)
    if not source:
        return ["D9 [SOURCE] source/rendering unavailable for quotation verification"], []
    failures = []
    for quote in quotes:
        quote_words = _normalize_words(quote)
        if len(quote_words.split()) >= 4 and quote_words not in source:
            failures.append(quote.strip())
    return ([f"D9 [SOURCE] long quotation not verified: {failures[0]}"] if failures else [], [])


def check_christology_anchor_terms(ctx, config):
    required = [str(term).lower() for term in ctx.brief.get("christology_required_echoes", []) if str(term).strip()]
    christology = str(ctx.prose.get("christ_fulfillment", "")).lower()
    missing = [term for term in required if term not in christology]
    return ([f"D12a [CHRISTOLOGY] missing anchor terms: {', '.join(missing)}"] if missing else [], [])


def check_theological_risk_register(ctx, config):
    return ([] if ctx.theological_risk_register else ["T1 [CHRISTOLOGY] theological risk register missing"], [])


def check_semantic_proof_chain(ctx, config):
    return ([] if ctx.brief.get("semantic_proof_chain") else ["S1 [ARC] semantic proof chain missing"], [])


def check_literary_style_rights(ctx, config):
    failures = validate_style_brief(ctx.literary_style) if ctx.literary_style else []
    return ([f"D21 [STYLE] {failure}" for failure in failures], [])


def check_same_chapter_reference_style(ctx, config):
    if not config.enforce_same_chapter_reference_style:
        return [], []
    chapter_ref = str(ctx.chapter_ref).strip()
    if not chapter_ref:
        return [], []
    body = _devotional_body_text(ctx)
    if re.search(rf"\b{re.escape(chapter_ref)}\b", body, re.I):
        return [f"D22 [PROSE] use 'the psalm' for repeated references to {chapter_ref}"], []
    return [], []


def check_full_focus_verses_and_translation_style(ctx, config):
    if not config.require_full_focus_verses and not config.require_key_verse_selection:
        return [], []
    focus = str(ctx.prose.get("focus_bible_verses", "")).strip()
    failures = []
    if ctx.chapter_ref and not re.search(rf"\b{re.escape(ctx.chapter_ref)}\b", focus, re.I):
        failures.append(f"missing reference label {ctx.chapter_ref}")
    word_count = len(re.findall(r"[A-Za-z’'-]+", focus))
    if word_count < config.focus_verses_min_words:
        failures.append(f"focus verses look like citation only ({word_count} words)")
    low = f" {focus.lower()} "
    archaic = [word for word in KJV_ARCHAISMS if re.search(rf"\b{re.escape(word)}\b", low)]
    if archaic:
        failures.append(f"KJV-style archaisms present: {', '.join(archaic)}")
    if config.require_key_verse_selection:
        total = ctx.source_layer.get("chapter_verse_count")
        selected = _selected_reference_verses(focus, ctx.chapter_ref)
        if not isinstance(total, int) or total < 1:
            failures.append("chapter verse count unavailable for key-verse validation")
        elif not selected:
            failures.append("focus reference does not identify selected key verses")
        elif min(selected) < 1 or max(selected) > total:
            failures.append("focus reference contains verse outside chapter range")
        elif selected == set(range(1, total + 1)):
            failures.append("focus verses select the whole chapter instead of key verses")
    return ([f"D23 [SOURCE] {'; '.join(failures)}"] if failures else [], [])


def check_unnecessary_adverbs(ctx, config):
    if not config.warn_unnecessary_adverbs:
        return [], []
    text = _devotional_body_text(ctx).lower()
    found = sorted({word for word in UNNECESSARY_ADVERBS if re.search(rf"\b{re.escape(word)}\b", text)})
    return [], ([f"D24 unnecessary adverbs: {', '.join(found)}"] if found else [])


def check_image_physics(ctx, config):
    if not config.warn_image_physics:
        return [], []
    text = _structured_text(ctx).lower()
    source_context = " ".join(
        [
            ctx.source_text,
            ctx.working_rendering,
            " ".join(str(item) for item in ctx.chapter_design_map.get("physical_vocabulary", [])),
            str(ctx.chapter_design_map.get("divine_action", "")),
        ]
    ).lower()
    miracle_terms = {"miracle", "sea", "waters split", "sun stood", "resurrection", "raised"}
    if any(term in source_context for term in miracle_terms):
        return [], []
    warnings = [message for pattern, message in IMAGE_PHYSICS_MISMATCHES if re.search(pattern, text)]
    return [], ([f"D25 image physics issue: {warnings[0]}"] if warnings else [])


def check_explanatory_poem_language(ctx, config):
    if not config.warn_explanatory_poem:
        return [], []
    poem = ctx.poem.lower()
    found = [pattern for pattern in EXPLANATORY_POEM_PATTERNS if re.search(pattern, poem)]
    return [], (["D26 explanatory poem language detected"] if found else [])


def check_grounded_qualia(ctx, config):
    if not config.warn_grounded_qualia:
        return [], []
    words = _word_tokens(_devotional_body_text(ctx))
    grounding_terms = _chapter_grounding_terms(ctx)
    grounded = sorted({word for word in words if word in grounding_terms})
    emotional = [word for word in words if word in EMOTION_ONLY_TERMS]
    warnings = []
    if len(grounded) < config.qualia_min_grounded_terms:
        warnings.append("D27 grounded qualia weak: use embodied, chapter-born detail rather than abstract feeling")
    if emotional and len(emotional) > max(config.qualia_max_emotion_to_grounded_ratio * max(len(grounded), 1), config.qualia_max_emotion_to_grounded_ratio):
        warnings.append("D27 grounded qualia weak: emotional language is not sufficiently carried by concrete chapter imagery")
    return [], warnings[:1]


def check_poem_music(ctx, config):
    if not config.warn_poem_music:
        return [], []
    analysis = analyze_euphony(ctx.poem)
    warnings = []
    if analysis["harsh_clusters_per_100_words"] > 18 and analysis["soft_consonant_ratio"] < 0.45:
        warnings.append("D28 poem music is densely clustered; review consonant flow against chapter tone")
    if config.poem_form == "common_meter":
        long_lines = [line for stanza in split_stanzas(ctx.poem) for line in stanza if count_syllables(line) == 8]
        caesura_lines = [line for line in long_lines if has_midline_caesura(line)]
        if len(long_lines) >= 4 and len(caesura_lines) / len(long_lines) < 0.25:
            warnings.append("D28 common-meter long lines lack varied mid-line breath")
    return [], warnings


CHECK_REGISTRY = {"D0": check_required_fields, "D1": check_syllable_pattern, "D2": check_rhyme, "D3": check_stanza_count, "D5": check_image_head_term_exposure, "D6": check_forbidden_labels, "D8": check_prayer_address_and_close, "D9": check_long_quotations, "D11": check_repeated_stanzas, "D12a": check_christology_anchor_terms, "D13": check_tongue_trips, "D14": check_breath_overruns, "D17": check_artifact_heading_order, "D18": check_next_sequence, "D20": check_historical_metaphor_collision, "D21": check_literary_style_rights, "D22": check_same_chapter_reference_style, "D23": check_full_focus_verses_and_translation_style, "D24": check_unnecessary_adverbs, "D25": check_image_physics, "D26": check_explanatory_poem_language, "D27": check_grounded_qualia, "D28": check_poem_music, "V4": check_threshold_phrase, "T1": check_theological_risk_register, "S1": check_semantic_proof_chain}


def run_deterministic_harness(ctx, config=None):
    config = config or EngineConfig(); failures, warnings = [], []
    for check in CHECK_REGISTRY.values():
        f, w = check(ctx, config); failures.extend(f); warnings.extend(w)
    return failures, warnings
