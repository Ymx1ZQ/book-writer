# Book Revise — Prose Fix Executor

Apply pending smell-test (SMELL.md), editorial (REVIEW.md), and proofreading (PROOFREAD.md) fixes to written chapter prose. Does NOT touch project architecture — for that, use `/book fix`.

**Framing — read first.** Treat each finding as a critique from an outside editor reading cold. Evaluate it on merit; accept or reject calmly; if rejecting, record the rationale in the entry's `Status:` line so the rejection is visible to future passes. The goal is the best manuscript, not preserving a draft choice or defending a prior decision — regardless of who authored the finding (past you, the writer-side review pass, an external reviewer). Findings are signal, not competition.

**Routing context:** SMELL.md may contain entries written by `sniff`, `coherence`, `continuity`, `factcheck`, `motif`, `sensitivity`, `readability`, OR `adjacency` (each tags its origin via a `Source:` field). All route prose-target findings to SMELL.md per `world/canon-hierarchy.md` two-channel routing; revise consumes them uniformly. **Note (`adjacency`):** revise applies only adjacency's SMELL.md micro-fixes (idiolect reword, one-line POV-clean irony bridge, targeted compression); its *structural* findings live in `DEVPLAN.md` / `SMELL-PENDING.md` for the user and are NOT auto-applied here. Canon-side findings from those sources go to `DEVPLAN.md` and are applied by `/book fix` upstream — by the time revise runs, ANCHOR-NEEDED entries should already be resolved.

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
Parse all entries. Each carries TWO independent classifications (Phase 9 M2):
- `Routing:` field — one of `INLINE`, `ANCHOR-NEEDED`, `ACCEPT` (which channel applies the fix)
- `Flagging:` field — one of `SAFE-CUT`, `TRADE-OFF`, `SAFE-KEEP` (whether to apply at all)

Each entry may also include a `Source:` field naming the detection skill that wrote it (the sources listed under **Routing context**); processing is uniform regardless of source.

`factcheck` may also emit a `Flagging: VERIFY` value (a claim the agent could not confirm). Treat `VERIFY` exactly like `TRADE-OFF`: **never auto-apply** — surface to `chapters/<book>/SMELL-PENDING.md` with `Status: pending — verification required` so a human/web check resolves it. `readability` entries carry an extra `Register:` field (`default` / `intended-heavy`); only `default`-register INLINE×SAFE-CUT entries auto-apply (an `intended-heavy` entry should already be SAFE-KEEP).

Apply rules:
- **INLINE × SAFE-CUT** — process like editorial SAFE-CUT (look for `Suggested action`, apply, mark Fixed).
- **INLINE × TRADE-OFF** — **DO NOT auto-apply** (Phase 9 M3). Surface to `chapters/<book>/SMELL-PENDING.md` with `Status: pending — decision required`. Resolved by `/book arbiter` in the orchestrated pipeline; left for the user when `/book revise` is run standalone (see the PENDING template below).
- **INLINE × SAFE-KEEP** — note in revise summary as "acknowledged, no action"; mark in SMELL.md as `Status: ✓ Acknowledged (SAFE-KEEP)`.
- **ANCHOR-NEEDED × SAFE-CUT or TRADE-OFF** — resolved upstream by `/book fix`. If revise finds entry without `Status:` line, mark `Status: ⚠️ Unresolved upstream` and skip. If marked `Status: ✅ Resolved upstream by /book fix`, skip silently. Any cascade lives in a paired INLINE entry — process that.
- **ANCHOR-NEEDED × SAFE-KEEP** — rare; treat as ACCEPT.
- **ACCEPT** (any flagging) — noted, no action.

Backwards compatibility: if an entry has `Classification:` (legacy single field) but no separate `Routing:` and `Flagging:`, interpret `Classification:` as `Routing:` and default `Flagging:` to `SAFE-CUT`. Phase-9-onwards sniff/coherence/continuity write the two-field form.

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

