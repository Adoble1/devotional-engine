CLASSICAL_HYMNODY_PROFILE = {
    "source_scope": "public-domain metrical psalmody supplied by the project",
    "observed_strengths": [
        "Each stanza advances a distinct chapter movement instead of restating one idea.",
        "Rhetorical questions create dramatic pressure before the answering line arrives.",
        "Repeated gate summons return with greater force rather than functioning as filler.",
        "Concrete verbs such as ascend, stand, receive, lift, enter, and fight carry doctrine through action.",
        "End rhyme and alternating line weight make the text memorable for communal speech.",
        "Syntax crosses line endings, preventing every line from sounding like an isolated slogan.",
    ],
    "poem_guidance": [
        "Give each stanza or movement a new dramatic task: creation, ascent, examination, blessing, procession, acclamation.",
        "Use question and answer where the biblical text itself supplies them.",
        "Repeat a biblical summons only when its return deepens or enlarges the scene.",
        "Prefer strong chapter verbs and nouns over decorative emotional adjectives.",
        "Let stress, breath, and syntax govern the line before enforcing exact syllable count.",
        "Allow sentences to turn across lines; vary caesura and sentence endings.",
        "Use rhyme as memory and resolution, not as a reason to add weak words.",
    ],
    "avoid": [
        "automatic archaisms",
        "identical grammar in every stanza",
        "rhyme-driven filler",
        "refrains that do not develop",
        "line-by-line prose explanation",
        "meter treated as arithmetic without dramatic movement",
    ],
}


def build_hymnody_brief(chapter_design: dict | None = None) -> dict:
    chapter_design = chapter_design or {}
    return {
        **CLASSICAL_HYMNODY_PROFILE,
        "chapter_movement": chapter_design.get("emotional_movement", ""),
        "chapter_verbs": chapter_design.get("divine_action", ""),
        "chapter_images": list(chapter_design.get("physical_vocabulary", [])),
    }
