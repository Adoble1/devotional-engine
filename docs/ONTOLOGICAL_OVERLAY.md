# Ontological Overlay Contract

Version 6.9 adds a production-only overlay between the approved passage blueprint and composition.

The governing order is:

`Scripture and canonical warrant -> ontology -> affective path -> historical diction -> surface prose`

The overlay cannot create truth. It names the truth already established by grounding so the composer knows what exists, who acts, what relation has been broken, what God does, and what faithful restoration looks like.

## Purpose

Literary intensity weakens when emotion is detached from reality. The overlay gives emotional pressure an ontological cause:

- God is identified by the passage's own action and covenant relation.
- Human beings remain creatures, worshipers, sufferers, rebels, dependents, or recipients according to the text.
- Moral disorder is stated as a broken relation or false order, not as a floating feeling.
- Divine action supplies the actual turn.
- Application names the restored human posture.

Emotion must then arise from bodily, relational, or material evidence already warranted by the passage.

## Required production shape

```python
{
    "nodes": [
        {
            "id": "god",
            "kind": "divine",
            "name": "God",
            "truth": "The keeper who remembers and preserves",
            "warrant_ids": ["E2"],
        },
        {
            "id": "speaker",
            "kind": "human",
            "name": "the threatened singer",
            "truth": "A dependent creature who fears and learns trust",
            "warrant_ids": ["E1", "E2"],
        },
    ],
    "relations": [
        {
            "source": "god",
            "relation": "remembers and preserves",
            "target": "speaker",
            "warrant_ids": ["E2"],
        }
    ],
    "order": {
        "true_order": "God governs; the singer depends upon His word",
        "disorder": "Fear treats mortal threat as final authority",
        "divine_action": "God remembers, answers, and keeps",
        "restored_posture": "The singer trusts and walks before God",
    },
    "affective_path": {
        "pressure": "Fear closes around the singer",
        "embodied_evidence": ["tear", "wandering feet", "falling"],
        "turn": "God has counted every wandering",
        "settled_posture": "Trust walks forward in the light of life",
    },
    "diction": {
        "period_end_year": 1949,
        "source_document_ids": [
            "macdonald_unspoken_sermons_1867",
            "stevenson_vailima_prayers_1916",
        ],
        "selected_vocabulary": ["trust", "sorrow", "courage", "rest", "mercy"],
    },
}
```

Every node and relation must cite an evidence id from the grounding packet. Production planning fails closed if the overlay is absent, unwarranted, or incomplete.

## Public-domain diction register

The bundled register stores metadata, movement guidance, and single-word vocabulary atoms. It does not store source prose.

Approved sources are:

- John Bunyan, *The Pilgrim's Progress* (1678), Project Gutenberg eBook 131.
- George MacDonald, *Unspoken Sermons* (1867-1889), Project Gutenberg eBook 9057.
- Robert Louis Stevenson, *Prayers Written at Vailima* (1916 edition), Project Gutenberg eBook 616.
- Gerard Manley Hopkins, *Poems of Gerard Manley Hopkins* (1918 edition), Project Gutenberg eBook 22403.

The registry uses a conservative United States publication cutoff. As of 2026, works published in the United States before 1931 are in the U.S. public domain. Rights differ by jurisdiction, edition, translation, and later editorial matter, so publication review remains required outside that scope.

The source documents may guide:

- vocabulary atoms;
- emotional restraint;
- cadence pressure;
- concrete rather than therapeutic naming.

They may not supply:

- theological claims;
- historical claims;
- quotations;
- recognizable phrases;
- named-author pastiche;
- borrowed prayer language.

## Diction boundary

The devotional uses contemporary English grammar. The overlay rejects KJV surface forms such as `thee`, `thou`, `thy`, `hath`, `unto`, and related archaisms.

It also rejects conspicuously postwar therapeutic shorthand such as `inner child`, `safe space`, `self-care`, `trauma response`, and `nervous system regulation`. This does not deny the realities those phrases may describe. It requires the devotional to name fear, grief, shame, courage, mercy, weariness, hope, and bodily pressure in language compatible with the requested historical register.

## Review

Production review adds four scored dimensions:

1. `ontological_integrity`
2. `affective_truth`
3. `historical_diction`
4. `source_discipline`

A surface audit hard-blocks KJV language and the excluded postwar jargon. Absence of a selected period word at an emotional pressure point is advisory, since natural prose must not become a vocabulary checklist.

## Compatibility

`MockAgentAdapter` fixtures receive a fallback overlay and remain non-enforcing. Real adapters must provide the full overlay and review dimensions. The legacy devotional route is unchanged.
