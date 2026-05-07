# Book Proof Reader

Line-level proofreading of written chapters. This is the LAST pass before a chapter is considered finished — everything structural, narrative, and editorial has already been checked. This skill catches what spellcheck catches and what spellcheck misses.

## Invocation

```
/book proofread book-1 [ch03]
```

Arguments: `<book>` (book-1, book-2, book-3), optionally `<chapter>` (ch01, ch02, ...). If no chapter specified, proofread all existing chapters in the book.

---

## What This Skill Does

This is NOT editorial review (that's `/book review`). This is NOT narrative verification (that's the chapter-writer's 9 passes). This is **line-by-line language quality control** — the equivalent of a human proofreader with a red pen and a style guide.

The style guide is defined in the project.s `CLAUDE.md` (language, tense) and character/world files (proper nouns, terminology).

---

## Process

### 1. Load Reference

Read these files:
- `CLAUDE.md` — confirms "American English" as the language standard
- `characters/notes/voice-samples.md` — for proper noun spellings and character-specific vocabulary boundaries
- `world/prose-rules.md` — for line-level style grep patterns (P9)
- The target chapter file(s)

### 2. Run 9 Proofreading Checks

For each chapter, scan every line and report issues with **exact quotes and line numbers**.

---

#### P1. Grammar

- Subject-verb agreement errors
- Dangling or misplaced modifiers ("Walking to the terminal, the door opened" — the door didn't walk)
- Pronoun reference ambiguity (unclear "he/she/it/they" where multiple referents are possible)
- Sentence fragments that are NOT intentional style (Lena/Roe's clipped prose uses intentional fragments — these are fine. Unintentional fragments in Noah's POV or narration are errors.)
- Double negatives, split infinitives only if awkward, other structural grammar issues

**The rule:** Intentional rule-breaking for voice is fine (Roe's fragments, Lena's clinical truncation). Unintentional errors are not. If in doubt: does the construction serve the character's voice? If yes, leave it. If it's just sloppy, flag it.

#### P2. Tense Consistency

- The project's default tense is defined in `CLAUDE.md`. Typically past tense for fiction. Present tense is used ONLY for:
  - Text rendered as in-world system output (terminals, interfaces) may use present tense.
  - In-world game or interactive system output may use present tense.
  - Internal monologue fragments where the character's thought is rendered as present-tense flash (rare, intentional)
- Flag any unintentional tense shift — a paragraph that starts in past and slips into present, or vice versa.
- Pay special attention to complex sentences with multiple clauses: the tense must be consistent within the sentence.

#### P3. Punctuation

- **Em-dashes:** The project uses `—` (em-dash with no spaces). Flag any `--`, ` — ` (spaces around em-dash), or `–` (en-dash used as em-dash).
- **Dialogue punctuation:** American convention. Periods and commas INSIDE quotation marks. `"I know," she said.` NOT `"I know", she said.`
- **Quotation marks:** Double quotes for dialogue (`"..."`). Single quotes ONLY for quotes-within-quotes (`"She said 'don't' and left."`).
- **Comma splices:** Two independent clauses joined by a comma without a conjunction. Flag unless clearly stylistic (Dome clinical voice sometimes uses comma splices for rhythm — flag only if accidental).
- **Serial comma (Oxford comma):** Use it. `Red, green, and blue.` NOT `Red, green and blue.`
- **Ellipses:** Three dots with no spaces (`...`). NOT `. . .` or `.. .`.
- **Apostrophes:** Straight quotes (`'`) are acceptable. Ensure possessives are correct (`Noah's` not `Noahs`; `its` vs `it's`).

#### P4. Spelling & Proper Nouns

- Run a mental spellcheck on every word. Flag obvious typos.
- **Proper noun consistency** — these must be spelled identically EVERY time:
  - **Characters:** Noah, Lena, Roe, Ettore Lautero, Anyuk Setrakian, Ainur Akhmetov, Mariette, Tavish, Sorin, Mira, Niva, Nash, Leliloo, Vera, Marko, Fabia Morandi, Davan, Lydia, Clara Vaziri, Anika Rao, Dek, Kael
  - **Designation codes:** Lena-W-72E5CB8D, Roe-B-M3K7F019, Tavish-B-9B7C41E2 (used sparingly — but when used, must match)
  - **Places:** Marseille (NOT Marseilles), Le Panier, Rue de la République, Notre-Dame de la Garde, Porta Palazzo, Camera (Turin photography centre), Isle of Wight, St. Catherine's Lighthouse
  - **Technology:** Aletheia (NOT Aletheya/Alethia), Meridian, Algorithm (capitalized when referring to the Dome's governing system)
  - **Aliases:** E. Sauveterre (with period after E)
  - **The Game:** Always capitalized when referring to the specific Game
- Flag any variant spelling of these terms.
- **Foreign-language proper-noun grammar.** For proper nouns from non-English source languages (French, Italian, Spanish, German, etc.) — toponyms, institution names, product names — the source-language grammar is normative. The most common slip is the article-preposition contraction:
  - French: `de + le → du`, `de + les → des`, `à + le → au`, `à + les → aux`. Example: `Rue de + le Petit Puits → Rue du Petit Puits` (NOT `Rue de Petit Puits`).
  - Italian: `di + il → del`, `di + lo → dello`, `di + la → della`, `a + il → al`, `da + il → dal`, `in + il → nel`, `su + il → sul`. Example: `Via di + il Foro → Via del Foro` (NOT `Via di Foro`).
  - Spanish: `de + el → del`, `a + el → al`. Example: `Calle de + el Sol → Calle del Sol` (NOT `Calle de el Sol`).
  - German: definite-article form must agree with grammatical gender + case in compound place names.
  Also generic: gender agreement, plural forms, and accent marks (é, è, à, ñ, ü, ß, etc.) must be present where the source language requires them.
  **The rule applies even when the proper noun is rendered in CAPS** (e.g., on an in-world terminal output) **or surrounded by English-language narration.** Capitalization and English context do not exempt the noun from its source-language grammar.

#### P5. American English

The project.s language is defined in `CLAUDE.md`. If American English, flag:
- British spellings: colour → color, favour → favor, realise → realize, metre → meter (unit), centre → center (EXCEPT "Camera" which is an Italian proper noun), behaviour → behavior, defence → defense, grey → gray (NOTE: "grey" is used throughout the existing worldbuilding docs — decide on convention and enforce consistently)
- British vocabulary: flat → apartment, lift → elevator (EXCEPT in Dome context where "vertical lift" is established terminology), boot → trunk, torch → flashlight, queue → line (EXCEPT in Dome/Ark context where "queue" is the natural word for rationed access)
- British punctuation: see P3 above

**Exception handling:** Some words are intentionally non-American because they belong to the world:
- "Moka pot" (Italian term, correct)
- "Cezve" (Turkish/Armenian coffee pot, correct)
- Place names in French/Italian are correct as-is
- Dome/Ark terminology may use non-American constructions if they're established world terms

#### P6. Word Repetition

- **Within a paragraph:** Flag any non-trivial word used 3+ times (excluding articles, prepositions, pronouns, character names). "The door opened. Through the door, the corridor extended. At the end of the door—" → "door" x3.
- **Within a page (~300 words):** Flag unusual/distinctive words used 2+ times. "The mechanism cycled with a whisper" ... [5 lines later] ... "The whisper of compressed air" → "whisper" x2.
- **Across consecutive chapters:** Flag signature phrases that repeat verbatim. If Ch. 5 ended with "the system hummed" and Ch. 6 opens with "the system hummed," that's a repetition problem. (Cross-chapter check only applies to same-level consecutive chapters.)

**Exclusions:** Intentional repetition for effect is fine (Roe's "it doesn't calibrate" motif, the five-note description). Tic gestures repeating are fine (they're supposed to). Flag only UNINTENTIONAL repetition.

#### P7. Sentence Rhythm & Readability

- Flag passages where 5+ consecutive sentences have the same structure (e.g., all start with "She" or "He" or "The").
- Flag passages where 5+ consecutive sentences are the same approximate length (all short-short-short or all long-long-long). Variation is required.
- Flag sentences over 50 words that are hard to parse on first read (unless in Noah's rapid-fire speech mode, where run-ons are intentional).
- Flag paragraphs over 200 words that could be broken up.

**The rule:** Good prose breathes. Short sentence. Then a longer one that stretches and fills the space. Then short again. The variation is the rhythm. Monotony in either direction is a problem.

#### P8. Dialogue Formatting

- Each new speaker gets a new paragraph.
- Dialogue tags: "said" is invisible and preferred. Flag overuse of variant tags ("he exclaimed," "she breathed," "he intoned," "mormorò," "sussurrò") — max 2 per chapter per `prose-rules.md §Rule 15`. Count all variants and report the total; if >2, identify the weakest to convert to action beats.
- Action beats between dialogue: ensure they're attached to the correct speaker's paragraph.
- No dialogue tag needed when the speaker is clear from context or an action beat identifies them.
- Interior monologue: italics for direct thought only if used (the project style generally renders thought as indirect — "She wondered whether..." not *Was this right?*). Flag inconsistency.

#### P9. Style-Rule Line Patterns (`prose-rules.md` Rules 13-24)

Line-level greps for banned or capped patterns from the codified style. These are pattern-matches, not judgment calls — flag every hit.

- **Metaphor indicators in narration** (Rule 1 + Rule 9 clause): grep for `like a`, `as if`, `as though`, `was a [abstract noun such as prison/tomb/shadow/dream]`. Any hit in narration (not dialogue) is a flag. Quote the line and propose a rewrite as concrete image, synecdoche, or metonymy.
- **Banned transition phrases** (Rule 13): grep for `later that day`, `a few hours later`, `after that`, `eventually`, `meanwhile`, `più tardi`, `dopo`, `in seguito`, `frattanto`, `eventualmente`. Every hit = flag. Fix: replace with scene break (white space) + in-medias-res opening.
- **Stative chapter openers** (Rule 21): read the first sentence. If it matches pattern `[Name] was [adjective]`, `It was [time/place/weather]`, or `The [thing] did [action] as usual`, flag as banned opener. Fix: propose an in-medias-res alternative — concrete image + tension.
- **Summary chapter closing** (Rule 22): count sentences in the final paragraph. If >2, flag as closing-summary violation. Fix: identify the strongest single line and propose cutting the rest.
- **Stative `to be` verb overuse**: grep for `was`, `were`, `is`, `are` as main verbs in narration (not dialogue, not passive-voice necessary constructions). If >1 in 3 consecutive sentences of action, flag for verb-strengthening (Rule 9 extension — though not a hard fail, weak verbs collapse scenes).

**Output for P9:** each hit gets a line number, quoted passage, and the rule number violated. If the fix requires rewriting more than the minimal pattern (e.g., an opener rewrite needs a new image), note: "rewrite proposed in REVIEW.md scope, not PROOFREAD.md" and defer to the reviewer.

---

### 3. Output — The Report

For each chapter:

```
## Proofread Report — Ch. NN: [Title]

### Summary
- Grammar: X issues
- Tense: X issues
- Punctuation: X issues
- Spelling/Proper nouns: X issues
- American English: X issues
- Word repetition: X issues
- Sentence rhythm: X issues
- Dialogue formatting: X issues
- Style-rule line patterns (metaphors/transitions/openers/closers): X issues
- **Total: X issues**

### Issues (by line)

**Line ~XX:** [P1 Grammar] "quoted passage with error." → Fix: "corrected passage."
**Line ~XX:** [P4 Spelling] "Marsielle" → "Marseille"
**Line ~XX:** [P6 Repetition] "composite" used 4x in this paragraph. Vary: "the surface," "the wall," "the material."
...
```

### 4. Write PROOFREAD.md (MANDATORY)

The report is analysis; the corrections file is the actionable output. Create or update `chapters/<book>/PROOFREAD.md`.

**This file is processed by `/book fix`** — same skill that handles editorial fixes from REVIEW.md.

```markdown
# Book N — Proofreading Corrections

**Proofread:** Ch. X – Ch. Y
**Date:** YYYY-MM-DD
**Total issues:** X

## Ch. NN — [Title]

- [ ] Line ~XX: [P1 Grammar] "quoted error" → "fix"
- [ ] Line ~XX: [P4 Spelling] "Marsielle" → "Marseille"
- [ ] Line ~XX: [P6 Repetition] "composite" x4 → vary with "surface," "wall," "material"

## Ch. NN+1 — [Title]

- [ ] Line ~XX: [P3 Punctuation] `" , she said"` → `"," she said`
...
```

**Rules for PROOFREAD.md:**
- One section per chapter (all fixes for that chapter grouped).
- Each checkbox has: line number, check category [P1-P8], quoted error, and the specific fix.
- Fixes are ordered by line number within each chapter.
- Only issues that require TEXT CHANGES become checkboxes. Rhythm suggestions that are advisory (not clear errors) can be noted but not checkboxed.
- After writing, announce: *"Proofreading corrections written to PROOFREAD.md. Run `/book fix <book>` to apply."*

### 5. Summary

```
Book Proof Reader Complete
Book: [book]
Chapters proofread: X
Total issues: X
Devplan milestones created: X

Most common issue type: [P1-P8]
Cleanest chapter: Ch. NN (X issues)
Roughest chapter: Ch. NN (X issues)

Next step: /book fix <book> to apply fixes.
```

---

## When to Run This Skill

Run AFTER:
- ✅ Chapter writing is complete (`/book chapter`)
- ✅ Verification passes 1-9 are green
- ✅ Editorial review is done (`/book review`)
- ✅ Review fixes are applied (`/book fix`)

Run BEFORE:
- Declaring a chapter "final"
- Assembling the book draft

This is the LAST quality gate. After proofreading fixes are applied, the chapter is done.

---

## Rules

- ❌ Never change meaning. Proofreading fixes grammar, spelling, punctuation — NOT content, structure, or voice.
- ❌ Never flag intentional style as an error. Check each character's voice profile in their character sheet before flagging intentional style.
- ❌ Never rewrite sentences. Provide the minimal fix: the smallest change that corrects the error.
- ❌ Never skip the corrections devplan. The report without a devplan is useless.
- ✅ Quote the exact error. No paraphrasing.
- ✅ Provide the exact fix. No "consider revising."
- ✅ When in doubt about American vs British: American wins. When in doubt about comma: use it.
- ✅ Be pedantic. This is the red-pen pass. Pedantry is the job.
