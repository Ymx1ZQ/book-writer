# `/book coldread` — first-time-reader developmental pass

Read the chapter the way a reader holding the physical book reads it: carrying forward what the earlier chapters left them with, and nothing else — no outline, no character sheets, no worldbuilding, no writing notes. Catch what every other check is structurally blind to: whether the chapter is *alive on the page* and *legible to someone who has only the book*.

## Why this check exists

Every other pass in the pipeline reads WITH the canon loaded:

- `coherence-check.md` / `continuity-check.md` verify the chapter against `world/`, `characters/`, `plot/`.
- `reviewer.md` loads `voice-samples.md` and the POV character's sheet.
- `sniff.md` loads the level files and `timeline.md`.
- `proof-reader.md` loads the proper-noun canon.

That is correct for those checks — and it makes all of them unable to answer one question: *does this chapter work for a reader who has none of those files?* A reviewer that knows `davan.md` reads an empty chair as grief. A first-time reader reads an empty chair as an empty chair. The reviewer cannot un-know the canon; it will assert "the character reads as a person" because the ingredients are present in files the reader will never see.

`/book coldread` is the developmental-editor pass. It is the only check that reads cold. It does not verify correctness and it does not police line-craft — it asks whether the chapter has a reason to be turned page by page, and whether its most important moments land for someone reading the book and only the book.

## Context discipline — READ THIS FIRST

A reader at chapter N is not starting fresh and is not re-reading the whole book. They carry a *compressed memory* of everything so far. coldread models exactly that. The executing agent reads **only**:

1. **The reader-state snapshot** `chapters/coldread-state/book-N-ch(NN-1).md` — what a reader retains entering this chapter (see next section). For ch01 there is no snapshot — a true cold open.
2. **The immediately-preceding chapter in full** — `ch(NN-1).md` — sharp short-term memory of the handoff (the cliffhanger just inherited, the exact note the last chapter ended on). For ch01 there is none.
3. **The target chapter** — `chNN.md`.

The agent MUST NOT read: `outline.md`, `writing-notes.md`, `state.md`, anything under `world/`, `characters/`, or `plot/`, the `SMELL.md` / `REVIEW.md` / `PROOFREAD.md` finding files, or `CLAUDE.md` project content beyond locating the chapters directory. If the agent carries canon facts in working memory from earlier in the session, it sets them aside and judges only what the snapshot and the chapter pages deliver. **The whole value of this pass collapses if canon leaks in** — a finding reasoned from a file the reader cannot see is a false negative; a chapter excused by a fact the reader was never given is a false pass.

This bounds the cost: one snapshot (~1.5k tokens) + one prior chapter + the target chapter — flat, regardless of how deep into the trilogy the chapter sits.

## The reader-state snapshot

`chapters/coldread-state/book-N-chNN.md` — one file per chapter, holding what a reader *retains* as of the end of that chapter (= what they carry *into* the next chapter). The files are book-prefixed and form one trilogy-continuous chain: `book-1-ch30` → `book-2-ch01` → … — reader memory does not reset between books.

Each snapshot has four blocks, **sized like reader memory — the strong retained beats, not a log**:

- **Open loops** — unresolved questions, cliffhangers, ticking clocks: what the reader is still actively wondering.
- **Character investment** — per major character: how much the reader cares, what they know about them, the character's current situation. (This is what tells coldread, for a chapter introducing a new POV, that investment in that character is *zero*.)
- **Emotional / thematic throughline** — where the reader's emotional state and the book's felt concerns stand.
- **Planted-but-unresolved** — setups the reader has registered as load-bearing ("this will matter").

Rules:

- The snapshot is built ONLY from chapter texts, by coldread itself. It is **never** seeded from `state.md`, `outline.md`, or any canon file — `state.md` is authorial bookkeeping and includes what the reader does not yet know; the snapshot is strictly reader-side.
- It is a memory, not a transcript. Resolved loops get closed and dropped; minor texture decays; only what a real reader would still be holding survives. A snapshot that grows without bound is wrong.

## Usage

