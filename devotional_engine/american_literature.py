from dataclasses import dataclass, field
from .classical_hymnody import CLASSICAL_HYMNODY_PROFILE
from .poetic_music import POETIC_MUSIC_PROFILE

US_PUBLIC_DOMAIN_PUBLISHED_THROUGH = 1930


@dataclass(frozen=True)
class AmericanLiteraryPattern:
    pattern_id: str
    author: str
    work: str
    publication_year: int
    genre: str
    mode: str
    movement: tuple[str, ...]
    syntax: tuple[str, ...]
    image_logic: tuple[str, ...]
    devotional_use: str
    avoid: tuple[str, ...]
    keywords: tuple[str, ...]
    public_domain_us: bool
    usage: str = "pattern"
    notes: str = ""


@dataclass(frozen=True)
class StyleMatch:
    pattern: AmericanLiteraryPattern
    score: int
    matched_keywords: tuple[str, ...] = field(default_factory=tuple)


CREATIVE_MASTERY_LAYER = {
    "principles": [
        "Prefer vivid, concrete, chapter-born images over abstract explanation.",
        "Let form follow the chapter's movement: lament, praise, confession, trust, judgment, wonder, or pilgrimage.",
        "Seek emotional inevitability rather than cleverness.",
        "Maintain image physics unless the biblical chapter itself warrants miracle logic.",
        "Use musical sentences, varied cadence, restrained surprise, and felt human truth.",
    ],
    "revision_targets": [
        "coherence",
        "beauty",
        "theological fidelity",
        "image discipline",
        "read-aloud cadence",
    ],
    "avoid": [
        "named living-author imitation",
        "verbatim imitation",
        "generic devotional transitions",
        "filler adverbs",
        "ornamental metaphors detached from the chapter",
        "pretty images with broken physical logic",
    ],
}


def _pd(year: int) -> bool:
    return year <= US_PUBLIC_DOMAIN_PUBLISHED_THROUGH


