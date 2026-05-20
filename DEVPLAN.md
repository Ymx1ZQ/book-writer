# Book Skill — DEVPLAN

Tooling milestones for the `/book` skill. Project-content milestones live in each book project's own DEVPLAN.

---

## Phase 1 — PDF Export (2026-04-29) — DONE

`/book pdf <book> [chNN]` — render Markdown chapters to a book-quality PDF via WeasyPrint + python-markdown. Single-chapter and whole-book modes. Output → `chapters/<book>/pdf/`.

- [x] M1: `scripts/build_pdf.py` + `scripts/book.css` (A5, Georgia 11pt, drop-cap, scene-break ornament `* * *`, page numbers, title page for whole-book mode).
- [x] M2: `instructions/pdf.md` dispatcher instruction.
- [x] M3: SKILL.md commands-table row + routing (`pdf → instructions/pdf.md`).
- [x] M4: project-side `.gitignore` of `chapters/*/pdf/` (applied to the consuming project, not the skill repo).
- [x] M5: smoke test — book-1 ch01 (43K) + book-1 whole (81K with title page) generated cleanly.

---

## Phase 2 — EPUB Export (2026-04-29) — DONE

`/book epub <book> [chNN]` — mirror of `/book pdf` for the digital Kindle pipeline. Engine: `ebooklib` (pure-Python, MIT, no native deps). Output → `chapters/<book>/epub/`. Optional `chapters/<book>/meta.yaml` overrides title/author/identifier/language; defaults: title from `outline.md`, author "Unknown Author", deterministic UUID, lang "en".

- [x] M1: `scripts/build_epub.py` + `scripts/epub.css` (reflow-friendly em-based, no page-sizes, drop-cap, `* * *` scene break).
- [x] M2: `instructions/epub.md`.
- [x] M3: SKILL.md commands-table row + routing.
- [x] M4: smoke test — **closed by Phase 5 M5/M6 (2026-05-01)**. uv self-bootstrap resolved the PEP 668 issue; smoke test surfaced two pre-existing bugs (empty EpubNav content, chapter content set as str instead of bytes), both fixed in Phase 5 M6. EPUBs now valid in both single-chapter and whole-book modes.

---

## Phase 3 — Writer Guardrails + Smell-Test Layer (2026-04-29) — IN PROGRESS (IDD fallback)

> **Execution mode:** IDD, not TDD. Phase 3 deliverables are markdown LLM-instruction files (`sniff.md`, edits to `chapter-writer.md` / `coherence-check.md` / `revise.md` / `SKILL.md`). The skill repo has no test runner, and grep-tests for markdown content would be cargo-cult TDD (the "test" would be a near-duplicate of the content being written). Per `~/.claude/skills/devplan/TDD.md` §1, falling back to IDD for these milestones with the reasoning logged here.

Surfaced from analysis of the first written Ch.01 (ground-truth project). The chapter exposed a class of recurring failure: the writer agent fills worldbuilding silence with **plausible-but-uncanonicalized invention** (€2/kg sardines in 2045 Marseille; "filtration alert tier two" with no canonical tier system; "drone corridor 042" with no schema; "beat off by 0.3" technobabble). Coherence-check catches internal contradictions. Reviewer catches craft. Proofreader catches surface. **Nothing in the current pipeline catches "would a skeptical, informed reader call BS on this?"** — what we're calling the *smell test*.

This phase adds three layers:

1. **A new `/book sniff` subcommand** — adversarial skeptical-reader pass producing `SMELL.md` with three classifications: INLINE (revise can fix), ANCHOR-NEEDED (worldbuilding gap; surface to project DEVPLAN), ACCEPT (deliberate, signoff).
2. **Hardened `chapter-writer.md` rules** — pre-drafting checks that prevent the most common invention patterns (economic, system-implying numbers, unearned capabilities, interior labeling, undocumented outline cuts).
3. **Hardened `coherence-check.md`** — BLOCKING / WARNING / NOTE flags for the same classes the sniff pass catches, run in the routine coherence flow.

Phase 3 does not implement project-content milestones — those are filed in each book project's DEVPLAN as anchor-fill milestones surfaced by the sniff output.

### M1: New `instructions/sniff.md` — adversarial skeptical-reader pass ✅

**File:** `instructions/sniff.md` (NEW).

- [x] Define usage: `/book sniff <book> [chNN]`. Reads the latest draft of the chapter (or the most recent if no chapter specified), produces `chapters/<book>/SMELL.md`.
- [x] Specify the reader persona for the executing agent: *informed, skeptical, well-read, not romantic about the work*. Looks for things that would make a reader pause and call BS.
- [x] Nine objection categories the agent must scan for, line by line:
  1. **Anachronism** — does the assertion track with 21 years of climate / tech / society evolution from 2024 baseline?
  2. **Worldbuilding-canon contradiction** — direct conflict with `world/` or `characters/` files?
  3. **Technobabble without referent** — specific number/term ("0.3", "tier two", "corridor 042") implies a system; does that system exist in canon?
  4. **Unearned capability or knowledge** — character/object/agent does/knows something not previously established.
  5. **Domain plausibility** — would an economist, engineer, doctor, person with disability, or local (Marseillais, etc.) call BS?
  6. **Physical implausibility** — geometry, physics, biology of described action.
  7. **Character behavior** — consistent with established sheet?
  8. **Plot armor / convenience** — events resolve too easily; info appears when needed.
  9. **Continuity within chapter** — timeline, geography, props consistent across the chapter itself (e.g., object in pocket → in hand without transition).
- [x] Output format: `SMELL.md` with one entry per objection. Each entry:
  - **File:line** (or scene reference)
  - **Quote** (the offending passage)
  - **Objection category** (one of the 9 above)
  - **What the reader would think**
  - **Classification:** INLINE / ANCHOR-NEEDED / ACCEPT
  - **Suggested action:**
    - INLINE → proposed prose fix.
    - ANCHOR-NEEDED → which worldbuilding file needs a section, what the section must define, suggested milestone language for the project DEVPLAN.
    - ACCEPT → why deliberate (only if the writer agent has documented evidence in the outline or world files).
- [x] Write a short calibration note: the agent must err toward *more* objections, not fewer. False positives are cheap (the user dismisses); false negatives let bad prose ship.
- [x] After producing `SMELL.md`, the skill prints a one-line summary: `wrote SMELL.md — N objections (X INLINE, Y ANCHOR-NEEDED, Z ACCEPT)`.

### M2: Wire the dispatcher ✅

**File:** `SKILL.md` (REVISIONE).

- [x] Commands-table row: `| sniff <book> [ch] | Adversarial skeptical-reader pass → SMELL.md | /book sniff book-1 ch01 |`.
- [x] Routing list: `sniff → instructions/sniff.md`.
- [x] `## The Pipeline` section: insert sniff between write and review:
  ```
  WRITING LOOP (repeat per batch)
    6. /book write book-1        → write 5 chapters
    7. /book sniff book-1        → adversarial skeptical-reader → SMELL.md
    8. /book review book-1       → editorial review → REVIEW.md
    9. /book proofread book-1    → line-level review → PROOFREAD.md
   10. /book revise book-1       → apply SMELL + REVIEW + PROOFREAD fixes to prose
  ```

### M3: Extend `instructions/revise.md` to consume SMELL.md INLINE items ✅

**File:** `instructions/revise.md` (REVISIONE).

- [x] Add SMELL.md to the load list.
- [x] Apply INLINE entries (proposed prose fixes from the sniff pass) BEFORE editorial/proof fixes — gaffes cleared first, craft after.
- [x] ANCHOR-NEEDED entries are NOT applied; instead, surface them in the revise summary as "deferred to worldbuilding (see SMELL.md ANCHOR-NEEDED block)" and stop there. They become input to the project's DEVPLAN.
- [x] ACCEPT entries are noted in the summary but not acted on.

### M4: Harden `instructions/chapter-writer.md` — pre-drafting `MUST` rules ✅

**File:** `instructions/chapter-writer.md` (REVISIONE — add a new Pre-Drafting Anchor Checks section).

- [x] **4a — Level-aware economic-anchor pre-check.** Before drafting any scene with a *price, wage, cost, balance, salary, rent, fee, fine, tip, ration, memory-credit transaction, kilo+price pairing, monetary unit (€/euros/CBDC/GPU-HE) near digits, allocation request, compliance-score gating*, the agent MUST read the level-appropriate anchor file (Reality → `economy.md §Consumer Anchors`; Ark → `daily-life.md §Economy`; Dome → `bureaucracy.md §Allocation Mathematics`) and pick a value consistent with it. If no anchor exists, STOP and request a worldbuilding-anchor milestone before drafting.
- [x] **4b — Broader no-invent rule** (system-implying details). For any *tier system, score, hum frequency in Hz, MHz, latency / bandwidth / corridor / channel number, % offer / discount, compliance threshold, hardware-vintage capability claim*, the agent MUST verify a canonical worldbuilding anchor exists. If absent, STOP. The trigger keyword set is explicit (no fuzzy matching): `tier`, `score`, `Hz`, `MHz`, `% offer`, `compliance check`, `corridor 0\d\d`, `latency`, `bandwidth`, `LED`, `firmware`, `handshake`, `signature`.
- [x] **4c — Show-don't-tell hard rule with forbidden formulas.** The following constructions are FORBIDDEN as interior labeling and may only appear when they describe an EXTERIOR observation:
  - `the closest thing to <emotion> he/she had had in days/weeks/years`
  - `a kind of <abstract noun>`
  - `almost <verb>` / `almost felt like`
  - `started to <verb>` ... `before/and stopped` (when used as interior gesture-labeling rather than exterior fact)
  - `<character> felt X` followed by an explanation of what X is
  Express interior states through physical action, gesture, or sensory tightening. The agent reviews its own draft for these patterns at self-edit and rewrites or deletes.
