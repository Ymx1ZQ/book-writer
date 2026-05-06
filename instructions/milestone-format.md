# Milestone Format — Executable vs Operational

This file defines the canonical format for `DEVPLAN.md` milestones in book-skill projects. Cross-link from any instruction that writes to `DEVPLAN.md`.

## Two kinds of items

**Executable items** use checkbox `- [ ]` (and `- [x]` when done). They are consumable by the autonomous pipeline:

- Canon milestones consumed by `/book fix` (sniff, coherence, continuity output).
- Prose entries consumed by `/book revise` (`REVIEW.md`, `PROOFREAD.md`; `SMELL.md` uses its own `## #N` + `**Status:**` structure already).
- Chapter entries consumed by `/book write` / `/book chapter`.
- Direct file edits the implementing agent will perform without human intervention.

**Operational items** use plain bullet `- ` (no checkbox). They describe steps the autonomous pipeline cannot close on its own:

- Orchestration script runs (`./run-coherence-cycle.sh ...`, `./run-write-cycle.sh ...`).
- Manual test runs requiring user action.
- Verification gates depending on a future live run.
- Deferred work pending an external trigger.
- Documentation / runbook steps.

Operational bullets may carry an inline status tag where useful: `- pending`, `- done 2026-MM-DD`, `- deferred — requires live run`.

## Why the distinction matters

`run-coherence-cycle.sh` (and `run-write-cycle.sh`) compute the unresolved-findings count by `grep -c "^- \[ \]"` on `DEVPLAN.md`. If operational items use checkboxes, they accumulate as a constant offset that no consumer can clear, and the stuck-issue guardrail (exit code 7) fires spuriously even when the pipeline has actually converged.

By reserving `- [ ]` for items the pipeline can close, the counter becomes a true convergence signal: it goes to zero when (and only when) all autonomous fixes have been applied.

## Examples

**Executable (checkbox):**

```
### M3: Reconcile la boîte distance to 0.5 km

- [ ] Update `chapters/book-1/writing-notes.md §Texture Palette` row "la boîte distance" from 1.8 km to 0.5 km.
- [ ] Append foundation-hum bullet to `world/level-0-reality/architecture.md §Data Center Adjacency` documenting Le Panier 0.5 km radius.
```

`/book fix` reads these, applies them, marks `[x]`, the count drops.

**Operational (plain bullet):**

```
### M12: Live pre-writing convergence run

- Run `./run-coherence-cycle.sh all --until-clean`. Capture log to `archive/...md`. — pending
- Verify: zero BLOCKING + zero WARNING, ≤ 2 cycles. — pending
- On success, mark closes M9 first item and M11 Test 1.
```

These describe a runbook. The user runs the script (or instructs Claude to run it). No `/book fix` invocation will close them. Plain bullets keep the convergence counter clean.

## Override of global CLAUDE.md

Global CLAUDE.md may instruct "every task uses a checkbox." This skill's doctrine **overrides** that for `DEVPLAN.md` files inside book-skill projects: only executable items get checkboxes. Project-level CLAUDE.md should restate the override and point here.

## What never enters DEVPLAN

DEVPLAN holds **milestones only** — never future-writer instructions, never editorial-choice escalations, never long-lived backlog. The following patterns are anti-patterns regardless of the label used:

- **`### Pending` / `### Decisions Pending` / `### Drafting-Only` / `### Awaits Draft` / `### Escalated to User` sections** → BANNED. Route by content:
  - Drafting-time guidance for an undrafted chapter → keyed section `## ChNN-<short-name>` in `chapters/<book>/writing-notes.md` + `→ See writing-notes.md §ChNN-<short-name>` pointer at the relevant outline beat. Apply the writing-notes section *now*, even though the chapter prose does not yet exist; that *is* the action.
  - Editorial choice between A/B → see §Autonomous-decision principle below. The system picks one and records the rationale; it does not escalate.
  - Tracker drift / list maintenance with no obvious assignment → derive the most defensible target (closest chapter that imports the relevant context, character file owning the trait, etc.) and apply now. Don't park.
- **`Status: Pending (awaits ...)` lines** in any tracker file (SMELL.md, REVIEW.md, PROOFREAD.md, DEVPLAN.md) → BANNED. Same routing as above.
- **`### Deferred to Phase NNN` sections** → permitted ONLY for cap-overflow inside a single coherence/continuity phase, AND only if the successor phase consumes them within 1-2 cycles. A "Deferred" section that survives 3+ phases is a backlog leak — promote everything to writing-notes / outline / character file and delete the section.
- **Future-writer instructions** (e.g., "verify draft uses X phrasing", "remember at draft time to surface the Y plant") → BANNED in DEVPLAN. Route to `chapters/<book>/writing-notes.md` as a drafting guard, with `→ See writing-notes.md §...` pointer at the relevant outline beat. The writing-notes section is the durable home; DEVPLAN is the work-in-progress ledger.

