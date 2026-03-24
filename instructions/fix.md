# Book Fix — Unified Fix Executor

Apply ALL pending fixes from any source: editorial review (REVIEW.md), proofreading (PROOFREAD.md), and coherence fixes (DEVPLAN.md milestones).

## Invocation

```
/book fix <book>
/book fix <book> review       — only REVIEW.md fixes
/book fix <book> proofread    — only PROOFREAD.md fixes
/book fix <book> coherence    — only coherence-related milestones from DEVPLAN.md
```

---

## Process

### 1. Scan for Pending Fixes

Check three sources:

**A. REVIEW.md** — `chapters/<book>/REVIEW.md`
Parse all unchecked `- [ ]` items. These are editorial fixes (show/tell, voice, structure, pacing). Organized by severity: Critical > High > Medium > Low > Cross-Chapter.

**B. PROOFREAD.md** — `chapters/<book>/PROOFREAD.md`
Parse all unchecked `- [ ]` items. These are line-level fixes (grammar, spelling, punctuation, repetition). Organized by chapter.

**C. Coherence Devplan** — `DEVPLAN.md`
Find the most recent "Coherence Fixes" phase. Parse unchecked `- [ ]` milestones that affect files in `chapters/<book>/`, `world/`, `characters/`, or `plot/`.

**Announce:**
```
📋 Book Fix — [book]
Pending fixes:
  Coherence (DEVPLAN.md): X milestones
  Editorial (REVIEW.md): X items (C:X H:X M:X L:X CC:X)
  Proofreading (PROOFREAD.md): X items
  Total: X

Processing order: Coherence → Editorial → Proofreading
```

If a filter was specified, only process that source.

### 2. Processing Order

**Coherence fixes FIRST** — these may change structure, add beats, modify outlines. They can affect the text that editorial and proofreading fixes reference.

**Editorial fixes SECOND** (by severity: Critical → High → Medium → Low → Cross-Chapter) — these change prose: cutting, rewriting, restructuring sentences and scenes.

**Proofreading fixes LAST** — surface-level: grammar, spelling, punctuation. They operate on the final text.

### 3. Apply Each Fix

For each fix, regardless of source:

#### Step A — Read Context

- Read the file mentioned in the fix.
- Locate the exact quote or section specified.
- If the quote is NOT found (already fixed, or line numbers shifted): grep for nearby text, or announce "Quote not found — may already be fixed" and skip to verification.

#### Step B — Apply the Fix

Follow the fix instruction. Types:

- **Cut** — Delete the quoted passage. Read the surrounding lines to ensure the prose still flows after deletion. If removing a sentence creates an awkward transition, smooth the join (but add NOTHING thematic — only conjunctions, paragraph breaks, or minor rewordings of the adjacent sentence).
- **Rewrite** — Replace the quoted passage with the suggested alternative. If the fix says "consider" or "e.g.", choose the best option and apply it. Stay within the POV character's vocabulary register (check `characters/notes/voice-samples.md`).
- **Add** — Insert the specified content at the indicated location. Read the full context before and after to ensure the addition fits.
- **Restructure** — Larger changes (moving sections, breaking apart scenes). Read the full scene before and after, then apply.
- **Reduce frequency** — For cross-chapter items (e.g., "max 1 per chapter"). Read ALL affected chapters, identify every occurrence, keep the strongest one per chapter, vary or cut the rest.
- **Evolve the motif** — For cross-chapter pattern items. The fix specifies how to change the pattern in later chapters. Apply the variation while preserving the motif's function.

#### Step C — Verify the Fix

After applying, verify:

1. **The original problem is gone.** Grep for the old text — it should not appear.
2. **Word count still meets minimum** (if editing a chapter file). If a cut dropped the chapter below the minimum word count, flag it: `⚠️ Ch. N now at XXXX words (below minimum). Needs expansion.` Do NOT expand automatically — flag it for the next writing session.
3. **The surrounding prose flows.** Read 5 lines before and 5 lines after the edit. Fix orphaned transitions, dangling references, or broken paragraphs.
4. **No new violations introduced.** The fix must not create new show/tell violations, break character voice registers, or introduce tic-caption errors.

#### Step D — Propagate to State (if the fix changes chapter content)

Check if the fix affects anything tracked in `chapters/<book>/state.md`:
- **Character positions** — if a fix changes where a character is at chapter end
- **Plot progress** — if a fix changes what happened in the chapter
- **Micro-details planted** — if a fix removes or changes a planted detail
- **Tic introductions** — if a fix changes how a tic is introduced
- **Open threads** — if a fix closes or opens a narrative thread

If YES: update the corresponding "After Chapter N" section in state.md.
If NO: skip this step.

#### Step E — Mark Complete

Update the source file:
- REVIEW.md: `- [x] ... ✅ Fixed. [State updated: yes/no]`
- PROOFREAD.md: `- [x] ... ✅ Fixed.`
- DEVPLAN.md: `- [x] ... ✅`

Announce:
```
✅ Fixed: [brief description] (source: [review/proofread/coherence])
   File: [path]
   Word count: XXXX (OK / ⚠️ below minimum)
   State propagated: [yes/no]
   Remaining: X items
```

### 4. Handle Cross-Chapter Fixes

Cross-chapter fixes (from REVIEW.md "Cross-Chapter" section) affect multiple files:

1. Read ALL affected chapters listed in the fix.
2. Grep for every occurrence of the pattern across all chapters.
3. Apply the fix in each chapter, following the instruction (keep first occurrence, vary later ones, etc.).
4. Verify each affected chapter individually.
5. Mark complete with a note listing all files modified.

### 5. Word Count Recovery

If any chapter dropped below the minimum word count after cuts:

1. Collect all flagged chapters.
2. For each: identify the best location to add DIALOGUE (not description, not narration).
3. Add 1-3 dialogue exchanges that are character-appropriate and advance the scene.
4. Verify the chapter is back above minimum.

### 6. Session Complete

```
📋 Book Fix — Session Complete

Applied:
  Coherence: X/X milestones
  Editorial: X/X items
  Proofreading: X/X items

Chapters modified: [list with word counts]
State propagated: [which chapters]

Remaining: X items
Next: [what to do if items remain]
```

---

## Rules

- ❌ Never add thematic content while fixing. Fixes are surgery, not writing.
- ❌ Never skip verification (word count + flow check) after each fix.
- ❌ Never apply proofreading before editorial — the text may change.
- ❌ Never mark an item `[x]` without actually applying the fix.
- ❌ Never rewrite MORE than the fix specifies. Minimal changes only.
- ✅ Grep for exact quotes before editing — line numbers shift as fixes accumulate.
- ✅ Process top-to-bottom within each source to minimize drift.
- ✅ If a fix references text changed by a prior fix, re-locate and adapt.
- ✅ If a fix would break continuity, flag it and skip rather than applying blindly.
