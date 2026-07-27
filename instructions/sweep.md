# /book sweep — Terminal Sweep of Review Artifacts

Archive the residual review artifacts of fully-closed chapters from `chapters/<book>/` root into `chapters/<book>/archive/`.

## Invocation

```
/book sweep <book>
```

Argument: `<book>` (e.g. `book-1`, `book-2`, `book-3`).

## Why this exists

Every review-producing skill (`sniff`, `review`, `coldread`, `proofread`) and `revise`'s `*-PENDING.md` emitters already have a **rotate-on-write** archival pattern: when re-run for the next cycle on the same book, they move the existing artifact into `archive/<TYPE>-<TIMESTAMP>-<chapter>.md` before writing the new one.

That handles every cycle except the **last one for a chapter** — no follow-up run for a closed chapter ever happens, so its terminal artifacts sit forever at the chapter-dir root, accumulating across chapters.

## What it does

Shells out to `<repo>/sweep-chapter-archive.sh <book>` (the single bash motor — see comments in that file for full spec). For each of these basenames at the chapter-dir root:

- `SMELL.md`, `SMELL-PENDING.md`
- `REVIEW.md`, `REVIEW-PENDING.md`
- `PROOFREAD.md`
- `COLDREAD.md`

…archive only when **all** of these hold (fail-safe: any doubt → keep in place):

1. File is one of the names above and at chapter-dir root.
2. No `Status: pending` line (case-insensitive, accepts bold-wrapped variants).
3. No unprocessed `- [ ]` checkbox.
4. Header references parsable `chNN` token(s) AND every referenced chapter is `- [x]` in `chapters/<book>/DEVPLAN.md` AND no multi-chapter range collision (`Ch.04 – Ch.06` skip; degenerate `Ch.03 – Ch.03` pass).
5. File mtime > 60s (race guard against in-flight cycles).

Destination: `chapters/<book>/archive/<TYPE>-<YYYYMMDD-HHMMSS>-final-<chapter>.md`. Suffix `-final-` distinguishes the terminal archive from the existing interim rotate-on-write archives. Filename collision at the same second appends `-2`, `-3`, …

`mv` not `rm`. Exit 0 always (best-effort). Silent when no candidates exist.

## When to invoke

- **Manually**: when you want to clear residue without waiting for the next batch.
- **Auto** (no user action required): the writer's Session Start runs it before context refresh; `run-coherence-cycle.sh` and `run-write-cycle.sh` run it at clean exit.

## Execution

1. Run `bash <repo-root>/sweep-chapter-archive.sh <book>` (no flags for live; add `--dry-run` to preview).
2. Surface the script's stdout to the user verbatim. Output is one of:
   - silent (no candidates found — nothing to do)
   - per-file `ARCHIVED <name> → archive/<dst>` / `SKIP <name>: <reason>` lines + summary `sweep: N archived, M skipped`
   - `WOULD ARCHIVE …` / summary `sweep: N candidate(s), M skipped` in dry-run mode

## Safety properties

- **Idempotent.** Re-running on a clean directory is a silent no-op.
- **Reversible.** Every action is `mv` into a timestamped destination; `git mv` undoes any wrong move.
- **Fail-safe.** Any parsing ambiguity → SKIP with reason. The script never deletes, and never archives a file that still has actionable content.
- **Race-safe.** 60-second mtime guard prevents racing against a cycle that just wrote a fresh artifact.

## Related

- `instructions/sniff.md`, `instructions/reviewer.md`, `instructions/coldread-enum.md`, `instructions/coldread-filter.md`, `instructions/proof-reader.md`, `instructions/revise.md` — pre-step rotate-on-write archival (interim cycles).
- `instructions/writer.md` §Session Start Step 0 — auto-invocation hook.
- `run-coherence-cycle.sh`, `run-write-cycle.sh` — auto-invocation at clean exit.
