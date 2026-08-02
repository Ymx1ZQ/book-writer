# `/book coldread-filter` — adversarial triage of enum findings into SMELL entries

Convert raw findings from `/book coldread-enum` into actionable SMELL.md entries that `/book revise` can consume — or dismiss them as noise with justification.

This is the validation layer between paranoid enumeration (high recall, low precision) and mechanical patch execution. It is allowed canon access (outline + chapter + enum findings) because it must judge routing and produce concrete Suggested actions, which require knowing intent.

## Usage

```
/book coldread-filter <book> [chNN]
```

## Inputs

**Graph-assisted triage (optional — gating in `instructions/graph-recall.md`, index mode).** This step is where canon knowledge belongs, and the division of labour with `coldread-enum` is the reason the pair works: **enum enumerates blind, filter triages informed.** Enum is forbidden the graph precisely so a fact the prose never established shows up as a stumble instead of being supplied from canon; this step then decides whether each stumble is a real gap or a reader who simply has not reached the setup yet. That decision is a corpus-wide lookup per finding — with forty findings, it is the whole cost of the step.

```bash
graphify query "where is <the fact the reader is missing> established across the corpus"
graphify query "<element> — which chapter introduces it, which pays it off"
```

**Index mode only.** A finding is dismissed as NOISE only after reading the file the query points at and confirming the setup is really there, in a chapter the reader has already passed. An empty query result is not evidence the setup is absent — it means read, not conclude. Graph absent or stale → triage on the file reads below, identically.

1. **Enum findings** at `chapters/<book>/COLDREAD.md` (output of `/book coldread-enum`)
2. **Chapter prose** at `chapters/<book>/chNN.md`
3. **Outline Ch.NN section** extracted from `chapters/<book>/outline.md` — find the `## Ch. NN` block to the next `## Ch.` block.

## Output

Appends entries to `chapters/<book>/SMELL.md` in standard sniff-compatible format. NOISE dismissals to a `## NOISE-Dismissed` section with justifications.

## Procedure

For each finding in COLDREAD.md, classify and process:

**Classification**:
- VALID — a real reader stumble; produce a SMELL entry
- NOISE — false positive; dismiss with one-sentence justification per rule 3 (never "the reader will figure it out" alone)
- ADJACENT — partial signal; either merge with a sibling VALID (note merge) or dismiss

**For VALID, produce SMELL entry** with these fields:

```
## #N — [short title]
- **Location:** chNN.md line range
- **Quote:** "exact text"
- **Category:** [enum category from finding] + severity hint (BLOCK / WEAKNESS / NOTE)
- **What the reader thinks:** 1-2 sentences from reader perspective
- **Routing:** INLINE / ANCHOR-NEEDED / ACCEPT
- **Flagging:** SAFE-CUT / TRADE-OFF / SAFE-KEEP
- **Voice-floor:** yes / no
- **Improvement (if fix applied):** what gets better (1 sentence)
- **Loss (if fix applied):** what's potentially lost (1 sentence)
- **Suggested action:** CONCRETE — executable by /book revise without further judgment
- **Status:** pending
```

## Conservative rules (mandatory)

1. **Voice-floor default = YES** for findings in categories TONAL-SHIFT, UNPREPARED-FORM, UNGROUNDED-IMPLICATION, UNEARNED-IMPORTANCE. These are voice-related; fixes risk damaging authorial voice; route to PENDING for `/book arbiter` — never to a human, per the pipeline contract below.

2. **SAFE-CUT eligibility**: only when ALL of:
   (a) the fix is purely additive (adds clarity, doesn't subtract voice content)
   (b) voice-floor = no
   (c) category is one of: AMBIGUOUS-PRONOUN (with unambiguous referent), UNGLOSSED-TERM (≤6 word anchor), UNSETUP-FACT (one anchoring sentence)
   Everything else → TRADE-OFF.

3. **Dismissal justification required**: for every NOISE classification, output ≥1 sentence explaining why a real reader at speed would NOT stumble. Must reference snapshot context, chapter context, outline intent, or genre convention.

4. **Adversarial bias**: when in doubt between VALID and NOISE → choose VALID. When in doubt between SAFE-CUT and TRADE-OFF → choose TRADE-OFF. When in doubt about voice-floor → choose yes.

5. **Suggested action must be executable by `/book revise` without further judgment**:
   - GOOD: "Change 'It boots from cold.' (line 229) to '[explicit new text]'"
   - GOOD: "Add anchoring phrase 'his phone agent' at first occurrence (approx line 247)"
   - BAD: "Make the moment clearer." / "Consider rephrasing."

## Output structure (write to chapters/<book>/SMELL.md, appending or replacing)

```
## Filter summary
- VALID: N
- NOISE: M
- ADJACENT-merged: K
- ADJACENT-dismissed: L

## Valid entries
[## #N — Title blocks, fields as above]

## NOISE-Dismissed
- Enum #X: [justification]
- Enum #Y: [justification]

## Adjacent merged
- Enum #A merged into Entry #B because [reason]
```

## Integration with /book revise

Output entries are SMELL-compatible. `/book revise <book> <chapter>` consumes pending entries:
- INLINE+SAFE-CUT → auto-apply
- INLINE+TRADE-OFF voice-floor=no → apply with logged tradeoff
- voice-floor=yes → routed to SMELL-PENDING.md, **then ALWAYS to `/book arbiter` next step** — never to a human
- ANCHOR-NEEDED → DEVPLAN milestone for `/book fix`
- ACCEPT/SAFE-KEEP → acknowledged

**Pipeline contract (Phase 42)**: no human-in-the-loop. PENDING entries are always resolved by `/book arbiter` autonomously (APPLY or ACCEPT-keep, never a third "defer to human" option). The voice-floor=yes flag signals a delicate call to the arbiter, not a request for human input. The arbiter must commit to a binary decision and document the rationale.

## Commit hygiene

Use `git commit -- chapters/<book>/SMELL.md` (targeted) NOT `git add -A`. See Phase 40 M7 incident for rationale.

## Design history

- Phase 41 M1-M3: filter prompt iterated against ch04 enum-v2 (94 findings) with user review gate. Conservative defaults derived from observed filter failures during M3 calibration.
- Voice-floor=yes default for 4 voice-related categories came from observation that voice-related fixes by `/book revise` risk damaging deliberate stylistic choices.
- Adversarial bias built in because filter is single-pass LLM; over-dismissal causes silent signal loss whereas over-keeping triggers user review (correctable).
