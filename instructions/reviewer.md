# Book Reviewer

Deep editorial review of written chapters. Analyzes prose quality, structural issues, and bestseller potential — the kind of honest feedback a professional editor would give.

## Invocation

```
/book review book-1
```

Optional: `/book review book-1 ch03` to review a single chapter.

Arguments: `<book>` (book-1, book-2, book-3), optionally `<chapter>` (ch01, ch02, ...).

---

## What This Skill Does

This is NOT the chapter-writer's verification (which checks completeness: beats, checklist, word count). This is an EDITORIAL REVIEW that checks whether the prose is publishable — whether a reader would keep turning pages, whether an agent would request the full manuscript.

The verification passes ask: "Did the chapter do what it was supposed to?"
The reviewer asks: "Is the chapter GOOD?"

---

## Execution

### 1. Load Reference

Read these files:
- `world/prose-rules.md` — the full prose-rule set (Rule 0 stella polare + Rules 1-24)
- `world/tones.md` — tonal registers
- `characters/notes/voice-samples.md` — voice profiles
- `world/writing-checklists.md` — for context, not re-verification
- `world/technology-comparison.md` — if it exists (needed for check I: level fingerprint)
- `plot/prestige-inventory.md` — if it exists (needed for check K and M: plants + object permanence)
- `plot/motif-tracking.md` — if it exists (needed for check M: echo-not-repetition)

Load these upfront once. Do not read them again mid-review.

### 2. Check Existing Reviews & Read the Chapters

**Before reading chapters, check `chapters/<book>/REVIEW.md`.**

If the file exists, parse the `**Reviewed:**` line to determine which chapters have already been reviewed. A chapter is considered "already reviewed" if:
1. It appears in the `**Reviewed:**` range, AND
2. It has NO unchecked (`- [ ]`) entries remaining in the REVIEW.md (all its fixes are `- [x]`).

If a chapter still has unchecked fixes, it has NOT been fully reviewed — but do NOT re-review it either. It's in the "corrections pending" state. Skip it and inform the user.

**Chapter selection logic:**
- If a specific chapter is given (e.g., `ch03`): review that chapter regardless of prior review status. This is an explicit override.
- If no chapter specified: read ALL existing chapter files in `chapters/<book>/ch*.md` (excluding plan files), then **exclude** chapters that are already reviewed (all fixes completed) or have corrections pending (unchecked fixes remain). From the remaining unreviewed chapters, **cap the session at 10**. If more than 10 unreviewed chapters exist, take the first 10 in chapter order and announce how many remain for the next session.
- If all chapters have been reviewed or are pending corrections: inform the user and stop. Do not re-review.

**Session cap rule:** Loading more than 10 chapters (~30,000 words of prose) in a single review session degrades analysis quality and risks context overflow. The cross-chapter analysis (step 4) in a capped session uses the chapters reviewed in THIS session plus the last chapter from the previous review session (for voice/pacing continuity). Relaunch `/book review <book>` for remaining chapters.

**Output to the user** which chapters are being reviewed, which are skipped (and why: "already reviewed — all fixes applied" vs "corrections pending — N fixes remaining"), and how many remain for the next session if the cap applies.

### 3. Analyze — 8 Dimensions

For each chapter (or across all chapters if reviewing a batch), evaluate:

**A. SHOW vs TELL ratio**
Find every instance where the narrator EXPLAINS what a scene just showed. Quote the offending passage. Count them. A publishable chapter has 0-1. More than 2 = problem.

Specific patterns to flag:
- "It was also the first time..."
- "What [character] recognized/understood was..."
- "This meant..."
- "In other words..."
- A paragraph that ends with a thematic summary of its own content
- The narrator decoding subtext for the reader (e.g., explaining what "I trust the pipe" really means)

**B. APHORISM count**
Find sentences that could appear on a book jacket or motivational poster without context. Quote each. Count them. Target: 0 per chapter. Each one is the writer stepping in front of the story.

**C. DIALOGUE density and quality**
Calculate approximate dialogue percentage. Is it ≥30%? Is the dialogue ALIVE — do characters interrupt, hesitate, say the wrong thing? Or is it functional — information exchange in speech marks? Quote the best and worst dialogue exchanges.

