# Graph-Assisted Recall (graphify) — Shared Doctrine

Optional accelerator: when the consuming project keeps a graphify knowledge graph, pipeline steps replace bulk canon loading with targeted graph queries — same conclusions, a fraction of the tokens. This file is the SINGLE SOURCE OF TRUTH for how the graph is used. Consumers (`chapter-writer.md`, `coherence-check.md`, `continuity-check.md`, `motif.md`, `adjacency.md`, `fidelity.md`, `sniff.md`, `reviewer.md`) cross-reference this file — they never restate it.

## Opt-in detection

Graph use activates ONLY if `graphify-out/graph.json` exists in the project root:

```bash
test -f graphify-out/graph.json
```

Absent → every instruction behaves exactly as today. No graph, no change, no warning. The skill stays project-agnostic: whether a project builds a graph (via `/graphify`) is the project's choice.

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
- Different → list the content files changed since the build:

```bash
git diff --name-only "$BUILT" HEAD -- 'world/' 'characters/' 'plot/' 'chapters/'
```

Filter the output to `.md` files. Empty → **fresh** (only non-canon files moved). Non-empty → **stale**:

- **Answer mode** is forbidden on a stale graph. Either run the incremental update first (`/graphify --update`) or fall back to file loading for that check.
- **Index mode** may proceed — but every pointer into a file on the changed list MUST be re-read from disk (which index mode does anyway).

If the gate cannot be evaluated (`jq` missing, not a git repo, `built_at_commit` absent from graph.json), treat the graph as stale: index mode only.

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
- `judge.md`, `arbiter.md`, `integrate-anchors.md` — keep their verbatim loads (voice/rule fidelity). No graph substitution.
- `reviewer.md` (Phase 21) keeps its verbatim rubric set (`prose-rules.md`, `voice-samples.md`, `writing-notes.md`, the target chapters) but uses index-mode graph triage to name which prior-chapter §§ its checks K and M re-read — see `reviewer.md` step 2.6. Nothing in the rubric or the review set is substituted.

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

Any command whose edits touch graph-covered sources (`world/`, `characters/`, `plot/`, `chapters/`) ends with a refresh step, so the next consumer's freshness gate passes instead of degrading to file loads. Commands carrying the step: `fix.md`, `revise.md`, `chapter-writer.md`, `compact.md`, `integrate-anchors.md`, `arbiter.md` (APPLY outcomes only — a pure ACCEPT-keep run changes no prose and skips it).

- **Gate** — same opt-in as the read side: `test -f graphify-out/graph.json`. Absent → skip silently, no warning.
- **Mechanics** — run the incremental update flow: `/graphify . --update`. It re-extracts only changed files; the session itself is the extractor, so cost is proportional to the edit — typically 1-10 files.
- **Bound** — before refreshing, count what the update would re-extract (same diff as the freshness gate: `git diff --name-only "$BUILT" HEAD -- 'world/' 'characters/' 'plot/' 'chapters/'`, filtered to `.md`). If the count exceeds 25, SKIP the inline refresh and leave it to the cycle-boundary backstop (`run-merge-phase.sh` terminal refresh), logging one line: `graph refresh skipped: N changed files > 25, deferred to cycle boundary`. A bulk rewrite must not trigger a mid-command mega-extraction.
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
