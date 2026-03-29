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

Each file is created with a header, a brief instruction comment, and empty sections to fill.

**Character template — foreground (protagonist/major):**

```markdown
# [Character Name]

<!-- Fill this file using /book setup or manually.
     RULE: each piece of information lives in ONE section only.
     If a flashback is in Flashback Beats, do NOT retell it in Backstory. Cross-ref instead.
     Include a Usage Tracker section at the end — empty checkboxes for each character detail to be shown in prose. Items are marked [x] ONLY when the chapter is written and verified. -->

## Identity
**Role:** [protagonist / antagonist / mentor / etc.]
**Age/Origin:** [age at story start, background]
**Appearance:** [physical description — ONE place, not repeated in subsections]
**First Appearance:** [book, chapter area]

## Personality
[Core traits, flaws, contradictions. Stated goals vs true goals. 1-2 paragraphs max.]

## Arc
[Per-book trajectory. 1 short paragraph per book. What changes, what's at stake.]

## Key Relationships
[1 line per relationship. Name — role — dynamic.]

## Flashback Beats
[THE canonical location for all past scenes. Full rendered scenes, 300-500w each.
 These are NOT retold in any other section. Other sections cross-ref here.]

### Flashback 1 — [Name] (age N)
[Full scene]

### Flashback 2 — [Name] (age N)
[Full scene]

## Sensory Signature
[3 sensory memories. Involuntary gestures. Physical tics. Unique detail.
 Each item once — do not repeat in other sections.]

## Voice
[Speech patterns: stress, relaxed, lying. Words never used. 2-3 sample lines.]

## Core
**Worst Act:** [1 paragraph]
**Inconfessable Desire:** [1 paragraph]
**Core Contradiction:** [1 paragraph]

## Narrator Boundaries
<!-- Narrator Boundaries are stored in characters/notes/narrator-boundaries.md, not here.
     This section is a placeholder — populate the consolidated file instead. -->
→ See characters/notes/narrator-boundaries.md §[Character]
```

**Character template — midground (secondary):**

```markdown
# [Character Name]

## Identity
**Role:** | **Age/Origin:** | **Appearance:** | **First Appearance:**

## Personality & Arc
[Combined — 1-2 paragraphs. Traits, goals, what changes.]

## Key Relationships
[1 line per relationship.]

## Flashback Beats
[0-2 scenes, 200-300w each. Canonical location — not retold elsewhere.]

## Sensory Signature
[1-2 sensory details. 1 gesture. 1 tic.]

## Voice
[Speech pattern, 1-2 sample lines.]

## Core
**Worst Act / Core Contradiction:** [1 paragraph combining both.]
```

**Character template — background/functional:**

```markdown
# [Character Name]

**Role:** | **Level:** | **Appears:** [book, chapters]

[1-2 paragraphs covering everything: personality, function, 1 distinguishing detail.]
```

**Key template principles:**
- **All files with discrete elements** (character files, world files, plot tracking files) include a `## Usage Tracker` section with the same TABLE format mapping elements to specific chapters:

  | Element | Book | Ch | Detail | Status |
  |---------|------|----|--------|--------|
  | [description] | B1 | 07 | scene/accent | —/planned/written |

  - `scene` = rendered beat · `accent` = one-two sentence texture
  - `—` = no chapter assigned · `planned` = chapter assigned · `written` = in draft
  - The tracker IS the placement plan — no need to duplicate in chapter outlines
  - One format everywhere: character files, world files, plot files. No exceptions.
  - Keep files under ~150 lines of content before the tracker. If larger, split by topic so the chapter writer loads only what's relevant

- Chapter outlines include a `context:` field in each chapter header listing which conditional world/plot files the chapter-writer must load beyond the always-loaded set. Only add a file to `context:` if it has tracker items mapped to that chapter.
- No overlapping sections. Each fact lives in ONE section. Other sections use `→ See §[section]` if they need to reference it.
- Each concept has ONE canonical file. When generating level context files, technology files, and thematic files, check for overlap. If two files would describe the same mechanism, pick one as canonical and cross-ref from the other.
- Foreground files: ~1500-2500 words. Midground: ~800-1500. Background: ~100-500.
- Writing instructions (how to render the character in prose) go in `characters/notes/narrator-boundaries.md`, NOT inline in character files.

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

## Information Architecture — Single Source of Truth

Each concept has ONE canonical file. Other files cross-reference with `→ see [file] §[section]`, never restate.

| Concept | Canonical file |
|---------|---------------|
| Chronological timeline | `world/timeline.md` |
| Historical roots (2020s) | `world/timeline.md` |
| ASI strategies per bloc | `world/level-0-reality/asis.md` |
| Cross-level mechanisms (echoes, PLC, alignment window) | `world/temporal-echoes.md` |
| The Game mechanics + master key | `world/level-0-reality/the-game.md` |
| Corporate structure (Meridian) | `world/level-0-reality/meridian.md` |
| Flashback scenes (per character) | `characters/<char>.md §Flashback Beats` |
| Chapter-level plot detail | `chapters/book-N/outline.md` |
| Book-level story structure | `plot/episode-N.md` |
| Trilogy-level plot summary | `plot/overview.md` |

**Rule**: when writing in a non-canonical file and about to explain a mechanism, write `→ see <file> §<section>` instead of re-explaining.

## Plot Documentation Hierarchy

| Level | File | Contains | Does NOT contain |
|-------|------|----------|-----------------|
| Trilogy | `plot/overview.md` | Structural summary, emotional bridges, themes | Chapter-level detail |
| Book | `plot/episode-N.md` | Act structure, design decisions, proportions | Beat-by-beat detail, mechanism explanations |
| Chapter | `chapters/book-N/outline.md` | Scene beats, tracking, cliffhangers | Mechanism re-explanations (use cross-refs) |

Information lives at the LOWEST level where it's needed. Never duplicate between levels.

## File Lifecycle

- **Review/audit reports**: once corrections are applied to canonical files, move to `archive/`. Do not keep in active directories.
- **Writing notes** (`chapters/book-N/writing-notes.md`): extracted from outline `⚠️` blocks. Live alongside the outline, not inline.
- **Character files**: include Usage Trackers with empty checkboxes. Mark `[x]` only when the detail is written in a chapter and verified.
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
