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
| `fix <book>` | Apply ALL pending fixes (REVIEW.md + PROOFREAD.md + coherence devplan) | `/book fix book-1` |
| `write <book>` | Write chapters in batches of 5 | `/book write book-1` |
| `chapter <book> <ch>` | Write a single chapter | `/book chapter book-1 ch03` |
| `review <book> [ch]` | Editorial review → REVIEW.md | `/book review book-1` |
| `proofread <book> [ch]` | Grammar/syntax/punctuation → PROOFREAD.md | `/book proofread book-1` |
| `continuity <from> <to>` | Cross-book continuity check | `/book continuity book-1 book-2` |

## The Pipeline

```
PROJECT SETUP
  1. /book init                → create directory structure + templates
  2. /book setup               → interactive wizard to fill worldbuilding, characters, plot, outlines

PRE-WRITING
  3. /book coherence all       → find problems, write devplan
  4. /book fix book-1          → apply coherence fixes

WRITING LOOP (repeat per batch)
  5. /book write book-1        → write 5 chapters
  6. /book review book-1       → editorial review → REVIEW.md
  7. /book proofread book-1    → proofreading → PROOFREAD.md
  8. /book fix book-1          → apply all pending fixes

BETWEEN BOOKS
  9. /book continuity book-1 book-2 → verify cross-book consistency
```

## Execution

When a command is received:

1. **Parse the command** from the arguments.
2. **Read the instruction file** from `~/.claude/skills/book/instructions/<command>.md`:
   - `init` → `instructions/init.md`
   - `setup` → `instructions/setup.md`
   - `coherence` → `instructions/coherence-check.md`
   - `fix` → `instructions/fix.md`
   - `write` → `instructions/writer.md`
   - `chapter` → `instructions/chapter-writer.md`
   - `review` → `instructions/reviewer.md`
   - `proofread` → `instructions/proof-reader.md`
   - `continuity` → `instructions/continuity-check.md`
3. **Follow the instruction file exactly.** The instruction file IS the skill — this dispatcher just routes to it.
4. **Pass all remaining arguments** to the instruction file's process.

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
