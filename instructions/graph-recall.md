# Graph-Assisted Recall (graphify) — Shared Doctrine

Optional accelerator: when the consuming project keeps a graphify knowledge graph, pipeline steps replace bulk canon loading with targeted graph queries — same conclusions, a fraction of the tokens. This file is the SINGLE SOURCE OF TRUTH for how the graph is used. Consumers (`chapter-writer.md`, `coherence-check.md`, `continuity-check.md`, `motif.md`, `adjacency.md`, `sniff.md`, `reviewer.md`, `factcheck.md`, `sensitivity.md`, `coldread-filter.md`, `readability.md`) cross-reference this file — they never restate it.

## Opt-in detection

Graph use activates ONLY if `graphify-out/graph.json` exists in the project root:

```bash
test -f graphify-out/graph.json && [ "${GRAPH_DISABLE:-0}" != "1" ]
```

Absent → every instruction behaves exactly as today. No graph, no change, no warning. The skill stays project-agnostic: whether a project builds a graph (via `/graphify`) is the project's choice.

**`GRAPH_DISABLE=1` forces the no-graph path with the graph still on disk.** It exists to test the claim this whole file rests on — that a check reaches the same findings either way. Nothing has ever measured that: the fallback ladder below is a *design*, and every defence around it (the skip declaration, the wiring tests) catches a step that declined a path, not a step that took both paths and got different answers. Run a chapter's detectors twice, once with the flag, and diff the findings; a material difference falsifies the equivalence and the savings are not free. It is a measurement switch, not a mode — nothing in the pipeline sets it by default.

## Two modes

| Mode | What the query result is | Staleness tolerance |
|---|---|---|
| **Index mode** (default) | File/§ **pointers**. The agent reads the pointed-to sections from disk — the file is the truth. | Tolerant — pointers into changed files are re-read from disk anyway (already the rule). |
| **Answer mode** | Content consumed **directly** (plant/payoff tables, thread lists, tracker assignments) without opening the underlying files. | Strict — allowed ONLY when the freshness gate below passes. |

Consumers declare which mode each of their graph uses runs in. When in doubt, use index mode — it can never serve stale content because the disk read is the final word.

## Freshness gate

Run from the project root:

```bash
BUILT=$(jq -r .built_at_commit graphify-out/graph.json)
git rev-parse HEAD
```

- Same commit → **fresh**.
- Different → list the **narrative content** files changed since the build:

```bash
git diff --name-only "$BUILT" HEAD -- 'world/' 'characters/' 'plot/' 'chapters/' \
  | grep '\.md$' \
  | grep -vE '(^|/)(SMELL|REVIEW|PROOFREAD|COLDREAD)[^/]*\.md$' \
  | grep -vE '(^|/)DEVPLAN\.md$' \
  | grep -vE '(^|/)(archive|coldread-state|pub)/'
```

Empty → **fresh** (only non-canon files moved). Non-empty → **stale**:

- **Answer mode** is forbidden on a stale graph. Either run the incremental update first (`/graphify --update`) or fall back to file loading for that check.
- **Index mode** may proceed — but every pointer into a file on the changed list MUST be re-read from disk (which index mode does anyway).

If the gate cannot be evaluated (`jq` missing, not a git repo, `built_at_commit` absent from graph.json), treat the graph as stale: index mode only.

**Run the two commands above and nothing else. Do not substitute your own staleness test.** In particular, **never derive freshness from `graphify-out/manifest.json`.** That file lists every path graphify has ever scanned, including the ones `.graphifyignore` keeps *out* of the graph — so comparing it against disk reports the working ledgers as changes to a graph that does not contain them, and returns stale forever. Measured 2026-08-02: with `built_at_commit` equal to `HEAD` and the git gate returning **0**, a `/book fidelity` run that improvised a manifest comparison reported *"stale — 128 content files changed"* and skipped its triage on a graph that had been rebuilt eleven minutes earlier. The gate is two commands because two commands are auditable; a re-derivation is not.

