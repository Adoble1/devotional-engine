from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devotional_engine import EngineConfig, EngineContext, MockAgentAdapter, State, render_flow_artifact, run_engine


def main() -> None:
    outputs = json.loads((Path(__file__).with_name("psalm23_mock_outputs.json")).read_text())
    config = EngineConfig(
        require_full_focus_verses=True,
        enforce_same_chapter_reference_style=True,
        warn_unnecessary_adverbs=True,
        warn_image_physics=True,
        warn_explanatory_poem=True,
        warn_grounded_qualia=True,
    )
    ctx = run_engine(EngineContext(chapter_ref="Psalm 23"), MockAgentAdapter(outputs), config)
    if not ctx.trace or ctx.trace[-1] is not State.DONE:
        raise SystemExit(f"Engine did not finish: {ctx.error or ctx.failed_checks}")
    print(render_flow_artifact(ctx))


if __name__ == "__main__":
    main()
