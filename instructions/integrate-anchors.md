# `/book integrate-anchors` — Scout-not-Surgeon Writer Pass

This command takes a chapter that has won a multi-model judge competition, plus an aggregated pool of "anchors" — micro-elements (lines, images, moves, beats, concepts) that loser drafts of the same chapter executed better. For each anchor, the writer-agent decides whether to integrate, partially adapt, or skip it, with hard constraints on POV, emotional arc, voice, and word count.

**The writer is the chef, not the scout.** The judge already said "this anchor is interesting in isolation." The writer's job is the *separate* judgment: "does it fit *here*, in this chapter, in this voice, in this rhythm — and if yes, where, and at what dose?" Reject anchors that are good in isolation but break the chapter's spell. Padding the integration log with "skip — does not fit" is the correct outcome for some anchors; do not force fits.

## Invocation

```
/book integrate-anchors <aggregated-json-path>
```

The aggregated JSON is the output of `aggregate-judges.sh`. The fields the writer reads:
- `winner` — id of the winning draft (e.g. `"B"`)
- `anchor_pool` — array of anchor objects with `from`, `type`, `excerpt`, `rationales` (list, one per judge that flagged it)

The winning chapter is at the canonical path `chapters/<book>/<chapter>.md` (already copied into the main repo before this command is invoked). The book and chapter ids are derivable from that path or passed alongside the JSON; establish them before reading.

The current working directory is the project root.

## Hard constraints (apply per anchor)

An anchor is **rejected** (decision = `skip`) if integration would violate any of the following:

1. **POV preservation** — the integrated move must be expressible from the scene's existing POV character. An anchor that requires another character's interiority breaks the rule.
2. **Emotional arc preservation** — the anchor must not invert a beat's emotional valence. If the beat lands as dread, an anchor that turns it into relief is rejected.
3. **Voice match** — the anchor (after any rewording) must match the POV character's voice samples in `characters/notes/voice-samples.md`. If integrating would force a register shift the character would not make, reject.
4. **Word-count budget** — the chapter's total word count may grow or shrink by no more than ±5% across all integrations combined. Each integration's word delta must be tracked; once the budget is exhausted, remaining anchors are rejected with reason `over_budget`.
5. **No external setup** — if a `concept`-type anchor would require introducing setup beats outside this chapter (a prior plant, a future payoff in another chapter, a canon detail not yet established), reject.

## Decision protocol per anchor

For each anchor in `anchor_pool`:

1. **Read the anchor's excerpt + rationales** to understand what the judges identified as the win.
2. **Locate the corresponding slot in the winner** — the scene or paragraph that the anchor improves on. For `beat`-type anchors, the slot is the specific outline beat the loser executed better. For `line`/`image`-type anchors, the slot is the equivalent moment in the winner.
3. **Check the 5 hard constraints.** If any fails, decision = `skip`, log the reason.
4. **Decide between `integrate` (verbatim or near-verbatim) and `partial` (concept/move adapted into the winner's voice and rhythm).** Verbatim integration is rare — most anchors will be `partial` because the winner's voice differs from the loser's. Verbatim is OK only when the line/image is so distinct it would lose force in adaptation.
5. **Apply the edit in place** in `chapters/<book>/<chapter>.md`. Track the word-count delta.
6. **Log the decision** in `archive/integration-log-<book>-<chapter>.md` (see schema below).

## Read these files before any integration

- `chapters/<book>/<chapter>.md` — the winner draft (full read)
- `chapters/<book>/outline.md` — to map beats and slot the anchors correctly
- `characters/notes/voice-samples.md` — the binding constraint on voice match
- `world/tones.md` — register check per scene
- `world/prose-rules.md` — to avoid integrating moves that violate prose rules in the new context

## Integration log schema

Path: `archive/integration-log-<book>-<chapter>.md`. Overwrite on each run (one log per chapter; if re-run, the new log replaces the old).

```markdown
# Integration Log — book-1 ch01

Winner: draft B
Anchors processed: N
Word count before: X
Word count after: Y (delta: ±Z%)

## Decisions

### Anchor 1 — from A, type: line
- **Excerpt:** "..."
- **Judge rationales:**
  - codex: ...
  - claude-default: ...
- **Decision:** integrate (verbatim) | partial (adapted) | skip
- **Location:** scene 3, between paragraphs starting "He turned..." and "The screen..."
- **Adaptation (if partial):** original "..." → integrated as "..."
- **Word delta:** +12 / -3 / 0
- **Rationale:** one sentence on why the decision was right for THIS chapter

### Anchor 2 — from C, type: image
...
```

## Self-check before completion

Before returning:
- Word-count budget respected (total delta within ±5%)
- Each anchor has exactly one decision logged
- All `integrate` and `partial` anchors have explicit location pointers in the log
- All `skip` anchors have a reason logged that maps to one of the 5 hard constraints OR a `taste` rejection ("good in isolation, breaks the chapter's spell here")
- The revised `chapters/<book>/<chapter>.md` reads end-to-end without seams from the integrations

Report at the end: counts of integrate / partial / skip, total word delta, path to the log.
