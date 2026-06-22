# Immersive Sacred Devotional Ghostwriting Engine v6.3

A local, deterministic Python skeleton for the **Truth–Beauty Discovery Engine**. It moves a chapter through source and rendering layers, chapter design, theological risk, art direction, creative divergence, a director's arc gate, structured prose and poem composition, deterministic checks, beauty/evaluator/contradiction passes, protected editorial smoothing, ledger capture, and final artifact rendering.

The package deliberately has **no UI and no live LLM integration**. Every creative or theological role is accessed through `AgentAdapter`; the included `MockAgentAdapter` makes runs reproducible and testable.

## Requirements and setup

Python 3.11 or newer is required. From the repository root:

```bash
python -m pip install -e '.[test]'
python -m pytest
```

The implementation otherwise uses the Python standard library.

## Mock integrations

```bash
python examples/run_psalm18_mock.py
python examples/run_psalm19_mock.py
python examples/run_psalm20_mock.py
python examples/run_psalm21_mock.py
python examples/run_psalm22_mock.py
python examples/run_psalm22_flow.py
python examples/run_psalm23_mock.py
python examples/run_psalm23_flow.py
python examples/run_psalm24_mock.py
python examples/run_psalm24_flow.py
python examples/render_psalm22_html.py
python examples/show_american_style_brief.py
```

Each example loads its matching JSON fixture, runs every state, requires the trace to end at `DONE`, and prints the validated Markdown artifact. Psalm 18 uses **“Love speaks before thunder.”** Psalm 19 uses **“Creation speaks without a sound.”** Psalm 20 uses **“Trouble teaches the true name.”** Psalm 21 uses **“The crown is mercy.”** Psalm 22 uses **“The circle opens into song.”** Psalm 23 uses **“Mercy learns the road.”** Psalm 24 uses **“The gates remember their King.”**

The Psalm 22 flow renderer prints a heading-free devotional with the full focus-verse rendering immediately after the opening sentence. The Psalm 22 HTML renderer writes `artifacts/psalm22_devotional.html`.

## Implemented now

- Complete state enum and guarded state-machine runner.
- Dataclass engine context and role temperature metadata.
- Mock adapter and lightweight contracts for major structured agent outputs.
- Chapter-arc and threshold-phrase validation.
- Explicit deterministic check registry, including optional common-meter stanza/rhyme checks, open lyric shape checks, prayer, structure, risk-register, proof-chain, and conservative read-aloud checks.
- First-pass source grounding, long-quotation verification, Christological anchor checks, forbidden engine-label detection, and repeated-stanza rejection.
- American pre-1950 literary pattern matching for prose and poetry, with automatic style-brief generation before art direction, public-domain gating, and anti-pastiche validation.
- Creative mastery guidance distilled into safe craft principles: concrete chapter-born images, organic form, emotional inevitability, musical cadence, and image physics.
- Public-domain classical hymnody guidance for question-and-answer movement, developing refrain, strong chapter verbs, varied syntax, and non-mechanical cadence without forced archaism.
- Poetic music guidance for euphony, meaningful roughness, occasional trochaic first-foot inversion, and grammatical mid-line breath.
- Optional full-focus-verse and same-chapter reference discipline for heading-free flow devotionals.
- Optional key-verse selection enforcement that rejects using the entire chapter as the devotional focus passage.
- Optional poem-quality warnings for filler adverbs, false image physics, explanatory language, and ungrounded emotional padding, plus strict beauty mode that can promote those warnings into revision pressure.
- Heuristic beauty pass, evaluator and contradiction-editor contracts.
- Prose-only editorial smoothing with immutable fields, deterministic revalidation, and rollback.
- Structured-only Markdown renderer and ordered-heading validation.
- Sequence ledger updates and regression tests.
- Global state-transition guard plus bounded voice, beauty, evaluator, contradiction, checker, gate, and editorial loops.

The engine still remains a local deterministic skeleton. It does not provide live model credentials, a web UI, persistent storage, deployment infrastructure, or human publication approval workflow.

## Production safety notes

Before publishing generated devotionals publicly, add a real model adapter with timeouts, bounded retries, model/version logging, secret management, prompt-injection isolation, and rate limits. Keep Scripture licensing and quotation attribution explicit, and require human theological/editorial review before release.

The current harness is intentionally conservative, but some semantic checks remain heuristic. Treat `DONE` as "locally validated by configured checks," not as a replacement for human review.

See `docs/GO_LIVE_CHECKLIST.md`, `docs/SECURITY.md`, `docs/POETIC_FLOW.md`, `docs/AMERICAN_LITERARY_SYSTEM.md`, `docs/MODULAR_STAGE_LOOP.md`, and `docs/ENGINE_REVIEW.md` for the local launch checklist, approval expectations, security notes, poem-agent creative-flow guidance, American literary pattern system, modular stage loop, and current creative/coherence/stability review.

## Adding a real model adapter

Implement the `AgentAdapter.call(role, payload)` protocol and return dictionaries matching each role's contract. The role names and temperature metadata are in `devotional_engine/config.py`. Keep API credentials, retries, provider-specific schemas, and network behavior inside the adapter; the engine core should remain provider-independent. Validate or normalize provider responses before returning them, then pass the adapter to:

```python
ctx = run_engine(EngineContext(chapter_ref="Psalm 18", source_text="..."), RealAdapter())
```

A production adapter should also record model/version metadata externally and preserve deterministic mocks for regression tests.

The package includes `UnconfiguredExternalModelAdapter` as a fail-closed scaffold. It validates adapter configuration shape but intentionally refuses to call any provider until a real adapter is implemented.
