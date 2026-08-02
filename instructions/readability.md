# `/book readability` — register-aware flow / "scorrevolezza" pass

Run a reader who wants to be *carried* over the latest chapter draft. Catch the one defect no other pass owns: the chapter has become a **brick** — dense, effortful, hard to follow at reading speed — *where the density was not deliberate*. The book must read with pleasure; heaviness is a defect **except** where the project's own files declare the heavy register an intended tonal choice.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Plausibility / "would a reader call BS" | `sniff.md` |
| Internal consistency against canon | `coherence-check.md` |
| Craft (voice, scene shaping, pacing as structure) | `reviewer.md` |
| Reader-stumble at a single point (ambiguous pronoun, unsetup fact) | `coldread-enum.md` |
| Surface (grammar, punctuation) | `proof-reader.md` |
| **"Is this stretch a slog to *read*? Could a reader follow it on one pass without effort?"** | **THIS check** |

Readability asks the cumulative, textural question the others miss: **does prolonged reading become work?** A chapter can be plausible, canonical, well-shaped, stumble-free and grammatically clean, and still be a brick. This pass protects *scorrevolezza* — flow.

**The load-bearing constraint: register awareness.** Density is not automatically a defect — the project deliberately uses heavy registers (a disorienting interior, a bureaucratic catalog). Flag only the **accidental** brick — heaviness outside an intended-heavy register — and never flatten an intended one: misfiring destroys the very tonal range the project depends on. When in doubt, the stretch is intended; the burden of proof is on the flag.

**Milestone format:** see `instructions/milestone-format.md`. Findings are prose-side and route to `SMELL.md` (`Source: readability`); they are consumed by `/book revise` exactly like sniff INLINE entries.

## Usage

```
/book readability <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`).
- `chNN` — optional. Scans only that chapter; if omitted, the most recently written chapter for that book.

## Output

**Skip declaration (mandatory — see `instructions/skip-declaration.md`).** Any path this check declines to run — a stale graph, an absent input, a deferred sub-check — is stated in the report below with its reason, on its own line, before the findings. A skip that narrows coverage and is not declared is indistinguishable from a path that is quietly broken; all three defects that rule was written for were found by accident, late.

Appends entries to `chapters/<book>/SMELL.md` with `Source: readability`, plus a mandatory **"Readability / Flow Audit"** section (metrics per scene, always present — transparency). If `SMELL.md` does not exist, create it with the standard header; otherwise append, never overwrite — sniff and coherence may have written to it already.

## Reader persona for the executing agent

You are an intelligent reader reading for pleasure, at speed, on a couch, not studying for an exam. You do not re-read; you do not stop to admire craft. When a sentence makes you back up to parse it, when a paragraph asks you to hold five things in working memory at once, when exposition runs long enough that your attention drifts, you feel friction — and a few stretches of friction and you put the book down. You are NOT charitable: if a passage *can* be read as effortful, it is effortful. You do not supply the connective work a tired reader won't do.

But you respect intent. You have read the project's tone files, so you know which scenes are *meant* to be heavy; there you complain about weight only where the text gave you no reason to carry it.

## Step 0 — Build the register map (load-bearing, do this first)

Before reading the chapter, read the project's tonal/style canon and build a map of which registers are **intended-heavy** vs **default**:

**Graph-assisted register lookup (optional — gating in `instructions/graph-recall.md`, index mode).** Six files feed the register map and only parts of each apply to one chapter's level. When the graph is available and fresh, use it to find which sections to open:

```bash
graphify query "<chapter level> register — tones, prose rules, forbidden patterns"
graphify query "<book> ch<NN> — declared register locks and intentional techniques"
```

**Index mode only, and Category 0 is the reason it matters here.** The forbidden-pattern catalog in item 6 gates a hard blocklist, so it is read **verbatim from `world/register-locks.md`** — never paraphrased from a query result. A blocklist recalled approximately is a blocklist that misses. The graph points at the section; the disk supplies the patterns. Graph absent or stale → load all six as written.

