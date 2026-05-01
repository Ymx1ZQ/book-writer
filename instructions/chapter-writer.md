# Chapter Writer

Write a single chapter. This is the SINGLE SOURCE OF TRUTH for how chapters are written — `/book write` delegates here for each chapter.

## Invocation

```
/book chapter book-1 ch03
```

Arguments: `<book>` (book-1, book-2, book-3) and `<chapter>` (ch01, ch02, ..., ch31).

---

## Step 1: Load Context

Read the project's files. Paths are relative to the project root.

**Always load:**
- `CLAUDE.md` — project instructions, language, structure overview
- `chapters/<book>/outline.md` — load ONLY the specific chapter entry. Use a targeted read: locate the chapter's header (e.g., `## Ch. NN` or `### Ch. NN`) and read from there to the next chapter's header. Do NOT load the entire outline file. If the outline is split into per-chapter files (`chapters/<book>/ch<NN>.md`), read only that file.
- `chapters/<book>/state.md` — the ENTIRE most recent "After Chapter N" section
- `world/tones.md` — tonal register for this chapter's level
- `world/pacing-rules.md` — pacing and tension rules
- `world/writing-checklists.md` — sensory enforcement (read the section for this chapter's level)
- `world/prose-rules.md` — prose quality rules (CRITICAL — read every time)
- `characters/notes/voice-samples.md` — voice profiles
- `characters/notes/narrator-boundaries.md` — POV narrator rules (em-dash limits, vocabulary restrictions, metaphor register)
- `plot/cliffhanger-map.md` — cliffhanger type for this chapter

**Batch session optimization:** If running inside `/book write` (a batch session), `world/tones.md`, `world/prose-rules.md`, `world/pacing-rules.md`, and `world/writing-checklists.md` were loaded at session start and remain in context. Do NOT re-read them — they have not changed. Re-read them only when running `/book chapter` as a standalone command in a fresh session where they are not yet in context.

**Load based on level:**
Identify this chapter's narrative level from the outline. Then load files from the corresponding `world/level-*-<name>/` directory SELECTIVELY: list the files in the directory, then load only those whose `## Usage Tracker` contains items mapped to THIS chapter (matching Book and Ch). Skip files with no tracker items for this chapter — they waste context. Also load `world/technology-comparison.md` (or equivalent) to ensure this level's tech fingerprint is correct and distinct from other levels.

**Load based on POV character:**
- The POV character's sheet from `characters/foreground/` or `characters/midground/`
- Sheets for other characters appearing in this chapter

**Load from `context:` tag (MANDATORY):**
Read the `context:` field from this chapter's header in the outline. Load every file listed there in addition to the always-loaded set. These are the conditional context files for this chapter — determined during outline planning, not at the writer's discretion. If a file in the context tag does not exist, stop and report.

Also load any `plot/` files explicitly referenced in the chapter's scene beats (e.g., mythology fragments) that are not already in the `context:` tag.

**Load if they exist (optional — reader architecture support):**
- `plot/prestige-inventory.md` — plants and payoffs; check if this chapter has a plant or payoff assigned
- `plot/motif-tracking.md` — which motif is foregrounded in this chapter
- `plot/reader-journey.md` — what the reader knows/believes/feels at this point
- `plot/echo-choreography.md` — cross-level echo assignments for this chapter

**Load if they exist AND chapter is tagged [RAPID CROSS-CUT] or is a climax chapter:**
- `plot/climax-choreography.md` — beat-by-beat simultaneity design for the climax sequence
- `plot/mechanical-set-pieces.md` — rule-driven spectacle scenes
- `plot/ticking-clocks-physical.md` — physical countdown indicators for this chapter

If none of these files exist, skip — the skill works without them. If they exist, they inform the Reader Architecture section and the Simultaneity section of the plan.

Announce: *"📖 Ch. N: [title] — [Level] / [POV] / [Tone] / Cliffhanger: [type]"*

---

## Step 2: Plan (MANDATORY WRITTEN ARTIFACT)

Create a plan file at `chapters/<book>/ch<NN>-plan.md`. Answer the 30 reasoning questions in your thinking first, then write the plan.

**Reasoning questions (answer in thinking):**

Story (5): What happens? What does the reader know that characters don't? What does each character know/feel NOW? What changes by the end? Which questions open/close?

Tone (4): What level? What register? What does it FEEL like? What's the emotional temperature?

Character (4): Whose POV? Their tics? Who else appears? What's the POV character feeling but NOT saying?

Pacing (4): Where in the arc? What tags? Cliffhanger type and build? Long or short?

Continuity (3): Micro-details from previous chapters? Echoes from other level? What am I planting?

Technical (2): Technology described? Correct terminology?

Anti-AI (2): What patterns to avoid? What sensory anchors?

World Pressure (2): 5+ checklist items by name. Where does the world press on characters?

Reader Architecture (4): What does the reader believe RIGHT NOW — both true and false? Which false belief am I reinforcing (good) or accidentally correcting (bad, too early)? What detail am I planting that pays off later? What will a re-reader notice in this chapter that a first-time reader will miss?

Bullshit Detector (2): For each scene — why does the character do this? Would a reader ask "but why?" If a scene has no clear character motivation, rewrite the beat. If something only makes sense because the worldbuilding doc says so (but the reader hasn't read that doc), it will confuse — add context or cut it.

**Then write the plan file:**

```markdown
# Ch. NN — [Title] — Plan

## Opening Type: [in medias res / dialogue / sensory / statement / time skip]
Previous chapter opened with: [type] — this MUST differ.

## Scene Breakdown (max 80 words per scene — use cross-refs for mechanisms)
- Scene 1: [beat] → action: [what happens physically], dialogue: [X exchanges between WHO], world: [checklist item] (~XXX words)
- Scene 2: ...
- Scene 3: ...

## Target Word Count: XXXX
## Chapter Type: normal (≥2500) | rapid cross-cut (≥800)

## Writing Checklist Items (5 minimum)
1. [item] — Scene X
2. ...

## Cross-Level Echo
[One specific detail from the OTHER level's most recent chapter that echoes here.
Must be subtle — a temperature, material, phrase, number. NOT explained.]

## Character Agency
What does the POV character CHOOSE that has CONSEQUENCES?
[If "nothing" — add a beat with stakes.]

## Dialogue Density
Target: ≥30% of word count.
Characters who speak: [list with # of exchanges]
[If zero dialogue: justify and compensate.]

## Reserve Scene
[One optional CHARACTER INTERACTION (not description) activated if chapter runs short.]

## Emotional Disruption
[One moment where a character's reaction is disproportionate, wrong, or surprising.]

## World Pressure Moment
[Where the world intrudes on a human moment.]

## Usage Targets
[Which character details or world elements will be SHOWN in this chapter?

Check `## Usage Tracker` tables in ALL loaded files — character files, world files, plot files.
Filter rows where Book AND Ch match THIS chapter. Those are the elements PRE-PLANNED for this
chapter — target ALL of them (they are `scene` or `accent` as specified in the Detail column).
If a `scene` item doesn't fit naturally, flag it — don't force it.

Example: "Noah's calluses noticed by Anyuk (fabia.md → B3 Ch.17, scene, planned),
XR as dominant entertainment (society.md → B1 Ch.01, accent, planned),
drone taxis texture (society.md → B1 Ch.01, accent, planned)."

After the chapter is written and verified, change Status from `planned` to `written`.
NEVER update status before the chapter is actually written in prose.]

## Reader Architecture
Reader's false beliefs at this point: [list what the reader thinks is true but isn't]
Reinforcing: [which false belief this chapter strengthens — or "N/A, no active misdirection"]
Planting: [detail that pays off in Ch. __ / Book __. If `plot/prestige-inventory.md` exists, check it]
Re-read reward: [one detail that means something different once the reader knows ___]
Foregrounded motif: [one primary motif for this chapter. If `plot/motif-tracking.md` exists, check it]

