# `/book snapshot` — generate or update reader-state snapshot

Build or refresh the compressed reader-memory snapshot for a chapter. The snapshot models what a first-time reader retains entering the NEXT chapter — open loops, character investment, planted-but-unresolved threads, emotional/thematic throughline.

## Usage

```
/book snapshot <book> [chNN]
```

## Inputs

1. **Target chapter** at `chapters/<book>/chNN.md`
2. **Prior snapshot** at `chapters/coldread-state/<book>-ch(NN-1).md` (if exists; ch01 = cold open, no prior).

**Do NOT read**: `state.md` (authorial bookkeeping; includes what the reader does not yet know), `outline.md`, `world/`, `characters/`, `plot/`. The snapshot is **reader-side only**, built strictly from chapter texts.

## Output

`chapters/coldread-state/<book>-<chNN>.md` — the snapshot a reader carries entering ch(NN+1).

## Snapshot structure (4 blocks, sized like reader memory — strong retained beats, not a log)

```markdown
# Reader-state snapshot — end of Book N, Chapter NN

*Brief context paragraph: which POVs are active, which threads warm/cool.*

## Open loops

**[POV-name]'s thread ([warm/cool]):**
- Unresolved question 1
- Unresolved question 2

**Cross-thread:**
- Cross-cutting question

## Character investment

- **[Character name]** — what the reader knows; current investment level; situation

## Emotional / thematic throughline

- **[Theme]** — current state of reader's engagement

## Planted-but-unresolved

**[POV-name]'s thread:**
- Setup the reader has registered as load-bearing
```

## Discipline

- **Reader-side only**. Built strictly from chapter texts. Never seeded from `state.md`, `outline.md`, or any canon file.
- **It is a memory, not a transcript**. Resolved loops get closed and dropped. Minor texture decays. Only what a real reader would still be holding survives.
- **A snapshot that grows without bound is wrong**. Curate.
- **Continuity across books**: the snapshot chain is book-prefixed and continuous (`book-1-ch30` → `book-2-ch01` → ...). Reader memory does not reset between books.

## Invocation pattern

- After a chapter is finalized OR significantly revised, call `/book snapshot` to refresh the snapshot that the NEXT chapter's pipeline will consume.
- The pipeline (per Phase 41 M9 `run-merge-phase.sh` step 8.5e) calls this automatically after the cold-read enum/filter/revise cycle.
- Manual invocation: when a chapter is edited outside the pipeline (e.g. retroactive Phase 41 M10 patches), refresh the snapshot for that chapter so subsequent chapters' enum runs have accurate memory.

## Commit

`git commit -- chapters/coldread-state/<book>-<chNN>.md` — targeted, not `git add -A`.

## Design history

- Extracted from deprecated `/book coldread` (Phase 41 M7) where snapshot generation was a side effect of the 5-reads cold-reading.
- Now standalone so `/book coldread-enum` consumes a snapshot without re-doing the reading work, and snapshots can be refreshed independently after chapter edits.
