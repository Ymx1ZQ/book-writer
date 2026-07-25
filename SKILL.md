---
name: book
description: >-
  Unified writing pipeline for multi-book fiction projects. One entry point (`/book
  <command>`) over ~29 commands: project setup, coherence fixing, batched chapter writing,
  a multi-pass review stack (sniff, factcheck, sensitivity, readability, cold-read,
  proofread, adjacency…), revision, PDF/EPUB export, and a parallel-write merge phase
  (judge / integrate-anchors / arbiter). Genre-agnostic — tone, rules, structure and genre
  come from the project's own files (CLAUDE.md, world/, characters/), never from the skill.
---

# Book — Unified Writing Pipeline

Single entry point for all book-writing operations. Genre-agnostic — reads tone, rules, structure, and genre from the project's own files (CLAUDE.md, world/, characters/).

## Invocation

```
/book <command> [arguments]
```

## Commands

| Command | What it does | Example |
|---------|-------------|---------|
| `help` | Show this help + the full pipeline | `/book help` |
| `init` | Scaffold a new book project (directories, empty templates) | `/book init` |
| `setup` | Interactive wizard to populate project files (worldbuilding, characters, plot) | `/book setup` |
| `coherence [scope]` | Find problems across project, write fix devplan | `/book coherence all` |
| `fix <scope>` | Apply coherence fixes from DEVPLAN.md to project files | `/book fix all` |
| `fix common` | Apply ONLY coherence fixes on shared files (world/, characters/, plot/) | `/book fix common` |
| `revise <book>` | Apply editorial (REVIEW.md) + proofreading (PROOFREAD.md) fixes to chapter prose | `/book revise book-1` |
| `write <book>` | Write chapters in batches of 5 | `/book write book-1` |
| `chapter <book> <ch>` | Write a single chapter | `/book chapter book-1 ch03` |
| `review <book> [ch]` | Editorial review → REVIEW.md | `/book review book-1` |
| `proofread <book> [ch]` | Grammar/syntax/punctuation → PROOFREAD.md | `/book proofread book-1` |
| `compact [scope]` | Remove bloat, enforce cross-refs, de-duplicate | `/book compact all` |
| `continuity <from> <to>` | Cross-book continuity check | `/book continuity book-1 book-2` |
| `pdf <book> [ch]` | Render a chapter or a whole book to PDF | `/book pdf book-1 ch01` |
| `epub <book> [ch]` | Render a chapter or a whole book to EPUB (Kindle/KDP) | `/book epub book-1` |
| `sniff <book> [ch]` | Adversarial skeptical-reader pass → SMELL.md (catches plausibility / nose-wrinkle issues coherence/review/proof don't) | `/book sniff book-1 ch01` |
| `factcheck <book> [ch]` | Active real-world accuracy: enumerate every external-world claim → verify each → SMELL.md (`Source: factcheck`) + VERIFY items to PENDING | `/book factcheck book-1 ch01` |
| `fidelity <book> <ch>` | Planned-vs-rendered check: chapter outline § vs prose vs outline-deviation.md ledger — silent cuts, unplanned beats, ledger drift, false `written` tracker marks → SMELL.md (`Source: fidelity`) + ledger-/tracker-side → DEVPLAN | `/book fidelity book-1 ch04` |
| `motif <book> [ch]` | Symbolic / motif coherence: motif not inverted/drifted, evolution intentional, payoff lands → SMELL.md (`Source: motif`) + canon → DEVPLAN | `/book motif book-1 ch01` |
| `sensitivity <book> [ch]` | Conservative representation / dated-language pass (advisory-first, diegetic-intent gated) → SMELL.md (`Source: sensitivity`) | `/book sensitivity book-1 ch01` |
| `readability <book> [ch]` | Register-aware flow / "scorrevolezza" pass — flags the accidental brick (slog, clause-stacking, paragraph-mass) only outside intended-heavy registers → SMELL.md (`Source: readability`) | `/book readability book-1 ch01` |
| `coldread-enum <book> [chNN]` | Paranoid defect cataloguer; canon-blind cold-read producing raw finding catalog → COLDREAD.md | `/book coldread-enum book-1 ch04` |
| `coldread-filter <book> [chNN]` | Adversarial triage of coldread-enum output into SMELL.md entries | `/book coldread-filter book-1 ch04` |
| `snapshot <book> [chNN]` | Generate or update reader-state snapshot for a chapter → `chapters/coldread-state/<book>-<chNN>.md` | `/book snapshot book-1 ch04` |
| `adjacency <book> [chNN] [chNN-chMM]` | Cross-chapter pass over a window of consecutive chapters: shape-repetition / idiolect-collision / dramatic-irony legibility → SMELL.md (`Source: adjacency`); structural findings → DEVPLAN for the user | `/book adjacency book-1 ch03` |
| `judge <manifest> <out>` | Cross-model chapter comparator → rank-only JSON (parallel-pipeline merge phase) | `/book judge manifest.json out.json` |
| `integrate-anchors <json>` | Integrate winning-draft anchors from loser drafts (parallel-pipeline merge phase) | `/book integrate-anchors aggregated.json` |
| `arbiter <book> <ch>` | Autonomous resolution of `*-PENDING.md` trade-offs (parallel-pipeline merge phase) | `/book arbiter book-1 ch01` |
| `sweep <book>` | Archive terminal review artifacts (SMELL/REVIEW/COLDREAD/PROOFREAD/PENDING) for closed chapters → `chapters/<book>/archive/`. Auto-invoked from `writer.md` Session Start and the cycle scripts. | `/book sweep book-1` |

## The Pipeline

```
PROJECT SETUP
  1. /book init                → create directory structure + templates
  2. /book setup               → interactive wizard to fill worldbuilding, characters, plot, outlines

PRE-WRITING
  3. /book coherence all       → find problems, write devplan
  4. /book fix all             → apply coherence fixes to project files
  5. /book compact all         → remove bloat, enforce cross-refs, de-duplicate

WRITING LOOP (repeat per batch)
  6. /book write book-1        → write 5 chapters
  7. /book sniff book-1        → adversarial skeptical-reader → SMELL.md
 7b. /book factcheck book-1    → active external-world claim verification → SMELL.md (Source: factcheck)
  8. /book review book-1       → editorial review → REVIEW.md
 8b. /book motif book-1        → symbolic/motif coherence → SMELL.md (Source: motif) + canon → DEVPLAN
 8c. /book sensitivity book-1  → representation/dated-language (advisory) → SMELL.md (Source: sensitivity)
  9. /book coldread-enum book-1 → paranoid defect catalog → COLDREAD.md
 9b. /book coldread-filter book-1 → triage to SMELL.md entries
 9c. /book readability book-1  → register-aware flow pass → SMELL.md (Source: readability)
 10. /book proofread book-1    → line-level review → PROOFREAD.md
 11. /book revise book-1       → apply SMELL (sniff+factcheck+motif+sensitivity+readability+adjacency) + REVIEW + PROOFREAD fixes to prose
 11b. /book snapshot book-1    → refresh reader-state snapshot for next chapter
 11c. /book adjacency book-1 chNN → cross-chapter pass over [ch(NN-1), chNN]: shape/idiolect/irony-legibility → SMELL.md (structural → user). Runs once the chapter is final, against its predecessor. Its SMELL micro-fixes are consumed by the NEXT cycle's revise (adjacency runs after this chapter's revise by design — it needs the chapter final).
 11d. /book arbiter book-1 chNN → resolve any `*-PENDING.md` trade-offs this cycle produced (autonomous, Phase 42). In the orchestrated pipeline this runs every cycle; in a bare hand-run linear flow the PENDING files are instead left for the user.

BETWEEN BOOKS
 12. /book compact all         → post-cycle cleanup
 13. /book continuity book-1 book-2 → verify cross-book consistency

PARALLEL PIPELINE — MERGE PHASE (run-merge-phase.sh, per chapter)
  /book judge <manifest> <out>     → cross-model judge (×N ensemble) → rank-only JSON
  /book integrate-anchors <json>   → integrate loser-draft anchors into the winner
  /book arbiter <book> <ch>        → autonomously resolve *-PENDING.md trade-offs
```

`judge`, `integrate-anchors`, and `arbiter` were standalone `book-*` skills until Phase 11 consolidated the toolchain into this one skill. `judge` is cross-CLI: under Claude it routes to `instructions/judge.md`; under Codex it is the `codex/SKILL.md` variant installed to `~/.codex/skills/book/`.

## The human cold-read gate

The steps above are the *machine* pipeline. Completing them yields a **machine-checked** chapter — every enumerable check passed — not a *finished* one. The machine passes are structurally blind to what only a linear, committed, skeptical human reading catches: referential friction felt at reading speed, implausibility a cooperative reader rationalizes away, jargon the agent silently decodes, and whether the chapter is *alive* on the page. A chapter is reader-validated only after a human has read it at speed. The machine pipeline's job is to make that human read **cheap** — to exhaust the enumerable so the human's attention lands only where a human is required. Do not report a machine-checked chapter as "done" or "clean"; report it as machine-checked and awaiting human cold-read.

**Pre-draft context symmetry:** the chapter-writer agent enforces beat↔context symmetry before drafting (chapter-writer Step 2.6 — STOP on missing files, advisory on orphans). `coherence-check` flags drift on already-written outlines as WARNING (classes R + S). No standalone subcommand: the symmetry check lives inside `chapter-writer` (write-time) and `coherence-check` (audit-time).

## Execution

When a command is received:

1. **Parse the command** from the arguments.
2. **Read the instruction file** from `~/.claude/skills/book/instructions/<command>.md`:
   - `init` → `instructions/init.md`
   - `setup` → `instructions/setup.md`
   - `coherence` → `instructions/coherence-check.md`
   - `fix` → `instructions/fix.md`
   - `revise` → `instructions/revise.md`
   - `write` → `instructions/writer.md`
   - `chapter` → `instructions/chapter-writer.md`
   - `review` → `instructions/reviewer.md`
   - `proofread` → `instructions/proof-reader.md`
   - `compact` → `instructions/compact.md`
   - `continuity` → `instructions/continuity-check.md`
   - `pdf` → `instructions/pdf.md`
   - `epub` → `instructions/epub.md`
   - `sniff` → `instructions/sniff.md`
   - `factcheck` → `instructions/factcheck.md`
   - `fidelity` → `instructions/fidelity.md`
   - `motif` → `instructions/motif.md`
   - `sensitivity` → `instructions/sensitivity.md`
   - `readability` → `instructions/readability.md`
   - `coldread-enum` → `instructions/coldread-enum.md`
   - `coldread-filter` → `instructions/coldread-filter.md`
   - `snapshot` → `instructions/snapshot.md`
   - `adjacency` → `instructions/adjacency.md`
   - `judge` → `instructions/judge.md`
   - `arbiter` → `instructions/arbiter.md`
   - `integrate-anchors` → `instructions/integrate-anchors.md`
   - `sweep` → `instructions/sweep.md`
3. **Follow the instruction file exactly.** The instruction file IS the skill — this dispatcher just routes to it.
4. **Pass all remaining arguments** to the instruction file's process.
5. **After the instruction completes**, commit changes — **scoped to this skill's outputs only** (Phase 41 M13 hygiene):
   - The instruction file declares which files this skill produces/modifies. Stage ONLY those declared output paths via targeted `git add <path1> <path2> ...`.
   - If the instruction does not explicitly declare outputs, use `git diff --name-only` on the working tree to enumerate files this skill *actually* touched, and stage those — DO NOT use `git add -A` (it captures dirty work unrelated to this skill; this caused the Phase 40 M7 commit-bundling incident).
   - Commit with message: `book <command> <args>: <one-line summary of what was done>`
   - Do NOT push (the caller decides when to push).

## Optional: graph-assisted recall (graphify)

If the consuming project keeps a graphify knowledge graph (`graphify-out/graph.json` in the project root), several instructions replace bulk canon loading with targeted graph queries — see `instructions/graph-recall.md` for the full doctrine (opt-in detection, index vs answer mode, the freshness gate, the never-substitute list, canon-blind exclusions, fallback ladder). Consumers: `chapter-writer.md`, `coherence-check.md`, `continuity-check.md`, `motif.md`, `adjacency.md`, `fidelity.md`. Write side: mutating commands (`fix`, `revise`, `chapter`, `compact`, `integrate-anchors`, `arbiter` on APPLY) refresh the graph after their commit — see `instructions/graph-recall.md` §Keeping the graph fresh. Without the graph, every command behaves exactly as documented — the graph is a per-project accelerator, never a dependency.

## Recommended model per command

| Tier | Commands | Rationale |
|---|---|---|
| **Opus** | `chapter` / `write`, `revise`, `integrate-anchors`, `judge`, `arbiter`, `review`, `sniff`, `coldread-filter`, `setup` | Creative drafting and judgment calls — these need the strongest prose + evaluation model. |
| **Sonnet** | `coherence`, `continuity`, `fix`, `proofread`, `factcheck`, `fidelity`, `motif`, `sensitivity`, `readability`, `adjacency`, `coldread-enum`, `snapshot`, `compact`, `sweep` | Detection and mechanical passes are rubric-driven — the rubric carries the quality, not the model. |

Unlisted commands (`help`, `init`, `pdf`, `epub`) are mechanical/scripted and run fine on either tier. Scripted enforcement of this table lives in the consuming project's pipeline (ground-truth DEVPLAN Phase 80), not in this skill; interactive users pick the tier via `/model` before running the command.

## Milestone Format

`DEVPLAN.md` milestones use two formats depending on what closes them:

- **Executable items** (consumable by `/book fix`, `/book revise`, `/book write`, or direct agent edits) use checkbox `- [ ]`.
- **Operational items** (orchestration script runs, manual tests, deferred verifications, runbook steps) use plain bullet `- ` without checkbox.

Reason: `run-coherence-cycle.sh` and `run-write-cycle.sh` count `^- \[ \]` as unresolved findings. Operational items in checkbox form accumulate as a constant offset that trips the stuck-issue guardrail spuriously. See `instructions/milestone-format.md` for the full doctrine, examples, and the override of any global "every task = checkbox" rule.

## Genre Agnosticism

This skill contains NO genre-specific content. All genre, tone, style, and structural rules come from the project's own files:
- `CLAUDE.md` — project-level instructions, language, structure overview
- `world/tones.md` — tonal registers per narrative level
- `world/prose-rules.md` — writing quality rules
- `world/writing-checklists.md` — sensory enforcement per level
- `characters/notes/voice-samples.md` — character voice profiles

The instructions reference these files generically: "read the project's tone file" not "apply Kafkaesque register." This makes the pipeline usable for any multi-book fiction project.

## If `help` is the command

Display the Commands table and Pipeline section above. Then stop.

## Rules

- ❌ Never execute without reading the instruction file first
- ❌ Never hardcode genre, tone, or style in the dispatcher or instructions — it comes from the project
- ✅ If the command is not recognized, show the help table
- ✅ If arguments are missing, show the relevant command's usage
