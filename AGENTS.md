# Codex instructions

## Governing architecture

Plan the work's state before generating its surface.

Blueprint preserves coherence. Script performs beauty. Harness validates alignment. Evaluator protects truth.

## Six governing laws

1. **Source Truth** — Claims, scenes, images, and conclusions may not outrun Scripture, evidence, or the established story world.
2. **Reality and Genre Fidelity** — Preserve ordinary causality unless Scripture records a miracle or a fictional premise declares another physics. Preserve the literary mode.
3. **Continuity** — Maintain theological, factual, character, world, argument, and series state.
4. **Revelatory Pacing** — Let understanding arrive in the order warranted by the text, scene, or argument. Do not explain the answer before the reader encounters the pressure.
5. **Human Truth** — Earn emotion through perception, action, consequence, memory, desire, and embodied fact.
6. **Protected Aesthetic Freedom** — Permit cadence, structure, image, and narrative variation within truth, continuity, rights, and safety boundaries.

## Profile isolation

Load only the rules and maps required for the selected mode.

### Devotional

- Preserve historical Israel and the passage's original covenant and literary setting.
- Ordinary physics governs unless Scripture explicitly presents miracle, vision, prophecy, or apocalyptic imagery.
- Explicit New Testament quotation or interpretation outranks thematic echoes.
- Follow the covenant movement through Israel's Messiah into the one household of believing Jews and Gentiles without replacement theology.
- Do not invent historical incidents, motives, weather, danger, deprivation, or emotion.
- Canonical development must arise from Scripture rather than resemblance alone.

### Fiction

- Preserve declared world physics, character knowledge, desire, point of view, chronology, and causal consequence.
- Do not solve scene tension by introducing unplanned facts or abilities.
- Update the continuity ledger after approved changes.

### Nonfiction

- Trace each material claim to evidence.
- Separate fact, inference, opinion, and uncertainty.
- Never fabricate sources, quotations, data, or consensus.
- Preserve the argument map through revision.

## Rule lifecycle

Do not convert every correction into a global rule.

1. **Local constraint** — applies to one passage, scene, chapter, or document.
2. **Candidate principle** — tested across multiple relevant works.
3. **Profile rule** — broadly necessary within one mode.
4. **Governing law** — necessary across all modes.

Unknown candidate rules must remain local. Consolidate overlapping rules rather than accumulating synonyms.

## Invariants

- Preserve deterministic mock behavior and regression coverage.
- Script generation begins only after the relevant planning packet or blueprint passes validation.
- Repairs target the failing component unless a finding requires global regeneration.
- The engine remains provider-independent and fail-closed.
- Source, evidence, canonical anchors, approved world state, and approved claims are immutable during smoothing.
- Protect Scripture, common doctrine, facts, and public-domain influence while rejecting distinctive unattributed overlap and imitation of living authors.

## Commands

```bash
python -m pip install -e '.[test]'
python -m pytest
python -m compileall -q devotional_engine examples
```

## Workflow

Work on a feature branch. Keep changes reviewable. Document architectural effects. Run tests before opening a pull request against `main`.
