# Chapter-Shaped Corporate Prayer

The devotional prayer is not a generic closing paragraph with biblical words added afterward. It is a concise first-person-plural transformation of the chapter's own movement.

The governing rule is:

> Convert the chapter's movement into first-person-plural prayer, preserving its order, emphasis, responsibility, canonical resolution, and emotional destination.

## Planning contract

Production planners must provide `prayer_design` with:

- `mode: chapter_shaped_corporate`;
- `voice: first_person_plural`;
- an approved opening address: `Our Father`, `Father`, or `Abba Father`;
- a divine identity grounded in textual evidence;
- at least three ordered prayer movements;
- a human-response movement as well as petitions for divine action;
- a Christological resolution when the grounding packet validates a canonical pathway;
- a concise word target, normally 90 to 150 words.

Each movement contains:

```python
{
    "function": "dependence",
    "chapter_position": 3,
    "chapter_action": "God goes before and daily bears His people.",
    "prayer_transformation": "Go before us, provide for us, and bear us up day by day.",
    "evidence_ids": ["E3"],
    "source_refs": [],
}
```

`chapter_position` values must increase strictly so the prayer follows the chapter's rhetorical or narrative order rather than collecting themes arbitrarily.

## Supported functions

- `adoration`
- `confession`
- `lament`
- `intercession`
- `petition`
- `dependence`
- `human_response`
- `christological_resolution`
- `assurance`
- `submission`
- `thanksgiving`
- `doxology`

The final movement must reach the chapter's own destination. Depending on the chapter, that may be lament, assurance, submission, thanksgiving, Christological resolution, or doxology.

## Composer standard

The composer must:

1. begin with the approved address;
2. pray predominantly in `we`, `us`, and `our` language;
3. transform the major chapter actions into petitions, confession, praise, or response in the supplied order;
4. preserve both God's sovereign action and the worshiper's faithful responsibility;
5. include Christ only through the validated canonical pathway;
6. end at the chapter's own theological and emotional destination;
7. close with `Amen`.

The composer must not add generic petitions that could move unchanged to another chapter.

## Deterministic draft audit

The production adapter checks that the prayer:

- begins with an approved address followed by a comma;
- remains predominantly first-person plural;
- stays within the approved word range;
- ends with `Amen`.

These findings are supplied to the integrated reviewer and route a failing prayer to targeted revision without reopening approved grounding, prose, or poetry.

## Review dimension

Production reviewers score `chapter_shaped_prayer` from zero to ten. A passing prayer must be chapter-specific, ordered, corporate, concise, canonically disciplined, and balanced between dependence and obedience.

A useful final test is:

> Could this prayer only have emerged from this chapter?

## Psalm 68 example

Psalm 68 moves from God arising and scattering evil, through His protection of the vulnerable and daily bearing of His people, into sanctuary praise, Christ's victorious ascent, and strength given to the nations.

A chapter-shaped prayer therefore follows that same movement rather than treating those themes as an unordered list.