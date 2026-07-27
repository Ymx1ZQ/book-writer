# Book Coherence Check

Run a coherence review across the project's worldbuilding, characters, and outlines. Combines the "reader who asks obvious questions" with the rigor of a professional script doctor. Genre, tone, and structural rules are read from the project's own files — this instruction is genre-agnostic.

**Routing doctrine:** every finding written by this skill is classified by its primary target file and routed to one of three channels per `world/canon-hierarchy.md`:

- Target in `world/`, `plot/`, `characters/`, `chapters/<book>/outline.md`, `chapters/<book>/state.md`, or `chapters/<book>/writing-notes.md` → **DEVPLAN milestone** (consumed by `/book fix`).
- Target in `chapters/<book>/ch*.md` (chapter prose, file exists) → **per-chapter `chapters/<book>/SMELL.md` entry** (consumed by `/book revise`).
- Target in `chapters/<book>/ch*.md` but the file does not yet exist (chapter undrafted) → add a new keyed section `## ChNN-<short-name>` to `chapters/<book>/writing-notes.md` with the action guidance, AND a `→ See writing-notes.md §ChNN-<short-name>` pointer at the relevant beat in `chapters/<book>/outline.md`. Do NOT write to SMELL.md and do NOT create a "Pending" / "Drafting-Only" entry in DEVPLAN. Reason: SMELL.md tracks fixes against existing prose; deferred-by-design instructions for future writer passes belong in context, not in fix-tracking.

A single finding may produce paired entries in BOTH channels when the contradiction needs canon AND prose updates (the orchestration scripts run `fix` and `revise` in sequence so both close in the same cycle). Without the prose channel, prose-target milestones written to DEVPLAN would never be applied — `/book fix` does not touch chapter prose by design.

**Autonomous decision + no-Pending entries:** see `instructions/milestone-format.md` §What never enters DEVPLAN and §Autonomous-decision principle. Triage NEVER produces "user picks", "needs design decision", or "deferred-only" buckets — the system commits a default per the four-tier order (canon-hierarchy → existing canon → chapter guards → Occam) and records the rationale.

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

**Do NOT load everything at once.** Load only what each check category needs, just before running that category; the rest is context spent on files the check never reads.

**Load upfront (orientation for all checks):**
- `world/overview.md` — narrative levels, central themes, structural rules
- `chapters/book-N/outline.md` — the relevant outline(s) for scope
- `chapters/book-N/opening-strategy.md` — if it exists

**Load per category:**

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
| J — Chekhov | `plot/prestige-inventory.md` (if exists), `plot/motif-tracking.md` (if exists), ALL outlines across all books — including each outline header's §Inline Plant Tracking table — and every canon file holding a `## Usage Tracker` section (`grep -rl "## Usage Tracker" characters/ world/ plot/`). The last two are the other two registers this check reconciles (→ `instructions/registers.md`) |
| K — Context Tags & Trackers | Every canon file holding a `## Usage Tracker` section (`grep -rl "## Usage Tracker" characters/ world/ plot/` — every directory, level directories included: their rows are resolved by rule, not skipped), all files referenced in `context:` tags across outlines, and each book's outline header §Context Tags (always-loaded set + texture-palette proxy) |
| L — Economic-Anchor Audit | The level-appropriate anchor file for each chapter draft in scope: Reality → `world/level-0-reality/economy.md` (+ `consumer-anchors.md` if present); Ark → `world/level-1-ark/daily-life.md` §Economy; Dome → `world/level-2-dome/bureaucracy.md` §Allocation Mathematics + `context.md` §Economy and Distribution; cross-level → `world/economy-cross-level.md` (if present). Load chapter drafts (`chapters/book-N/ch*.md`). |
| M — System-Implying-Number Audit | Re-use level files already loaded for L and E; load `world/level-0-reality/surveillance.md`, `world/level-0-reality/agent-capabilities.md`, `world/the-authors-method.md` if present; load chapter drafts. |
| N — Interior-Labeling Detector | Chapter drafts only (re-use those loaded for G); reference `world/prose-rules.md` if not already loaded. |
| O — Outline-to-Draft Coverage | Outlines already loaded for the scope; chapter drafts (re-use); `chapters/book-N/outline-deviation.md` if present (written by chapter-writer Step 2.5.d when scenes are cut/split/merged). |
| P — Cross-Substrate Sensory-Echo | `world/temporal-echoes.md` already loaded for A, §Cross-Substrate Sensory Resonances if present; chapter drafts (re-use). |
| Q — Redundancy-with-Adjacent-Text | Chapter drafts only (re-use). |
| T — First-Appearance Delivery | Re-use character sheets from D and chapter drafts from G/L. |
| U — Single Ownership | The project's Concept → Canonical file table (`CLAUDE.md` §Information Architecture or whatever its own file names), plus the frontmatter of every file that table lists. Read the slug list from the project — never carry a copy here. |

