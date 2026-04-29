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

## Phase 2 — EPUB Export (2026-04-29) — DONE (smoke test deferred pending `ebooklib` install)

`/book epub <book> [chNN]` — mirror of `/book pdf` for the digital Kindle pipeline. Engine: `ebooklib` (pure-Python, MIT, no native deps). Output → `chapters/<book>/epub/`. Optional `chapters/<book>/meta.yaml` overrides title/author/identifier/language; defaults: title from `outline.md`, author "Unknown Author", deterministic UUID, lang "en".

- [x] M1: `scripts/build_epub.py` + `scripts/epub.css` (reflow-friendly em-based, no page-sizes, drop-cap, `* * *` scene break).
- [x] M2: `instructions/epub.md`.
- [x] M3: SKILL.md commands-table row + routing.
- [ ] M4: smoke test — blocked by missing `ebooklib` in active Python (PEP 668 system Python). User to choose install path: `pip install --user --break-system-packages ebooklib` OR a dedicated venv with shebang updates. Not blocking the rest of the work.

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

- [ ] Define usage: `/book sniff <book> [chNN]`. Reads the latest draft of the chapter (or the most recent if no chapter specified), produces `chapters/<book>/SMELL.md`.
- [ ] Specify the reader persona for the executing agent: *informed, skeptical, well-read, not romantic about the work*. Looks for things that would make a reader pause and call BS.
- [ ] Nine objection categories the agent must scan for, line by line:
  1. **Anachronism** — does the assertion track with 21 years of climate / tech / society evolution from 2024 baseline?
  2. **Worldbuilding-canon contradiction** — direct conflict with `world/` or `characters/` files?
  3. **Technobabble without referent** — specific number/term ("0.3", "tier two", "corridor 042") implies a system; does that system exist in canon?
  4. **Unearned capability or knowledge** — character/object/agent does/knows something not previously established.
  5. **Domain plausibility** — would an economist, engineer, doctor, person with disability, or local (Marseillais, etc.) call BS?
  6. **Physical implausibility** — geometry, physics, biology of described action.
  7. **Character behavior** — consistent with established sheet?
  8. **Plot armor / convenience** — events resolve too easily; info appears when needed.
  9. **Continuity within chapter** — timeline, geography, props consistent across the chapter itself (e.g., object in pocket → in hand without transition).
- [ ] Output format: `SMELL.md` with one entry per objection. Each entry:
  - **File:line** (or scene reference)
  - **Quote** (the offending passage)
  - **Objection category** (one of the 9 above)
  - **What the reader would think**
  - **Classification:** INLINE / ANCHOR-NEEDED / ACCEPT
  - **Suggested action:**
    - INLINE → proposed prose fix.
    - ANCHOR-NEEDED → which worldbuilding file needs a section, what the section must define, suggested milestone language for the project DEVPLAN.
    - ACCEPT → why deliberate (only if the writer agent has documented evidence in the outline or world files).
- [ ] Write a short calibration note: the agent must err toward *more* objections, not fewer. False positives are cheap (the user dismisses); false negatives let bad prose ship.
- [ ] After producing `SMELL.md`, the skill prints a one-line summary: `wrote SMELL.md — N objections (X INLINE, Y ANCHOR-NEEDED, Z ACCEPT)`.

### M2: Wire the dispatcher

**File:** `SKILL.md` (REVISIONE).

- [ ] Commands-table row: `| sniff <book> [ch] | Adversarial skeptical-reader pass → SMELL.md | /book sniff book-1 ch01 |`.
- [ ] Routing list: `sniff → instructions/sniff.md`.
- [ ] `## The Pipeline` section: insert sniff between write and review:
  ```
  WRITING LOOP (repeat per batch)
    6. /book write book-1        → write 5 chapters
    7. /book sniff book-1        → adversarial skeptical-reader → SMELL.md
    8. /book review book-1       → editorial review → REVIEW.md
    9. /book proofread book-1    → line-level review → PROOFREAD.md
   10. /book revise book-1       → apply SMELL + REVIEW + PROOFREAD fixes to prose
  ```

### M3: Extend `instructions/revise.md` to consume SMELL.md INLINE items

**File:** `instructions/revise.md` (REVISIONE).

- [ ] Add SMELL.md to the load list.
- [ ] Apply INLINE entries (proposed prose fixes from the sniff pass) BEFORE editorial/proof fixes — gaffes cleared first, craft after.
- [ ] ANCHOR-NEEDED entries are NOT applied; instead, surface them in the revise summary as "deferred to worldbuilding (see SMELL.md ANCHOR-NEEDED block)" and stop there. They become input to the project's DEVPLAN.
- [ ] ACCEPT entries are noted in the summary but not acted on.

### M4: Harden `instructions/chapter-writer.md` — pre-drafting `MUST` rules

**File:** `instructions/chapter-writer.md` (REVISIONE — add a new Pre-Drafting Anchor Checks section).

