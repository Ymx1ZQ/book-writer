# Book Coherence Check

Run a comprehensive coherence review across the project's worldbuilding, characters, and outlines. Combines the "reader who asks obvious questions" with the rigor of a professional script doctor. Genre, tone, and structural rules are read from the project's own files — this instruction is genre-agnostic.

## Invocation

```
/book coherence [scope]
```

Scope options:
- `all` — full project review (default)
- `book-1` — Book 1 outline + relevant worldbuilding/characters
- `book-2` — Book 2
- `book-3` — Book 3
- `characters` — character files only
- `world` — worldbuilding files only

---

## Process

### 1. Load Files

Read ALL files in the specified scope:
- `world/` — all context, technology, comparison, temporal-echoes files
- `characters/foreground/` — all foreground character sheets
- `characters/midground/` — all midground sheets
- `characters/notes/` — voice samples, flashback beats
- `plot/` — all episode files, key-scenes, cliffhanger-map, chorus-poem-map, sauveterre-plant
- `chapters/book-N/outline.md` — the relevant outline(s)
- `chapters/book-N/opening-strategy.md` — if it exists

### 2. Check Categories (10 checks)

For every issue found: **cite the specific file and section**, and **propose a practical fix**.

---

#### A. Cross-Level Architecture
Analyze the relationship between the project.s narrative levels (read from `world/overview.md`). This is a multi-level narrative, not a multi-timeline one — but the same rules apply:
- Do actions in one level have **logical, consistent consequences** in the connected levels?
- If the project uses cross-level echoes or causal links, check that actions in one level produce consistent effects in connected levels. Is the echo specific enough for the reader to notice?
- 
- 
- Flag any **causal weakness or paradox** in the cross-level links.

#### B. Plot Holes & Deus Ex Machina
- Identify narrative threads left dangling (introduced and never resolved).
- Flag conflicts resolved too conveniently — characters rescued by coincidence, problems solved by information that appears from nowhere, technology that works exactly when needed and fails exactly when dramatic.
- Flag any event that happens **without justification** within the rules of the world.
- Check the resolution of each book's climax: is it earned, or does it rely on contrivance?

#### C. Causal Flow & Knowledge Consistency
- For each major plot beat: trace the cause-and-effect chain backward. Does it hold?
- Flag scenes where characters **know things they shouldn't yet know**. Cross-reference what each character has learned in previous chapters.
- Flag **logical jumps** — moments where the narrative skips from A to C without establishing B.
- Pay special attention to cross-level knowledge: does a character in one level know something that only a reader of another level.s chapters would know?

#### D. Character Consistency
- For each protagonist's major decision: is it consistent with their established personality, background, and trauma?
- Flag any character who acts **"out of character" to serve the plot** — they do something only because the story needs them to, not because they would.
- Check character arcs: does each protagonist change in a way that follows from what happened to them? Is the change gradual or abrupt?
- Verify the naming convention: Check that character naming conventions match the rules defined in their character sheets.

