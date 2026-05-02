# Book Coherence Check

Run a comprehensive coherence review across the project's worldbuilding, characters, and outlines. Combines the "reader who asks obvious questions" with the rigor of a professional script doctor. Genre, tone, and structural rules are read from the project's own files — this instruction is genre-agnostic.

**Routing doctrine:** every finding written by this skill is classified by its primary target file and routed to one of two channels per `world/canon-hierarchy.md`:

- Target in `world/`, `plot/`, `characters/`, `chapters/<book>/outline.md`, `chapters/<book>/state.md`, or `chapters/<book>/writing-notes.md` → **DEVPLAN milestone** (consumed by `/book fix`).
- Target in `chapters/<book>/ch*.md` (chapter prose) → **per-chapter `chapters/<book>/SMELL.md` entry** (consumed by `/book revise`).

A single finding may produce paired entries in BOTH channels when the contradiction needs canon AND prose updates (the orchestration scripts run `fix` and `revise` in sequence so both close in the same cycle). The two-channel routing is what closes the loop on chapter-prose findings — without it, prose-target milestones written to DEVPLAN would never be applied (`/book fix` does not touch chapter prose by design).

**Milestone format:** see `instructions/milestone-format.md` — checkboxes only for pipeline-executable items. Coherence findings routed to `DEVPLAN.md` are executable by `/book fix`, so they correctly use `- [ ]`.

## Invocation

```
/book coherence [scope]
```

Scope options:
- `all` — full project review (default)
- `book-N` — a single book's outline + relevant worldbuilding/characters. Discover available books by listing `chapters/book-*/outline.md`.
- `characters` — character files only
- `world` — worldbuilding files only

---

## Process

### 1. Load Files (deferred — load per check category, not all upfront)

**Do NOT load everything at once.** Load only the files each check category actually needs, just before running that category. This keeps context lean and avoids reading dozens of files that are irrelevant to specific checks.

**Load upfront (needed for orientation across all checks):**
- `world/overview.md` — narrative levels, central themes, structural rules
- `chapters/book-N/outline.md` — the relevant outline(s) for scope
- `chapters/book-N/opening-strategy.md` — if it exists

**Load per category (just before running each check):**

| Check | Load at this point |
|---|---|
| A — Cross-Level Architecture | `world/temporal-echoes.md`, `world/simulation-rules.md` (if exists) |
| B — Plot Holes | `plot/` files: episode overviews, key-scenes, cliffhanger-map |
| C — Causal Flow & Knowledge | `plot/` files (if not already loaded), `plot/information-asymmetry.md` (if exists) |
| D — Character Consistency | `characters/foreground/` all sheets, `characters/midground/` all sheets, `characters/notes/` |
| E — Technology | `world/technology-comparison.md`, all `world/level-*-<name>/` files relevant to scope |
| F — Pacing | `world/pacing-rules.md`, re-use outlines already loaded |
| G — Infodump | Re-use outlines; load chapter drafts only if they exist (`chapters/book-N/ch*.md`, excluding plan files) |
| H — Thematic | Re-use `world/overview.md` already loaded |
| I — Reader Experience | `plot/reader-journey.md` (if exists), re-use outlines |
| J — Chekhov | `plot/prestige-inventory.md` (if exists), `plot/motif-tracking.md` (if exists), ALL outlines across all books |
| K — Context Tags & Trackers | All `world/level-*-<name>/` files (if not already loaded), all files referenced in `context:` tags across outlines |
| L — Economic-Anchor Audit | Level-appropriate anchor files: Reality → `world/level-0-reality/economy.md` (+ `consumer-anchors.md` if present); Ark → `world/level-1-ark/daily-life.md`; Dome → `world/level-2-dome/bureaucracy.md` + `context.md`; cross-level → `world/economy-cross-level.md` (if present). Load chapter drafts (`chapters/book-N/ch*.md`). |
| M — System-Implying-Number Audit | Re-use level files already loaded for L and E; load `world/level-0-reality/surveillance.md`, `world/level-0-reality/agent-capabilities.md`, `world/the-authors-method.md` if present; load chapter drafts. |
| N — Interior-Labeling Detector | Chapter drafts only (re-use those loaded for G); reference `world/prose-rules.md` if not already loaded. |
| O — Outline-to-Draft Coverage | Outlines already loaded for the scope; chapter drafts (re-use); `chapters/book-N/outline-deviation.md` if present. |
| P — Cross-Substrate Sensory-Echo | `world/temporal-echoes.md` already loaded for A; chapter drafts (re-use). |
| Q — Redundancy-with-Adjacent-Text | Chapter drafts only (re-use). |