- [ ] **4a — Level-aware economic-anchor pre-check.** Before drafting any scene with a *price, wage, cost, balance, salary, rent, fee, fine, tip, ration, memory-credit transaction, kilo+price pairing, monetary unit (€/euros/CBDC/GPU-HE) near digits, allocation request, compliance-score gating*, the agent MUST read the level-appropriate anchor file (Reality → `economy.md §Consumer Anchors`; Ark → `daily-life.md §Economy`; Dome → `bureaucracy.md §Allocation Mathematics`) and pick a value consistent with it. If no anchor exists, STOP and request a worldbuilding-anchor milestone before drafting.
- [ ] **4b — Broader no-invent rule** (system-implying details). For any *tier system, score, hum frequency in Hz, MHz, latency / bandwidth / corridor / channel number, % offer / discount, compliance threshold, hardware-vintage capability claim*, the agent MUST verify a canonical worldbuilding anchor exists. If absent, STOP. The trigger keyword set is explicit (no fuzzy matching): `tier`, `score`, `Hz`, `MHz`, `% offer`, `compliance check`, `corridor 0\d\d`, `latency`, `bandwidth`, `LED`, `firmware`, `handshake`, `signature`.
- [ ] **4c — Show-don't-tell hard rule with forbidden formulas.** The following constructions are FORBIDDEN as interior labeling and may only appear when they describe an EXTERIOR observation:
  - `the closest thing to <emotion> he/she had had in days/weeks/years`
  - `a kind of <abstract noun>`
  - `almost <verb>` / `almost felt like`
  - `started to <verb>` ... `before/and stopped` (when used as interior gesture-labeling rather than exterior fact)
  - `<character> felt X` followed by an explanation of what X is
  Express interior states through physical action, gesture, or sensory tightening. The agent reviews its own draft for these patterns at self-edit and rewrites or deletes.
- [ ] **4d — Outline-to-chapter coverage contract.** If the writer cuts, splits, or reorders outlined scenes during drafting, it MUST: (i) update `chapters/book-N/outline.md` to reflect the new split (move plant tags, update beat-section structure); (ii) write a one-line entry to `chapters/book-N/outline-deviation.md` (NEW file, append-only): `Ch.NN: <scene> moved/cut/merged because <reason>. Plants shifted: <list>.`; (iii) flag any plants that lost their planned chapter so the next write call surfaces them. No silent cuts.

### M5: Harden `instructions/coherence-check.md` — six new check classes

**File:** `instructions/coherence-check.md` (REVISIONE).

- [ ] **5a — Economic-anchor BLOCKING** (level-aware). For every chapter draft, scan for monetary/transactional/allocation details (regex set: `€\d`, `\beuros?\b`, `\bCBDC\b` near digits, `\bGPU-HE\b` near digits, `\bkilo\b`/`\b/kg\b` in price context, `\bbalance\b` near numeric, `\bration\b` near numeric, `\bcompliance score\b`, `\bmemory credit\b`, `\benzyme cloth\b` near numeric, `W-RAR-03`). Verify each match traces to the level-appropriate anchor file. Unanchored or contradictory → BLOCKING.
- [ ] **5b — System-implying-number BLOCKING.** Same regex strategy on the trigger set from M4b above (`tier <digit>`, `corridor 0\d\d`, `<digit> Hz` outside canonical anchors, `% offer`, etc.). Each match must trace to canon. BLOCKING if not.
- [ ] **5c — Interior-labeling NOTE** (soft). Scan for the M4c forbidden formulas. Each match → NOTE-level flag with the line and a suggested rewrite. NOT BLOCKING — these are advisory.
- [ ] **5d — Outline-to-draft coverage WARNING.** For every scene listed in the relevant outline, verify a corresponding section exists in the draft (heuristic: scene's distinctive props/characters appear in the draft text). Missing scenes → WARNING with cross-ref to `outline-deviation.md`. Missing AND no entry in `outline-deviation.md` → BLOCKING (the writer cut without documenting).
- [ ] **5e — Cross-substrate sensory-echo WARNING.** Maintain a registry of canonical sensory anchors (e.g., 440 Hz hum in Ark per Phase 111 M3). For every chapter draft, when a sensory detail matches a number/object already canonical at a *different* level, flag WARNING: "this echo is intentional (cross-substrate plant) or accident (collision)? confirm in `temporal-echoes.md §Cross-Substrate Sensory Resonances`." Forces the question to be answered, doesn't block.
- [ ] **5f — Redundancy-with-adjacent-text NOTE.** Heuristic: if a paragraph repeats specific information given in the immediately preceding paragraph (especially across a system message → flashback boundary, e.g., the Game says "your mother made couscous" and the next paragraph describes that exact couscous), flag NOTE for review — the writer may want to defer / vary the second beat to avoid the reader feeling told twice.

---

**Phase 3 totals:** 5 milestones, all in this skill repo. Phase 3 produces a check (sniff) and rules (chapter-writer, coherence-check) that surface project-content gaps; the gaps themselves go to each book project's DEVPLAN.

**Out of scope:** the smell-test does NOT auto-fix worldbuilding gaps — it just surfaces them. The user/agent triages.
