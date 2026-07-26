# `/book coldread-enum` — paranoid defect cataloguer

Enumerate every place a reader at normal reading speed could stumble in a chapter. This is the **defect cataloguer** persona — paranoid, exhaustive, structural. NOT a reader-experience judgment ("does this chapter work?") — that framing was tried in the deprecated `/book coldread` and shown to catch only 0.5/19 of user-reported reader-stumble bugs on book-1 ch04 (Phase 40 M2). The enumeration framing catches 13-15/19 (Phase 40 M8 v2).

## Why this check exists

Standard quality checks (sniff/reviewer/proofread/coherence/continuity) read **with canon loaded**. They cannot answer "naive reader cannot follow." The deprecated `/book coldread` attempted naive-reader simulation via reader-experience persona, but the LLM (smart or dumb) reads too well — it silently resolves ambiguities a human stumbles on, then says "page-turn yes." Confirmed across smart Claude (Phase 40 M2) and deepseek-v4-flash (Phase 40 M7) — both produced essentially identical indulgent reading.

This skill flips the framing: instead of asking the agent to *read*, ask it to *enumerate defects* per explicit categories. LLMs are good at static analysis of text against criteria when told to be paranoid. The agent finds where a real reader could stumble by checking each sentence against the 10 categories below, with adversarial bias.

The skill is **canon-blind by design** (no `world/`, `characters/`, `plot/`, `outline.md` access — only the snapshot + chapter). This forces the simulation: if a fact isn't in the snapshot or chapter, the reader doesn't have it.

## Usage

```
/book coldread-enum <book> [chNN]
```

- `<book>` — chapter directory (e.g. `book-1`)
- `chNN` — optional; defaults to most recently modified `chapters/<book>/ch*.md`

## Inputs (the agent reads ONLY these)

1. **Reader-state snapshot for the prior chapter** at `chapters/coldread-state/<book>-ch(NN-1).md` — the compressed memory the reader carries forward. For ch01, no snapshot (true cold open).

   **Staleness check — read the snapshot's opening lines first, before the chapter.** If they carry `**STALE — do not consume.**`, STOP. Do not read the target chapter, do not enumerate, and do not write `COLDREAD.md` — not even a partial one. Report which snapshot is stale and the exact command that regenerates it (`/book snapshot <book> ch(NN-1)`, run ascending from the earliest stamped chapter), then exit. The stamp is written by `/book revise` when a prose edit invalidates the chapter a snapshot was built from; see `instructions/revise.md` §5.7. Enumerating against a stale snapshot yields findings about prose that no longer exists, in a `COLDREAD.md` that is indistinguishable from a valid one — `/book coldread-filter` triages those findings into SMELL.md and `/book revise` applies them. That is worse than producing no findings at all, which at least leaves the gap visible.

2. **Target chapter** at `chapters/<book>/chNN.md`.

