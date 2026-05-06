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
