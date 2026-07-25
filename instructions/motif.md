# `/book motif` — symbolic / motif coherence pass

Audit the chapter's recurring symbols and motifs against the project's own motif canon. Catch the one defect no other pass owns: a motif used **inverted**, **drifting**, or **arriving without its meaning** — the symbol that the reader's accumulated associations make *mean* something the prose did not intend.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Plant → payoff bookkeeping (is the planted gun fired?) | `coherence-check.md` §Chekhov |
| Motif *density* / device saturation (too much of a stylistic form) | `sniff.md` Category 10 |
| Plant density / re-read reward (craft) | `reviewer.md` §Reader Architecture |
| **"Does this motif still mean what it established? Is its evolution intentional? Does its payoff land?"** | **THIS check** |

Coherence tracks whether plants pay off; sniff tracks whether a *device* is overused; reviewer judges plant *density*. None of them tracks whether a motif's **semantic charge** is consistent — whether the moka pot that meant *home* in ch01 is accidentally inverted into *threat* in ch03 without the text earning the reversal, or whether the five-note motif's evolution (trill → bell → scratch) is deliberate and meaningful or just drift. That semantic-consistency gap is this check.

**Milestone format:** see `instructions/milestone-format.md`. Two-channel routing: prose-side misuse → `SMELL.md` (`Source: motif`, consumed by `/book revise`); canon-side drift (the motif tracker itself is wrong or under-specified) → a `DEVPLAN.md` phase for `/book fix`.

## Usage

```
/book motif <book> [chNN]
```

- `<book>` — book directory under `chapters/`.
- `chNN` — optional; defaults to the most recently written chapter.

## Output

- Prose findings → appended to `chapters/<book>/SMELL.md` (`Source: motif`).
- Canon findings → a new `## Phase <NN+1> — Motif canon fixes (<book> <chNN>)` in `DEVPLAN.md`.
- A mandatory **"Motif Coherence Audit"** section in SMELL.md (every tracked motif, its instances this chapter, and a verdict — always present).

## Step 0 — Load the motif canon

1. `plot/motif-tracking.md` — the canonical registry: each motif, its established meaning, intended evolution across books/chapters, and payoff plan. **This is the source of truth.** If it does not exist or is thin, that is itself a canon finding (route to DEVPLAN: "motif registry under-specified").
2. `plot/prestige-inventory.md` and any plant/payoff tracking — motifs that double as plants.
3. `world/` symbolic anchors if the project keeps them (objects/colors/sounds with assigned meaning).
4. Prior chapters' use of each motif (read the earlier `chapters/<book>/chNN.md` occurrences, or the snapshots in `chapters/coldread-state/`) to know the **accumulated** reader association entering this chapter.
   **Graph-fresh path (optional — see `instructions/graph-recall.md`):** if `graphify-out/graph.json` exists AND the freshness gate passes, bound this re-read: for each motif actually present in the target chapter, run `graphify query "<motif> established meaning, instances by chapter, intended evolution"` and `graphify path "<motif>" "<payoff-chapter>"`, then re-read from disk ONLY the prior-chapter §§ the graph cites (index mode — the disk text is the truth). Graph absent or stale → the unbounded prior-chapter re-read above stays the fallback.

Build, per motif: *established meaning*, *meaning the reader holds entering this chapter*, *intended state/evolution at this chapter* (per the tracker).

## The four motif-coherence categories

For each motif instance in the chapter:

1. **Inversion (BLOCKING-grade if unearned).** The instance carries a charge **opposite** to the established meaning, and the text does not earn the reversal. A symbol of safety used in a threatening beat reads, to a reader carrying the association, as either a mistake or an unsignaled irony. Earned reversal (the text deliberately turns the symbol, and signals the turn) is correct and is SAFE-KEEP — note it as intentional. Unearned inversion flags.

2. **Drift.** The motif's meaning has slid gradually from its established charge without an intentional evolution in the tracker. Each instance is individually plausible; across the chapter the symbol no longer means what it meant. Distinct from inversion (a single opposite use) — drift is cumulative erosion.

