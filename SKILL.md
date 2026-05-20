# Book — Unified Writing Pipeline

Single entry point for all book-writing operations. Genre-agnostic — reads tone, rules, structure, and genre from the project's own files (CLAUDE.md, world/, characters/).

## Invocation

```
/book <command> [arguments]
```

## Commands

| Command | What it does | Example |
|---------|-------------|---------|
| `help` | Show this help + the full pipeline | `/book help` |
| `init` | Scaffold a new book project (directories, empty templates) | `/book init` |
| `setup` | Interactive wizard to populate project files (worldbuilding, characters, plot) | `/book setup` |
| `coherence [scope]` | Find problems across project, write fix devplan | `/book coherence all` |
| `fix <scope>` | Apply coherence fixes from DEVPLAN.md to project files | `/book fix all` |
| `fix common` | Apply ONLY coherence fixes on shared files (world/, characters/, plot/) | `/book fix common` |
| `revise <book>` | Apply editorial (REVIEW.md) + proofreading (PROOFREAD.md) fixes to chapter prose | `/book revise book-1` |
| `write <book>` | Write chapters in batches of 5 | `/book write book-1` |
| `chapter <book> <ch>` | Write a single chapter | `/book chapter book-1 ch03` |
| `review <book> [ch]` | Editorial review → REVIEW.md | `/book review book-1` |
| `proofread <book> [ch]` | Grammar/syntax/punctuation → PROOFREAD.md | `/book proofread book-1` |
| `compact [scope]` | Remove bloat, enforce cross-refs, de-duplicate | `/book compact all` |
| `continuity <from> <to>` | Cross-book continuity check | `/book continuity book-1 book-2` |
| `pdf <book> [ch]` | Render a chapter or a whole book to PDF | `/book pdf book-1 ch01` |
| `epub <book> [ch]` | Render a chapter or a whole book to EPUB (Kindle/KDP) | `/book epub book-1` |
| `sniff <book> [ch]` | Adversarial skeptical-reader pass → SMELL.md (catches plausibility / nose-wrinkle issues coherence/review/proof don't) | `/book sniff book-1 ch01` |
| `coldread <book> [ch]` | First-time-reader developmental pass → COLDREAD.md (scene engine, propulsion, legibility — reads with NO canon loaded) | `/book coldread book-1 ch03` |

## The Pipeline

```
PROJECT SETUP
  1. /book init                → create directory structure + templates
  2. /book setup               → interactive wizard to fill worldbuilding, characters, plot, outlines

PRE-WRITING
  3. /book coherence all       → find problems, write devplan
  4. /book fix all             → apply coherence fixes to project files
  5. /book compact all         → remove bloat, enforce cross-refs, de-duplicate

WRITING LOOP (repeat per batch)
  6. /book write book-1        → write 5 chapters
  7. /book sniff book-1        → adversarial skeptical-reader → SMELL.md
  8. /book review book-1       → editorial review → REVIEW.md
  9. /book coldread book-1     → first-time-reader developmental pass → COLDREAD.md
 10. /book proofread book-1    → line-level review → PROOFREAD.md
 11. /book revise book-1       → apply SMELL + REVIEW + PROOFREAD fixes to prose

BETWEEN BOOKS
 12. /book compact all         → post-cycle cleanup
 13. /book continuity book-1 book-2 → verify cross-book consistency
```

**Pre-draft context symmetry:** the chapter-writer agent enforces beat↔context symmetry before drafting (chapter-writer Step 2.6 — STOP on missing files, advisory on orphans). `coherence-check` flags drift on already-written outlines as WARNING (classes R + S). No standalone subcommand: the symmetry check lives inside `chapter-writer` (write-time) and `coherence-check` (audit-time).

## Execution

When a command is received:

1. **Parse the command** from the arguments.
2. **Read the instruction file** from `~/.claude/skills/book/instructions/<command>.md`:
   - `init` → `instructions/init.md`
   - `setup` → `instructions/setup.md`
   - `coherence` → `instructions/coherence-check.md`
   - `fix` → `instructions/fix.md`
   - `revise` → `instructions/revise.md`
   - `write` → `instructions/writer.md`
   - `chapter` → `instructions/chapter-writer.md`
   - `review` → `instructions/reviewer.md`
   - `proofread` → `instructions/proof-reader.md`
   - `compact` → `instructions/compact.md`
   - `continuity` → `instructions/continuity-check.md`
   - `pdf` → `instructions/pdf.md`
   - `epub` → `instructions/epub.md`
   - `sniff` → `instructions/sniff.md`
   - `coldread` → `instructions/coldread.md`
3. **Follow the instruction file exactly.** The instruction file IS the skill — this dispatcher just routes to it.
4. **Pass all remaining arguments** to the instruction file's process.
5. **After the instruction completes**, commit all changes:
   - Stage all modified and new files: `git add -A`
   - Commit with message: `book <command> <args>: <one-line summary of what was done>`
   - Do NOT push (the caller decides when to push).

## Milestone Format

`DEVPLAN.md` milestones use two formats depending on what closes them:

- **Executable items** (consumable by `/book fix`, `/book revise`, `/book write`, or direct agent edits) use checkbox `- [ ]`.
- **Operational items** (orchestration script runs, manual tests, deferred verifications, runbook steps) use plain bullet `- ` without checkbox.

Reason: `run-coherence-cycle.sh` and `run-write-cycle.sh` count `^- \[ \]` as unresolved findings. Operational items in checkbox form accumulate as a constant offset that trips the stuck-issue guardrail spuriously. See `instructions/milestone-format.md` for the full doctrine, examples, and the override of any global "every task = checkbox" rule.

## Genre Agnosticism

This skill contains NO genre-specific content. All genre, tone, style, and structural rules come from the project's own files:
- `CLAUDE.md` — project-level instructions, language, structure overview
- `world/tones.md` — tonal registers per narrative level
- `world/prose-rules.md` — writing quality rules
- `world/writing-checklists.md` — sensory enforcement per level
- `characters/notes/voice-samples.md` — character voice profiles

The instructions reference these files generically: "read the project's tone file" not "apply Kafkaesque register." This makes the pipeline usable for any multi-book fiction project.

## If `help` is the command

Display the Commands table and Pipeline section above. Then stop.

## Rules

- ❌ Never execute without reading the instruction file first
- ❌ Never hardcode genre, tone, or style in the dispatcher or instructions — it comes from the project
- ✅ If the command is not recognized, show the help table
- ✅ If arguments are missing, show the relevant command's usage