## Simultaneity Choreography (ONLY for [RAPID CROSS-CUT] or climax chapters — skip otherwise)
Causal chain: [Action in Level A → consequence in Level B → enables action in Level C]
Physical countdown indicator: [what the reader tracks across every cut — a number, temperature, sound, light]
Rhythm plan: [starting section length → peak compression → resolution expansion]
Elapsed story-time: [total real-time duration of the cross-cut sequence]
[If `plot/climax-choreography.md` exists, cross-reference the beat map for this chapter]

## Cliffhanger
Type: [QUESTION/THREAT/REVEAL/CUT/DREAD]
Build: [how the chapter escalates toward this ending]

## Ending Type
Type: [F action freeze / G dialogue cut / H arrival-departure / I body betrayal / J contemplative]
Contemplative endings used so far in this book: X/2
[If J and already at 2: choose a different type.]
```

**The plan MUST exist before writing. If it has < 3 scenes, target below 2500 (normal) / 800 (rapid), or zero dialogue with no justification: add more before proceeding.**

---

## Step 2.5: Pre-Drafting Anchor Checks (MANDATORY)

Before drafting a single sentence, scan the plan for elements that REQUIRE a worldbuilding anchor. The chapter writer MUST NOT invent fact-with-system-implications when a canonical anchor is missing — invented "flavor numbers" silently corrupt the worldbuilding and force expensive retrofits later. STOP rather than invent.

### 2.5.a — Level-aware economic-anchor pre-check (HARD `MUST`)

If the plan contains ANY of these triggers in a scene, the corresponding anchor file MUST be loaded and the scene's monetary detail MUST come from there:

**Trigger keywords** (match in plan beat descriptions):
`price`, `wage`, `cost`, `balance`, `salary`, `rent`, `fee`, `fine`, `tip`, `ration`, `memory credit`, `kilo+price pairing` (`<digit>/kg`, `per kilo`, `the kilo`), `monetary unit (€/euros/CBDC/GPU-HE) near digits`, `allocation request`, `compliance score gating`.

**Anchor file by level:**

| Level | Anchor file |
|---|---|
| Reality (L0) | `world/level-0-reality/economy.md` §Consumer Anchors (or `consumer-anchors.md` if split) |
| Ark (L1) | `world/level-1-ark/daily-life.md` §Economy |
| Dome (L2) | `world/level-2-dome/bureaucracy.md` §Allocation Mathematics + `context.md` §Economy and Distribution |
| Cross-level (memory credits) | `world/economy-cross-level.md` §Memory Credits — Canonical Definition |

**If no appropriate anchor exists,** STOP. Do not draft the scene. Announce: *"⛔ Pre-drafting anchor check failed: scene <name> requires monetary detail; no canonical anchor in <expected file>. Stopping. The user must add a worldbuilding-anchor milestone to the project's DEVPLAN before this chapter can be drafted."* Save the plan; exit.

### 2.5.b — Broader no-invent rule (system-implying details) (HARD `MUST`)

The same STOP rule applies to ANY fact that implies a system. Trigger keywords (in plan or expected prose):

`tier <digit>`, `score`, `Hz` near digits, `MHz` near digits, `% offer`, `% loyalty`, `compliance check at <time>`, `corridor 0\d\d`, `latency`, `bandwidth`, `LED <state>` with hardware-vintage capability claim, `firmware`, `handshake`, `signature` (sonic/digital), drone-altitude class, attestation tier, filtration alert tier.

For each match, verify a canonical worldbuilding file defines the system. If not, STOP and request a worldbuilding-anchor milestone. The writer MUST NOT pick a plausible-looking number to fill the gap.

### 2.5.c — Cross-substrate sensory echo check (MUST)

If the plan involves a sensory anchor (a number, a frequency, a specific object) that ALSO appears canonically at a DIFFERENT narrative level, verify whether the echo is intentional. Read `world/temporal-echoes.md` §Cross-Substrate Sensory Resonances (if present). If the echo is canonical, USE the canonical signature exactly. If the echo is not yet documented and the writer cannot determine intent, STOP and ask for a one-line decision in `world/temporal-echoes.md` before drafting. Examples to flag: any 440 Hz reference (already canonical in Ark per Phase 111 M3); any "Phrygian quarter-tone bent-third" signature; any object that recurred in another book's chapter.

### 2.5.d — Outline-deviation contract (MUST)

If the plan during Step 2 deviates from the chapter outline (cuts a scene, splits a scene across chapters, merges scenes, drops a planted detail), the writer MUST:

1. Update `chapters/<book>/outline.md` to reflect the new structure (move plant tags, update beat sections, mark moved beats with `[moved to chXX]` annotations).
2. Append a one-line entry to `chapters/<book>/outline-deviation.md` (CREATE if missing, append-only):
   ```
   Ch.NN (YYYY-MM-DD): <scene name> moved/cut/merged because <reason>. Plants shifted: <list, with new chapter destinations>. Open debt: <list of plants now without a planned chapter>. Context: -<file>, +<file>.
   ```
3. If any plant lost its planned chapter and has no new destination, FLAG this in the writer's announcement: *"⚠️ Plant orphaned: <plant>. Will be unassigned until reassigned in a future writer call."*
4. **Update the affected chapter's `**context:**` field** to keep beat↔context symmetry (per Step 2.6): remove files that lose their justifying beat after the cut/move (orphans per 2.6.b); add files newly required by the surviving or relocated beats (gaps per 2.6.a). If a beat moved to a different chapter, the source chapter loses the corresponding files and the destination chapter gains them — both `**context:**` fields update; both diffs go into the deviation entry's `Context:` field.

**Silent cuts are forbidden.** Step 7 (Outline Cleanup) verifies the contract was respected.

Announce upon completion of Step 2.5:
*"✅ Pre-drafting anchor checks passed. Proceeding to write."*

---

## Step 2.6: Pre-Drafting Context Symmetry Check (MANDATORY)

The chapter's `**context:**` list (in the outline) and its scene beats must stay symmetric: every file in `context:` must justify itself with at least one beat reference; every beat that needs a file must list that file. Drift in either direction is an invention surface (orphan = wasted context window; gap = the writer fills silence with plausible-but-uncanonicalized invention). This check runs after Step 2.5 and before Step 3.

### 2.6.a — Beat-side scan (missing files) (HARD `MUST`)

Parse the chapter outline beats up to the next chapter header. Extract:

- **Explicit references**: every `→ see <path>` and every bare `<path>` mentioned in beats.
- **Implicit references**: every named character (cross-ref `characters/**.md`); every named location (cross-ref `world/level-N-*/locations*.md` or `world/level-0-reality/architecture.md`); every named system, mechanism, or technical anchor (cross-ref `world/**.md`); every named ration unit, compliance score, anomaly code, frequency, or hardware artifact that traces to a canonical file.

Compare the union against the chapter's `**context:**` list, **minus** the always-loaded set declared in the outline header. Files referenced in beats but missing from `**context:**` → STOP. Output the list of missing files and request user confirmation to add (or auto-add if the writer call explicitly pre-authorized context-list edits).

### 2.6.b — Context-side scan (orphan candidates)

For every file in `**context:**` (excluding always-loaded), verify at least one beat reference exists per 2.6.a. Files with zero references → flag as "orphan candidate" in the pre-draft summary. NOT blocking — orphans are advisory, since some files may be load-bearing for consistency-only checks. The agent proposes one of:

- **Remove** (file adds no value to this chapter), OR
- **Promote to always-loaded** (file is universally needed across the book), OR
- **Keep + document** (file IS load-bearing for consistency, despite no explicit beat — agent must justify in the pre-draft summary).

User confirms before drafting proceeds. Drafting MAY proceed with documented orphans.

### 2.6.c — Post-draft audit

After Step 5 (Verify), the agent generates `chapters/<book>/ch<NN>-context-audit.md` (ephemeral; project should gitignore via `chapters/*/ch*-context-audit.md` pattern). For each file in `**context:**`, the audit maps the file to the beat / line-range where it was actually used in prose. The audit also lists any file used in prose but not in `**context:**` (drift). One-line summary at the top of the file:

```
context drift: -N file(s) planned-but-unused (<list>); +M file(s) used-but-unplanned (<list>).
```

Drift entries feed back into the symmetry check for the next chapter — used-but-unplanned files become candidates for next chapter's `**context:**`; planned-but-unused files become orphan candidates.

### 2.6.d — Always-loaded set awareness

Read the outline header's "Always-loaded reference" paragraph (typically lists `world/technology-comparison.md`, `world/temporal-echoes.md`, `world/tones.md`, plus trilogy-wide foreground character files and any book-specific promotions). Exclude every file in this paragraph from BOTH the missing (2.6.a) and orphan (2.6.b) checks. Always-loaded references are out of scope for per-chapter symmetry — they are loaded by default and need no per-chapter justification.

Announce upon completion of Step 2.6:
*"✅ Pre-drafting context symmetry check passed. Proceeding to write."*

---

## Step 3: Write the Chapter

Write to `chapters/<book>/ch<NN>.md`.

### Scene Construction (weights matter)

Every outline beat becomes a RENDERED SCENE. The components, in order of weight:

1. **ACTION + DIALOGUE — 60% of each scene.** Things happening. People talking. Bodies moving. Objects touched, opened, broken, shared. Dialogue is SPOKEN — actual words with pauses, interruptions, body language between lines. Not summary ("Anyuk explained"). Real words.

2. **POV INTERIOR — 20%.** The character's thought woven INTO the action. Not commentary after the action. Not "She recognized that..." but the thought arriving mid-gesture, fragmentary, unfinished. Thought as texture, not analysis.

3. **WORLD/SETTING — 15%.** 1-2 sentences to anchor in space. Then MOVE. The world emerges from the action — a hand touching a warm pipe tells us the temperature. A drone humming during a conversation tells us the surveillance. Don't describe the room and then put people in it. Put people in the room and let the room reveal itself through what they do.

4. **CLOSING DETAIL — 5%.** One image or fact that plants something for later.

### The 500-Word Rule

The inciting tension — what this chapter is ABOUT — must emerge within the first 500 words. If the first 500 words are pure setting with no tension, the chapter is mis-structured. Start with or near the tension. Let setting emerge from it.

### Prose Rules (from `world/prose-rules.md` — CRITICAL)

- **SHOW THEN MOVE ON.** After an image or action renders a beat, do NOT explain it. No "It was also the first time..." No "What she recognized was..." Cut every explanation sentence.
- **NO APHORISMS.** No fortune-cookie endings to paragraphs. No "Systems rewarded persistence."
- **NOT EVERYTHING MEANS SOMETHING.** 2-3 details per chapter that are just details. A stain, a loose thread, a sound unrelated to theme.
- **EMOTIONAL MESSINESS.** One moment per chapter where a reaction is disproportionate, wrong, or surprising. A character snaps at the wrong person, a classification system fails, someone says something they shouldn.t.
- **NARRATOR STAYS AT CHARACTER LEVEL.** No analyzing unconscious behavior with literary-critic vocabulary. Show the deviation. Let the reader name it.
- **30% DIALOGUE** when characters are present.
- **VARY OPENINGS.** Must differ from previous chapter (checked in plan).

### Other Rules

- Match the tonal register for this chapter's level (per `world/tones.md`)
- Match the POV character's voice (check `characters/notes/voice-samples.md`)
- Follow pacing rules and tags from the outline and `world/pacing-rules.md`
- End on the correct cliffhanger type (per outline and `plot/cliffhanger-map.md`)
- Target: 3000-4000 words normal, 800-1200 words [RAPID CROSS-CUT]
- Technology and world details must come from the project's worldbuilding files, not from generic genre conventions

---

## Step 3.5: Self-Edit Pass (MANDATORY — between writing and word count)

Before checking word count, re-read the chapter and apply these cuts:

1. **Em-dash glosses:** Count them. Max per POV character (check the character.s narrator boundaries in their character sheet). If over the limit, cut the weakest ones — replace with a period or restructure the sentence without the gloss.
2. **Explanation sentences:** Find every sentence that follows a strong image/action and explains what it meant. Delete it. Read the paragraph without it. If the meaning is clear, the sentence was redundant. Target: ZERO.
3. **"The way" count:** If >3 occurrences, rewrite at least half with different constructions ("like," "as," direct statement, or no simile).
4. **Tic captions:** Check the state file's Tic Introductions section. If any tic has been introduced in a previous chapter, REMOVE the explanation. Gesture only.
5. **Ending type:** Check the final paragraph. Is it a character standing/sitting still, processing? If yes, check the plan's ending type. If type J (contemplative) and 2 have already been used in this book, REWRITE the ending to use a different type (F, G, H, or I).
6. **Aphorisms in narration:** Find sentences that could appear on a book jacket without context. Cut or bury inside a longer thought. Max 1 in narration. Aphorisms in dialogue are acceptable ONLY if the character.s voice profile specifies they speak that way.
7. **Vocabulary check:** Read voice-samples.md Vocabulary Evolution section. Does the narration use words/constructions the POV character doesn't have access to at this chapter range? If yes, rewrite in the character's available register.
8. **Metaphor check (Rule 1 + Rule 9):** grep narration (not dialogue) for `like a`, `as if`, `as though`, `was a [abstract noun]`. Each hit is a potential metaphor. Rewrite as physical/concrete image (synecdoche, metonymy, precise detail, negative space). Target: **0** metaphors in narration. Dialogue metaphors permitted only if the character's voice-sample profile specifies (e.g., Mira in manifestos, Anyuk in proverbs).
9. **Adverbial dialogue tags (Rule 15):** count variant tags replacing `said`. EN: `muttered, whispered, exclaimed, retorted, gasped, snapped, hissed, breathed`. IT: `mormorò, sussurrò, esclamò, ribatté, ansimò, sibilò`. If the chapter's total variant-tag count is >2, rewrite the weakest half as action beats (e.g., `He set the mug down. "I know."`).
10. **Chapter opening check (Rule 21):** read the first 150 words. Must contain a concrete image + tension (question, wrongness, decision). If the first paragraph is summary, orientation, or stative verb (`Noah was X`, `It was Y`, `The Z did W as usual`), rewrite the opening into an in-medias-res image.
11. **Chapter closing check (Rule 22):** read the final paragraph. Must be ≤2 sentences and resolve as single image or single line. If it is a summary paragraph or contemplative wrap-up >2 sentences, cut to the most resonant single line. Never end with narrator-delivered significance.
12. **Transition phrases (Rule 13):** grep for banned transitions — `later that day, a few hours later, after that, eventually, meanwhile, più tardi, dopo, in seguito, frattanto, eventualmente`. Each hit = replace with white-space scene break + in-medias-res opening of the next scene.
13. **Object permanence (Rule 16):** verify at least one prior-introduced object is touched/used/noticed, OR at least one new plant-object is introduced for later. Check `plot/prestige-inventory.md` if it exists and `chapters/<book>/state.md` §Micro-details Planted. If neither, add one sentence of object interaction in the strongest scene.
14. **Silence beat (Rule 20):** if this chapter contains a dramatic peak (revelation, betrayal, death, crossing, body blow), verify at least one silent beat exists — a white-space break or a single short sentence isolated between longer paragraphs. If the peak chapter has no silent beat, insert one after the peak's physical moment.
15. **Forbidden interior-labeling formulas (HARD):** grep the narration (NOT dialogue) for these patterns. Each match is a candidate for cut or rewrite — express interior states through physical action, gesture, or sensory tightening, NOT through narrator labels of feeling-words.
    - `the closest thing to <emotion> [he|she|they] had had in (days|weeks|years|months)` — ALWAYS cut. The preceding image is doing the work; the chiosa betrays it.
    - `a kind of <abstract noun>` (e.g., "a kind of pleasure", "a kind of relief") — rewrite as the concrete physical correlate or cut.
    - `almost <verb>` / `almost felt like` — interior hedging. Rewrite as the gesture itself or its interruption.
    - `started to <verb>` ... `[before|and] stopped` (when used as interior gesture-labeling rather than exterior fact) — rewrite as the gesture or its bare interruption, no narrator commentary.
    - `<character> felt <X>` immediately followed by an explanation of what `<X>` is — collapse to the physical signal alone.
    Target: **0** matches in narration. Aphorism-style interior labels are forbidden regardless of the count cap in check #6 — that cap covers narrator wisdom; this check covers narrator emotion-labeling, a distinct failure mode.

---

## Step 4: Word Count Gate (HARD GATE)

```bash
wc -w chapters/<book>/ch<NN>.md
```

**Normal:** < 2,500 → INCOMPLETE. Do NOT verify. Expand by adding DIALOGUE SCENES AND CHARACTER INTERACTIONS, not description or interior narration. Activate the reserve scene from the plan. NEVER expand by adding environmental paragraphs or worldbuilding blocks.

**Rapid cross-cut:** < 800 → INCOMPLETE.

**Non-negotiable. An incomplete chapter cannot proceed.**

---

## Step 5: Verify (9 passes — MANDATORY)

**Run verification passes inline — do NOT launch a separate Agent.** All reference files are already in context from Step 1. An Agent would re-read them from scratch and double the token cost.

**Exception:** only launch an Agent if running in a context where Step 1 files have been cleared (e.g., a fresh session resumed mid-chapter). In that case, tell the agent explicitly which files are already loaded and which it must read. The agent MUST read:
- The chapter file (`chapters/<book>/ch<NN>.md`)
- The plan file (`chapters/<book>/ch<NN>-plan.md`)
- `world/technology-comparison.md` — for Pass 9 (level-identification check)
- `world/temporal-echoes.md` — ONLY if a temporal echo is noted in the plan file
- `characters/notes/voice-samples.md` — for Pass 2 and Pass 9 voice check

**Do NOT re-read** (already in context from Step 1): `tones.md`, `prose-rules.md`, `pacing-rules.md`, `writing-checklists.md`, `narrator-boundaries.md`, the POV character sheet, the outline entry, `cliffhanger-map.md`, `state.md`.

**Pass 1 — Plot:** Outline beats present? Cliffhanger correct? State contradictions?
**Pass 2 — Character:** Voice matches profile? Knowledge consistent? No forbidden knowledge?
**Pass 3 — World (writing-checklists.md):** ≥5 checklist items verifiable with line references? If <5 = FAIL.
**Pass 4 — Style:** Tone matches level? No cliches? No telling-not-showing?
**Pass 5 — Micro-details:** Tags respected? Chorus/poem seeds? Analog objects?
**Pass 6 — World Pressure (Reality only):** Analog alongside 2045 tech? Could be 2026 = FAIL.
**Pass 7 — Word Count & Scene Density:** ≥2500 (normal) / ≥800 (rapid)? Every beat a rendered scene? ≥3 dialogue exchanges if characters present?
**Pass 8 — Prose Discipline (prose-rules.md):** Check ALL of:
- Explanation sentences after powerful images? (**>0 = FAIL** — zero tolerance)
- Aphorisms in narration? (**>1 = FAIL** — aphorisms in dialogue OK if in-character)
- Em-dash glosses exceed POV character limit? (exceeds POV character.s max from their character sheet = **FAIL**)
- "The way" simile count >3? (If yes = **FAIL**)
- Tic caption on a previously-introduced tic? (If yes = **FAIL**)
- ≥30% dialogue when characters present? (If not = FAIL)
- ≥1 moment of emotional messiness? (If not = FAIL)
- Inciting tension within first 500 words? (If not = FAIL)
- Opening type differs from previous chapter? (If not = FAIL)
- ≥2 non-thematic details (things that are just things)? (If not = FAIL)
- Ending type J (contemplative) when 2 already used in book? (If yes = **FAIL**)
- Vocabulary outside POV character's chapter-range register? (If yes = **FAIL** — check voice-samples.md Vocabulary Evolution)
- **Metaphors in narration?** (**>0 = FAIL** — zero tolerance. Use synecdoche, metonymy, precise image, negative space. Rule 1 + Rule 9)
- **Variant dialogue tags (non-"said") count?** (**>2 = FAIL** — replace with action beats. Rule 15)
- **Chapter opening has concrete image + tension within first 150 words?** (If not = **FAIL**. Rule 21 — stricter than the 500-word inciting-tension rule)
- **Chapter closing is ≤2-sentence image or single line?** (Summary paragraph or contemplative wrap-up >2 sentences = **FAIL**. Rule 22)
- **Banned transition phrases present?** (`later that day / a few hours later / after that / eventually / meanwhile / più tardi / dopo / in seguito / frattanto / eventualmente`. **>0 = FAIL** — use white-space scene break + in-medias-res. Rule 13)
- **Object permanence:** prior-introduced object touched/used/noticed OR new plant-object introduced? (Neither present = **NOTE** — consider adding in revision. Rule 16)
- **Silence beat after dramatic peak?** (Peak chapter with zero silent beats = **FAIL**. Rule 20)
- **Dialogue from desire, not information?** (Any "as you know" construction OR character-A-tells-character-B what both already know = **FAIL**. Rule 14)
- **Sentence length progression in climax chapter?** (If this is a climax chapter and avg sentence length does not decrease ≥30% from opening to closing = **FAIL**. Rule 18)
- **Echo, not repetition:** any motif phrase returning from a prior chapter carries semantic shift? (If identical semantic meaning on return = **FAIL**. Rule 19)
- **Reader plant (dramatic irony):** at least one detail the POV character notices but does not process, that the reader can? (If none = **NOTE** — add in revision if feasible. Rule 23)
- **Consequence, not explanation:** any narrator paragraph explaining HOW a mechanism works (not the character discovering it through action)? (If yes = **FAIL** — move to diegetic artifact or cut. Rule 24)

**Pass 9 — Reader Perspective (MANDATORY — added Phase 25):** The agent answers these questions as a reader who has NOT read the worldbuilding docs:
- "Does this chapter make sense to someone who only knows what previous chapters established?" (If not = FAIL — identify what's confusing)
- "Is any section boring? Where would a reader skip ahead?" (If yes = FAIL — identify the drag and propose a cut or replacement with dialogue/action)
- "Does the reader want to read the next chapter?" (If not = FAIL — the cliffhanger or tension isn't working)
- "Does anything not make logical sense? Would a reader ask 'but why?'" (If yes = FAIL — the bullshit detector caught something)
- "Are the character's emotions visible in their BODY, not just narrated?" (If not = FAIL — show the implant fight, the tremor, the jaw lock, the sweat)
- "Can the reader tell which level (the project.s narrative levels) they're in from any random paragraph, without character names?" (If not = FAIL — technology/sound/light fingerprint is missing. Check `world/technology-comparison.md`)
- "Is the reader's attention being directed correctly — toward the mystery, away from unrevealed information?" (If a detail accidentally reveals something the reader shouldn't know yet = FAIL)
- "Is there at least one detail that will mean something different on re-read?" (If not, consider adding one — this is what separates good from great)
- "Does this chapter maintain or reinforce any false belief the reader currently holds?" (Check the plan's Reader Architecture section — if the chapter accidentally corrects a false belief too early = FAIL)

**Pass 10 — Simultaneity & Spectacle (ONLY for [RAPID CROSS-CUT] or climax chapters — skip otherwise):**
- "Does each cross-cut section end with an action that the NEXT section (different level) visibly responds to?" (If cuts are parallel but not causal = FAIL — they're juxtaposition, not choreography)
- "Is the physical countdown indicator present in every cross-cut section?" (If the reader loses track of the ticking clock = FAIL)
- "Does the prose rhythm accelerate as the sequence progresses?" (If section lengths stay uniform = FAIL — compression creates urgency)
- "Can the reader reconstruct the causal chain? (A triggered B which enabled C)" (If the chain is unclear = FAIL)

If any pass fails: revise and re-check. Max 2 revision cycles.

---

## Step 5.5: Update Usage Trackers (MANDATORY)

Open every file loaded in Step 1 that has a `## Usage Tracker` section.

