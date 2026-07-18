# Immersive Sacred Devotional Ghostwriting Engine v6.6

A provider-independent writing system built around one principle:

> Blueprint preserves coherence. Script performs beauty. Harness validates alignment. Evaluator protects truth.

Version 6.6 simplifies the production devotional path to four stages while preserving Scripture provenance, canonical discipline, deterministic validation, bounded repair, and human publication review.

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

1. `devotional_grounder` — one Text Grounding Packet containing source wording, provenance, historical meaning, literary mode, textual evidence, governing claim, hinge, divine action, canonical classification, Christological fulfillment, and risks.
2. `devotional_planner` — one Passage Blueprint containing the governing question, reader transformation, section burdens, governing image, art direction, poem arc, supporting elements, and local constraints.
3. `devotional_composer` — one protected creative pass. The composer may freely choose title, opening, paragraph shape, imagery, cadence, transitions, and poem form while the grounding and blueprint remain immutable.
4. `devotional_reviewer` — one integrated review separating hard findings from advisory literary judgment. At most one targeted revision is permitted by default.

The deterministic control path is:

`textual evidence -> governing claim -> textual hinge -> divine answer -> canonical fulfillment -> reader response`

That path protects meaning. It does not prescribe sentence rhythm, paragraph count, metaphor count, title shape, or poem form.

## Compatibility

`run_engine` defaults to `EngineConfig(devotional_pipeline="auto")`.

- Real adapters use the integrated four-stage path.
- Mocks that provide all four integrated roles use that path.
- Older deterministic mock fixtures automatically use the v6.5 legacy compatibility runner.

Explicit selection is available:

```python
from devotional_engine import EngineConfig, EngineContext, run_engine

config = EngineConfig(devotional_pipeline="integrated")
result = run_engine(EngineContext(chapter_ref="Psalm 52"), RealAdapter(), config)
```

The legacy path remains for regression safety, not as the recommended production design.

## Scripture source contract

Every source and rendering must identify one quotation mode:

- `public_domain` — named translation and edition, attribution, and verified exact quotation.
- `licensed` — named translation and edition, attribution, license profile, and verified exact quotation.
- `independent_rendering` — identified Hebrew or Greek source, explicit attribution, and mandatory human review.
- `paraphrase` — identified source, explicit attribution, and mandatory human review.

Example independent rendering metadata:

```python
{
    "quotation_mode": "independent_rendering",
    "source_text_id": "Masoretic Text / Psalm 52",
    "attribution": "Independent rendering from the Hebrew",
    "verified_exact_match": False,
    "human_review_required": True,
}
```

Missing or malformed provenance fails before planning or composition. The selected attribution is rendered beneath the focus verses. Deterministic `MockAgentAdapter` runs may use `test_fixture`, which is always labeled not for publication.

## Integrated review contract

Hard findings include:

- unsupported textual or historical claims;
- invalid Scripture provenance;
- contradiction of the approved blueprint;
- canonical overclaim;
- serious theological error;
- disconnected application;
- missing required artifact fields;
- deterministic harness failure.

Advisory findings include:

- mechanical cadence;
- over-explanation;
- weak transitions;
- repeated language;
- supporting material that threatens to displace the governing subject;
- poem or prose that should be reviewed aloud.

Advisories do not automatically block publication or force revision. The reviewer decides whether the whole work requires one targeted repair.

## Writing profiles

### Devotional

Uses the integrated four-stage core, Scripture provenance, evidence-path validation, canonical classification, Christological fulfillment without replacement, prayer, poem, deterministic harness, and human review.

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

## Lean fiction or nonfiction pipeline

```python
from devotional_engine import WritingRequest, run_profiled_engine

request = WritingRequest(
    mode="fiction",
    project_ref="Novel / Chapter 4",
    source_material="Existing manuscript and continuity ledger",
    plan={
        "governing_question": "Will Mara reveal what she knows?",
        "truth_contract": ["The bridge is raised.", "Mara knows the signal code."],
        "local_constraints": ["Remain in Mara's point of view."],
        "planning_maps": {
            "truth_map": {"established": ["night", "raised bridge"]},
            "revelation_map": {"entry": "alarm", "turn": "recognition"},
            "reader_transformation_map": {"from": "suspicion", "to": "recognition"},
            "art_direction": {"register": "compressed suspense"},
            "world_state": {"bridge": "raised"},
            "character_state": {"Mara": {"desire": "protect her brother"}},
            "causal_scene_map": {"alarm": "crowd stops"},
            "continuity_ledger": {"chapter_3": "Mara learned the code"},
        },
    },
)

result = run_profiled_engine(request, RealAdapter())
```

## Production limits

The repository contains no provider credentials or live model implementation. Real adapters must handle timeouts, bounded retries, model/version logging, secret management, prompt-injection isolation, and provider response normalization.

A `DONE` state means the configured checks passed. It does not replace human theological, literary, rights, or publication review.