**Do NOT read**: the prior chapter in full (the snapshot is the authoritative reader-memory model — prior chapter inline over-feeds the agent with detail a real reader wouldn't retain), `outline.md`, `world/`, `characters/`, `plot/`, prior `SMELL.md` / `REVIEW.md` / etc.

## Output

`chapters/<book>/COLDREAD.md` — list of enumerated findings, this format only:

```
## #N — [CATEGORY]
- LINE: line range
- QUOTE: "exact text"
- WHY: one sentence — why a reader could stumble here
```

NO verdict, NO summary, NO ranking, NO "page-turn yes" line. Just the catalog.

## The 10 categories

1. **AMBIGUOUS-PRONOUN** — A pronoun (he, she, it, they, this, that, "the X") where two or more reasonable referents exist in the prior 10 sentences of the chapter. Flag even if context resolves. **Sub-attend to POV-default suppression (TIGHT trigger — precision matters here):** flag the first `he/she` of a passage ONLY when the most recent SUBJECT (the actor of the immediately preceding sentences) is a DIFFERENT same-gender character than the POV — so the reader attaches the pronoun to that character, not the POV default. (Recovers the ch04 *"He had built the prototype" → reads as the father* bug: the prior subject was the father.) Do NOT fire merely because of a section break if the POV is already the active subject going into it (that was a false-positive source — ch03 L39, where Roe was the prior subject). The competing referent must be genuinely more salient/recent than the POV.

2. **UNSETUP-FACT** — A capability, system property, character trait, technology, or factual claim NOT established in the snapshot AND NOT established earlier in this chapter.

3. **UNGLOSSED-TERM** — An acronym, jargon term, brand name, technical term, or world-specific term used without an anchoring detail within 3 sentences AND not established in the snapshot.

4. **TONAL-SHIFT** — A sentence whose voice, syntax, formality, or register differs noticeably from surrounding paragraphs. Includes formal repetitions ("X was the X", "the Y kept its Y-ness") that feel like a different narrator briefly stepping in.

5. **SPATIAL-TEMPORAL-AMBIGUITY** — An action sequence where the reader cannot reconstruct: physical layout, time of day, sequence of events, which of two characters is performing the action, or whether something is body / object / tool. **Sub-attend to body-vs-tool ambiguity** — when "leg / arm / hand" could refer to a biological body part OR a mechanical apparatus, flag it. (This sub-attend was critical in M8 v2 — recovered the gambe-robot-vs-corpo bug.)

6. **UNBRIDGED-TRANSITION** — A scene break, section break, or new paragraph that doesn't orient the reader to: where we are, when we are, whose POV. Also: flashbacks that begin without sensory or temporal anchor.

7. **UNPREPARED-FORM** — A rhetorical pattern (refrain, parallel structure, repeated litany like "He had said. She had said. He had said.") appearing for the first time in the chapter without earlier setup that prepares the reader for that form.

8. **UNGROUNDED-IMPLICATION** — A sentence that seems to imply something important indirectly, but whose weight depends on information not stated in the chapter or in the snapshot.

9. **TEMPO-INTERRUPTION** — A passage of texture (bodily routine, environmental cataloguing, descriptive density) that breaks the emotional or causal momentum of the surrounding scene.

10. **UNEARNED-IMPORTANCE** — An object, person, or claim that the chapter treats as load-bearing without giving the reader a reason to feel its weight (and the snapshot does not provide that weight either).

> **Removed: a "cognition-without-object" category was tried (catch the *"He had known [what]"* shape) and pulled.** On a restraint-driven prose it fires on the book's entire signature surface (every `she knew` / `it meant` / `had known`), and the enum cannot separate *confusingly* cryptic from *deliberately* cryptic — that separation is the irreducibly human judgment (the "poetic-cryptic" LLM-blind class). It manufactured ~50 false flags per chapter and buried the one real instance. The cognition-cryptic class stays **human-judged** (user cold-read → SMELL), not enumerated.

## Paranoia constraint (the unlock)

Flag the finding **EVEN IF the surrounding context resolves the ambiguity**. A reader at speed does not always have time to resolve from context. Smart LLMs (you) tend to silently resolve ambiguities — fight that tendency. If a single sentence taken in isolation could parse two ways, flag it.

**Exception**: for UNSETUP-FACT and UNGLOSSED-TERM only, use the snapshot to dismiss false positives. If the snapshot establishes X, do NOT flag X as unsetup. All other categories: flag paranoiacally regardless of snapshot.

## Aim for 25-50 findings on a typical chapter

Better to overflag than underflag. The downstream `/book coldread-filter` will dismiss noise. Your job is recall, not precision.

## Do NOT

- Judge whether the chapter "works"
- Summarize the plot
- Rank findings by importance
- Give a verdict
- Skip findings because "the reader will figure it out"
- Output a "page-turn yes" or any other reader-experience verdict (this was the failure mode of the deprecated coldread)

## Output writing

Write the catalog to `chapters/<book>/COLDREAD.md` (overwrite any existing file at that path — that path now belongs to enum output, not the deprecated narrative coldread).

Then commit: `git add chapters/<book>/COLDREAD.md && git commit -m "book coldread-enum <book> <chapter>: N raw findings catalogued"`

**Important — commit hygiene**: use `git commit -- chapters/<book>/COLDREAD.md` (targeted) NOT `git add -A` (which would stage unrelated dirty files; see Phase 40 M7 incident).

## Design history (do not change without rereading Phase 40)

- Phase 40 M2: standard /book coldread on ch04 → 0.5/19 user-bug recall.
- Phase 40 M7: dumb deepseek-v4-flash same task → also 0.5/19 (model capability is not the lever).
- Phase 40 M8 v1: enumeration prompt without snapshot → 11/19 robust hits.
- Phase 40 M8 v2: enumeration prompt with snapshot + body-vs-tool sub-attend → 13/19 robust hits + 2 partial.
- 4 user bugs remain LLM-blind (all beat-craft category — Mariette/Mom naming, "she did not write" timing, boots-from-cold setup, mani-che-funzionavano poetic-cryptic). Accept user as canonical judge for those; handle via direct user feedback into SMELL.md (see Phase 41 M2 examples), not via this skill.
