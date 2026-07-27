#!/usr/bin/env python3
"""Extract the claim set from an instruction file, and diff two versions of it.

Built for Phase 27, a compression pass over the instruction set. The problem it
solves is that compression is unverifiable by reading: whoever shortened the
text knows what it used to say, so re-reading it confirms nothing.

Two halves, and the split is the point.

EXACT -- backticked tokens (paths, commands, flags), numbers carrying a unit or
a threshold, severity keywords, headings, and cross-file references. These are
sets and compare as sets. A dropped instruction shows up as a set difference and
a reworded one does not, which is exactly the discrimination the pass needs.

COUNTED -- imperative sentences. These cannot be set-compared, because rewording
is the point of the pass, so they are counted per section and a decrease is a
finding to justify rather than a failure. Reported separately and never mixed
into the exact verdict: a check that claimed to be exact here would be the kind
of false confidence this project has already paid for.

    ./claims_inventory.py FILE                  print the inventory
    ./claims_inventory.py BEFORE AFTER          diff two files, exit 1 on loss
    ./claims_inventory.py --git REF FILE        diff FILE against REF's version

Exit 0 when the exact sets are equal, 1 when anything was lost, 2 on usage error.
Gaining a claim is reported and does not fail: adding an instruction is a real
edit, not a compression defect.
"""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

# `world/timeline.md`, `--check`, `chapter_load.py`, `§Ch13-Density-Cap`.
BACKTICKED = re.compile(r"`([^`\n]+)`")
# A number that carries meaning: a unit, a percentage, a comparison, an ordinal
# bound. A bare "one" or a year inside prose is not a claim; "≤5 named textures"
# and "exit 1" are.
NUMBER = re.compile(
    r"(?:(?<=[\s(])|^)(?:[≤≥<>]=?\s*)?\d+(?:[.,]\d+)?\s*"
    r"(?:%|x\b|px\b|words?\b|w\b|pp\b|pages?\b|chapters?\b|rows?\b|files?\b|"
    r"seconds?\b|minutes?\b|hours?\b|days?\b|k\b|KB\b|MB\b)",
    re.I)
SEVERITY = re.compile(r"\b(MUST NOT|MUST|NEVER|ALWAYS|HARD|BLOCKING|WARNING|NOTE|FAIL|OK|"
                      r"MANDATORY|REQUIRED|FORBIDDEN|BANNED)\b")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
CROSSREF = re.compile(r"(?:instructions/|scripts/)?([a-z0-9_-]+\.(?:md|py|sh|bats))")
# An imperative opens a line or a bullet with a bare verb. Deliberately loose:
# this half is counted, not compared, so a false positive costs nothing and a
# tight pattern would under-count the thing being watched.
IMPERATIVE = re.compile(
    r"^\s*(?:[-*]\s+|\d+\.\s+)?(?:\*\*)?(Read|Write|Run|Check|Verify|Load|Add|Remove|Delete|"
    r"Flag|Report|Route|Apply|Create|Open|Close|Skip|Stop|Use|Do NOT|Do not|Never|Always|"
    r"Set|Keep|Move|Replace|Compare|Extract|Count|List|Mark|Record|Confirm|Ensure|Emit)\b",
    re.M)


