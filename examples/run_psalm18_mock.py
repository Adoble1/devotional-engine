from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def main() -> None:
    outputs = json.loads((Path(__file__).with_name("psalm18_mock_outputs.json")).read_text())
    ctx = run_engine(EngineContext(chapter_ref="Psalm 18"), MockAgentAdapter(outputs))
    if not ctx.trace or ctx.trace[-1] is not State.DONE:
        raise SystemExit(f"Engine did not finish: {ctx.error or ctx.failed_checks}")
    print(ctx.artifact)
    print("\nTRACE:", " -> ".join(state.name for state in ctx.trace), file=sys.stderr)


if __name__ == "__main__":
    main()
