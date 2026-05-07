# `/book sniff` — adversarial skeptical-reader pass

Run an informed-but-skeptical reader over the latest chapter draft. Catch what coherence-check, reviewer, and proofreader will NOT catch: the things that make a real reader stop and call BS.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Internal consistency of the book against its own canon | `coherence-check.md` |
| Craft (voice, pacing, structure, scene shaping) | `reviewer.md` |
| Surface (grammar, syntax, punctuation, line-level) | `proof-reader.md` |
| **"Would a reader call BS on this?"** | **THIS check** |

Sniff is the **plausibility / nose-wrinkle** layer. It assumes the reader is informed, skeptical, and not romantic about the work. It catches the patterns a writer agent typically falls into when worldbuilding is silent: filling gaps with plausible-but-uncanonicalized invention, modern unconscious bias, technobabble without referent, unearned capabilities, convenient coincidences.

**Milestone format:** see `instructions/milestone-format.md` — checkboxes only for pipeline-executable items. ANCHOR-NEEDED milestones written to `DEVPLAN.md` are executable by `/book fix`, so they correctly use `- [ ]`.

## Usage

```
/book sniff <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`).
- `chNN` — optional. If provided, scans only that chapter. If omitted, scans the most recently written chapter for that book.

## Output

Writes `chapters/<book>/SMELL.md` with one entry per objection.

## Reader persona for the executing agent

You are a well-read, skeptical, informed reader. You are not romantic about this book. You read fast, you notice friction, you know how the world works (economics, technology, biology, sociology, geography). When something doesn't track, you stop. You err toward MORE objections, not fewer — false positives are cheap (the user dismisses them), false negatives let bad prose ship.

You are NOT the writer. You do not justify, soften, or rationalize. You report friction.

## The nine objection categories

For every concrete assertion in the chapter (a number, a fact, an object, a capability, a behavior, a coincidence), check it against all nine categories. Most lines will pass. The lines that fail are the chapter's smell.

1. **Anachronism.** The chapter is set at a specific date in the project's timeline (read `world/timeline.md` for the year + macro context). Does the assertion track with the elapsed years of climate / technology / society / economy / language evolution from the present-day baseline (2024)? A 2045 scene with 2024-era prices, 2024-era hardware availability, 2024-era social assumptions, 2024-era technology defaults is the most common failure.

2. **Worldbuilding-canon contradiction.** Does the assertion contradict an explicit fact in `world/`, `characters/`, or `plot/`? Read the relevant level files (Reality → `world/level-0-reality/`; Ark → `world/level-1-ark/`; Dome → `world/level-2-dome/`) and the cross-substrate files (`world/temporal-echoes.md`, `world/the-authors-method.md`). If the chapter says X and a canonical file says NOT-X, that is BLOCKING-grade unless ACCEPT can be argued.

3. **Technobabble without referent.** A specific number ("0.3", "tier two", "corridor 042", "440 Hz") or specific term ("filtration alert", "compliance check at 06:48") implies a system. Does that system exist in canon? If the writer agent invented the number/term to flavor the prose, the reader feels the vapor. Either canonicalize the system (ANCHOR-NEEDED) or remove the false specificity (INLINE).

4. **Unearned capability or knowledge.** Does a character, agent, object, or institution know or do something that has not been previously established? "The agent knew where they were and that was the deal" — what deal? Whose? Earned by what? "The Game printed: YOUR MOTHER MADE COUSCOUS LAST WEEK" — by what mechanism does the Game know this? If the chapter expects the reader to accept the capability without setup, the reader smells convenience.

