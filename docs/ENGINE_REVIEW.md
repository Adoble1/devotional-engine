# Engine Review: Creative Freedom, Coherence, Stability

This review records the current local evidence for the engine's three active quality goals.

## Creative Freedom

Current support:

- `EngineConfig.poem_form` defaults to `open`, so the poem agent is not locked into common meter.
- `docs/POETIC_FLOW.md` describes organic flow patterns and reserves strict meter for explicit director briefs.
- `creative_divergence_agent` must produce multiple title, threshold, opening, image, christology, and poem-arc candidates.
- American literary style matching supplies craft movements and anti-pastiche guidance rather than copied source text.
- A creative mastery layer adds chapter-born imagery, organic form, emotional inevitability, musical cadence, and anti-cleverness revision targets without unsafe persona or imitation instructions.
- Flow rendering can omit devotional headings while preserving structured-field validation.

Watch points:

- Open poem bounds are still deterministic safety rails, not aesthetic proof.
- Beauty checks remain heuristic until a real evaluator adapter supplies richer critique, though strict beauty mode can make selected deterministic warnings consequential.

## Coherence

Current support:

- Chapter arc gate ties opening, closing, central thought, emotional charge, threshold phrase, and rationale together.
- Same-chapter reference discipline can require repeated chapter references to become "the psalm."
- Full focus-verse checks can reject citation-only text and KJV-style archaisms.
- Historical metaphor collision protects Psalm 22-style typology from confusing poetic beasts with physical crucifixion.
- Image-physics warnings flag known pretty-but-false images unless the source chapter itself warrants miracle physics.
- Explanatory-poem warnings can flag didactic connectors such as "not because / but because" when a poem starts explaining instead of singing.
- Grounded-qualia warnings can flag devotional language that tries to add feeling through abstract emotional adjectives without enough embodied, chapter-born detail.
- Strict beauty mode can promote filler-adverb, image-physics, explanatory-poem, and grounded-qualia warnings into beauty-pass revision pressure so a high model score cannot overrule deterministic craft concerns.

Watch points:

- Image-physics detection is intentionally conservative and pattern-based.
- Coherence still needs human review for subtle theological overreach or weak literary judgment.

## Stability

Current support:

- All agent calls go through `AgentAdapter`; local mocks are deterministic.
- State transitions are traced and bounded.
- Gate, checker, evaluator, editorial, voice, beauty, and contradiction loops are configurable through `EngineConfig`.
- Exceptions fail closed into `ESCALATED` with `ctx.error` preserved.
- Editorial smoothing snapshots prose, forbids poem/focus-verse/christology changes, and rolls back on deterministic failure.
- Regression tests cover route targets, loop termination, artifact rendering, prayer validation, poem form, style rights, reference discipline, and Psalm 18-23 mock runs.

Verification commands:

```bash
PYTHONPATH=/tmp/devotional-engine-test-deps python3 -m pytest -q
python3 examples/run_psalm22_flow.py
python3 examples/run_psalm23_flow.py
python3 -m compileall -q devotional_engine examples
git diff --check
```

## Current Conclusion

The engine is stable for local deterministic Psalm mock testing and has improved creative freedom and coherence guardrails. It is not production-ready for public devotional publishing until the go-live checklist is satisfied, especially human review, source-rights confirmation, live adapter hardening, and persistent audit logging.
