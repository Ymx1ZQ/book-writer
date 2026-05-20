# `/book coldread` — first-time-reader developmental pass

Read the chapter the way a reader holding the physical book reads it: with no access to the outline, the character sheets, the worldbuilding, or the writing notes — only what the published pages before this one have already told them. Catch what every other check is structurally blind to: whether the chapter is *alive on the page* and *legible to someone who does not have the canon*.

## Why this check exists

Every other pass in the pipeline reads WITH the canon loaded:

- `coherence-check.md` / `continuity-check.md` verify the chapter against `world/`, `characters/`, `plot/`.
- `reviewer.md` loads `voice-samples.md` and the POV character's sheet.
- `sniff.md` loads the level files and `timeline.md`.
- `proof-reader.md` loads the proper-noun canon.

That is correct for those checks — and it makes all of them unable to answer one question: *does this chapter work for a reader who has none of those files?* A reviewer that knows `davan.md` reads an empty chair as grief. A first-time reader reads an empty chair as an empty chair. The reviewer cannot un-know the canon; it will assert "the character reads as a person" because the ingredients are present in files the reader will never see.

`/book coldread` is the developmental-editor pass. It is the only check that reads cold. It does not verify correctness and it does not police line-craft — it asks whether the chapter has a reason to be turned page by page, and whether its most important moments land for someone reading blind.

## Context discipline — READ THIS FIRST

The executing agent MUST read **only**:

- the target chapter file, and
- every prior chapter of the same book, in order (`ch01.md` … up to the chapter before the target).

The agent MUST NOT read: `outline.md`, `writing-notes.md`, `state.md`, anything under `world/`, `characters/`, or `plot/`, the `SMELL.md` / `REVIEW.md` / `PROOFREAD.md` finding files, or `CLAUDE.md` project content beyond what is needed to locate the chapters directory. If the agent carries canon facts in working memory from earlier in the session, it must set them aside and judge only what the chapter pages deliver. **The whole value of this pass collapses if canon leaks in** — a finding reasoned from a file the reader cannot see is a false negative.

If the target is `ch01`, there are no prior chapters; the agent reads the chapter alone (a true cold open).

## Usage

```
/book coldread <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`).
- `chNN` — optional. If provided, cold-reads that chapter. If omitted, cold-reads the most recently modified `chapters/<book>/ch*.md`.

## Output

Writes `chapters/<book>/COLDREAD.md`.

## Reader persona for the executing agent

You are holding the book. You bought it, or a friend lent it to you. You are not the author, not an editor, not invested. You have read everything up to this page and nothing else. You will put the book down if a chapter bores you. You are generous enough to keep going when something pulls — a question, a person you have come to care about, a tightening — and ruthless enough to disengage when a chapter is the same note held for ten pages. You judge only what is on the page.

## The five reads

Run the chapter through five questions. Each produces zero or more findings.

### 1. Scene engine — does the POV character want something?

A scene needs the POV to want something in it — something small is fine, even just "to get through the shift without feeling the empty chair." If the POV wants nothing and merely registers events at uniform affect, the scene has no engine and the reader has nothing to pull against. **Finding if:** you cannot name, in one plain sentence, what the POV character is trying to do or to avoid in this chapter.

### 2. Propulsion — does tension rise, or stay flat?

Read section by section (scene break to scene break). At each break, ask: is the pressure higher than at the last break? A chapter can have a strong final line and a dead body — propulsion is the *middle*, not the close. **Finding if:** a stretch of the chapter holds the same intensity for a long run with no rising question, no escalation, no change in the POV's situation.

### 3. Legibility — do the important moments land cold?

Name the 3 (±1) most important things that happen in the chapter. For each, ask: would a reader who has read only the prior chapters understand *why it matters*? A plot event whose stakes live in a file the reader cannot see is illegible. The classic failure: a name dropped once, expecting the reader to feel a loss for a person they were never introduced to. **Finding if:** an important moment's weight depends on information the chapter — and the prior chapters — never delivered to the reader.

### 4. Monotone — is one device carrying the chapter?

Without counting precisely (`sniff.md` §10.f does the metrics), ask the reader's question: does the chapter feel like one trick repeated? If a single sentence-shape or rhetorical move is the dominant texture — so the prose has one volume and you cannot feel which beats are meant to matter — that is a monotone. **Finding if:** you could name the chapter's defining device after two pages, and it never varies after.

### 5. Emotional core — is there one, and is it legible?

What is the chapter's emotional center — the thing it wants the reader to *feel*, not to know? Is it on the page for a cold reader, or only implied for someone holding the character sheet? **Finding if:** the chapter has an emotional core but a cold reader would miss it — or it has no emotional core at all.

## Severity

Each finding carries a severity:

- **BLOCK** — the chapter does not function for a first-time reader: no scene engine, OR a dead middle with no propulsion, OR the emotional core is illegible cold. A BLOCK means the chapter is not done, regardless of how clean every other pass is.
- **WEAKNESS** — the chapter functions, but a real reader's engagement dips: a monotone stretch, one illegible secondary moment, a slack section.
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

If the chapter has zero findings, still write the file with the Cold verdict paragraph and `Findings: 0 BLOCK / 0 WEAKNESS / 0 NOTE` — the verdict is the artifact.

## Steps for the executing agent

1. Resolve the target chapter: if `chNN` provided, that chapter; else the most recently modified `chapters/<book>/ch*.md`.
2. Read every prior chapter of the book in order, then the target chapter. Read **nothing else** — see Context discipline.
3. **Pre-step archive:** if `chapters/<book>/COLDREAD.md` exists from a prior cycle, rename it to `chapters/<book>/archive/COLDREAD-<YYYYMMDD-HHMMSS>-<chapter>.md` (creating the archive subdir if needed) before writing the new one.
4. Run the five reads. For each, produce findings with severity.
5. Write the **Cold verdict** paragraph first — the honest gut reaction, would-you-turn-the-page — then the findings in chapter order.
6. Write `chapters/<book>/COLDREAD.md`.
7. Print: `wrote COLDREAD.md — N findings (A BLOCK / B WEAKNESS / C NOTE). Cold verdict: <page-turn yes / no / qualified>.`

## Calibration

- **You are not the editor. You do not know the plan. Judge the pages.** If you catch yourself reasoning from a fact the chapter never stated, stop — that is the failure mode this pass exists to prevent.
- **Generosity and ruthlessness both.** Keep reading when something genuinely pulls; say so plainly when nothing does.
- **"Boring" is a valid, important finding** — but name *where* and *why* (one device, no engine, no rising question). Never just "this chapter is slow."
- **A clean chapter that no one would turn the page for is a failed chapter.** Correctness is the other passes' job. Aliveness is yours.
- **Legibility is judged from the reader's seat, not the writer's.** "The reader can infer it" is not the same as "the chapter delivered it." If the weight of a moment sits in a file the reader will never open, it is not on the page.