5. **Domain plausibility.** Read each assertion as if the reader has expert knowledge in the relevant domain — economist, engineer, doctor, person with the relevant disability, native of the city/region, professional in the depicted field. Would they call BS? "Two euros the kilo" for fresh sardines in a 2045 climate-stressed Mediterranean = an economist calls BS. A wheelchair maneuver that cannot physically be done with the chair geometry described = a wheelchair user calls BS. A surgical detail wrong by current medical practice = a doctor calls BS.

   **5.a — Real-world factual-claim audit (operational sub-rubric).** The expert-reader framing above is the lens; this sub-rubric is the procedure. For every concrete assertion in the chapter that depends on knowledge **external to the project's canon files**, classify into one of three buckets:

   - **Anchored in canon** — the assertion is supported by a canonical project file (e.g., `world/`, `characters/`, `plot/`, `consumer-anchors.md`). Cite the file. Pass.
   - **Real-world verifiable, high confidence** — the assertion is a fact about the real world (geography, physics, language grammar, etc.) that the agent can confirm with high confidence. Declare it. Pass.
   - **Cannot verify / makes friction** — neither anchored nor confidently real. Flag. Classification: INLINE if a prose tweak fixes it, ANCHOR-NEEDED if the project should canonicalize an in-world override, ACCEPT only with explicit outline evidence per the standard rule.

   Categories the agent must scan, generic across the trilogy:

   - **Real-world places** — streets, neighborhoods, landmarks, country/city facts, geography, climate. A real city named in the prose (Marseille, Torino, Bruxelles) inherits the real geography of that city; relative positions of named places must match the real map unless the project canonicalizes an override.
   - **Specific technology** — model numbers, connector types, version numbers, hardware compatibility, software stacks, physical chains (source→display, etc.). Period plausibility: does it exist at the implied year? was it in actual use at that year? is the chain of compatibility physically realizable in the implied direction?
   - **Foreign-language grammar in proper nouns** — when the text names a French / Italian / Spanish / etc. proper noun, source-language grammar applies (article-preposition contractions, gender agreement, accents). Capitalization in in-world terminal output does not exempt the noun from its source-language grammar.
   - **Real physics, biology, medicine, law, finance** — assertions in these domains are checkable against domain knowledge.
   - **Real brand names, dates, currencies, units** — real things named in the prose must be real.

   **Calibration (load-bearing).** Specific-sounding details fail at higher rates than their tone suggests. A writer agent producing "model VGA-to-HDMI converter cable" or "Rue de Petit Puits, Le Panier" is not stating a verified fact — it is selecting a plausible-sounding token to add texture. Sniff must treat highly-specific technical or geographic assertions with **more** suspicion than general descriptive ones, because the failure mode is *plausibly worded → plausibly wrong*. Err toward flagging when the specificity exceeds the agent's actual confidence.

   The prevention layer is `chapter-writer.md` §3.5 #16 (the writer's self-edit "External-world claim discipline" check). Sniff §5.a is the post-draft safety net. The continuity-within-chapter check is §9 (props/geometry consistency *inside* the scene), distinct from §5.a (claims about the *external* world).

6. **Physical implausibility.** Geometry, physics, biology of described actions. Does the room dimension allow the movement described? Does the elapsed time match the action volume? Does the body do what the prose says it does (cold travels up the bones; can hands feel cold "stop where the calluses started"? — physiologically, no — but it can be a metaphor signaled as such)?

7. **Character behavior.** Read the character's sheet in `characters/foreground/` or `characters/midground/`. Does the behavior in the scene match the established voice, defaults, history, relationships? A character described as withholding who suddenly delivers a soliloquy about themes is a smell.

8. **Plot armor / convenience.** Does an event resolve too easily? Does information appear exactly when needed? Does a chance encounter feel engineered? "The number's been disconnected since 2031" — convenient confirmation; is the chain of inference signposted, or did the reader leap with the writer's hand?

9. **Continuity within the chapter.** Timeline, geography, props consistent across the chapter itself. The moka pot is on the gas flame in line 3 → does it move plausibly to "three feet to my left" by line 178? The chair "slides back two inches" in line 117 → is the writer tracking that the chair is now two inches back for the rest of the scene, or did it teleport? An object placed in pocket should re-emerge from pocket, not from hand, without transition.

## Output format — `SMELL.md`

Header section:

```markdown
# SMELL.md — Chapter <id>, drafted <date>, sniffed <date>

Total objections: N
- INLINE: X (revisable in prose)
- ANCHOR-NEEDED: Y (worldbuilding gap; surface to project DEVPLAN)
- ACCEPT: Z (deliberate; signoff)
```

Then one entry per objection, in chapter order:

```markdown
## #N — <one-line summary>

- **Location:** ch01.md line 49 (or scene reference if no line numbers)
- **Quote:** "Two euros the kilo. Came in at five."
- **Category:** 5 — Domain plausibility (economic) + 1 — Anachronism
- **What the reader thinks:** Sardines at €2/kg in 2045 Marseille after 21 years of compound inflation and climate-driven scarcity? Today's price is €4–10/kg. Even ignoring scarcity, generic CPI alone makes €2 nonsense. The reader stops here.
- **Classification:** INLINE
- **Suggested action:** Replace with anchored value. Per the project's economic anchors (or the canon being built in `world/level-0-reality/economy.md §Consumer Anchors`), real-catch sardines on a fresh-landing day are scarcity-premium goods. Plausible Sélim line: "Twenty-five the half-kilo. Came in this morning, won't last past noon." Trade dialogue rhythm preserved; price now signals scarcity instead of contradicting it.
```

For ANCHOR-NEEDED entries, include a sub-block:

```markdown
- **Classification:** ANCHOR-NEEDED
- **Anchor required in:** `world/level-0-reality/ecology.md` (new sub-section §Filtration Alert Tiers)
- **What the section must define:** Tier 1–N scale, per-tier trigger threshold, per-tier behavioral mandate, per-tier exemptions, broadcast channel.
- **Suggested project DEVPLAN milestone language:**
  > **M-N: Filtration alert tier system → `world/level-0-reality/ecology.md` §Air Quality (NEW sub-section).** Define tiers 1–4: trigger thresholds, behavioral mandates, exemptions, broadcast channels. Anchor against `timeline.md` climate-stress trajectory.
```

For ACCEPT entries, the writer agent must show evidence in the outline or world files that the choice is deliberate:

```markdown
- **Classification:** ACCEPT
- **Evidence:** `chapters/book-1/outline.md` Ch.01 §3 explicitly tags this as "deliberate dis-anchor — character's moment of disconnect from the procedural world; signaled by the prose register shift (italics + non-justified line)."
- **Action:** none.
```

## Steps for the executing agent

1. Resolve the chapter file: if `chNN` provided, read `chapters/<book>/<ch>.md`; else find the most recently modified `chapters/<book>/ch*.md`.
2. Load the project context for the level the chapter is set in (read CLAUDE.md to find the level mapping; for a Reality scene, load `world/level-0-reality/*.md` and the relevant character sheets).
3. Load `world/timeline.md` to know the year and macro context.
4. Load `world/canon-hierarchy.md` — the resolution doctrine. Use it when classifying ANCHOR-NEEDED entries to decide which file should change and what the canonical value should be.
5. Read the chapter line by line. For every concrete assertion, run the nine categories. Aggregate findings.
6. Classify each finding (INLINE / ANCHOR-NEEDED / ACCEPT) using the heuristics above.
7. Write `chapters/<book>/SMELL.md` with the format above.
8. **For every ANCHOR-NEEDED entry, also append a fix milestone to `DEVPLAN.md`.** Open `DEVPLAN.md`, scan for the highest existing `## Phase NN —` heading, and append a new phase named `## Phase <NN+1> — Sniff anchor fixes (<book> <chNN>) (<date>)`. Under that phase, write one milestone per ANCHOR-NEEDED entry, using the format below. Reuse the entry's existing "Suggested project DEVPLAN milestone language" content as the milestone body, augmented with the canon-hierarchy resolution rationale.
9. Print: `wrote SMELL.md — N objections (X INLINE, Y ANCHOR-NEEDED, Z ACCEPT). Wrote Phase <NN+1> to DEVPLAN.md with Y anchor-fix milestone(s).`

## DEVPLAN milestone format (for ANCHOR-NEEDED entries)

```markdown
### M<n>: <one-line title — match the SMELL.md entry summary>

**Files affected:** `<canonical file to update>` (REVISIONE), `<other affected files>` (cascade).

- [ ] <The "Suggested project DEVPLAN milestone language" content from the SMELL.md entry>
- [ ] **Resolution per canon-hierarchy:** higher-tier file <file> wins over lower-tier <file>. Update <lower-tier-file> §<section> to value <X> (was <Y>). Internal-consistency check: <one-line citation of the sibling canon that supports the chosen value>.
- [ ] **Cascade:** grep the repository for the conflicting value <Y> and update every occurrence (writing-notes, prose, state.md, outlines, callbacks). Verify no residual.
```

**Autonomous decision + no-Pending entries:** when an ANCHOR-NEEDED finding has multiple plausible resolutions across canon files, the implementing agent picks the canon-defended default per `instructions/milestone-format.md` §Autonomous-decision principle (priority: canon-hierarchy → existing canon → chapter guards → Occam) and writes that choice into the milestone — never escalates the choice to the user via DEVPLAN as "user picks A or B?". The Resolution and Cascade fields above must contain the chosen value, not options.

## Calibration

- **Err toward more objections.** A false positive (an objection the user dismisses) costs nothing. A false negative (a smell that ships) costs trust with the reader.
- **Don't soften.** The reader doesn't soften. Report what you'd flag.
- **Don't rationalize for the writer.** If you find yourself constructing a defense ("well, maybe the writer meant…"), that is a smell — write it as ANCHOR-NEEDED ("the prose does not signal X, so either the prose changes or the worldbuilding canonicalizes X").
- **Specific quotes, not vague feelings.** Every objection is anchored to a quote and a line. "The chapter feels off" is useless.
- **No INLINE for capability/knowledge gaps.** If a character, agent, or object has an unearned capability, prose tweaks rarely fix it — the worldbuilding has to earn it (ANCHOR-NEEDED) or the scene has to defer it (INLINE only if the deferral is clean).

## Notes

- This command is on-demand but recommended after every chapter write, before review/proofread/revise. The pipeline order is: `write → sniff → fix → coherence (chapter-scoped) → fix → review → proofread → revise`.
- `revise.md` consumes SMELL.md INLINE entries automatically (alongside REVIEW.md and PROOFREAD.md). **ANCHOR-NEEDED entries are auto-routed**: the SMELL.md entry stays for traceability; the corresponding fix milestone is appended to `DEVPLAN.md` and applied by `/book fix` on the next orchestration step. By the time `/book revise` runs, ANCHOR-NEEDED entries should already be resolved upstream — revise marks them `Status: ✅ Resolved upstream by /book fix`.
- ACCEPT entries are noted but not acted on. ACCEPT entries that recommend a canon tightening (e.g., "add a sentence to `temporal-echoes.md` to license this uncanny") still get a DEVPLAN milestone — they are auto-applied silently.
- The `SMELL.md` file is per-chapter and overwritten on re-runs. Older sniffs live in git history.
- See `world/canon-hierarchy.md` for the tier order and resolution rules used when populating the Resolution and Cascade fields of each milestone.