1. `world/tones.md` — tonal registers per narrative level. Identify any register the project *wants* dense, airless, ornate, fragmented, or slow.
2. `world/prose-rules.md` and `world/writing-checklists.md` — writing-quality rules; note any that license density (long sentences for a specific effect, catalog prose, etc.).
3. `characters/notes/voice-samples.md` — the POV character's voice signature. A naturally maximalist or recursive voice is an intended register, not a brick.
4. `chapters/<book>/writing-notes.md` — per-chapter intentional techniques and register locks. **This is the strongest signal**: a stretch the writing-notes names as deliberately heavy is intended-heavy by default.
5. `chapters/<book>/outline.md` — the chapter's beat entry; an outline tag like "deliberately disorienting / airless / claustrophobic prose here" marks an intended-heavy stretch.
6. `world/register-locks.md` §<this chapter's level> — the **explicit forbidden-pattern catalog** for the chapter's narrative level (Dome / Ark / Reality). Extract the verbatim **Forbidden patterns** list (e.g. Reality forbids "X was the X" tautologies, apophatic chains of 4+, compliance-system vocabulary). This list gates **Category 0** below — a hard, level-specific blocklist, not a flow heuristic.

Record, per scene or stretch, the verdict: **intended-heavy** (the project asked for weight here) or **default** (the project expects flow here). The six flow categories only fire in **default** stretches. **Category 0 (register leak) is register-independent** — a forbidden cross-level pattern is a breach wherever it appears in a chapter of the wrong level, intended-heavy or not.

## Category 0 — Register leak (runs first, register-independent)

**Deterministic backbone — run this FIRST and treat its output as authoritative.** Before any LLM reading, run the linter (zero-LLM, fully reproducible — it does not miss literal tics the way an LLM scan can):

```
python3 ~/.claude/skills/book/scripts/register_leak_lint.py <chapter_file> --level <reality|ark|dome>
```

Pass the chapter's level (determined in Step 0). Every `LEAK …` line it prints is an **authoritative SAFE-CUT register-leak finding** — emit a Category-0 SMELL entry for each, verbatim location and pattern. The linter covers the machine-checkable subset of `register-locks.md` (the "X was the X" tautology family + compliance-vocabulary blocklist for Reality/Ark; Dome has no deterministic patterns). *(Rationale: a cold validation, project Phase 44 M3, showed the LLM scan alone missed `the lines were the lines` in a Reality chapter that this linter catches instantly — so the literal half of Category 0 must not rely on LLM judgment.)*

**Then** do the LLM semantic scan below for the patterns the linter cannot catch (Mediterranean warmth leaking into the Dome, measurement-substitution that erases POV agency, apophatic chains of 4+).

The LLM semantic scan runs against the **Forbidden patterns** list extracted in Step 0 item 6 (`register-locks.md` §<this level>) — a literal / near-literal pattern match, not a flow judgment:

- **"X was the X" tautologies** (Reality) — `the cord was where the cord was`, `the kitchen kept its kitchen sounds`, `the plate was where she had set it`, `the kitchen was the same kitchen`, and any `<noun> … was … <same noun>` stasis construction. These are **Dome-narrator** tics; in a Reality chapter they read as the wrong tonal world.
- **Apophatic chains of 4+** consecutive "She did not ___ / He did not ___" sentences in a Reality or Ark chapter (the sustained apophatic accumulation is Dome-only).
- **Compliance-system vocabulary** in Reality (`compliance nudge`, `deniable band`, `within parameters`, `measurement-substitution-for-feeling` that erases POV agency) — those belong to the Dome.
- Symmetrically, the level's own forbidden list from `register-locks.md` (Dome forbids Mediterranean-warmth leaks; Ark forbids apophatic chains + compliance language).

A Category-0 hit is a **breach, not a trade-off**. It does NOT get the three-question / register-floor treatment the flow categories get — the intent is already encoded in `register-locks.md`, so the pattern is removed:

- **Flagging: SAFE-CUT. Routing: INLINE.** (Never SAFE-KEEP, never TRADE-OFF.)
- `Category: 0 — Register leak (<pattern> vs register-locks §<LEVEL>)`
- Suggested action: rephrase to the level's own register (re-rhythm / concrete varied prose for Reality), preserving meaning — do not merely delete the sentence if it carries a beat.

