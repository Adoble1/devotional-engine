from .models import EngineContext
import re

HEADINGS = [
    "## Focus Bible Verses", "## I. Introduction", "## II. Reflection",
    "## III. Christ the Fulfillment", "## IV. Personal Application",
    "## Prayer", "## Poem", "## Next in sequence",
]

FLOW_KEYS = ["reflection", "christ_fulfillment", "application", "prayer"]


def _display_key(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _split_opening_sentence(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return "", ""
    if "\n\n" in stripped:
        opening, remainder = stripped.split("\n\n", 1)
        return opening.strip(), remainder.strip()
    match = re.search(r"(?<=[.!?])\s+", stripped)
    if not match:
        return stripped, ""
    return stripped[: match.start()].strip(), stripped[match.end() :].strip()


def render_artifact(ctx: EngineContext) -> str:
    p = ctx.prose
    return (
        f"# {p['title']}\n\n" f"*{p['epigraph']}*\n\n"
        f"## Focus Bible Verses\n\n" f"{p['focus_bible_verses'].strip()}\n\n"
        f"## I. Introduction\n\n" f"{p['introduction'].strip()}\n\n"
        f"## II. Reflection\n\n" f"{p['reflection'].strip()}\n\n"
        f"## III. Christ the Fulfillment\n\n" f"{p['christ_fulfillment'].strip()}\n\n"
        f"## IV. Personal Application\n\n" f"{p['application'].strip()}\n\n"
        f"## Prayer\n\n" f"{p['prayer'].strip()}\n\n"
        f"## Poem\n\n" f"{ctx.poem.strip()}\n\n"
        f"## Next in sequence\n\n" f"{p['next_in_sequence'].strip()}\n"
    )


def validate_artifact_structure(md_text: str) -> bool:
    if not md_text.startswith("# "):
        return False
    heading_lines = [line.strip() for line in md_text.splitlines() if line.startswith("## ")]
    if heading_lines != HEADINGS:
        return False
    positions = [md_text.find(h) for h in HEADINGS]
    return all(p >= 0 for p in positions) and positions == sorted(positions)


def render_flow_artifact(ctx: EngineContext) -> str:
    p = ctx.prose
    opening, introduction_remainder = _split_opening_sentence(p["introduction"])
    title = p["title"].strip()
    blocks = [title]
    epigraph = p["epigraph"].strip()
    title_key = _display_key(title)
    opening_key = _display_key(opening)
    if epigraph and _display_key(epigraph) not in {title_key, opening_key}:
        blocks.append(epigraph)
    if opening and opening_key != title_key:
        blocks.append(opening)
    blocks.append(p["focus_bible_verses"].strip())
    if introduction_remainder:
        blocks.append(introduction_remainder)
    blocks.extend(p[key].strip() for key in FLOW_KEYS)
    blocks.append(ctx.poem.strip())
    blocks.append(p["next_in_sequence"].strip())
    return "\n\n".join(block for block in blocks if block).strip() + "\n"