- **Cut** — Delete the quoted passage; read the surrounding lines to confirm the prose still flows. If the deletion creates an awkward transition, smooth the join (add NOTHING thematic — only conjunctions, paragraph breaks, or minor rewordings of the adjacent sentence).
- **Rewrite** — Replace the quoted passage with the suggested alternative. If the fix says "consider" or "e.g.", choose the best option and apply it. Stay within the POV character's vocabulary register (check `characters/notes/voice-samples.md`).
- **Add** — Insert the specified content at the indicated location. Read the full context before and after to ensure the addition fits.
- **Restructure** — Larger changes (moving sections, breaking apart scenes). Read the full scene before and after, then apply.
- **Reduce frequency** — For cross-chapter items (e.g., "max 1 per chapter"). Read ALL affected chapters, identify every occurrence, keep the strongest one per chapter, vary or cut the rest.
- **Evolve the motif** — For cross-chapter pattern items. The fix specifies how to change the pattern in later chapters. Apply the variation while preserving the motif's function.

#### Step C — Verify the Fix

After applying, verify:

1. **The original problem is gone.** Grep for the old text — it should not appear.
2. **Word count still meets minimum.** If a cut dropped the chapter below minimum, flag it: `⚠️ Ch. N now at XXXX words (below minimum). Will be recovered in Step 5.` Do not expand inline (it would interleave with the fix queue and risk introducing fixes whose target text has just shifted) — Step 5 (Word Count Recovery) collects all flagged chapters at session end and applies dialogue-only expansion. Auto-recovery is the standard path; never defer to a future writing session.
3. **The surrounding prose flows.** Read 5 lines before and 5 lines after the edit. Fix orphaned transitions, dangling references, or broken paragraphs.
4. **No new violations introduced.** The fix must not create new show/tell violations, break character voice registers, or introduce tic-caption errors.

#### Step D — Propagate to State

Check if the fix affects anything tracked in `chapters/<book>/state.md`:
- **Character positions** — where a character is at chapter end
- **Plot progress** — what happened in the chapter
- **Micro-details planted** — a planted detail removed or changed
- **Tic introductions** — how a tic is introduced
- **Open threads** — a narrative thread opened or closed

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
**Decisions awaiting resolution:** N

**Who resolves these:** in the orchestrated/merge pipeline these `*-PENDING.md`
entries are resolved autonomously by `/book arbiter` (Phase 42 — APPLY or
ACCEPT-keep, no human-in-the-loop). When `/book revise` is run standalone
(bare linear flow, no arbiter step), they are left for the user, who for each
entry below reviews the proposed fix, weighs Loss vs Gain, and either:
(a) applies the fix to prose manually, OR
(b) updates Status to `✓ Accepted (defer)` to keep current text, OR
(c) updates Status to `✅ Fixed (manual)` after applying it yourself.

Items with no Status update by next cycle are re-emitted unchanged.

---

## #N — <one-line summary>
[verbatim copy of the SMELL.md entry, including Routing, Flagging,
Improvement, Loss, Voice-floor, Suggested action]

**Status:** pending — manual decision required
```

**`chapters/<book>/REVIEW-PENDING.md`** — same structure, for REVIEW TRADE-OFF entries (the `## Trade-Off Decisions Pending` section content from REVIEW.md).

**Persistence rule:** if `*-PENDING.md` from a prior cycle exists, read it. Entries marked with a final Status (`✓ Accepted (defer)` or `✅ Fixed (manual)`) are dropped from the new pending file. Entries still `pending — manual decision required` are re-emitted alongside any new TRADE-OFFs from this cycle. The pending file accumulates user-decided history across cycles, never clears silently.

**Pre-step archive (Phase 9 M4):** if `*-PENDING.md` exists, rename it to `chapters/<book>/archive/SMELL-PENDING-<YYYYMMDD-HHMMSS>-<chapter>.md` (or REVIEW-PENDING) before writing the merged version. Forensic history of what was decided when.

### 5.7. Invalidate the reader-state snapshots

Run this once, at session end, after every prose edit of the session is known. Do not run it per fix: the set of snapshots to stamp is fixed by the lowest-numbered chapter this session edited, and that is not settled until the last fix lands.

Reader-state snapshots live at `chapters/coldread-state/<book>-chNN.md`. They are derived from chapter prose, and `/book coldread-enum` reads them as its only model of what the reader remembers entering the next chapter. Once a chapter's prose changes, its snapshot describes text that is no longer there, while keeping the same filename and structure as a current one.

Reader-state is cumulative: the snapshot for chapter N carries what the reader retained from chapters 1 through N, so an edit to chapter N invalidates it and every later snapshot in the same book.

