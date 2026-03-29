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
- `chapters/<book>/outline.md` — find the specific chapter entry with all beats, tags, notes
- `chapters/<book>/state.md` — the ENTIRE most recent "After Chapter N" section
- `world/tones.md` — tonal register for this chapter's level
- `world/pacing-rules.md` — pacing and tension rules
- `world/writing-checklists.md` — sensory enforcement (read the section for this chapter's level)
- `world/prose-rules.md` — prose quality rules (CRITICAL — read every time)
- `characters/notes/voice-samples.md` — voice profiles
- `characters/notes/narrator-boundaries.md` — POV narrator rules (em-dash limits, vocabulary restrictions, metaphor register)
- `plot/cliffhanger-map.md` — cliffhanger type for this chapter

**Load based on level:**
Identify this chapter's narrative level from the outline. Then load ALL context/technology files in the corresponding `world/level-*-<name>/` directory. Also load `world/technology-comparison.md` (or equivalent) to ensure this level's tech fingerprint is correct and distinct from other levels.

**Load based on POV character:**
- The POV character's sheet from `characters/foreground/` or `characters/midground/`
- Sheets for other characters appearing in this chapter

**Load from `context:` tag (MANDATORY):**
Read the `context:` field from this chapter's header in the outline. Load every file listed there in addition to the always-loaded set. These are the conditional context files for this chapter — determined during outline planning, not at the writer's discretion. If a file in the context tag does not exist, stop and report.

Also load any `plot/` files explicitly referenced in the chapter's scene beats (e.g., mythology fragments) that are not already in the `context:` tag.

Announce: *"📖 Ch. N: [title] — [Level] / [POV] / [Tone] / Cliffhanger: [type]"*

---

## Step 2: Plan (MANDATORY WRITTEN ARTIFACT)

Create a plan file at `chapters/<book>/ch<NN>-plan.md`. Answer the 26 reasoning questions in your thinking first, then write the plan.

**Reasoning questions (answer in thinking):**

Story (5): What happens? What does the reader know that characters don't? What does each character know/feel NOW? What changes by the end? Which questions open/close?

Tone (4): What level? What register? What does it FEEL like? What's the emotional temperature?

Character (4): Whose POV? Their tics? Who else appears? What's the POV character feeling but NOT saying?

Pacing (4): Where in the arc? What tags? Cliffhanger type and build? Long or short?

Continuity (3): Micro-details from previous chapters? Echoes from other level? What am I planting?

Technical (2): Technology described? Correct terminology?

Anti-AI (2): What patterns to avoid? What sensory anchors?

World Pressure (2): 5+ checklist items by name. Where does the world press on characters?

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
[Which character details or world elements will be SHOWN for the FIRST TIME in this chapter?
Check the `## Usage Tracker` section in ALL loaded files — character files AND context-tagged
world/plot files. Every file with a Usage Tracker is fair game.
Pick 2-3 unchecked items to target. Example: "Noah's calluses noticed by Anyuk (first time),
Anyuk's glasses described, moka pot ritual shown, temporal echo Ch.10→Ch.11 door."
After the chapter is written and verified, mark targeted items `[x]` with the Book/Chapter reference.
NEVER mark `[x]` before the chapter is actually written in prose.]

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

Launch an Agent. **If you skip verification, the chapter is NOT complete.**

The agent reads the chapter, the plan file, and relevant reference files. **The agent MUST also read:**
- `world/technology-comparison.md` — for Pass 9 (level-identification check)
- `world/temporal-echoes.md` — if a temporal echo is noted in the plan file
- `characters/notes/voice-samples.md` — for Pass 2 and Pass 9 voice check

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

**Pass 9 — Reader Perspective (MANDATORY — added Phase 25):** The agent answers these questions as a reader who has NOT read the worldbuilding docs:
- "Does this chapter make sense to someone who only knows what previous chapters established?" (If not = FAIL — identify what's confusing)
- "Is any section boring? Where would a reader skip ahead?" (If yes = FAIL — identify the drag and propose a cut or replacement with dialogue/action)
- "Does the reader want to read the next chapter?" (If not = FAIL — the cliffhanger or tension isn't working)
- "Does anything not make logical sense? Would a reader ask 'but why?'" (If yes = FAIL — the bullshit detector caught something)
- "Are the character's emotions visible in their BODY, not just narrated?" (If not = FAIL — show the implant fight, the tremor, the jaw lock, the sweat)
- "Can the reader tell which level (the project.s narrative levels) they're in from any random paragraph, without character names?" (If not = FAIL — technology/sound/light fingerprint is missing. Check `world/technology-comparison.md`)

If any pass fails: revise and re-check. Max 2 revision cycles.

---

## Step 5.5: Update Usage Trackers (MANDATORY)

Open every file loaded in Step 1 that has a `## Usage Tracker` section (character files + context-tagged world/plot files). For each item that was SHOWN in the draft prose, mark `[x]` with the Book and Chapter reference. Example: `- [x] Temporal echo Ch.10→Ch.11 door (Book 1, Ch. 11)`.

**Rules:**
- NEVER mark `[x]` for items not rendered in prose — the detail must be visible in the chapter text.
- If you targeted an item in the plan (Step 2, Usage Targets) but it didn't make it into the draft, leave it `[ ]`.
- Character trackers AND context-file trackers follow the same process — no exceptions.

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

This step is incremental — 2 minutes per chapter. Skipping it causes the outline to grow ~200 words per chapter of dead weight.

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
