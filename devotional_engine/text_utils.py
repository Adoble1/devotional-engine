import re

PERSISTENT_SYLLABLE_EXCEPTIONS = {
    "never": 2, "upon": 2, "every": 2, "portion": 2, "fallen": 2,
    "pleasures": 2, "evermore": 3, "measured": 2, "measures": 2,
    "heaven": 2, "heavens": 2, "rescue": 2, "rescued": 2, "thunder": 2,
    "steadfast": 2, "anointed": 3, "bowed": 1,
}


def split_stanzas(poem: str) -> list[list[str]]:
    return [[line.strip() for line in block.splitlines() if line.strip()]
            for block in re.split(r"\n\s*\n", poem.strip()) if block.strip()]


def syllables_in_word(word: str) -> int:
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    if word in PERSISTENT_SYLLABLE_EXCEPTIONS:
        return PERSISTENT_SYLLABLE_EXCEPTIONS[word]
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and not word.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(1, count)


def count_syllables(line: str) -> int:
    return sum(syllables_in_word(w) for w in re.findall(r"[A-Za-z']+", line))


def last_nonempty_line(text: str) -> str:
    return next((line.strip() for line in reversed(text.splitlines()) if line.strip()), "")


def first_words(text: str, count: int) -> str:
    return " ".join(re.findall(r"\b[\w’'-]+\b", text)[:count])


def breath_overruns(text: str, limit_words: int = 28) -> list[tuple[int, str]]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    return [(i + 1, s) for i, s in enumerate(sentences) if len(s.split()) > limit_words]


def tongue_trip_spans(text: str) -> list[str]:
    found = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words = re.findall(r"[A-Za-z]+", sentence.lower())
        for i in range(len(words) - 3):
            initials = [w[0] for w in words[i:i + 4]]
            if len(set(initials)) == 1 and all(len(w) > 3 for w in words[i:i + 4]):
                found.append(" ".join(words[i:i + 4]))
    return found
