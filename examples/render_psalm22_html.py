from pathlib import Path
from html import escape
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devotional_engine import EngineContext, MockAgentAdapter, State, run_engine


def render_html(markdown: str) -> str:
    lines = markdown.splitlines()
    body = []
    in_poem = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            body.append(f"<h1>{escape(line[2:].strip())}</h1>")
            in_poem = False
        elif line.startswith("## "):
            heading = line[3:].strip()
            body.append(f"<h2>{escape(heading)}</h2>")
            in_poem = heading == "Poem"
        elif line.startswith("*") and line.endswith("*"):
            body.append(f"<p class=\"epigraph\"><em>{escape(line.strip('*'))}</em></p>")
            in_poem = False
        elif in_poem:
            body.append(f"<p class=\"poem-line\">{escape(line)}</p>")
        else:
            body.append(f"<p>{escape(line)}</p>")
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Psalm 22 Devotional - The Circle Opens</title>
  <style>
    body {
      color: #241c15;
      background: #fbf7ef;
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.58;
      margin: 0;
      padding: 3rem 1.25rem;
    }
    main {
      background: #fffdf8;
      border: 1px solid #e7dcc8;
      box-shadow: 0 16px 40px rgba(70, 48, 24, 0.08);
      margin: 0 auto;
      max-width: 760px;
      padding: 3rem;
    }
    h1 {
      font-size: 2.35rem;
      letter-spacing: -0.03em;
      margin: 0 0 0.5rem;
      text-align: center;
    }
    h2 {
      border-top: 1px solid #eadfce;
      color: #5a351a;
      font-size: 1.1rem;
      margin-top: 2rem;
      padding-top: 1.2rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    p {
      font-size: 1.05rem;
      margin: 0.7rem 0;
    }
    .epigraph {
      color: #6b4b2b;
      margin-bottom: 2rem;
      text-align: center;
    }
    .poem-line {
      margin: 0.1rem 0 0.1rem 1.25rem;
      white-space: pre-wrap;
    }
    h2 + .poem-line {
      margin-top: 0.75rem;
    }
  </style>
</head>
<body>
<main>
""" + "\n".join(body) + """
</main>
</body>
</html>
"""


def main() -> None:
    outputs = json.loads((Path(__file__).with_name("psalm22_mock_outputs.json")).read_text())
    ctx = run_engine(EngineContext(chapter_ref="Psalm 22"), MockAgentAdapter(outputs))
    if not ctx.trace or ctx.trace[-1] is not State.DONE:
        raise SystemExit(f"Engine did not finish: {ctx.error or ctx.failed_checks}")
    out_path = ROOT / "artifacts" / "psalm22_devotional.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(ctx.artifact), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
