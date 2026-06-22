from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devotional_engine import build_style_brief, match_american_patterns


def main() -> None:
    signals = ["forsaken", "beasts", "death", "congregation", "nations", "praise"]
    matches = match_american_patterns(signals)
    brief = build_style_brief(matches)
    print("Selected American literary patterns:")
    for source in brief["style_sources"]:
        print(f"- {source['pattern_id']}: {source['author']}, {source['work']} ({source['genre']})")
    print("\nMovement guidance:")
    for item in brief["movement_guidance"][:8]:
        print(f"- {item}")
    print("\nAvoid:")
    for item in brief["avoid"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
