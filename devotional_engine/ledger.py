from .text_utils import first_words, last_nonempty_line, split_stanzas


def update_ledger(ctx) -> dict:
    entry = {
        "chapter": ctx.chapter_ref, "title": ctx.prose.get("title", ""),
        "epigraph_pattern": "", "selected_threshold_phrase": ctx.brief.get("selected_threshold_phrase", ""),
        "threshold_phrase_type": "", "first_sentence_pattern": "",
        "governing_image": ctx.brief.get("governing_image", ""),
        "image_lexicon": ctx.brief.get("image_lexicon", []),
        "christology_pathway": ctx.brief.get("christology_pathway", ""),
        "poem_stanza_count": len(split_stanzas(ctx.poem)),
        "poem_final_line": last_nonempty_line(ctx.poem),
        "theological_terminus": ctx.brief.get("theological_terminus", ""),
        "prayer_opener": first_words(ctx.prose.get("prayer", ""), 2),
        "beauty_score": ctx.scores.get("beauty_score", 0), "lingering_line": "",
        "editorial_smoothing_applied": ctx.scores.get("editorial_smoothing_applied", False),
    }
    ctx.ledger.setdefault("entries", []).append(entry)
    return entry