**D. STRUCTURAL variety**
How does each chapter open? Is there variety across the batch? Do any two consecutive chapters use the same structure? Is the inciting tension present within 500 words?

**E. EMOTIONAL range**
Is there at least one moment per chapter where a character's reaction is messy, disproportionate, or surprising? Or is everything perfectly calibrated understatement? Quote the messiest emotional moment. If there isn't one, flag it.

**F. NARRATOR intelligence**
Does the narrator stay at the POV character's level? Or does the narrator analyze, classify, and explain the character's unconscious behavior with the vocabulary of a literary critic? Quote the worst offender in each chapter.

**G. WORLDBUILDING balance**
How many words are spent on environment/setting before the first piece of tension or action? Is the world emerging from action, or is it described in blocks that pause the story? Give a word count for "words before tension" in each chapter.

**H. PAGE-TURNER test**
The most subjective but most important question: at the end of each chapter, does the reader NEED to keep reading? Not "want to" — NEED to. Is there enough momentum, enough unresolved tension, enough emotional investment? Rate each chapter's cliffhanger pull on a 1-5 scale.

**I. READER LOGIC test (added Phase 25)**
Read each chapter as a READER, not as a project manager. For each scene:
- "Does this make sense to someone who only knows what previous chapters established?" If not, flag it — what's missing?
- "Would a reader ask 'but why does this character do this?' or 'how does this character know this?'" If yes, flag it.
- "Is anything only comprehensible because the worldbuilding docs explain it?" If yes, the chapter has failed to establish context. The worldbuilding docs don't ship with the book.
- "Does the world feel like THIS world or like generic dystopia/sci-fi?" Check `world/technology-comparison.md` — are the level's technological fingerprints visible in the prose?

**J. CHARACTER INVESTMENT test (added Phase 25)**
After reading each chapter, ask: "Do I care about this person?" If the answer is "I'm interested in the plot but not the person" — the character hasn't earned investment. Flag which scenes establish WHO this person IS (backstory, reaction, flaw, warmth, humor) vs which scenes establish WHAT IS HAPPENING TO them. A reader follows a person, not a situation.

**K. READER ARCHITECTURE test**
Evaluate how well the chapter manages the reader's knowledge, beliefs, and attention:
- **Plant density:** How many details in this chapter will pay off later? (Target: ≥1 per chapter. If `plot/prestige-inventory.md` exists, cross-reference.) Flag chapters with 0 plants — they're missed opportunities.
- **False belief management:** Is the reader's incorrect understanding being maintained where it should be? Or does the chapter accidentally reveal something too early? Quote any line that risks spoiling a later reveal.
- **Re-read reward density:** How many details would hit differently on a second reading? (Target: ≥1 per chapter.) Quote the best re-read detail. Flag chapters with 0.
- **Misdirection health:** If the project has active misdirections (e.g., a false villain, a trusted character who will betray), is the chapter reinforcing or weakening them? A misdirection that weakens before the planned reveal is a structural failure.
- **Information reveal pacing:** Is the chapter giving the reader too much, too little, or just right? Does the reader have 2-3 open questions at the end? Does the chapter close a question while opening a new one?

**L. SIMULTANEITY & SPECTACLE test (ONLY for [RAPID CROSS-CUT] or climax chapters — skip otherwise)**
- **Causal chain clarity:** Can the reader reconstruct how Action A in Level X caused Consequence B in Level Y? Or are the cross-cuts merely parallel? Quote the strongest and weakest causal links.
- **Physical countdown:** Is a ticking clock indicator present and trackable across every cross-cut section? Does it create body-level urgency?
- **Prose rhythm:** Do section lengths compress as the sequence escalates? Measure the word count of each cross-cut section — is there a clear acceleration pattern?
- **Rules-as-spectacle:** Does the reader feel the world's RULES creating the drama (not just characters reacting to events)? The mechanism should be the action, not the backdrop.

**M. STYLE-RULE AUDIT (Rules 13-24 + Rule 0 stella polare + Rule 1 metaphor clause)**

