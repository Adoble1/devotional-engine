# Writing Profiles and Rule Compilation

Version 6.5 separates the shared writing architecture from genre-specific requirements.

## Shared core

Every mode compiles the same six governing laws: source truth, reality and genre, continuity, revelatory pacing, human truth, and aesthetic freedom.

The compiler deduplicates legacy rules by mapping them into those laws. For example:

- `emotion_earned_by_physical_fact` maps to `human_truth`.
- `no_unwarranted_deprivation` maps to `source_truth`.
- `genre_preservation` and `physics_consistency` map to `reality_and_genre`.
- `discovery_before_explanation` maps to `revelatory_pacing`.

An unknown local instruction is not promoted. It remains in the planning packet's `local_constraints`.

## Planning maps

All modes require:

- truth map
- revelation map
- reader transformation map
- art direction

Devotional adds:

- canonical map
- theological risk map

Fiction adds:

- world state
- character state
- causal scene map
- continuity ledger

Nonfiction adds:

- claim–evidence map
- argument map
- uncertainty ledger
- source ledger

## Execution paths

`run_engine` remains the complete devotional workflow.

`run_profiled_engine` is a bounded shared path for fiction, nonfiction, and smaller experiments. It validates the planning packet, composes a draft, evaluates against mode-specific dimensions, permits at most the configured number of revisions, and fails closed if the result does not pass.

This split protects the mature devotional harness while allowing fiction and nonfiction to share its planning discipline without inheriting devotional output sections or theological checks.