#### E. Worldbuilding & Technology Consistency
Using `world/technology-comparison.md` as primary reference:
- Does technology respect the established rules per level? (Check the project's `world/technology-comparison.md` or equivalent for the specific rules.)
- Is there a **coherent evolution** between levels? (Reality 2045 → Dome sim of 2095 → Ark sim of orbital station)
- Flag technology that appears or disappears conveniently ("they hack the terminal" — do they have the skills/tools established for this?).
- Flag any confusion between levels: a Dome chapter that describes Reality-style drones, or an Ark chapter with Dome-style silent surveillance.
- Are technology aesthetics maintained consistently per level?

#### F. Pacing & Cross-Level Balance
- Does the alternation between levels maintain tension, or does switching break momentum?
- Do transitions happen at the right moments (cliffhangers, not mid-scene)?
- **Is one level visibly weaker or more boring than the others?** If so, identify which and why.
- Check chapter length variation: do crisis sections use shorter chapters? Does the pacing arc match what `world/pacing-rules.md` prescribes?
- Verify the [RAPID CROSS-CUT] sections: are they genuinely rapid (2-3 pages), and does the cross-cutting create urgency?

#### G. Infodump Detection
- Flag any passage where worldbuilding or technology is explained in a **block of exposition** rather than through action, dialogue, or sensory experience.
- Flag any dialogue that is really **exposition wearing quotation marks** ("As you know, the Algorithm monitors all Blue-tier workers...").
- Check the first 3 chapters especially: do they show the world through the character's experience, or do they stop to explain it?
- The rule: if removing a paragraph of description doesn't break the scene's action, the paragraph is probably an infodump.

#### H. Thematic Resonance
- Do all three levels explore the **central themes** consistently? (the project's central themes (read from `world/overview.md` or `CLAUDE.md`))
- Is the **emotional stake** clear in each level? (Read the project's theme/stakes from world files.
- Do the levels **comment on each other thematically**? (Check that levels comment on each other thematically — testing the same question from different angles.
- Flag any level or arc that feels **thematically disconnected** from the others.

#### I. Reader Experience & Investment
- "Is this boring?" — Flag sections that are mostly exposition without action/tension.
- "Does the reader have a reason to care about this character?" — Flag characters who appear without emotional setup.
- "Would a reader continue reading after this chapter?" — Check every chapter ending for forward momentum.
- "Does this make sense to someone who HASN'T read the worldbuilding docs?" — The docs don't ship with the book.
- "Where would a reader on a train put the book down?" — Flag those moments.

#### J. Chekhov's Inventory
A complete inventory of introduced elements and their payoff status:
- **Plants:** Things introduced early that pay off later (E. Sauveterre, the five notes, the notebook, specific character details). Is every plant paid off? Is any payoff missing its plant?
- **Promises:** Things the narrative promises to the reader (a mystery, a threat, a character's growth). Is every promise kept?
- **Orphans:** Things introduced and abandoned — characters, objects, questions, subplots.
- **Retroactive plants:** Things that appear in Book 2-3 that SHOULD have been planted in Book 1 but weren't.

### 3. Output — Report to User

Display issues to the user in order of severity:

```
## BLOCKING (must fix before writing)
- [issue description] — [file:line or file1 vs file2]. **Fix:** [practical solution]

## WARNING (should fix, could cause reader confusion)
- [issue description] — [file:line]. **Fix:** [practical solution]

## NOTE (minor, fix when convenient)
- [issue description] — [file:line]. **Fix:** [practical solution]
```

### 4. Write the Corrections Devplan (MANDATORY)

**This is the critical step.** The report is analysis; the devplan is the actionable output. Without this step, findings are lost.

Create or append to `DEVPLAN.md` a new Phase with milestones for every fix. The Phase is named `Phase NN — Coherence Fixes ([scope])`.

**Format:**

```markdown
## Phase NN — Coherence Fixes ([scope], [date])

Coherence check found X blocking / X warning / X note issues.
Fixes ordered by severity, then by file.

### M[next]: [Fix title — BLOCKING]

**File:** `[path]` (REVISIONE)

- [ ] [Specific fix instruction with enough context to execute without re-reading the report]
- [ ] [Second fix if the milestone touches the same file]

### M[next+1]: [Fix title — BLOCKING]
...

### M[next+N]: [Fix title — WARNING]
...

### M[next+N+M]: [Fix title — NOTE]
...
```

**Rules for the corrections devplan:**
- Every BLOCKING and WARNING issue MUST become a milestone. NOTEs are optional (include if the fix is quick).
- Group fixes by file when possible — one milestone per file, not one per issue.
- Each milestone's checkbox must contain enough context to execute the fix WITHOUT re-reading the full report.
- Include the file path, the section to modify, and the specific change to make.
- The devplan is appended to the existing `DEVPLAN.md`, never overwriting previous phases.
- After writing, announce: *"Coherence devplan written: X milestones. Run `/book fix <book>` to apply fixes."*

### 5. Summary

```
Book Coherence Check Complete
Scope: [scope]
Files reviewed: X
Issues found: X blocking / X warning / X note
Devplan milestones created: X

Strongest level: [which level has the fewest issues]
Weakest level: [which level needs the most work]
Most common issue type: [A-J category]

Next step: /book fix <book> to apply all fixes.
```

---

## Rules

- ❌ Never assume the reader has read the worldbuilding docs
- ❌ Never let "the outline says so" be sufficient — if it doesn't make sense to a reader, it doesn't work
- ❌ Never soften the assessment. This is script-doctor mode. Be spietato.
- ❌ Never skip Step 4 (the corrections devplan). The report without a devplan is useless — findings evaporate.
- ✅ For every problem, propose a PRACTICAL narrative fix — not just "this is wrong"
- ✅ Flag everything that makes you go "hmm" — better to over-flag than miss something
- ✅ Cross-reference aggressively — contradictions between files are the most common issue
- ✅ Think like a reader on a train, not like a project manager
- ✅ Cite specific passages/sections, not vague references
- ✅ The devplan is the REAL output. The report is context for the devplan.
