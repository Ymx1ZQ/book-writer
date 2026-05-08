# Book Revise — Prose Fix Executor

Apply pending smell-test (SMELL.md), editorial (REVIEW.md), and proofreading (PROOFREAD.md) fixes to written chapter prose. Does NOT touch project architecture — for that, use `/book fix`.

**Routing context:** SMELL.md may now contain entries written by `sniff`, `coherence`, OR `continuity` (each entry tags its origin via a `Source:` field). All three sources route prose-target findings to SMELL.md per `world/canon-hierarchy.md` two-channel routing. Revise consumes them uniformly. Canon-side findings from those same sources are routed to `DEVPLAN.md` and applied by `/book fix` upstream — by the time revise runs, ANCHOR-NEEDED entries should already be resolved upstream.

**Milestone format:** see `instructions/milestone-format.md`. `/book revise` parses only `- [ ]` items in REVIEW.md and PROOFREAD.md (and SMELL.md INLINE entries). Operational items in plain-bullet form are ignored.

## Invocation

```
/book revise <book>              — apply all pending prose fixes for that book
/book revise <book> sniff        — only SMELL.md INLINE fixes
/book revise <book> review       — only REVIEW.md fixes
/book revise <book> proofread    — only PROOFREAD.md fixes
/book revise all                 — apply all pending prose fixes for every book
```

---

## Process

### 1. Scan for Pending Fixes

Check three sources:

**A. SMELL.md** — `chapters/<book>/SMELL.md`
Parse all entries. Each entry now carries TWO independent classifications (Phase 9 M2):
- `Routing:` field — one of `INLINE`, `ANCHOR-NEEDED`, `ACCEPT` (which channel applies the fix)
- `Flagging:` field — one of `SAFE-CUT`, `TRADE-OFF`, `SAFE-KEEP` (whether to apply at all)

Each entry may also include a `Source:` field indicating which detection skill wrote it (`sniff`, `coherence`, `continuity`); processing is uniform regardless of source.

Apply rules:
- **INLINE × SAFE-CUT** — process like editorial SAFE-CUT (look for `Suggested action`, apply, mark Fixed).
- **INLINE × TRADE-OFF** — **DO NOT auto-apply** (Phase 9 M3). Surface to `chapters/<book>/SMELL-PENDING.md` with `Status: pending — manual decision required`. User reviews and applies (or marks `Status: ✓ Accepted (defer)`) manually before next cycle.
- **INLINE × SAFE-KEEP** — note in revise summary as "acknowledged, no action"; mark in SMELL.md as `Status: ✓ Acknowledged (SAFE-KEEP)`.
- **ANCHOR-NEEDED × SAFE-CUT or TRADE-OFF** — resolved upstream by `/book fix`. If revise finds entry without `Status:` line, mark `Status: ⚠️ Unresolved upstream` and skip. If marked `Status: ✅ Resolved upstream by /book fix`, skip silently. Any cascade lives in a paired INLINE entry — process that.
- **ANCHOR-NEEDED × SAFE-KEEP** — rare; treat as ACCEPT.
- **ACCEPT** (any flagging) — noted, no action.

For backwards compatibility: if an entry has `Classification:` (legacy single field) but no separate `Routing:` and `Flagging:`, interpret `Classification:` as `Routing:` and default `Flagging:` to `SAFE-CUT`. New entries written by Phase-9-onwards sniff/coherence/continuity use the two-field form.

**B. REVIEW.md** — `chapters/<book>/REVIEW.md`
Parse all unchecked `- [ ]` items in the Critical / High / Medium / Low / Cross-Chapter sections — these are editorial SAFE-CUT fixes. Then parse the `## Trade-Off Decisions Pending` section (Phase 9 M1) — these are NOT auto-applied; surface to `chapters/<book>/REVIEW-PENDING.md` for user decision. The `## Acknowledged (No Action)` section is informational.

**C. PROOFREAD.md** — `chapters/<book>/PROOFREAD.md`
Parse all unchecked `- [ ]` items. These are line-level mechanical fixes (grammar, spelling, punctuation, repetition); by definition SAFE-CUT.

**Announce:**
```
📋 Book Revise — [book]
Pending fixes:
  Smell-test (SMELL.md): Routing X INLINE / Y ANCHOR-NEEDED / Z ACCEPT
                         Flagging A SAFE-CUT / B TRADE-OFF / C SAFE-KEEP
    sources: a sniff / b coherence / c continuity
  Editorial (REVIEW.md): X SAFE-CUT items (C:X H:X M:X L:X CC:X) + Y TRADE-OFF items
  Proofreading (PROOFREAD.md): X items
  Total auto-applying: X
  Total surfaced to *-PENDING.md (manual decision): Y
```

If a filter was specified (sniff/review/proofread), only process that source. TRADE-OFF surfacing to *-PENDING.md applies regardless of filter.

### 2. Processing Order

**Smell-test INLINE fixes FIRST.** Plausibility gaffes invalidate downstream craft work — fixing "two euros sardines" before polishing the dialogue around it avoids wasted effort. Each INLINE entry contains a quote (the offending passage) and a `Suggested action` (the proposed rewrite). Apply per entry.

**Editorial fixes SECOND** (by severity: Critical → High → Medium → Low → Cross-Chapter) — these change prose: cutting, rewriting, restructuring sentences and scenes.

**Proofreading fixes LAST** — surface-level: grammar, spelling, punctuation. They operate on the final text.

### 3. Apply Each Fix

For each fix:

