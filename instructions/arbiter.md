# `/book arbiter` — Autonomous Decision for PENDING Trade-Offs

Resolves every open item in `chapters/<book>/{SMELL,REVIEW,PROOFREAD}-PENDING.md` with a forced binary decision (`apply` or `defer`) — no third option, no human-in-loop. This stage is where the pipeline's autonomy is guaranteed: after it runs, no PENDING file may carry a `Status: pending` line.

The arbiter is a **single judge** by design: a deterministic 6-step rubric, one decision per item. Borderline calls are broken by the rubric's tie-breaker rules, not by deferring to the user.

## Invocation

```
/book arbiter <book> <chapter>
```

`<book>` e.g. `book-1`. `<chapter>` e.g. `ch01`. Current working directory is the project root.

## Files to read

- `chapters/<book>/SMELL-PENDING.md` — sniff trade-offs (Quote / Loss / Voice-floor / Suggested action format)
- `chapters/<book>/REVIEW-PENDING.md` — review trade-offs (Find / Proposed fix / Loss / Gain / Voice-floor flag / Voice-Signature flag format)
- `chapters/<book>/PROOFREAD-PENDING.md` — if present
- `chapters/<book>/SMELL.md` — the full sniff output; read to detect Category 10 §10.f `SATURATION` findings (a saturated device disables rule-3 protection for its instances — see rule 3)
- `chapters/<book>/<chapter>.md` — the chapter prose (read in full before editing)
- `chapters/<book>/writing-notes.md` — the chapter's voice-floor pillar beats and per-chapter constraints
- `characters/notes/voice-samples.md` — voice signature reference per POV character
- `world/prose-rules.md` — prose-quality rules and named patterns (§9 negation chains, §12 banned terms, etc.)
- `world/writing-checklists.md` — level-appropriate sensory expectations
- The character file matching the chapter's POV (e.g. `characters/foreground/noah.md`) — Voice Signature section + canon constraints

If a PENDING file does not exist or has no open items, skip it. If no PENDING file has any open items, exit immediately with a one-line confirmation; do not edit anything.

## Decision rubric — 6 weighted rules, applied in order

For each open item, evaluate the rules below in order. The **first matching rule** determines the decision. Stop at the first match.

1. **Hard-rule violation** — if the item flags a concrete canon contradiction (character age / location / technology level / domain plausibility like SCI temperature sensation / banned slang from `language-evolution.md`) OR a `world/prose-rules.md` §X explicit rule violation **AND** the proposed fix removes the violation: **APPLY**. Override only if the chapter's `writing-notes.md` documents an explicit per-chapter exception (rare; require a literal cross-reference).

2. **Voice-Signature alignment** — if the item's flags name a Voice-Signature property (e.g. Noah §Voice Signature: "never explains his own emotions") AND the current text violates that property (narrator label, telling-not-showing, premature interpretation) AND the proposed fix removes the violation: **APPLY**.

3. **Voice-Floor protection** — if the item carries `Voice-floor: Yes` (an unqualified yes, not "borderline") meaning it sits in one of the chapter's 3–7 voice-floor pillar beats per `writing-notes.md`: **DEFER**. Pillar beats outrank tightening wins.

   **Saturation carve-out.** Rule 3 protects *distinct* pillar beats. It does NOT fire when the item is an instance of a stylistic device that `chapters/<book>/SMELL.md` has raised a Category 10 §10.f `SATURATION` finding for. A line interchangeable with a dozen others is not a pillar beat, and deferring every instance of a saturated device is the exact failure mode the `SATURATION` finding exists to break. When this carve-out applies, skip rule 3 and continue to rules 4-6.

   **Beat-economy carve-out.** Likewise, rule 3 does NOT protect the *redundant re-render* of a **beat-economy / discharged-recurrence** finding (Reviewer Rule 25) whose guards were already cleared at the reviewer stage (not a registered motif/payoff, not a voice-floor pillar, not escalating thematic work). The protected thing is the beat's *first*, function-discharging occurrence — the fix does not touch it; it only compresses the *later* re-render down to its delta (the one new element). A second near-verbatim rendering of an already-discharged beat is not a distinct pillar beat. When this carve-out applies, skip rule 3 and continue to rules 4-6 (which APPLY the delta-compression unless rule 1/2 fired earlier). The `Suggested action`'s delta-preserving instruction is the change to apply verbatim.

   **Exposition-economy carve-out.** Likewise, rule 3 does NOT protect the *redundant / self-evident / over-run span* of an **exposition-economy** finding (Reviewer Rule 26) whose guards were already cleared at the reviewer stage (not first-occurrence onramp, not a planted payoff, not a voice-floor pillar, not a once-stated irony/thematic payload, not in-character expert perception). The protected thing is the *first, load-bearing* statement of the fact/rule/stake — the fix never touches it; it removes only the restatement, the self-evident justification, or the run-up past the button. Neither a re-statement of something the chapter already established nor a justification of something the reader already infers is a distinct pillar beat. When this carve-out applies, skip rule 3 and continue to rules 4-6 (which APPLY the trim unless rule 1/2 fired earlier). For pattern-(a) pure restatement the finding is SAFE-CUT and bypasses the trade-off ledger entirely.

