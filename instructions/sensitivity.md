# `/book sensitivity` — representation / dated-language pass

A conservative, advisory-first read for the defect class no other pass owns: stereotype, caricature, dated or ableist language, and representation handled in a way that would read as careless or wrong to a member of the depicted group. This is **not** a content-politics filter and it does not soften the book's themes, darkness, or characters' ugliness — fiction depicts cruelty, bias, and flawed people on purpose.

## What this check is, and what it is NOT

| | |
|---|---|
| **IS** | Unintended stereotype in narration; caricature standing in for a real person; dated/ableist term used without authorial intent; a depicted group rendered only through cliché |
| **IS NOT** | A character holding bigoted views *on purpose* (that is characterization — SAFE-KEEP); dark/violent/transgressive content that is thematically intended; sanitizing voice or theme; policing what the book is allowed to be about |

The distinction is **diegetic intent**: a bigoted *character* is the book working; a stereotype in the *narrator's own framing*, unsignaled, is the defect. When unsure which it is, default to surfacing it as a TRADE-OFF for the human, never to silent edits.

**Milestone format:** see `instructions/milestone-format.md`. Findings route to `SMELL.md` (`Source: sensitivity`); almost all are **TRADE-OFF** (→ `SMELL-PENDING.md`, human decides).

## Usage

```
/book sensitivity <book> [chNN]
```

## Output

- Findings → `chapters/<book>/SMELL.md` (`Source: sensitivity`), advisory-first.
- A mandatory **"Sensitivity Audit"** section: groups depicted in the chapter + verdict.

## Step 0 — Load intent

**Graph-assisted intent lookup (optional — gating in `instructions/graph-recall.md`, index mode).** Two of the three questions below are corpus-wide, not chapter-local: is this depicted group represented with depth *elsewhere* in the book, and is this viewpoint marked as deliberately biased *anywhere* in its sheet. Answering them by reading means opening every character sheet. When the graph is available and fresh:

```bash
graphify query "<depicted group> — appearances and depth across characters/ and chapters/"
graphify query "<POV character> — narration bias, deliberate limitation, narrator boundaries"
```

**Index mode only: the results locate the sheets to open, they do not settle intent.** A thin depiction is only a finding after reading what the located files actually say — the difference between a slice of a well-drawn group and the whole of a flat one is a judgment the disk text has to support. Graph absent or stale → load as written below.

1. `characters/notes/narrator-boundaries.md` — per-POV narration constraints. A close-POV narrator inside a biased character's head *should* carry that bias; that is boundary-correct, not a finding.
2. The relevant `characters/` sheets — is a viewpoint deliberately bigoted, naive, or limited? Is a depicted group represented elsewhere with depth (so a thin appearance here is a slice, not the whole)?
3. `world/tones.md` and the outline beat — is the darkness/edge here intended?

A finding only fires where the issue sits in **narration the project does not mark as a character's deliberate viewpoint**.

## The four categories (all advisory)

1. **Stereotype in narration.** The narrator's own framing (not a character's line/thought) renders a group through cliché — a trait, accent, role, or motive that stands in for an individual. Flag the framing, not the topic.
2. **Caricature.** A character belonging to a marginalized or minority group exists only as a cliché — no interiority, present solely to embody a type. (If the project gives them depth elsewhere, note that and downgrade.)
3. **Dated / able"ist" language.** A word or idiom that is dated, slur-adjacent, or ableist, used in narration without the author signaling intent. Only the clearly-dated-with-clean-modern-equivalent case is SAFE-CUT; anything that might be a deliberate period or voice choice is TRADE-OFF.
4. **Representation thinness.** A group central to the scene is rendered only from the outside, through assumption, where the prose seems to *intend* depth but misses — surfaced as a gentle note for the author, never an auto-edit.

## Flagging discipline

- **SAFE-CUT** (INLINE) — reserved for unambiguous dated-term swaps with zero loss of meaning, tone, or character. Rare.
- **TRADE-OFF** (→ SMELL-PENDING.md) — the default for this entire check. The author decides; the agent surfaces with a clear, non-preachy rationale.
- **SAFE-KEEP** — diegetic intent (a character's deliberate viewpoint), boundary-correct close POV, or thematically intended darkness. Note in Acknowledged.

**Calibration (load-bearing).** This is the most conservative detector in the suite. Its job is to *inform the author*, not to sanitize the book. Over-firing here is corrosive — it makes the author distrust the whole pipeline and dulls the work. Surface only what a thoughtful editor would genuinely raise, framed as "you may want to know," and let the human judge. Never moralize in the entry.

## Output — SMELL.md entries

```markdown
## #N — <one-line, neutral, e.g. "ch02: market vendor rendered only through accent + haggling cliché">

- **Source:** sensitivity
- **Location:** ch02.md line 70
- **Group / topic:** <group>
- **Quote:** "..."
- **Category:** 2 — Caricature
- **Diegetic intent check:** narration (not a character's viewpoint per narrator-boundaries.md §<POV>); the vendor does not recur with depth elsewhere.
- **What a reader of that group might feel:** rendered as a type, not a person.
- **Routing:** INLINE
- **Flagging:** TRADE-OFF   (default) | SAFE-CUT (dated-term swap only) | SAFE-KEEP (if diegetic)
- **Improvement (if addressed):** one specifying detail gives the vendor interiority without changing the beat.
- **Loss (if addressed):** negligible — the beat survives.
- **Suggested action:** advisory — "consider one individuating detail"; for SAFE-KEEP, name the intent.
```

### Sensitivity Audit section (always present)

```markdown
## Sensitivity Audit (Source: sensitivity)

Groups / identities depicted this chapter: N.

| Group / topic | Rendered via | Diegetic intent? | Verdict |
|---|---|---|---|
| Marseille market vendor | accent + haggling | no (narration) | #N TRADE-OFF (caricature) |
| POV character's bias toward X | character's own thought | yes (boundary-correct) | SAFE-KEEP |

Findings surfaced: A (A-1 SAFE-CUT / rest TRADE-OFF). SAFE-KEEP (diegetic/intended): B.
```

## Steps for the executing agent

1. Resolve the chapter file. Step 0 — load narrator-boundaries + character sheets + tones to establish intent.
2. Read the chapter; for each depicted group/identity, run the four categories with the diegetic-intent gate.
3. Append SMELL.md entries (`Source: sensitivity`, append — do not overwrite) + the Sensitivity Audit section.
4. Print: `sensitivity: appended N entries to SMELL.md (A SAFE-CUT / B TRADE-OFF). Groups audited: G (D diegetic/SAFE-KEEP).`

## Calibration

- **Inform, do not sanitize.** Never auto-rewrite voice or theme.
- **Diegetic intent is the gate.** Only unsignaled *narration* flags.
- **TRADE-OFF by default.** Never silent-edit, never silent-pass.
- **No moralizing.** The rationale is editorial, specific, and neutral. The author decides.