For each tracker item matching THIS chapter (same Book and Ch) that was SHOWN in the draft prose, change Status from `planned` to `written`. If an item didn't make it into the draft, leave it as `planned`. Do NOT change items in other chapters' rows.

**Rules:**
- NEVER update status for items not rendered in prose — the detail must be visible in the chapter text.
- Status reflects what's actually in the draft, not what was planned.

---

## Step 6: Update State (MANDATORY)

Update `chapters/<book>/state.md`:

```markdown
## After Chapter N

### Character Positions
- [Character]: [where, what they know, emotional state]

### Plot Progress
- [What changed]

### Open Threads
- [Questions opened/still open]

### Ticking Clocks
- [Countdown statuses]

### Micro-details Planted
- [Chorus, poem, dread, objects, echoes]

### Tic Introductions (caption-free after first use)
- [Tic]: INTRODUCED Ch. N — no further caption
- [Tic]: INTRODUCED Ch. N — no further caption
[Update this section each time a tic appears with its full explanation for the first time.
In subsequent chapters, the chapter-writer reads this section and does NOT explain any tic
that has already been introduced. The gesture appears alone, without gloss or em-dash caption.]

### Ending Types Used
- [list ending types used so far: F(count), G(count), H(count), I(count), J(count/2 max)]
```

