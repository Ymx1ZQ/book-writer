# Book Writer

Orchestrate writing a book of the trilogy in batches of 5 chapters. Delegates all chapter-writing to the chapter-writer process.

## Invocation

```
/book write book-1
```

Argument: `<book>` (book-1, book-2, book-3).

---

## General Behavior

- **Pre-approved** within a batch. No confirmation between chapters.
- **Max 5 chapters per session.** Then STOP.
- Ambiguity → choose and proceed.
- Stop ONLY for unresolvable blocking errors.

---

## Session Start — Context Refresh (MANDATORY)

Before writing any chapter:

1. Read `chapters/<book>/DEVPLAN.md` — find the next uncompleted chapter
2. Read `chapters/<book>/state.md` — the ENTIRE most recent "After Chapter N" section
3. If chapters exist, read the last 2 written chapter files (style/voice continuity)
4. Read `world/writing-checklists.md`, `world/tones.md`, and `world/prose-rules.md` (full refresh)
5. **If this is the FIRST batch of the book** (Ch. 1-5): ALSO read `chapters/<book>/opening-strategy.md`. The first 3 chapters decide if the reader continues. The opening strategy defines emotional objectives, structural requirements, and explicit "what must NOT happen" rules for each opening chapter. This is MANDATORY for the first batch.
6. **If resuming from a previous session** (not the first batch): run Voice Calibration before writing:
   a. Read the BEST chapter from the previous batch (not the last — the best, identified by review score or word count).
   b. Read the voice samples for the POV character of the NEXT chapter to write.
   c. Write a 100-word voice test (NOT saved, just for calibration): a paragraph in the POV character's voice describing something mundane. If it sounds right, proceed. If not, re-read voice samples and try again.
   The risk between sessions is voice drift — characters start sounding alike. Calibration is the vaccine.

**Batch context note:** The files loaded in steps 2 and 4 above (`state.md`, `tones.md`, `prose-rules.md`, `writing-checklists.md`) remain in context for the entire batch. When chapter-writer runs for each chapter, it will skip re-reading these files (see its "Batch session optimization" note in Step 1). This saves ~4 file reads per chapter × 5 chapters = 20 redundant reads per batch.

---

## Chapter Loop

For each chapter in the batch:

### 1. Identify

Read `chapters/<book>/DEVPLAN.md`. Find the next `- [ ]` entry. Extract chapter number, title, level, POV.

### 2. Write the Chapter

**Follow the complete process defined in `/chapter-writer`:** Load context → Plan → Write → Word count gate → Verify (8 passes) → Update state → Mark complete.

All writing rules, verification passes, prose rules, and quality gates live in the chapter-writer skill. Do not duplicate them here — read and follow that process.

### 2b. Track Ending Types

After each chapter is complete, update the running ending type tracker. If J (contemplative) reaches 2, flag all subsequent plans that default to contemplative — they must choose F, G, H, or I instead.

### 3. Degradation Check (every 3 chapters)

After every 3rd chapter in the batch:

```bash
wc -w chapters/<book>/ch<LAST3>.md
```

If average < 2,500 (normal) or < 800 (rapid): **STOP.** Announce degradation. Review last chapter for compressed scenes. Rewrite before proceeding.

**Qualitative degradation check (ALSO every 3 chapters):**

Read the last 500 words of each of the 3 chapters just written. Check for:
- **Repeated phrases** across chapters (same sentence opener, same description, same emotional beat)
- **Dialogue going flat** — has it become functional information exchange, or is it still alive (interruptions, hesitations, wrong things said)?
- **Narrator explaining** instead of showing — the most common degradation pattern

If qualitative degradation detected: **STOP.** Announce it. Re-read the best chapter from the previous batch to recalibrate voice before proceeding.

### 4. Next Chapter or Stop

If < 5 chapters completed in this session → return to step 1.
If 5 chapters completed → proceed to Batch Complete.

---

## Batch Complete — STOP

```
📦 Batch N complete (Ch. X — Ch. Y)
Chapters: 5/5 ✅
Word counts: [list]
Average: XXXX words/chapter
Total book progress: X/31 chapters, ~XX,XXX words
State: updated through Ch. Y
Ending types used: F(X), G(X), H(X), I(X), J(X/2 max)

Relaunch /book write <book> for the next batch.
```

**STOP. The user relaunches in a fresh session.**

---

## Final Batch — Assemble

When all chapters are done:

```bash
mkdir -p output
echo "# [Project Title] — Book N: [Title]" > output/book-N-draft.md
echo "**Draft assembled: $(date)**" >> output/book-N-draft.md
echo "---" >> output/book-N-draft.md
for f in chapters/book-N/ch*.md; do
  [[ "$(basename $f)" == *plan* ]] && continue
  cat "$f" >> output/book-N-draft.md
  echo -e "\n\n---\n" >> output/book-N-draft.md
done
wc -w output/book-N-draft.md
```

```
📚 Book N complete!
Chapters: X/X ✅
Total words: ~XXX,XXX
[Chapter list with word counts]
[Any issues needing manual review]
```

---

## Rules

- ❌ Never write more than 5 chapters per session
- ❌ Never duplicate chapter-writing instructions (they live in chapter-writer)
- ❌ Never skip the degradation check
- ✅ Everything about HOW to write a chapter → follow chapter-writer
- ✅ This skill handles only WHEN and IN WHAT ORDER
- 🛑 Stop after 5 chapters OR for unresolvable errors
