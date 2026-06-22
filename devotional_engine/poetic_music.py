import re


SOFT_CONSONANTS = frozenset("lmnr swh".replace(" ", ""))
OPEN_VOWELS = frozenset("oae")
HARSH_CLUSTERS = ("pt", "kt", "ks", "ct", "xt", "rk", "ck", "cks")
ROUGH_TEXTURE_SIGNALS = ("battle", "judgment", "wrath", "terror", "break", "war", "enemy", "thunder")

POETIC_MUSIC_PROFILE = {
    "priority_order": [
        "textual and theological truth",
        "chapter-born image and physical coherence",
        "dramatic movement",
        "breath and stress",
        "euphony",
    ],
    "euphony": {
        "favor": "soft rolling consonants and open vowels when the chapter's emotional movement permits",
        "soft_consonants": sorted(SOFT_CONSONANTS),
        "open_vowels": sorted(OPEN_VOWELS),
        "watch_clusters": list(HARSH_CLUSTERS),
        "rule": "prefer vocal continuity, but retain rough sounds when they enact battle, rupture, judgment, or fear",
    },
    "meter": {
        "base": "common meter usually leans iambic",
        "variation": "allow occasional first-foot trochaic inversion for emphasis before returning to the prevailing pulse",
        "limit": "use inversion as meaningful syncopation, not on every line",
        "warning": "do not infer English stress mechanically from spelling alone",
    },
    "caesura": {
        "guidance": "place a natural grammatical breath near the middle of selected long lines",
        "marks": [",", ";", ":", "—"],
        "rule": "the pause must clarify syntax or intensify the turn; do not sprinkle punctuation to simulate music",
    },
}


def build_poetic_music_brief(chapter_design: dict | None = None) -> dict:
    chapter_design = chapter_design or {}
    signals = " ".join(
        [
            str(chapter_design.get("emotional_movement", "")),
            str(chapter_design.get("divine_action", "")),
            " ".join(str(item) for item in chapter_design.get("physical_vocabulary", [])),
        ]
    ).lower()
    roughness_warranted = any(signal in signals for signal in ROUGH_TEXTURE_SIGNALS)
    return {
        **POETIC_MUSIC_PROFILE,
        "sonic_mode": "mixed texture" if roughness_warranted else "predominantly euphonic",
        "roughness_warranted": roughness_warranted,
    }


def analyze_euphony(text: str) -> dict:
    low = text.lower()
    letters = [character for character in low if character.isalpha()]
    consonants = [character for character in letters if character not in "aeiouy"]
    soft_count = sum(character in SOFT_CONSONANTS for character in consonants)
    open_vowel_count = sum(character in OPEN_VOWELS for character in letters)
    cluster_hits = [cluster for cluster in HARSH_CLUSTERS for _ in re.finditer(re.escape(cluster), low)]
    words = re.findall(r"[a-z]+", low)
    return {
        "soft_consonant_ratio": soft_count / len(consonants) if consonants else 0.0,
        "open_vowel_ratio": open_vowel_count / len(letters) if letters else 0.0,
        "harsh_cluster_count": len(cluster_hits),
        "harsh_clusters_per_100_words": (len(cluster_hits) * 100 / len(words)) if words else 0.0,
    }


def has_midline_caesura(line: str) -> bool:
    words = line.split()
    if len(words) < 5:
        return False
    for index, word in enumerate(words[1:-1], 1):
        if any(mark in word for mark in POETIC_MUSIC_PROFILE["caesura"]["marks"]):
            position = index / (len(words) - 1)
            if 0.3 <= position <= 0.7:
                return True
    return False