- [x] **4d — Outline-to-chapter coverage contract.** If the writer cuts, splits, or reorders outlined scenes during drafting, it MUST: (i) update `chapters/book-N/outline.md` to reflect the new split (move plant tags, update beat-section structure); (ii) write a one-line entry to `chapters/book-N/outline-deviation.md` (NEW file, append-only): `Ch.NN: <scene> moved/cut/merged because <reason>. Plants shifted: <list>.`; (iii) flag any plants that lost their planned chapter so the next write call surfaces them. No silent cuts.

### M5: Harden `instructions/coherence-check.md` — six new check classes ✅

**File:** `instructions/coherence-check.md` (REVISIONE).

- [x] **5a — Economic-anchor BLOCKING** (level-aware) — implemented as check class **L**. For every chapter draft, scan for monetary/transactional/allocation details (regex set: `€\d`, `\beuros?\b`, `\bCBDC\b` near digits, `\bGPU-HE\b` near digits, `\bkilo\b`/`\b/kg\b` in price context, `\bbalance\b` near numeric, `\bration\b` near numeric, `\bcompliance score\b`, `\bmemory credit\b`, `\benzyme cloth\b` near numeric, `W-RAR-03`). Verify each match traces to the level-appropriate anchor file. Unanchored or contradictory → BLOCKING.
- [x] **5b — System-implying-number BLOCKING** — implemented as check class **M**. Same regex strategy on the trigger set from M4b above (`tier <digit>`, `corridor 0\d\d`, `<digit> Hz` outside canonical anchors, `% offer`, etc.). Each match must trace to canon. BLOCKING if not.
- [x] **5c — Interior-labeling NOTE** (soft) — implemented as check class **N**. Scan for the M4c forbidden formulas. Each match → NOTE-level flag with the line and a suggested rewrite. NOT BLOCKING — these are advisory.
- [x] **5d — Outline-to-draft coverage WARNING** — implemented as check class **O**. For every scene listed in the relevant outline, verify a corresponding section exists in the draft (heuristic: scene's distinctive props/characters appear in the draft text). Missing scenes → WARNING with cross-ref to `outline-deviation.md`. Missing AND no entry in `outline-deviation.md` → BLOCKING (the writer cut without documenting).
- [x] **5e — Cross-substrate sensory-echo WARNING** — implemented as check class **P**. Maintain a registry of canonical sensory anchors (e.g., 440 Hz hum in Ark per Phase 111 M3). For every chapter draft, when a sensory detail matches a number/object already canonical at a *different* level, flag WARNING: "this echo is intentional (cross-substrate plant) or accident (collision)? confirm in `temporal-echoes.md §Cross-Substrate Sensory Resonances`." Forces the question to be answered, doesn't block.
- [x] **5f — Redundancy-with-adjacent-text NOTE** — implemented as check class **Q**. Heuristic: if a paragraph repeats specific information given in the immediately preceding paragraph (especially across a system message → flashback boundary, e.g., the Game says "your mother made couscous" and the next paragraph describes that exact couscous), flag NOTE for review — the writer may want to defer / vary the second beat to avoid the reader feeling told twice.

---

**Phase 3 totals:** 5 milestones, all in this skill repo. Phase 3 produces a check (sniff) and rules (chapter-writer, coherence-check) that surface project-content gaps; the gaps themselves go to each book project's DEVPLAN.

**Out of scope:** the smell-test does NOT auto-fix worldbuilding gaps — it just surfaces them. The user/agent triages.

---

## Phase 4 — Context-symmetry Guardrails (2026-04-30) — IDD

Surfaced from the ground-truth project's Phase 113 M4 / Phase 114 investigation. Pre-Phase-114, B1 Ch.01 carried 28 files in `**context:**`; manual audit showed only 16 were genuinely beat-referenced, 12 were orphan accumulation, and 3 newly-canonical files (post-Phase-112) were absent. The previous mitigation was a malformed rule on Ch.01 only ("MAX 3 files actively drawn from in prose"); abandoned in Phase 114 as a band-aid for bloat.

This phase encodes the symmetry principle skill-side so future drift is caught at write-time and at coherence-time, not via manual audit:

- **Symmetry rule (project-side, in each book's outline.md §Context Tags):** every file in `**context:**` has at least one beat that references it; every beat that needs a file lists that file. When beats mutate, `**context:**` mutates.
- **Skill-side enforcement (this phase):** the chapter-writer agent checks symmetry before drafting; the coherence-check agent flags asymmetries on existing outlines as WARNING.

**Execution mode:** IDD (instruction-file deliverables, same justification as Phase 3 §32 — no test runner; grep-tests over markdown rules would be cargo-cult).

### M1: chapter-writer pre-draft Context Symmetry Check ✅

**File:** `instructions/chapter-writer.md` (REVISIONE — append a new Pre-Drafting Context Symmetry Check section after the existing Pre-Drafting Anchor Checks).

- [x] **1a — Beat-side scan (missing files).** Before drafting, the agent parses the chapter outline beats up to the next chapter header, extracting:
  - Explicit references: every `→ see <path>` and every `<path>` mentioned by name.
  - Implicit references: every named character (cross-ref `characters/**.md`), every named location (cross-ref `level-N-*/locations*.md` or `level-0-reality/architecture.md`), every named system / mechanism / technical anchor (cross-ref `world/**.md`).
  Compares the union against the chapter's `**context:**` list (excluding always-loaded set declared in the outline header). Files referenced in beats but missing from `**context:**` → STOP. Output the list of missing files and request user confirmation to add (or auto-add if user has pre-authorized).
- [x] **1b — Context-side scan (orphan files).** For every file in `**context:**` (excluding always-loaded), the agent verifies at least one beat reference exists per 1a. Files with no beat reference → flag as "orphan candidate" in pre-draft summary. NOT blocking — orphans are advisory, since some files may be load-bearing for consistency-only checks (in which case the agent should propose moving them to always-loaded). User confirms before drafting proceeds.
- [x] **1c — Post-draft audit.** After drafting, the agent generates `chapters/book-N/chNN-context-audit.md` (gitignored, ephemeral): each file in `**context:**` mapped to the beat / line-range where it was actually used in prose, plus any file used in prose but not in `**context:**`. Compares against the planned context list and outputs a one-line drift summary: `context drift: -<file> (planned, unused), +<file> (used, unplanned)`. Drift entries feed back into the symmetry check for the next chapter.
- [x] **1d — Always-loaded set awareness.** The agent loads the outline header's always-loaded reference paragraph (typically `world/technology-comparison.md`, `world/temporal-echoes.md`, `world/tones.md`, foreground character files) and excludes those from both the "missing" and "orphan" checks. Always-loaded references are out of scope for per-chapter symmetry.

### M2: coherence-check — context-symmetry as WARNING (R + S) ✅

**File:** `instructions/coherence-check.md` (REVISIONE — append two new check classes after existing Q Redundancy-with-adjacent-text NOTE).

Implementation note: the original DEVPLAN proposed numeric class names (5g/5h), but Phase 3 M5 had already shipped using letter classes (L–Q). To stay consistent with the in-file convention, the new classes are **R** (orphan WARNING) and **S** (missing-context WARNING).

- [x] **R — Context-list orphan WARNING.** For every chapter in the relevant outline, parse `**context:**` and check that each listed file (excluding always-loaded set declared in the outline header) has at least one beat reference (explicit `→ see` OR a named entity that semantically requires the file's content). Files with zero references → WARNING.
- [x] **S — Missing-context WARNING.** For every explicit `→ see <path>` reference and every named character / location / system / technical anchor in beats, verify the corresponding canonical file is in the chapter's `**context:**` (or in always-loaded). Missing → WARNING.
- [x] Both checks are WARNING-level (not BLOCKING) because: (i) the heuristic for "named entity → canonical file" is fuzzy and false positives are non-trivial; (ii) project-side review is the right place to adjudicate. BLOCKING would over-fire.

### M3: Outline-mutation hook in 4d ✅

**File:** `instructions/chapter-writer.md` (REVISIONE — extend existing Phase 3 M4 4d Outline-to-chapter coverage contract).

- [x] **4d.iv — Context-list update on outline mutation.** When the writer cuts/splits/reorders scenes per 4d (i)-(iii), the writer ALSO updates the affected chapter's `**context:**` field — removing files that lose their justifying beat (per 2.6.b), adding files newly required (per 2.6.a). The outline-deviation entry must include a `Context: -<file>, +<file>` line summarizing the diff so the change is auditable in `outline-deviation.md`.
- [x] If a beat moves to a different chapter (Phase 113 example: Ch.01 Beat 2a body-maintenance moved to Ch.04), the source chapter loses the corresponding files (e.g., `medicine-and-body.md`) and the destination chapter gains them. Both `**context:**` fields update; both diffs go to `outline-deviation.md`.

### M4: SKILL.md routing + dispatcher hint ✅

**File:** `SKILL.md` (REVISIONE — small touch).

- [x] Add a one-line note in the Pipeline section pointing at chapter-writer Step 2.6 + coherence-check classes R/S.
- [x] No new subcommand — symmetry checks live inside existing chapter-writer + coherence-check, not as a standalone command.

---

**Phase 4 totals:** 4 milestones, all instruction-file edits. No new tooling. No new subcommand. Tightens the existing chapter-writer + coherence-check + revise pipeline so context-list drift is caught at the two natural enforcement points: write-time (chapter-writer pre-check, blocking on missing files) and audit-time (coherence-check, WARNING on orphans + gaps).

**Out of scope:** auto-fixing the trilogy's existing context-list drift — that's project-side work in `ground-truth/DEVPLAN.md` Phase 114 M3 (sub-agent-driven trilogy audit, applied per-chapter).

---

## Phase 5 — uv-managed export scripts (2026-05-01) — IN PROGRESS

Phase 1 (PDF) shipped expecting `weasyprint` + `markdown` to be on the system Python; Phase 2 (EPUB) added `ebooklib` + `pyyaml`. On modern Linux distros (PEP 668), `pip install --user` is blocked without `--break-system-packages`, and the install.sh dependency-check just emits a warning and leaves the user to figure it out. Phase 2 M4 (smoke test) has been blocked on this since 2026-04-29.

This phase migrates both export scripts to **PEP 723 inline script metadata** with a `uv run --script` shebang. Each script declares its own dependencies in a header block; `uv` resolves them into an ephemeral cached venv on first run and reuses it on subsequent runs. No persistent venv to manage, no machine-specific paths, no pip-vs-system-python contention. install.sh's dependency check collapses to a single `command -v uv` probe.

### M1: `scripts/build_pdf.py` — PEP 723 header + uv shebang ✅

**File:** `scripts/build_pdf.py` (REVISIONE — first 10 lines).

- [x] Replace shebang `#!/usr/bin/env python3` with `#!/usr/bin/env -S uv run --script`.
- [x] Insert PEP 723 metadata block immediately after shebang:
  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = [
  #     "markdown",
  #     "weasyprint>=60",
  # ]
  # ///
  ```
- [x] No code changes. Imports stay as-is.

### M2: `scripts/build_epub.py` — PEP 723 header + uv shebang ✅

**File:** `scripts/build_epub.py` (REVISIONE — first 10 lines).

- [x] Replace shebang `#!/usr/bin/env python3` with `#!/usr/bin/env -S uv run --script`.
- [x] Insert PEP 723 metadata block:
  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = [
  #     "markdown",
  #     "ebooklib",
  #     "pyyaml",
  # ]
  # ///
  ```
- [x] Promote `pyyaml` from optional (`try: import yaml`) to required — it's <100 KB and the conditional-import logic adds noise. Update the body if it has a try/except guard.

### M3: `install.sh` — collapse dependency checks to `uv` probe ✅

**File:** `install.sh` (REVISIONE — replace the MISSING[] block).

- [x] Drop the per-module `python3 -c "import X"` checks for `markdown`, `weasyprint`, `ebooklib`, `pyyaml`.
- [x] Replace with: `command -v uv >/dev/null 2>&1 || MISSING+=("uv (https://docs.astral.sh/uv/getting-started/installation/) — needed for /book pdf and /book epub")`.
- [x] Keep the `python3` check (still needed as fallback / sanity).
- [x] Update the warning text: "Only /book pdf and /book epub need uv; deps are auto-resolved at first run."

### M4: `instructions/pdf.md` + `instructions/epub.md` — drop `python3` prefix ✅

**Files:** `instructions/pdf.md`, `instructions/epub.md` (REVISIONE — invocation lines).

- [x] Replace `python3 ~/.claude/skills/book/scripts/build_pdf.py <args>` with `~/.claude/skills/book/scripts/build_pdf.py <args>` (script self-bootstraps via uv shebang).
- [x] Same for `build_epub.py`.
- [x] Add a one-line note: "First invocation triggers uv to resolve dependencies (cached after); subsequent runs are instant."

### M5: Smoke tests (closes Phase 2 M4) ✅

**Targets:** synthetic minimal markdown (book-1 has no drafted chapters yet — Ch.01 reset by Phase 112 M1).

- [x] Built temp test book at `/tmp/tmp.*/book-1/` with `outline.md` + `ch01.md` (~150 words).
- [x] PDF single-chapter test: `~/.claude/skills/book/scripts/build_pdf.py /tmp/.../book-1 --chapter ch01` → `wrote .../pdf/ch01.pdf`. uv resolved 14 packages on first run. ✅
- [x] EPUB single-chapter: surfaced **two pre-existing Phase 2 bugs** (see M6). Fix landed in M6, then re-tested → `wrote .../epub/ch01.epub` (1965 bytes, 7 internal files: mimetype + container.xml + content.opf + style.css + ch01.xhtml + toc.ncx + nav.xhtml). ✅
- [x] EPUB whole-book: `~/.claude/skills/book/scripts/build_epub.py /tmp/.../book-1` → `wrote .../epub/book-1.epub`. ✅
- [x] uv cache reuse verified — second invocation does not re-download (env reused at `~/.cache/uv/environments-v2/`).
- [x] **Closes Phase 2 M4** (smoke test deferred since 2026-04-29 because of `ebooklib` PEP 668 install issue, now solved by uv self-bootstrap).

### M6: Fix EpubNav empty-content + chapter-content-as-str bugs (closes Phase 2 M4 properly) ✅

**File:** `scripts/build_epub.py` (REVISIONE).

Surfaced by the M5 smoke test — these are **pre-existing Phase 2 bugs** that nobody had ever triggered because nobody had ever run the script (M4 deferred since 2026-04-29).

**Bug 1 — `EpubNav()` empty content.** ebooklib's auto-nav-gen runs at `write()` time, but the `_get_nav` call inside `_write_items` happens before that auto-gen populates content. Modern lxml rejects an empty document body with `lxml.etree.ParserError: Document is empty`. The error was non-fatal (epub still got written), but the resulting nav was missing.

**Bug 2 — `chap.content` set as `str`.** `EpubHtml.content` requires `bytes`. When given a `str`, ebooklib wrote a 0-byte chapter file. Same for the CSS item.

- [x] **Fix 1:** Add `make_nav(items, title) -> epub.EpubNav` helper that builds explicit nav XHTML with TOC ol/li, sets `nav.content` as bytes. Replace `book.add_item(epub.EpubNav())` (both single-chapter and whole-book code paths) with `book.add_item(make_nav([chap], title))` / `make_nav(items, title)`.
- [x] **Fix 2:** Add `.encode("utf-8")` to `chap.content` assignment in `make_chapter_item`. Switch CSS load from `read_text(encoding="utf-8")` to `read_bytes()`.
- [x] Re-tested — both single-chapter and whole-book modes now emit valid EPUBs with populated chapter XHTML and nav.

---

**Phase 5 totals:** 6 milestones. Migrates Phase 1 + Phase 2 scripts to PEP 723 / uv self-bootstrap; surfaces and fixes two pre-existing EPUB bugs along the way. Removes the install.sh PEP 668 footgun. Closes Phase 2 M4 (smoke test, blocked since 2026-04-29).

**Out of scope:** generic uv migration of any future Python tooling — handle case-by-case as scripts are added. The pattern (PEP 723 + `uv run --script` shebang) is now the project's default for standalone Python scripts in this skill.

---

## Phase 6 — Verification-block scope rule (2026-05-06)

Surfaced by ground-truth project DEVPLAN: 17 stale "Pending milestones from Phases X/Y/Z still require application" meta-statements + 13 stale "Apply Phase NN via `/book fix <scope>` — pending" operational items, all referencing phases that had been applied + re-verified clean by subsequent coherence cycles. Root cause: `coherence-check.md` / `continuity-check.md` Step 4 specify the executable milestone template but not the `### Verification & next steps` block, so the model invents that block per phase and propagates prior-phase status forward; `/book fix` closes only `[ ]` checkboxes, never the matching plain-bullet `— pending` operational items.

Fix is two complementary doctrine additions: (a) constrain the verification block to per-phase scope (no transitive forward-looking, no prior-phase restatement), (b) extend `/book fix` to close operational items that name its just-completed invocation.

- [x] **M1**: Add `## Verification & next-steps blocks` section to `instructions/milestone-format.md` codifying three rules — per-phase scope only, no transitive forward-looking unblock claims, `/book fix` closes matching operational items. ✅
- [x] **M2**: In `instructions/coherence-check.md` §4 "Rules for the corrections devplan", add a bullet cross-linking to `instructions/milestone-format.md` §Verification & next-steps blocks. ✅
- [x] **M3**: In `instructions/continuity-check.md` §4 "Write Corrections", add the same cross-link. ✅
- [x] **M4**: In `instructions/fix.md` §2 "Apply Each Milestone", add `Step E — Close Matching Operational Items` describing the scan-and-update logic (match `/book fix <scope>` references in DEVPLAN, update `— pending` → `— done YYYY-MM-DD`). ✅
- [x] **M5**: Reinstall — `cd ~/Documents/software/skills/book && ./install.sh --force`. ✅ (deployed to `~/.claude/skills/book` 2026-05-06)

**Out of scope:** retroactive cleanup of the 30 already-stale markers in the ground-truth project's DEVPLAN. Those will close on the next `/book fix` invocation that touches a phase referenced by them, OR via a one-shot chirurgical edit (separate ask).

---

## Phase 7 — Operational closure across pre-writing commands (2026-05-06)

Surfaced from ground-truth DEVPLAN audit after Phase 6 deployment: `/book fix all` §2.5 closed 20 of 48 residual `— pending` items; 28 remained. Two doctrine gaps:

1. Operational items pointing to non-`/book fix` pre-writing commands (`/book coherence`, `/book continuity`, `/book compact`) have no consumer that closes them — Phase 6 §2.5 deferred to "their own consumers" but those consumers don't exist.
2. Operational items pointing to `/book write` and drafting-unblock state observations leak writing-phase content into the pre-writing ledger. Pre-writing convergence (worldbuilding / coherence-clean) is the prior phase; drafting is a separate ledger and its readiness statements belong in chapter-level state docs, not phase ledgers.

Fix is symmetric across pre-writing commands plus a doctrine ban on write-phase refs.

**Convergence trace.** Post-Phase-7 + post-M6 sweep, `run-coherence-cycle.sh` leaves the ledger clean across cycles:

| Step in cycle | What it closes | New refs it may write |
|---------------|----------------|----------------------|
| `/book coherence <scope>` (0/0/0) | §4.5: own pending refs | only allowed pre-writing refs |
| `/book fix <scope>` | §2.5: own pending refs (+ widened sweep, M5) | n/a — fix doesn't add operational items |
| `/book revise <scope>` (no chapters) | n/a | n/a — no-op until drafting starts |
| `/book continuity X Y` (0/0/0) | §4.5: own pending refs | only allowed pre-writing refs |
| `/book compact <scope>` | §4.5: own pending refs (idempotent) | n/a |

Invariants at convergence (stable across cycles):
- `grep -c "^- \[ \]" DEVPLAN.md == 0` (existing — checkbox count)
- `grep -c "— pending$" DEVPLAN.md == 0` (new — operational-item count)

The cycle script's `count_unresolved_global` already enforces invariant 1. Phase 7 makes invariant 2 self-maintaining.

- [x] **M1**: `instructions/milestone-format.md` §Verification & next-steps blocks — extend rule 2 with explicit allow/ban list. **Allowed** pre-writing refs in operational blocks: `/book fix`, `/book coherence`, `/book continuity`, `/book compact`. **Banned** writing-phase refs: `/book write`, `/book chapter`, `/book sniff`, `/book review`, `/book proofread`, `/book revise` — these belong to a separate writing-phase ledger (chapter-level files: `chapters/<book>/state.md`, SMELL.md, REVIEW.md, PROOFREAD.md). Drafting-unblock state observations ("B1 drafting unblocked once Phase X closes") route to `chapters/<book>/state.md` §Open Threads, never phase ledgers — they are transitive-forward-looking per existing rule 2 and decay silently. Orchestration script refs (`./run-coherence-cycle.sh ...`) are circular in phase ledgers (the script generated the phase) — discouraged; if genuinely needed, use plain bullet without `— pending` (informational, not actionable).
- [x] **M2**: `instructions/coherence-check.md` — add §4.5 "Close Matching Operational Items" mirroring fix.md §2.5. Trigger: invocation produces 0 BLOCKING / 0 WARNING / 0 NOTE actionable findings (the verification semantic). Action: scan DEVPLAN for plain-bullet items matching `/book coherence <scope>` or `Re-run .*/book coherence <scope>` with status `— pending`, update to `— done YYYY-MM-DD`. Scope-aware (matches `all` against per-book scopes per the union rule).
- [x] **M3**: `instructions/continuity-check.md` — same §4.5 pattern for `/book continuity <from> <to>` (or `/book continuity X Y`). Trigger same: 0/0/0 actionable.
- [x] **M4**: `instructions/compact.md` — same §4.5 for `/book compact <scope>`. Trigger: every invocation (compact is idempotent — re-running on a converged state confirms convergence; a fresh run is valid evidence the named compact was performed).
- [x] **M5**: `instructions/fix.md` §2.5 — defensive widen. After the existing pattern matches, if the invocation completes with DEVPLAN at zero unchecked `[ ]`, also sweep `— pending` items in fully-`[x]`-closed phases whose action describes pre-writing work (fix/coherence/continuity/compact/cycle script). Catches edge-case phrasings the literal patterns miss (e.g., `M1 closes via /book fix book-2`, `After M1 applies, ...`). Defensive — should not fire on the happy path post-M1+M6, but provides a safety net.
- [x] **M6**: One-time chirurgical sweep of the 28 residuals in `~/Documents/books/ground-truth/DEVPLAN.md`. Rationale: all 28 reference banned commands per M1 OR describe verifiably-completed actions (commit history + Phase 181 convergence trace). Update each `— pending` → `— done 2026-05-06`. Lines: 247–250, 291, 292, 385, 386, 441, 442, 477, 512, 547, 578, 614, 645, 682, 723, 761, 762, 796, 848, 880, 925, 964, 1003, 1033, 1082.
- [x] **M7**: Reinstall (`cd ~/Documents/software/skills/book && ./install.sh --force`) + commit skill repo + commit project DEVPLAN sweep.

**Out of scope:** writing-phase ledger architecture (separate file? separate top-level section in DEVPLAN.md?). For now, writing-phase state lives in chapter-level files. If a recurring pattern emerges where writing needs its own DEVPLAN section, surface as Phase 8.

---

## Phase 8 — External-world factual-claim guardrails (2026-05-07)

> **Execution mode:** IDD fallback expected, per Phase 3 precedent. Deliverables are markdown LLM-instruction edits; grep-tests would be cargo-cult per `~/.claude/skills/devplan/TDD.md` §1 ("if you cannot articulate a testable user-visible behavior, fall back to IDD").

Surfaced from B1 Ch.01 audit (ground-truth project, 2026-05-07). The chapter passed the writer's 9 verification passes and would have passed coherence-check (canon-internal). Manual reader audit caught four real errors: a hardware-connector direction inverted (HDMI-to-VGA ↔ VGA-to-HDMI), a real-world street name placed in the wrong arrondissement, a French toponym with broken article-preposition contraction (`Rue de Petit Puits` for `Rue du Petit Puits`), and an intra-scene continuity slip on a wrapping cloth.

Three of the four are **assertions about facts external to the project's canon** — real geography, real technology, foreign-language grammar of proper nouns. The skill canonizes its own world meticulously but assumes the writer agent's internal model is reliable for facts not in the canon files. In practice the writer agent confidently produces plausible-sounding-but-wrong specifics in this class. The fourth (cloth) is intra-scene continuity, already covered by sniff §9 — a calibration matter, not a structural gap.

Phase 8 adds three structural guardrails, one per stage of the cycle (prevention, detection, enforcement):

1. **Prevent at draft.** chapter-writer.md self-edit gets an "External-world claim discipline" check (#16).
2. **Detect at sniff.** sniff.md §5 gets an explicit "Real-world factual claim" sub-rubric.
3. **Enforce at proofread.** proof-reader.md P4 gets a foreign-language proper-noun grammar rule.

Generic across the trilogy. Not patching the four specific Ch.01 incidents — patching the class.

**Out of scope (separate trilogy-side concern):** `run-write-cycle.sh` line 574 — flip `needs_thinking` from `0` to `1` for the PROOFREAD step so selective `--ultrathink` flows into proofread. The script lives in the trilogy project, not the skill repo. Will be applied separately project-side after Phase 8 ships.

### M1: chapter-writer.md self-edit — add #16 "External-world claim discipline"

**File:** `instructions/chapter-writer.md` §Step 3.5 Self-Edit Pass (REVISIONE — append item 16).

Insert a 16th item in the numbered self-edit checklist, in the same format as items 1-15. Content: for every concrete real-world assertion in the draft (real place name, technical specification, foreign-language grammar of a proper noun, real physics/biology/medicine/law/finance, real brand or date or currency), the writer agent must classify the assertion as one of:

- **(a) Project canon supports it** — the writer can cite a canonical file (e.g., `world/level-0-reality/...`, `consumer-anchors.md`, etc.). Keep.
- **(b) High-confidence real-world fact** — the writer is confident this is correct external knowledge. Keep, but the assertion is now declared as load-bearing on real-world fact.
- **(c) Cannot verify** — abstract or cut. False precision is more costly than vagueness.

Default rule: when in doubt, cut the specificity. A scene rendered with a generic "the cable" is worth more than a scene rendered with a specific cable model that is wrong.

The check explicitly cross-references sniff.md §5 (where the post-draft detection layer lives). The self-edit is the prevention layer; sniff is the safety net.

- [x] Append item 16 to the numbered list at lines 325-349, matching the existing item format (one short bold lead-in clause, then the rule). ✅
- [x] Item title: **External-world claim discipline (see `sniff.md` §5).** ✅
- [x] Body: 5 lines. Cover the (a)/(b)/(c) classification + the default-to-cut bias + cross-link to sniff §5. ✅
- [x] No examples that name specific Ch.01 incidents (HDMI/VGA, Marseille, etc.) — keep the rule generic across the trilogy. ✅

### M2: sniff.md §5 — explicit "Real-world factual claim" sub-rubric

**File:** `instructions/sniff.md` §5 (REVISIONE — restructure).

Today §5 ("Domain plausibility") names a few expert-reader personas (economist, engineer, doctor, native of the city/region) as a single short paragraph. Restructure §5 into a layered rubric: (a) keep the existing expert-reader framing as the lead, (b) add an explicit sub-rubric "Real-world factual claim audit" that operationalizes it.

The sub-rubric: for every concrete assertion that depends on knowledge external to the project's canon files, the sniff agent classifies into:

- **Anchored in canon** — cite the file. Pass.
- **Real-world verifiable, high confidence** — declare. Pass.
- **Cannot verify / makes friction** — flag. Classification: INLINE if prose-fixable, ANCHOR-NEEDED if the project should canonicalize an in-world override, ACCEPT only with explicit outline evidence.

Categories the agent must scan (generic, not chapter-specific):

- Real-world places: streets, neighborhoods, landmarks, country/city facts, geography, climate facts.
- Specific technology: model numbers, connector types, version numbers, hardware compatibility, software stacks, period plausibility (does this exist at the implied year? is it in actual use at that year? is the chain physically realizable?).
- Foreign-language grammar in proper nouns: when the text names a French / Italian / Spanish / etc. proper noun, the source-language grammar applies (article-preposition contractions, gender agreement, etc.).
- Real-world physics, biology, medicine, law, finance.
- Real brand names, dates, currencies, units.

Calibration note (load-bearing): **specific-sounding details fail at higher rates than their tone suggests.** A writer agent producing "model VGA-to-HDMI converter cable" is not stating a verified fact; it's selecting a plausible-sounding token to add texture. Sniff must treat highly-specific technical assertions with more suspicion than general descriptive ones, because the failure mode is "plausibly worded → plausibly wrong."

- [x] Restructure §5 to have a lead paragraph (existing expert-reader framing, kept) + a sub-rubric "Real-world factual claim audit" with the three-way classification. ✅
- [x] List the 5 categories generically (no Ch.01-specific examples). ✅ (places, technology, foreign-language grammar, physics/biology/medicine/law/finance, brands/dates/currencies/units)
- [x] Add the calibration note about tone-vs-correctness. ✅
- [x] Cross-link forward to §9 (continuity within chapter) and back to chapter-writer.md §3.5 #16 (the prevention layer). ✅

### M3: proof-reader.md P4 — foreign-language proper-noun grammar

**File:** `instructions/proof-reader.md` P4 (REVISIONE — append sub-rule).

Today P4 ("Spelling & Proper Nouns") lists project-canonical proper nouns and flags variants. Add a generic sub-rule: foreign-language proper nouns must respect source-language grammar.

Rule: for proper nouns from non-English source languages — toponyms, institution names, product names — the source-language grammar is normative. The most common slip a model anglophone makes is the article-preposition contraction:

- French: `de + le → du`, `de + les → des`, `à + le → au`, `à + les → aux`. So `Rue de + le Petit Puits → Rue du Petit Puits`.
- Italian: `di + il → del`, `di + lo → dello`, `di + la → della`, `a + il → al`, etc. So `Via di + il Foro → Via del Foro`.
- Spanish: `de + el → del`, `a + el → al`. So `Calle de + el Sol → Calle del Sol`.
- German: noun-gender + case agreement on articles in compound place names.

Also generic: gender agreement, plural forms, accent marks (é, è, à, ñ, ü) must be present where the source language requires them.

The rule applies even when the proper noun is rendered in CAPS (e.g., on an in-world terminal) or surrounded by English-language narration. Capitalization does not exempt the noun from its source-language grammar.

- [x] Append a sub-rule under P4 with the rule + the four example forms (FR / IT / ES + DE gender-case agreement). Generic, not Ch.01-specific. ✅
- [x] Note the in-CAPS / in-English-context exemption-is-not-allowed clause. ✅
- [x] One-line example each, no full case studies. ✅

### M4: Reinstall + commit + push

- [x] `cd ~/Documents/software/skills/book && ./install.sh --force` — deploy to `~/.claude/skills/book/`. ✅ (deployed 2026-05-07; verified via `grep -c "External-world claim discipline"` etc. on the installed copy)
- [x] `git add` modified instruction files + DEVPLAN.md, commit with message describing Phase 8 scope. ✅ (split per-milestone: M1 a887fd3, M2 14f8e88, M3 2ec2879)
- [x] `git push` to skill repo origin. ✅ (pushed after each milestone)

---

**Phase 8 totals:** 4 milestones (3 doctrine + 1 deploy). Adds prevention/detection/enforcement guardrails for one class of failure: external-world factual assertions. Generic across the trilogy. Out of scope: trilogy-side `run-write-cycle.sh` line 574 flip (separate, applied project-side after Phase 8 ships).

---

## Phase 9 — Reviewer flagging discipline: signal-not-noise (2026-05-08)

> **Execution mode:** IDD fallback per Phase 3 / Phase 8 precedent — markdown LLM-instruction edits, no test runner. The "test" of Phase 9 is the next chapter's REVIEW/SMELL output: under the new doctrine, fewer SAFE-CUT findings, some TRADE-OFF findings explicitly surfaced for user decision, and SAFE-KEEP entries acknowledged-but-not-actioned.

Surfaced from B1 Ch.01 cycle 1-3 polish run on the trilogy project (commits `4413287` → `2444c35` → `d7a857b`, 2026-05-08). Three cycles of SNIFF + REVIEW + PROOFREAD + REVISE removed four real factual bugs (HDMI/VGA direction, Marseille streets, French grammar, scarf continuity) — Phase 8 guardrails worked as designed. But the same three cycles also smoothed away the chapter's three sharpest beats: the iconic moka-pot opening, the Mariette-paid-the-contractor backstory paragraph, and the *"He did not look up"* close on the curb fall. Each cut was technically defensible per a style rule (compressed opening is a stative pattern; the backstory paragraph was an em-dash gloss; the line was an aphoristic close). Each cut weakened the chapter.

The cycle is good at finding errors. It's less good at distinguishing problem from voice. The Reviewer's burden of proof is on the wrong foot: today, a rule-violation is automatic flag → REVISE auto-applies. Phase 9 flips it: a rule-violation is flagged ONLY IF removing it improves the chapter; the reviewer must articulate the improvement. If the reviewer can't articulate, no flag. When the reviewer does flag and the affected line is voice-floor (compression, body-first, deliberate violation, named in writing-notes as intentional), classification is TRADE-OFF — surfaced for user decision, NOT auto-applied.

This is *not* a relaxation of standards. It's a higher standard: the Reviewer must *earn* each flag by stating the loss-vs-gain explicitly, not by pattern-matching against rule lists.

Three concrete additions across reviewer/sniff/revise:

1. **Voice-Floor Pass at the start of REVIEW and SNIFF** — first read identifies the chapter's load-bearing beats (compression, surprise, body-first close, deliberate stylization). Marked as VOICE-FLOOR for the second pass.
2. **Three-tier classification** — every flag is classified as SAFE-CUT (rule-violation, removal improves chapter, REVISE auto-applies), TRADE-OFF (rule-violation OR voice-floor candidate, removal has named cost AND named benefit, REVISE does NOT auto-apply, surfaces in `*-PENDING.md`), or SAFE-KEEP (rule-violation but the line is earning its keep — informational, no action).
3. **Pre-step archive** — at the start of each SNIFF/REVIEW/PROOFREAD step, if the existing finding-file is present, rename it to `archive/<NAME>-<timestamp>-<chapter>.md` before writing the new one. Forensic history of polish decisions across cycles.

Plus one Reviewer addition that uses character canon as a positive constraint:

4. **Voice-Signature positive check** — the Reviewer loads `voice-samples.md`, looks for a `§Voice Signature` paragraph per character (4-6 qualities to preserve, e.g. "Noah: short declarative sentences after long compressed ones; ends scenes on absence not summary; never explains his own emotions"), and uses it as a positive checklist. A fix that erodes a Voice-Signature quality is automatic TRADE-OFF, never SAFE-CUT.

Out of scope (project-side, separate concern): authoring `§Voice Signature` paragraphs in the trilogy's `characters/notes/voice-samples.md`. Phase 9 specifies the format and tells the Reviewer how to use it. If the section is missing, the Reviewer notes the gap as a soft warning and falls back to style-rule-only mode (current behavior). That keeps the skill self-consistent on projects that haven't authored signatures yet.

### M1: Reviewer voice-floor pass + three-tier classification + raised flagging bar

**File:** `instructions/reviewer.md` (REVISIONE).

- [x] Insert new step 2.5 (between current "Check Existing Reviews" and "Analyze — 8 Dimensions"): `Voice-Floor First Pass`. Body: read each chapter once before applying rule scans. Identify 3-7 voice-floor beats per chapter — sentences/paragraphs that are doing the heaviest work via compression, surprise, body-first cadence, deliberate violation of style rule for tonal effect, or matching a named technique in `writing-notes.md`. List them in working memory before the rule scan.
- [x] Modify step 3 ("Analyze — 8 Dimensions"): each finding the Reviewer would historically flag must now be tested against three questions before being added to REVIEW.md: (1) does removing this line improve the chapter? articulate the gain in one sentence. (2) what is lost? articulate the loss in one sentence. (3) is the line voice-floor (from step 2.5)? If yes, classification is TRADE-OFF regardless of (1)/(2). If no but (1) > (2), SAFE-CUT. If (1) ≤ (2) or (1) cannot be articulated, SAFE-KEEP.
- [x] Modify step 5 ("Output — The Report"): each entry now carries a Classification: line (SAFE-CUT / TRADE-OFF / SAFE-KEEP). TRADE-OFF entries include explicit `Loss:` and `Gain:` lines. SAFE-KEEP entries are listed in a separate "Acknowledged, no action" block.
- [x] Modify step 6 ("Write the Review Devplan"): only SAFE-CUT items become checkboxes in REVIEW.md. TRADE-OFF items go in a new `## Trade-Off Decisions Pending` section without checkboxes — REVISE will read but not auto-apply. SAFE-KEEP items in `## Acknowledged (No Action)` section.
- [x] Add a Calibration paragraph at the end of step 3: "Most rule-violations in a polished chapter are SAFE-KEEP, not SAFE-CUT. The Reviewer's job is signal, not coverage. If you cannot articulate a one-sentence improvement from removing a line, that line is not a finding."

### M2: Sniff three-tier classification

**File:** `instructions/sniff.md` (REVISIONE).

- [x] In §"The nine objection categories", add a preamble paragraph: each objection must pass the same three-question test as the Reviewer (improvement articulable? loss articulable? voice-floor? → SAFE-CUT / TRADE-OFF / SAFE-KEEP). The existing INLINE/ANCHOR-NEEDED/ACCEPT classification is orthogonal — applies to canon-vs-prose routing, not to flagging discipline.
- [x] In §"Output format — SMELL.md", augment the entry template to include a `Classification: SAFE-CUT | TRADE-OFF | SAFE-KEEP` line alongside the existing `Classification:` (which is INLINE/ANCHOR-NEEDED/ACCEPT). Clarify these are two distinct dimensions: the routing dimension (INLINE/etc) and the flagging-discipline dimension (SAFE-CUT/etc).
- [x] Add Calibration: "An objection that satisfies all nine categories but doesn't improve the chapter when fixed is still SAFE-KEEP. Specificity-feels-wrong is not the same as specificity-actually-wrong-and-fixing-it-helps."

### M3: Revise handles TRADE-OFF — does not auto-apply

**File:** `instructions/revise.md` (REVISIONE).

- [x] In the load-list section, add: read REVIEW.md and SMELL.md TRADE-OFF blocks. These are NOT auto-applied.
- [x] After SAFE-CUT items are applied, write `chapters/<book>/REVIEW-PENDING.md` and `chapters/<book>/SMELL-PENDING.md` containing the TRADE-OFF entries verbatim with `Status: pending — manual decision required` on each. These files are user-facing surfaces; the user reviews and applies (or marks `Status: ✓ Accepted (defer)`) manually before the next cycle.
- [x] In the revise summary output, include a `Trade-Off decisions surfaced: N` line and the path to the *-PENDING.md files. Surface specifically: how many entries pending, location, brief preview.
- [x] In the load-list section, also handle the case where *-PENDING.md exists from a prior cycle: items already present are NOT re-prompted; their state is preserved and re-emitted in the next cycle's *-PENDING.md so the user can accumulate decisions across cycles.

### M4: Pre-step archive for SMELL/REVIEW/PROOFREAD

**Files:** `instructions/sniff.md`, `instructions/reviewer.md`, `instructions/proof-reader.md` (each REVISIONE — small addition at start of process).

- [x] In each of the three skill files, at step 1 (or earliest pre-write step), add: "If `chapters/<book>/<NAME>.md` already exists from a prior cycle, rename it to `chapters/<book>/archive/<NAME>-<YYYYMMDD-HHMMSS>-<chapter>.md` (creating the archive subdir if needed) BEFORE writing the new one. This preserves per-cycle finding history without manual git archaeology."
- [x] Note: the archive lives under `chapters/<book>/archive/` (per-book, not per-project root) so each book's polish history is self-contained.

### M5: Reviewer Voice-Signature positive check

**Files:** `instructions/reviewer.md` (REVISIONE — positive constraint logic), `instructions/init.md` (light update — voice-samples.md format expectation).

- [x] In `reviewer.md` step 1 (Load Reference), expand voice-samples.md handling: read each character's `§Voice Signature` section if present (format: 4-6 bullet lines describing prose-level qualities to preserve, e.g. compression patterns, sentence rhythm signatures, what the character never does, deliberate stylistic moves). If a character's section is missing, note as a soft warning in the report and fall back to style-rule-only review for that character.
- [x] In `reviewer.md` step 3, add a "Voice-Signature drift check" sub-step before the 8 dimensions. For each chapter, scan: does the prose preserve the character's listed voice-signature qualities? If a candidate flag (from rule scan) would erode a voice-signature quality, classification becomes TRADE-OFF automatically — Reviewer cannot SAFE-CUT a fix that breaks character voice signature.
- [x] In `instructions/init.md` (light touch), add: "After voice-samples.md exists, each foreground character should have a `§Voice Signature` paragraph (4-6 prose-level qualities to preserve) — used by reviewer for positive constraint. If absent, reviewer falls back to style-rule-only mode."

### M6: Install + commit + push

- [x] `cd ~/Documents/software/skills/book && ./install.sh --force`
- [x] Stage all instruction edits + DEVPLAN.md, single commit with message describing Phase 9 scope.
- [x] `git push` to origin.

---

**Phase 9 totals:** 6 milestones (5 doctrine + 1 deploy). Raises the Reviewer/Sniff flagging bar from "rule-violation = flag" to "rule-violation that doesn't improve when fixed = SAFE-KEEP". Introduces TRADE-OFF as user-decision channel (not auto-applied). Adds per-cycle archive of finding-files. Adds Voice-Signature positive constraint with graceful fallback if missing.

**Out of scope (project-side, separate phase or done in next chapter prep):**
- Authoring `§Voice Signature` paragraphs in trilogy's `characters/notes/voice-samples.md` for Noah, Lena, Roe, etc. The skill ships the format expectation and the fallback; authoring the actual signatures is a one-time project-side write.

---

## Phase 10 — Engagement gate + saturation finding: closing the "boring chapter ships clean" hole (2026-05-20)

> **Execution mode:** IDD fallback, per Phase 3 / 8 / 9 precedent — markdown LLM-instruction edits, no test runner.

Surfaced from book-1 ch03 (ground-truth project, 2026-05-20 editorial cold-read). ch03 shipped through the full pipeline with `REVIEW.md` verdict *"Roe reads as a person … page-turner 4/5"* and zero Critical/High/Medium/Low findings — while a cold reader (the user) found it boring and incomprehensible. **The pipeline did not miss the defect. Three protection layers, each added by a prior real milestone, suppressed it:**

1. **sniff Category 10** (ground-truth book-1 M14) was built to detect "Stylistic Excess" but calibrated to the wrong failure mode. `sniff.md` line ~232: *"Do not flag a device wholesale ('the chapter uses too many tautologies')."* §10.b writing-notes veto gives a canonized device a "high ceiling." §10.d budget: *"max 1-3 occurrences per device — if you exceed that … recalibrate to default SAFE-KEEP."* The more saturated the defect, the more the check tells itself to back off. M14's calibration success criterion was literally "zero new flags." Cat 10 catches one too-extreme instance (M13's framing); by construction it cannot catch saturation.
2. **reviewer flagging bar** (Phase 9): a voice-floor candidate is classified TRADE-OFF, never SAFE-CUT.
3. **book-tradeoff-arbiter rule 3**: TRADE-OFF + unqualified voice-floor → DEFER. "Pillar beats outrank tightening wins."

On ch03 the reviewer *did* flag the tautology formula and the abstract terminal paradox (`REVIEW-PENDING.md` #1, #2) — both died at arbiter rule 3. Every layer behaved exactly as specified; each was added to fix a real prior over-cut (Phase 9 saved the moka-pot opening). Composed, they are a one-way ratchet toward protection, with no counterforce that measures cumulative reader experience.

Two structural gaps:

- **Gap A — no saturation finding.** sniff Cat 10 is forbidden from raising a wholesale "device X carries the whole chapter" finding.
- **Gap B — no developmental pass.** Every existing check is correctness (sniff 1-9, coherence L-S, continuity) or line-craft (sniff 10, reviewer 8-dimension, proofreader). None asks "is the chapter alive, and is it legible to a reader without the canon files." The reviewer reads WITH all canon loaded — it asserted "Roe reads as a person" because it knows `davan.md`; a first-time reader does not.

### M1: sniff Cat 10 — add the Saturation finding type

**File:** `instructions/sniff.md` (REVISIONE).

- [x] Replace the line-~232 prohibition ("Do not flag a device wholesale") with a licensed, bounded wholesale finding: when a device's total count or max-window density exceeds a threshold, sniff MUST raise exactly ONE chapter-level `SATURATION` finding for that device (the per-occurrence 1-3 budget stays for non-saturation cases). Implemented as new §10.f.
- [x] The Saturation finding is exempt from the §10.b writing-notes veto — writing-notes licenses a device's existence and register, not unlimited saturation. Exemption stated explicitly in §10.b and §10.f.
- [x] Saturation classification is SAFE-CUT-class (structural), not TRADE-OFF — not subject to per-line voice-floor protection (the fix is "vary ~N occurrences," not "delete a pillar beat").
- [x] Threshold defined concretely: Count ≥ 12 OR max 50-line-window density ≥ 6 (calibration-tunable; M4 calibrates against ch01/ch02/ch03).

### M2: book-tradeoff-arbiter rule 3 — saturation carve-out

**File:** `~/Documents/software/skills/book-tradeoff-arbiter/SKILL.md` (REVISIONE).

- [x] Amend rule 3: voice-floor protection applies to per-line / per-beat trade-offs only. An item that is an instance of a device carrying a §10.f `SATURATION` finding in `SMELL.md` is NOT rule-3 deferred — it falls through to rules 4-6. Added `SMELL.md` to the arbiter's read list so it can detect saturation findings.

### M3: New developmental cold-read pass

**Files:** `instructions/coldread.md` (NEW), `SKILL.md` (REVISIONE).

- [x] New `/book coldread` subcommand: a developmental-editor pass that reads the chapter with ONLY prior chapters as context — no outline, no character files, no canon. New subcommand rather than a reviewer pre-step: the defining constraint (canon NOT loaded) is incompatible with `reviewer.md`, which loads voice-samples and character files.
- [x] Five reads per chapter: (1) scene engine — does the POV want something? (2) propulsion — does tension rise? (3) legibility — do the important moments land cold? (4) monotone — is one device carrying the chapter? (5) emotional core — is there one, legible without canon?
- [x] Output `chapters/<book>/COLDREAD.md`; findings carry severity BLOCK / WEAKNESS / NOTE. Developmental findings are NOT auto-applied by `/book revise` — surfaced for the writer; a BLOCK becomes a named rewrite milestone.
- [x] Wired into `SKILL.md` Pipeline: cold-read runs after review, before proofread/revise. Commands table + routing list updated.

### M4: Validate + deploy

- [x] `./install.sh --force` for the `book` skill and the `book-tradeoff-arbiter` skill — both deployed.
- [x] Commit + push the `book` skill repo (commit `d427851`, pushed to `origin/main`). **The `book-tradeoff-arbiter` skill is not under version control** — `~/Documents/software/skills/book-tradeoff-arbiter/` is not a git repo. M2's edit is in the dev tree and installed, but cannot be committed/pushed until the repo is initialized (user decision pending).
- Run the corrected sniff + new `/book coldread` on book-1 ch01, ch02, ch03. Expected: ch03 triggers a tautology `SATURATION` finding + cold-read legibility findings; ch01 and ch02 trigger no false saturation. This is the user-requested re-check of ch01 + ch02 — run with the fixed checks, not the old blind ones. - pending

### M5: coldread — inherited context via per-chapter reader-state snapshots (supersedes M3's "read all prior chapters")

**Files:** `instructions/coldread.md` (REVISIONE — replaces the Context-discipline mechanism); `chapters/coldread-state/` (NEW project-side directory of per-chapter snapshots, created at runtime by coldread).

**Why** (user feedback, 2026-05-20): three linked problems with the M3 cut.

1. **Cost.** M3's context discipline is "read the target chapter + every prior chapter of the book." Cold-reading book-1 ch30 reads 30 chapters; one full-book coldread pass is 1+2+…+30 = 465 chapter-reads; with trilogy-wide reader memory (a book-3 chapter's reader has read ~94 chapters) a single run approaches ~300k input tokens. Trilogy-wide the naive design is ~15M tokens of chapter input and grows superlinearly. Unsustainable.
2. **Fidelity.** Re-reading every prior chapter in full gives the agent *perfect verbatim recall* — which a real reader does not have. A reader at chapter 28 carries a compressed *memory*, not the transcript.
3. **Addressability.** Reader-state is needed *as of a specific chapter* — coldread of chapter N needs the state the reader had *entering* N. A single rolling file holds only the latest state; the moment a chapter is rewritten and re-cold-read (e.g. ch03 under M27), the entry-state it needs has already been overwritten. State must be addressable per chapter.

The fix is one structure, and it is the better reader-model: **per-chapter reader-state snapshots** — `chapters/coldread-state/book-N-chNN.md`, one file per chapter, each holding what a reader *retains* as of the end of that chapter (= the state a reader carries *into* the next chapter). The sequence is book-prefixed and trilogy-continuous (`book-1-ch30` → `book-2-ch01` → …) — reader memory does not reset between books, and neither does the snapshot chain. This answers the cross-3-books concern directly.

**Design:**
- Each snapshot, four content blocks, sized like reader memory — strong retained beats, not a log: **Open loops** (unresolved questions, cliffhangers, ticking clocks); **Character investment** (per major character: how much the reader cares, what they know, current situation — this tells coldread "new POV → zero investment"); **Emotional / thematic throughline**; **Planted-but-unresolved** (setups the reader has registered as load-bearing).
- Built ONLY from chapter texts by coldread itself — never seeded from `state.md`, `outline.md`, or any canon file (the snapshot is strictly reader-side; `state.md` is authorial bookkeeping and includes what the reader does not yet know).
- **Per-run context** = the `book-N-ch(NN-1)` snapshot + the immediately-preceding chapter in full (sharp short-term memory of the handoff) + the target chapter. Bounded ~8-10k tokens regardless of position in the trilogy (~750k trilogy-wide vs ~15M, and flat instead of superlinear). Exactly one snapshot is ever loaded per run; the rest are addressable history at zero context cost.
- **The fold:** after producing findings for chapter N, coldread writes a new snapshot `book-N-chNN.md` = the N-1 snapshot with chapter N's changes folded in (new open loops added, resolved ones closed, character investment updated).
- **Invalidation:** re-cold-reading chapter N rewrites `book-N-chNN.md` and invalidates every later snapshot (each rebuilds when its chapter is re-cold-read); all earlier snapshots are untouched — so re-cold-reading the rewritten ch03 just loads the intact `book-1-ch02.md`.

This supersedes M3's "read every prior chapter" context discipline and subsumes the original M5 intent (credit inherited context): coldread reads the N-1 snapshot *as* its context, so Reads 1-2 judge against inherited state automatically.

- [x] Rewrite `coldread.md` §"Context discipline": per-run context is the `book-N-ch(NN-1)` snapshot + the immediately-preceding chapter in full + the target chapter — NOT all prior chapters. Still NO outline / character / world / plot / canon files.
- [x] Add a snapshot-spec section to `coldread.md`: the four content blocks, the "reader memory not transcript" sizing rule, the build-only-from-chapter-text rule, the separation from `state.md`, the `chapters/coldread-state/book-N-chNN.md` naming.
- [x] Add the **fold step** to the Steps: after writing COLDREAD.md, write the new `book-N-chNN.md` snapshot.
- [x] Bootstrap + ordering rules in `coldread.md`: if the `book-N-ch(NN-1)` snapshot is absent, coldread builds the missing snapshots first by reading those chapters in order (one-time cost); ch01 has no prior snapshot and no prior chapter — true cold open. Document the invalidation rule (re-cold-read N → snapshots after N are stale).
- [x] Recalibrate Read 1 (Scene engine) and Read 2 (Propulsion) to judge as a *continuation* against the snapshot — the engine may be a carried-forward want; propulsion is whether the chapter honors and advances the inherited open loops, not whether it rebuilds stakes from zero.
- [x] Guardrail in the Calibration section: inherited momentum is credited, never an alibi — a chapter that only coasts and advances nothing is still a finding; a new-POV chapter (e.g. ch03/Roe) inherits the book's open loops but zero investment in its POV, so it must do more first-chapter-of-a-character work, not less.
- [x] `chapters/coldread-state/` is committed (consistent with `state.md` / `SMELL.md` — small, makes coldread runs reproducible and inspectable).
- [x] `./install.sh --force` + commit + push the `book` skill. (M5 lands before the M4 validation run, which bootstraps snapshots ch01 → ch02 → ch03.)

**Phase 10 totals:** 5 milestones (4 doctrine + 1 deploy/validate). Adds the one missing counterforce — a saturation finding sniff cannot silence, and a cold developmental pass no canon-aware check can replace, fed by per-chapter reader-state snapshots so it models a mid-book reader (compressed memory, bounded cost, state addressable per chapter) rather than a cold start or a perfect-recall re-read. Out of scope: gating the orchestration scripts (`run-merge-phase.sh`, `run-write-cycle.sh`) on a COLDREAD `BLOCK` — project-side script work, surface as a follow-up phase if wanted.

---

## Phase 11 — Consolidate the book toolchain into one skill (2026-05-20)

> **Execution mode:** IDD fallback, per Phase 3 / 8 / 9 / 10 precedent — markdown LLM-instruction edits, no test runner.

There are four `book-*` skills: `book` (the unified pipeline) plus three satellites — `book-judge`, `book-tradeoff-arbiter`, `book-integrate-anchors`. They are one system: all three satellites are pipeline stages invoked by `run-merge-phase.sh` (the arbiter also by `run-write-cycle.sh`), all share the SAFE-CUT/TRADE-OFF/SAFE-KEEP vocabulary, the `*-PENDING.md` files, and the writing-notes / voice-samples / prose-rules doctrine. The split costs: (1) inconsistent invocation — `/book sniff` but `/book-judge`; (2) `/book help` cannot show the full pipeline; (3) **three of the four are not git repos** — `book-judge`, `book-tradeoff-arbiter`, `book-integrate-anchors` have no version control at all; (4) shared doctrine split across repos — Phase 10 M2 had to reach from `book` into the standalone arbiter to add the SATURATION carve-out.

Consolidate all three into `book` as routed `/book <command>` subcommands. The unified skill keeps the name **`book`** (the `/book` command is load-bearing across 15+ commands and every orchestration script) and its existing repo **`Ymx1ZQ/book-writer`** — the satellites have no repos and no history to preserve, so consolidation needs no new repo. This also closes the Phase 10 M4 open item: the arbiter is not given its own repo — it is absorbed into `book`, which is versioned.

### M1: Absorb book-tradeoff-arbiter → `/book arbiter`

- [x] Move `book-tradeoff-arbiter/SKILL.md` content → `book/instructions/arbiter.md` (carries the Phase 10 M2 saturation carve-out, already present in the standalone file).
- [x] `book/SKILL.md`: add command-table row `arbiter <book> <ch>`, add routing `arbiter → instructions/arbiter.md`, add the stage to the pipeline diagram (merge-phase auto-resolution of `*-PENDING.md`).
- [x] Claude-only — every invocation is via `$CLAUDE`; no model variant needed.

### M2: Absorb book-integrate-anchors → `/book integrate-anchors`

- [x] Move `book-integrate-anchors/SKILL.md` → `book/instructions/integrate-anchors.md`; fold `book-integrate-anchors/README.md` into `book/README.md` (or the instruction header).
- [x] `book/SKILL.md`: command-table row + routing + pipeline-diagram stage.
- [x] Claude-only.

### M3: Absorb book-judge → `/book judge` (cross-CLI — the one wrinkle)

`book-judge` is invoked under BOTH `$CLAUDE` (`run-merge-phase.sh` lines 139, 144) and `$CODEX` (line 157) and ships two model variants: `claude/SKILL.md` + `codex/SKILL.md`.

- [x] Move the two variants → `book/instructions/judge/claude.md` + `book/instructions/judge/codex.md`, preserving the model split; fold `book-judge/README.md` into `book/README.md`.
- [x] `book/SKILL.md`: command-table row `judge <manifest> <outpath>` + routing — Claude invocations route to `instructions/judge/claude.md`.
- [x] Inspect `book-judge/install.sh` for its codex-side install path; extend `book/install.sh` so it also installs the codex-side `book` skill (at minimum the `judge` command + `instructions/judge/codex.md`) into Codex's skill location, so `/book judge` resolves under `$CODEX` — preserving book-judge's current cross-CLI capability. This is the one non-trivial part of the consolidation.

### M4: Retire the satellites

- [x] Confirm `book/install.sh` installs every new file (the three new instructions, the `judge/` subdir, the codex side). Discard the three satellites' `install.sh`.
- [x] Delete dev-tree dirs `~/Documents/software/skills/book-{judge,tradeoff-arbiter,integrate-anchors}/` and their installed copies `~/.claude/skills/book-{judge,tradeoff-arbiter,integrate-anchors}/` (plus the codex-side `book-judge`).
- [x] The satellites carry no DEVPLAN files — nothing to merge into `book/DEVPLAN.md`.

### M5: Update orchestration scripts (project-side — `ground-truth` repo; must land atomically with M6)

The scripts invoke the old skill names; they break the instant the satellites are retired, so this milestone is committed together with M6.

- [x] `run-merge-phase.sh`: `/book-judge` → `/book judge` (lines 139, 144, 157), `/book-integrate-anchors` → `/book integrate-anchors` (347), `/book-tradeoff-arbiter` → `/book arbiter` (391); update the banner/comment lines (9, 11, 232, 235, 345, 378).
- [x] `run-write-cycle.sh`: `/book-tradeoff-arbiter` → `/book arbiter` (line 597; comment line 592).
- [x] `aggregate-judges.sh`: update the comment path reference `~/.claude/skills/book-judge/SKILL.md` → `~/.claude/skills/book/instructions/judge/` (lines 4-5 — comment only, no invocation).

### M6: Deploy + commit

- [x] `./install.sh --force` from `book/`.
- [x] Smoke-test: `/book help` lists `judge`, `arbiter`, `integrate-anchors`; the dispatcher resolves each to its instruction file.
- [x] Commit + push the `book` skill repo (`book-writer.git`). Commit the M5 orchestration-script changes to the `ground-truth` repo — atomically with the skill deploy so the merge phase is never in a broken intermediate state.

**Phase 11 totals:** 6 milestones. Collapses four `book-*` skills into one routed skill — uniform `/book` invocation, one repo, one install, one version, shared doctrine co-located. Closes the Phase 10 M4 arbiter-versioning limbo. One non-trivial part: M3's cross-CLI judge install.

**Implementation note (2026-05-20):** the judge model-variant layout deviates slightly from M3's stated paths, for cleanliness — the Claude judge instruction is `instructions/judge.md` (dispatched by `/book judge`); the Codex variant is `codex/SKILL.md` + `codex/agents/openai.yaml` (the codex install payload), rather than an `instructions/judge/` subdir. `book/install.sh` is dual-target: Claude → `~/.claude/skills/book/`, Codex → `~/.codex/skills/book/`. Satellite READMEs were not folded — their content is redundant with each instruction file's own intro. All three satellites retired from the dev tree and from the installed Claude/Codex skill paths. Phase 11 deployed and verified; M5 orchestration-script edits committed to the `ground-truth` repo.

---

## Phase 12 — coldread severity calibration: legibility is conditional on engagement (2026-05-21)

> **Execution mode:** IDD fallback, per Phase 3 / 8 / 9 / 10 / 11 precedent.

Surfaced from M4 validation (book-1 ch03, 2026-05-21). The user's lived reaction to ch03 was BLOCK-grade — *"pallosissimo e neanche capisco cosa sta succedendo"* (boring; could not follow the plot). `/book coldread` rated ch03 **0 BLOCK / 1 WEAKNESS / 2 NOTE**, cold verdict *"qualified yes — the chapter works."* It assigned **the same severity profile to all three chapters** (ch01, ch02, ch03 each 0 BLOCK / 1 WEAKNESS) — it could not discriminate the chapter a real reader bounced off (ch03) from the two they did not (ch01, ch02).

coldread's *diagnosis* was sharp — finding #1 correctly identified that ch03's opening third structurally re-runs ch02 (déjà vu) — but two calibration faults:

1. **It judged the Davan / empty-stool emotional core "a live wire that works"** (Read 3, Legibility). The user, a real reader, did not register it ("only understood the stone in the boot"). Root cause: coldread reads cold (no canon) but still reads *attentively* — it recovers buried meaning by connecting dots a disengaged or uninvested reader skips. Legibility is being judged as "can an attentive agent recover it," not "will a reader at this engagement level register it."
2. **Severity undercalls.** The persona says "you put the book down if bored," but the agent's actual reading never degrades, so the verdict never reaches BLOCK on a chapter a real reader would abandon.

### M1: bind the coldread verdict to lived reader experience

**File:** `instructions/coldread.md` (REVISIONE).

- [ ] Read 3 (Legibility): when Read 2 (Propulsion) finds a slog/slack stretch, meaning that is *technically present but buried* in that stretch is a legibility **finding**, not a pass — a reader whose attention the chapter has lost will not do the connective work. Reframe the test: "will a reader at this engagement level register it," not "can an attentive agent recover it."
- [ ] Severity: a chapter whose emotional core is present-but-buried-under-a-slog, or that a real reader would disengage from before the payoff, escalates toward BLOCK even when every element is technically on the page. The persona's "you put the book down if bored" must bind the verdict, not merely color the prose.
- [ ] Calibration section: add — the agent must not let its own attentiveness paper over a real reader's inattention; the test is the median reader's lived experience, not the diligent agent's recovery. If the same severity would land on a chapter that pulls and one that drags, the rubric is not discriminating — re-judge.
- [ ] `./install.sh --force` + commit + push.

**Phase 12 totals:** 1 milestone. M4 validated the saturation finding (Phase 10 M1) cleanly; it also surfaced that coldread, while diagnostically sharp, undercalls severity because it cannot model a real reader's degraded attention. This milestone binds the verdict to lived reader experience.