**For scope `characters`:** load only rows D and skip all others.
**For scope `world`:** load only rows A, E, H, L (anchor files only), and skip character/outline/draft checks.
**For scope `book-N`:** load outlines upfront for that book only; load ALL books' outlines only for check J. Checks L–Q only run if chapter drafts exist for the scope.

### 2. Check Categories (19 checks)

For every issue found: **cite the specific file and section**, and **propose a practical fix**.

---

#### A. Cross-Level Architecture
Analyze the relationship between the project.s narrative levels (read from `world/overview.md`). This is a multi-level narrative, not a multi-timeline one — but the same rules apply:
- Do actions in one level have **logical, consistent consequences** in the connected levels?
- If the project uses cross-level echoes or causal links, check that actions in one level produce consistent effects in connected levels. Is the echo specific enough for the reader to notice?
- 
- 
- Flag any **causal weakness or paradox** in the cross-level links.

#### B. Plot Holes & Deus Ex Machina
- Identify narrative threads left dangling (introduced and never resolved).
- Flag conflicts resolved too conveniently — characters rescued by coincidence, problems solved by information that appears from nowhere, technology that works exactly when needed and fails exactly when dramatic.
- Flag any event that happens **without justification** within the rules of the world.
- Check the resolution of each book's climax: is it earned, or does it rely on contrivance?

#### C. Causal Flow & Knowledge Consistency
- For each major plot beat: trace the cause-and-effect chain backward. Does it hold?
- Flag scenes where characters **know things they shouldn't yet know**. Cross-reference what each character has learned in previous chapters.
- Flag **logical jumps** — moments where the narrative skips from A to C without establishing B.
- Pay special attention to cross-level knowledge: does a character in one level know something that only a reader of another level.s chapters would know?

#### D. Character Consistency
- For each protagonist's major decision: is it consistent with their established personality, background, and trauma?
- Flag any character who acts **"out of character" to serve the plot** — they do something only because the story needs them to, not because they would.
- Check character arcs: does each protagonist change in a way that follows from what happened to them? Is the change gradual or abrupt?
- Verify the naming convention: Check that character naming conventions match the rules defined in their character sheets.

