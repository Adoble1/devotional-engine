# Devotional Navigation Control

The devotional engine now treats generation as a bounded route rather than a single prompt. The design borrows the control discipline of navigation software without pretending that interpretation is as mechanically observable as location.

## Route

The production route is:

`grounding -> blueprint -> composition -> review -> validation -> emission`

The four model roles operate only inside the first four checkpoints. Deterministic code owns final validation and emission.

Each checkpoint records:

- status: pending, active, passed, failed, or escalated;
- attempt count;
- route sequence numbers;
- SHA-256 fingerprints of inputs and outputs;
- checkpoint-specific findings.

A role called out of order raises `NavigationContractError`. A review may route back to composition for one bounded repair. It does not regenerate approved grounding or blueprint decisions.

## Mission and objective function

Every production adapter receives a `navigation_contract` containing:

- the chapter-specific mission;
- the current checkpoint and complete route;
- completed checkpoints;
- objective weights;
- the uncertainty policy;
- the targeted-replanning rule.

The final objective function uses normalized scores from zero to one:

| Objective | Default weight | Evidence |
|---|---:|---|
| Truth | 0.35 | Textual fidelity, theological accuracy, canonical warrant, ontology, affective truth |
| Alignment | 0.20 | Blueprint alignment |
| Literary | 0.15 | Economy, literary quality, poem integrity, sensory presence, read-aloud flow, diction discipline |
| Safety | 0.20 | No unresolved deterministic failures or engine error |
| Provenance | 0.10 | Scripture provenance is present and accepted by the existing provenance gate |

The default aggregate release threshold is `0.85`. Truth, alignment, safety, and provenance each have a default hard floor of `0.80`. Literary quality contributes to the aggregate but is not a separate hard floor, preserving warranted aesthetic freedom.

A run that previously reached `DONE` is downgraded to `ESCALATED` when the objective gate fails.

## Uncertainty contract

Real production grounders must return an `uncertainty_register`. Deterministic mock fixtures remain backward compatible and do not receive additional payload fields.

Each uncertainty record contains:

```python
{
    "field": "christological_fulfillment",
    "claim": "Christ bears false accusation and rises beyond its verdict.",
    "status": "strong_inference",
    "evidence_ids": [],
    "source_refs": ["1 Peter 2:22-24"],
    "rationale": "Canonical support is explicit, while the relation to this psalm is thematic."
}
```

Allowed statuses are:

- `verified`
- `strong_inference`
- `reasonable_inference`
- `speculative`
- `unsupported`

The protected claims are:

- `governing_claim`
- `textual_hinge`
- `divine_action`
- `christological_fulfillment`

A protected claim cannot advance as speculative or unsupported. Every record must cite grounding evidence IDs or external source references. Unknown evidence IDs fail closed.

## Replanning boundary

The route controller applies one rule:

> Repair only the failed checkpoint and dependent fields. Preserve previously validated evidence, blueprint decisions, and unaffected artistic choices.

This is the equivalent of route recalculation. It prevents a local poem, application, or wording failure from silently replacing the established interpretation.

## Context outputs

After a run, `EngineContext` exposes:

- `navigation_state`
- `checkpoint_log`
- `uncertainty_register`
- `objective_scores`

`objective_scores` includes the five component scores and the aggregate score. The checkpoint log is JSON-compatible and suitable for audit storage.

## Configuration

```python
EngineConfig(
    enforce_navigation_control=True,
    navigation_require_uncertainty_register=True,
    navigation_min_objective_score=0.85,
    navigation_hard_floor=0.80,
    navigation_objective_weights={
        "truth": 0.35,
        "alignment": 0.20,
        "literary": 0.15,
        "safety": 0.20,
        "provenance": 0.10,
    },
)
```

The weights are normalized at runtime. Zero or negative total weight falls back to the default objective function.

## Limits

The controller makes process state, evidence, uncertainty, and release criteria inspectable. It does not make disputed interpretation objectively singular. Human theological, literary, rights, and publication review remain required.