```
/book coldread <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`).
- `chNN` — optional. If provided, cold-reads that chapter. If omitted, cold-reads the most recently modified `chapters/<book>/ch*.md`.

## Output

Writes `chapters/<book>/COLDREAD.md` (the findings) and `chapters/coldread-state/<book>-<chNN>.md` (the updated snapshot).

## Reader persona for the executing agent

You are holding the book. You bought it, or a friend lent it to you. You are not the author, not an editor, not invested. You have read everything up to this page and nothing else. You will put the book down if a chapter bores you. You are generous enough to keep going when something pulls — a question, a person you have come to care about, a tightening — and ruthless enough to disengage when a chapter is the same note held for ten pages. You judge only what is on the page and what the earlier pages left you carrying.

## The five reads

Run the chapter through five questions. Each produces zero or more findings. Reads 1 and 2 are judged as a *continuation* — against the inherited snapshot, not from zero.

### 1. Scene engine — does the POV character want something?

A scene needs the POV to want something in it — small is fine. The want may be **fresh to this chapter** OR a **book-level want carried forward** (from the snapshot's open loops / character investment): a reader pulled by "will she reach the Gate" does not need the chapter to manufacture a new want. **Finding if:** you cannot name, in one plain sentence, what the POV is trying to do or avoid — and no live inherited want is on the page either.

### 2. Propulsion — does tension rise, or stay flat?

Judge propulsion as continuation. The chapter opens already carrying the prior chapter's pressure and the snapshot's open loops; the question is whether it **honors and advances** that inherited tension, and whether it adds its own. Read section by section (scene break to scene break): is the pressure higher than at the last break? A chapter can have a strong final line and a dead body — propulsion is the *middle*. **Finding if:** a stretch holds the same intensity for a long run with no rising question, no escalation, no change in the POV's situation. A BLOCK-level "no propulsion" is valid only when the chapter *both* fails to generate its own pull AND squanders the inherited tension (ignores the open loops, lets the cliffhanger go slack).

### 3. Legibility — do the important moments land cold?

Name the 3 (±1) most important things that happen. For each: would a reader with the snapshot + the prior chapters understand *why it matters*? A plot event whose stakes live in a file the reader cannot see is illegible. The classic failure: a name dropped once, expecting the reader to feel a loss for a person they were never introduced to. **Finding if:** an important moment's weight depends on information neither the chapter, the prior chapter, nor the snapshot ever delivered.

### 4. Monotone — is one device carrying the chapter?

Without counting precisely (`sniff.md` §10.f does the metrics), ask the reader's question: does the chapter feel like one trick repeated? If a single sentence-shape or rhetorical move is the dominant texture — so the prose has one volume and you cannot feel which beats are meant to matter — that is a monotone. **Finding if:** you could name the chapter's defining device after two pages, and it never varies after.

### 5. Emotional core — is there one, and is it legible?

What is the chapter's emotional center — the thing it wants the reader to *feel*, not to know? Is it on the page (or carried legibly by the snapshot's investment), or only implied for someone holding the character sheet? **Finding if:** the chapter has an emotional core a cold reader would miss — or has none at all.

## Severity

- **BLOCK** — the chapter does not function for a first-time reader: no scene engine and no live inherited want, OR a dead middle that also squanders inherited tension, OR the emotional core is illegible cold. A BLOCK means the chapter is not done, regardless of how clean every other pass is.
- **WEAKNESS** — the chapter functions but a real reader's engagement dips: a monotone stretch, one illegible secondary moment, a slack section.
- **NOTE** — an observation worth the writer's attention, not a defect.

## Findings are developmental — not auto-applied

`COLDREAD.md` findings are NOT consumed by `/book revise` for auto-application. A scene-engine fix or a legibility fix is a creative rewrite, not a line edit — it cannot be applied mechanically. `COLDREAD.md` is a report for the writer (the next write/revise cycle, or the user). A BLOCK-severity finding should become a named rewrite milestone in `DEVPLAN.md`, authored deliberately — never silently auto-patched.

## Output format — `COLDREAD.md`

