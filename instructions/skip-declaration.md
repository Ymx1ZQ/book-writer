# Skip Declaration — Shared Doctrine

Every check in this skill has paths it can decline to run: a graph that is stale, a predecessor chapter that
does not exist, a snapshot that was never generated, an optional detector whose input is absent. Declining
is usually correct. **Declining without saying so is not**, and that is the rule this file exists to state.

## The rule

**If a step skips something that changes what it checked, the skip goes in the step's own output, with the
reason.** Not in the transcript, not in a log a reader has to go find — in the report the step writes, next
to the findings, where anyone reading the verdict will see it.

A skip that changes nothing needs no line. A skip that narrows coverage always does.

## Why, and it is measured rather than argued

Three separate defects in the ground-truth pipeline over 2026-08-01/02 were invisible for as long as they
existed, and all three were hidden by the same construct — a silent fallback:

| Defect | Hidden by | Cost |
|---|---|---|
| `/book revise` skipped: its guard matched `**Status:** pending` while the file had written `- **Status:** pending` | `(no pending SMELL entries — revise skipped)` | 5 reader-comprehension fixes never reached the prose; nothing failed |
| `/book fidelity` graph triage queried two node ids no graph has ever produced | `node missing → skip triage silently` | the triage never ran once, for as long as the section existed |
| A session-limit probe wired to read a file nothing writes | the probe simply returned "no limit found" | the fix looked installed and protected nothing |

None of the three produced an error. Each was found by accident, weeks or months late. **A silent fallback
hides a broken path exactly as well as it hides a legitimately unnecessary one** — and from outside, the two
are indistinguishable.

The countermeasure is cheap and it worked the same day it was applied: `/book fidelity` was made to declare
its triage status, and the very next run reported `skipped (stale — 128 content files changed)` on a graph
that had been rebuilt eleven minutes earlier. That declaration is what exposed the step improvising its own
freshness test. One line in a report turned an invisible failure into a measured one inside a single run.

## The form

One line, in the step's summary block, before the findings table:

```
<Path name>: <ran | skipped — reason>
```

Examples from steps that already carry it:

- `Graph triage: fresh (built_at_commit = HEAD) — pair diff used`
- `Graph triage: skipped (stale — 3 narrative files changed since build); verbatim reads performed directly`
- `Adjacency window: skipped (ch01 has no predecessor)`
- `Corpus checks A, B, F, H, I, J, K, U: deferred (chapter scope — not properties of a single chapter)`

Two qualities make the line useful, and a line missing either is not worth writing:

1. **It names the path, not the outcome.** "Some checks skipped" tells a reader nothing they can act on.
2. **The reason distinguishes *unnecessary* from *unavailable*.** `skipped (ch01 has no predecessor)` is a
   closed question. `skipped (graph stale)` is an open one — somebody can go make it fresh.

## The reason must be checkable, not just stated

The prose line above says a path was declined. It cannot say whether the stated reason is **true**, and a
false reason reads exactly like a true one.

**Measured, `ground-truth` ch09 and ch10, 2026-08-02.** `/book fidelity` skipped its entire graph triage on
both runs, declaring `skipped — no per-chapter outline nodes`. The declaration worked: the skip was visible
in both reports. The reason was wrong — it belonged to a query shape already discarded and said nothing
about the two queries then in force. **The rule above caught the skip and could not catch the reason**, so
the triage stayed dead through two more chapters. (That particular path is gone — `fidelity.md` now uses
`chapter-load.py` — but the failure shape is general and every graph-reading check still has it.)

So a declared skip carries a second line, next to the prose one, in a form a script can re-evaluate:

```
SKIP: <path-name> reason=<token> <field>=<value> ...
```

The permitted tokens, and the predicate each one promises:

| `reason=` | Means | Re-checked by |
|---|---|---|
| `stale` | the graph is behind the working tree | re-running the two-command freshness gate; contradicted if it passes |
| `absent` | a required input is not on disk | `test -f <path>`; the line must carry `path=` |
| `empty-result` | a query ran and returned nothing usable | re-running it; the line must carry `query=` and is contradicted if rows come back |
| `no-predecessor` | first chapter of a book, nothing to compare against | the chapter number; a closed question, never re-opened |
| `out-of-scope` | the sub-check belongs to a different scope | the declared scope; `coherence-check.md` book scope deferring the prose checks is this |

**An unrecognised token is itself a finding.** Without that, a run evades the checker by inventing a reason
no predicate covers — which is the precise shape of the ch09/ch10 failure, where the reason named a
condition nothing was testing. If a genuine new reason appears, it is added to this table with its
predicate; it is not declared ad hoc.

The checker reports a contradiction; it does not fail the step. A step that skipped for a false reason has
already produced a narrowed report, and failing it afterwards deletes the partial coverage without
recovering the rest. What matters is that the contradiction is visible in the same cycle rather than found
by accident months later, which is how all three defects in the table above surfaced.

## What this is not

It is not a licence to skip. The fallback ladders and gating rules each check defines still govern **whether**
a path may be skipped; this file governs only that the skip is **stated**. A step that skips something it
should have run is still wrong — it is merely no longer invisible.
