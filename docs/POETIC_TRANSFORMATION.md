# Warranted Poetic Transformation

The engine distinguishes three different outcomes:

1. **Foreign imagery** imports a scene, object, event, actor, claim, or doctrine that the passage and its canonical warrant do not supply.
2. **Literal lineation** preserves the passage's nouns but does too little poetic work. It excerpts, catalogues, or breaks prose into lines without sufficient compression, music, tension, or discovery.
3. **Warranted poetic transformation** keeps the biblical world intact while shaping its language through legitimate poetic craft.

The governing rule is:

> Scripture supplies the world; poetry supplies the music.

## Positive poetic strategy

Real production planners must now provide:

```python
{
    "poetic_strategy": {
        "genre_force": "A processional hymn rising from conflict into praise.",
        "emotional_tone": "Triumphant without hardness; tender toward the vulnerable.",
        "formal_strategy": "Two common-meter stanzas with alternating rhyme.",
        "discovery": "The strength that scatters evil is the strength that carries the weak.",
    }
}
```

This is a positive literary contract. It asks what the poem should accomplish, not how many images or sensory details it should contain.

## Permitted operations

The planner may register any number of poetic transformations, including none. Supported operations are:

- `compression`
- `metrical_paraphrase`
- `bounded_implication`
- `personification`
- `contrast`
- `refrain`
- `canonical_echo`

Each registered transformation must identify:

- the proposed phrase;
- the poetic operation;
- the textual anchor;
- grounding evidence ids or canonical source references;
- a rationale explaining why the transformation deepens rather than replaces the text.

Example:

```python
{
    "phrase": "captives leave their chains",
    "operation": "bounded_implication",
    "textual_anchor": "He leads out the prisoners to prosperity.",
    "warrant_ids": ["E2"],
    "source_refs": [],
    "rationale": (
        "Chains are a conventional implication of captivity and intensify release "
        "without introducing a separate event."
    ),
}
```

The word *chains* need not occur in the psalm for the phrase to be faithful. Captivity warrants the implication. By contrast, an invented prison room, guard, weather condition, or escape sequence would create a new scene and exceed the warrant.

## Review boundary

Real production reviewers must score `poetic_transformation` from zero to ten.

A passing poem must:

- do more than excerpt or lineate the passage;
- preserve the passage's genre force and emotional temperature;
- use meter, rhyme, sound, repetition, compression, or implication with purpose;
- keep each nonliteral development inside its textual or canonical warrant;
- avoid importing a foreign imaginative world.

A low score routes the poem to targeted revision without reopening approved grounding, theology, or unaffected prose.

## Compatibility

`MockAgentAdapter` payloads remain unchanged. The new contract is enforced only for real production adapters.

Human literary and theological review remains necessary. The contract makes poetic judgment inspectable; it does not reduce poetry to a mechanical formula.
