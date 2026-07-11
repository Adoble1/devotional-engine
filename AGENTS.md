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
- Interpret each passage through a global canonical view: historical meaning, canonical trajectory, apostolic interpretation, Christological fulfillment, ecclesial application, then personal application.
- When the New Testament explicitly quotes or interprets an Old Testament passage, that apostolic interpretation outranks thematic echoes while preserving the Old Testament setting.
- Identify the mystery or unresolved tension in the earlier revelation and the later canonical revelation that fulfills rather than replaces it.
- Protect Scripture, creedal language, and standard doctrine while rejecting distinctive unattributed overlap, imitation of living authors, and generic AI cadence.
- Prefer discovery before explanation. Stage the textual sequence and let the reader perceive the tension before supplying interpretation.

## Global canonical view

Every blueprint must record:

1. Historical meaning in its original covenant and literary setting.
2. Canonical trajectory through the rest of Scripture.
3. Explicit apostolic quotation or interpretation, when present.
4. Christological fulfillment that preserves continuity and escalation.
5. Governing mystery left unresolved in the earlier text.
6. Governing revelation disclosed later in the canon.

Explicit New Testament interpretation is the highest-ranked canonical link. Typology, thematic correspondence, and general echoes remain subordinate.

## Earned emotion rule

The body must carry the feeling before the prose names it. Prefer panting, interrupted breathing, repeated drinking, clenched hands, lowered posture, tears used as food, or another warranted physical fact over an abstract emotional label.

Bad: `The deer longs desperately for water.`

Better: `The deer comes panting toward the stream. It lowers its head and drinks, lifting only long enough to breathe.`

The second version earns thirst through action. It also preserves the text's claim without inventing a dry stream.

## Originality and plagiarism rule

Before delivery, distinguish protected common material from creative prose.

Protected material:

- Scripture quotations and close working translations.
- Historic creedal and doctrinal formulations.
- Names, dates, and established theological terms.

Creative material must:

- contain no substantial distinctive unattributed overlap with a source;
- avoid deliberate imitation of a living author or model-generated reference piece;
- avoid repeated house phrases, perfectly balanced aphorisms, and generic AI devotional cadence;
- record intentional sources in an influence ledger;
- regenerate rather than lightly paraphrase when overlap is substantial.

Originality concerns expression, not novelty of doctrine. Ancient truth should receive fresh, text-governed language.

## Commands

```bash
python -m pip install -e '.[test]'
python -m pytest
```

## Prohibited shortcuts

- Do not replace the existing state machine with a simplified rewrite.
- Do not bypass deterministic checks, risk checks, canonical hierarchy, originality checks, or human-review boundaries.
- Do not add provider credentials or live model calls to the core package.
- Do not silently mutate source, canonical, or theological fields.
- Do not let literary novelty outrank explicit apostolic interpretation.

## Workflow

Work on a feature branch, keep changes reviewable, document architectural effects, and submit a pull request against `main`.