A compact per-chapter check against the cinematic+bestseller style codification. Quote the offender for any violation.

- **Rule 0 — Stella Polare:** can every sentence be filmed AND felt in the body? Find one sentence that fails both (pure essay/abstraction). Quote it. Zero = PASS; quote one = HIGH severity.
- **Rule 1 metaphor clause + Rule 9 metaphor cap:** any metaphor in narration (e.g. `his life was a prison`, `the room was a tomb`, `like a shadow`, `as if she were drowning`)? Quote each. Target 0. Each hit = HIGH.
- **Rule 13 — Cut, don't transition:** any banned transition phrase in the chapter? (`later that day`, `a few hours later`, `after that`, `eventually`, `meanwhile`, `più tardi`, `dopo`, `in seguito`, `frattanto`, `eventualmente`). Quote each. Any hit = HIGH.
- **Rule 14 — Dialogue from desire, not information:** any exchange where a character delivers worldbuilding to another character without intent/stakes? Any `as you know…` construction? Quote the worst offender. Any hit = HIGH.
- **Rule 15 — Dialogue tags invisible:** count variant tags (whispered / muttered / exclaimed / retorted / gasped / snapped / hissed / breathed / mormorò / sussurrò / esclamò / ribatté / ansimò / sibilò). Report count. >2 per chapter = MEDIUM.
- **Rule 16 — Object permanence:** does the chapter touch/use/notice a prior-introduced object OR plant a new object? Quote the object beat. Neither present = NOTE.
- **Rule 17 — Temporal precision:** any vague time reference (`a while later`, `in the afternoon`, `soon`) where a precise one would fit? Quote each. Pattern of vagueness = MEDIUM.
- **Rule 18 — Sentence length as pulse:** for climax chapters, measure opening vs closing avg sentence length. Report both. <30% reduction from opening to closing = HIGH.
- **Rule 19 — Echo, not repetition:** any motif phrase returning from an earlier chapter? Does it carry a new meaning, or is it identical in effect? Quote the recurrence + its original. Identical effect on return = MEDIUM.
- **Rule 20 — Silence as tool:** does this chapter contain a dramatic peak (revelation, body blow, betrayal, death, crossing, discovery)? If yes, is there at least one silent beat (white-space break or single-line paragraph isolated between longer paragraphs) after the peak? No silent beat on a peak chapter = HIGH.
- **Rule 21 — Chapter opening: image + tension within 150 words:** read the first 150 words. Is there concrete image AND tension? Quote the opening sentence. Banned opener (stative `was X`, `It was Y`, `The Z did W as usual`) = HIGH.
- **Rule 22 — Chapter closing: single line or image:** count sentences in the final paragraph. >2 = HIGH. Is the closing a summary/contemplative wrap-up? If yes = HIGH. Quote the final paragraph.
- **Rule 23 — Reader smarter than character:** is there at least one signal the POV character notices but does not process, that the reader can recognize as meaningful (now or on re-read)? If zero = NOTE.
- **Rule 24 — Consequence, not explanation:** any narrator paragraph explaining HOW a mechanism works (not a character discovering it through action, and not a diegetic artifact like a cassette/letter)? Quote each. Any hit = HIGH. Character problem-solving in technical vocabulary (verb mode) is PASS; narrator exposition in technical vocabulary (subject mode) is FAIL.

### 4. Cross-Chapter Analysis (batch review only)

If reviewing multiple chapters:

- **Voice drift:** Do the characters' voices stay distinct across chapters? Do characters. voices stay distinct across chapters? Does any POV character.s voice bleed into the narrator.s?
- **Pacing arc:** Is tension building across the batch? Or does each chapter feel like it starts from zero?
- **Echo threading:** Are there cross-level echoes (Reality ↔ Dome) that the attentive reader can catch?
- **Repetition:** Same phrases, same constructions, same emotional beats repeated across chapters?

### 5. Output — The Report

Structure the report as:

```
## Book Reviewer Report — [Book] [Chapters reviewed]

### Executive Summary
[2-3 sentences: overall quality assessment, biggest strength, biggest problem]

### Chapter-by-Chapter

#### Ch. N — [Title]
- Show/Tell violations: X [quotes]
- Aphorisms: X [quotes]
- Dialogue: XX% [best/worst exchange quoted]
- Opening: [type], tension at word ~XXX, first-150w image+tension? [yes/no]
- Closing: [final paragraph sentence count, type F/G/H/I/J, summary? yes/no]
- Emotional messiness: [present/absent, quote if present]
- Narrator overreach: [worst quote]
- Setting before tension: XXX words
- Page-turner pull: X/5
- Plants: X [what pays off later]
- Re-read rewards: X [best detail quoted]
- Misdirection status: [maintained/weakened/N/A]
- Metaphors in narration: X [quotes — target 0]
- Variant dialogue tags: X [target ≤2]
- Banned transitions: X [quotes — target 0]
- Object permanence: [prior-object touched / new plant / none]
- Silence beat (if peak chapter): [present/absent]
- Temporal precision: [any vague-time drift? quotes]
- Mechanism explanation in narration: [present/absent, quote if present]

#### Ch. N+1 — ...

### Cross-Chapter Issues
[Voice drift, pacing, echoes, repetition, information reveal pacing]

### Top 5 Things to Fix
[Ordered by impact. Specific, actionable.]

### Top 5 Things That Work
[What to keep and build on.]
```

### 6. Write the Review Devplan (MANDATORY)

After the report, create (or update) the file `chapters/<book>/REVIEW.md`. This is a **correction devplan** — an ordered checklist of every fix the reviewer identified, sorted by impact (highest first).

Each fix is a checkbox with: severity tag, chapter reference, exact quote to find, and the correction instruction.

Severity tags:
- **[CRITICAL]** — Structural duplication, broken endings, missing beats. The chapter doesn't work until this is fixed.
- **[HIGH]** — Show/tell violations, narrator overreach, repeated motifs hardening into tics. Quality-blocking.
- **[MEDIUM]** — Aphorisms, borderline vocabulary violations, pacing sags. Noticeable but not fatal.
- **[LOW]** — Minor word choices, frequency tweaks, optional polish. Nice-to-fix.

Format:

```markdown
# Book N — Review Corrections

**Reviewed:** Ch. X – Ch. Y
**Date:** YYYY-MM-DD
**Verdict:** [summary — would an agent request the full manuscript?]

## Critical

- [ ] **Ch. NN, line ~XXX** — [description]. Find: `"exact quote to locate"`. Fix: [specific instruction — cut, rewrite, restructure].
- [ ] ...

## High

- [ ] **Ch. NN, line ~XXX** — [description]. Find: `"exact quote"`. Fix: [instruction].
- [ ] ...

## Medium

- [ ] ...

## Low

- [ ] ...

## Cross-Chapter (apply across all reviewed chapters)

- [ ] **[severity]** — [pattern description]. Affected: Ch. X, Ch. Y, Ch. Z. Fix: [instruction].
- [ ] ...
```

Rules for the devplan:
- Every fix from "Top 5 Things to Fix" MUST appear as a checkbox.
- Every show/tell violation, aphorism, and narrator-overreach quote from the chapter-by-chapter analysis MUST appear as a checkbox.
- Cross-chapter repetition problems get their own section at the bottom.
- Fixes are ordered: CRITICAL first, then HIGH, MEDIUM, LOW. Within each severity: ordered by chapter number.
- Each checkbox must contain enough context to find and fix the issue without re-reading the full report.
- When the reviewer runs again later, it checks existing `REVIEW.md` entries and marks completed ones `[x]` if the fix has been applied. New issues get appended.

---

## Rules

- ❌ Never soften the assessment. If it's bad, say it's bad.
- ❌ Never say "this is a matter of taste" for problems that are structural.
- ❌ Never confuse completeness (beats hit, checklist passed) with quality (prose that compels).
- ❌ Never skip the Review Devplan. The report is analysis; the devplan is the actionable output.
- ✅ Quote specific passages — don't speak in generalities.
- ✅ Compare to the target: a novel a reader can't put down, not an experiment they admire.
- ✅ The question is always: would an agent at a top literary agency request the full manuscript after reading these chapters?