AMERICAN_PATTERNS: tuple[AmericanLiteraryPattern, ...] = (
    AmericanLiteraryPattern(
        "edwards_sermon_pressure",
        "Jonathan Edwards",
        "Sinners in the Hands of an Angry God",
        1741,
        "prose",
        "sermon pressure",
        ("doctrinal premise", "image intensification", "direct address", "urgent appeal"),
        ("long periodic pressure", "plain declarative warning", "second-person narrowing"),
        ("weight", "fire", "hand", "precariousness"),
        "Use when a psalm needs holy dread without melodrama.",
        ("revenge fantasy", "shame manipulation", "unearned terror"),
        ("judgment", "wrath", "terror", "fire", "enemy", "danger"),
        _pd(1741),
    ),
    AmericanLiteraryPattern(
        "franklin_plain_moral_clarity",
        "Benjamin Franklin",
        "Autobiography",
        1791,
        "prose",
        "plain moral accounting",
        ("concrete observation", "self-scrutiny", "practical maxim", "measured resolve"),
        ("short balanced clauses", "earthy nouns", "aphoristic compression"),
        ("ledger", "habit", "tool", "daily practice"),
        "Use when application needs concreteness and humility.",
        ("smug self-improvement", "moralism without grace"),
        ("wisdom", "practice", "discipline", "speech", "work", "daily"),
        _pd(1791),
    ),
    AmericanLiteraryPattern(
        "poe_enclosed_dread",
        "Edgar Allan Poe",
        "The Fall of the House of Usher",
        1839,
        "prose",
        "enclosed dread",
        ("threshold atmosphere", "psychic pressure", "symbolic architecture", "collapse"),
        ("sensory accumulation", "claustrophobic modifiers", "delayed revelation"),
        ("house", "vault", "echo", "crack", "shadow"),
        "Use when a lament feels sealed inside a narrowing chamber.",
        ("gothic costume", "sensational horror", "despair without gospel turn"),
        ("dark", "silence", "fear", "forsaken", "beasts", "death"),
        _pd(1839),
    ),
    AmericanLiteraryPattern(
        "emerson_spiritual_turn",
        "Ralph Waldo Emerson",
        "Nature",
        1836,
        "prose",
        "perception to spiritual turn",
        ("seen world", "interior recognition", "transcendent inference", "renewed stance"),
        ("lucid abstraction", "balanced image and idea", "ascending cadence"),
        ("light", "sky", "eye", "transparent world"),
        "Use when creation imagery must become reverent perception.",
        ("vague divinity", "nature replacing revelation"),
        ("creation", "light", "heavens", "glory", "wonder", "seeing"),
        _pd(1836),
    ),
    AmericanLiteraryPattern(
        "thoreau_stripped_attention",
        "Henry David Thoreau",
        "Walden",
        1854,
        "prose",
        "stripped attention",
        ("particular object", "patient looking", "moral exposure", "simplified response"),
        ("lean sentences", "concrete nouns", "reflective pivots"),
        ("pond", "axe", "path", "morning", "bread"),
        "Use when the devotional must cut through noise into one obedient act.",
        ("self-sufficient solitude", "nature-as-savior"),
        ("attention", "quiet", "path", "morning", "obedience", "simplicity"),
        _pd(1854),
    ),
    AmericanLiteraryPattern(
        "douglass_witness_to_freedom",
        "Frederick Douglass",
        "Narrative of the Life of Frederick Douglass",
        1845,
        "prose",
        "witness to freedom",
        ("wound named plainly", "false power exposed", "turning event", "freedom speech"),
        ("controlled moral clarity", "specific scenes", "grave restraint"),
        ("chain", "book", "voice", "road", "light"),
        "Use when the chapter exposes bondage and names deliverance.",
        ("appropriating suffering", "abstracting oppression", "cheap triumph"),
        ("deliverance", "oppression", "bondage", "voice", "freedom", "rescue"),
        _pd(1845),
    ),
    AmericanLiteraryPattern(
        "hawthorne_symbolic_conscience",
        "Nathaniel Hawthorne",
        "The Scarlet Letter",
        1850,
        "prose",
        "symbolic conscience",
        ("public sign", "hidden guilt", "communal judgment", "ambiguous mercy"),
        ("formal sentences", "moral shadow", "symbolic recurrence"),
        ("mark", "cloth", "forest", "scaffold", "heart"),
        "Use when sin, shame, and public identity need careful handling.",
        ("voyeuristic guilt", "legalism", "mercy withheld"),
        ("sin", "shame", "hidden", "heart", "mercy", "judgment"),
        _pd(1850),
    ),
    AmericanLiteraryPattern(
        "melville_metaphysical_pressure",
        "Herman Melville",
        "Moby-Dick",
        1851,
        "prose",
        "metaphysical pressure",
        ("visible creature", "obsessive pursuit", "cosmic question", "humbling vastness"),
        ("catalog and surge", "biblical undertone", "philosophic interruption"),
        ("sea", "whale", "rope", "storm", "depth"),
        "Use when creaturely force opens into awe and judgment.",
        ("bombast", "overextended analogy", "captain-as-hero fixation"),
        ("sea", "storm", "depth", "leviathan", "awe", "wrath"),
        _pd(1851),
    ),
    AmericanLiteraryPattern(
        "whitman_catalogic_praise",
        "Walt Whitman",
        "Leaves of Grass",
        1855,
        "poetry",
        "catalogic praise",
        ("expansive naming", "body and world gathered", "democratic widening", "large affirmation"),
        ("long free-verse lines", "parallel clauses", "anaphoric momentum"),
        ("body", "road", "grass", "breath", "multitude"),
        "Use when praise must widen from one speaker toward many.",
        ("self-deification", "formless sprawl", "unbounded assertion"),
        ("praise", "nations", "body", "breath", "many", "congregation"),
        _pd(1855),
    ),
    AmericanLiteraryPattern(
        "dickinson_compressed_slant",
        "Emily Dickinson",
        "Poems",
        1890,
        "poetry",
        "compressed slant revelation",
        ("small aperture", "strange comparison", "dash turn", "aftershock"),
        ("compressed lines", "slant rhyme", "syntactic fracture", "capitalized pressure words"),
        ("bee", "door", "light", "grave", "nerve"),
        "Use when the psalm needs a short lyric incision rather than a hymn.",
        ("cute obscurity", "random dashes", "private code with no theological clarity"),
        ("death", "silence", "hope", "nerve", "door", "light"),
        _pd(1890),
    ),
    AmericanLiteraryPattern(
        "twain_moral_vernacular",
        "Mark Twain",
        "Adventures of Huckleberry Finn",
        1884,
        "prose",
        "vernacular moral awakening",
        ("ordinary speech", "social pressure", "conscience crisis", "plainspoken choice"),
        ("vernacular rhythm", "comic deflation", "moral plainness"),
        ("river", "raft", "shore", "fog", "road"),
        "Use sparingly when application needs plain conscience without ornament.",
        ("dialect imitation", "comic sacred tone", "regional caricature"),
        ("conscience", "river", "choice", "mercy", "neighbor", "freedom"),
        _pd(1884),
    ),
    AmericanLiteraryPattern(
        "crane_stark_naturalism",
        "Stephen Crane",
        "The Open Boat",
        1897,
        "prose",
        "stark natural pressure",
        ("small human craft", "indifferent vastness", "shared endurance", "chastened survival"),
        ("bare clauses", "hard physical detail", "unsentimental observation"),
        ("boat", "wave", "oar", "shore", "cold"),
        "Use when danger must feel physical without melodrama.",
        ("nihilism", "mercy erased", "stoic self-salvation"),
        ("waters", "danger", "weakness", "endurance", "rescue", "storm"),
        _pd(1897),
    ),
    AmericanLiteraryPattern(
        "chopin_interior_awakening",
        "Kate Chopin",
        "The Awakening",
        1899,
        "prose",
        "interior awakening",
        ("social enclosure", "inner restlessness", "sensory threshold", "costly recognition"),
        ("sensuous precision", "interior drift", "quiet defiance"),
        ("sea", "room", "bird", "heat", "threshold"),
        "Use when a psalm names desire, confinement, or the need to tell the truth inwardly.",
        ("romanticizing disobedience", "mistaking impulse for freedom"),
        ("desire", "heart", "awakening", "truth", "voice", "sea"),
        _pd(1899),
    ),
    AmericanLiteraryPattern(
        "frost_turning_image",
        "Robert Frost",
        "North of Boston",
        1914,
        "poetry",
        "plain image with late turn",
        ("ordinary scene", "plain speech", "pressure underneath", "late moral turn"),
        ("conversational blank verse", "rural concreteness", "understatement"),
        ("wall", "road", "field", "snow", "stone"),
        "Use when the poem needs plain surface and hidden ache.",
        ("greeting-card rusticity", "moral stated too early"),
        ("road", "field", "stone", "choice", "winter", "neighbor"),
        _pd(1914),
    ),
    AmericanLiteraryPattern(
        "cather_memory_landscape",
        "Willa Cather",
        "My Antonia",
        1918,
        "prose",
        "memory landscape",
        ("remembered place", "beloved figure", "loss and gratitude", "landscape as witness"),
        ("clear elegiac prose", "visual spaciousness", "restrained feeling"),
        ("prairie", "light", "house", "field", "horizon"),
        "Use when remembrance and place need reverent spaciousness.",
        ("nostalgia as salvation", "sentimental landscape"),
        ("memory", "land", "home", "light", "loss", "gratitude"),
        _pd(1918),
    ),
    AmericanLiteraryPattern(
        "eliot_modern_fragment",
        "T. S. Eliot",
        "Ash Wednesday",
        1930,
        "poetry",
        "modern fragment to prayer",
        ("spiritual exhaustion", "fragmented confession", "liturgical reach", "petition"),
        ("repetition with variation", "broken syntax", "prayerful refrain"),
        ("stair", "turning", "bone", "word", "desert"),
        "Use only for licensed or public-domain 1930 editions; good for penitential psalms.",
        ("opaque collage", "despair aesthetic", "borrowed liturgical costume"),
        ("repentance", "turn", "desert", "prayer", "word", "dryness"),
        _pd(1930),
        notes="Public-domain status depends on edition and jurisdiction; use pattern descriptors, not copied text.",
    ),
    AmericanLiteraryPattern(
        "faulkner_polyphonic_burden",
        "William Faulkner",
        "As I Lay Dying",
        1930,
        "prose",
        "polyphonic burden",
        ("many voices", "burdened journey", "fractured perception", "grim arrival"),
        ("voice differentiation", "compressed interiority", "rural severity"),
        ("road", "coffin", "river", "heat", "burden"),
        "Use only as structural pattern when a chapter has multiple human angles on one grief.",
        ("imitating dialect", "grotesque exploitation", "confusion for depth"),
        ("grief", "journey", "burden", "family", "death", "voice"),
        _pd(1930),
        notes="Pattern only; do not imitate proprietary later Faulkner works.",
    ),
    AmericanLiteraryPattern(
        "steinbeck_dust_mercy",
        "John Steinbeck",
        "The Grapes of Wrath",
        1939,
        "prose",
        "dust and communal mercy",
        ("dispossession", "journey under pressure", "communal endurance", "costly mercy"),
        ("biblical plainness", "interchapters of scale", "earth-heavy nouns"),
        ("dust", "road", "hunger", "hand", "field"),
        "Reference only unless licensed; useful for chapters of exile, hunger, and communal mercy.",
        ("unlicensed imitation", "political flattening", "poverty aesthetic"),
        ("exile", "hunger", "road", "poor", "mercy", "justice"),
        False,
        usage="licensed_reference_only",
        notes="Published after the current U.S. public-domain cutoff; descriptors only without license.",
    ),
    AmericanLiteraryPattern(
        "hughes_blues_resilience",
        "Langston Hughes",
        "Montage of a Dream Deferred",
        1951,
        "poetry",
        "blues resilience",
        ("wounded dream", "musical repetition", "communal voice", "deferred ache"),
        ("jazz cadence", "refrain", "street-level compression"),
        ("dream", "street", "music", "night", "voice"),
        "Excluded by the requested cutoff, included as a blocked example to prevent accidental use.",
        ("using post-cutoff works", "appropriating voice", "unlicensed imitation"),
        ("dream", "deferred", "song", "city", "ache"),
        False,
        usage="blocked_post_cutoff",
        notes="After 1950; blocked by this system.",
    ),
)


