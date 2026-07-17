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
- The v6.5 coherence contract treats cross-section repetition and supporting-theme displacement as advisory findings, not universal style bans.
- Title/opening distinction is an explicit local option. Biblical refrain may still govern title, epigraph, and opening when the passage warrants it.

Watch points:

- Open poem bounds are still deterministic safety rails, not aesthetic proof.
- Beauty checks remain heuristic until a real evaluator adapter supplies richer critique, though strict beauty mode can make selected deterministic warnings consequential.

## Coherence

Current support:

- Chapter arc gate ties opening, closing, central thought, emotional charge, threshold phrase, and rationale together.
- The v6.5 coherence gate compiles one passage-center map before prose: governing subject, human predicament, supporting elements, textual hinge, divine answer, canonical fulfillment, and reader response.
- List-shaped director and art-direction instructions are deduplicated while preserving their first wording and order.
- Local and art-direction constraints are compared as one effective set; conservative exact contradictions fail before composition.
- Exact duplicate section burdens fail before composition so reflection, Christ fulfillment, application, prayer, and poem do not become the same paragraph in different clothing.
- Final prose is checked again after editorial smoothing, preventing a passing draft from drifting before artifact emission.
- Same-chapter reference discipline can require repeated chapter references to become "the psalm."
- Full focus-verse checks can reject citation-only text and KJV-style archaisms.
- Historical metaphor collision protects Psalm 22-style typology from confusing poetic beasts with physical crucifixion.
- Image-physics warnings flag known pretty-but-false images unless the source chapter itself warrants miracle physics.
- Explanatory-poem warnings can flag didactic connectors such as "not because / but because" when a poem starts explaining instead of singing.
- Grounded-qualia warnings can flag devotional language that tries to add feeling through abstract emotional adjectives without enough embodied, chapter-born detail.
- Strict beauty mode can promote filler-adverb, image-physics, explanatory-poem, and grounded-qualia warnings into beauty-pass revision pressure so a high model score cannot overrule deterministic craft concerns.

Watch points:

- Passage-center weighting is lexical and advisory; it cannot replace theological and literary judgment.
- Contradiction detection is deliberately conservative. It catches normalized opposite directives, not every subtle tension between two instructions.
- Image-physics detection is intentionally conservative and pattern-based.
- Coherence still needs human review for subtle theological overreach or weak literary judgment.

## Stability

Current support:

- All agent calls go through `AgentAdapter`; local mocks are deterministic.
- State transitions are traced and bounded.
- Gate, checker, evaluator, editorial, voice, beauty, and contradiction loops are configurable through `EngineConfig`.
- Exceptions fail closed into `ESCALATED` with `ctx.error` preserved.
- Editorial smoothing snapshots prose, forbids poem/focus-verse/christology changes, and rolls back on deterministic failure.
- Final v6.5 coherence errors convert `DONE` to `ESCALATED`; advisory warnings are deduplicated.
- Regression tests cover route targets, loop termination, artifact rendering, prayer validation, poem form, style rights, reference discipline, passage-center compilation, instruction conflicts, section-burden duplication, local title/opening distinction, final post-edit coherence, and Psalm 18-24 plus Psalm 49 runs.

Verification commands:

```bash
python -m pytest -q
python -m compileall -q devotional_engine examples
```

## Current Conclusion

The engine is stable for deterministic biblical devotional mock testing and has stronger creative-freedom and coherence guardrails. It protects a passage's governing burden without turning every successful local edit into a global formula. It is not production-ready for public devotional publishing until the go-live checklist is satisfied, especially human theological and editorial review, source-rights confirmation, live-adapter hardening, and persistent audit logging.
