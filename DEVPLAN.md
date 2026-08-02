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

## Phase 12 — coldread severity calibration: a balanced, discriminating verdict (2026-05-21)

> **Execution mode:** IDD fallback, per Phase 3 / 8 / 9 / 10 / 11 precedent.

Surfaced from M4 validation (book-1 ch03, 2026-05-21) and the user's follow-up directive: coldread *"deve essere equilibrato — non voglio che faccia modifiche a cazzo ma neanche lasciar sempre perdere."* The verdict must be a **trustworthy signal**: when coldread says BLOCK we act, when it says NOTE we leave it, and the WEAKNESS between is a genuine judgement call — neither reflexive rewriting nor reflexive shrugging.

The M4 evidence was an **under-call**: the user's lived reaction to ch03 was BLOCK-grade ("pallosissimo e neanche capisco cosa sta succedendo"), but `/book coldread` rated it 0 BLOCK / 1 WEAKNESS, "qualified yes," and gave **the same severity profile to all three chapters** — it could not discriminate the chapter a real reader bounced off from the two they did not. Root cause: coldread reads cold (no canon) but still reads *attentively* — it recovers buried meaning a disengaged reader skips, and judged ch03's Davan core "a live wire that works." But the fix must not over-correct into reflexive harshness: a texture observation must stay a NOTE. The target is a severity ladder where BLOCK / WEAKNESS / NOTE are genuinely different claims, each tracking the median reader's lived experience.

### M1: make the coldread verdict discriminating and balanced

**File:** `instructions/coldread.md` (REVISIONE).

- [x] Read 3 (Legibility): when Read 2 (Propulsion) finds a slog/slack stretch, meaning *technically present but buried* in that stretch is a legibility **finding**, not a pass — a reader whose attention the chapter has lost will not do the connective work. The test: "will a reader at this engagement level register it," not "can an attentive agent recover it."
- [x] Severity, against **under-call**: a chapter whose emotional core is present-but-buried-under-a-slog, or that a real reader would disengage from before the payoff, escalates toward BLOCK even when every element is technically on the page. The persona's "you put the book down if bored" must bind the verdict, not merely colour the prose.
- [x] Severity, against **over-call**: BLOCK / WEAKNESS / NOTE are a real ladder — a texture observation, a forward-looking craft note, an accumulation watch-point are NOTEs and stay NOTEs; coldread must not inflate severity to manufacture findings, and must not flag a chapter that genuinely pulls. Over-calling burns the verdict's trust as surely as under-calling.
- [x] Discrimination test (Calibration section): if the same severity would land on a chapter that pulls and one that drags, the rubric is not discriminating — re-judge. The agent must not let its own attentiveness paper over a real reader's inattention; the test is the median reader's lived experience.
- [x] Codify the **act / don't-act doctrine** in coldread.md so coldread is balanced *in use*, not only in wording: coldread NEVER edits prose — it has no auto-apply path, so it structurally cannot "make changes haphazardly"; a **BLOCK** must become a named rewrite milestone, authored deliberately — never silently dropped; a **WEAKNESS** is surfaced for the writer's deliberate craft decision — neither auto-acted nor auto-ignored; a **NOTE** is recorded only. The severity *is* the act/don't-act signal — which is why it must be calibrated.
- [x] `./install.sh --force` + commit + push.

**Phase 12 totals:** 1 milestone. M4 validated the saturation finding (Phase 10 M1) cleanly and surfaced that coldread under-calls. This milestone makes the verdict discriminating in **both** directions — so a BLOCK is acted on, a NOTE is left alone, and coldread is a trustworthy signal rather than a reflex toward either rewriting or shrugging.

---

## Phase 13 ✅ — Gap-coverage checks: readability/flow, motif, factcheck, sensitivity (2026-05-28)

> Close-out note 2026-07-25: these checkboxes were left unticked when the work
> shipped (May 2026). Verified today item-by-item: all four instruction files
> exist with their Audit sections, register/VERIFY/advisory-first/two-channel
> features present, SKILL.md rows + pipeline order in place, revise.md Source
> enumeration extended. Ticked retroactively after verification.

> **Execution mode:** IDD fallback, per Phase 3 / 8 / 9 / 10 / 11 / 12 precedent.
> **Paired with:** project `ground-truth` DEVPLAN **Phase 42** (pipeline wiring + clean QC re-run). This skill phase builds the four new detectors; Phase 42 wires them into the orchestrators and re-runs them on Book 1.

**Status: COMPLETE (2026-05-29).** All four detectors (`readability`, `motif`, `factcheck`, `sensitivity`) authored, SKILL.md dispatch + pipeline order updated, `revise.md` `Source:` enumeration + `VERIFY` handling extended, deployed via `./install.sh --force`, and smoke-validated through the live Book-1 ch01–ch04 QC re-run (Phase 42 operational). M1–M6 done.

The audit of the pipeline (2026-05-28) found the QC matrix exhausts the *enumerable* defects but leaves four machine-addressable gaps uncovered, plus the user's explicit new requirement: the book must stay **scorrevole** — a brick is a defect except where a heavy register is *deliberate*. Two further gaps (beat↔voice alignment, adaptive beta-reader "why would a reader care?") stay HUMAN by nature and are out of scope. Each new detector follows the existing two-channel routing (canon → DEVPLAN milestone via `fix`; prose → `SMELL.md` INLINE via `revise`) and the voice-floor protection doctrine — **none of these may flatten an intended voice.**