def public_domain_patterns(patterns: tuple[AmericanLiteraryPattern, ...] = AMERICAN_PATTERNS) -> list[AmericanLiteraryPattern]:
    return [pattern for pattern in patterns if pattern.public_domain_us and pattern.usage == "pattern"]


def pre_1950_reference_patterns(patterns: tuple[AmericanLiteraryPattern, ...] = AMERICAN_PATTERNS) -> list[AmericanLiteraryPattern]:
    return [pattern for pattern in patterns if pattern.publication_year <= 1950]


def blocked_patterns(patterns: tuple[AmericanLiteraryPattern, ...] = AMERICAN_PATTERNS) -> list[AmericanLiteraryPattern]:
    return [pattern for pattern in patterns if not pattern.public_domain_us or pattern.usage != "pattern"]


def match_american_patterns(signals: list[str] | tuple[str, ...] | str, *, include_restricted: bool = False, limit: int = 4) -> list[StyleMatch]:
    if isinstance(signals, str):
        signal_words = set(signals.lower().replace("-", " ").split())
    else:
        signal_words = set(" ".join(signals).lower().replace("-", " ").split())
    candidates = pre_1950_reference_patterns() if include_restricted else public_domain_patterns()
    matches = []
    for pattern in candidates:
        matched = tuple(sorted(set(pattern.keywords).intersection(signal_words)))
        score = len(matched)
        if score:
            matches.append(StyleMatch(pattern=pattern, score=score, matched_keywords=matched))
    return sorted(matches, key=lambda item: (-item.score, item.pattern.publication_year, item.pattern.pattern_id))[:limit]