**For scope `characters`:** load only rows D and skip all others.
**For scope `world`:** load only rows A, E, H, L (anchor files only), and skip character/outline/draft checks.
**For scope `book-N`:** load outlines upfront for that book only; load ALL books' outlines only for check J. Checks L–Q and T only run if chapter drafts exist for the scope.

**Check U is corpus-wide and runs on every scope, including `characters` and `world`.** Ownership is a property of the whole canon set: a scoped run would compare a file against only some of its rivals and report clean while the duplicate sits in the skipped directory.

**Graph-assisted load (optional — see `instructions/graph-recall.md`):** if `graphify-out/graph.json` exists in the project root AND the freshness gate passes (answer mode per `graph-recall.md` §Freshness gate), the relational checks replace their bulk loads:

| Check | Graph-fresh path (replaces that check's load-table row) |
|---|---|
| J — Chekhov | `graphify query "every prestige-inventory plant and its payoff chapter"` + `graphify explain "<plant>"` on each plant the query returns with no payoff edge. Replaces loading ALL outlines across all books. Classification rules in check J apply to the query output unchanged. The §Inline Plant Tracking tables and the tracker rows are read from disk regardless — the register reconciliation compares the registers as written, so neither source may be substituted by a query result. |
| K — Context Tags & Trackers | The tracker-assignment query (`graphify query "usage-tracker items assigned to <book> ch<NN>"`, per chapter in scope); open ONLY the files the graph names. Replaces loading all `world/level-*-<name>/` files. |
| B / C / D | Graph triage first — query for threads introduced and never resolved (B), knowledge routes across levels (C), character-trait contradictions (D) — then open plot files / character sheets only on flagged hits. |

Checks E, L, M consume verbatim numeric values (never-substitute list per `graph-recall.md`) — their load rows are unchanged. Graph absent or stale → the load table above applies unchanged.

### 2. Check Categories (21 checks)

For every issue found: **cite the specific file and section**, and **propose a practical fix**.

---

#### A. Cross-Level Architecture
Analyze the relationship between the project's narrative levels (read from `world/overview.md`) — a multi-level narrative, not a multi-timeline one, but the same rules apply:
- Do actions in one level have **logical, consistent consequences** in the connected levels?
- Where the project uses cross-level echoes or causal links: is the echo specific enough for the reader to notice?
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
- Pay special attention to cross-level knowledge: does a character in one level know something that only a reader of another level's chapters would know?

#### D. Character Consistency
- For each protagonist's major decision: is it consistent with their established personality, background, and trauma?
- Flag any character who acts **"out of character" to serve the plot** — they do something only because the story needs them to, not because they would.
- Check character arcs: does each protagonist change in a way that follows from what happened to them? Is the change gradual or abrupt?
- Verify character naming conventions match the rules defined in their character sheets.

#### E. Worldbuilding & Technology Consistency
Primary reference: `world/technology-comparison.md` or the project's equivalent for the per-level rules, its worldbuilding files for the level progression.
- Does technology respect the established rules per level?
- Is there a **coherent evolution** between levels?
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
- Do all levels explore the **central themes** consistently? (themes read from `world/overview.md` or `CLAUDE.md`)
- Is the **emotional stake** clear in each level? (stakes read from the project's world files)
- Do the levels **comment on each other thematically** — testing the same question from different angles?
- Flag any level or arc that feels **thematically disconnected** from the others.

#### I. Reader Experience & Investment
- "Is this boring?" — Flag sections that are mostly exposition without action/tension.
- "Does the reader have a reason to care about this character?" — Flag characters who appear without emotional setup.
- "Would a reader continue reading after this chapter?" — Check every chapter ending for forward momentum.
- "Does this make sense to someone who HASN'T read the worldbuilding docs?" — The docs don't ship with the book.
- "Where would a reader on a train put the book down?" — Flag those moments.

#### J. Chekhov's Inventory

##### Multi-book awareness

When scope is a single book, this check MUST still load the outlines of ALL books (`chapters/book-*/outline.md`) plus all files in `plot/`. The scoped book is the **focus** — you audit its plants in detail — but payoffs can land in ANY book of the series. (Graph-fresh path: per §1, the plant/payoff query replaces the all-books outline load.)

Classification rules:
- A plant in Book N with payoff in Book N → normal plant/payoff. Check it.
- A plant in Book N with payoff in a later book → **cross-book plant**. Tag as `✅ CROSS-BOOK: planted B{N}, payoff B{M}`. NOT an orphan.
- A plant in Book N with NO payoff in ANY book → **orphan**. Flag it.
- A payoff in Book N with NO plant in any earlier book → **missing plant / retroactive plant**. Flag it.

##### Inventory categories

- **Plants:** Things introduced early that pay off later (a name dropped in passing, recurring objects, specific character details). Is every plant paid off within the series? Is any payoff missing its plant?
- **Cross-book plants:** payoff lands in a later book. List each with its source book and payoff book. NOT orphans — flag only if the payoff is missing from ALL books.
- **Promises:** Things the narrative promises to the reader (a mystery, a threat, a character's growth). Is every promise kept by the end of the series?
- **Orphans:** Things introduced and abandoned — characters, objects, questions, subplots — with no payoff in ANY book.
- **Retroactive plants:** Things that appear in a later book and SHOULD have been planted in an earlier one.

##### Register reconciliation (plant table ↔ Usage Trackers)

A recurrence is recorded in the outline header's §Inline Plant Tracking table and in the owning canon file's `## Usage Tracker`, written at different times by different commands (→ `instructions/registers.md`). Reconcile both directions:

- An element whose tracker rows span **three or more chapters** is a recurrence the reader is expected to accumulate, so it needs a §Inline Plant Tracking row. Missing → WARNING: "element tracked at Ch.NN/NN/NN with no plant row." **Route to:** DEVPLAN milestone adding the row to `chapters/<book>/outline.md` §Inline Plant Tracking.
- A plant-table instance at Ch.N whose element has **no tracker row for Ch.N** is an instance nothing owns: no file carries the obligation, so `/book chapter` 2.6.c cannot collect it, Step 5.5 has nothing to tick, and Step 1's selective pass never opens the file when the element lives in the chapter's own level directory. WARNING → DEVPLAN milestone adding the row to the file that owns the element.
- A payoff instance whose **enabling element has no row of its own** in either register is the retroactive-plant class above, reached from the register side rather than the prose side. Flag it as a retroactive plant, naming which register is empty.

##### Instance count and gap

- A payoff with **fewer than two prior instances** → WARNING: "payoff at Ch.N rests on <count> prior instance(s)."
- **Derive the gap bound from the project's own table; do not decree a number.** For every plant row *other than the one under test*, compute the consecutive gaps between numbered instances (the chapter distance from `#k` to `#k+1`) and take the maximum — the gap this book's working plants demonstrably sustain. A gap in the row under test that exceeds it → WARNING: "gap of N chapters between #k and #k+1 exceeds the book's observed maximum of M (`<other plant>`, #j→#j+1)." A single-instance element whose payoff sits N chapters later is measured the same way, instance-to-payoff. If no other row has two numbered instances, no bound can be derived: report that and skip the gap test rather than substituting a figure.
- **The remedy is instances, not a better sentence.** Both flags route to a DEVPLAN milestone adding intermediate instances at named chapters (a plant-table cell each, plus the matching tracker row and outline beat). Rewriting the single mention closes neither finding: the deficit is how many times the reader meets the element, not the wording of one meeting.

#### K. Context Tag & Usage Tracker Audit

(Graph-fresh path: per §1, the tracker-assignment query replaces the bulk load; the audit rules below are unchanged.)

**Context tags:**
- For each chapter in scope, verify a `context:` field exists in the chapter header. If a chapter mentions a temporal echo, flashback, thematic concept, or countdown beat but lacks the corresponding file in its `context:` tag, flag as WARNING.
- For each file listed in any chapter's `context:` tags, verify it has a `## Usage Tracker` section. If a file contains discrete consumable details but lacks a tracker, flag as WARNING: "context file without tracker."

**World file trackers (table format — Book/Ch/Detail/Status):**
- Verify all world files in `world/level-*-<name>/` directories have a `## Usage Tracker` section. Flag missing trackers as WARNING.
- For every tracker row naming a target chapter, in every file and every directory: the row is valid only if its owning file is reachable from that chapter through one of the four routes of the reachability set (→ `instructions/registers.md`) — the chapter's `**context:**` list, the book's always-loaded set, its texture-palette proxy, or the chapter's own `world/level-*-<name>/` directory, which `/book chapter` Step 1 opens selectively from the rows themselves — a row there is reachable by rule, needs no `context:` entry, and is not flagged.
- Every other unreachable row → WARNING: "tracker row mapped to <book> Ch.NN but the owning file is not reachable from that chapter." No rule reaches `world/` root files, `plot/` or `characters/`, so a row in one of those is unreachable from every chapter until that chapter's `context:` names it — run this over the whole tracker set, not only the level directories.
- If the row's owning file sits in a *different* level's directory, report the register conflict instead of the WARNING: that file is reachable by no route, so the row targets the wrong chapter or the content is filed in the wrong file. The register outranks the tracker and the fix is a content move or a retarget, never a `context:` entry.
- Flag a `context:` entry only when the file has NEITHER a tracker row for that chapter NOR a beat that references it — the two independent justifications `/book chapter` 2.6.a and 2.6.c enforce. Exclusions come from this book's outline header §Context Tags (always-loaded set + texture-palette proxy), parsed at run time — never from a list hardcoded in this file. Report zero-justification entries once, under check R.
- Flag any world file where >50% of elements have no chapter assigned (`—` status) as NOTE: "worldbuilding without placement plan."

**Character file trackers (same table format):**
- Verify all character files in scope have a `## Usage Tracker` section with the standard table format (Book/Ch/Detail/Status).
- Flag character files still using the old checkbox format as NOTE: "character tracker needs migration to table format."

#### L. Economic-Anchor Audit (BLOCKING for unanchored monetary detail)

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

**For each match:** verify the figure traces to the level-appropriate anchor file, as either (a) a direct anchor citation (the value matches a published number there), or (b) a value within the documented range/scarcity-premium band the anchor states.

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

**For each match:** verify a canonical worldbuilding file documents the system implied. If the chapter says "filtration alert tier two", a tier system MUST exist in `ecology.md` or similar; "drone corridor 042" needs a corridor numbering schema in `surveillance.md` or similar.

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

NOT BLOCKING — advisory; revise applies them flagged `Severity: NOTE` so a downstream pass can deprioritize.

#### O. Outline-to-Draft Coverage (WARNING; BLOCKING if undocumented)

**For each chapter draft in scope:**
- Read the outline entry for the chapter (use the per-chapter targeted load — locate `## Ch. NN` header, read to next chapter header).
- Enumerate the outlined scenes (each `### N.` or numbered beat block).
- For each outlined scene, verify a corresponding section/passage exists in the draft. Heuristic: the scene's distinctive props, character names, location, or beat-summary keywords must appear in the draft text. A draft missing 30%+ of an outlined scene's distinctive markers is "missing".

**Flag:**
- Outlined scene missing from draft AND documented in `outline-deviation.md` → **WARNING**: "scene <name> moved/cut per outline-deviation.md — verify the deviation entry's plant-shift list is complete." **Route to:** DEVPLAN milestone (verify `outline-deviation.md` plant-shift list).
- Outlined scene missing from draft AND NOT documented in `outline-deviation.md` → **BLOCKING**: "SILENT CUT: outlined scene <name> is absent from the draft and has no entry in outline-deviation.md." **Route to:** PAIRED entries — (a) SMELL.md entry on the chapter classified ANCHOR-NEEDED with the suggestion "restore the scene to the draft per outline" (the prose-side restore), AND (b) DEVPLAN milestone "document the deviation retroactively in `chapters/<book>/outline-deviation.md` with plant-shift list" (the canon-side documentation). The orchestration applies fix first (canon docs the deviation), then revise restores or confirms via the SMELL.md entry.

#### P. Cross-Substrate Sensory-Echo Audit (WARNING — confirm intent)

**Maintain a registry** of the canonical cross-substrate sensory anchors documented in `world/temporal-echoes.md` §Cross-Substrate Sensory Resonances (or the project's equivalent). Examples (Ground Truth): 440 Hz hum, canonical Ark; Phrygian quarter-tone bent-third, sonic side-channel signature.

**For each chapter draft:**
- Scan for sensory specifics that match a registered canonical anchor (number/object/signature).
- For each match, verify the echo is documented as intentional in `temporal-echoes.md §Cross-Substrate Sensory Resonances`.

**Flag:**
- Match documented as intentional → no flag (this is a planted echo working correctly).
- Match NOT documented → **WARNING**: "potential cross-substrate sensory echo at <file>:<line>: \"<quote>\". Same value/object as <canonical anchor> at <other-level>." **Route to:** PAIRED entries — (a) DEVPLAN milestone proposing a one-line addition to `world/temporal-echoes.md §Cross-Substrate Sensory Resonances` (intentional resonance is the default: uncoordinated matches at the same value are statistically rare), AND (b) SMELL.md entry on the chapter classified ACCEPT with `Status: ✅ Resolved upstream by /book fix` once the addition lands. If the resonance reading is wrong (the prose value should change instead), the post-fix coherence pass will catch the residual inconsistency and write a SMELL.md INLINE entry.

NOT BLOCKING — auto-resolves via the canon-side addition.

#### Q. Redundancy-with-Adjacent-Text (NOTE)

**Heuristic check:** for each chapter draft, scan for paragraphs that repeat specific information given in the immediately preceding paragraph or system-message line. Common pattern: a Game/system-text line says "YOUR MOTHER MADE COUSCOUS LAST WEEK" and the next paragraph describes that exact evening — the reader gets the same datum twice.

**Detection:** within a 3-paragraph window, if paragraph N+1 contains specific concrete details (named ingredient, named location, named object, named action) that are explicitly stated in paragraph N, AND paragraph N is a system-text / dialogue / revelation moment, flag.

**Flag every match as NOTE:** "redundancy with adjacent text at <file>:<para>: \"<quote>\". The reader receives this datum twice — consider deferring or varying the second beat (or trusting the reader to fill in)." **Route to:** SMELL.md entry on the chapter (INLINE, Severity: NOTE).

NOT BLOCKING — revise applies the trim or vary with light authority: NOTE-level fixes are last in the apply order, so a redundancy trim never pre-empts a higher-severity fix.

#### R. Context-list Orphan (WARNING)

**Symmetry rule (project side):** every file listed in a chapter's `**context:**` field has at least one beat reference (defined below); every beat that needs a file lists that file. When beats mutate, `**context:**` mutates.

**Heuristic check (this class):** for every chapter in the active outline, parse the chapter's `**context:**` field. For each file listed (excluding the always-loaded set and the texture-palette proxy declared in the outline header `### Context Tags` paragraphs), verify at least one beat reference exists **or** a `## Usage Tracker` row mapped to that chapter — a file listed for a tracker row is justified even with no beat, and `/book chapter` 2.6.c re-adds it on the next draft if it is removed. The one exception is a file in the chapter's own level directory: Step 1 reaches it by rule, so the entry is redundant rather than orphaned. Neither case is flagged. A beat reference is:

- An explicit `→ see <file>` or bare `<file>` mentioned in beats.
- An implicit reference: a named character (cross-ref `characters/**.md`); a named location (cross-ref `world/level-N-*/locations*.md` or `world/level-0-reality/architecture.md`); a named system / mechanism / technical anchor (cross-ref `world/**.md`); a named ration unit, compliance score, anomaly code, frequency, or hardware artifact whose canonical home is the listed file.

**Flag every file with zero justifications as WARNING:** "context-list orphan at `chapters/<book>/outline.md` Ch.NN: file `<path>` listed in `**context:**` but no beat references it and no tracker row maps to this chapter. Remove from per-chapter context, OR promote to always-loaded if consistency-only, OR add a beat reference."

**Why WARNING (not BLOCKING):** the heuristic for "named entity → canonical file" is fuzzy (synonyms, common words), so a strict rule would over-fire. Project-side review adjudicates.

#### S. Missing-context (WARNING)

**Heuristic check:** the inverse of R. For every chapter in the active outline, parse beats. For every explicit `→ see <path>` reference and every named entity / system / location / mechanism / anchor that traces to a canonical file, verify the corresponding file is reachable from the chapter through one of the four routes of the reachability set (→ `instructions/registers.md`, enumerated under check K; the same exclusion `/book chapter` 2.6.a applies via Step 1 and 2.6.e).

**Flag every beat reference whose canonical file is reachable through none of the four routes as WARNING:** "context-gap at `chapters/<book>/outline.md` Ch.NN: beat references `<entity>` (canonical to `<file>`) but file not in `**context:**`. Add the file, OR promote `<entity>` to always-loaded, OR justify the omission."

**Why WARNING (not BLOCKING):** same fuzziness as R. The chapter-writer's pre-draft Step 2.6.a runs this scan as a HARD `MUST` for chapters about to be drafted; here it is a routine audit over the static outline, where over-flagging is affordable because the user dismisses false positives in batch.

#### Load files for R + S

Same heuristic source: the active outline's `### Context Tags` header (always-loaded list); the per-chapter `**context:**` fields; the beat blocks following each chapter heading. No additional canon files needed beyond what's already loaded for L–Q.

#### T. First-Appearance Delivery (WARNING)

Checks D and I verify that a character is *consistent* and *cared about*; neither verifies that the introduction chapter *delivers* the premises the rest of the story leans on. A chapter can be fully canon-consistent and still omit a load-bearing trait, leaving a later payoff standing on nothing. (Ground Truth: ch01 never established Noah as a lifelong player of the Game, which `world/level-0-reality/the-game.md` §Master Key Primitive depends on; the coherence pass asked "does canon support decades of play?", confirmed the canon, concluded "no problem" — the wrong layer.)

**Runs only when chapter drafts exist for the scope.**

**For each chapter draft that is a character's first POV chapter, or a major character's first substantial on-page appearance:**
- Load the character sheet (`characters/foreground/` or `characters/midground/` — reuse those loaded for Check D).
- From the sheet, identify the **3-5 load-bearing premises**: the role line, the central wound / arc engine, the defining physical or situational facts (disability, where and how they live, occupation), and the relationships the plot actively uses. Load-bearing = a later chapter, a planted payoff, or a canonical mechanism *depends* on the reader knowing it.
- For each premise, verify the chapter renders it **on-page** — through action, dialogue, or sensory experience. It need not be stated outright, but it must be inferable from the page by a reader who has only the book.

**Flag** each load-bearing premise absent from its character's introduction chapter as **WARNING**: "establishment gap at `chapters/<book>/chNN.md`: <character>'s introduction does not deliver <premise> (canon: `<file>`). A reader finishes the chapter without it." **Route to:** SMELL.md entry on the chapter — INLINE if a line or two can carry the premise, ANCHOR-NEEDED if it needs a new beat.

This is delivery, not contradiction — WARNING, not BLOCKING. Escalate in triage if a documented later plant or reveal depends on the missing premise.

#### U. Single Ownership (WARNING)

Every check above compares two statements of a fact and asks whether they agree. This one asks why there are two. A project that states an information architecture — one canonical file per concept, everything else cross-referencing with `→ see <file> §<section>` — and then verifies nothing accretes a second explanation in a neighbouring file, which drifts. Found by hand in `ground-truth` on 2026-07-27: a simulation tell with two different mechanisms across three files; a forbidden causal link restated in three files including the one that owns the topic; one rule carried by three line citations, one of which pointed at a blank line. None of the twenty checks above could have found any of them — each was internally consistent in the file it sat in.

**Read the slug list from the consuming project, never from here.** The project's `CLAUDE.md` (or the file its own §Information Architecture names) carries a Concept → Canonical file table; each canonical file declares `owns: [<slug>, ...]` in its frontmatter. Adding a row to that table must change what this check reports, with no edit to this instruction — otherwise the check grows the second source of truth it exists to prevent.

**For each slug:**
- More than one file claims it in `owns:` → **WARNING**: "concept `<slug>` claimed by `<file A>` and `<file B>`; one of them is the canonical owner and the other cross-references it." **Route to:** DEVPLAN milestone.
- No file claims it → **WARNING**: "concept `<slug>` is named in the Concept → Canonical file table and no file declares it." **Route to:** DEVPLAN milestone adding the frontmatter.
- A file that does *not* own the slug **explains** the concept rather than pointing at its owner — a mechanism restated, a value re-derived, a rule re-stated in its own words — → **WARNING**: "`<file>` explains `<slug>`, owned by `<owner>`; replace the explanation with `→ see <owner> §<section>`." A passing mention, a name used in a sentence, or a `→ see` line is not an explanation.

**Why WARNING, not BLOCKING** — the same grounds as a register CONFLICT: resolving a duplicate means deciding which file keeps the content and moving it, a judgment about the corpus rather than a repair the pipeline can apply. Blocking here would stop a write cycle on a question no automatic fix can answer.

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

The report is analysis; the corrections are the actionable output. Without this step, findings are lost.

**Routing rule (applied to every finding):** classify the finding's primary target file BEFORE writing the milestone or entry, and route it to one of the three channels of §Routing doctrine above — canon target → **DEVPLAN milestone** (format below); existing chapter prose → **`chapters/<book>/SMELL.md` entry**; undrafted chapter → keyed section in `chapters/<book>/writing-notes.md`.

- A SMELL.md entry uses the same format `sniff.md` uses (Quote, Category, What the reader thinks, Classification — INLINE / ANCHOR-NEEDED / ACCEPT, Suggested action) with an additional `Source: coherence` tag inside the entry. If the chapter has no SMELL.md yet, create it with the standard header. If a SMELL.md exists, append entries (do not overwrite — sniff and coherence entries coexist).
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
- Each milestone's checkbox must contain enough context to execute the fix WITHOUT re-reading the full report: the file path, the section to modify, and the specific change to make.
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
- The `### Verification & next steps` block (if written) follows `instructions/milestone-format.md` §Verification & next-steps blocks: per-phase scope only, no restatement of prior phases' pending status, no transitive forward-looking unblock claims, allowed/banned command-reference list per rule 2.
- After writing, announce: *"Coherence corrections written: X canon milestones in DEVPLAN.md, Y prose entries written to SMELL.md across N chapters. Run `/book fix <book>` then `/book revise <book>` to apply both channels."*

### 4.5 Close Matching Operational Items

**Triggers when this `/book coherence <scope>` invocation produces 0 BLOCKING / 0 WARNING / 0 NOTE actionable findings**: the run has itself verified that scope `<scope>` is coherence-clean, so any operational item naming `/book coherence <scope>` as pending elsewhere in DEVPLAN.md can be closed. Per `instructions/milestone-format.md` §Verification & next-steps blocks rule 3.

If findings are non-zero, skip §4.5 — convergence has not been re-verified.

If 0/0/0:

Scan DEVPLAN.md for plain-bullet operational items in any phase whose action names this invocation. Match patterns (scope-aware):
- `Re-run .*/book coherence <scope>` (verification re-run — the canonical phrasing)
- `Then .*/book coherence <scope>` / `After .* /book coherence <scope>` (phasing-language phrasings)
- For invocations with `<scope>=all`: also match per-book scopes (`/book coherence book-1`, `/book coherence book-2`, `/book coherence book-3`, `/book coherence common`) since `all` is the union.

For each match with status `— pending`, update to `— done YYYY-MM-DD` (today's date). Skip matches already marked `— done`. Do NOT touch operational items referencing other commands — those close from their own consumers (`/book fix` §2.5, `/book continuity` §4.5, `/book compact` §5.5).

Announce in the summary:
```
Operational items closed: X (in phases: [list])
```

### 5. Summary

```
Book Coherence Check Complete
Scope: [scope]
Files reviewed: X
Issues found: X blocking / X warning / X note
Devplan milestones created: X

Strongest level: [which level has the fewest issues]
Weakest level: [which level needs the most work]
Most common issue type: [A-U category]

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