```markdown
# COLDREAD.md — Chapter <id>, cold-read <date>

**Cold verdict:** <one paragraph — would a first-time reader turn the page? what pulls, what drags. Honest, plain, no craft jargon.>

Findings: A BLOCK / B WEAKNESS / C NOTE

## #N — <one-line summary>

- **Read:** [1 Scene engine | 2 Propulsion | 3 Legibility | 4 Monotone | 5 Emotional core]
- **Severity:** BLOCK | WEAKNESS | NOTE
- **Location:** [section / line range / "chapter-wide"]
- **What the cold reader experiences:** [concrete — what the reader feels, or fails to feel, and where]
- **What's missing on the page:** [the canon fact or the craft move the chapter leans on but never delivers to the reader]
- **Developmental direction:** [what kind of rewrite would fix it — a direction, not a line edit]
```

If the chapter has zero findings, still write the file with the Cold verdict paragraph and `Findings: 0 BLOCK / 0 WEAKNESS / 0 NOTE`.

## Steps for the executing agent

1. Resolve the target chapter: if `chNN` provided, that chapter; else the most recently modified `chapters/<book>/ch*.md`.
2. **Load inherited context** — read `chapters/coldread-state/<book>-ch(NN-1).md` (the snapshot) and `chapters/<book>/ch(NN-1).md` (the prior chapter, full). For ch01, skip both — a true cold open.
3. **Bootstrap / ordering check:** if the `<book>-ch(NN-1)` snapshot is absent (or its chain is incomplete), build the missing snapshots first — cold-read the missing chapters in order, oldest first, each producing its snapshot — then proceed. Across a book boundary, `book-(N-1)-ch<last>` is the snapshot that precedes `book-N-ch01`.
4. Read the target chapter. Read **nothing else** — see Context discipline.
5. **Pre-step archive:** if `chapters/<book>/COLDREAD.md` exists from a prior cycle, rename it to `chapters/<book>/archive/COLDREAD-<YYYYMMDD-HHMMSS>-<chapter>.md` (creating the archive subdir if needed) before writing the new one.
6. Run the five reads (Reads 1-2 as continuation against the snapshot). Produce findings with severity.
7. Write the **Cold verdict** paragraph first — the honest gut reaction, would-you-turn-the-page — then the findings in chapter order. Write `chapters/<book>/COLDREAD.md`.
8. **Fold step:** write the updated snapshot `chapters/coldread-state/<book>-chNN.md` = the N-1 snapshot with chapter N's changes folded in — new open loops added, resolved ones closed and dropped, character investment updated, throughline advanced. Keep it memory-sized. (Re-cold-reading chapter N overwrites this snapshot; snapshots for chapters after N are now stale and are rebuilt when those chapters are re-cold-read.)
9. Print: `wrote COLDREAD.md — N findings (A BLOCK / B WEAKNESS / C NOTE); updated snapshot <book>-chNN. Cold verdict: <page-turn yes / no / qualified>.`

## Calibration

- **You are not the editor. You do not know the plan. Judge the pages.** If you catch yourself reasoning from a fact the chapter never stated and the snapshot never carried, stop — that is the failure mode this pass exists to prevent.
- **Inherited momentum is credited, never an alibi.** A reader at chapter N arrives invested; a chapter may legitimately ride that. But a chapter that *only* coasts on inherited tension and advances nothing of its own is still a finding. Crediting the inheritance is not excusing the chapter.
- **Inheritance is POV-specific.** A chapter introducing a brand-new POV inherits the book's open loops but **zero investment in that character** — it must do more first-chapter-of-a-character work, not less. Check the snapshot's Character-investment block before judging Reads 1 and 5.
- **Generosity and ruthlessness both.** Keep reading when something genuinely pulls; say so plainly when nothing does.
- **"Boring" is a valid, important finding** — but name *where* and *why* (one device, no engine, no rising question). Never just "this chapter is slow."
- **A clean chapter that no one would turn the page for is a failed chapter.** Correctness is the other passes' job. Aliveness is yours.
