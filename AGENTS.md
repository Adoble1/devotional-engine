# Codex instructions

## Governing architecture

Plan the devotional's state before generating its surface.

Blueprint preserves coherence. Script performs beauty. Harness validates alignment. Evaluator protects truth.

## Invariants

- Preserve deterministic mock behavior and all existing regression tests.
- Scripture source text, focus verses, Christological anchors, and approved theological claims are immutable during editorial smoothing.
- Script generation must not begin until the Story Plan Blueprint passes validation.
- Repairs must target the failing component unless a finding explicitly requires global regeneration.
- The engine remains provider-independent and fail-closed.
- Emotion must be earned through bodily action, sensory fact, consequence, or pressure already warranted by the text.
- Do not explain an emotion immediately after the physical scene has already made it legible.
- Do not invent deprivation, danger, weather, pursuit, injury, or absence merely to intensify a biblical image.
- Distinguish what the text establishes from what is only plausible. Plausible detail may never become asserted narrative fact.

## Earned emotion rule

The body must carry the feeling before the prose names it. Prefer panting, interrupted breathing, repeated drinking, clenched hands, lowered posture, tears used as food, or another warranted physical fact over an abstract emotional label.

Bad: `The deer longs desperately for water.`

Better: `The deer comes panting toward the stream. It lowers its head and drinks, lifting only long enough to breathe.`

The second version earns thirst through action. It also preserves the text's claim without inventing a dry stream.

## Commands

```bash
python -m pip install -e '.[test]'
python -m pytest
```

## Prohibited shortcuts

- Do not replace the existing state machine with a simplified rewrite.
- Do not bypass deterministic checks, risk checks, or human-review boundaries.
- Do not add provider credentials or live model calls to the core package.
- Do not silently mutate source, canonical, or theological fields.

## Workflow

Work on a feature branch, keep changes reviewable, document architectural effects, and submit a pull request against `main`.
