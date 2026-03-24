# `/book` — A Claude Code Skill for Writing Books

A unified writing pipeline for multi-book fiction projects, designed as a [Claude Code](https://claude.ai/claude-code) custom skill. Genre-agnostic — works for sci-fi, literary fiction, fantasy, thriller, or any multi-book narrative.

## What It Does

Takes a book project from zero to finished manuscript through a structured pipeline:

```
/book init          → scaffold project structure
/book setup         → interactive wizard to build world, characters, plot
/book coherence     → find plot holes, contradictions, logic gaps
/book fix           → apply all pending fixes (coherence + editorial + proofreading)
/book write         → write chapters in batches of 5
/book review        → editorial review (structure, voice, pacing)
/book proofread     → line-level proofreading (grammar, spelling, punctuation)
/book continuity    → verify consistency between books
/book help          → show the full pipeline
```

## Installation

Copy the `book/` directory into your Claude Code skills folder:

```bash
cp -r book/ ~/.claude/skills/book/
```

Then invoke with `/book help` in any Claude Code session.

## The Pipeline

```
PROJECT SETUP
  1. /book init             create directory structure + empty templates
  2. /book setup            interactive wizard: worldbuilding, characters, plot, outlines

PRE-WRITING
  3. /book coherence all    find problems across all project files
  4. /book fix book-1       apply coherence fixes

WRITING LOOP (repeat per batch of 5 chapters)
  5. /book write book-1     write 5 chapters (with voice calibration + degradation checks)
  6. /book review book-1    editorial review → REVIEW.md
  7. /book proofread book-1 proofreading → PROOFREAD.md
  8. /book fix book-1       apply all pending fixes

BETWEEN BOOKS
  9. /book continuity book-1 book-2    verify cross-book consistency
```

## Project Structure

`/book init` creates this structure:

```
project/
├── CLAUDE.md                    ← project instructions
├── DEVPLAN.md                   ← development plan
├── world/                       ← worldbuilding
│   ├── overview.md              ← themes, structure
│   ├── tones.md                 ← tonal registers per level
│   ├── prose-rules.md           ← writing quality rules
│   ├── writing-checklists.md    ← sensory enforcement per level
│   ├── pacing-rules.md          ← tension and pacing rules
│   ├── technology-comparison.md ← cross-level tech differentiation
│   └── level-N-<name>/          ← one per narrative level
│       ├── context.md
│       └── technology.md
├── characters/
│   ├── foreground/              ← main characters (full sheets)
│   ├── midground/               ← supporting characters
│   ├── functional/              ← role-based characters
│   ├── background/              ← mentioned-only
│   └── notes/
│       ├── voice-samples.md     ← speech patterns
│       └── flashback-beats.md   ← flashback scenes
├── plot/
│   ├── overview.md              ← series structure
│   ├── episode-N-<title>.md     ← one per book
│   ├── key-scenes.md            ← pillar scenes
│   └── cliffhanger-map.md      ← chapter endings
└── chapters/
    └── book-N/
        ├── outline.md           ← chapter-by-chapter outline
        ├── opening-strategy.md  ← first 3 chapters strategy
        ├── state.md             ← running state tracker
        └── DEVPLAN.md           ← chapter writing checklist
```

## How It Works

The skill is a **dispatcher** — a lightweight router (`SKILL.md`, ~60 lines) that reads the appropriate instruction file from `instructions/` based on the sub-command. The instruction files contain the detailed process for each operation.

```
book/
├── SKILL.md                     ← dispatcher (loaded into context)
├── README.md                    ← this file
└── instructions/                ← detailed instructions (loaded on demand)
    ├── init.md                  ← project scaffolding
    ├── setup.md                 ← interactive worldbuilding wizard
    ├── coherence-check.md       ← find plot holes and contradictions
    ├── fix.md                   ← apply fixes from any source
    ├── writer.md                ← batch chapter writing orchestration
    ├── chapter-writer.md        ← single chapter writing (the core engine)
    ├── reviewer.md              ← editorial review
    ├── proof-reader.md          ← grammar/syntax/punctuation
    └── continuity-check.md      ← cross-book consistency
```

Only `SKILL.md` is loaded into Claude's context on invocation (~60 lines). The relevant instruction file is loaded on demand, keeping the context window free for your actual content.

## Key Features

- **Genre-agnostic.** All genre, tone, and style rules come from your project files, not from the skill itself. Works for sci-fi, literary fiction, fantasy, or any narrative genre.
- **9 verification passes** per chapter: plot, character voice, world consistency, style, micro-details, world pressure, word count, prose discipline, and reader perspective.
- **Unified fix command.** `/book fix` applies editorial, proofreading, AND coherence fixes in the correct order (structural → editorial → surface).
- **Voice calibration between sessions.** When resuming writing after a break, the skill calibrates by re-reading the best previous chapter and writing a quick voice test.
- **Quality degradation detection.** Every 3 chapters, checks for both quantitative (word count) and qualitative (repetition, flat dialogue, narrator overreach) degradation.
- **Cross-book continuity.** Verifies character positions, open threads, vocabulary evolution, and planted details carry correctly between books.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- A Claude model with sufficient context (Opus recommended for long chapters)

## License

MIT
