# American Literary Pattern System

This subsystem gives the devotional engine a craft vocabulary drawn from American prose and poetry before 1950 without copying source text or imitating living/copyrighted voices.

## Copyright Boundary

As of 2026 in the United States, works published in 1930 have entered the public domain. Pre-1950 does not mean automatically usable. Works published from 1931 through 1950 are treated as restricted unless a future project provides rights metadata or a license.

The registry therefore separates:

- `public_domain_us=True`: enabled for craft-pattern guidance.
- `usage="licensed_reference_only"`: documented but blocked unless licensed.
- `usage="blocked_post_cutoff"`: unavailable to the pre-1950 system.

Reference checks used while creating this policy:

- Duke Center for the Study of the Public Domain: <https://web.law.duke.edu/cspd/publicdomainday/2026/>
- Cornell public-domain term chart: <https://guides.library.cornell.edu/copyright/publicdomain>

## What the System Stores

The engine does not store long passages. It stores pattern descriptors:

- rhetorical movement
- syntax habits
- image logic
- devotional use
- anti-pastiche warnings
- keyword signals

Example:

```python
{
    "mode": "compressed slant revelation",
    "movement": ["small aperture", "strange comparison", "dash turn", "aftershock"],
    "syntax": ["compressed lines", "slant rhyme", "syntactic fracture"],
    "avoid": ["cute obscurity", "random dashes"]
}
```

## Enabled Pattern Families

Prose patterns include:

- Jonathan Edwards: sermon pressure and holy dread
- Benjamin Franklin: plain moral accounting
- Edgar Allan Poe: enclosed dread
- Ralph Waldo Emerson: perception to spiritual turn
- Henry David Thoreau: stripped attention
- Frederick Douglass: witness to freedom
- Nathaniel Hawthorne: symbolic conscience
- Herman Melville: metaphysical pressure
- Mark Twain: vernacular moral awakening
- Stephen Crane: stark natural pressure
- Kate Chopin: interior awakening
- Willa Cather: memory landscape
- William Faulkner, 1930 only: polyphonic burden

Poetry patterns include:

- Walt Whitman: catalogic praise
- Emily Dickinson: compressed slant revelation
- Robert Frost, early public-domain works: plain image with late turn
- T. S. Eliot, 1930 editions only: modern fragment to prayer

Restricted examples are intentionally present so the engine can reject them rather than accidentally use them.

## How to Use

```python
from devotional_engine import build_style_brief, match_american_patterns

matches = match_american_patterns(["forsaken", "beasts", "death", "praise"])
brief = build_style_brief(matches)
```

Attach the result to `EngineContext.literary_style`. The deterministic harness checks it with `D21`.

`run_engine` also builds this brief automatically after commentary grounding and before art direction when `EngineConfig.enable_american_literary_patterns` is true.

The generated brief includes a `creative_mastery` layer distilled from editorial craft guidance:

- concrete, chapter-born images over abstract explanation
- form shaped by the chapter's movement
- emotional inevitability instead of cleverness
- image physics unless the chapter itself warrants miracle logic
- musical cadence, restrained surprise, and felt human truth

It intentionally excludes unsafe identity claims, "uncensored" modes, and direct imitation of named living authors.

## Anti-Pastiche Rule

The system should never write:

- "in the style of Mark Twain"
- author-labeled prose
- dialect imitation
- copied lines
- source-text collage

It should instead transform a chapter's movement through craft moves: pressure, turn, image discipline, cadence, and closure.
