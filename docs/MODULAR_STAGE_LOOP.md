# Modular Stage Loop

The stage loop separates a creative or engineering task into four reusable passes. The goal is not to make the system more verbose; it is to keep what worked, name what failed, discard the failed parts, and recombine a cleaner next version.

## 1. Planning Stage

- Define the task, objectives, and constraints.
- Name the verification boundary before generation begins.
- Produce a plan artifact, not final prose.

## 2. Tool-Use Stage

- Run agents, tools, searches, renderers, or local checks.
- Save each output as a separate artifact with optional claims, evidence, and tags.
- Avoid blending partial results too early.

## 3. Verification Stage

- Test each artifact independently.
- Accept artifacts that meet the checks.
- Reject failed artifacts with explicit reasons.
- Do not let a strong artifact rescue a weak one by proximity.

## 4. Reflection Stage

- Retain accepted artifacts.
- Jettison rejected artifacts and preserve the discard reasons.
- Recombine only verified content into an improved version.
- Carry lessons forward without carrying failed text forward.

## Why This Helps Devotional Writing

For truth, the verification stage can require source evidence, chapter-born imagery, quote fidelity, Christology anchors, and contradiction review.

For beauty, it can require concrete image pressure, musical cadence, grounded qualia, and freedom from filler adverbs or decorative emotional words. The engine should not add “ache,” “tenderness,” or “wonder” as perfume. It should let feeling arise from embodied, chapter-specific perception: cup, oil, road, table, shadow, bread, water, house.

## Local API

Use `run_stage_cycle` for the full loop, or call each stage independently:

```python
from devotional_engine import run_stage_cycle

_, _, verification, reflection = run_stage_cycle(
    "Revise Psalm 23 poem",
    outputs=[
        {"id": "kept", "content": "The cup cannot hold its brim.", "evidence": ("cup",)},
        {"id": "cut", "content": "Beautiful emotion happens.", "evidence": ()},
    ],
    checks={"has_evidence": lambda artifact: (bool(artifact.evidence), "missing evidence")},
)
```

The resulting `reflection.improved_version` contains only retained artifact content plus discard reasons for auditability.
