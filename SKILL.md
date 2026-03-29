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
  7. /book review book-1       → editorial review → REVIEW.md
  8. /book proofread book-1    → line-level review → PROOFREAD.md
  9. /book revise book-1       → apply review + proofread fixes to prose

BETWEEN BOOKS
  10. /book compact all         → post-cycle cleanup
  11. /book continuity book-1 book-2 → verify cross-book consistency
```

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
3. **Follow the instruction file exactly.** The instruction file IS the skill — this dispatcher just routes to it.
4. **Pass all remaining arguments** to the instruction file's process.
5. **After the instruction completes**, commit all changes:
   - Stage all modified and new files: `git add -A`
   - Commit with message: `book <command> <args>: <one-line summary of what was done>`
   - Do NOT push (the caller decides when to push).

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