4. **Loss specific + Gain generic** — if the Loss field names concrete content (a specific image, compression burst, structural function, beat-level role) and the Gain field is generic ("tighter", "cleaner", "removes editorializing" without naming what specifically): **DEFER**. Concrete value outranks generic improvement.

5. **Loss generic + Gain specific** — inverse of rule 4. The Gain names a concrete rule alignment, beat function, or canon pairing; the Loss is hand-wavy: **APPLY**.

6. **Balanced** — both Loss and Gain are specific (or both generic): **DEFER**. Default to preserving the writer's choice on a genuine coin-flip; conservative is the right bias for an autonomous editor on the first integration pass.

If two rules could fire (e.g. rule 1 hard-rule + rule 3 voice-floor), the lower-numbered rule wins. Hard rules always beat voice-floor protection because plausibility breaks the reader contract harder than a softer beat does.

## What to do on APPLY

1. Open `chapters/<book>/<chapter>.md`
2. Locate the line(s) cited in the item's `Location:` field (and quote, if present)
3. Apply the change per the item's `Suggested action:` (SMELL) or `Proposed fix:` (REVIEW) field
4. If the suggested action is a choice ("either X or Y"), pick the option that introduces the smallest word-count delta consistent with preserving voice
5. After the edit, re-read the surrounding paragraph to confirm flow is preserved; if a graft-seam appears, smooth with a one-clause adjustment

## What to do on DEFER (= ACCEPT-keep)

The arbiter is choosing to keep the current prose as-is. This is a **final** decision, not a postponement — the word "defer" is internal arbiter shorthand for "accept current text". The decision must propagate to the active convergence ledger so future codex book-editor cycles do not re-emit the same trade-off.

Two actions on ACCEPT-keep:

1. **No prose change** in `chapters/<book>/<chapter>.md`.

2. **Append a SAFE-KEEP entry** to the active source file's `## Acknowledged (SAFE-KEEP — no action)` section (for SMELL) or `## Acknowledged (No Action)` section (for REVIEW). Map the active PENDING file to its source (SMELL-PENDING→SMELL.md, REVIEW-PENDING→REVIEW.md, …); the item's `Source:` field names the *detector* (sniff/coherence/factcheck/…), not the filename.

   - If the Acknowledged section does not exist in the source file, create it at the bottom (use exactly the heading the codex book-editor uses for that file type — see `chapters/<book>/SMELL.md` / `REVIEW.md` for live reference).
   - Entry format (SMELL):
     ```
     - **<short title from the PENDING item>.** <one-paragraph rationale citing the rule that made the arbiter ACCEPT — e.g. "Rule 3 voice-floor protection: this beat is one of the chapter's 3–7 voice-floor pillars per writing-notes; tightening costs more than it gains." Reference the original PENDING item by its `Source:` line so the convergence ledger trail is auditable.>
     ```
   - Entry format (REVIEW): same shape, written into REVIEW.md's Acknowledged (No Action) section.

   This closes the loop: next cycle's codex sniff/review sees the SAFE-KEEP entry and does not re-flag the trade-off.

## Status field update — required for every item

In the PENDING file, replace the item's existing `Status: pending — manual decision required` line with one of:

- `**Status:** ✅ Fixed (autonomous) — rule N: <one-sentence rationale>` (for APPLY)
- `**Status:** ✓ Accepted (autonomous) — rule N: <one-sentence rationale>` (for ACCEPT-keep)

Use `Accepted (autonomous)` literally — not `defer-autonomous`, not `accept-autonomous`. "Defer" was an early naming mistake; the decision is a final accept-keep.

The rule number must match the rubric step that fired. The rationale must explain *why* that rule applied to this specific item — not just restate the rule.

## Final summary

After processing all items, append at the bottom of each modified PENDING file:

```
---

## Autonomous-arbiter run — <YYYY-MM-DD HH:MM>

- Total items: N
- APPLY: N (rules: N1×rule1, N2×rule2, ...)
- ACCEPT-keep: N (rules: N3×rule3, N4×rule4, N5×rule5, N6×rule6)
- Chapter prose lines modified: N
- Chapter word count delta: ±N
- SAFE-KEEP entries appended to active ledger: N
```

Then print to stdout a short status line per PENDING file (count of apply/defer + path), and a final summary across all files.

## Self-check before completing

- Every open item now has a `✅ Fixed (autonomous)` or `✓ Accepted (autonomous)` status — zero `pending` remain across all PENDING files
- Every APPLY decision corresponds to an actual prose edit in `chapters/<book>/<chapter>.md`
- Every ACCEPT-keep decision corresponds to a SAFE-KEEP entry appended to the source file's Acknowledged section
- The chapter still reads end-to-end without seams from the autonomous edits
- Word-count delta across all APPLYs is reasonable (typically <2% per arbiter pass)
- No new PENDING items were created (the arbiter never surfaces new trade-offs)

If any check fails, fix before exiting.

## Graph refresh (post-commit — APPLY outcomes only)

If at least one item resolved as APPLY (chapter prose actually changed) and `graphify-out/graph.json` exists in the project root, refresh the knowledge graph after the arbiter's commit lands, per `instructions/graph-recall.md` §Keeping the graph fresh (incremental update; >25-changed-file skip bound; soft-fail — a failed refresh never fails the run). A pure ACCEPT-keep run changes no prose — skip the refresh entirely. This is graph maintenance only: the no-graph-consumption rule for this command is unchanged. Graph absent → skip silently.
