#!/usr/bin/env python3
"""Deterministic register-leak linter — the reliable backbone of readability Category 0 (B-i).

Implements the *machine-checkable subset* of world/register-locks.md "Forbidden patterns":
the literal/regexpable tics that an LLM scan can (and demonstrably does) miss. The canonical
intent lives in register-locks.md; this script implements only the patterns that can be
matched deterministically. Semantic patterns (Mediterranean warmth leaking into the Dome,
measurement-substitution that erases POV agency) stay the LLM's job in readability Category 0.

Why this exists: a cold validation (project Phase 44 M3) showed the readability LLM Category-0
scan reported a Reality chapter "clean" while missing `the lines were the lines` (l.15) — which
a one-line grep caught instantly. Literal-pattern detection must not depend on an LLM.

Usage:
    register_leak_lint.py <chapter_file.md> --level {reality|ark|dome}

Exit code: 1 if any leak found (and prints each), 0 if clean.
"""
import argparse
import re
import sys

# "X was the X" stasis-tautology family. Forbidden in REALITY and ARK (it is the Dome's
# own signature, so NOT checked for Dome). Each tuple: (name, compiled regex).
# Anchored tight ("the <noun> ...") to keep false positives near zero; a `not` between the
# anchors disqualifies the match (e.g. "his voice was not the voice he had meant" — meaningful).
TAUTOLOGY_PATTERNS = [
    ("noun-repeat (the X was the X)",
     re.compile(r"\bthe (\w+) (?:was|were) (?:the |the same )?\1\b", re.IGNORECASE)),
    ("where-the-X stasis (the X was where the X)",
     re.compile(r"\bthe (\w+) (?:was|were) where the \1\b", re.IGNORECASE)),
    ("kept-its-X (the X kept its X)",
     re.compile(r"\bthe (\w+) kept its \1\b", re.IGNORECASE)),
    ("where-pronoun-had stasis (the X was where she/he/it had set/put/been …)",
     re.compile(r"\bthe \w+ (?:was|were) where (?:she|he|they|it) had "
                r"(?:set|put|left|placed|been)\b", re.IGNORECASE)),
]

# Compliance-system vocabulary: belongs to the Dome; a leak in REALITY or ARK.
COMPLIANCE_VOCAB = [
    "compliance nudge", "compliance pulse", "deniable band", "within parameters",
]

# Which deterministic checks apply per level. Dome has none here (its forbidden list is
# semantic — warmth, visible emotion — which the LLM handles).
LEVEL_CHECKS = {
    "reality": {"tautology": True, "vocab": True},
    "ark":     {"tautology": True, "vocab": True},
    "dome":    {"tautology": False, "vocab": False},
}


def lint(path, level):
    checks = LEVEL_CHECKS[level]
    hits = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if checks["tautology"]:
                for name, rx in TAUTOLOGY_PATTERNS:
                    for m in rx.finditer(line):
                        if " not " in m.group(0).lower():
                            continue  # meaningful negation, not a stasis tautology
                        hits.append((lineno, m.group(0).strip(), name))
            if checks["vocab"]:
                low = line.lower()
                for term in COMPLIANCE_VOCAB:
                    idx = low.find(term)
                    if idx != -1:
                        hits.append((lineno, line[idx:idx + len(term)], f"compliance vocab ({term})"))
    return hits


def main():
    ap = argparse.ArgumentParser(description="Deterministic register-leak linter (readability Category 0 backbone).")
    ap.add_argument("chapter", help="path to the chapter .md file")
    ap.add_argument("--level", required=True, choices=["reality", "ark", "dome"],
                    help="narrative level of this chapter (determines which forbidden patterns apply)")
    args = ap.parse_args()

    if not LEVEL_CHECKS[args.level]["tautology"] and not LEVEL_CHECKS[args.level]["vocab"]:
        print(f"register-leak-lint: level={args.level} has no deterministic patterns "
              f"(semantic checks are the LLM's job in readability Category 0). clean.")
        return 0

    hits = lint(args.chapter, args.level)
    if not hits:
        print(f"register-leak-lint: {args.chapter} (level={args.level}) — 0 hits, clean.")
        return 0
    for lineno, text, name in hits:
        print(f"LEAK {args.chapter}:{lineno}: \"{text}\"  [pattern: {name} — vs register-locks §{args.level}]")
    print(f"register-leak-lint: {len(hits)} hit(s) — each is a SAFE-CUT register breach. Rephrase to the level's register, preserving meaning.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