Take the lowest-numbered chapter whose prose this session edited. Stamp its snapshot and the snapshot of every later chapter in that book that has one. Insert the stamp immediately after the snapshot's H1 line. If a stamp from an earlier session is already sitting there, replace it — each file carries one stamp line, never a stack of them.

```
> **STALE — do not consume.** Invalidated YYYY-MM-DD by a prose edit to chNN (`/book revise <book>`). Reader-state is cumulative, so an edit at chapter N invalidates chapter N's snapshot and every later one in the book. Regenerate ascending with `/book snapshot <book> chNN` before any gate reads this file.
```

Fill the three placeholders per file: `YYYY-MM-DD` is today's date; the first `chNN` is the edited chapter that invalidated this snapshot (the lowest chapter this session edited at or below this snapshot's own chapter); the `chNN` in the last sentence is this snapshot's own chapter, so the command as written regenerates this file. "Ascending" means run the stamped chapters in increasing order, because each snapshot is built on the one below it.

If the session applied no prose edits — every finding surfaced as TRADE-OFF, acknowledged as SAFE-KEEP, or deferred — stamp nothing.

**Do not regenerate the snapshots here.** Regeneration costs one `/book snapshot` run per chapter from the edited chapter to the last drafted one, each reading a full chapter, and the runs are serial because each snapshot depends on the one below it. How much of the book to rebuild, and when, is the operator's call, made with the rest of the pass in view. Revise records the invalidation and names the command; it does not spend that cost on its own.

### 5.8. Re-point the line citations the edits moved

Run this once, at session end, after every prose edit is applied and **before the commit**. The script compares the working tree against `HEAD`, so a committed edit is invisible to it.

```bash
python3 <skill>/scripts/remap_citations.py <repo-root> chapters/<book>/chNN.md [more chapter files...]
```

The corpus cites prose by line number, and those citations are load-bearing: a later pass follows one to check that a canon claim is still true against the text. An insertion silently invalidates every citation below it in the same file — the stale citation still points at a real line, which now says something else, so the pass that follows it either verifies the wrong text or writes a second false claim on top of the first.

Measured on the ground-truth corpus, 2026-07-26: one revise pass inserted seven lines at `ch07.md:39-45`; a later pass re-verified the five deviation-ledger entries it was told to check and found four carried a wrong line, and the same shift had already propagated into two canon files and an outline. The corpus holds 140 live prose citations, only 11% of which quote the text they cite, and none of the shifted ones pointed past end of file — so neither a quotation check nor a bounds check would have caught any of it. The only component that knows the shift is the one that caused it: this step.

What the script does and does not touch:

- It rewrites citations in files that assert current truth — canon, outlines, character files, plot files, writing-notes, state.
- It leaves **historical records** alone: `archive/`, `SMELL*`, `PROOFREAD*`, `REVIEW*`, `COLDREAD*`, `DEVPLAN.md` and `outline-deviation.md`. A SMELL entry cites the line it actually examined on its own date, and the deviation ledger is append-only by its own rule — a stale citation there is corrected by a dated append, never by editing the ratified text.
- A citation whose target line was **rewritten or deleted** has no counterpart, so the script reports it and exits 1 rather than picking the nearest surviving line. Resolve each by reading the new text; a plausible-looking number is worse than a reported one, because it looks verified.
- A bare `chNN.md:LINE` names no book. While one book is drafted the reference is unambiguous; once the same chapter number is drafted in two books the script reports the ambiguity instead of guessing.

Exit 1 means at least one citation needs a decision. Do not commit past it without resolving them.

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
Reader-state snapshots stamped STALE: N — [chapter list, e.g. ch04-ch09]
  Regenerate ascending with /book snapshot <book> chNN before the next
  /book coldread-enum, which refuses to run on a stale snapshot.

Remaining: X items
Next: [what to do if items remain — typically "triage ANCHOR-NEEDED into project
       DEVPLAN, then re-run /book sniff after the worldbuilding lands"]
```

### 7. Graph Refresh (post-commit)

If `graphify-out/graph.json` exists in the project root, refresh the knowledge graph after this session's commit lands — chapter prose and `state.md` edits are graph-covered sources. Follow `instructions/graph-recall.md` §Keeping the graph fresh (incremental update; >25-changed-file skip bound; soft-fail — a failed refresh never fails the session). Graph absent → skip silently.

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