**If state is not updated, the chapter is NOT complete.**

---

## Step 7: Outline Cleanup (MANDATORY — prevents bloat accumulation)

After writing and verifying the chapter, clean up this chapter's entry in the outline:

1. **Remove struck-through items** in this chapter's outline section. They were decisions — now resolved.
2. **Extract `⚠️` blocks** to `chapters/<book>/writing-notes.md`. Replace with one-line cross-ref: `→ See writing-notes.md §ChNN-[topic]`.
3. **Replace inline mechanism re-explanations** with cross-refs to the canonical source. If this chapter re-explains the Alignment Window, PLC channel, or any mechanism already documented in `world/`, replace with: `→ See [file] §[section]`.
4. **Compress beat descriptions** — no single beat over 100 words. Replace authorial reasoning ("the reader should feel...", "on reread...") with one-line directives or move to writing-notes.md.
5. **Remove process wrappers** — delete "Note:", "MANDATORY:", "drafting note:", "author note:" prefixes from corrected content. The outline should read as if the content was always there.

6. **Consolidate cross-references** — if this chapter's outline entry has ≥3 `→ See` references, collect them into a single `**Refs:**` line at the end of the chapter entry.
7. **Density check** — run `wc -w` on this chapter's outline entry (header to next header). If >250 words (normal) or >100 words (rapid): compress further.

