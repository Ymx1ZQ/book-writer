# Book Init — Project Scaffolding

Create the directory structure and empty template files for a new multi-book fiction project.

## Invocation

```
/book init
```

No arguments. The command asks the user for project parameters interactively.

---

## Process

### 1. Ask Project Parameters

Ask the user these questions (accept brief answers — we'll flesh things out in `/book setup`):

1. **Project name** — What's the working title?
2. **Number of books** — How many books in the series? (1, 2, 3, or more)
3. **Narrative levels** — Does the story have multiple narrative levels, timelines, or worlds? If yes, how many and what are their names? (e.g., "Reality, Dome, Ark" or "Past, Present, Future" or "just one")
4. **Approximate chapters per book** — Rough number? (default: 30)
5. **Language** — What language is the book written in? (default: American English)
6. **Genre/tone keywords** — Brief genre description? (e.g., "sci-fi thriller" or "literary fiction" or "fantasy with horror elements") — used only for template hints, not hardcoded

### 2. Create Directory Structure

```
<project>/
├── CLAUDE.md                    ← operational instructions (HOW to work)
├── README.md                    ← project orientation (directory map)
├── DEVPLAN.md                   ← master development plan (empty)
├── world/                       ← worldbuilding
│   ├── overview.md              ← story structure, themes
│   ├── tones.md                 ← tonal registers (1 per level, or 1 if single level)
│   ├── prose-rules.md           ← writing quality rules
│   ├── writing-checklists.md    ← sensory enforcement per level
│   ├── pacing-rules.md          ← pacing and tension rules
│   ├── technology-comparison.md ← cross-level tech differentiation (if multiple levels)
│   └── level-N-<name>/          ← one directory per narrative level
│       ├── context.md           ← environment, technology, daily life
│       └── technology.md        ← interfaces, devices, infrastructure
├── characters/
│   ├── foreground/              ← main characters (full sheets)
│   ├── midground/               ← secondary characters (key scenes)
│   ├── functional/              ← role-based characters
│   ├── background/              ← mentioned-only characters
│   └── notes/
│       ├── voice-samples.md     ← speech patterns and tics
│       └── flashback-beats.md   ← flashback scenes per character
├── plot/
│   ├── overview.md              ← trilogy/series structure
│   ├── episode-N-<title>.md     ← one per book (detailed plot)
│   ├── key-scenes.md            ← pillar scenes across all books
│   └── cliffhanger-map.md       ← chapter endings by type
└── chapters/
    └── book-N/                  ← one per book
        ├── outline.md           ← chapter-by-chapter outline
        ├── opening-strategy.md  ← emotional objectives for first 3 chapters
        ├── state.md             ← running state tracker
        └── DEVPLAN.md           ← chapter writing checklist
```

### 3. Generate Template Files

Each file is created with a header, a brief instruction comment, and empty sections to fill. Example for a character template:

```markdown
# [Character Name]

<!-- Fill this file using /book setup or manually. -->

**Role:** [protagonist / antagonist / mentor / etc.]
**Appearance:** [physical description]
**Personality:** [core traits, flaws, contradictions]
**Stated Goals:** [what they say they want]
**True Goals:** [what they actually want]
**Ties:** [relationships to other characters]
**First Appearance:** [book, chapter area]

### Backstory
[Key events before the story begins]

### Worst Act
[The worst thing this character does in the story]

### Core Contradiction
[The tension that makes them interesting]

## Usage Tracker
- [ ] Physical appearance described in scene (Book __, Ch. __)
- [ ] Involuntary gesture shown (Book __, Ch. __)
- [ ] Speech under stress demonstrated (Book __, Ch. __)
[etc.]
```

### 4. Generate CLAUDE.md

**CRITICAL: CLAUDE.md is an OPERATIONAL file, not a narrative file.** It tells Claude HOW to work and WHERE to find things. It NEVER contains narrative content (plot summaries, character descriptions, tonal details, worldbuilding). All narrative content lives in the project files (`world/`, `characters/`, `plot/`). CLAUDE.md only POINTS to those files.

Generate CLAUDE.md with this structure:

```markdown
# [Project Title]

> **This file contains operational instructions only.** All narrative content
> (plot, characters, worldbuilding, tones, concepts) lives in the project files.
> Never duplicate narrative details here — use pointers instead. CLAUDE.md tells
> you HOW to work and WHERE to find things. The project files tell you WHAT the
> project is.

## Project Structure

[Minimal directory tree — folders only, one-word role each. For the full tree, see README.md.]

## Where to Find Things

[Reference table mapping needs to files. Example:]

| What you need | Where it lives |
|---------------|---------------|
| Tonal registers | `world/tones.md` — **read before every chapter** |
| Pacing rules | `world/pacing-rules.md` |
| Prose quality rules | `world/prose-rules.md` |
| Character voice samples | `characters/notes/voice-samples.md` |
| Full trilogy plot | `plot/overview.md` |
| Cliffhanger map | `plot/cliffhanger-map.md` |
[...etc, one row per key file]

## Writing Language

[Language setting from Step 1]

## How to Write a Chapter

Use the `/book chapter` skill. It handles everything:
1. Reads the outline, context, and state
2. Writes the draft
3. Runs verification passes
4. Revises if needed
5. Updates state
6. Marks complete

For batch writing, use `/book write book-N`.

## Files to Read Before Any Writing Task

Always load these before writing:
- The chapter's outline entry (from `chapters/book-N/outline.md`)
- The relevant tonal register (from `world/tones.md`)
- The POV character's foreground sheet
- The cliffhanger type for this chapter (from `plot/cliffhanger-map.md`)
- The current state file (from `chapters/book-N/state.md`)
- `world/pacing-rules.md`
- `world/prose-rules.md`
- `world/writing-checklists.md`
- `characters/notes/voice-samples.md`
```

**What CLAUDE.md must NEVER contain:**
- Plot summaries or key concepts (those go in `world/overview.md`, `world/the-word.md`, etc.)
- Tonal descriptions (those go in `world/tones.md`)
- Character lists or descriptions (those go in `characters/`)
- Chapter counts or structural details that change over time
- Anything that duplicates content from project files

### 5. Generate README.md

**README.md is a minimal orientation file** for anyone opening the project folder for the first time. It contains:

```markdown
# [Project Title]

[One-line description from Step 1]

---

## Project Structure

[Full directory tree with every file and a one-line description per entry.
This is the ONLY place the full tree lives. CLAUDE.md points here.]

---

## How to Work

- `CLAUDE.md` — operational instructions (how to write, where to find things)
- `DEVPLAN.md` — what needs to be done (milestones, fixes, progress)
- `/book help` — all available commands
```

**What README.md must NEVER contain:**
- Narrative content (themes, character rosters, plot summaries)
- Development history or milestone counts (these go stale)
- Anything that duplicates content from project files

### 6. Announce

```
Project scaffolded: [title]
Books: N
Levels: [list]
Chapters/book: ~N
Language: [language]

Files created: X
Empty templates ready for: /book setup

Next step: /book setup
```

---

## The Separation Principle

The project has three meta-files with distinct, non-overlapping roles:

| File | Role | Contains | Never contains |
|------|------|----------|----------------|
| `CLAUDE.md` | **How to work** | Operational instructions, file pointers, writing process | Narrative content, plot, characters, tones, counts |
| `README.md` | **Where things are** | Directory tree, one-line descriptions | Narrative content, development history, counts that change |
| `DEVPLAN.md` | **What to do** | Milestones, fixes, progress tracking | Operational instructions, directory maps |

This separation prevents stale data: when narrative details change (e.g., a level moves from deep-space to LEO), only the project file (`world/tones.md`) needs updating. CLAUDE.md and README.md don't break because they never contained the detail — they only pointed to it.

---

## Rules

- ❌ Never create narrative content — only structure and templates. Content comes from `/book setup`.
- ❌ Never assume genre specifics — templates are generic.
- ❌ Never put narrative content in CLAUDE.md — it is operational only.
- ❌ Never put development history or stale counts in README.md — it is structural only.
- ✅ Create every directory and file, even if empty — the structure IS the project.
- ✅ Use markdown comments `<!-- -->` in templates to guide the user.
- ✅ CLAUDE.md points to project files. README.md shows the full tree. DEVPLAN.md tracks work.
