# `/book fidelity` — planned-vs-rendered check

Compare a chapter's outline entry (the plan of record) against the chapter prose (what was actually rendered), with `chapters/<book>/outline-deviation.md` as the ledger of legitimate differences between them. Catch the class of defect where plan and prose silently diverge: a planned beat that never made the page, a rendered beat nobody planned, a ledger entry that no longer describes the prose it ratified, a tracker row marked `written` for an element the prose does not contain, a plant instance the book's plant table assigned to this chapter and the prose skipped.

The skill already has the **write-time half** of this contract: `chapter-writer.md` Step 2.5.d (the outline-deviation contract) and Step 7 item 8 (the writer's own silent-cut self-check). Fidelity is that self-check's **independent post-hoc verifier** — per the canon-hierarchy doctrine that no single skill validates its own output, the writer's word that the contract was respected is never the last word. Fidelity re-derives the comparison from scratch, assuming nothing about whether Step 7 ran or ran honestly.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Write-time silent-cut self-check (the writer verifying its own contract) | `chapter-writer.md` Step 7 item 8 |
| The deviation contract itself (update outline, append ledger entry) | `chapter-writer.md` Step 2.5.d |
| Plant → payoff bookkeeping across the whole book | `coherence-check.md` §Chekhov |
| Motif semantic charge across chapters | `motif.md` |
| Cross-chapter shape / voice / irony across a window | `adjacency.md` |
| Craft judgment of the rendered prose | `reviewer.md` |
| **"Did the prose render what the outline planned? Is everything substantive in the prose either planned or ledgered? Does the ledger still describe the prose? Is every `written` tracker mark true of the prose? Did this chapter's plant instances land?"** | **THIS check** |

The three registers a chapter is judged against — Usage Tracker, `context:` list, §Inline Plant Tracking — are defined in `instructions/registers.md`; classes (d) and (e) below read the first and third.

**Milestone format:** see `instructions/milestone-format.md`. Two-channel routing (`world/canon-hierarchy.md` convention, as `motif.md`/`factcheck.md` already apply it): prose-side findings → `SMELL.md` (`Source: fidelity`, consumed by `/book revise`); outline-, ledger- and tracker-side findings (including a false `written` mark to revert) → `DEVPLAN.md` milestones (consumed by `/book fix`).

## Usage

```
/book fidelity <book> <chNN>
```

- `<book>` — book directory under `chapters/`.
- `<chNN>` — the chapter to check.

## Inputs (read all before judging)

1. The chapter's § of `chapters/<book>/outline.md`, **verbatim** (header to next chapter header) — every beat, plant assignment, motif assignment, cliffhanger. This is the plan of record.
2. The chapter prose `chapters/<book>/<chNN>.md`, **verbatim**.
3. `chapters/<book>/outline-deviation.md` **if it exists** — the append-only legitimate-deviations ledger (per the `chapter-writer.md` Step 2.5.d contract). It may not exist: the file is created only when a deviation is first logged, so absence means "no deviations ever ratified", not an error.
4. Every canon file holding a `## Usage Tracker` row for this Book+Ch — collected the way `chapter-writer.md` 2.6.c collects them (`grep -rlF "| B<N> | <NN> |" characters/ world/ plot/`, span rows like `B1 | 01-30` ignored), NOT restricted to the chapter's `context:` list — 2.6.c's collection step only: its own-level-directory exemption governs auto-add, never what fidelity reads. Class (d) only; the rows' Status column is the claim under test.
5. The book outline header's §Inline Plant Tracking table — this chapter's column, every non-`—` cell, with its instance number and payoff marking. Class (e) only.

**Graph triage (optional — see `instructions/graph-recall.md` for gating):** only when `graphify-out/graph.json` exists AND the freshness gate passes, run a cheap planned-vs-rendered diff BEFORE the verbatim reads, against the chapter's node pair — planned node `chapters_book_N_outline_chNN`, rendered node `chapters_book_N_chNN`:

```bash
graphify query "chapters_book_N_outline_chNN — planned beats, plants, cliffhanger" --budget 4000
graphify query "chapters_book_N_chNN — beats, plants, cliffhanger actually rendered" --budget 4000
```

Both queries pass `--budget 4000`: per-chapter node detail sits deep in the traversal output and the default 2000-token cap truncates it (project-side Phase 80 M5 re-extraction finding). The pair diff yields a **candidate list** that prioritizes the verbatim comparison — it never replaces it: findings are asserted only from the verbatim reads (the disk text is the truth). Graph absent, stale, or either node missing → skip triage; the check runs **identically** on file reads alone (an empty query result is never evidence of absence, per `instructions/graph-recall.md` fallback ladder).

## The five finding classes

### (a) Planned-not-rendered (silent cut)

An outline beat, plant assignment, cliffhanger, or motif assignment absent from the prose AND absent from `outline-deviation.md`. This is the writer's silent-cut class (Step 2.5.d violation), verified independently.

Per `instructions/milestone-format.md` §Autonomous-decision principle, the check commits ONE resolution per finding:

- **Default — render it (prose-side).** The outline is the plan of record; the missing element enters `SMELL.md` with a concrete weave suggestion. `Flagging: TRADE-OFF` when the weave adds substantive prose (revise surfaces it to `SMELL-PENDING.md`); `SAFE-CUT`/INLINE only for a mechanical one-line element (a plant mention, a named object) whose insertion point is unambiguous.
- **Exception — ratify the cut (ledger-side).** Only when the prose demonstrably fulfills the beat's function another way (the plant lands via a different vehicle, the cliffhanger promise is kept by a different beat): route a `DEVPLAN.md` milestone for `/book fix` to append the retroactive `outline-deviation.md` entry and outline annotation (`[moved to chXX]` / cut marker), mirroring Step 7's own retroactive procedure. Any plant left without a destination chapter is named as **orphaned** in the milestone.

### (b) Rendered-not-planned

A substantive prose beat with no outline basis and no deviation entry. Two legitimate resolutions exist — **ratify** (a retroactive `outline-deviation.md` entry + outline annotation) or **trim** (cut/compress the prose beat) — and this check **NEVER auto-decides which**. The finding is one `SMELL.md` entry, `Flagging: TRADE-OFF` (never SAFE-CUT), whose `Suggested action` names BOTH resolutions; revise surfaces TRADE-OFF entries to `SMELL-PENDING.md` and `/book arbiter` (or the user) adjudicates. If the adjudication is "ratify", the resolution converts to a `DEVPLAN.md` milestone for `/book fix` (ledger-side); if "trim", it is applied as a prose edit.

### (c) Deviation-ledger drift

An `outline-deviation.md` entry that no longer matches the prose it describes: the entry says a scene moved to ch07 but ch07's prose never received it; a plant's recorded destination disagrees with where the prose actually planted it; a ledgered cut was later restored without a new entry. The ledger is append-only, so the fix is a **corrective append** (plus any outline-annotation update) — never a rewrite of ledger history. Ledger-side → `DEVPLAN.md` milestone consumed by `/book fix`. If the drift exposes a plant with no valid destination, name it as orphaned.

**Acknowledged rule (load-bearing):** entries already recorded in `outline-deviation.md` are ACKNOWLEDGED. A beat cut-and-ledgered is legitimate — never re-flagged as (a); a beat added-and-ledgered is legitimate — never re-flagged as (b). The ledger is the contract instrument; fidelity verifies against it, it does not second-guess ratified deviations. Only class (c) touches an existing entry, and only when the entry no longer describes the prose. The ledger does not reach class (d): a ratified deviation explains why a beat is absent, it never makes a `written` tracker mark true.

### (d) Marked-written-not-rendered

A `## Usage Tracker` row for this Book+Ch whose Status reads `written` while the element is absent from the prose. `chapter-writer.md` Step 5.5 sets `planned` → `written` and no later step ever re-reads the mark, so this is the first and only verification the forward direction gets. Measured baseline on the one chapter audited exhaustively: 17% of its 12 marks false, 33% counting partials; 21 false marks across the book.

For each `written` row, locate the element in the prose and apply the **channel test**: the mark is true only when the prose renders the element in the channel the row names. Coolant promised as *smell and memory* is not delivered by burn and stain — the object is present, the named channel is not. A row whose Detail column says `scene` is not satisfied by a one-clause accent.

- **Absent** → tracker-side: a `DEVPLAN.md` milestone for `/book fix` reverting that row to `planned`, naming file, row text and chapter. Add a `SMELL.md` entry as well only when the element is one this chapter should carry (then classes (a)'s routing rules apply to the weave).
- **Partial** (right object, wrong channel or weight) → one `SMELL.md` entry, `Flagging: TRADE-OFF`, whose suggested action names both resolutions: complete the channel in prose, or revert the row to `planned`. Never auto-decided.

A row still `planned` is not a class (d) finding — under-ticking is bookkeeping noise, over-ticking is a false claim that canon reached the page. Tracker rows are per-element; do not re-flag as (d) an element already flagged as (a) from the outline side — reference the (a) entry instead.

### (e) Plant-instance-not-rendered

A §Inline Plant Tracking cell assigning an instance to this chapter whose element is absent from the prose. The plant table is a separate register from the outline beats (`instructions/registers.md`): an instance can be assigned in the table and mentioned in no beat, so class (a) does not reach it. Apply the same channel test as (d) — the cell names how the instance appears, and a different vehicle is not that instance.

- **Default — render it (prose-side).** `SMELL.md`, `Flagging: TRADE-OFF` when the instance needs a substantive beat, `SAFE-CUT`/INLINE when the cell describes a one-line appearance with an unambiguous insertion point.
- **Exception — move the instance (table-side).** Only when the prose plants the element at a different point in the chapter or the deviation ledger already moved the scene: a `DEVPLAN.md` milestone for `/book fix` renumbering the row's cells so the instances stay consecutive.

A missing instance on a plant whose payoff has already been drafted is named as a **broken payoff** in the story-debt line, not merely an unrendered detail. Do not double-report: if the same element is already flagged as (a) from an outline beat or as (d) from a tracker row, reference that entry instead.

## Flagging discipline (per `reviewer.md` conventions)

Signal, not coverage — **substantive beats only, never line-level wording.** The outline compresses; the prose expands. What is NOT a finding: expansion of a planned beat (texture, dialogue growth, micro-beats inside a planned scene, sensory detail), reordering within a scene that breaks no planted dependency, outline directive language ("compress", "one line") treated as a checklist. What IS substantive for class (b): a new scene or location, a new character appearance, a new plant or reveal, a capability/knowledge change, any beat a later chapter could depend on.

Every finding must name the concrete **story debt**: an orphaned plant, an unprepared payoff chapter, a broken cliffhanger promise, an unratified fact that entered canon. If you cannot name what breaks downstream (or what un-planned fact the prose canonized), it is not a finding. Cost asymmetry per `reviewer.md`: a false flag spends the writer's rendering latitude; the default verdict is clean.

## Output — SMELL.md entries

Standard SMELL.md format with `Source: fidelity` and a `Class:` field:

```markdown
## #N — <one-line, e.g. "ch04: outline plant 'ledger stamp' never rendered — no deviation entry">

- **Source:** fidelity
- **Class:** (a) planned-not-rendered   ← (a) | (b) rendered-not-planned | (c) deviation-ledger drift | (d) marked-written-not-rendered | (e) plant-instance-not-rendered
- **Planned (outline):** outline.md §Ch04 — "<the beat/plant/cliffhanger, quoted>"   (— for class (b): none; for class (d): the tracker row, quoted, with its owning file; for class (e): the plant row and cell, quoted, e.g. `Hand-to-ribs | #2 involuntary`)
- **Rendered (prose):** <absent | ch04.md line NNN — "<quote>">   (class (d) partial: name the channel delivered vs the channel promised)
- **Ledger:** <no outline-deviation.md entry | the drifted entry, quoted (class c) | — (class d)>
- **Story debt:** <orphaned plant / unprepared payoff in chNN / broken cliffhanger promise / unratified canon fact>
- **Routing:** INLINE   (or: → DEVPLAN for a ledger-side resolution)
- **Flagging:** SAFE-CUT | TRADE-OFF | SAFE-KEEP
- **Suggested action:** <(a) the one-line weave that renders the element, OR the retroactive deviation entry text (→ DEVPLAN); (b) BOTH options — "ratify: append '<entry text>' to outline-deviation.md (→ DEVPLAN milestone for /book fix)" OR "trim: <the cut>" — adjudicated via SMELL-PENDING, never auto-decided here; (c) the corrective ledger append; (d) partials — BOTH "complete the channel: <the weave>" and "revert the row to `planned` (→ DEVPLAN milestone for /book fix)">
```

### Fidelity Audit section (always present)

```markdown
## Fidelity Audit (Source: fidelity)

Chapter: ch04. Outline elements enumerated: N. Ledger entries touching ch04: M. Tracker rows for ch04 marked `written`: W (files: <list>). Plant-table instances assigned to ch04: P. Graph triage: <fresh — pair diff used | skipped (absent/stale/no node)>.

| Planned element / prose beat / tracker row | Rendered | Ledger | Verdict |
|---|---|---|---|
| cold-open at dispensary | ch04.md l.1-40 | — | clean |
| plant: ledger stamp | ABSENT | no entry | #N (a) flagged |
| scene: corridor interview | moved to ch05 | Ch.04 entry 2026-05-02 | acknowledged |
| (prose) rooftop exchange, l.210 | present | no entry | #M (b) flagged |
| (tracker) micro-details.md "coolant — smell + memory" `written` | object only, l.88 | — | #P (d) flagged, partial |
| (plant) Hand-to-ribs #2 involuntary | ABSENT | — | #Q (e) flagged |

Findings: A class (a) / B class (b) / C class (c) / D class (d) / E class (e). Acknowledged deviations: F. Ledger-, tracker- and plant-table-side milestones → DEVPLAN Phase NN.
```

## DEVPLAN milestone format (ledger-side findings)

Per `instructions/milestone-format.md`, same shape sniff uses for ANCHOR-NEEDED (see `sniff.md` §"DEVPLAN milestone format"): append `## Phase <NN+1> — Fidelity ledger fixes (<book> <chNN>) (<date>)`, one `- [ ]` milestone per finding carrying the retroactive `outline-deviation.md` entry text (append-only, dated), the outline annotation to apply (`[moved to chXX]` / cut marker), and any orphaned-plant reassignment target derived per the §Autonomous-decision principle — never "user picks A or B?". Class (d) milestones carry instead: the owning file, the row quoted verbatim, and the single edit `written` → `planned`. Class (e) milestones carry the plant row, the cell being moved, and the renumbering of the row's remaining instances.

## Steps for the executing agent

1. Resolve the chapter prose file and its outline §. Either missing → print the error and exit.
2. Graph triage only when fresh per `instructions/graph-recall.md`: query the planned/rendered node pair with `--budget 4000`; hold the diff as a candidate list. Node missing or result empty → skip triage silently.
3. Read the outline § verbatim; enumerate every beat, plant assignment, motif assignment, and cliffhanger. Read `outline-deviation.md` if present; extract the entries touching this chapter. Collect the tracker files per Input 4; extract the rows for this Book+Ch marked `written`. Read the plant table per Input 5; extract this chapter's column.
4. Read the prose verbatim. Run classes (a), (b), (c), (d), (e), applying the acknowledged rule, the substantive-beat bar, and the channel test that classes (d) and (e) share.
5. Append SMELL.md entries (`Source: fidelity` — append, never overwrite) + the Fidelity Audit section to `chapters/<book>/SMELL.md`.
6. Ledger-side, tracker-side and plant-table-side findings → append the DEVPLAN phase.
7. Print: `fidelity: <book> <chNN> — A planned-not-rendered / B rendered-not-planned / C ledger-drift / D false-written (of W marks checked) / E plant-instance-not-rendered (of P instances due); F acknowledged. G entries → SMELL.md; H milestones → DEVPLAN Phase NN.`

## Calibration (load-bearing)

- **Independent verifier, both ways.** Never assume the writer's Step 7 self-check ran or ran honestly — re-derive everything. But also never punish the latitude the contract grants: the outline is a plan, not a transcript.
- **The ledger closes findings.** Acknowledged = closed. Re-flagging a ratified deviation is the check failing, not the chapter.
- **Never auto-decide class (b).** Ratify-vs-trim is an authorial call; the check's job is to make the call impossible to skip, not to make it.
- **Class (d) checks the writer's own claim.** The `written` mark was set by the session that wrote the prose (`chapter-writer.md` Step 5.5) and is re-read nowhere else in the skill. Treat every mark as unverified until the element is located on the page, in the channel the row names.
- **Coordinate with Chekhov.** Plant/payoff existence across the book, the register reconciliation and the instance-gap bound are `coherence-check.md` §Chekhov's; fidelity checks THIS chapter against ITS plan, so class (e) asks only whether the instances due here landed — never whether the row has enough of them. If Chekhov already flagged the missing plant, reference its entry in the audit table instead of duplicating.
