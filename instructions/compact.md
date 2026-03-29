# Book Compact — Bloat Removal & Cross-Reference Enforcement

Remove accumulated overhead from project files without losing any information. Run after `/book fix` cycles and between books.

## Invocation

```
/book compact [scope]
```

Scope options:
- `all` — full project (default)
- `book-1`, `book-2`, `book-3` — specific book's outline + related files
- `characters` — character files only
- `world` — worldbuilding files only
- `outlines` — outline files only

---

## Process

### 1. Outline Cleanup

For each `chapters/book-N/outline.md` in scope:

**A. Remove struck-through items.** Grep for `~~`. Delete every line containing struck-through text. These are decisions already made — the old version has no value.

**A1. Strip milestone ID markers.** Grep for patterns like `(M\d+)`, `(M\d+ — [^)]+)`, `(M\d+, [^)]+)` across ALL files in scope — outlines, writing-notes, character files, world files, plot files. Remove every such occurrence. These markers are DEVPLAN tracking artifacts — they have no place in narrative or reference content. Strip inline (e.g. `**Beat title (M123):**` → `**Beat title:**`) and standalone (e.g. `(M456 — RESOLVED)` on its own) occurrences. Exception: DEVPLAN.md itself is never touched.

**B. Extract inline directives.** Find all blocks starting with `⚠️ WRITING NOTE`, `⚠️ WRITING DIRECTIVE`, `⚠️ AUTHOR REFERENCE`, `⚠️ INFODUMP GUARD`, `⚠️ STRUCTURAL NOTE`. Move each to `chapters/book-N/writing-notes.md`, organized by chapter number. In the outline, replace the block with a single-line cross-ref: `→ See writing-notes.md §ChNN-[topic]`.

**C. De-duplicate mechanism explanations.** Identify mechanisms explained more than once across chapters (Alignment Window, PLC channel, shadow pass, drone frequencies, side-channel, substrate architecture). Keep the FIRST full explanation (in the chapter where the mechanism is introduced or activates). In all subsequent chapters, replace re-explanations with: `→ Mechanism: see [file] §[section]` or `→ See Ch.NN mechanism block`.

**D. Consolidate plant tracking.** For plants tracked across multiple chapters (Sauveterre, "it calibrates", Chorus/Poem, coin, swimming, neuroprosthetics), replace per-chapter tracking notes with a single tracking table at the outline's header:

```markdown
### Plant Tracking
| Plant | Introduced | Maintained | Payoff |
|-------|-----------|------------|--------|
| Sauveterre | Ch.01 | Ch.04, Ch.07 | Ch.10 |
```

Remove the inline `[Sauveterre — ...]` notes from individual chapters. The table is the canonical tracker.

**E. Density check.** Measure word count per chapter entry. Flag any chapter entry over 800 words (normal) or 300 words (rapid cross-cut). These are bloated — compress beats to 1-2 sentences each and replace mechanism explanations with cross-refs. Target: normal chapters 150-300 words, rapid cross-cut 50-100 words.

**F. Authorial reasoning check.** Flag any outline text containing: "the reader should", "on reread", "the attentive reader", "the question is", "MANDATORY —" followed by >50 words of explanation. These are authorial reasoning blocks — move to writing-notes.md, leave one-line directive in outline.

### 2. Character De-duplication

For each character file in scope:

**A. Consolidate flashback scenes.** Each flashback/formative scene must exist in ONE place only: the `## Flashback Beats` section. Remove duplicate tellings from:
- Background/Backstory sections
- "Formative Scene Expanded" sections
- "Missing Years" or timeline sections
- "Sensory Past" sections (if they retell the same scene)

In removed locations, leave a one-line pointer: `→ See Flashback Beats §[name]`.