#### Step A — Read Context
- Read the chapter file mentioned in the fix.
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
2. **Word count still meets minimum.** If a cut dropped the chapter below the minimum word count, flag it: `⚠️ Ch. N now at XXXX words (below minimum). Will be recovered in Step 5.` Do not expand inline (it would interleave with the fix queue and risk introducing fixes whose target text has just shifted) — Step 5 (Word Count Recovery) collects all flagged chapters at session end and applies dialogue-only expansion. Auto-recovery is the standard path; never defer to a future writing session.
3. **The surrounding prose flows.** Read 5 lines before and 5 lines after the edit. Fix orphaned transitions, dangling references, or broken paragraphs.
4. **No new violations introduced.** The fix must not create new show/tell violations, break character voice registers, or introduce tic-caption errors.

#### Step D — Propagate to State

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
- SMELL.md: append `**Status:** ✅ Fixed (INLINE applied)` under the entry. ANCHOR-NEEDED entries get `**Status:** ⏸ Deferred to project DEVPLAN`. ACCEPT entries get `**Status:** ✓ Accepted (no action)`.
- REVIEW.md: `- [x] ... ✅ Fixed. [State updated: yes/no]`
- PROOFREAD.md: `- [x] ... ✅ Fixed.`

Announce:
```
✅ Fixed: [brief description] (source: [review/proofread])
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

### 5.5. Surface TRADE-OFF Entries to *-PENDING.md (Phase 9 M3)

Before session-complete summary, write user-facing decision surfaces for any TRADE-OFF entries collected from SMELL.md and REVIEW.md.

**`chapters/<book>/SMELL-PENDING.md`** — for SMELL TRADE-OFF entries:
```markdown
# SMELL — Trade-Off Decisions Pending

**Book:** <book>
**Chapter:** <chNN>
**Cycle ended:** YYYY-MM-DD
**Decisions awaiting user input:** N

For each entry below: review the proposed fix, weigh Loss vs Gain, and either:
(a) apply the fix to prose manually, OR
(b) update Status to `✓ Accepted (defer)` to keep current text, OR
(c) update Status to `✅ Fixed (manual)` after applying it yourself.

Items with no Status update by next cycle are re-emitted unchanged.

---

## #N — <one-line summary>
[verbatim copy of the SMELL.md entry, including Routing, Flagging,
Improvement, Loss, Voice-floor, Suggested action]

**Status:** pending — manual decision required
```

**`chapters/<book>/REVIEW-PENDING.md`** — same structure, for REVIEW TRADE-OFF entries (the `## Trade-Off Decisions Pending` section content from REVIEW.md).

**Persistence rule:** if `*-PENDING.md` from a prior cycle exists, read it. Entries marked with a final Status (`✓ Accepted (defer)` or `✅ Fixed (manual)`) are dropped from the new pending file. Entries still `pending — manual decision required` are re-emitted alongside any new TRADE-OFFs from this cycle. The pending file accumulates user-decided history across cycles, never clears silently.

**Pre-step archive (Phase 9 M4):** before writing the new `*-PENDING.md`, if the file exists, rename to `chapters/<book>/archive/SMELL-PENDING-<YYYYMMDD-HHMMSS>-<chapter>.md` (or REVIEW-PENDING) before writing the merged version. Forensic history of what was decided when.

### 6. Session Complete

```
📋 Book Revise — [book] — Complete

Applied (SAFE-CUT, auto-applied):
  Smell-test INLINE: X/X items
  Editorial: X/X items
  Proofreading: X/X items

Trade-Off decisions surfaced (NOT applied — see *-PENDING.md):
  Smell-test TRADE-OFF: X items → chapters/<book>/SMELL-PENDING.md
  Editorial TRADE-OFF: X items → chapters/<book>/REVIEW-PENDING.md

Acknowledged (SAFE-KEEP, no action):
  Smell-test SAFE-KEEP: X items
  Editorial SAFE-KEEP: X items

Deferred to project DEVPLAN (ANCHOR-NEEDED, NOT applied):
  [list each ANCHOR-NEEDED entry with its suggested DEVPLAN milestone language,
   so the user can paste them straight into the project's DEVPLAN.md]

Accepted (Routing: ACCEPT — no action):
  [list ACCEPT entries with the evidence that supported the deliberate choice]

Chapters modified: [list with word counts]
State propagated: [which chapters]

Remaining: X items
Next: [what to do if items remain — typically "triage ANCHOR-NEEDED into project
       DEVPLAN, then re-run /book sniff after the worldbuilding lands"]
```

---

## Rules

- ❌ Never touch project architecture files (world/, characters/, plot/) — that is `/book fix` territory.
- ❌ Never add thematic content while revising. Fixes are surgery, not writing.
- ❌ Never skip verification (word count + flow check) after each fix.
- ❌ Never apply proofreading before editorial — the text may change.
- ❌ Never mark an item `[x]` without actually applying the fix.
- ❌ Never rewrite MORE than the fix specifies. Minimal changes only.
- ✅ ANCHOR-NEEDED entries are resolved upstream by `/book fix` per `world/canon-hierarchy.md` two-channel routing. Revise consumes the paired INLINE entry that handles the prose cascade after the canon update; if no INLINE pair exists and the ANCHOR-NEEDED entry is unmarked, flag it as a stuck-issue candidate for the orchestration script.
- ✅ Grep for exact quotes before editing — line numbers shift as fixes accumulate.
- ✅ Process top-to-bottom within each source to minimize drift.
- ✅ If a fix references text changed by a prior fix, re-locate and adapt.
- ✅ If a fix would break continuity, flag it and skip rather than applying blindly.
- ✅ See `world/canon-hierarchy.md` for the routing doctrine that determines which findings reach SMELL.md vs DEVPLAN.