**Why the filters, and why they must match the project's `.graphifyignore`.** The gate asks whether the graph still describes the corpus, so it must only count files the graph *contains*. The excluded names are working ledgers the pipeline rewrites many times per chapter — `SMELL.md` alone is touched by sniff, coherence, factcheck, motif, sensitivity, fidelity, readability, adjacency, coldread-filter and revise — plus rotated archives, reader-state snapshots and build output. Measured on `ground-truth` 2026-08-02: of the eight files that marked the graph stale after a chapter merge, **six were ledgers and two were narrative**. Counting them meant the gate read stale from the second step of every cycle, so all eight consumers below fell back to whole-file loading, silently, and the saving this file exists to describe never arrived.

The filter list and the project's `.graphifyignore` are one decision in two places: a file the graph indexes but the gate ignores can go stale unnoticed, and a file the gate counts but the graph never held makes the gate lie in the safe direction forever. **Change one, change the other.**

## Never-substitute list

These are ALWAYS read verbatim from disk, in full, exactly as each instruction specifies today. The graph may POINT at them; it may never paraphrase them:

- `world/prose-rules.md`
- `characters/notes/voice-samples.md`
- `world/register-locks.md`
- `characters/notes/narrator-boundaries.md`
- `chapters/*/writing-notes.md`
- Any numeric canon anchor (prices, frequencies, allocation math) — the exact figure comes from the anchor file, never from a graph node's summary of it.

Reason: these files carry voice, register, and numeric fidelity. A paraphrase that is 95% right is a defect injector — the remaining 5% is precisely the class of drift the pipeline exists to catch.

## Canon-blind exclusions

The graph is a canon-recall device. Commands whose value depends on NOT having canon, or on verbatim-load fidelity, never use it:

- `coldread-enum.md` and `snapshot.md` — **MUST NOT gain graph access.** Their measured detector value (Phase 40: 0.5/19 → 13/19 user-class bugs) depends on canon-blindness; a graph query is a canon leak.
  **Second measurement, `ground-truth` ch10 on 2026-08-02:** coldread-enum returned **40 findings on a chapter where factcheck, motif, sensitivity, fidelity, adjacency and readability each returned zero**. The gap is not enum being noisy — it is the only step reading as a reader who does not know the project, and it is the class of defect the canon-aware checks structurally cannot see. Anything that closes that gap deletes the capability. Its partner `coldread-filter` is where canon belongs: **enumerate blind, triage informed** — which is why the 2026-08-02 rollout added the graph to the filter and not the enum.
- `judge.md`, `arbiter.md`, `integrate-anchors.md` — keep their verbatim loads (voice/rule fidelity). No graph substitution.
  For `judge.md` there is a second, independent reason worth recording so nobody re-opens it: **three of its four lanes run outside Claude Code** (codex, and DeepSeek/Gemini under opencode) and have no `graphify query`. Wiring only the Anthropic lane would give one judge of four a different evidence base from the other three — worse for the ensemble than giving none of them the graph.
- `reviewer.md` (Phase 21) keeps its verbatim rubric set (`prose-rules.md`, `voice-samples.md`, `writing-notes.md`, the target chapters) but uses index-mode graph triage to name which prior-chapter §§ its checks K and M re-read — see `reviewer.md` step 2.6. Nothing in the rubric or the review set is substituted.

## Answered without the graph

A question a deterministic script already answers does not belong here. The graph's value is recall over
text nothing has indexed; where the project ships an index, the graph is a slower copy of it that can also
be stale.