If `register-locks.md` is absent for the project, skip Category 0 and note it in the audit ("Register-leak scan: skipped — no register-locks.md").

## The six friction categories

Evaluated stretch-by-stretch (a scene, a paragraph cluster), not line-by-line — flow is a cumulative property. For each candidate, the stretch must be in a **default** register (Step 0) before it can flag.

1. **Sentence-length slog.** A run of consecutive long sentences with no short sentence to release the reader. Prose breathes when length varies; an unbroken streak of 30+-word sentences reads as effortful however well-formed each is. Metric: longest run of consecutive sentences all above ~25 words, and the scene's mean sentence length vs the chapter's. Flag only when no variation relieves the run and the register is default.

2. **Clause-stacking / subordination depth.** A single sentence nesting subordinate clauses, parentheticals, em-dash asides and qualifiers so deep the reader loses the main clause before reaching the verb. The test: read it once, forward, at speed — can you hold the subject until the predicate lands? If you have to re-read to find "who did what," flag.

3. **Referential overload.** Within a paragraph, the count of live pronouns / definite references / tracked entities exceeds what a reader holds in working memory. Distinct from coldread's *ambiguous* pronoun (one antecedent unclear): here every reference may be individually resolvable, but there are too many at once — "he… it… the other one… that… the same…" — and the cumulative bookkeeping is the burden.

4. **Unbroken exposition / info-mass.** Explanation, backstory, mechanism or worldbuilding delivered as a continuous wall, without a scene beat, line of dialogue, action or sensory anchor to break it. The reader's attention has nothing to hold. (Distinct from coherence's *infodump* finding, which is structural placement; here it is the *reading experience* of the block — its length and unrelieved texture at reading speed.)

5. **Paragraph mass.** Paragraphs so long they present as a grey slab; the eye finds no landing. Many sentences with no break, especially in a default-register scene, raises the activation energy to keep reading. Metric: longest paragraph (sentences / approx lines) vs the scene norm.

6. **Compression opacity (too-dense-to-follow).** The inverse of slog: prose so compressed — elision, stacked telegraphic fragments, dropped referents, unbridged leaps between beats — that the reader cannot reconstruct what is happening at speed. The project may *want* compression as voice (intended-heavy), but flag where the register is default and the reader has to decompress consciously. The test: can a first-time reader narrate, in one pass, what physically happened in this stretch?

## Flagging discipline (same three-question test as sniff)

Every candidate is a *candidate*, not a verdict. Before adding to SMELL.md:

