# Book Fix — Coherence Fix Executor

Apply pending coherence fixes from `DEVPLAN.md` to project files (world/, characters/, plot/, outlines). Does NOT touch chapter prose — for that, use `/book revise`.

## Invocation

```
/book fix <book>    — coherence milestones affecting that book's files
/book fix all       — all coherence milestones (shared files first, then per-book)
/book fix common    — only milestones affecting shared files (world/, characters/, plot/)
```

---

## Process

### 0. Resolve Target

**If target is `common`:**
- Scan DEVPLAN.md for coherence milestones that affect ONLY shared files (`world/`, `characters/`, `plot/`). Exclude any milestone whose changes are limited to `chapters/<book>/`.
- Run Steps 1, 2, 3, 4 on those milestones only.

**If target is `all`:**
1. First, run the `common` flow above (shared-file coherence fixes).
2. Then, detect all books by scanning for `chapters/book-*/` directories.
3. For each book found (in natural order: book-1, book-2, book-3, ...):
   - Run the full per-book fix process below (Steps 1–4).
   - Announce the per-book session complete before moving to the next book.
4. After all books are processed, announce a combined summary.

**If target is a specific book (e.g., `book-1`):**
- Process milestones affecting `chapters/<book>/` plus any shared-file milestones not yet applied.

### 1. Scan for Pending Milestones

Read `DEVPLAN.md` from the bottom — the most recent phase is always appended at the end. Read the last 500 lines first; if the most recent phase with unchecked milestones is not found there, expand upward in 500-line increments. Do NOT read the full file from the top.

Scan for the most recent "Coherence Fixes" phase (or any phase with unchecked milestones). Parse all unchecked `- [ ]` items.

**Announce:**
```
📋 Book Fix — [scope]
Pending coherence milestones: X
Files affected: [list]

Processing in milestone order.
```

### 2. Apply Each Milestone

For each unchecked milestone:

#### Step A — Read Context
- Read every file mentioned in the milestone.
- Locate the exact section or text specified.
- If the target text is NOT found (already fixed, or content shifted): grep for nearby text, or announce "Target not found — may already be fixed" and skip.

#### Step B — Apply the Fix
Follow the milestone instruction exactly. Types:
- **Edit** — Change text in the specified file and section.
- **Add** — Insert content at the indicated location. Read surrounding context to ensure fit.
- **Move** — Relocate content between files. Verify both source (removed) and destination (added).
- **Delete** — Remove the specified content. Verify surrounding text still flows.
- **Cross-ref** — Replace restated content with a pointer to the canonical source.

#### Step C — Verify
1. **The original problem is gone.** Grep for the old text.
2. **The surrounding content flows.** Read 5 lines before and after.
3. **Cross-references point to existing targets.** If the fix added a `→ See [file] §[section]`, verify the target exists.

#### Step D — Mark Complete
Update DEVPLAN.md: `- [x] ... ✅`

Announce:
```
✅ Fixed: [brief description]
   File: [path]
   Remaining: X milestones
```

### 3. Session Complete

```
📋 Book Fix — [scope] — Complete

Applied: X/X milestones
Files modified: [list]
Remaining: X milestones
Next: [what to do if milestones remain]
```

**Combined summary** (for `all` and `common` modes):
```
📋 Book Fix — All — Combined Summary

Common (shared files):
  Milestones: X/X
  Files modified: [list]

Per-book:
  book-1: X/X milestones
  book-2: X/X milestones
  book-3: X/X milestones

Total remaining: X milestones
```

---

## Rules

- ❌ Never touch chapter prose (ch01.md, ch02.md, etc.) — that is `/book revise` territory.
- ❌ Never add thematic or narrative content. Fixes are surgery, not writing.
- ❌ Never mark an item `[x]` without actually applying the fix.
- ❌ Never rewrite MORE than the milestone specifies. Minimal changes only.
- ❌ Never embed milestone IDs in outline or project file text. Milestone tracking lives in DEVPLAN.md only.
- ❌ Never create standalone ⚠️ blocks, "Nolan constraint:" boxes, or "MANDATORY:" wrappers. Write constraints as single-sentence parentheticals.
- ✅ Grep for exact text before editing — content shifts as fixes accumulate.
- ✅ Process milestones in order (blocking → warning → note).
- ✅ If a fix would break continuity, flag it and skip rather than applying blindly.
- ✅ Verify cross-reference targets exist before replacing content with a pointer.
- ✅ **Word budget gate (per-milestone):** After applying any fix that adds content, run `wc -w <file>`. If over budget (see init.md template principles), compress or convert to cross-ref.
- ✅ **Per-milestone residue check:** After each milestone, verify: (a) no mechanism paragraphs >2 sentences added (→ cross-ref), (b) no authorial reasoning added outside writing-notes.md (→ move), (c) no inline `→ See` refs when footer section exists (→ move to footer), (d) no prose restating tracker content (→ delete).
- ✅ After applying a fix to an outline, remove all process language — no "Note:", "MANDATORY:", "drafting note:" wrappers.
- ✅ **Post-session auto-compact:** After all milestones, run compact Step 1A (milestone ID stripping) and Step 1E (density check) on all modified files.