3. **Evolution mismatch.** The tracker specifies an intended evolution (e.g., the five-note motif should harden from *trill* → *scratch* by Book 2); the chapter either fails to evolve it (still the old form when it should have moved) or evolves it in a direction/at a pace the tracker did not intend. Route: if the prose is wrong → SMELL; if the *tracker* is the thing that should change (the chapter's evolution is better and canon should ratify it) → DEVPLAN.

4. **Payoff misalignment / unprepared payoff.** A motif's payoff beat fires but the setup instances in this (or prior) chapters did not prepare its specific charge, so the payoff lands flat or unearned; OR a setup instance is doing payoff-weight work too early, spending the charge before the planned payoff. Coordinate with coherence's Chekhov pass — this is the *semantic* complement (the gun is fired, but does the firing *mean* what the setups promised?).

## Flagging discipline

Same three-question test as sniff (Improvement / Loss / Voice-floor), with the **register/intent floor** being the motif tracker:

- **SAFE-CUT** (INLINE) — clear unearned inversion/drift, fix improves, no intentional irony lost. Auto-applied by revise.
- **TRADE-OFF** — the "misuse" may be deliberate irony or a defensible authorial turn; surface to `SMELL-PENDING.md`.
- **SAFE-KEEP** — the instance is consistent, or the reversal is earned and signaled, or the evolution matches the tracker. Note in Acknowledged; no action.

**Calibration (load-bearing).** Symbolism is interpretive; this check must be the *least* trigger-happy of the detectors. Default to SAFE-KEEP. Only flag when the misuse is something a careful reader holding the accumulated association would actually register as wrong — not every resonance you can construct. An ambiguous symbolic reading is SAFE-KEEP, never a flag. The cost of flattening a deliberate symbolic turn is high.

## Output — SMELL.md entries

Standard SMELL.md format with `Source: motif`:

```markdown
## #N — <one-line, e.g. "ch03: moka pot used as threat-image, inverts ch01 'home' charge, unsignaled">

- **Source:** motif
- **Location:** ch03.md line 142 (scene: kitchen confrontation)
- **Motif:** Moka pot (established meaning per motif-tracking.md §Domestic objects: hearth / home / the mother)
- **Quote:** "<the offending instance>"
- **Category:** 1 — Inversion (unearned)
- **Reader association entering ch03:** hearth/home (set ch01 l.12, reinforced ch02 l.88)
- **What the reader experiences:** The pot is framed as menacing here with no signaled turn; a reader carrying "home" reads it as a slip, not as irony, and the intended menace misfires into confusion.
- **Routing:** INLINE   (or: → DEVPLAN if the tracker itself should change)
- **Flagging:** SAFE-CUT | TRADE-OFF | SAFE-KEEP
- **Improvement (if fix applied):** Re-frame the menace through a different object, or add the one beat that earns the turn (the pot's meaning curdling).
- **Loss (if fix applied):** Minor — the menace can land elsewhere.
- **Suggested action:** <prose fix>, OR for canon: "ratify a deliberate inversion in motif-tracking.md §Moka pot — see DEVPLAN Phase NN M1."
```

### Motif Coherence Audit section (always present)

```markdown
## Motif Coherence Audit (Source: motif)

Motifs tracked (from motif-tracking.md): N.

| Motif | Established meaning | Instances this chapter | Reader assoc. entering | Verdict |
|---|---|---|---|---|
| Moka pot | hearth / home | l.142 | home | #N inversion flagged |
| Five-note signal | the Author's reach | l.30, l.205 | softening menace | evolves on-plan (SAFE-KEEP) |
| Cold-on-the-bones | mortality creeping | — | — | absent this chapter (OK) |

Instances flagged: A. Canon findings raised: B (→ DEVPLAN Phase NN). Intentional turns confirmed SAFE-KEEP: C.
```

## DEVPLAN milestone format (for canon findings)

When the *tracker* is wrong/under-specified (not the prose), append a phase exactly as sniff does for ANCHOR-NEEDED (see `sniff.md` §"DEVPLAN milestone format"), titled `## Phase <NN+1> — Motif canon fixes (<book> <chNN>) (<date>)`, one `- [ ]` milestone per canon finding, with Resolution + Cascade fields carrying the chosen value (autonomous decision per `instructions/milestone-format.md` — never escalate options to the user).

## Steps for the executing agent

1. Resolve the chapter file.
2. Step 0 — load the motif canon and build per-motif established/accumulated/intended meaning.
3. Read the chapter; for each motif instance, run the four categories + three-question test.
4. Append SMELL.md entries (`Source: motif`) + the Motif Coherence Audit section (do not overwrite SMELL.md — append, per `readability.md` Step 5 rule).
5. For canon findings, append the DEVPLAN phase.
6. Print: `motif: appended N entries to SMELL.md (A SAFE-CUT / B TRADE-OFF / C SAFE-KEEP); B canon findings → DEVPLAN Phase NN. Motifs audited: M.`

## Calibration

- **Least trigger-happy detector.** Symbolism is interpretive; default SAFE-KEEP.
- **Earned reversals are good.** A signaled turn of a symbol is craft, not a defect — confirm it SAFE-KEEP and say so in the audit.
- **The tracker is the truth.** Judge against `motif-tracking.md`, not against your own reading. If the tracker is silent on a motif, the finding is "registry under-specified" (canon → DEVPLAN), not a prose flag.
- **Coordinate with Chekhov.** Plant/payoff *existence* is coherence's; payoff *meaning* is yours. Don't duplicate the existence check.