#### E. Worldbuilding & Technology Consistency
Using `world/technology-comparison.md` as primary reference:
- Does technology respect the established rules per level? (Check the project's `world/technology-comparison.md` or equivalent for the specific rules.)
- Is there a **coherent evolution** between levels? (Check the project's worldbuilding files for the specific level progression.)
- Flag technology that appears or disappears conveniently ("they hack the terminal" — do they have the skills/tools established for this?).
- Flag any confusion between levels: technology, aesthetics, or vocabulary from one level leaking into another.
- Are technology aesthetics maintained consistently per level?

#### F. Pacing & Cross-Level Balance
- Does the alternation between levels maintain tension, or does switching break momentum?
- Do transitions happen at the right moments (cliffhangers, not mid-scene)?
- **Is one level visibly weaker or more boring than the others?** If so, identify which and why.
- Check chapter length variation: do crisis sections use shorter chapters? Does the pacing arc match what `world/pacing-rules.md` prescribes?
- Verify the [RAPID CROSS-CUT] sections: are they genuinely rapid (2-3 pages), and does the cross-cutting create urgency?

#### G. Infodump Detection
- Flag any passage where worldbuilding or technology is explained in a **block of exposition** rather than through action, dialogue, or sensory experience.
- Flag any dialogue that is really **exposition wearing quotation marks** ("As you know, [worldbuilding detail the character already knows]...").
- Check the first 3 chapters especially: do they show the world through the character's experience, or do they stop to explain it?
- The rule: if removing a paragraph of description doesn't break the scene's action, the paragraph is probably an infodump.

#### H. Thematic Resonance
- Do all three levels explore the **central themes** consistently? (the project's central themes (read from `world/overview.md` or `CLAUDE.md`))
- Is the **emotional stake** clear in each level? (Read the project's theme/stakes from world files.
- Do the levels **comment on each other thematically**? (Check that levels comment on each other thematically — testing the same question from different angles.
- Flag any level or arc that feels **thematically disconnected** from the others.

#### I. Reader Experience & Investment
- "Is this boring?" — Flag sections that are mostly exposition without action/tension.
- "Does the reader have a reason to care about this character?" — Flag characters who appear without emotional setup.
- "Would a reader continue reading after this chapter?" — Check every chapter ending for forward momentum.
- "Does this make sense to someone who HASN'T read the worldbuilding docs?" — The docs don't ship with the book.
- "Where would a reader on a train put the book down?" — Flag those moments.

#### J. Chekhov's Inventory

##### Multi-book awareness

When scope is a single book, this check MUST still load the outlines of ALL books (`chapters/book-*/outline.md`) plus all files in `plot/`. The scoped book is the **focus** — you audit its plants in detail — but payoffs can land in ANY book of the series.

Classification rules:
- A plant in Book N with payoff in Book N → normal plant/payoff. Check it.
- A plant in Book N with payoff in a later book → **cross-book plant**. Tag as `✅ CROSS-BOOK: planted B{N}, payoff B{M}`. NOT an orphan.
- A plant in Book N with NO payoff in ANY book → **orphan**. Flag it.
- A payoff in Book N with NO plant in any earlier book → **missing plant / retroactive plant**. Flag it.

##### Inventory categories

A complete inventory of introduced elements and their payoff status:
- **Plants:** Things introduced early that pay off later (a name dropped in passing, recurring objects, specific character details). Is every plant paid off within the series? Is any payoff missing its plant?
- **Cross-book plants:** Plants whose payoff lands in a later book. List each with its source book and payoff book. These are NOT orphans — they are working as intended. Only flag if the payoff is missing from ALL books.
- **Promises:** Things the narrative promises to the reader (a mystery, a threat, a character's growth). Is every promise kept by the end of the series?
- **Orphans:** Things introduced and abandoned — characters, objects, questions, subplots — with no payoff in ANY book.
- **Retroactive plants:** Things that appear in a later book that SHOULD have been planted in an earlier book but weren't.

#### K. Context Tag & Usage Tracker Audit

**Context tags:**
- For each chapter in scope, verify a `context:` field exists in the chapter header. If a chapter mentions a temporal echo, flashback, thematic concept, or countdown beat but lacks the corresponding file in its `context:` tag, flag as WARNING.
- For each file listed in any chapter's `context:` tags, verify it has a `## Usage Tracker` section. If a file contains discrete consumable details but lacks a tracker, flag as WARNING: "context file without tracker."

**World file trackers (table format — Book/Ch/Detail/Status):**
- Verify all world files in `world/level-*-<name>/` directories have a `## Usage Tracker` section. Flag missing trackers as WARNING.
- For tracker items in files OUTSIDE level directories (e.g., `world/temporal-echoes.md`, `world/nothingness.md`): verify the target chapter's `context:` field includes this file. If not, flag as WARNING: "tracker item mapped to chapter but file not in context tag." Files inside `world/level-*-<name>/` directories are loaded selectively by the chapter writer based on tracker items — they do NOT need context tags.
- Flag any chapter with a context tag pointing to a file that has NO tracker items mapped to that chapter (unnecessary loading, wastes agent context). Exclude always-loaded files (tones.md, prose-rules.md, etc.) from this check.
- Flag any world file where >50% of elements have no chapter assigned (`—` status) as NOTE: "worldbuilding without placement plan."

**Character file trackers (same table format):**
- Verify all character files in scope have a `## Usage Tracker` section with the standard table format (Book/Ch/Detail/Status).
- Flag character files still using the old checkbox format as NOTE: "character tracker needs migration to table format."

#### L. Economic-Anchor Audit (BLOCKING for unanchored monetary detail)

**Load:** the level-appropriate anchor file for each chapter draft in scope (Reality → `world/level-0-reality/economy.md` and `consumer-anchors.md` if present; Ark → `world/level-1-ark/daily-life.md` §Economy; Dome → `world/level-2-dome/bureaucracy.md` §Allocation Mathematics + `context.md` §Economy and Distribution; cross-level → `world/economy-cross-level.md` if present).

**Scan each chapter draft (`chapters/<book>/ch*.md`)** for monetary/transactional/allocation details using these patterns:

- `€\d` (euro symbol followed by digits)
- `\beuros?\b` (the word "euro" or "euros")
- `\bCBDC\b` near digits (within ~10 chars)
- `\bGPU-HE\b` near digits
- `\bkilo\b` / `\b/kg\b` / `\bper kilo\b` in a price context
- `\bbalance\b` near a numeric (CBDC balance reference)
- `\bration\b` near a numeric (Dome rationing or Ark surplus mention)
- `\bcompliance score\b` (Dome score reference)
- `\bmemory credit\b` near a numeric (cross-level)
- `\benzyme cloth\b` near a numeric (Ark unit-of-value reference)
- `W-RAR-03` (Dome resource allocation form)

**For each match:** verify the figure traces to the level-appropriate anchor file. The figure must be either: (a) a direct anchor citation (the value matches a published number in the anchor file), or (b) within the documented range/scarcity-premium band stated by the anchor.

**Flag:**
- Match without traceable anchor → **BLOCKING**: "unanchored monetary detail at <file>:<line>: \"<quote>\". Required anchor: <file> §<section>." **Route to:** if the prose value can be aligned to the anchor file by editing the anchor (the prose is already canonical-shaped) → DEVPLAN milestone targeting the anchor file. If the prose value must change to match the anchor → SMELL.md entry on the chapter, with INLINE classification and a Suggested action that quotes the anchor's value. If both must change (anchor missing AND prose un-grounded) → paired entries in BOTH channels.
- Match contradicting the anchor (price outside documented range with no in-text scarcity-premium justification) → **BLOCKING**: "monetary detail contradicts canonical anchor (<value> vs <range>)." **Route to:** apply canon-hierarchy: anchor file is higher-tier than prose, so prose changes → SMELL.md entry on the chapter (INLINE).
- If the level-appropriate anchor file does NOT exist at all, flag as **BLOCKING** at the project level: "level <N> has chapter drafts with monetary detail but no Consumer Anchors / Allocation Mathematics section. Add the anchor before the chapter can ship." **Route to:** DEVPLAN milestone (creates the anchor file or section).

#### M. System-Implying-Number Audit (BLOCKING for invented systems)

**Scan each chapter draft** for specific numbers/terms that imply a system. Pattern set:

- `tier <digit>` (e.g., "filtration alert tier two")
- `\bscore\b` near digits (compliance, attestation, etc.)
- `<digit> Hz` outside canonical anchors
- `<digit> MHz`
- `% offer` / `% loyalty` / `% discount` (loyalty program numbers)
- `compliance check at <time>` (specific time-of-day procedural reference)
- `corridor 0\d\d` (drone corridor numbering schema)
- `\blatency\b` / `\bbandwidth\b` near specific values
- `LED` with a hardware-vintage capability claim (e.g., "wired in series with the capture circuit")
- `\bfirmware\b` / `\bhandshake\b` claims about specific hardware behavior
- `\bsignature\b` (sonic, digital, side-channel) with a specific descriptor
- drone-altitude class / attestation tier / filtration alert tier references with a specific value

**For each match:** verify a canonical worldbuilding file documents the system implied. If the chapter says "filtration alert tier two", a tier system MUST exist in `ecology.md` or similar. If the chapter says "drone corridor 042", a corridor numbering schema MUST exist in `surveillance.md` or similar.

**Flag:**
- Match without a documented system → **BLOCKING**: "system-implying detail at <file>:<line>: \"<quote>\" — implies a <system-name> not documented in canon. Either canonicalize the system in <expected file> or remove the false specificity (replace with non-specific phrasing)." **Route to:** DEVPLAN milestone proposing the system definition (canon creation per `canon-hierarchy.md` anchor-creation policy — propose a value derived from adjacent anchors and timeline trajectory, with a `Reasoning:` block).
- Match contradicting a documented system → **BLOCKING**: "value contradicts canonical <system-name>." **Route to:** SMELL.md entry on the chapter (INLINE) — prose is lower-tier than the system definition, so prose changes.

#### N. Interior-Labeling Detector (NOTE — soft, advisory)

**Scan each chapter draft narration (NOT dialogue)** for forbidden interior-labeling formulas. Use chapter Step 3.5 check #15 as the spec; coherence-check is the second-line catch in case the writer's self-edit missed one.

Patterns:
- `the closest thing to <emotion>` (with `had had in <time>` or similar narrator-chiosa context)
- `a kind of <abstract noun>`
- `almost <verb>` / `almost felt like`
- `started to <verb> ... [before|and] stopped` as interior gesture-labeling
- `<character> felt <X>` followed by an explanation sentence

**Flag every match as NOTE:** "interior labeling at <file>:<line>: \"<quote>\". Suggested rewrite: collapse to physical signal alone (Rule 9, narrator-emotion-labeling)." **Route to:** SMELL.md entry on the chapter (INLINE). All N findings are prose-target.

NOT BLOCKING — these are advisory; revise applies them but flagged with `Severity: NOTE` so a downstream pass can deprioritize if needed.

#### O. Outline-to-Draft Coverage (WARNING; BLOCKING if undocumented)

**Load** `chapters/<book>/outline.md` and any `chapters/<book>/outline-deviation.md` (created by chapter-writer Step 2.5.d when scenes are cut/split/merged).

**For each chapter draft in scope:**
- Read the outline entry for the chapter (use the per-chapter targeted load — locate `## Ch. NN` header, read to next chapter header).
- Enumerate the outlined scenes (each `### N.` or numbered beat block).
- For each outlined scene, verify a corresponding section/passage exists in the draft. Heuristic: the scene's distinctive props, character names, location, or beat-summary keywords must appear in the draft text. A draft missing 30%+ of an outlined scene's distinctive markers is "missing".

**Flag:**
- Outlined scene missing from draft AND documented in `outline-deviation.md` → **WARNING**: "scene <name> moved/cut per outline-deviation.md — verify the deviation entry's plant-shift list is complete." **Route to:** DEVPLAN milestone (verify `outline-deviation.md` plant-shift list).
- Outlined scene missing from draft AND NOT documented in `outline-deviation.md` → **BLOCKING**: "SILENT CUT: outlined scene <name> is absent from the draft and has no entry in outline-deviation.md." **Route to:** PAIRED entries — (a) SMELL.md entry on the chapter classified ANCHOR-NEEDED with the suggestion "restore the scene to the draft per outline" (the prose-side restore), AND (b) DEVPLAN milestone "document the deviation retroactively in `chapters/<book>/outline-deviation.md` with plant-shift list" (the canon-side documentation). The orchestration applies fix first (canon docs the deviation), then revise restores or confirms via the SMELL.md entry.

#### P. Cross-Substrate Sensory-Echo Audit (WARNING — confirm intent)

**Load** `world/temporal-echoes.md` (specifically the §Cross-Substrate Sensory Resonances section, if present — added in Phase 112 M5h of the ground-truth project; equivalent in other projects).

**Maintain a registry** of canonical cross-substrate sensory anchors documented there. Examples (Ground Truth project): 440 Hz hum (canonical Ark per Phase 111 M3); Phrygian quarter-tone bent-third (sonic side-channel signature per Phase 112 M5e if landed).

**For each chapter draft:**
- Scan for sensory specifics that match a registered canonical anchor (number/object/signature).
- For each match, verify the echo is documented as intentional in `temporal-echoes.md §Cross-Substrate Sensory Resonances`.

**Flag:**
- Match documented as intentional → no flag (this is a planted echo working correctly).
- Match NOT documented → **WARNING**: "potential cross-substrate sensory echo at <file>:<line>: \"<quote>\". Same value/object as <canonical anchor> at <other-level>." **Route to:** PAIRED entries — (a) DEVPLAN milestone proposing a one-line addition to `world/temporal-echoes.md §Cross-Substrate Sensory Resonances` (intentional resonance — the default, since silently un-coordinated matches at the same value are statistically rare), AND (b) SMELL.md entry on the chapter classified ACCEPT with `Status: ✅ Resolved upstream by /book fix` once the addition lands. If the resonance reading is wrong (the prose value should change instead), the post-fix coherence pass will catch the residual inconsistency and write a SMELL.md INLINE entry.

NOT BLOCKING — auto-resolves via the canon-side addition.

#### Q. Redundancy-with-Adjacent-Text (NOTE)

**Heuristic check:** for each chapter draft, scan for paragraphs that repeat specific information given in the immediately preceding paragraph or system-message line. Common pattern: a Game/system-text line says "YOUR MOTHER MADE COUSCOUS LAST WEEK" and the next paragraph describes that exact couscous evening (cumin, lamb, kitchen counter) — the reader gets the same datum twice.

**Detection:** within a 3-paragraph window, if paragraph N+1 contains specific concrete details (named ingredient, named location, named object, named action) that are explicitly stated in paragraph N, AND paragraph N is a system-text / dialogue / revelation moment, flag.

**Flag every match as NOTE:** "redundancy with adjacent text at <file>:<para>: \"<quote>\". The reader receives this datum twice — consider deferring or varying the second beat (or trusting the reader to fill in)." **Route to:** SMELL.md entry on the chapter (INLINE, Severity: NOTE).

NOT BLOCKING — revise applies the trim or vary, with light authority (NOTE-level fixes are last in the apply order so other higher-severity fixes don't get pre-empted by a redundancy trim).

#### R. Context-list Orphan (WARNING)

**Symmetry rule (project side):** every file listed in a chapter's `**context:**` field has at least one beat reference (explicit `→ see <file>` OR a named entity / system / location / mechanism that semantically requires the file's content); every beat that needs a file lists that file. When beats mutate, `**context:**` mutates.

**Heuristic check (this class):** for every chapter in the active outline, parse the chapter's `**context:**` field. For each file listed (excluding the always-loaded set declared in the outline header `### Context Tags` paragraph), verify at least one beat reference exists. A beat reference is:

- An explicit `→ see <file>` or bare `<file>` mentioned in beats.
- An implicit reference: a named character (cross-ref `characters/**.md`); a named location (cross-ref `world/level-N-*/locations*.md` or `world/level-0-reality/architecture.md`); a named system / mechanism / technical anchor (cross-ref `world/**.md`); a named ration unit, compliance score, anomaly code, frequency, or hardware artifact whose canonical home is the listed file.

**Flag every file with zero beat references as WARNING:** "context-list orphan at `chapters/<book>/outline.md` Ch.NN: file `<path>` listed in `**context:**` but no beat references it. Remove from per-chapter context, OR promote to always-loaded if consistency-only, OR add a beat reference."

**Why WARNING (not BLOCKING):** the heuristic for "named entity → canonical file" is fuzzy (synonyms, common words); a fully strict rule would over-fire. Project-side review adjudicates.

#### S. Missing-context (WARNING)

**Heuristic check:** the inverse of R. For every chapter in the active outline, parse beats. For every explicit `→ see <path>` reference and every named entity / system / location / mechanism / anchor that traces to a canonical file, verify the corresponding file is in the chapter's `**context:**` (or in the always-loaded set declared in the outline header).

**Flag every beat reference whose canonical file is NOT in `**context:**` (and NOT always-loaded) as WARNING:** "context-gap at `chapters/<book>/outline.md` Ch.NN: beat references `<entity>` (canonical to `<file>`) but file not in `**context:**`. Add the file, OR promote `<entity>` to always-loaded, OR justify the omission."

**Why WARNING (not BLOCKING):** same fuzziness reason as R. The chapter-writer agent's pre-draft Step 2.6.a runs the same scan as a HARD `MUST` for chapters about to be drafted; coherence-check runs the same scan over the static outline as a routine audit, which is the right place for WARNING-level over-flagging because the user can dismiss false positives in batch.

#### Load files for R + S

Same heuristic source: the active outline's `### Context Tags` header (always-loaded list); the per-chapter `**context:**` fields; the beat blocks following each chapter heading. No additional canon files needed beyond what's already loaded for L–Q.

### 3. Output — Report to User

Display issues to the user in order of severity:

```
## BLOCKING (must fix before writing)
- [issue description] — [file:line or file1 vs file2]. **Fix:** [practical solution]

## WARNING (should fix, could cause reader confusion)
- [issue description] — [file:line]. **Fix:** [practical solution]

## NOTE (minor, fix when convenient)
- [issue description] — [file:line]. **Fix:** [practical solution]
```

### 4. Write the Corrections (MANDATORY)

**This is the critical step.** The report is analysis; the corrections are the actionable output. Without this step, findings are lost.

**Routing rule (applied to every finding):** classify the finding's primary target file BEFORE writing the milestone or entry. Per `world/canon-hierarchy.md`:

- Target file in `world/`, `plot/`, `characters/`, `chapters/<book>/outline.md`, `chapters/<book>/state.md`, or `chapters/<book>/writing-notes.md` → write a **DEVPLAN milestone** (format below).
- Target file in `chapters/<book>/ch*.md` (chapter prose) → write a **per-chapter `chapters/<book>/SMELL.md` entry** using the same format `sniff.md` uses (Quote, Category, What the reader thinks, Classification — INLINE / ANCHOR-NEEDED / ACCEPT, Suggested action) with an additional `Source: coherence` tag inside the entry. If the chapter has no SMELL.md yet, create it with the standard header. If a SMELL.md exists, append entries (do not overwrite — sniff and coherence entries coexist).
- Findings that need both canon AND prose changes → write **paired entries** in both channels, citing the pairing in each entry's body. The orchestration runs `/book fix` first (canon), then `/book revise` (prose) so the prose entry sees the corrected canon.

Create or append to `DEVPLAN.md` a new Phase with milestones for the canon-side fixes. The Phase is named `Phase NN — Coherence Fixes ([scope])`.

**Format:**

```markdown
## Phase NN — Coherence Fixes ([scope], [date])

Coherence check found X blocking / X warning / X note issues.
Fixes ordered by severity, then by file.

### M[next]: [Fix title — BLOCKING]

**File:** `[path]` (REVISIONE)

- [ ] [Specific fix instruction with enough context to execute without re-reading the report]
- [ ] [Second fix if the milestone touches the same file]

### M[next+1]: [Fix title — BLOCKING]
...

### M[next+N]: [Fix title — WARNING]
...

### M[next+N+M]: [Fix title — NOTE]
...
```

**Rules for the corrections devplan:**
- Every BLOCKING and WARNING issue MUST become a milestone. NOTEs are optional (include if the fix is quick).
- Group fixes by file when possible — one milestone per file, not one per issue.
- Each milestone's checkbox must contain enough context to execute the fix WITHOUT re-reading the full report.
- Include the file path, the section to modify, and the specific change to make.
- The devplan is appended to the existing `DEVPLAN.md`, never overwriting previous phases.
- Fix instructions for outline files: MAX 1 sentence of new content. Anything longer → cross-ref. No exceptions.
- Fix instructions that add content to project files MUST specify the EXACT text — max 2 sentences per addition. If more needed, justify why a cross-ref is insufficient.
- Fixes MUST NOT add mechanism explanations to outlines — use `→ See [canonical-file] §[section]`.
- Fixes MUST NOT add authorial reasoning ("the reader should...", "on reread...") to any file except writing-notes.md.
- Fixes MUST NOT add Nolan-constraint boxes, "MANDATORY" blocks, or meta-commentary wrappers. Write constraints as single-sentence parentheticals.
- Fixes MUST NOT add introductory framing to sections. No "This section covers..." preambles.
- Fixes that add cross-references: add to the file's `## References` footer section, not inline.
- Every fix that adds content must include: "Verify file stays within word budget (see init.md)."
- Classify each fix as SUBTRACTIVE (removes/corrects) or ADDITIVE (adds content). Max 10 additive fixes per phase. If more needed, split phases with `/book compact` between them.
- Total additions per phase: max 500 words across all fixes. Compress or defer if exceeded.
- After writing, announce: *"Coherence corrections written: X canon milestones in DEVPLAN.md, Y prose entries written to SMELL.md across N chapters. Run `/book fix <book>` then `/book revise <book>` to apply both channels."*

### 5. Summary

```
Book Coherence Check Complete
Scope: [scope]
Files reviewed: X
Issues found: X blocking / X warning / X note
Devplan milestones created: X

Strongest level: [which level has the fewest issues]
Weakest level: [which level needs the most work]
Most common issue type: [A-J category]

Next step: /book fix <book> to apply all fixes.
```

---

## Rules

- ❌ Never assume the reader has read the worldbuilding docs
- ❌ Never let "the outline says so" be sufficient — if it doesn't make sense to a reader, it doesn't work
- ❌ Never soften the assessment. This is script-doctor mode. Be spietato.
- ❌ Never skip Step 4 (the corrections devplan). The report without a devplan is useless — findings evaporate.
- ✅ For every problem, propose a PRACTICAL narrative fix — not just "this is wrong"
- ✅ Flag everything that makes you go "hmm" — better to over-flag than miss something
- ✅ Cross-reference aggressively — contradictions between files are the most common issue
- ✅ Think like a reader on a train, not like a project manager
- ✅ Cite specific passages/sections, not vague references
- ✅ The devplan is the REAL output. The report is context for the devplan.
