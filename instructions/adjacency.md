# `/book adjacency` — cross-chapter adjacency pass

Every other analyst reads ONE chapter (against canon, against itself, against the reader's single-point memory). This pass reads a **window of consecutive chapters together** and catches the three defects that only exist *between* chapters — the ones a per-chapter QC matrix is structurally blind to:

1. **Shape repetition** — two adjacent chapters walk the same beat-skeleton, so the second reads as "I've seen this form" and drains tension.
2. **Idiolect collision** — a signature device or phrasing is reused *verbatim across different POV characters*, flattening voices the canon defines as distinct.
3. **Dramatic-irony legibility** — where the project's reader-journey design declares an irony or reader-knowledge state spanning the pair, the prose fails to make it legible to a first-time reader, so the planned irony is inert and the rhyme reads as mere repetition.

These are the exact defects a human cold-read of Book-1 ch01–ch04 surfaced (project Phase 43 / 44) and that no single-chapter analyst can see.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Single-point reader stumble (ambiguous pronoun, unsetup fact) | `coldread-enum.md` |
| Within-chapter device saturation (one form overused in one chapter) | `sniff.md` Category 10 |
| Plant → payoff bookkeeping across the book | `coherence-check.md` §Chekhov |
| Motif semantic drift across chapters | `motif.md` |
| Flow / brick within a chapter | `readability.md` |
| **"Do these adjacent chapters rhyme too closely? Do voices collide across them? Does the planned cross-chapter irony actually land?"** | **THIS check** |

`motif` tracks whether a *symbol* stays consistent across chapters; this tracks whether the *shape, the voices, and the reader's intended knowledge-state* work across the seam. It is the only analyst that holds two chapters in view at once.

**Milestone format:** see `instructions/milestone-format.md`. Two-channel + three-tier routing (below): prose-side micro-fixes → `SMELL.md` (`Source: adjacency`); **structural** findings → `DEVPLAN.md` / `SMELL-PENDING.md` for the **user** (never auto-applied).

## Usage

```
/book adjacency <book> [chNN] [chNN-chMM]
```

- `<book>` — book directory under `chapters/`.
- no chapter arg → window = the most recently written chapter + its immediate predecessor.
- `chNN` → window = ch(NN-1) + chNN (the chapter and the one before it). ch01 has no predecessor → no-op (print and exit).
- `chNN-chMM` → explicit window of consecutive chapters (e.g. `ch02-ch04`).

The default and orchestrator-wired form is the **two-chapter window [predecessor, current]** — it runs when a freshly merged chapter has a predecessor, so each new chapter is checked against the one before it as it lands.

## Inputs (read all before judging)

1. The chapters in the window (full prose).
2. `plot/reader-journey.md` — the per-chapter **New Knowledge / Active Beliefs / Dramatic Irony** rows for the window. This declares what a first-time reader is *supposed* to know and what irony is *supposed* to be live across the pair. **This is the legibility yardstick for class (c).**
3. `characters/notes/voice-samples.md` and `characters/notes/narrator-boundaries.md` — each POV character's **distinct** signature tics/idiolect. Class (b) fires only when a device the canon assigns to ONE character appears verbatim in ANOTHER's chapter.
4. `plot/motif-tracking.md` — the chapter→level map (Dome / Ark / Reality) and the foregrounded motif per chapter. Two same-level consecutive chapters carry the highest shape-repetition risk; differing foregrounded motifs are evidence the rhyme is *intended* contrast.
5. `plot/echo-choreography.md` — whether a cross-chapter rhyme is a *designed* echo (load-bearing) rather than accidental.

**Graph-assisted inputs (optional — see `instructions/graph-recall.md`):** if `graphify-out/graph.json` exists in the project root AND the freshness gate passes, run the granularity probe first: `graphify query "reader-journey state of <book> ch<NN>" --budget 4000` for the target chapter. Only if the probe returns a **per-chapter node** (the graph carries per-chapter granularity — a companion re-extraction ships it project-side, but the probe gates regardless), replace inputs 2, 4, and 5 with two queries (answer mode):

- Class (a) shape repetition: `graphify query "is the rhyme between ch<NN> and ch<MM> a designed echo" --budget 4000` — the echo-choreography + motif-tracking chapter map.
- Class (c) irony legibility: `graphify query "dramatic irony live across ch<NN> and ch<MM>" --budget 4000` — the reader-journey per-chapter rows.

All three queries pass `--budget 4000` because per-chapter node detail sits deep in the traversal output and the default 2000-token cap truncates it before the per-chapter rows surface (project-side Phase 80 M5 re-extraction finding).

Input 3 (`voice-samples.md` + `narrator-boundaries.md`) stays verbatim regardless — never-substitute list per `graph-recall.md`; class (b) always runs on the disk files. Probe fails (no per-chapter node), graph absent, or graph stale → inputs 1–5 apply unchanged.

## Reader persona for the executing agent

You are reading the window the way a first-time reader does: **in order, once, at speed, carrying the first chapter's shape into the second.** When the second chapter's beats arrive in the same order, with the same emotional cadence, you feel "haven't I just done this?" — UNLESS the text gives you a reason the return is meaningful (you now know something a character doesn't; you are watching the same machine grind a different caste). You do not supply that reason yourself; if the prose does not light it, it is not lit.

You also know the project's design. You have read `reader-journey.md`. You know which seams are *meant* to rhyme (a dramatic irony, a cross-caste mirror) — and there your job is not "is this repetitive?" but **"does the prose deliver the charge that makes the repetition worth it?"**

## The three classes

### (a) Shape repetition

Adjacent chapters share a beat-skeleton — same opening mode → same mid-turn → same closing posture — closely enough that the later one reads as a re-run.

- Map each chapter's skeleton as a short ordered list of beats (e.g. *routine-open → transit-anomaly → workstation-anomaly → record-beat → suspended-ending*). Compare.
- **Gate (load-bearing rhyme):** before flagging, check `reader-journey.md` + `echo-choreography.md`. If the parallel *serves* a declared irony or a designed cross-level/cross-caste mirror, the rhyme is **intended** — it is NOT a shape-repetition defect; route any problem to class (c) instead (the rhyme is fine, the *charge* may be missing). A rhyme is a class-(a) defect only when it is **inert** — repetition with no design reason.
- Where the rhyme IS intended but heavy, the fix is rarely "break the structure" (that can destroy the irony). Prefer: compress the *redundant establishment* the later chapter re-pays (the reader already learned the mode), and sharpen the *divergence* (where the two chapters split). **Deep beat-order reshape is a structural finding → user channel, never auto-applied.**

### (b) Idiolect collision

A signature involuntary-gesture / measurement-frame / sentence-formula that `voice-samples.md` or `narrator-boundaries.md` assigns to one POV appears **verbatim or near-verbatim in another POV's chapter**, so two characters read as one consciousness in different costumes.

- Build the per-POV signature list from canon. For each device, scan the other POV's chapter for the same wording.
- Distinguish **shared theme** (legitimate — e.g. "a body acting outside its owner's control" is a trilogy theme all three may express) from **shared phrasing** (the defect — the *same words* for it). The fix preserves the theme, differentiates the wording per idiolect.
- These are prose-side and fixable → `SMELL.md`, INLINE, usually SAFE-CUT (reword the later/derivative instance, keep the canonical owner's).

### (c) Dramatic-irony legibility

`reader-journey.md` declares, for a chapter, a Dramatic-Irony entry or a reader Knowledge-state that depends on the *previous* chapter (e.g. "Reader knows X did Y to this character; the character doesn't"). Check the later chapter's prose actually lets a first-time reader hold that knowledge across the seam.

- Identify the bridge the irony rests on (a shared entity / location / code / object named in both chapters). Is it salient enough in BOTH that a first reader connects them — or is it buried (named once, unsignposted)?
- If the bridge is faint, the irony is inert and the rhyme reads as repetition. The fix is usually a **one-line weighting** of the bridge in the later chapter (POV-clean — the character stays oblivious; only the *reader's* connective tissue is strengthened). → `SMELL.md`, INLINE, TRADE-OFF if it requires added prose; or a `Suggested action` the user ratifies.
- Never make the bridge legible by violating POV (the character must not perceive what the design says they don't know).

## Routing — two-channel, three-tier

| Finding kind | Channel | Tier |
|---|---|---|
| Idiolect collision (reword a derivative instance) | `SMELL.md` (`Source: adjacency`) | SAFE-CUT / INLINE |
| Irony-legibility bridge (a one-line weighting, POV-clean) | `SMELL.md` (`Source: adjacency`) | TRADE-OFF / INLINE |
| Inert-rhyme compression (cut redundant re-establishment) | `SMELL.md` (`Source: adjacency`) | TRADE-OFF |
| **Deep beat-order reshape** (would alter chapter architecture) | `DEVPLAN.md` phase **for the user** + note in `SMELL-PENDING.md` | **USER — never auto-applied** |

The structural tier is load-bearing: hand-reshaping a QC-closed chapter is high-risk and can destroy a designed irony. The detector **proposes** structural changes for the user; it does not let `revise` execute them.

## Output — entries appended to `SMELL.md`

Standard SMELL.md entry format, `Source: adjacency`, with a `Window:` field:

```markdown
## #N — <one-line, e.g. "ch02→ch03: first dramatic irony inert — BA-009 bridge unsignposted, rhyme reads as repetition">

- **Source:** adjacency
- **Window:** ch02 + ch03 (Dome → Dome)
- **Class:** (c) dramatic-irony legibility   ← (a) shape repetition | (b) idiolect collision | (c) irony legibility
- **Design ref:** reader-journey.md ch03 — "Reader knows Lena deleted Roe's record; Roe doesn't" (Dramatic Irony Inventory)
- **What the reader experiences:** ch03 walks ch02's beat-shape, but the link (junction BA-009 / Sector 7-A, the deleted deviation's source = Roe) is named once and unweighted, so the "I know / he doesn't" charge never fires; the rhyme reads as repetition, not dread.
- **Bridge:** junction BA-009 + Sector 7-A (the deleted entry's SOURCE in ch02; the junction Roe watches in ch03).
- **Routing:** INLINE
- **Flagging:** TRADE-OFF
- **Suggested action:** weight BA-009 in ch03 as the junction at Roe's own sector seam his route crosses, so the reader connects the deleted proximity-triplet to Roe. POV-clean — Roe stays oblivious. (If a deeper reshape is implied, it goes to the user channel, NOT here.)
```

### Adjacency Audit section (always present)

```markdown
## Adjacency Audit (Source: adjacency)

Window: ch02 + ch03 (levels: Dome, Dome)

Beat-skeletons:
- ch02: routine-open → transit-jitter → archive-sweep → self-recognition turn → ACT (delete) → flag-holds → suspended
- ch03: dispensary-open → transit-late-door → junction-sweep → glyph turn → FREEZE → nothing-logged → suspended

| Class | Verdict |
|---|---|
| (a) shape repetition | intended mirror (cross-caste + irony) — SAFE-KEEP; charge gap routed to (c) |
| (b) idiolect collision | 1 found ("without deciding" Noah↔Roe) → #N SAFE-CUT |
| (c) irony legibility | inert (#M TRADE-OFF) |

Structural findings routed to user channel: <none | DEVPLAN Phase NN>.
```

## Steps for the executing agent

1. Resolve the window (default: most-recent chapter + predecessor). If the window has <2 chapters (e.g. ch01), print `adjacency: window has no predecessor — nothing to compare` and exit 0.
2. Read all window chapters + the five input files (on the graph path, inputs 2/4/5 are replaced by the two queries — see Inputs).
3. Map each chapter's beat-skeleton; build the per-POV idiolect-signature list; pull the window's `reader-journey.md` irony/knowledge rows (or the irony-query result on the graph path).
4. Run classes (a), (b), (c) with the high burden of proof. For (a), apply the **load-bearing-rhyme gate** before flagging.
5. **Pre-step archive:** SMELL.md is shared — append only (do not overwrite). If a prior adjacency audit section from this same cycle exists, replace that section only.
6. Append prose-side entries + the Adjacency Audit to `chapters/<book>/SMELL.md`. Route any structural finding to a `## Phase <NN+1> — Adjacency structural finding (<book> <window>)` in `DEVPLAN.md` (flagged FOR USER, not for `fix`) and a pointer line in `SMELL-PENDING.md`.
7. Print: `adjacency: window <chXX+chYY> — A idiolect / B irony / C compression entries to SMELL.md; S structural → user channel.`

## Calibration (load-bearing)

- **The failure mode is destroying authored structure.** A deliberate cross-caste mirror that delivers a dramatic irony is *good craft* — flagging it as "repetition" would gut the design. Burden of proof is on the flag; when a rhyme is declared in `reader-journey.md` / `echo-choreography.md`, treat it as intended and ask only whether its *charge* lands (class c).
- **Never auto-reshape.** Structural findings are proposals to the user. `revise` may apply only the SMELL.md micro-fixes (reword, one-line bridge, targeted compression).
- **POV is inviolable.** An irony-legibility fix strengthens the *reader's* connection, never the character's knowledge.
- **Idiolect: theme shared, words distinct.** Do not flag two characters expressing the same *theme*; flag only the same *wording*. The fix differentiates phrasing, it does not delete the shared device.
- **Two chapters is the unit.** Do not try to judge a whole book's structure here; the window is small by design so the judgment stays grounded in what a reader actually carries across one seam.
