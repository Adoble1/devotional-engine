# Immersive Sacred Devotional Ghostwriting Engine v6.5

A provider-independent Python writing system built around one principle:

> Blueprint preserves coherence. Script performs beauty. Harness validates alignment. Evaluator protects truth.

Version 6.5 keeps the full devotional state machine and adds a smaller shared writing core for fiction and nonfiction. The modes share six governing laws, but each mode loads only its own planning maps, rules, outputs, and evaluator dimensions. Devotional doctrine does not leak into fiction; fiction continuity checks do not become nonfiction rules.

## Why v6.5

Earlier versions promoted many useful passage-level corrections into global rules. That improved local drafts but risked constraint bloat, repetitive prose, and genre cross-contamination. v6.5 consolidates those observations into six governing laws:

1. Source Truth
2. Reality and Genre Fidelity
3. Continuity
4. Revelatory Pacing
5. Human Truth
6. Protected Aesthetic Freedom

Project- and passage-specific constraints remain local. They are not automatically promoted into permanent engine laws.

## Writing profiles

### Devotional

Uses the existing guarded state machine, Story Plan Blueprint, canonical development, theological risk, Christological alignment, prayer, poem, and deterministic harness.

Required profile concerns include textual sovereignty, ordinary physics unless Scripture reveals otherwise, literary-mode preservation, apostolic priority, Israel–Church continuity, and Christological fulfillment without replacement.

### Fiction

Uses world state, character state, causal scene mapping, point-of-view continuity, and a continuity ledger. It protects the declared physics of the story world and requires emotion to arise from character perception, desire, action, and consequence.

### Nonfiction

Uses claim–evidence mapping, argument structure, source and uncertainty ledgers, and explicit separation of fact, inference, and opinion.

## Installation and tests

```bash
python -m pip install -e '.[test]'
python -m pytest
```

The package otherwise uses the Python standard library.

## Full devotional pipeline

```python
from devotional_engine import EngineContext, run_engine

ctx = EngineContext(chapter_ref="Psalm 49", source_text="...")
result = run_engine(ctx, RealAdapter())
```

`run_engine` remains the full devotional path. It is blueprint-first, fail-closed, and compatible with the existing deterministic mock fixtures.

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

The profiled runner uses four roles:

- `profile_planner`
- `profile_composer`
- `profile_evaluator`
- `profile_reviser` when one bounded revision is needed

## Safety and production limits

The repository contains no provider credentials or live model implementation. Real adapters must handle timeouts, bounded retries, model/version logging, secret management, prompt-injection isolation, and provider response normalization.

`DONE` or a passing profile evaluation means the configured local checks passed. It does not replace human theological, editorial, factual, or publication review.