8. **Outline-deviation contract verification** — verify Step 2.5.d was respected:
   - Compare the chapter draft against the original outline entry: every scene from the outline must be either present in the draft, OR documented as moved/cut in `chapters/<book>/outline-deviation.md`.
   - If a scene is missing from the draft AND has no entry in `outline-deviation.md`: this is a SILENT CUT — write the contract entry now, retroactively, and announce the violation: *"⚠️ Silent cut detected: <scene>. Documenting retroactively in outline-deviation.md."* Then list any plant orphaned by the cut so the next writer call can pick it up.
   - If `outline-deviation.md` does not exist and no deviations occurred, do not create the file (it is append-only and only exists when there is a deviation to log).

This step is incremental — 2 minutes per chapter. Skipping it causes the outline to grow ~200 words per chapter of dead weight, and silent cuts to accumulate undetected.

---

## Step 8: Mark Complete

Update `chapters/<book>/DEVPLAN.md`:
```
- [x] Ch. NN — Title (Level / POV) ✅
```

Announce: *"✅ Ch. N complete — [title] — [word count] words — [level]/[POV] — Cliffhanger: [type]"*

---

## Rules

- ❌ Never skip the plan file (Step 2)
- ❌ Never skip the word count gate (Step 4)
- ❌ Never skip verification (Step 5)
- ❌ Never skip state update (Step 6)
- ❌ Never mark complete without ALL gates passed
- ❌ Never explain what a scene just showed
- ❌ Never end a paragraph with an aphorism
- ❌ Never let the narrator be smarter than the character
- ❌ Never spend >500 words on setting before the tension arrives
- ❌ Never break the tonal register
- ❌ Never let a character know something they shouldn't
- ✅ Show, then move on
- ✅ 60% action+dialogue, 20% POV, 15% world, 5% closing
- ✅ Emotional messiness over calibrated understatement
- ✅ Physical sensations over abstract descriptions
- ✅ The reader should always have 2-3 open questions