> **Integration design (refined 2026-05-29 — chosen over separate artifact files).** The four detectors do **not** introduce new artifact files (no `READABILITY.md`/`MOTIF.md`/…). They append prose-side findings to the shared **`SMELL.md`** sink with a `Source: <detector>` tag (exactly as `coherence`/`continuity` already do), plus a per-detector transparency **audit section** appended to `SMELL.md` (mirroring sniff's "Stylistic Device Audit"). Canon-side findings append a phase to `DEVPLAN.md` for `/book fix`. Consequence: `revise` (consumes SMELL.md uniformly by `Source:`), `arbiter` (resolves `SMELL-PENDING.md`), and `sweep` (archives `SMELL.md`/`SMELL-PENDING.md`) need **zero logic changes** — only a one-line `Source:` enumeration mention in `revise.md`. This is strictly more consistent with `world/canon-hierarchy.md` two-channel doctrine than separate files would be.

### M1: `instructions/readability.md` — register-aware flow pass (→ SMELL.md, `Source: readability`)

- [x] New detector. Reads `world/tones.md`, `world/prose-rules.md`, `world/writing-checklists.md`, and `characters/notes/voice-samples.md` to map which narrative levels/sections carry an **intended-heavy** register vs the **default** register.
- [x] Flags only *accidental* brick outside intended-heavy registers: run-on sentence-length streaks, clause-stacking / subordinate-clause depth, referential overload (antecedent density per paragraph), unbroken exposition blocks, paragraph mass, un-glossed-term density at reading speed.
- [x] Every finding tagged `Register: default | intended-heavy`. Only `default`-register findings become INLINE (SAFE-CUT / TRADE-OFF); `intended-heavy` stretches downgrade to ACCEPT/SAFE-KEEP so deliberate density is never penalised. Inherits voice-floor protection (a finding that would erase a voice signature is a TRADE-OFF, never auto-cut). Always emits a "Readability / Flow Audit" section in SMELL.md (sentence-length & paragraph-mass metrics per scene) for transparency, even at zero flags.

### M2: `instructions/motif.md` — symbolic / motif coherence (→ SMELL.md prose / DEVPLAN canon)

- [x] New detector. Reads `plot/motif-tracking.md`, `plot/prestige-inventory.md`, and plant/payoff tracking. Per motif instance: checks direction (motif not used *inverted* vs its established meaning), that any evolution is intentional, and payoff alignment.
- [x] Two-channel routing: canon drift (motif meaning contradicts the tracker) → DEVPLAN milestone for `fix`; prose-side misuse → `SMELL.md` INLINE (`Source: motif`) for `revise`. Conservative: an ambiguous symbolic reading is SAFE-KEEP, not a flag. Emits a "Motif Coherence Audit" section listing every tracked motif's instances and verdict.

### M3: `instructions/factcheck.md` — active real-world accuracy (→ SMELL.md / DEVPLAN / VERIFY-PENDING)

- [x] New detector that **extends, does not duplicate**, Phase 8's reactive in-prose factual-claim flag inside `sniff`. `sniff` stays the reactive guardrail; `factcheck` is the dedicated batch verifier: extract real-world claims → verify against `world/timeline.md` (tech-chains coherent with the in-world year), geography, physics/medicine/law/finance.
- [x] Auto-resolvable canon contradictions route to DEVPLAN/SMELL normally; non-machine-verifiable claims become `Flagging: VERIFY` entries surfaced to `SMELL-PENDING.md` for human/web confirmation rather than silent auto-edits. Emits a "Fact-Check Audit" section (claim → bucket: anchored / verified / VERIFY).

### M4: `instructions/sensitivity.md` — stereotype / dated-language / representation (→ SMELL.md, advisory-first)

- [x] New detector, conservative and advisory-first: stereotypes, caricature, dated or ableist language, representation gaps. Findings default to `SMELL-PENDING.md` (TRADE-OFF) for human decision; only unambiguous dated-term swaps may auto-apply (SAFE-CUT). Reads `characters/notes/narrator-boundaries.md` to respect per-POV constraints. Emits a "Sensitivity Audit" section.

### M5: SKILL.md — dispatch, routing, pipeline order

- [x] Add commands-table rows for `readability`, `motif`, `factcheck`, `sensitivity`; add their `instructions/<cmd>.md` entries to the Execution routing map.
- [x] Update "The Pipeline" writing-loop order to: `write → sniff → factcheck → review → motif → sensitivity → coldread-enum → coldread-filter → readability → proofread → revise → snapshot`. (Readability runs late, just before proofread, so it judges near-final prose; factcheck early next to sniff; motif/sensitivity in the editorial cluster.)

### M6: consumer doc-touch — revise.md

- [x] `instructions/revise.md`: extend the `Source:` enumeration (currently `sniff` / `coherence` / `continuity`) to also list `readability` / `motif` / `factcheck` / `sensitivity`, and add `VERIFY` alongside the SMELL flagging values that surface to `SMELL-PENDING.md`. **No logic change** — processing is already uniform by `Source:`. `sweep.md` and `arbiter.md` are unchanged (they already operate on `SMELL.md` / `SMELL-PENDING.md` generically).

**Operational (run after the milestones above):**
- `./install.sh --force` from the skill dev tree to deploy (never edit the installed copy).
- Smoke test each new subcommand once on `ground-truth` book-1 ch01; confirm each appends correctly-`Source`-tagged SMELL.md entries + its audit section, and the `Register:` tag (readability) behaves on a known intended-heavy passage.

## Phase 14 — Close the two cold-read defect-detection gaps: register-leak detection + cross-chapter adjacency (2026-05-29)

> **Execution mode:** IDD fallback, per prior precedent.
> **Paired with:** project `ground-truth` DEVPLAN **Phase 44** (wires the adjacency detector into `run-merge-phase.sh` over the [prev, current] window).

**Trigger.** A human cold-read of Book-1 ch01–ch04 (project Phase 43) surfaced three defect classes; the user asked which the pipeline catches on its own. Audit answer: of the three, **one is prevented at write time but not detected post-hoc, and two are structurally invisible to the per-chapter QC matrix.**

| Defect class | Example | Pipeline status BEFORE Phase 14 |
|---|---|---|
| 1. Register leak (cross-level narrator tic, e.g. "X was the X" tautology in a Reality chapter) | ch04 | **Prevented** at write time (`chapter-writer` loads `register-locks.md` as a hard constraint) but **undetected** post-hoc — `readability` read only `tones.md`, not the explicit forbidden-pattern list, so a leak that slips the writer ships clean (this is exactly why ch04's leaks survived the Phase 42 QC re-run; only the human caught them). |
| 2. Idiolect collision | the same involuntary-body formula ("without deciding") reused verbatim across Noah / Lena / Roe, flattening three canon-distinct idiolects | **Invisible** — every analyst is per-chapter; none compares POV voice signatures across chapters. |
| 3. Shape-repetition / dramatic-irony-not-landing | ch03 reads as a repeat of ch02 because the ch02→ch03 braid (Lena deletes Roe's record; `BA-009` is the shared junction) is unsignposted, so the first dramatic irony is inert | **Invisible** — no analyst reads consecutive chapters together or checks a planned `reader-journey.md` irony for legibility. |

**Decision.** Class 1 → close the **detection** gap by wiring `register-locks.md` into the `readability` detector (B-i). Classes 2 & 3 → build a new **cross-chapter adjacency** detector (B-ii). Classes 2 & 3 remain *partly* human by nature (irony-landing is a reader judgment); the detector raises the floor — it flags the candidates a human would otherwise have to catch unaided, and routes the *structural* (un-auto-fixable) ones to a DEVPLAN/PENDING channel for the user, never auto-reshaping a chapter.

### M1 (B-i): wire `register-locks.md` into `readability` — register-leak detection

- [x] `instructions/readability.md` Step 0: additionally load `world/register-locks.md` §<this chapter's level> and extract its **Forbidden patterns** list (the explicit phrase/pattern catalog, e.g. Reality's "X was the X" tautologies + compliance-system vocabulary).
- [x] Add **Category 0 — Register leak** ahead of the six flow categories: a literal/near-literal scan for this level's forbidden patterns. A hit is a **breach, not a trade-off** → `SAFE-CUT` / `INLINE` (the leak is removed; it is never SAFE-KEEP, because register-locks already encodes the intent). Distinct from the flow categories, which stay register-gated.
- [x] The Flow Audit section gains a one-line "Register-leak scan: N hits against register-locks §<LEVEL>" so the scan is visible even at zero hits.

### M2 (B-ii): new `instructions/adjacency.md` — cross-chapter detector

- [x] New analyst. Reads a **window of consecutive chapters** (default: the just-written chapter + its immediate predecessor) plus `plot/reader-journey.md` (intended reader-knowledge / dramatic-irony per chapter), `characters/notes/voice-samples.md` + `narrator-boundaries.md` (per-POV distinct idiolects), and `plot/motif-tracking.md` (level per chapter).
- [x] Flags three classes, each with a high burden of proof: **(a) shape repetition** — adjacent chapters share too-close a beat-skeleton without the rhyme being load-bearing; **(b) idiolect collision** — a signature device/phrasing reused verbatim across different POV characters where canon assigns each a distinct tic; **(c) dramatic-irony legibility** — where `reader-journey.md` declares an irony/reader-knowledge state for the pair, check the prose actually makes it legible to a first-time reader.
- [x] **Two-channel + three-tier routing.** Prose-side micro-fixes (idiolect reword; a one-line bridge to light an irony) → `SMELL.md` (`Source: adjacency`), INLINE/SAFE-CUT or TRADE-OFF. **Structural** findings (deep beat-order reshape) are **never auto-applied** — they route to a `DEVPLAN.md` phase / `SMELL-PENDING.md` for the **user**, honoring the "don't hand-reshape QC-closed chapters" doctrine. Emits an "Adjacency Audit" section (window, per-pair verdicts).
- [x] Conservative calibration: a load-bearing parallel (deliberate cross-caste mirror that *serves* an irony) is SAFE-KEEP, not a flag. The detector's job is to catch the *inert* rhyme and the *unlit* irony, not to sand away authored structure.

### M3: SKILL.md + revise.md consumer touch

- [x] SKILL.md: add `adjacency` command-table row + routing-map entry; insert into "The Pipeline" order (adjacency runs at batch/window level, after per-chapter QC).
- [x] `instructions/revise.md`: add `adjacency` to the `Source:` enumeration (no logic change — uniform by `Source:`).

### M4 (B-i hardening): deterministic register-leak linter — the reliable backbone of Category 0

> **Trigger:** the Phase-44 M3 cold validation empirically showed the `readability` LLM Category-0 scan reporting a Reality chapter "clean" while MISSING `the lines were the lines` (a leak a one-line grep caught instantly). Literal-pattern detection must not depend on LLM judgment.

- [x] `scripts/register_leak_lint.py` — zero-LLM, deterministic. Implements the machine-checkable subset of `register-locks.md`: the "X was the X" stasis-tautology family (4 regex forms covering all documented examples — noun-repeat, where-the-X, kept-its-X, where-pronoun-had) + the compliance-vocabulary blocklist, gated per level (Reality/Ark check; Dome has none — its forbidden list is semantic). `--level` arg; exit 1 on any hit. `not`-guard avoids false positives like "was not the voice he had meant".
- [x] `instructions/readability.md` Category 0: run the linter FIRST as the authoritative backbone (every `LEAK` line → SAFE-CUT entry), THEN the LLM semantic scan for what the linter cannot catch (warmth-in-Dome, agency-erasure, apophatic 4+). Deterministic for the literal, LLM for the semantic.

**Operational:**
- [x] `./install.sh --force` from the skill dev tree to deploy.
- [x] Smoke test the linter: against pre-fix ch04 (git 7f32e4d) it must flag the documented tautologies; against current ch04 it must report 0; against a Dome chapter it must report "no deterministic patterns".
- Orchestrator wiring (adjacency over [prev,current] at `run-merge-phase.sh` step 8.5a3) lives in project Phase 44 (the script is in the project repo).

## Phase 15 — Engineering-hygiene parity: tests, frontmatter, installer --check, CI (2026-06-10)

Brings `book` to the engineering-hygiene bar the code-audit / devplan / deck
skills reached this session. **Not** in scope: the broad multi-assistant
installer (book is a Claude-Code-native 25-command pipeline; the codex side is
deliberately just the `judge` lane — opencode/gemini can't run the pipeline, so
forcing them would be cargo-culting). No flatten (already flat).

### M1 — Test suite (the #1 gap: the largest skill has zero tests)

> **Trigger:** `register_leak_lint.py` is a deterministic regex linter with an
> exit-code contract and a documented motivating bug (`the lines were the lines`
> slipped past the LLM) — a textbook unit-test target — yet nothing tests it,
> and the two PEP723 build scripts and the installer have no smoke either.

- [x] `tests/test_register_leak_lint.py` — pytest: a Reality fixture with `the X was the X` → exit 1 + the leak printed; a clean Reality fixture → exit 0; the `not`-guard negative case stays clean; a Dome chapter → "no deterministic patterns" (exit 0); the `--level` arg gating (Reality/Ark check, Dome skips).
- [x] `tests/test_build_scripts.py` — the two PEP723 scripts parse and expose `--help` without importing heavy deps (invoke `python3 build_pdf.py --help` / `build_epub.py --help`, or assert the `# /// script` block + argparse usage parse); skip the real render if `uv` absent.
- [x] `tests/test_install.sh` — bash smoke: install to a temp HOME with `--force`; assert `SKILL.md`, `instructions/`, `scripts/`, the codex `judge` variant landed, and the build scripts are executable.

**Operational:**
- [x] `pytest tests/ -q` green locally; `bash tests/test_install.sh` green.

### M2 — Root SKILL.md frontmatter (agentskills.io standard)

- [x] Add YAML frontmatter (`name: book` + a `description` covering the pipeline + the `/book <command>` surface) to the root `SKILL.md`, matching the codex variant and the other skills. Body unchanged.

**Operational:**
- [x] `./install.sh --force` redeploys; `/book help` still routes.

### M3 — Installer hygiene parity (`--check` + SHA stamp)

- [x] `install.sh --check` — compare the installed claude payload (SKILL.md + instructions/ + scripts/) and the codex judge variant against source; report `OK`/`DRIFT` per side, exit 1 on drift or missing. No writes.
- [x] On install, stamp `.installed-from` with the source git short SHA (both claude + codex dests).
- [x] `tests/test_install.sh` extended: `--check` clean after install; drift detected on a hand-edited installed file.

### M4 — CI: run the test suite on push

- [x] `.github/workflows/tests.yml` (`checkout@v5`, ubuntu-latest): install pytest, run `pytest tests/` + `bash tests/test_install.sh`. uv/weasyprint not required (build-script tests are `--help`/parse only). README CI note.

**Operational:**
- [x] Push; confirm the run is green.

## Out of scope for Phase 15

- Multi-assistant installer beyond claude + codex(judge) (by design).
- De-hardcoding `~/.claude/skills/book/` paths (book is Claude-native; defensible).
- Content/prose-pipeline changes (separate review).

## Phase 16 — Content doc-correctness: wrong-consumer, dead refs, stale counts, PENDING contradiction, human-gate marker (2026-06-10)

From the Phase-15 content audit. Documentation-correctness only — no prose-rule
changes. Closes the 3 🔴 + the stale-count / cross-ref 🟡 the audit surfaced.

### M1 — proof-reader routes to the wrong consumer (🔴)

- [x] `proof-reader.md`: every `/book fix` → `/book revise` (PROOFREAD.md is applied by revise, not fix — `fix.md:139` never touches prose). Lines 175, 201, 216, 227; drop the spurious "Devplan milestones created: X" (210 — proofread writes no DEVPLAN milestones).

### M2 — dead instruction reference in sweep (🔴)

- [x] `sweep.md:62`: `instructions/coldread.md` → `coldread-enum.md` + `coldread-filter.md`. Fix `:15` "rotate-on-write" wording for coldread (coldread-enum overwrites COLDREAD.md, does not rotate).

### M3 — PENDING/arbiter contradiction made consistent (🔴)

- [x] Reconcile the two models: orchestrated/merge pipeline → PENDING resolved by `/book arbiter` (autonomous, Phase 42); bare `/book revise` run standalone → PENDING left for the user. Update `revise.md` ("User reviews and applies manually" → the two-path framing) and add an arbiter note to the SKILL.md writing-loop so the linear flow's PENDING producers have a documented consumer.

### M4 — stale counts + arbiter field description (🟡)

- [x] `reviewer.md`: "8 Dimensions" → "13 Dimensions" (A–M); "Rules 13-25" → "Rules 13-28" (26 exposition-economy, 27 reality-plausibility, 28 register-lock exist).
- [x] `arbiter.md`: `Source:` field names the *detector* (sniff/coherence/…), not the filename — fix `:70`; "7 strongest beats"/"pillar 7" → "the 3–7 voice-floor pillar beats" (`:38`, `:75`) to match sniff/reviewer.
- [x] `judge.md`: model id `claude-opus-4-7` → `claude-opus-4-8` (`:117`, `:145`).
- [x] `milestone-format.md` "Used by" list: add factcheck, motif, adjacency, sensitivity, readability.

### M5 — human cold-read marker in chapter-writer (🔴, paired with ground-truth)

- [x] `chapter-writer.md` Step 8 "Mark Complete": the close marker becomes `- [x] Ch. NN — Title (Level / POV) ✅ machine-checked — awaiting cold-read`, and the step states a chapter is NOT human-validated until a human removes the `awaiting cold-read` tag (per SKILL.md:96). Defines the convention the ground-truth scripts consume.

**Operational:**
- [x] `pytest tests/` + `bash tests/test_install.sh` still green (no code changed); `./install.sh --force` redeploy.

## Phase 17 ✅ — Graph-assisted recall (graphify) + per-command model guidance (2026-07-25)

Two goals from the user: (1) each pipeline step should run on the right model tier
(Opus vs Sonnet) — script-side wiring lives in the project repo (ground-truth
DEVPLAN Phase 80); the skill documents the per-command recommendation. (2) The
skill should use a project's graphify knowledge graph, where one exists, to
replace bulk canon loading with targeted queries — cutting per-step token cost
and giving steps step-by-step recall of plants, threads, tracker assignments,
and cross-references.

Evidence base (measured on ground-truth, ~587k-word corpus): `chapter-writer`
Step 1 loads 130-140k tok before drafting (ch01 `context:` tag alone = 31 files
≈ 80k tok); `coherence all` worst-case ≈ 385k tok; `motif` re-reads all prior
chapters (unbounded); `continuity` is 100% relational. Graph queries over
`graphify-out/graph.json` (1,928 nodes / 2,920 edges) answer the relational
part at near-zero token cost.

**Design invariants (all milestones):**
- **Opt-in per project.** Graph use activates ONLY if `graphify-out/graph.json`
  exists in the project root. Absent → every instruction behaves exactly as
  today. The skill stays project-agnostic; no ground-truth specifics hardcoded.
- **Index mode vs answer mode.** Index mode (default, staleness-tolerant): the
  query returns file/§ pointers; the agent reads the pointed-to sections from
  disk — the graph navigates, the file is the truth. Answer mode
  (staleness-strict): the query result is consumed directly (plant/payoff
  tables, thread lists); allowed only when the freshness gate passes.
- **Freshness gate.** Compare `built_at_commit` in graph.json against
  `git rev-parse HEAD`; if they differ, list changed `.md` files under `world/
  characters/ plot/ chapters/`. Empty diff → fresh. Non-empty → answer-mode
  queries require an incremental graph update first (`/graphify --update`
  flow) or fall back to file loading; index-mode queries may proceed but every
  pointer into a changed file must be re-read from disk (already the rule).
- **Never-substitute list.** `world/prose-rules.md`, `characters/notes/
  voice-samples.md`, `world/register-locks.md`, `characters/notes/
  narrator-boundaries.md`, `chapters/*/writing-notes.md`, and any numeric canon
  anchor (prices, frequencies, allocation math) are ALWAYS read verbatim from
  disk. The graph may point at them, never paraphrase them.
- **Canon-blind exclusions.** `coldread-enum.md` and `snapshot.md` MUST NOT
  gain graph access — their measured detector value (Phase 40: 0.5/19 → 13/19)
  depends on not having canon. `judge.md`, `arbiter.md`, `reviewer.md`,
  `integrate-anchors.md` keep their verbatim loads (voice/rule fidelity).

### M1 — `instructions/graph-recall.md`: shared doctrine file

- [x] New instruction file defining: opt-in detection, index/answer modes, the
  freshness gate (exact git + jq commands), the never-substitute list, the
  canon-blind exclusion list, fallback behavior (graph absent/stale/query
  returns nothing → load files as today), and the query grammar with examples
  (`graphify query`, `graphify path`, `graphify explain`). Consumed via
  cross-reference by M2-M5; single source of truth, no restating in consumers.

### M2 — chapter-writer: two-tier context load (highest ROI, ~60k tok/chapter)

- [x] `chapter-writer.md` Step 1: when the graph is present, BEFORE loading the
  `context:` tag files, run (a) `graphify query "usage-tracker items assigned
  to <book> ch<NN>"` and (b) `graphify query "what must <book> ch<NN> set up
  and pay off"` (plants due, motif assignment, echo/reader-journey state).
  Load IN FULL only: the always-load verbatim set (unchanged), the POV
  character sheets, and the `context:` files that carry a tracker row / plant /
  motif hit for this chapter. Remaining `context:` files: read only the §
  sections the graph points to. Graph absent → Step 1 unchanged. The Step 2.6
  symmetry check stays (the `context:` tag remains the authored artifact; the
  graph prunes the load, it does not edit the tag).

### M3 — coherence-check: graph-first for the relational checks

- [x] `coherence-check.md` §1: when the graph is fresh (answer mode), check J
  (Chekhov/plants — currently loads ALL outlines across all books) runs on
  `graphify query "every prestige-inventory plant and its payoff chapter"` +
  `graphify explain` on plants with no payoff edge; check K (context tags &
  Usage Trackers — currently loads all `world/level-*/`) runs on the
  tracker-assignment query and opens only the files the graph names; checks
  B/C/D use graph triage (threads never resolved, knowledge routes,
  character-trait contests) and open sheets only on flagged hits. Checks E/L/M
  (verbatim values) unchanged. Graph absent/stale → §1 load table unchanged.

### M4 — continuity-check: three queries replace the cross-book file sweep

- [x] `continuity-check.md` §1: graph-fresh path = `open threads and ticking
  clocks at end of <book-N>` / `plants placed in <book-N> paying off in
  <book-N+1>` / `character positions at end of <book-N> vs opening of
  <book-N+1>`, then verify each finding against `state.md` (which remains
  PRIMARY input and the write-target). Graph absent → unchanged.

### M5 — motif: bounded traversal replaces the unbounded prior-chapter re-read

- [x] `motif.md` Step 0 item 4: graph-fresh path = `graphify query "<motif>
  established meaning, instances by chapter, intended evolution"` +
  `graphify path <motif> <payoff-chapter>`; re-read from disk only the prior-
  chapter §§ the graph cites for the motifs actually present in the target
  chapter. Graph absent → unchanged.

### M6 — SKILL.md + README: graph dependency + per-command model table

- [x] SKILL.md: document graphify as an OPTIONAL per-project accelerator
  (pointer to `graph-recall.md`); add a "Recommended model per command" table —
  Opus: `chapter/write`, `revise`, `integrate-anchors`, `judge`, `arbiter`,
  `review`, `sniff`, `coldread-filter`, `setup`; Sonnet: `coherence`,
  `continuity`, `fix`, `proofread`, `factcheck`, `motif`, `sensitivity`,
  `readability`, `adjacency`, `coldread-enum`, `snapshot`, `compact`, `sweep`.
  Rationale one-liner per tier (creative/judgment vs detection/mechanical);
  note that scripted enforcement lives in the project pipeline (ground-truth
  Phase 80) and interactive users pick via `/model`.
- [x] README.md: replace the single "Opus recommended" line with a pointer to
  the SKILL.md table.

### M7 — adjacency: graph-first for designed-echo and irony checks (user-requested)

- [x] `adjacency.md` "Inputs": when the graph is fresh AND carries per-chapter
  granularity (probe: a query for the reader-journey state of the target
  chapter returns a per-chapter node — granularity added by ground-truth
  Phase 80 M5), class (a) shape-repetition runs on `graphify query "is the
  rhyme between ch<NN> and ch<MM> a designed echo"` (echo-choreography +
  motif-tracking chapter map) and class (c) irony legibility on `graphify
  query "dramatic irony live across ch<NN> and ch<MM>"` (reader-journey
  per-chapter rows) — replacing the `reader-journey.md` + `echo-choreography.md`
  + `motif-tracking.md` loads (~15k tok). Class (b) idiolect collision keeps
  `voice-samples.md` + `narrator-boundaries.md` verbatim (never-substitute
  list). Probe fails or graph absent/stale → Inputs unchanged.

**Operational:**
- Frontmatter/reference lint: `pytest tests/` + `bash tests/test_install.sh` green; new file carries standard frontmatter; `sweep.md`-style dead-ref check passes for `graph-recall.md` cross-refs. — done 2026-07-25 (14 pytest + 9 install checks green; all `instructions/graph-recall.md` refs resolve. NOTE: "standard frontmatter" wording predated the Phase 18 codification — instruction files carry NO frontmatter by convention; deviation resolved convention-side, see Phase 18)
- Deploy with `./install.sh --force` after approval of the applied edits. — done 2026-07-25 (--check clean; covers Phase 17 + 18)

## Out of scope for Phase 17

- Draft-variant model diversity in `run-parallel-write.sh` (experiment, project-side, deferred).
- Codex-lane model routing (codex CLI has its own config).

## Phase 18 ✅ — Frontmatter convention: codify + enforce (2026-07-25)

From the Phase 17 deviation: the Phase 17 operational bullet assumed "new file
carries standard frontmatter", but the skill's actual convention (established
Phase 15 M2) is that ONLY the root `SKILL.md` carries YAML frontmatter
(agentskills.io: `name` + `description`, consumed by the loader);
`instructions/*.md` carry none (H1 title + lead paragraph). Nothing states
this rule anywhere and nothing enforces it, so the wrong assumption can drift
back in — the next contributor (human or agent) writing an instruction file
has no source to check and no test to fail.

### M1 — codify the convention

- [x] `README.md`: short "File conventions" note under the layout/development
  section: root `SKILL.md` is the ONLY frontmatter carrier (`name` +
  `description`, agentskills.io standard, per Phase 15 M2);
  `instructions/*.md` files start with an H1 title + lead paragraph, no YAML
  frontmatter; cross-references between instruction files use the
  `instructions/<file>.md` path form.
- [x] `DEVPLAN.md` Phase 17 operational bullet: append a pointer noting the
  "standard frontmatter" wording predated this codification and the deviation
  was resolved convention-side (Phase 18), so the record is self-explaining.

### M2 — enforce it mechanically

- [x] `tests/test_frontmatter.py` (pytest): (a) `SKILL.md` begins with `---`
  and its YAML block parses with non-empty `name` and `description`; (b) NO
  file under `instructions/` (recursive, `archive/` included) begins with
  `---`; (c) every `instructions/*.md` non-archive file begins with an H1
  (`# `) line. Sweep run confirms all current files already comply — the test
  encodes the status quo, it does not require edits.

**Operational:**
- `pytest tests/` + `bash tests/test_install.sh` green with the new test file. — done 2026-07-25 (17 pytest + 9 install checks)
- Deploy folded into the pending Phase 17 `./install.sh --force` run (single redeploy for both phases). — done 2026-07-25

## Phase 19 ✅ — adjacency query budget + planned-vs-rendered fidelity check (2026-07-25)

Two user requests. (1) The M5 re-extraction showed per-chapter node detail
sits deep in `graphify query`'s default 2000-token output — adjacency's graph
queries need a larger budget. (2) Every chapter should have BOTH a planned
node (outline: what it must do) and a rendered node (prose: what it did), and
the skill should CHECK the two against each other. The skill already has the
write-time half (chapter-writer Step 7 silent-cut self-check + the append-only
`outline-deviation.md` contract); this phase adds the independent post-hoc
verifier — per the canon-hierarchy doctrine that no single skill validates its
own output. Companion project work (per-chapter planned nodes for B1/B2):
ground-truth Phase 81.

### M1 — adjacency: pass --budget 4000

- [x] `adjacency.md` graph block: both class (a) and class (c) queries (and
  the granularity probe) gain `--budget 4000` so per-chapter node detail
  survives the traversal output cap. One-line rationale referencing the M5
  finding.

### M2 — `instructions/fidelity.md`: the planned-vs-rendered check

- [x] New detection command `/book fidelity <book> <chNN>`. Inputs: the
  chapter's outline § (verbatim), the chapter prose (verbatim),
  `chapters/<book>/outline-deviation.md` (the legitimate-deviations ledger),
  and — graph-fresh only, per `graph-recall.md` — the planned node
  (`chapters_book_N_outline_chNN`) vs rendered node (`chapters_book_N_chNN`)
  pair as triage before the verbatim reads. Finding classes:
  (a) **planned-not-rendered** — outline beat/plant/cliffhanger/motif
  assignment absent from prose AND absent from outline-deviation.md
  (chapter-writer's silent-cut class, verified independently);
  (b) **rendered-not-planned** — substantive prose beat with no outline basis
  and no deviation entry (flag for retroactive outline-deviation.md entry or
  prose trim — never auto-decide which);
  (c) **deviation-ledger drift** — outline-deviation.md entries that no longer
  match the prose they describe.
  Entries recorded in outline-deviation.md are ACKNOWLEDGED — never re-flagged.
  Routing per canon-hierarchy two-channel: prose-side findings → SMELL.md
  entries (consumed by `/book revise`); outline/ledger-side findings →
  DEVPLAN milestones (consumed by `/book fix`). Severity discipline and
  flagging thresholds per reviewer.md conventions; graph absent/stale → the
  check runs identically on file reads alone.

### M3 — registration

- [x] `SKILL.md`: command table row (+1 to the command count wherever stated),
  "Recommended model per command" table → Sonnet tier (detection), graphify
  section consumer list gains fidelity.
- [x] `README.md`: pipeline/command-count mentions updated if any state a
  number.
- [x] `graph-recall.md`: consumers list gains `fidelity.md`.

**Operational:**
- `pytest tests/` (frontmatter test auto-covers the new instruction file) +
  `bash tests/test_install.sh` green (17 + 9, 2026-07-25); `./install.sh --force` redeploy — done 2026-07-25 (single deploy for 19+20+21, --check clean)

## Phase 20 ✅ — Write-side graph freshness: mutating commands refresh the graph (2026-07-25)

User request: when a skill command CHANGES files, the graph should be updated.
Phase 17 added the read side (consumers gate on freshness and fall back);
Phase 80 M3 added the cycle-boundary backstop (merge-phase terminal refresh).
Missing: the write side — the mutating commands themselves leaving the graph
fresh for the next consumer, so intra-cycle queries stop degrading to file
loads. With per-command refresh in place the boundary refresh becomes a cheap
no-op (no changed files), not a redundancy.

### M1 — graph-recall.md §Keeping the graph fresh (doctrine)

- [x] New section defining the write-side rule: any command whose edits touch
  graph-covered sources (`world/`, `characters/`, `plot/`, `chapters/`) ends
  with a refresh step. Gate: `graphify-out/graph.json` exists (same opt-in as
  the read side). Mechanics: run the incremental update flow (`/graphify .
  --update` — re-extracts only changed files; the session itself is the
  extractor, cost is proportional to the edit, typically 1-10 files). Bound:
  if the changed-file count exceeds 25, SKIP the inline refresh and leave it
  to the cycle-boundary backstop, logging one line — a bulk rewrite must not
  trigger a mid-command mega-extraction. Ordering: refresh runs AFTER the
  command's own commit, so graph artifacts never enter the command's commit.
  Soft-fail: a failed refresh never fails the command — consumers are
  protected by the read-side freshness gate.

### M2 — refresh step in the six mutating commands

- [x] Append the refresh step (one short block cross-referencing
  `graph-recall.md` §Keeping the graph fresh, never restating) to:
  `fix.md` (canon mutations), `revise.md` (prose), `chapter-writer.md`
  (new prose + state/outline updates — after Step 8's commit),
  `compact.md` (canon rewrites — the likeliest >25-file skip case),
  `integrate-anchors.md` (prose), `arbiter.md` (prose on APPLY — refresh
  only when it actually applied edits).
- [x] Explicitly NOT added to: `coldread-enum.md`/`snapshot.md` (canon-blind
  wall stays absolute — snapshot's output file going briefly stale in the
  graph is accepted), detection commands (read-only), `setup.md`/`init.md`
  (graph does not exist yet at project creation).

### M3 — SKILL.md note

- [x] One line in the graphify section: mutating commands refresh the graph
  after their commit (pointer to graph-recall.md §Keeping the graph fresh).

**Operational:**
- Sequencing: executes AFTER the Phase 19 agent lands (both touch
  graph-recall.md / SKILL.md); single `./install.sh --force` deploy covers
  19 + 20 + 21. — done 2026-07-25 (--check clean)
- `pytest tests/` + `bash tests/test_install.sh` green. — done 2026-07-25 (17 + 9)

## Phase 21 ✅ — Cost/quality optimization: last graph consumers + model-string refresh (2026-07-25)

From the user-requested deep cost/quality review (2026-07-25). Verified pricing
(claude-api reference, cached 2026-06-24): Opus 5 $5/$25 per MTok, Sonnet 5
$3/$15 ($2/$10 intro through 2026-08-31), Haiku 4.5 $1/$5 — so the Phase 80
Opus/Sonnet routing saves ~40-60% per routed step (correcting the earlier
"1/5th" claim in conversation). The two remaining un-graphed heavy loaders are
sniff (~92k tok/chapter: whole level directory) and reviewer (~85k tok/session:
rubric + up to 10 full drafts). Same invariants as Phase 17 (opt-in, index/answer
modes, never-substitute list, fallback).

### M1 — sniff: claim-driven canon lookup

- [x] `sniff.md`: when the graph is fresh (per `graph-recall.md`), replace the
  "load `world/level-N/*.md` wholesale" step with claim-driven lookup — per
  suspicious assertion, `graphify query "<asserted fact> canon status"
  --budget 4000` → read only the pointed-to file §§ (index mode). Category 7
  (character behavior) gets graph triage on the character's established
  constraints, opening the sheet only on a hit. NEVER substituted: §5/§5.a
  plausibility checks keep their verbatim anchor-value reads (prices,
  frequencies, allocation math), and `writing-notes.md` stays a full read
  (never-substitute list). Graph absent/stale → step unchanged.

### M2 — reviewer: graph triage for plants/object-permanence/echo checks

- [x] `reviewer.md`: checks K and M (plants landing, object permanence,
  echo-not-repetition — today driving multi-chapter re-reads) gain a
  graph-fresh triage path: plant/payoff + object-location queries name the
  prior-chapter §§ to re-read; only those are opened instead of whole prior
  drafts. Rules 0-28 application, `prose-rules.md`, `voice-samples.md`,
  `writing-notes.md`, and the TARGET chapter full read are untouched (verbatim
  set). Graph absent/stale → unchanged.

### M3 — judge.md model-string refresh (July 2026 landscape)

- [x] `judge.md:117` example `model` values and the `:145` lane self-id table:
  `claude-opus-4-8` → `claude-opus-5` (the claude-default lane now runs
  `--model opus` per ground-truth Phase 80; alias resolves to Opus 5);
  `gemini-3.1-pro` → `gemini-3.6-flash`; deepseek row unchanged
  (`deepseek-v4-pro` is the current DeepSeek 4). Detection logic (env-var
  sniffing) unchanged — only the canonical strings emitted.

### M4 — stale model mentions sweep

- [x] Grep SKILL.md + README.md + instructions/ for hardcoded model IDs;
  update any stale ones to aliases or current IDs (keep aliases wherever the
  text means "the current tier model").

**Operational:**
- `pytest tests/` + `bash tests/test_install.sh` green (17 + 9, 2026-07-25); single
  `./install.sh --force` redeploy. — done 2026-07-25 (--check clean)

## Phase 22 ✅ — The skill enforces beat↔context symmetry and not tracker↔context symmetry (2026-07-25)

Source: the `ground-truth` corpus, 2026-07-25. Eleven findings passes over Book 1's nine drafted chapters, plus a mechanical whole-corpus scan, produced numbers that are not a property of that project — every outline, tracker row and draft in it was written by this skill, so each figure below is a measurement of this skill's behavior:

- **445 tracker rows across three books name a chapter whose `context:` list does not contain the owning file.** The row cannot reach a reader: the writer never opens the file. 66 of them are on chapters already drafted; 379 sit on chapters not yet written, where the repair is currently free.
- **Two canon files are in no `context:` list in the entire trilogy.** Everything in them is dead by construction.
- **102 rows were rendered and never ticked**, and **21 rows are ticked `written` with the element absent from the prose.** Both directions of the ledger are wrong, and nothing in the skill checks either.
- Of the 269 rows still `planned` on drafted chapters, only 101 were real losses. The outline elements the prose genuinely failed to render across nine chapters number **8**. The drafting held; the bookkeeping did not.

### M1 — Step 2.6 checks one symmetry and the corpus needs two

`chapter-writer.md` §2.6 enforces **beat ↔ context**: every file in `**context:**` must be justified by a beat, every beat that needs a file must list it. It even auto-adds the missing files (2.6.a). Nothing enforces **tracker ↔ context**, and that is the direction that decides whether canon reaches a reader. `init.md:176` states only the outbound half — *"Only add a file to `context:` if it has tracker items mapped to that chapter"* — so a file holding rows for Ch.07 while absent from Ch.07's context list violates no rule the skill knows.

- [x] Add 2.6.c, tracker↔context symmetry: for the chapter being written, every canon file holding a Usage Tracker row for this Book+Ch must appear in the chapter's `**context:**` list, in the always-loaded set, or in the texture-palette proxy. Missing → AUTO-ADD, exactly as 2.6.a already does for beats, with the same announcement line.
- [x] Add the reciprocal statement to `init.md`: writing a tracker row for chapter X and adding the owning file to X's `**context:**` are one action. A row whose file X does not load is not a plan.
- [x] Guard the auto-add against the level register (M4). A tracker row must never cause a Level-0 file to be added to a Dome or Ark chapter's context list.

### M2 — `init.md` does not scaffold §Context Tags, so books diverge

In `ground-truth`, Book 1's `outline.md` declares an always-loaded set **and** a `**Texture-palette proxy:**` paragraph; Books 2 and 3 declare the always-loaded set and no palette. Same skill, same project, three books, two shapes. A structure that appears in one book and not the others was emitted once and not the other twice.

- [x] `init.md` — specify the §Context Tags block as a required outline header section with named parts: the always-loaded reference list, the texture-palette proxy paragraph (or an explicit statement that this book has none), and the context-list discipline paragraph. Scaffold it for **every** book the command creates, not the first.
- [x] State that each book derives its own two lists from its own `writing-notes.md`, and that copying another book's list is wrong — the sets differ per book by design.
- [x] Anything reading these lists must parse them from the outline. A consumer that hardcodes a copy becomes a fourth hand-maintained list, which is the defect.

### M3 — Step 5.5 can only tick rows in files Step 1 happened to load

`chapter-writer.md` Step 5.5 opens **"every file loaded in Step 1 that has a `## Usage Tracker` section."** Step 1 loads the context list plus the always-loaded set. A file holding a row for this very chapter but absent from its context list is therefore never opened: its row cannot be rendered and cannot be ticked. Both measured failures come out of that one sentence — the 445 unreachable rows, and the part of the 102 unticked rows whose owning file the chapter never loaded (3 of ch08's 7, to take the case that was counted).

- [x] Change Step 5.5's scope from *files loaded in Step 1* to *every file holding a row for this Book+Ch*. With M1 in place the two sets are identical for a compliant chapter; keeping them distinct means a stale outline silently drops rows again.
- [x] Where the two sets differ, Step 5.5 reports the difference rather than skipping it quietly — that difference is precisely a tracker↔context violation M1 should have caught earlier.

### M4 — the level register is enforced by convention only

Dome chapters do not load `world/level-0-reality/*` because the POV cannot see it. That exclusion is load-bearing and written nowhere the skill can apply it, so 69 rows in `ground-truth` sit in files the target chapter's level bars — including four Level-0 files carrying `### Dome` subsections authored for Dome chapters by name, and five Level-0 files holding rows for Ark chapters.

- [x] Document the register rule in the skill: a chapter's `**Level:**` determines which level-scoped canon directories are legal for it; character and plot files are level-neutral.
- [x] Make M1's auto-add register-aware: file legal for the level → add it; file barred → report a conflict naming both hypotheses (the row targets the wrong chapter, or the content is filed in the wrong file) and resolve neither. The register outranks the tracker.
- [x] Note the corollary for canon authors: a `### Dome` subsection inside a Level-0 file is unreachable from every chapter that wants it. Level-scoped content belongs in the level's own directory.

### M5 — nothing ever re-reads a `written` mark

Step 5.5 sets `planned` → `written` and no step revisits it. Measured on the one chapter small enough to audit exhaustively (12 marks, all checked): **17% false, 33% counting partials.** Across Book 1, 21 marks name an element that is not in the prose. A recurring signature: the row names a **sensory modality** rather than a fact — canon promised coolant as *smell and memory*, the prose delivered burn and stain, and the mark was set on the object without checking the channel.

- [x] `fidelity.md` already re-derives planned-vs-rendered independently. Add the `written`-mark direction to it explicitly as a fourth finding class: a row marked `written` whose element is absent from the prose.
- [x] Add the modality trap to Step 5.5's rules: the mark is valid only if the prose renders the element **in the channel the row names**. Rendering the right object through the wrong sense is not a rendered element.

### Verification

- Re-run the `ground-truth` measurements after M1–M5 deploy. The counts that must move: 445 unreachable → 0 for compliant chapters, and no new `written` mark surviving a fidelity pass. — pending
- `pytest tests/` + `bash tests/test_install.sh` green, single `./install.sh --force` redeploy. — done 2026-07-25 (17 passed / 9 passed; `--check` clean)

**Where the corresponding data repair lives:** `ground-truth` `DEVPLAN.md` Phases 87 and 88. Those fix one corpus. This phase is why it will not have to be done again — and the ordering matters: deploy M2 before repairing Books 2 and 3's outlines by hand, so the repaired files match what the skill will emit from then on.

## Phase 23 ✅ — The three registers: tracker, context list, plant table (2026-07-26)

Source: the `ground-truth` corpus, 2026-07-26, and the author's reading of a fix applied there — *"non credo che il lettore che in ch2 legge una frase che può voler dire niente poi se la ricorda 19 capitoli dopo."* He was right, and diagnosing why exposed a second defect underneath the one Phase 22 closed.

**Three registers record one fact and none of them is checked against the others.**

| Register | Lives in | Says |
|---|---|---|
| Usage Tracker | the canon file that owns the element | this element belongs in B1 Ch.07 |
| `context:` list | the chapter's outline header | to write B1 Ch.07, load these files |
| §Inline Plant Tracking | one table in the book's outline | this thing recurs at #1 Ch.05, #2 Ch.12, #3 Ch.14, #4 Ch.19 |

Phase 22 bound the first two. This phase binds the third, and repairs the reason the first binding was ineffective in the file that already had it.

### M1 — Check K states a loading mechanism that does not exist, and exempts most of the corpus on the strength of it — **premise false; direction reversed by Phase 24**

`coherence-check.md` §K already carries the tracker↔context rule: *"verify the target chapter's `context:` field includes this file. If not, flag as WARNING."* The next sentence cancels it for the directory where most canon lives:

> *"Files inside `world/level-*-<name>/` directories are loaded selectively by the chapter writer based on tracker items — they do NOT need context tags."*

`chapter-writer.md` Step 1 has no such path. It loads the `context:` list plus the always-loaded set, and nothing reads tracker rows to decide what to open. The sentence describes a behavior the writer does not have and uses it to exempt `world/level-0-reality/` (20+ files), `level-1-ark/` and `level-2-dome/` from the only check that would have caught the 536 unreachable rows measured in `ground-truth`.

- [x] Delete the carve-out. Level-directory files reach a chapter the same way every other file does.
- [x] State the rule positively in its place, with the reachability set Phase 22 M1 defines: a tracker row is valid only if its file is in the chapter's `context:` list, the always-loaded set, or the texture-palette proxy.
- [x] Audit the rest of `coherence-check.md` for other claims about what the chapter-writer does. A check that reasons from a wrong model of the writer fails silently and reports success.

**Audit result (2026-07-26) — the premise above is wrong on one point.** `chapter-writer.md` Step 1 §Load based on level DID carry a tracker-driven selective load: *"load files from the corresponding `world/level-*-<name>/` directory SELECTIVELY … only those whose `## Usage Tracker` contains items mapped to THIS chapter"*. That sentence is where check K's carve-out came from, and it contradicts Phase 22's 2.6.c, which reaches the same files by auto-adding them to `context:`. Two load models for one directory, and the check trusted the one no longer enforced. Step 1 now routes level-scoped canon through the reachability set and forbids the directory scan, so deleting the carve-out leaves a single model. Claims audited:

| Claim in `coherence-check.md` | Verdict |
|---|---|
| K: level-dir files are loaded selectively from tracker rows, so they need no context tag | ~~**Wrong** — rewritten; Step 1 realigned (above)~~ **Correct.** Re-verdicted by Phase 24 |
| K: a `context:` entry with no tracker row for that chapter is unnecessary loading; exclude "always-loaded files (tones.md, prose-rules.md, etc.)" | **Wrong twice** — beat-referenced files are legitimate per 2.6.a, and the exclusion set must be parsed from the book's §Context Tags, not hardcoded (Phase 22 M2). Rewritten, deduplicated into R |
| R: a `context:` file with zero beat references is an orphan | **Incomplete** — a file 2.6.c auto-added for a tracker row has no beat; coherence would order the removal of what the next draft re-adds. Tracker row now counts as justification; palette excluded |
| S: a beat's canonical file must be in `context:` or the always-loaded set | **Incomplete** — 2.6.a excludes the texture-palette proxy too (2.6.e). Third route added |
| N: "use chapter Step 3.5 check #15 as the spec" | **Correct** — Step 3.5 #15 is the interior-labeling grep |
| S: "Step 2.6.a runs the same scan as a HARD `MUST`" | **Correct** |
| O: `outline-deviation.md` is created by chapter-writer Step 2.5.d on cut/split/merge | **Correct** |
| K: every chapter header carries a `context:` field the writer loads | **Correct** — Step 1 §Load from `context:` tag (MANDATORY) |
| K: a `context:` file holding discrete details should have a `## Usage Tracker` | **Correct** — `init.md` §Key template principles |
| Routing: "`/book fix` does not touch chapter prose by design" | **Correct** — `fix.md` §3 and its Rules |
| §4.5: operational items close from `/book fix` §2.5, `/book continuity` §4.5, `/book compact` §4.5 | **Two correct, one wrong** — compact's section is §5.5. Corrected |
| L, M, G, T: writer-side twins (2.5.a, 2.5.b) referenced only as doctrine, no behavioral claim | **No claim to check** |

**Correction (Phase 24, 2026-07-26) — M1's premise was false and its resolution went the wrong way.** The milestone was written on my claim that §K's carve-out described a mechanism the writer did not have. It had it: `chapter-writer.md:36` at `f1b6cd9` loaded the chapter's own `world/level-*-<name>/` directory selectively, by tracker row, and §K described that accurately. The contradiction M1 detected was real but sat elsewhere — Phase 22's 2.6.c required a `context:` entry for every tracker row without exempting the directory the selective path already covered. M1 resolved it by deleting the selective load; measured in `ground-truth`, that made 226 of 314 rows reported unreachable false positives. The checkboxes above stay ticked because they were implemented as written; Phase 24 restores the selective load as the fourth route of the reachability set and keeps the two parts of M1 that were right — the level-register conflict verdict, and the removal of §K's silence about `world/` root files, which had left `world/the-word.md` unreachable from all seven chapters that render it.

### M2 — Chekhov cannot see a plant that lives only in tracker rows

§J loads `plot/prestige-inventory.md`, `plot/motif-tracking.md` and every outline. It does not read §Inline Plant Tracking, and it does not read the Usage Trackers. In `ground-truth` the Dome's filtered spectrum existed as three tracker rows at B1 Ch.02 and no plant row, while the outline's Hex-code row already carried `#4 Ch.21 — spectral glass color`: the payoff was tracked and the thing it pays off was not. §J is the check that owns plant→payoff and it had no way to look.

- [x] Add both sources to §J's load row and reconcile them: an element with tracker rows across three or more chapters is a plant and needs a §Inline Plant Tracking row; a plant-table instance at Ch.N with no tracker row for that chapter is an instance nothing owns.
- [x] Flag the specific shape found: a payoff instance whose enabling element has no row of its own. That is the retroactive-plant class §J already defines, reached from the register side rather than the prose side.

### M3 — One instance is not a plant

A plant mentioned once, nineteen chapters before its payoff, is not planted. The corpus states the working convention itself: every plant in `ground-truth`'s table carries three or four instances (Hand-to-ribs 05/12/14/19; Dek 06/08/16/19; Niva 11/14/16/19/24), with consecutive gaps of two to eight chapters.

- [x] §J flags a payoff with fewer than two prior instances.
- [x] §J flags a gap larger than the project's own measured maximum. **Derive the bound from the book's existing table, do not decree a number** — the convention differs per project and a hardcoded figure is wrong in the second project that uses it.
- [x] Say what the fix is when the check fires: add instances, not a better single sentence. An abstract sentence cannot be made memorable enough to cross twenty chapters alone.

### M4 — The writer collects plant instances due this chapter, alongside tracker rows

Phase 22 added §2.6.c, the tracker-side scan. Plant instances assigned to the chapter being written are the same kind of obligation from the third register and nothing collects them.

- [x] Extend §2.6.c to collect §Inline Plant Tracking instances for this Book+Ch as well, and apply the same reachability and level-register rules to each.
- [x] `fidelity.md` gains a matching class: a plant instance the table assigns to this chapter and the prose did not render.

### M5 — `init.md` scaffolds the plant table and its numbering

Phase 22 M2 found Book 1 declaring a §Context Tags part that Books 2 and 3 lacked. The plant table has the same exposure and no scaffolding at all.

- [x] Specify §Inline Plant Tracking as a required outline section: one row per plant, numbered instances per chapter, the payoff instance marked as such.
- [x] State the convention M3 measures against — a plant carries multiple instances — where a writer will read it, not only where a checker will.

### M6 — Say once what each register owns

M1's defect is a file reasoning from a wrong model of another file. The three registers are described in three places and nowhere together.

- [x] Write the table at the head of this phase into the skill's shared doctrine, and have `chapter-writer.md`, `coherence-check.md`, `fidelity.md` and `init.md` point at it instead of restating it.

Doctrine file: `instructions/registers.md` (the table plus the reachability set, the level-register pointer, and the plant-table shape). `SKILL.md` names it alongside `graph-recall.md` and `milestone-format.md`; the four instruction files link to it.

### Verification

- Re-run the `ground-truth` measurements after deploy. `--check` there reports 0 orphans / 314 unreachable-MISSING / 50 CONFLICT; M1 is the change that should move MISSING. — pending
- `pytest tests/` + `bash tests/test_install.sh` green, single `./install.sh --force` redeploy. — done 2026-07-26 (17 passed / 9 passed; `--check` clean)

## Phase 24 ✅ — Restore the selective level-directory load, and make it the checked model (2026-07-26)

Source: Phase 23's own M1 audit, plus a measurement in `ground-truth` the same day. **Phase 23 M1 was implemented on a false premise supplied by the author of the phase — me.**

M1 said `coherence-check.md` §K's carve-out described a loading mechanism that does not exist. It exists. `chapter-writer.md:36` at commit `f1b6cd9` reads: *"load files from the corresponding `world/level-*-<name>/` directory **SELECTIVELY**: list the files in the directory, then load only those whose `## Usage Tracker` contains items mapped to THIS chapter."* §K's carve-out was an accurate description of it, and the two agreed.

What actually broke the agreement was **Phase 22's 2.6.c**, which required every tracker row's file to be in the `context:` list without exempting the level directories the selective path already covered. Phase 23 then resolved the contradiction by deleting the selective path. That direction is wrong, and the measurement says how wrong: of 314 rows `ground-truth`'s guard reported unreachable, **226 sit in the chapter's own level directory** and were reachable all along. **88** were genuinely unreachable.

**The selective load is the better mechanism and it is the one this skill argues for everywhere else.** It is derived rather than hand-maintained, it cannot drift, and it is the same principle Phase 22 M1 invoked against hardcoding the always-loaded set. Its real defect is different: a chapter's actual load is invisible in the outline, while §Context Tags calls the `context:` list authoritative.

### M1 — One model, stated once, covering both paths

- [x] Restore the selective level-directory load in `chapter-writer.md` Step 1, and state the complete model in `instructions/registers.md`: a chapter reaches a canon file if it is in the always-loaded set, in the texture-palette proxy, in the chapter's `context:` list, **or** in the chapter's own level directory carrying a tracker row for this Book+Ch. The last clause is the one Phase 23 removed.
- [x] Correct §Context Tags' claim that the `context:` list is the authoritative record of what a chapter loads. It is authoritative for conditional files; the level directory is reached by rule. A document that overstates its own scope is what produced this phase.

### M2 — 2.6.c must exempt what the selective path already covers

- [x] Amend §2.6.c: a tracker row whose file sits in the chapter's own level directory is reachable by rule and is **not** an auto-add candidate. Auto-add applies to `world/` root files, `plot/`, `characters/`, and any level directory that is not this chapter's own — the last of which is a register conflict, not a missing entry.
- [x] Say why in one line, so the exemption is not deleted again by someone reading 2.6.c alone.

### M3 — Restore §K to the model, without restoring its blind spot

§K's carve-out was right about level directories and silent about everything else, which is why `world/the-word.md` — a `world/` root file owning an entire character arc — was unreachable from all seven chapters that render it and no check said so.

- [x] Restate §K over the full reachability set: level-directory rows are covered by rule; every other tracker row needs a `context:` entry, and its absence is a WARNING.
- [x] Keep the level-register conflict verdict Phase 23 added. A row in a *different* level's directory is not reachable by any path.

### M4 — Consumers of the model

- [x] `fidelity.md` and `coherence-check.md` §J were written against Phase 23's single-path model in the same session; re-read both against the restored model and correct any reachability claim.
- [x] Where a project ships a tool that computes reachability, the model above is what it must implement. Say so in `registers.md` — `ground-truth`'s `chapter-load.py --unreachable` over-reported by 226 rows for exactly this reason.

**M4 audit (2026-07-26).** Every reachability claim in the two files, plus the ones the same grep found elsewhere:

| Claim | Verdict |
|---|---|
| `fidelity.md` Input 4: tracker files collected as 2.6.c collects them, NOT restricted to `context:` | **Correct** — but 2.6.c now also carries an exemption; added one clause so an implementer does not inherit it and skip level-directory rows |
| `fidelity.md` §19, class (d), class (e), §Coordinate with Chekhov | **Correct** — they read the tracker and plant registers directly and assert nothing about how a file is loaded |
| `fidelity.md` class (d): "a row still `planned` is not a class (d) finding" | **Correct** — unaffected by the load model |
| §J: a plant instance at Ch.N with no tracker row for Ch.N is owned by nothing | **Correct, and stronger** — with the selective load restored, a missing row also means Step 1 never opens the file; clause added |
| §J: three-or-more-chapter recurrence needs a plant row; instance-count and gap bounds | **Correct** — no reachability content |
| §K: three-route reachability set, level directories not exempt | **Wrong** — restated over the four routes; the WARNING now names `world/` root, `plot/`, `characters/` explicitly, so the blind spot §K had before Phase 23 is not restored with the carve-out |
| §K load row: "level directories included, no exemption" | **Wrong wording** — the rows are read and resolved by rule, not exempted; reworded |
| §K: flag a `context:` entry only when it has neither a tracker row nor a beat | **Correct** — a redundant entry is not flagged either way |
| §R: a tracker row justifies a `context:` entry because 2.6.c re-adds it | **Incomplete** — 2.6.c no longer re-adds own-level-directory files; that entry is redundant, not orphaned. Clause added |
| §S: three-route exclusion for beat-referenced files | **Incomplete** — fourth route added; a beat-referenced file already opened by Step 1 is not a context gap |
| `chapter-writer.md` 2.6.b: orphan = zero beat references | **Incomplete** — did not count tracker rows at all (a pre-existing mismatch with §R), and would flag an own-level-directory entry. Both fixed |
| `chapter-writer.md` Step 5.5: scope is every file holding a row for this Book+Ch, not the Step 1 load | **Correct** — the two sets now coincide for more chapters, and the difference report is unchanged |
| `init.md` §Context Tags: the `context:` list is authoritative | **Wrong** — authoritative for conditional files only; corrected, and the reciprocal rule at §Key template principles gained the fourth exemption |
| `SKILL.md` §The three registers: check K "came to exempt every `world/level-*/` file" | **Wrong** — that exemption matched the writer; the drift was 2.6.c ignoring it. Sentence corrected |

### Verification

- Re-run `ground-truth`'s guard after both repos land. — **done 2026-07-26.** `chapter-load.py` gained route 4 (project-side Phase 88 M9): unreachable-MISSING **314 → 88**, CONFLICT **50 → 50**. The unchanged conflict count is the check on the change rather than a coincidence — the register does not depend on the load model, so a correct fix must leave it untouched. 91 project tests green, including one pinning that no own-level-directory row is reported MISSING.
- `pytest tests/` + `bash tests/test_install.sh` green, single `./install.sh --force`. — done 2026-07-26 (17 passed / 9 passed; `--check` clean)

**Standing note for future phases.** Phase 23 M1 asked its implementer to *verify the premise before acting on it*, and the implementer did, found it false, and reported it. The instruction to verify is what saved this; the phase would otherwise have shipped a deletion of a working mechanism on the author's confidence alone.

## Phase 25 ✅ — A prose edit stamps the reader-state snapshots it invalidated (2026-07-26)

Source: a measurement in `ground-truth`, 2026-07-26. One `/book revise` pass edited all nine drafted chapters of book-1 and left all nine reader-state snapshots in `chapters/coldread-state/` untouched, dated seven weeks earlier than the prose they describe. Nothing on disk recorded the mismatch; it was found by hand weeks after the pass.

`instructions/revise.md` never mentioned the snapshot. Snapshots are derived from chapter prose and are the only model `/book coldread-enum` has of what the reader remembers. After an edit the snapshot keeps its filename, its structure and its four blocks, and describes text that is no longer in the chapter — a current snapshot and a stale one are indistinguishable on disk.

### M1 — `/book revise` stamps every snapshot its edits invalidated

Reader-state is cumulative: the snapshot for chapter N carries what the reader retained from chapters 1..N, so an edit at chapter N invalidates chapter N's snapshot and every later snapshot in the same book.

- [x] New `### 5.7` in `revise.md`, between 5.5 and §6. It runs once at session end over the full set of chapters edited, not per fix — the range to stamp is fixed by the lowest chapter the session touched, which is not known until the last fix lands.
- [x] The stamp is inserted immediately after the snapshot's H1 and replaces any stamp already present, so consecutive revise passes leave one line rather than a stack.
- [x] §6 announce block reports the number of snapshots stamped and which chapters.

**Mark stale, do not regenerate.** Regenerating costs one `/book snapshot` run per chapter from the edited chapter to the last drafted one, each reading a full chapter and each depending on the snapshot below it, so the runs are serial and ascending. How much of the book to rebuild, and when, is a decision the operator makes with the rest of the pass in view; spending it as a side effect of a prose fix takes that decision away. The stamp names the command to run instead.

### M2 — `/book coldread-enum` refuses a stale snapshot

- [x] Input 1 of `coldread-enum.md` gains the refusal: if the snapshot's opening lines carry `**STALE — do not consume.**`, the skill stops before reading the chapter, writes no `COLDREAD.md`, and reports the stale snapshot plus the exact `/book snapshot` command that regenerates it.

**Refuse, do not warn.** `coldread-enum` runs unattended inside `run-merge-phase.sh` step 8.5. A warning line there is read by nobody and the run continues: `COLDREAD.md` comes out in the normal format, `coldread-filter` triages it into SMELL.md, and `revise` applies findings written against prose that no longer exists. Those findings are indistinguishable from valid ones at every downstream step, and they arrive with the authority of a completed gate. Stopping leaves the pipeline blocked at the step that needs an operator, which is the state the pipeline is in.

### Verification

- `pytest tests/` + `bash tests/test_install.sh` green, single `./install.sh --force` redeploy. — done 2026-07-26 (17 passed / 9 passed)

## Phase 26 ✅ — Three guards move from a consuming project into the skill (2026-07-27)

Source: the `ground-truth` project's Phases 95-97. Each item below was built there, used there, and was
sitting in one repo where no other project could reach it. `registers.md` already carried the warning that
a partial reimplementation costs a consuming project a 314-versus-226 miscount; that warning existed
because the cost had been paid once and nothing had been done about the cause.

### M1 — `/book revise` re-points the line citations its edits moved ✅

A prose edit shifts every line below it. A citation written as `ch07.md:125` still resolves after the
shift — to a line that now says something else — so nothing fails and the reader of the citation is
silently misdirected. Measured in `ground-truth`: 140 live prose citations, of which 11% quoted the text
they cited and none pointed past end of file, so neither a quote check nor a bounds check would have found
the stale ones.

- [x] `scripts/remap_citations.py` — maps old line numbers to new ones with `difflib.SequenceMatcher`
  against `HEAD`, and returns `None` rather than the nearest survivor for a line with no counterpart. A
  rewritten line has no correct new number, and guessing one produces a citation that is wrong and looks
  right.
- [x] Historical records are excluded by path: `archive/`, `SMELL`, `PROOFREAD`, `REVIEW`, `COLDREAD`,
  `DEVPLAN.md`, `outline-deviation.md`. A citation in a record of what was found last month must keep
  pointing at the text as it was.
- [x] `revise.md` §5.8 runs it at session end and **before** the commit, because the script compares the
  working tree against `HEAD`.
- [x] Tests in `tests/test_build_scripts.py`: it shifts what moved, refuses what was rewritten, leaves
  historical files alone. The path-resolution bug — resolving a repo-relative path against the process cwd,
  which works only when the shell is already in the repo — was caught by those tests, not by review.
- Validated against the real failure: replaying `ground-truth` commit `dc40631` gives `ch07.md:125 → 133`,
  which is the correction that had been made there by hand. — done 2026-07-27

### M2 — `milestone-format.md` bans command-scoped deferrals ✅

- [x] `Deferred to /book fix book-2`, `Left for that pass`, `Route there` and their variants are banned.
  This form passed every check in the list because the banned constructs all named a phase or a user and
  this one names a **command**, so it reads as a routing decision: a reviewer sees a destination and moves
  on. It is not a destination — the run is one nobody has scheduled.
- [x] The rule restated as the action rather than the prohibition: an item whose content belongs to an
  undrafted chapter is not postponed, **its destination is the file the future step loads**. Write the
  constraint into that file in the form that file uses, then close the item in the same pass.
- [x] The measured instance recorded: nine items across two phases in `ground-truth`, all nine applicable
  the day they were parked.

### M3 — `scripts/chapter_load.py` ships with the skill ✅

Twelve of its 1,117 lines were project data; everything else parses this skill's conventions — Usage
Tracker tables, `**context:**` and `**Level:**` fields, the always-loaded set, the texture-palette proxy.

- [x] Ship the script. The consuming project keeps a small shim so its pipeline scripts, hooks and tests
  can invoke a stable path; the script resolves the project from `BOOK_PROJECT_ROOT`, then the git top
  level, never from its own install path.
- [x] Hold no project list. Books come from `chapters/book-*/`, drafted chapters from the prose on disk,
  level names and directories from `world/level-<n>-<name>/`, Level-0 chapters from the outlines'
  `**Level:**` fields. Every one of those was a hand-maintained constant first, and each stopped covering
  its corpus the day it changed while the guard kept reporting OK.
- [x] `tests/test_chapter_load.py` — 16 tests against a synthetic project in a tmpdir, including the empty
  corpus a freshly scaffolded project has. They pin the model, not a corpus: the four reachability routes,
  both directions of the register, the co-primary/parenthetical distinction, both derivations, the
  malformed-row check, the exit-2 contract, and the read-only guarantee.
- [x] `registers.md` §Tools that compute reachability rewritten: it told the next project to build this.

**A project's own suite does not move here.** `ground-truth`'s 114 bats tests assert against its files and
its history, including five inverted the day its backlog reached zero. That is a regression record and it
belongs where the regressions happened.

### M4 — `coherence-check.md` gains check U, Single Ownership ✅

The other twenty checks compare two statements of a fact and ask whether they agree. None asks why there
are two. A project that scaffolds one canonical file per concept states that rule and verifies nothing.

- [x] Check U reports a slug claimed twice, a slug claimed by nobody, and a non-owner that explains a
  concept instead of pointing at its owner. It reads the slug list from the consuming project's own
  Concept → Canonical file table — adding a row there must change what the check reports with no edit
  here, or the check grows the second source of truth it exists to prevent.
- [x] WARNING, not BLOCKING, on the same grounds as a register CONFLICT: resolving a duplicate means
  deciding which file keeps the content, which is a judgment and not a repair the pipeline can apply.
- [x] Runs on every scope. Ownership is a property of the whole canon set, so a scoped run would compare a
  file against only some of its rivals and report clean while the duplicate sat in the skipped directory.

Three defects of exactly this shape were found by hand, late, in `ground-truth` on 2026-07-27: a simulation
tell with two different mechanisms across three files, a forbidden causal link restated in three including
the file that owns the topic, and one rule carried by three different line citations, one pointing at a
blank line. Each was internally consistent in the file it sat in, which is why twenty checks missed them.

### Verification

- `pytest tests/` 36 passed; `bash tests/test_install.sh` green; single `./install.sh --force`; `--check`
  reports no drift. — done 2026-07-27
- Consuming project re-verified through the shim: 114 bats tests green, `./chapter-load.py --check` exit 0,
  and `--free` / `--check` / `--unreachable` / `--illegal-load` byte-identical to the pre-move output.
  — done 2026-07-27

## Phase 27 ✅ — Token-cost pass over the instruction set (2026-07-27)

Author's request: say the same thing more tersely across the whole skill, preserving information and
instruction. Measured first, because two obvious hypotheses are false.

**Measurements, 2026-07-27.**

| Quantity | Value |
|---|---|
| Instruction set + SKILL.md | **67,979 words**, 31 instruction files |
| Literal duplication across files (blocks >90 chars in 2+ files) | **226 words**, 0.3% |
| Paragraphs carrying a date, phase number, measurement or explicit reason | **5,626 words**, 8% |
| Largest single file | `chapter-writer.md` 8,214w — and it runs on every chapter |
| Next four | `coherence-check.md` 7,121 · `reviewer.md` 5,429 · `sniff.md` 5,182 · `init.md` 3,181 |
| Five catalogue sections | 21 checks 4,760 · 13 dimensions 3,189 · 11 objections 2,713 · self-edit 1,176 · 9 verify passes 1,174 = **13,012w, 19% of the set** |

**De-duplication is not the lever.** 226 words across the whole set, in four harmless pairs — the
cross-reference discipline in `registers.md` and `milestone-format.md` already works. Anyone starting this
pass expecting to find restated doctrine will not find it.

**Per-invocation cost is the number that matters, not the total.** No command loads 67,979 words. `/book
chapter` loads SKILL.md + `chapter-writer.md` + what it points at; `/book coherence` loads SKILL.md +
`coherence-check.md` + `registers.md` + `milestone-format.md`. Optimising a file no hot command loads buys
nothing, so the order below is by invocation frequency × size, not by size.

The per-command chain figures obtained by grepping cross-references (chapter-writer 26,527; sniff 34,922)
are **upper bounds, not measurements**: they count every file a document mentions, and a mention is not a
load. They are good enough to order the work and must not be quoted as savings.

**The catalogues are the mass and they compress least.** 19% of the set is five lists where each entry is a
distinct check. Nothing there can be deleted without deleting a check, and the older entries are already
terse — check D is four lines. The slack is concentrated in entries written recently, which carry their
rationale and their measured instance inline.

### The rule for what may be cut — this is the part that decides whether the pass helps or harms

This project's own doctrine is that a rule stated without its reason gets re-litigated by the next agent
that reads it, and it has been re-litigated twice on record (Phase 23 M1 deleted a working mechanism; Phase
24 restored it). So "asciutto" cannot mean dropping the reason.

**Cuts allowed:**
- Preamble that announces what a section is about before saying it.
- A second example where the first already establishes the shape.
- Restatement inside one file — a rule stated in the intro and again in the step that applies it.
- Hedges and softeners that change no instruction.
- Narrative connective tissue between numbered steps.

**Never cut:**
- Any imperative, MUST, threshold, exit code, file path, command name, or numeric bound.
- The one clause that gives a rule its reason. Compressed, never deleted: `WARNING, not BLOCKING —
  resolving a duplicate is a judgment` is enough; the paragraph of measurement behind it is not.
- Any statement of what a check does *not* cover. Those exist because something was assumed covered.

**The measured instance moves rather than dies.** A dated measurement (`nine items across two phases`,
`314 versus 226`, `eleven rows overwritten`) is what stops a *human* reopening a settled question, and
humans can follow a pointer; the one-clause reason is what stops the *agent* weakening the rule mid-run,
and that must stay inline. Instances move to `rationale/<file>.md`, which no command loads, with the
instruction keeping the one clause and a pointer. **This is the largest single saving available and the
one with the most risk — it is M1 so it is judged on one file before the rest follow.**

**`install.sh` copies `instructions/` and `scripts/` and nothing else** (lines 151-152), so a new top-level
`rationale/` ships nowhere and every pointer added to an installed instruction file resolves to a path that
does not exist on the consuming machine. Adding it to the installer is a prerequisite of M1, not a
follow-up, and `test_install.sh` must cover it — otherwise the first thing this pass produces is a set of
broken references, which is worse than the verbosity it removes.

**The risk this move carries is the one the doctrine names.** If the measurement is not in context, the
next agent to work on that file sees a rule with a one-clause reason and no evidence, which is a weaker
position than today's, not a neutral one. The move only pays if the surviving clause is strong enough to
stand alone — so the compression is doing real work, not relocation, and M1 is where that is judged.

### Verification — prose changes, claims do not

Compression is unverifiable by reading, because the reader who compressed it knows what it used to say. So
each file is checked mechanically before and after:

- **Claims inventory — the exact half.** Backticked tokens (paths, commands, flags), numbers with a unit
  or a threshold, severity keywords (`MUST`, `NEVER`, `HARD`, `BLOCKING`, `WARNING`, `NOTE`), headings, and
  cross-file references. These are **sets and compare exactly**: a dropped instruction is a set difference.
- **Claims inventory — the heuristic half, and it is stated as heuristic.** Imperative sentences cannot be
  set-compared, because rewording is the point of the pass. They are **counted per section** and a decrease
  is a finding to justify, not a failure. A check that pretended to be exact here would be the kind of
  false confidence this project has already paid for twice.
- **A blind read, because the person who compressed a text cannot audit it.** Before compressing, derive a
  fixed question list from the original — one question per instruction the file gives. After, a fresh agent
  reads **only the compressed file** and answers them. A wrong or absent answer is information loss, and it
  is the only evidence here that comes from behaviour rather than from string comparison.
- `./install.sh --check` clean. **The pytest and bats suites are not evidence for this pass** — they cover
  `scripts/`, and `test_frontmatter.py` asserts only that instruction files carry no frontmatter and open
  with an H1. Running them guards the new script in M1 and nothing else. Saying "suites green" about a
  prose change would be the sort of claim that reads as verification and is not.
- Word count recorded per file, before and after.

### M1 — Prove the rationale-move on one file, then decide ✅

`registers.md` (1,206w, **31% rationale** — the highest ratio in the set, and it is loaded by five commands).

- [x] Write `scripts/claims_inventory.py`: extract the claim set from a markdown file and diff two versions.
  **Done when** it reports zero difference on an unmodified file and a non-zero difference when a single
  `MUST` sentence is deleted from a copy.
- [x] Add `rationale/` to `install.sh` and to `test_install.sh`. **Done when** a fresh install carries the
  directory and the installer's drift check covers it.
- [x] Compress `registers.md`, moving dated measurements to `rationale/registers.md` and keeping the
  one-clause reason inline. **Done when** the exact claim inventory is unchanged, every measurement removed
  is present in the rationale file, and the blind read answers every question the original could.
  **No word target is set, here or anywhere in this phase.** A declared number invites hitting it by cutting
  something, which is the failure this project spent Phase 97 M7 measuring from the other side.
- [x] **Record the achieved ratio before touching a second file.** **Done when** this milestone states the
  before/after word count and whether the rest of the pass is worth running at that rate — if the saving on
  the highest-rationale file in the set is under 20%, the rationale-move does not pay for the risk and M2-M4
  drop the rationale-move and become prose-tightening only.

**M1 verdict, 2026-07-27: the rationale-move gave 8% and the threshold was 20, so it is dropped.** Both
halves of the item were built — the script and the installer support — and both were then reverted with the
directory, because unused scaffolding is a file that answers to a glob and to no caller. The reason it pays
so little: the 31% marker counted whole paragraphs containing a date or a figure, and inside those the
measurement is a clause while the rest is the rule, which stays either way.

Prose-tightening with the measurements left inline gives **3%** on `registers.md` and **10%** on the largest
procedure section in the set. M2-M4 ran as prose-tightening only.

`scripts/claims_inventory.py` stays and is the gate for the rest of the phase. **Its own negative test found
a hole in it**: deleting a sentence that referenced `chapter-writer.md` changed nothing, because a set sees
the loss of a token's *last* mention and not the loss of one of several. Occurrence counts were added and
report as `THINNED`; eight tests, one of which pins that limitation rather than hiding it.

`registers.md` also gained `--ownership`, missing from both its mode list and its exit-1 list since the mode
shipped.

### M2 — `chapter-writer.md`, the hot path ✅

8,214w on every chapter. Two sections are 30% of it: Step 3.5 Self-Edit (1,176w) and Step 5 Verify (1,174w).

- [x] Compress, exact claim inventory unchanged, blind read clean. **Done when** the before/after counts are
  recorded here and `/book chapter` drafts a full chapter end to end with no step failing for a missing
  instruction. That last is the real gate: this file is a procedure, and a procedure is verified by running
  it, not by diffing it.

**8,214 → 7,931, 3.4%.** Step 3.5 (seventeen checks) gave 10% by hand; the rest of the file gave 2%. Steps
2.5 and 2.6, the densest 2,150 words, yielded ~40 words of connective tissue — nearly every sentence is a
rule, the reason a rule exists, or a "report both hypotheses, resolve neither" instruction. Passes 1-7 are
six-to-ten-word lines with nothing to take.

### M3 — `coherence-check.md`, `reviewer.md`, `sniff.md` ✅

- [x] One file at a time, claims inventory unchanged per file. **Done when** all three are recorded with
  before/after counts and both suites are green after each.

`coherence-check.md` 7,121 → 6,751 (**5%**, and 7% inside the 21-check catalogue — three checks restated
their own load-table rows verbatim). `reviewer.md` 5,429 → 5,346 (**1.5%**). `sniff.md` 5,182 → 5,074
(**2%**). The two catalogues resisted: reviewer's Rules 25-28 are built from clauses that are individually
protected — guard lists with numbered exemptions, a boundary naming the sibling checks, a severity, a
classification — and sniff's categories each carry a named example that *is* the definition.

### M4 — The remaining 26 files ✅

- [x] Sweep, claims inventory unchanged per file. **Done when** every file has a recorded before/after and
  the set total is recorded against the 67,979 baseline.

### Result — 2.9%, and eight defects

**67,979 → 66,001 words, −1,978, 2.9% across 31 files.** One `LOST` verdict in the whole set, and it is the
deliberate heading correction below. 51 pytest, 9 install tests, `./install.sh --check` clean, and the
consuming project's guard still exits 0 through the shipped copy.

| Band | Files |
|---|---|
| 4-6% | `sensitivity.md`, `coherence-check.md`, `milestone-format.md`, `motif.md`, `sweep.md`, `readability.md` |
| 2-3% | the majority |
| 0-2% | `factcheck.md`, `coldread-enum.md`, `chapter-writer.md`, `reviewer.md`, `sniff.md`, `judge.md`, `compact.md` |
| 0% | `epub.md`, `pdf.md` — returned unchanged, with the reason |

**The 10% measured on Step 3.5 was an outlier, not a rate.** That section is seventeen checklist items each
carrying its rationale inline; almost nothing else in the set has that shape. The three largest files —
`chapter-writer.md`, `reviewer.md`, `sniff.md`, 18,700 words together — came in between 1.5% and 3.4%,
because they are catalogues where each line is a rule with its own threshold.

**Where the 2.9% actually came from, in every file that beat 4%: one rule stated twice.** `milestone-format`
stated its deferral rule negatively and then positively. `motif` had a §Calibration restating §Flagging
discipline. `coherence-check` had three checks whose `**Load:**` line duplicated their own row in the §1
load table, and a §4 routing rule restating §Routing doctrine from the top of the file. `readability` had
two Calibration blocks saying the same thing. That is the compressible shape, and it is scarce — literal
duplication across the whole set was 226 words before this pass, and the within-file kind is not much
larger.

**The return was not the tokens.** Eight defects surfaced, none of them compression, all verified before
fixing:

| File | Defect |
|---|---|
| `chapter-writer.md` | heading read `Verify (9 passes)` over ten passes — Pass 10 is conditional and skippable without noticing |
| `reviewer.md` | "Before the **8** dimensions" over thirteen; a duplicated question in §4; corrupted apostrophes |
| `sniff.md` | "one of the **ten** categories" and "satisfies all **nine**" over eleven |
| `sniff.md` | §Notes said `SMELL.md` is overwritten and history lives in git, while Step 5 archives it to `archive/` |
| `coherence-check.md` | §5 template classifies into `[A-J]` while the checks run to U; two empty bullets; two unclosed parentheses, one swallowing the rest of its bullet |
| `continuity-check.md` | check F had unbalanced parentheses and a stranded `(e.g.,` — a half-finished edit |
| `coldread-filter.md` | rule 1 routed PENDING to "arbiter/user review" against the contract that forbids a human, which would stall an unattended run |
| `init.md` | pointed at "§Context Tags below" with the section above it, in both the file and the generated outline |

Stale counts are the pattern: four of the eight are a number in a heading or lead-in that stopped matching
the list under it. Nothing checks those, and nothing here proposes a checker — they were found by reading
every line with intent, which is what a compression pass is.

**One rule held throughout and is worth keeping for any future pass: do not chase the number.** Every agent
was told the 10% was an observation and not a target. `epub.md` and `pdf.md` came back unchanged with their
reasoning, `factcheck.md` at 1.9%, and no agent invented a cut to hit a figure.

### What this phase does not do

- It does not touch `scripts/`. Python is not loaded into context.
- It does not merge files. The 31-file split is what makes per-invocation loading selective; merging would
  raise per-invocation cost while lowering the total, which is the wrong number.
- It does not delete a check, a dimension, or an objection category. If one of those is not worth its
  tokens, that is a separate decision with its own evidence, not a side effect of a compression pass.

---

## Phase 28 ✅ — The rendered book declares the language it is written in (2026-07-29)

Source: a translation of `ground-truth` book-1 into Italian, rendered through these two scripts on
2026-07-28. Both builders take `language` from `meta.yaml`; neither puts it where a renderer or a reader
can act on it.

**Measured on that build.** The EPUB carries `dc:language = it-IT` in the OPF, and every one of its nine
chapter documents opens `<html lang="en" xml:lang="en">` — `make_chapter_item` hardcodes it. A reader that
selects a text-to-speech voice or a hyphenation dictionary per document gets English for an Italian book.
The PDF is worse and language-independent: `wrap()` emits `<html>` with no `lang` at all, and
`book.css` has set `text-align: justify` with `hyphens: auto` since it was written. WeasyPrint hyphenates
only when the document declares a language, so **no PDF this script has ever produced has been hyphenated**
— 117 justified A5 pages at 11pt with the word spacing opened to fill every line. `build_pdf.py` loads
`language` at line 64 and never reads it again.

### M1 — every XHTML document in the EPUB carries the book's language ✅

- [x] `make_chapter_item(filename, title, html_body, language)` — `lang` comes from the caller instead of
  the literal `"en"`. Both call sites (`render_single`, `render_book`) already hold `language`.
- [x] `make_nav(items, title, language)` — the nav document is a document too; a reader narrating the table
  of contents hits it first.
- [x] Default stays `"en"` via `meta.get("language", "en")`, so a book with no `meta.yaml` renders exactly
  as it does today.

### M2 — the PDF declares its language, which is what turns hyphenation on ✅

- [x] `wrap(body, language)` emits `<html lang='…'>`. This is the whole fix: the CSS asking for
  hyphenation has been correct all along and had nothing to key on.
- [x] `render_single` loads `meta.yaml` — today it does not, so a single-chapter PDF has no metadata path
  at all and would keep rendering unhyphenated after M2 lands elsewhere.
- [x] **Consequence, stated because it is visible and not a regression:** the English book-1 PDF re-flows
  the first time it is rebuilt, because hyphenation changes line breaking. The rendered artifacts are
  compiled output under `chapters/*/pub/`, regenerable, and not committed. Measured after the fact, and
  smaller than predicted here: 2,834 → 2,807 lines and **112 pages either way** — see the Result section.

### M3 — a test that fails on the hardcoded value, and the two instruction files ✅

- [x] `tests/test_build_scripts.py`: render a two-chapter book with `language: it-IT` through `uv run
  --script` (guarded by the existing `skipif(shutil.which("uv") is None)`), unzip the EPUB, assert every
  chapter document and the nav declare `it-IT`. The same test with no `meta.yaml` asserts `en` — the
  default is the behaviour most consuming projects rely on.
- [x] The PDF half gets a render-and-exit-0 test plus a source assertion that the `<html` literal carries
  `lang`. A hyphenation assertion would have to read the PDF text layer for soft hyphens, which is a
  fragile check of WeasyPrint's dictionary rather than of this script.
- [x] `instructions/epub.md` — the `language` key stops being described as EPUB metadata only; it sets the
  per-document language that drives TTS voice and hyphenation.
- [x] `instructions/pdf.md` — documents `meta.yaml` for the first time. The file currently mentions none of
  the four keys `build_pdf.py` reads, and `language` is the one with a visible effect on the page.
- Deploy with `./install.sh --force`, run the full pytest set, then re-render the Italian book-1 EPUB/PDF
  so the delivered files carry the fix. — done 2026-07-29

### Result — 117 pages to 116, and 124 lines that stopped being needed

Measured on the same nine-chapter Italian book, rendered by the pre-fix and post-fix script into the same
directory: **117 pages → 116, and 3,130 → 3,006 lines of text.** Same words, 4% fewer lines, because
hyphenation now breaks them. The EPUB check is exact: all nine chapter documents and the nav declare
`it-IT` where every one of them declared `en` the day before.

Rendering the same book with `language: en-US` also lands on 116 pages — English patterns applied to
Italian words still break something. Page count therefore proves that *a* language was declared, not that
the right one was; the assertion that the declared language is the book's is the EPUB test's job.

**The same fix moves English an eighth as far, and the phase predicted otherwise.** The English book-1 PDF
was re-rendered on 2026-07-29 and measured against the pre-fix script from `8f71727`: **2,834 → 2,807
lines, and 112 pages both times.** M2 above said the page count would move; it does not for this book.
English words are shorter and offer fewer break points, so hyphenation recovers 1% of the lines where
Italian recovers 4% — a book in a compounding language is where this defect was costing something, and it
took translating one to surface a bug that had been shipping in every render since the stylesheet was
written. The English EPUB is the unambiguous half: its ten documents declared `{en-US, en}` before the fix
— the nav inheriting the book language, the nine chapters overriding it — and declare `en-US` after.

**The nav was already right, by an accident worth recording.** ebooklib serializes
`self.lang or self.book.language`, so a document that declares nothing inherits the book's language.
`make_nav` passed nothing and was correct; `make_chapter_item` passed `"en"` and was wrong — the defect was
not a missing value but an explicit one overriding a working fallback. `EpubNav.__init__` takes no `lang`
argument, so M1 sets the attribute after construction rather than through the constructor.

**Two tests were verified against the pre-fix scripts before the fix was kept**, by stashing them: the EPUB
assertion fails with `lang="en"` where `it-IT` was expected, and the source assertion fails on the bare
`<html>` literal. The `default-when-no-meta` case passes both before and after, which is the point — it
pins the default that every existing project relies on.

### What this phase does not do

- It does not touch `book.css` or `epub.css`. The stylesheets asked for hyphenation correctly and had
  nothing to key on; changing them would have hidden the defect instead of closing it.
- It does not assert hyphenation from the PDF text layer. That reads WeasyPrint's dictionary rather than
  this script, and pdftotext does not reliably preserve the inserted hyphen — the page-count and
  line-count deltas above are the evidence, recorded here rather than asserted in a test.

## Phase 29 ✅ — The graph was in the flow and never fresh enough to be used (2026-08-02)

Eight steps query the graph instead of loading canon in bulk. On the consuming project's ch10 cycle, not one
of them used it: the freshness gate reported stale from the second step onward, every consumer fell back to
whole-file loading, and nothing said so. The accelerator was wired, documented, and inert.

### M1 ✅ — The gate counted files the graph does not contain

The gate globbed `world/ characters/ plot/ chapters/` wholesale. Those directories also hold the working
ledgers — `SMELL.md` alone is rewritten by sniff, coherence, factcheck, motif, sensitivity, fidelity,
readability, adjacency, coldread-filter and revise — so a step that touched no narrative content still
invalidated the graph for the next step. Measured after the ch10 merge: **of the eight files that marked it
stale, six were ledgers and two were narrative.**

- [x] The gate now filters `SMELL*`, `REVIEW*`, `PROOFREAD*`, `COLDREAD*`, `DEVPLAN.md`, `archive/`,
  `coldread-state/` and `pub/` before deciding. Verified against three consecutive real pipeline steps
  (coldread-enum, sensitivity, fidelity) that each changed exactly one ledger: raw 1 → filtered 0, so the
  graph stays usable across all three where it previously died at the first.
- [x] The filter list and the consuming project's `.graphifyignore` are declared as **one decision in two
  places**, with the failure mode of letting them drift written next to it: a file the graph indexes but the
  gate ignores goes stale unnoticed, and a file the gate counts but the graph never held makes the gate lie
  in the safe direction forever.

### M2 ✅ — Four steps that were paying full price

- [x] `factcheck`, `sensitivity`, `coldread-filter` and `readability` added as consumers, all **index mode** —
  the query returns pointers, the disk supplies the verdict. Each does a corpus-wide lookup per item, which
  is the shape the graph serves: factcheck resolving an anchor per claim (18 on ch10), sensitivity asking
  whether a depicted group has depth elsewhere, coldread-filter asking whether a missing setup exists
  somewhere the reader has already passed, readability locating the register rules for one level.
- [x] `readability` carries an extra constraint because Category 0 gates a hard blocklist: the forbidden
  patterns are read **verbatim** from `register-locks.md`, never paraphrased from a query. A blocklist
  recalled approximately is a blocklist that misses.

### M3 ✅ — The exclusions were already there, and the first draft duplicated them

- [x] **Caught in review of my own change.** The first version of this work added a new "Steps that must NOT
  use the graph" section — while `## Canon-blind exclusions` had covered `coldread-enum`, `snapshot`,
  `judge`, `arbiter` and `integrate-anchors` since Phase 40. Two sections stating one rule is exactly the
  restatement this skill's own information-architecture doctrine forbids. The new section was deleted and
  the existing one strengthened instead.
- [x] Added to the existing section: a second measurement for the canon-blind rule — ch10, where
  **coldread-enum returned 40 findings on a chapter that factcheck, motif, sensitivity, fidelity, adjacency
  and readability each passed clean** — and the pairing that follows from it, *enumerate blind, triage
  informed*, which is why this phase gave the graph to the filter and not the enum.
- [x] Added an independent second reason for `judge`: **three of its four lanes run outside Claude Code** and
  have no `graphify query`, so wiring the Anthropic lane alone would give one judge of four a different
  evidence base from the other three. Recorded so the question is not re-opened on the token-saving argument.

### M4 ✅ — Tests

- [x] `tests/test_graph_recall_wiring.py`, 11 tests, verified in both directions: **6 fail against the
  pre-change instructions**, all 11 pass after. They pin the canon-blind exclusion, the gate's exclusion set,
  the gate/`.graphifyignore` coupling, the declared-consumer set, that every declared consumer actually
  cross-references the doctrine, and that no undeclared file quietly queries the graph.
- [x] **One test first passed for the wrong reason and was rewritten.** `consumer_list()` parsed "everything
  before the exclusions heading"; with the heading absent it fell back to scanning the whole file and
  reported `coldread-enum` as a declared consumer. It now parses the `Consumers (...)` parenthetical
  specifically. Third instance today of an assertion matching prose instead of code — the note is in the
  test so the next author sees it.
- Full skill suite **67/67**.

### M5 ✅ — `/book fidelity` queried two node ids that have never existed

Found while deciding what to test after the graph rebuild. The step's triage compared a "node pair" —
`chapters_book_N_outline_chNN` planned against `chapters_book_N_chNN` rendered. **Neither id has ever been
produced by any graph this project built.** So the pair diff never ran once, and the step's own *"either node
missing → skip triage silently"* clause meant nothing ever said so. The check itself was never wrong: it
falls back to verbatim reads, which are the authority. What was lost is the saving, silently, for as long as
the section has existed.

Measured on the freshly rebuilt graph (5,965 nodes, 10,093 edges, 182/182 documents):

| Side | Coverage | Conclusion |
|---|---|---|
| Rendered prose | 19-47 nodes for **every** chapter file, ch01-ch10, none missing | query it |
| Planned outline | book-3 has per-chapter nodes (`Ch. 29 — The Lighthouse Swim`, `loc=Ch. 29`); **book-1 has zero**, only 207 concept nodes | read it |

- [x] **The id cannot be repaired by renaming.** Outline granularity differs *between books from the same
  extractor on the same run* — so a query written against book-3's shape returns nothing for book-1, in a
  way the caller cannot distinguish from "nothing was planned". Rewritten around the asymmetry instead: the
  planned side is one ~20-line `## Ch. NN` block read from disk, and the expensive half — tracker rows
  marked `written` scattered across character and world files, plant-table instances — goes to the graph,
  which covers it reliably. Cheaper than what was specified, and identical in every book.
- [x] Two tests, both failing against the pre-change instructions: no instruction may name a synthetic
  per-chapter node id, and fidelity must say it reads the planned side from disk **and why**, so the next
  author does not optimise it back into a query.
- **The general lesson, recorded because it outlives this step:** a silent fallback hides a query that
  matches nothing exactly as well as it hides a stale graph. Every `→ skip silently` clause in this skill is
  now a place where a broken query can live undetected. The contract test is the cheap standing guard;
  writing a query without checking its shape against a real graph is what it guards against.
- Suite **69/69**.
