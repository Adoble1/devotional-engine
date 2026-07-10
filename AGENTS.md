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