- `fidelity.md` — **removed as a consumer 2026-08-03.** Its triage asked "which files carry the tracker rows
  marked `written` for ch<NN>", and `chapter-load.py --chapter <B>:<NN> --written` answers exactly that from
  the Usage Trackers, which are the source of truth for those rows. The script cannot go stale, has no
  fallback to decline, and costs no extraction. Its second query, for plant instances, was redundant with a
  read the check already performs (the outline's §Inline Plant Tracking table).

  Recorded rather than dropped, because the cost of the graph path was not hypothetical: measured on ch09
  and ch10, both runs skipped the whole triage citing a reason that did not apply, and both declared the
  skip correctly — the contract surfaced *that* a path was declined and could not tell the reason was false.
  Re-adding a query here re-adds that failure mode.

**Before wiring a new consumer, ask whether a script already knows.** `chapter_load.py` alone answers
tracker reachability, per-chapter load, orphans, rendered rows, concept ownership and devplan drift.

## Fallback ladder

At every rung, the answer is "load files as the instruction specifies today" — the file path is always the safety net, never an error state:

1. `graphify-out/graph.json` absent → no graph use at all.
2. Graph present but stale → index mode only; answer-mode checks fall back to file loading (or `/graphify --update` first).
3. Query returns nothing, or the node doesn't exist → load the files for that item as today. An empty query result is never evidence of absence — it may be a vocabulary mismatch.

## Query grammar

Three commands, run from the project root (the graphify skill handles interpreter resolution):

```bash
graphify query "<question>"          # BFS traversal — broad context
graphify query "<question>" --dfs    # DFS — trace a specific path
graphify query "<question>" --budget 1500   # cap answer at N tokens
graphify path "<node A>" "<node B>"  # shortest path between two concepts
graphify explain "<node>"            # plain-language explanation of one node
```

Concrete examples in pipeline use:

```bash
graphify query "usage-tracker items assigned to book-1 ch07"
graphify query "what must book-1 ch07 set up and pay off"
graphify query "every prestige-inventory plant and its payoff chapter"
graphify query "open threads and ticking clocks at end of book-1"
graphify path "moka pot" "book-2 ch05"        # does the motif reach its payoff chapter?
graphify explain "Sauveterre plant"            # everything the graph holds on one plant
```

Query results cite `source_location` (file + section) per node — in index mode those citations are the pointers you read from disk; in answer mode the cited locations are your audit trail.

## Keeping the graph fresh (write side)

**Instruct the extractor how to chunk, every time.** graphify splits work into chunks of 20-25 **files** with no line budget, so how much text one extraction agent receives depends on how large the files happen to be. Measured on `ground-truth` 2026-08-02: 216 files / 34,340 lines gives 10 agents at ~3,400 lines each, against a ~1,200-line budget — three times over, and not because of one oversized file (the largest was 1,179 lines). The symptom is under-extraction, and it is large: the same extractor produced **2,553 nodes / 3,604 edges** with file-count chunks and **5,965 / 10,093** with line-budget chunks over 40% *less* text. So every refresh this skill triggers should carry an instruction to budget by lines, to give any file over the budget its own agent, and to reject a chunk that returns zero edges or partial coverage rather than merge it.

A consuming project should keep that instruction in one versioned file rather than retyping it per call site — `ground-truth` uses `graph-refresh-prompt.sh`. **It is a mitigation and not a fix:** it is prose competing with graphify's own SKILL.md, it won when measured, and a refresh that comes back thin should be checked for whether the instruction was followed before the corpus is blamed. The fix belongs in graphify.

Any command whose edits touch graph-covered sources (`world/`, `characters/`, `plot/`, `chapters/`) ends with a refresh step, so the next consumer's freshness gate passes instead of degrading to file loads. Commands carrying the step: `fix.md`, `revise.md`, `chapter-writer.md`, `compact.md`, `integrate-anchors.md`, `arbiter.md` (APPLY outcomes only — a pure ACCEPT-keep run changes no prose and skips it).

- **Gate** — same opt-in as the read side: `test -f graphify-out/graph.json`. Absent → skip silently, no warning.
- **Mechanics** — run the incremental update flow: `/graphify . --update`. It re-extracts only changed files; the session itself is the extractor, so cost is proportional to the edit — typically 1-10 files.
- **Bound — measured in LINES, not files.** Before refreshing, size what the update would re-extract: take the same diff the freshness gate uses (`git diff --name-only "$BUILT" HEAD -- 'world/' 'characters/' 'plot/' 'chapters/'`, filtered to `.md` and to the same exclusions), then `wc -l` the survivors. **Over ~1,200 lines — one extraction agent's budget — SKIP the inline refresh** and leave it to the cycle-boundary backstop (`run-merge-phase.sh` terminal refresh), logging one line: `graph refresh skipped: N lines across M files > 1200, deferred to cycle boundary`. A bulk rewrite must not trigger a mid-command mega-extraction.

  **Why lines, and do not "simplify" this back to a file count.** Extraction runs at **~90 lines per minute** and it is model work, so it does not get cheaper on faster hardware. Measured on `ground-truth` 2026-08-03: a `/book fix` applying 14 items took 48 minutes, of which the edits were 11 and the inline refresh 37 — 33 of those in extraction alone, on 3,008 lines across 11 files. The chunking was correct; the gate that let it run inline was not, because it counted files and the cost is paid in lines. A file count errs both ways: 25 files at that delta's 273-line mean is ~6,800 lines and roughly 75 minutes inline without firing, while 26 character files at 40 lines is cheaper than a single chapter draft and is blocked. This is the same defect the paragraph above diagnoses in graphify's own chunker, and writing it here once already failed to stop it being written into the gate.

  For scale, the deltas this bound actually sees: a chapter draft is 135-176 lines, a routine `/book fix` around 330. The common case stays inline; only the bulk canon pass defers.

- **A deferral is recorded, not just logged.** On skipping, write `graphify-out/.refresh-deferred` containing the command name, the current commit and the line count. The cycle-boundary refresh clears it on success and, on failure with the marker present, reports a finding instead of a stderr warning. Without the marker the boundary run cannot tell whether it is the only thing keeping the graph fresh or a routine top-up, and it is allowed to fail quietly — which is safe only in the second case.
- **Ordering** — the refresh runs AFTER the command's own commit (SKILL.md dispatch step 5), so graph artifacts never enter the command's commit. `graphify-out/` is also gitignored project-side.
- **Soft-fail** — a failed refresh never fails the command. Log and move on; consumers are protected by the read-side freshness gate above.

The refresh is graph *maintenance*, not graph *consumption*: it feeds nothing back into the command's judgment. It therefore does not conflict with the canon-blind exclusions above — `arbiter.md` and `integrate-anchors.md` keep their verbatim loads and still refresh the graph their edits just invalidated. `coldread-enum.md` and `snapshot.md` stay fully outside on both sides: no graph access, no refresh step (their output files going briefly stale in the graph is accepted; the backstop covers them).

## Rules

- ❌ Never use the graph when `graphify-out/graph.json` is absent — behavior must be byte-identical to a graph-less project
- ❌ Never consume a query result directly (answer mode) without passing the freshness gate
- ❌ Never paraphrase a never-substitute file from graph content — point, then read from disk
- ❌ Never give `coldread-enum`, `snapshot`, `judge`, `arbiter`, or `integrate-anchors` graph access (`reviewer.md`'s graph use is confined to checks K/M prior-chapter triage, index mode — see §Canon-blind exclusions)
- ❌ Never treat an empty query result as "the thing doesn't exist" — fall back to file loading
- ✅ Index mode is the default; answer mode is the earned exception
- ✅ The graph prunes what you LOAD; it never edits what the project AUTHORED (outlines, `context:` tags, trackers stay the artifacts of record)
- ✅ When the graph and a disk file disagree, the disk file wins — rebuild the graph, don't trust it
- ✅ Mutating commands refresh the graph after their own commit (§Keeping the graph fresh); a failed or skipped refresh never fails the command
