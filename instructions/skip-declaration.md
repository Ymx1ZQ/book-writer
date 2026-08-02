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

## What this is not

It is not a licence to skip. The fallback ladders and gating rules each check defines still govern **whether**
a path may be skipped; this file governs only that the skip is **stated**. A step that skips something it
should have run is still wrong — it is merely no longer invisible.