**B. Consolidate repeated explanations.** Find concepts stated 3+ times in the same file. Keep the richest version, replace others with cross-refs. Common offenders:
- Core relationship dynamics restated in Background, Ties, Narrative Function, Core Contradiction
- Physical details described in Appearance, Depth-Compact, Physicality Expanded
- Key events retold in Background, Worst Act, Formative Scene

**C. PRESERVE Usage Trackers.** Do NOT remove or modify any `## Usage Tracker` section in any file — they are writing scaffolding. Each tracker is a checklist ensuring every character/concept detail gets used at least once and is not repeated. Empty checkboxes `- [ ]` are the POINT — they track what has NOT yet been written. Items are marked `[x]` ONLY by `/book chapter` after a chapter is written and verified. Leave all trackers intact. This applies to ALL files that contain a `## Usage Tracker` section: character files, world-concept files, plot files, and any other file with trackable content.

**D. Extract writing instructions from character files.** If a character file contains blocks that are writing instructions rather than character information (e.g., "The reader must SEE this fight", "This is the most powerful moment", multi-paragraph prose-rules embedded in the sheet), move them to the character's narrator boundaries section or to the relevant outline chapter. Character files define WHO the character is, not HOW to write them.

### 3. World File Cross-Reference Audit

For each world file in scope:

**A. Find cross-file duplicates.** For every paragraph >50 words, check if the same information exists in another world file. If it does:
- Identify which file is the CANONICAL source (per the Information Architecture in CLAUDE.md).
- In the non-canonical file, replace the paragraph with: `→ See [canonical-file] §[section]`.
- If no Information Architecture exists in CLAUDE.md yet, propose one.

**B. Find internal duplicates.** Within the same file, find concepts explained more than once. Consolidate to the first occurrence.

**C. Archive dead files.** If a file's content is 100% superseded by canonical files (e.g., one-time audit reports whose corrections have been applied), move it to an `archive/` directory.

### 4. Episode-Outline Hierarchy

For each `plot/episode-N-*.md`:

**A. Remove plot details that exist at greater detail in the outline.** The episode file's role is STRUCTURAL: act divisions, proportions, design decisions, emotional arcs. Chapter-level beats belong in the outline only.

**B. Remove process artifacts.** Milestone IDs (`M687`), correction lists, mechanism documentation blocks — these belong in the outline or in worldbuilding docs.

**C. Replace restated mechanisms with cross-refs.** If the episode file explains the Alignment Window, temporal echoes, or PLC channel, replace with: `→ See temporal-echoes.md`.

### 5. Report

```
📋 Book Compact — [scope] — Complete

Outline cleanup:
  Struck-through items removed: X
  Directive blocks extracted to writing-notes.md: X
  Mechanism re-explanations replaced with cross-refs: X
  Plant tracking consolidated: X plants

Character de-duplication:
  Flashback duplicates removed: X scenes
  Repeated explanations consolidated: X
  Usage Trackers verified present: X files
  Writing instructions extracted: X blocks

World cross-reference:
  Cross-file duplicates replaced with refs: X paragraphs
  Internal duplicates consolidated: X
  Dead files archived: X

Episode hierarchy:
  Plot details removed (exist in outlines): X paragraphs
  Process artifacts removed: X
  Mechanisms replaced with cross-refs: X

Estimated token reduction: ~X words
```

---

## Rules

- ❌ Never delete UNIQUE information. If in doubt, keep it and flag for the user.
- ❌ Never merge files — only cross-reference. Each file keeps its identity.
- ❌ Never compact files that are being actively written (draft chapters).
- ❌ Never remove checked `[x]` items from any tracker or devplan.
- ❌ Never add `[x]` to tracker items. Only `/book chapter` marks items as written after prose is verified.
- ❌ Never remove empty `[ ]` tracker items — they are scaffolding for future writing.
- ✅ When replacing content with a cross-ref, verify the target file and section exist.
- ✅ Show the user what you're about to remove before removing it, if it's >100 words.
- ✅ Count words before and after. Report the delta.
- ✅ The compact is reversible — git tracks everything.
