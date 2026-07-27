#!/usr/bin/env python3
"""Re-point `chNN.md:LINE` citations after a prose edit moved the lines.

The corpus cites prose by line number, and those citations are load-bearing: a
later pass follows one to check that a canon claim is still true against the
text. An insertion invalidates every citation below it in the same file, and it
does so silently -- the stale citation still points at a real line, which now
says something else, so the pass either verifies the wrong text or records a
second false claim on top of the first.

Measured on the ground-truth corpus, 2026-07-26: one `/book revise` pass
inserted seven lines at `ch07.md:39-45` and shifted 61 citations in the
deviation ledger alone; four of the five entries a later pass re-verified
carried a wrong line. Nothing failed. The corpus has 140 live prose citations,
only 11% of which quote the text they cite, and none of the shifted ones pointed
past end of file -- so neither a quote check nor a bounds check would have found
them. The only component that knows the shift is the one that caused it.

Called by `/book revise` (instructions/revise.md Step 5.8) with the chapter file
it just edited, before the commit. Compares the working tree against the last
commit, so it must run while the edit is still uncommitted.

Usage:
    remap_citations.py <repo-root> <chapter-file> [<chapter-file> ...]
    remap_citations.py --check <repo-root> <chapter-file> ...   # report only

Exit status is 0 when every citation was remapped or none needed it, and 1 when
at least one could not be (its target line was deleted, or the chapter name is
ambiguous across books). Those are reported for a decision and never guessed.
"""

import difflib
import re
import subprocess
import sys
from pathlib import Path

# Files whose citations are a historical record of what was true when written.
# Rewriting them would falsify the record: a SMELL entry dated 2026-06-04 cites
# the line it actually examined, and the deviation ledger is append-only by its
# own rule -- a stale citation there is corrected by a dated append, not by an
# edit to the ratified text.
HISTORICAL = re.compile(
    r"(^|/)(archive/|SMELL|PROOFREAD|REVIEW|COLDREAD|DEVPLAN\.md|outline-deviation\.md)"
)

CITATION = re.compile(r"\b(ch\d{2})\.md:(\d+)(-(\d+))?")


def _git(root, *argv):
    out = subprocess.run(
        ("git",) + argv, cwd=root, capture_output=True, text=True
    )
    return out.stdout if out.returncode == 0 else None


def line_map(old_text, new_text):
    """old line number (1-based) -> new line number, or None if the line is gone.

    difflib gives matching blocks; a line inside one moves by the block's offset.
    A line in a 'replace' or 'delete' range has no counterpart, and this returns
    None for it rather than picking the nearest survivor -- a citation whose
    target was rewritten needs a human verdict, not a plausible-looking number.
    """
    old = old_text.split("\n")
    new = new_text.split("\n")
    mapping = {}
    for block in difflib.SequenceMatcher(None, old, new, autojunk=False).get_matching_blocks():
        for k in range(block.size):
            mapping[block.a + k + 1] = block.b + k + 1
    return mapping


def drafted_books(root, chapter_stem):
    """Which books hold a file named <chapter_stem>.md."""
    return sorted(
        p.parent.name
        for p in (root / "chapters").glob(f"book-*/{chapter_stem}.md")
    )


def live_files(root):
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if HISTORICAL.search(rel) or rel.startswith(".git/"):
            continue
        yield p


def remap(root, chapter_paths, apply=True):
    root = Path(root).resolve()
    maps = {}
    unresolved = []

    for cp in chapter_paths:
        # Resolve against the repo root, not the process cwd. The caller passes
        # a repo-relative path (`chapters/book-1/ch07.md`), which only happens
        # to work when the shell is already sitting in the repo.
        cp = Path(cp)
        cp = cp if cp.is_absolute() else (root / cp)
        rel = cp.resolve().relative_to(root).as_posix()
        old = _git(root, "show", f"HEAD:{rel}")
        if old is None:
            print(f"  SKIP {rel} — not in HEAD, nothing to compare against")
            continue
        new = (root / rel).read_text(encoding="utf-8")
        if old == new:
            continue
        stem = cp.stem
        books = drafted_books(root, stem)
        if len(books) > 1:
            # A bare `chNN.md:LINE` citation names no book. With one drafted
            # book the reference is unambiguous; with several it is not, and
            # guessing would rewrite a citation into the wrong chapter.
            unresolved.append(
                f"{stem}.md is drafted in {len(books)} books ({', '.join(books)}) — "
                f"bare citations are ambiguous, remap by hand"
            )
            continue
        maps[stem] = line_map(old, new)

    if not maps:
        return unresolved

    changed_files = 0
    changed_cites = 0
    for f in live_files(root):
        text = f.read_text(encoding="utf-8")
        if not any(f"{stem}.md:" in text for stem in maps):
            continue
        rel = f.relative_to(root).as_posix()

        def sub(m):
            nonlocal changed_cites
            stem, start, dash, end = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            if stem not in maps:
                return m.group(0)
            mp = maps[stem]
            ns = mp.get(start)
            if ns is None:
                unresolved.append(
                    f"{rel}: {stem}.md:{m.group(2)}{dash or ''} — cited line was "
                    f"rewritten or deleted, no counterpart in the new text"
                )
                return m.group(0)
            if dash:
                ne = mp.get(int(end))
                if ne is None:
                    unresolved.append(
                        f"{rel}: {stem}.md:{start}-{end} — range end was rewritten "
                        f"or deleted"
                    )
                    return m.group(0)
                if (ns, ne) == (start, int(end)):
                    return m.group(0)
                changed_cites += 1
                return f"{stem}.md:{ns}-{ne}"
            if ns == start:
                return m.group(0)
            changed_cites += 1
            return f"{stem}.md:{ns}"

        out = CITATION.sub(sub, text)
        if out != text:
            changed_files += 1
            if apply:
                f.write_text(out, encoding="utf-8")
            print(f"  {'remapped' if apply else 'would remap'} {rel}")

    verb = "Remapped" if apply else "Would remap"
    print(f"{verb} {changed_cites} citation(s) across {changed_files} file(s).")
    return unresolved


def main(argv):
    apply = True
    if argv and argv[0] == "--check":
        apply, argv = False, argv[1:]
    if len(argv) < 2:
        print(__doc__.strip().split("Usage:")[1].strip(), file=sys.stderr)
        return 2
    unresolved = remap(argv[0], argv[1:], apply=apply)
    if unresolved:
        print("\nNeeds a decision — not rewritten:")
        for u in unresolved:
            print(f"  {u}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