def build_style_brief(matches: list[StyleMatch]) -> dict:
    return {
        "creative_mastery": CREATIVE_MASTERY_LAYER,
        "classical_hymnody": CLASSICAL_HYMNODY_PROFILE,
        "poetic_music": POETIC_MUSIC_PROFILE,
        "style_sources": [
            {
                "pattern_id": match.pattern.pattern_id,
                "author": match.pattern.author,
                "work": match.pattern.work,
                "genre": match.pattern.genre,
                "mode": match.pattern.mode,
                "matched_keywords": list(match.matched_keywords),
            }
            for match in matches
        ],
        "movement_guidance": [step for match in matches for step in match.pattern.movement],
        "syntax_guidance": [item for match in matches for item in match.pattern.syntax],
        "image_guidance": [item for match in matches for item in match.pattern.image_logic],
        "avoid": sorted(
            {item for match in matches for item in match.pattern.avoid}
            | set(CREATIVE_MASTERY_LAYER["avoid"])
            | {"named author pastiche", "verbatim imitation"}
        ),
    }


def validate_style_brief(brief: dict) -> list[str]:
    failures = []
    for source in brief.get("style_sources", []):
        pattern = next((item for item in AMERICAN_PATTERNS if item.pattern_id == source.get("pattern_id")), None)
        if pattern is None:
            failures.append(f"unknown style pattern: {source.get('pattern_id')}")
        elif not pattern.public_domain_us or pattern.usage != "pattern":
            failures.append(f"restricted style pattern used without license: {pattern.pattern_id}")
    return failures