The unifying rule: if a finding's resolution lives at draft time, the *current-phase* action is to write the drafting guidance into context (writing-notes / outline / character file) so the future writer pass picks it up automatically. Parking the finding in DEVPLAN as "deferred" routes it nowhere and accumulates as backlog leak.

## Autonomous-decision principle

The book pipeline is an **autonomous writer**, not an assistant. Editorial-choice escalations to the user are always a failure mode — the system must commit a position based on canon and apply it.

When a finding has multiple plausible resolutions, derive the default in this priority order:

1. **`world/canon-hierarchy.md` tier order** — explicit precedence rules between worldbuilding files, character files, plot files, outlines, and prose. The higher tier always wins; lower-tier files defer.
2. **Canon as already written** — among files at the same tier, the existing canon usage takes precedence over the new finding's framing. If 80% of the trilogy already calls a sensor "PD-073", the canonicalization adopts that form.
3. **Chapter's own tonal/structural guards already declared** — writing-notes per-chapter sections (density caps, register guards, opening-type rotation, beat-priority caps) constrain the resolution space. If a guard caps a beat at 1 sentence, the resolution must fit.
4. **Occam** — among options that survive (1)-(3), pick the one that adds the least new infrastructure (no new files, no new naming conventions, no new cross-references unless one already exists).

Apply the chosen default to canon AND record a one-line rationale in the appropriate decision-record location:

- Drafting-time guidance → `chapters/<book>/writing-notes.md` keyed section.
- Character-level decision → character file (Habits, Tradecraft, Voice, etc.).
- Plot-level decision → `plot/<file>.md` (key-scenes, ticking-clocks, plant tracking).
- Worldbuilding decision → `world/<file>.md`.

The user can always override later by editing the decision-record. But the system commits a position — it never returns "A or B?" as a question.

**Banned constructs:** `"User picks A or B?"`, `"Needs design decision"`, `"Escalated to user"`, `"Pending user input"`, `"Choice point — user must decide"`. If a triage step produces such a bucket, the triage is incomplete: re-derive the default per the four-tier order and apply.

**Genuine blockers** (the canon contradicts itself irreducibly, AND no defensible default exists from any of the four tiers) are vanishingly rare. Confirm the contradiction is irreducible before raising. If raised, present 2-3 options each with concrete canon evidence (file:line for each), not as an open question.

## Verification & next-steps blocks

Phases written by `/book coherence` and `/book continuity` may include a `### Verification & next steps` block listing operational items that close the phase. These items are plain-bullet (per the executable/operational distinction above) and may carry inline status (`- pending`, `- done YYYY-MM-DD`).

Three rules constrain the block:

**1. Per-phase scope only.** Operational items describe ONLY actions that close THIS phase's milestones (e.g., `/book fix <scope>` for the canon side, `/book revise <scope>` for the prose side, a re-run of THIS phase's check that verifies clean state). They do NOT restate prior phases' pending status. The cycle script's `count_unresolved_global` (run-coherence-cycle.sh) is the cross-phase source of truth — restating "Pending milestones from Phases X / Y / Z still require application" propagates a meta-statement that becomes stale the instant the next `/book fix` lands, and the propagation amplifies as each new phase copies it forward.

**2. No transitive forward-looking unblock claims.** Statements like "B1 drafting unblocked once Phase X / Y / Z close" depend on external phases and decay silently. Drafting readiness lives in episode/state docs, not phase ledgers. The verification block may reference the genuine immediate successor of THIS phase (`/book fix <scope>` → re-run `/book coherence <scope>` → `/book write <scope>` *only if it's the next pipeline step from THIS phase's clean state*), but never a transitive dependency on other phases.

**3. `/book fix` closes matching operational items.** When `/book fix <scope>` applies a phase's executable milestones, it MUST also scan DEVPLAN.md for plain-bullet operational items in OTHER phases whose action names the just-completed `/book fix <scope>` (typical patterns: `Apply Phase NN milestones via /book fix <scope>`, `Re-run /book fix <scope>`). For each match with status `— pending`, update to `— done YYYY-MM-DD`. This keeps the operational ledger consistent with the executable ledger so the user does not see stale "pending" markers after a clean cycle.

## Used by

`sniff.md`, `coherence-check.md`, `continuity-check.md`, `fix.md`, `revise.md`, `chapter-writer.md` — and by Claude when planning phases for the surrounding orchestration (write/coherence cycle scripts, deferred verifications).
