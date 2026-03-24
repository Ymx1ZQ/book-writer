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
├── CLAUDE.md                    ← project instructions (created with basics)
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
    └── book-N/
        ├── outline.md           ← chapter-by-chapter outline
        ├── opening-strategy.md  ← emotional objectives for first 3 chapters
        ├── state.md             ← running state tracker
        └── DEVPLAN.md           ← chapter writing checklist
    └── book-N/                  ← one per book
        ├── outline.md           ← chapter-by-chapter outline
        ├── state.md             ← running state tracker
        └── DEVPLAN.md           ← chapter writing tracker
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

Create a project CLAUDE.md with:
- Project title and description
- Directory structure reference
- Language setting
- Key writing rules (to be filled in `/book setup`)
- How to write a chapter (points to `/book chapter`)

### 5. Announce

```
📁 Project scaffolded: [title]
Books: N
Levels: [list]
Chapters/book: ~N
Language: [language]

Files created: X
Empty templates ready for: /book setup

Next step: /book setup
```

---

## Rules

- ❌ Never create content — only structure and templates. Content comes from `/book setup`.
- ❌ Never assume genre specifics — templates are generic.
- ✅ Create every directory and file, even if empty — the structure IS the project.
- ✅ Use markdown comments `<!-- -->` in templates to guide the user.
