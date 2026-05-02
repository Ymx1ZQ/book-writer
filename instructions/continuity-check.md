# Book Continuity Check

Verify continuity between books before starting the next one. Run this AFTER completing Book N and BEFORE writing Book N+1.

**Routing doctrine:** every finding written by this skill is classified by its primary target file and routed to one of two channels per `world/canon-hierarchy.md`:

- Target in `world/`, `plot/`, `characters/`, `outline.md`, `state.md`, `voice-samples.md`, `flashback-beats.md`, `chorus-poem-map.md`, `sauveterre-plant.md`, `temporal-echoes.md`, character sheets → **DEVPLAN milestone** (consumed by `/book fix`).
- Target in `chapters/<book-N>/ch*.md` or `chapters/<book-N+1>/ch*.md` (chapter prose) → **per-chapter `chapters/<book>/SMELL.md` entry** (consumed by `/book revise`) using the same format `sniff.md` uses, with `Source: continuity` tag inside the entry.
- Findings that need both canon AND prose changes → **paired entries** in both channels.

## Invocation

```
/book continuity book-1 book-2
```

Arguments: `<completed-book>` `<next-book>` (e.g., `book-1 book-2` or `book-2 book-3`).

---

## Process

### 1. Load Files

**From completed book:**
- `chapters/<completed-book>/state.md` — the LAST "After Chapter XX" section (final state). This is the PRIMARY source for checks A, B, C, D, F, G — it captures character positions, open threads, ticking clocks, world state, tic introductions, and micro-details planted.
- `chapters/<completed-book>/outline.md` — load ONLY if `state.md`'s "Micro-details Planted" section is sparse for check E (plants). If loaded, use a targeted read focused on plant-tracking entries — do not load the full file.

**From next book:**
- `chapters/<next-book>/outline.md` — the full outline
- `plot/episode-N+1-*.md` — the plot file for the next book

**Shared reference:**
- `characters/notes/voice-samples.md` — vocabulary evolution ranges
- `characters/notes/flashback-beats.md` — which beats were used, which remain
- `plot/chorus-poem-map.md` — which appearances occurred, which are next
- `plot/sauveterre-plant.md` — plant/payoff status
- `world/temporal-echoes.md` — echo progression

### 2. Check Categories

#### A. Character Positions
- Where did we leave each character at the end of the completed book?
- Where does the next book's outline pick them up?
- **Any gap?** If a character was "in the Dome, alone, alarms screaming" at the end of Book 1, they must start Book 2 in a state consistent with that — not casually walking a corridor.

#### B. Open Threads
- List every open thread from the completed book's final state.
- For each: does the next book's outline address it? (Doesn't need to resolve it — but it can't ignore it.)
- Flag any thread that DISAPPEARS — introduced in Book N, absent from Book N+1's outline.

#### C. Ticking Clocks
- Which clocks were running at the end of the completed book?
- Are they picked up in the next book? With the correct elapsed time?
- Flag any clock that resets without explanation.

#### D. Vocabulary & Voice Evolution
Check `voice-samples.md` for each POV character:
- What vocabulary range was the character in at the end of the completed book?
- What range should they be in at the START of the next book?
- Example: Lena ends Book 1 in "First Cracks" (Ch. 9-15 range). Book 2 should start in "Rhapsode Contamination" or beyond. Flag if the next outline assumes she's still clinical.

#### E. Micro-details & Plants
- Which micro-details were planted in the completed book that should PAY OFF in the next?
- Are they present in the next book's outline?
- Which plants from `sauveterre-plant.md` and `chorus-poem-map.md` were placed? Which are next?
- Flag any plant that was placed but has no payoff scheduled.

#### F. Tic & Gesture Continuity
- Which tics were introduced (with caption) in the completed book?
- The next book MUST use them caption-free. Flag any outline beat that re-explains an introduced tic.
- Are there tics that should EVOLVE? (e.g., Check character sheets for tics that evolve (gain objects, change meaning). Ensure evolved versions appear in the next book.

#### G. World State
- What is the state of each level at the end of the completed book?
  - Dome: compliance status, surveillance level, political state
  - Ark: fugitive situation, Lydia's communication status
  - Reality: Noah's position, trail progress, allies status
- Does the next book's opening match?

### 3. Output — Report

Each finding is annotated with its routing destination — `[→ DEVPLAN]`, `[→ SMELL.md ch.NN]`, or `[→ paired]`.

```
## Continuity Check: [Book N] → [Book N+1]

### Character Positions
✅ [character] — consistent: [end state] → [start state]
⚠️ [character] — GAP: ended at [X], outline starts at [Y]. Fix: [suggestion] [→ routing]

### Open Threads
✅ [thread] — addressed in Ch. NN of next book
⚠️ [thread] — NOT FOUND in next book outline. Fix: [suggestion] [→ routing]

### Ticking Clocks
✅ [clock] — picked up in Ch. NN
⚠️ [clock] — MISSING. Fix: [suggestion] [→ routing]

### Vocabulary Evolution
✅ [character] — correct range transition
⚠️ [character] — range mismatch. Fix: [suggestion] [→ routing]

### Plants & Payoffs
✅ [plant] — payoff scheduled in Ch. NN
⚠️ [plant] — NO PAYOFF found. Fix: [suggestion] [→ routing]

### Tic Continuity
✅ All tics carry forward correctly
⚠️ [tic] — re-explained in Ch. NN (should be caption-free). Fix: remove caption. [→ SMELL.md ch.NN]

### World State
✅ Consistent
⚠️ [mismatch]. Fix: [suggestion] [→ routing]
```

**Routing examples:**
- "Character X ended Book 1 in state Y, but Book 2 outline opens in state Z" — outline change → DEVPLAN.
- "Tic re-explained in B2 ch.03 prose" — prose change → SMELL.md for ch.03.
- "Plant placed in B1 ch.12, payoff missing from B2 outline AND from B2 prose" — paired (DEVPLAN: add payoff to outline; SMELL.md ch.NN: write payoff into prose at the chosen chapter).

### 4. Write Corrections (if issues found)

Same pattern as `/book coherence`: route each correction by target file. Canon-side findings → append a Phase to `DEVPLAN.md` with milestones. Prose-side findings → append entries to the affected chapter's `chapters/<book>/SMELL.md` with `Source: continuity` tag. Cross-link to `world/canon-hierarchy.md` for tier-respecting decisions when canon files disagree.

### 5. Summary

```
Continuity Check Complete: [Book N] → [Book N+1]
Issues: X warnings (Y → DEVPLAN, Z → SMELL.md, W → paired)
All critical positions: [consistent / X gaps found]
Next step: /book fix book-N+1 (canon) → /book revise book-N+1 (prose) → /book fix book-N → /book revise book-N
```

---

## Rules

- ❌ Never let a character teleport between books without explanation
- ❌ Never let an open thread vanish silently
- ❌ Never assume the reader remembers details from the previous book — but the TEXT must be consistent with them
- ✅ Check every named character, every open thread, every planted detail
- ✅ The transition between books is where continuity breaks most often — be thorough