def strip_code_blocks(text):
    """Fenced blocks are examples, not claims, and their churn would swamp the diff."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def inventory(text):
    """{kind: set} for the exact half, plus {'imperatives': {section: count}}."""
    body = strip_code_blocks(text)
    exact = {
        "backticked": {m.strip() for m in BACKTICKED.findall(body)},
        "numbers": {" ".join(m.split()).lower() for m in NUMBER.findall(body)},
        "severity": set(SEVERITY.findall(body)),
        "headings": {h.strip() for h in HEADING.findall(body)},
        "crossrefs": set(CROSSREF.findall(body)),
    }
    # Occurrence counts, not just presence. The sets above catch the loss of the
    # LAST mention of a token and are blind to losing one of several -- found by
    # the negative test on 2026-07-27, where deleting an instruction that
    # referenced `chapter-writer.md` changed nothing because the file was
    # referenced elsewhere. Counted rather than failed: removing a redundant
    # repeat is exactly what this pass is for.
    tokens = Counter(m.strip() for m in BACKTICKED.findall(body))

    counts, section = {}, "(preamble)"
    for line in body.split("\n"):
        h = HEADING.match(line)
        if h:
            section = h.group(1).strip()
            counts.setdefault(section, 0)
            continue
        if IMPERATIVE.match(line):
            counts[section] = counts.get(section, 0) + 1
    return exact, counts, tokens


def _read(path):
    return Path(path).read_text(encoding="utf-8")


def _git_show(ref, path):
    out = subprocess.run(("git", "show", f"{ref}:{path}"), capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"claims-inventory: cannot read {path} at {ref}")
    return out.stdout


def report_one(path):
    exact, counts, _ = inventory(_read(path))
    print(f"CLAIMS — {path}")
    for kind in sorted(exact):
        print(f"  {kind:<12} {len(exact[kind])}")
    print(f"  {'imperatives':<12} {sum(counts.values())} across {len(counts)} sections")
    return 0


def diff(before_text, after_text, before_label, after_label):
    b_exact, b_counts, b_tok = inventory(before_text)
    a_exact, a_counts, a_tok = inventory(after_text)
    lost, gained = {}, {}
    for kind in b_exact:
        l = b_exact[kind] - a_exact[kind]
        g = a_exact[kind] - b_exact[kind]
        if l:
            lost[kind] = sorted(l)
        if g:
            gained[kind] = sorted(g)

    b_w, a_w = len(before_text.split()), len(after_text.split())
    pct = f"{(b_w - a_w) * 100 // b_w}%" if b_w else "0%"
    print(f"CLAIMS DIFF — {before_label} → {after_label}")
    print(f"  words {b_w} → {a_w}  ({pct} shorter)")

    if lost:
        print(f"\n  LOST — {sum(len(v) for v in lost.values())} claim(s) present before and absent after.")
        print("  Each is either an instruction that was dropped or a rewording that changed a token")
        print("  the reader keys on. Both need a verdict; neither is automatically fine.")
        for kind, items in sorted(lost.items()):
            print(f"    {kind}:")
            for it in items:
                print(f"      - {it}")
    else:
        print("\n  No exact claim was lost.")

    if gained:
        print(f"\n  GAINED — {sum(len(v) for v in gained.values())} claim(s), reported and not a failure.")
        for kind, items in sorted(gained.items()):
            print(f"    {kind}: {', '.join(items)}")

    thinned = [(k, b_tok[k], a_tok.get(k, 0)) for k in b_tok
               if 0 < a_tok.get(k, 0) < b_tok[k]]
    if thinned:
        print(f"\n  THINNED — {len(thinned)} token(s) still present but mentioned fewer times.")
        print("  Counted, not failed: dropping a redundant repeat is what this pass is for, and")
        print("  dropping the one mention that carried an instruction is not. Read the list.")
        for k, b, a in sorted(thinned, key=lambda x: x[1] - x[2], reverse=True)[:15]:
            print(f"    {b} → {a}  `{k}`")

    # The heuristic half, stated as heuristic.
    drops = [(s, b_counts[s], a_counts.get(s, 0)) for s in b_counts
             if a_counts.get(s, 0) < b_counts[s]]
    b_imp, a_imp = sum(b_counts.values()), sum(a_counts.values())
    print(f"\n  imperatives {b_imp} → {a_imp} (counted, not compared — rewording moves this legitimately)")
    if drops:
        print("  sections where the count fell, to be justified rather than failed:")
        for s, b, a in sorted(drops, key=lambda x: x[1] - x[2], reverse=True)[:12]:
            print(f"    {b:3d} → {a:3d}  {s[:80]}")
    return 1 if lost else 0


def main(argv):
    if len(argv) == 2:
        return report_one(argv[1])
    if len(argv) == 3:
        return diff(_read(argv[1]), _read(argv[2]), argv[1], argv[2])
    if len(argv) == 4 and argv[1] == "--git":
        ref, path = argv[2], argv[3]
        return diff(_git_show(ref, path), _read(path), f"{ref}:{path}", path)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
