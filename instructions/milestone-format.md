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

## Used by

`sniff.md`, `coherence-check.md`, `continuity-check.md`, `fix.md`, `revise.md`, `chapter-writer.md` — and by Claude when planning phases for the surrounding orchestration (write/coherence cycle scripts, deferred verifications).