1. **Improvement test:** if you applied the fix (split the sentence, break the paragraph, intercut the exposition with a beat, vary the rhythm), does the chapter read more smoothly — state the gain in one sentence.
2. **Loss test:** what is lost — does the weight carry meaning here (tension, claustrophobia, a mind under load)? State it.
3. **Register test (this check's voice-floor):** is the stretch **intended-heavy** per Step 0? If yes → SAFE-KEEP / ACCEPT. Density that the project asked for is never a defect.

Three-tier flagging (orthogonal to Routing):

- **SAFE-CUT** — default register, clear flow gain, weight carries no meaning. Auto-applied by revise. Routing: INLINE.
- **TRADE-OFF** — flow gain is real BUT the weight also does work (tension, interiority, deliberate effort mirroring a character's effort) OR the stretch is borderline-intended. Surfaces to `SMELL-PENDING.md`; not auto-applied.
- **SAFE-KEEP** — intended-heavy register, OR the density earns its keep, OR fixing it would flatten voice. Noted in the Acknowledged block; no action.

**Calibration (load-bearing).** This check's failure mode is over-firing — sanding every chapter into the same frictionless, voiceless smoothness. Most long sentences are SAFE-KEEP; reserve SAFE-CUT for stretches where a reader at speed measurably labors and the labor buys nothing. Routing is almost always INLINE; ANCHOR-NEEDED essentially never applies (flow is a prose property).

## Output — entries appended to `SMELL.md`

Use the standard SMELL.md entry format (see `sniff.md`), with `Source: readability` and an extra `Register:` field:

```markdown
## #N — <one-line summary, e.g. "ch04 lines 88-121: six consecutive 30+-word sentences, default register, no release">

- **Source:** readability
- **Location:** ch04.md lines 88-121 (scene: Roe in the corridor)
- **Quote:** "<first ~15 words of the offending stretch> …" (stretch runs to l.121)
- **Category:** 1 — Sentence-length slog (+ 5 — Paragraph mass)
- **Register:** default  ← only `default` stretches flag; `intended-heavy` ⇒ SAFE-KEEP
- **What the reader experiences:** Six long sentences in a row with no short beat; attention drifts by the third; this scene is plot-forward (default register per tones.md §Reality), so the weight is accidental, not a chosen airlessness.
- **Routing:** INLINE
- **Flagging:** SAFE-CUT | TRADE-OFF | SAFE-KEEP
- **Improvement (if fix applied):** Splitting two sentences and adding one short beat restores rhythm; the scene moves.
- **Loss (if fix applied):** Negligible — the weight here carries no tension.
- **Suggested action:** Split the sentence at l.94 after "…corridor."; break the paragraph at l.107; let one 4-6 word sentence land before the next long one. Do NOT cut content — only re-rhythm.
```

### Readability / Flow Audit section (always present)

After the entries (and before any Acknowledged block), append the transparency audit — present even at zero flags, so the user sees the check ran:

```markdown
## Readability / Flow Audit (Source: readability)

Register map (from Step 0): <scene → intended-heavy | default>

| Scene / stretch | Register | Mean sentence len | Longest run >25w | Longest paragraph | Verdict |
|---|---|---|---|---|---|
| Opening (l.1-40) | default | 14w | 2 | 6 sentences | flows |
| Corridor (l.88-121) | default | 31w | 6 | 11 sentences | #N flagged |
| Interior collapse (l.150-178) | intended-heavy (writing-notes §register-lock) | 38w | 9 | 14 sentences | SAFE-KEEP — deliberate airlessness |

Stretches flagged: N. Stretches protected as intended-heavy: M.
Register-leak scan (Category 0, vs register-locks §<LEVEL>): K hits.
```

## Steps for the executing agent

1. Resolve the chapter file (as sniff Step 1).
2. **Step 0 — build the register map** from the project tone/style/voice/writing-notes/outline files AND extract the chapter level's Forbidden-patterns list from `register-locks.md` (item 6). This gates everything.
3. **Category 0 first — register-leak scan.** Match the whole chapter against the level's forbidden-pattern list; every hit is a SAFE-CUT / INLINE breach finding. Then read the chapter once at reading-pace, marking stretches where you labor.
4. For each labored stretch, compute the Step 0 register verdict; if intended-heavy, it is SAFE-KEEP — do not flag. If default, run the six categories and the three-question test.
5. **Pre-step archive:** SMELL.md is shared. Do NOT archive/overwrite it — append. (Archival is handled once per cycle by sniff's Step 5 or by sweep; readability appends only its own `Source: readability` entries and its audit section. If a prior readability audit section exists from this same cycle, replace that section only.)
6. Append entries + the Readability / Flow Audit section to `chapters/<book>/SMELL.md`.
7. Print: `readability: appended N entries to SMELL.md (A SAFE-CUT / B TRADE-OFF / C SAFE-KEEP). Stretches audited: S (M protected as intended-heavy).`

## Calibration

- **Flow is the goal; uniformity is not.** Varied rhythm — long then short, dense then open — *is* flow. Do not flatten variation into monotone smoothness; that is its own brick.
- **Register first, always.** Check Step 0 before every flag.
- **Cumulative, not pointwise.** One long sentence is never a finding. A *run* with no release is.
- **Re-rhythm, don't cut.** Suggested actions split, break and intercut — they do not delete content or add theme. Word count is preserved; only cadence changes.
- **Err toward SAFE-KEEP.** A characterful demanding passage a reader chooses to slow down for is good writing. Only flag the brick the reader did not choose.
