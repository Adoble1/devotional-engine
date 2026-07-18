# Immersive Sacred Devotional Ghostwriting Engine v6.7

A provider-independent writing system built around one principle:

> Blueprint preserves coherence. Script performs beauty. Harness validates alignment. Evaluator protects truth.

Version 6.7 keeps the four-stage devotional path but changes what each stage is allowed to carry. Research remains dense. The blueprint becomes spare. The composer receives only the load-bearing passage path and literary direction. The poem receives its own image-and-sound design rather than a sermon outline.

## Governing laws

All writing profiles share six laws:

1. Source Truth
2. Reality and Genre Fidelity
3. Continuity
4. Revelatory Pacing
5. Human Truth
6. Protected Aesthetic Freedom

Project- and passage-specific constraints remain local. A successful edit is not automatically promoted into a permanent global rule.

## Four-stage devotional core

Production adapters use:

1. `devotional_grounder` — source wording, provenance, historical meaning, literary mode, textual evidence, governing claim, hinge, divine action, canonical classification, Christological fulfillment, and risks.
2. `devotional_planner` — one governing question, one reader transformation, five concise prose movements, art direction, and a separate poem design.
3. `devotional_composer` — one protected creative pass using a lean composition packet rather than the full research context.
4. `devotional_reviewer` — one integrated truth-and-literature review, with at most one targeted revision by default.

The deterministic control path is:

`textual evidence -> governing claim -> textual hinge -> divine answer -> canonical fulfillment -> reader response`

That path protects meaning. It does not prescribe sentence rhythm, paragraph count, metaphor count, title shape, or poem form.

## Literary economy contract

The composer receives only:

- verified Scripture wording and provenance;
- the governing question, subject, hinge, and divine answer;
- the canonical classification and fulfillment;
- the reader transformation;
- one movement for each prose section;
- art direction;
- a compact set of non-duplicated boundaries;
- literary targets for economy.

The full grounding packet and legacy context object are not passed into composition. Duplicate local constraints already represented by risk boundaries are removed.

Literary targets are advisory signals, not universal hard limits. The defaults surface:

- devotional bodies that exceed roughly 850 words;
- a single prose section carrying more than half the argument;
- poems exceeding roughly 16 lines;
- prose-like average line length;
- lineation dominated by complete prose sentences;
- expository poem language;
- poem lines copied from the reflection;
- weak passage-born sensory presence.

The controlling editorial question is:

> Does every sentence and every line earn its place?

## Poem design

The poem is not assigned a sixth prose burden. It receives:

```python
{
    "image_field": ["razor", "olive tree"],
    "sensory_palette": ["steel", "root", "olive leaf", "oil", "wind"],
    "sonic_movement": "hard consonants opening into quieter breath",
    "emotional_turn": "from sudden injury to life held underground",
    "prohibited_exposition": [
        "do not summarize the reflection",
        "do not explain the theological argument",
        "do not turn prose sentences into line breaks",
    ],
}
```

The poem should transform the devotional’s emotional truth through image, sound, breath, compression, and qualia. It should not restate the thesis in shorter lines.

## Integrated review contract

Hard findings include unsupported textual or historical claims, invalid provenance, blueprint contradiction, canonical overclaim, serious theological error, disconnected application, missing artifact fields, and deterministic harness failure.

The reviewer also scores:

- textual fidelity;
- theological accuracy;
- canonical warrant;
- blueprint alignment;
- verbal economy;
- literary quality;
- poetic integrity;
- sensory presence;
- read-aloud flow.

A passing review must meet the configured minimum in every dimension. Literary findings remain advisory evidence, but the reviewer may use them to require one targeted revision. Repair instructions say: cut before adding.

## Compatibility

`run_engine` defaults to `EngineConfig(devotional_pipeline="auto")`.

- Real adapters use the literature-first integrated path.
- Mocks that provide all four integrated roles use that path.
- Older deterministic mock fixtures automatically use the v6.5 legacy compatibility runner.

The legacy path remains for regression safety, not as the recommended production design.

## Scripture source contract

Every source and rendering must identify one quotation mode:

- `public_domain` — named translation and edition, attribution, and verified exact quotation.
- `licensed` — named translation and edition, attribution, license profile, and verified exact quotation.
- `independent_rendering` — identified Hebrew or Greek source, explicit attribution, and mandatory human review.
- `paraphrase` — identified source, explicit attribution, and mandatory human review.

Missing or malformed provenance fails before planning or composition. The selected attribution is rendered beneath the focus verses. Deterministic `MockAgentAdapter` runs may use `test_fixture`, which is always labeled not for publication.

## Writing profiles

### Devotional

Uses the four-stage literature-first core, Scripture provenance, evidence-path validation, canonical classification, Christological fulfillment without replacement, prayer, poem, deterministic harness, and human review.

### Fiction

Uses world state, character state, causal scene mapping, point-of-view continuity, and a continuity ledger.

### Nonfiction

Uses claim-evidence mapping, argument structure, source and uncertainty ledgers, and explicit separation of fact, inference, and opinion.

## Installation and tests

```bash
python -m pip install -e '.[test]'
python -m pytest
python -m compileall -q devotional_engine examples
```

The package otherwise uses the Python standard library.

## Production limits

The repository contains no provider credentials or live model implementation. Real adapters must handle timeouts, bounded retries, model/version logging, secret management, prompt-injection isolation, and provider response normalization.

A `DONE` state means the configured checks passed. It does not replace human theological, literary, rights, or publication review.
