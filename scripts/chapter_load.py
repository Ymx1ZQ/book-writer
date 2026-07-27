#!/usr/bin/env python3
"""Derived chapter-load view over the Usage Trackers.

The Usage Tracker (element -> chapter, living in the canon file that owns the
element) is the source of truth and this script never writes to it. What is
missing is the reverse view: "what does B2 Ch09 have to carry?" requires
grepping ~30 files, so planning is blind even though drafting is not. That is
how B2 Ch09 reached 109 pending elements without anyone noticing.

Capacity is measured, not assumed: it is derived from rows already marked
`written`, i.e. what chapters have actually carried in practice.

    ./chapter-load.py                 per-chapter load, overloaded first
    ./chapter-load.py --unassigned    rows with no chapter, grouped by file
    ./chapter-load.py --chapter B2:09 everything queued for one chapter
    ./chapter-load.py --free          Level-0 chapters with room, least-loaded first
    ./chapter-load.py --unreachable   rows whose owning file the target chapter never loads
    ./chapter-load.py --illegal-load  context entries a chapter's own Level bars it from loading
    ./chapter-load.py --orphans       rows still 'planned' on a drafted chapter
    ./chapter-load.py --written       rows marked 'written', for a verification pass
    ./chapter-load.py --book-form     rows whose Book cell is not B1/B2/B3
    ./chapter-load.py --stale         artifacts older than the prose they describe
    ./chapter-load.py --renumber      chapter slots whose title moved, and the rows they invalidate
    ./chapter-load.py --devplan-drift open items whose named files moved after them
    ./chapter-load.py --ownership     concept slugs claimed twice, by nobody, or off-table

Read-only. Safe to run at any time.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

def project_root():
    """The book project this run is about — never the directory holding the script.

    The script ships with the `book` skill (`instructions/registers.md` §Tools
    that compute reachability), so `Path(__file__).parent` is the skill's
    install directory and would make every mode scan the wrong tree. Order:
    an explicit `BOOK_PROJECT_ROOT`, then the git top level of the working
    directory, then the working directory itself.
    """
    env = os.environ.get("BOOK_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    top = subprocess.run(("git", "rev-parse", "--show-toplevel"),
                         capture_output=True, text=True)
    if top.returncode == 0 and top.stdout.strip():
        return Path(top.stdout.strip()).resolve()
    return Path.cwd().resolve()


ROOT = project_root()
# The canon directories `init.md` scaffolds. A skill convention, not project
# data: every project built by this skill has these three, and a project that
# grows a fourth canon directory changes the skill's layout, not a local list.
SCAN = ("world", "plot", "characters")
ROW = re.compile(r"^\|(?P<el>[^|]+)\|(?P<book>[^|]+)\|(?P<ch>[^|]+)\|(?P<detail>[^|]+)\|(?P<status>[^|]+)\|")
DASH = {"—", "--", "-", ""}
def book_dirs():
    """Every book in the project, from the directories that hold the chapters.

    Derived for the same reason `drafted_chapters()` is: a literal `{"B1", "B2",
    "B3"}` is correct until the day a fourth book exists, and then every mode
    keyed on it silently stops covering that book while reporting OK.
    """
    return sorted(p.name.split("-", 1)[1] for p in (ROOT / "chapters").glob("book-*")
                  if p.is_dir() and p.name.split("-", 1)[1].isdigit())


# The corpus form for the Book cell. Every mode keys on (book, chapter), so a
# bare "1" joins against no outline and the row falls out of every verdict
# instead of being judged wrong.
BOOK_NUMBERS = book_dirs()
BOOKS = {f"B{n}" for n in BOOK_NUMBERS}
BOOK_DIGIT = re.compile("[" + "".join(BOOK_NUMBERS) + "]") if BOOK_NUMBERS else re.compile(r"(?!)")


def book_form(book):
    """Classify a Book cell: "" if it is the corpus form, else why it is not.

    BARE   names one book without the B — `1` where the corpus writes `B1`.
    RANGE  names two books (`2-3`), so no single B-form applies and rewriting it
           is a content decision about which chapter owns the element. Phase 84
           normalized the singles in plot/key-scenes.md and left both ranges.
    """
    if book in DASH or book in BOOKS:
        return ""
    return "BARE" if len(set(BOOK_DIGIT.findall(book))) == 1 else "RANGE"

# Register rule, canonical in the project's canon-hierarchy §Level register rule
# and in the skill's `registers.md` §Level register. A chapter's `**Level:**`
# decides which level directory it may load; the others are a POV guard, not an
# omission. Everything outside the level directories (world/ root, plot/,
# characters/) is level-neutral.
#
# Read off the directory names rather than declared: `world/level-<n>-<name>/`
# is the layout `init.md` scaffolds, and the `<name>` segment is the same token
# the outline's `**Level:**` field uses. A project that adds a fourth level gets
# it for free; a hand-maintained map would keep reporting OK while every row in
# the new directory fell out of every verdict.
def level_dirs():
    """{level name: directory prefix}, and {level name: its number}."""
    found, order = {}, {}
    for p in sorted((ROOT / "world").glob("level-*-*")):
        if not p.is_dir():
            continue
        _, num, name = p.name.split("-", 2)
        key = name.replace("-", " ").title()
        found[key] = f"world/{p.name}/"
        if num.isdigit():
            order[key] = int(num)
    return found, order


LEVEL_DIRS, LEVEL_ORDER = level_dirs()
ALL_LEVEL_DIRS = tuple(LEVEL_DIRS.values())
# The base level — the one canon is written at before any level nests above it.
# `--free` ranks its chapters because that is where level-0 canon can land.
LEVEL_ZERO = next((k for k, v in sorted(LEVEL_ORDER.items(), key=lambda kv: kv[1])), "")

def drafted_chapters():
    """Every chapter with prose on disk, derived rather than declared.

    Not just the Level-0 ones: listing only the Reality chapters made the six
    Dome chapters look open, which is a trap — rows placed there become orphans
    the moment they are written.

    This was a hand-maintained literal (`{("B1", n) for n in range(1, 10)}`)
    until Phase 92. A constant nobody checks is the same defect this module's
    --stale mode exists to catch: the day Ch.10 is drafted, every verdict keyed
    on this set silently stops covering it, and the guard reports OK because it
    was never told the chapter exists. The prose on disk is the reproducible
    source, so read that.
    """
    found = set()
    for path in (ROOT / "chapters").glob("book-*/ch[0-9][0-9].md"):
        found.add(("B" + path.parent.name.split("-")[1], int(path.stem[2:])))
    return found


WRITTEN_CHAPTERS = drafted_chapters()

# --- staleness (Phase 92 M2) -------------------------------------------------
#
# run-merge-phase.sh runs the certification gates in order for a chapter it
# merges, so a chapter written by the pipeline is certified by construction. A
# prose edit made OUTSIDE that path -- which is what `/book revise` is -- has no
# such property, and until this guard nothing compared an artifact against the
# prose it was derived from. On 2026-07-26 a revise pass edited all nine drafted
# chapters and left every derived artifact in place; the condition was found by
# hand, weeks later.
#
# Keyed on the git commit, never on mtime: a clone or a checkout rewrites mtime
# and would report the whole corpus fresh.

# Per chapter, and blocking. The snapshot is the reader-memory ledger the next
# chapter is drafted from, so a stale one is wrong about what the reader knows.
SNAPSHOT = "chapters/coldread-state/{book_dir}-ch{ch:02d}.md"
# Written into a snapshot by `/book revise` when a prose edit invalidates it
# (skill `instructions/revise.md` §5.7). Authoritative: the tool that broke the
# file says so in the file.
STAMP = "STALE — do not consume."
# Per book, and report-only: these are overwritten per run and legitimately lag
# whichever chapter was certified last.
BOOK_ARTIFACTS = ("COLDREAD.md", "PROOFREAD.md", "REVIEW.md")


def _git(*argv):
    out = subprocess.run(("git",) + argv, cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def _commit_ts(rel):
    """Commit time of the last commit touching rel, or None if never committed."""
    ts = _git("log", "-1", "--format=%ct", "--", rel)
    return int(ts) if ts else None


def _dirty(rel):
    return bool(_git("status", "--porcelain", "--", rel))


def stale_rows():
    """(book, ch, kind, artifact, verdict) for every drafted chapter's artifacts.

    verdict is "" when the artifact is at least as new as the prose.

    Two independent signals, either one sufficient:

      STAMPED  the file says so itself -- `/book revise` wrote the marker into it
               when a prose edit invalidated it. Snapshots only.
      STALE    the prose was committed after the artifact was.

    The timestamp rule alone has a known false negative: a single commit touching
    prose and artifact together reads as fresh. That is CORRECT for SMELL.md,
    which `/book revise` updates in the same commit as the prose it applies, and
    it is wrong only for accidentally bundled commits -- which the stash-isolation
    rule in CLAUDE.md §Pipeline architecture notes already prohibits.

    It is NOT correct for snapshots, and Phase 92 M11 exists because that was
    missed: revise stamps a snapshot rather than regenerating it, so the
    invalidated file and the prose that invalidated it necessarily share a commit.
    The one case this guard exists to catch was the one case the timestamps could
    not see -- measured, a revise pass stamped ten snapshots and --stale exited 0.
    Hence the stamp, which outranks the timestamps for the files that carry one.
    """
    def verdict(prose_ts, art, read_stamp=False):
        path = ROOT / art
        if not path.exists():
            return "ABSENT"
        # The stamp outranks the timestamps. `/book revise` marks a snapshot
        # stale rather than regenerating it (skill Phase 25), so the invalidated
        # file and the prose that invalidated it necessarily land in one commit
        # and read as equal age -- the single case this guard exists to catch is
        # the one case the timestamp rule cannot see. Measured on 2026-07-26: a
        # revise pass stamped ten snapshots and --stale still exited 0.
        if read_stamp and STAMP in path.read_text(encoding="utf-8")[:2000]:
            return "STAMPED"
        art_ts = _commit_ts(art)
        return "STALE" if art_ts is None or prose_ts > art_ts else ""

    rows = []
    newest = {}          # book -> (timestamp, chapter) of its most recently edited prose
    for book, ch in sorted(WRITTEN_CHAPTERS):
        book_dir = f"book-{book[1:]}"
        prose = f"chapters/{book_dir}/ch{ch:02d}.md"
        if not (ROOT / prose).exists():
            continue
        # An uncommitted edit is newer than anything already committed, so it
        # makes the artifact stale before the commit lands rather than after.
        prose_ts = float("inf") if _dirty(prose) else _commit_ts(prose)
        if prose_ts is None:
            prose_ts = float("inf")   # prose on disk, never committed
        if prose_ts >= newest.get(book, (-1, 0))[0]:
            newest[book] = (prose_ts, ch)
        art = SNAPSHOT.format(book_dir=book_dir, ch=ch)
        rows.append((book, ch, "snapshot", art, verdict(prose_ts, art, read_stamp=True)))

    # Book-level artifacts are judged once per book, against the newest prose in
    # it. Judging them per chapter reports the same file up to nine times and
    # inflates a three-file lag into twenty-seven findings.
    for book, (prose_ts, ch) in sorted(newest.items()):
        book_dir = f"book-{book[1:]}"
        for name in BOOK_ARTIFACTS:
            art = f"chapters/{book_dir}/{name}"
            rows.append((book, ch, "book", art, verdict(prose_ts, art)))
    return rows


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _header_map(line):
    """Return a column map for a tracker header, or None if this is not one.

    The corpus uses four header shapes, not one: `Element|Book|Ch|Detail|Status`
    (279 tables), `Book|Ch|Detail|Status` (16), `Book|Ch|Level|Appearance` (11)
    and `Book|Ch|Scene|Page Cap` (1). Assuming the first shape made the other 28
    tables invisible to the planner — the same class of silent gap this tool
    exists to catch. Parse the header instead of assuming it.

    Tables whose second column is not Book are not trackers at all:
    `temporal-echoes.md`'s cross-substrate registry is `Anchor|Reality form|...`,
    where `—` means "no Reality-side form", not "unassigned".
    """
    cells = [c.lower().rstrip(".") for c in _cells(line)]
    if "book" not in cells or "ch" not in cells:
        return None
    m = {"book": cells.index("book"), "ch": cells.index("ch")}
    for name, keys in (("element", ("element",)), ("detail", ("detail", "level", "scene")),
                       ("status", ("status", "appearance", "page cap"))):
        for k in keys:
            if k in cells:
                m[name] = cells.index(k)
                break
    return m


def scan():
    """Yield (file, element, book, ch, detail, status) for every tracker row."""
    for sub in SCAN:
        for path in sorted((ROOT / sub).rglob("*.md")):
            if "archive" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if "<!-- No Usage Tracker" in text:
                # The file declares it holds no tracker. 26 files carry this marker
                # in thirteen wordings, all sharing that prefix: doctrine, structural
                # indexes, and background characters exempt per CLAUDE.md. Reading
                # them anyway is how plot/motif-tracking.md's eleven Book-first
                # tables — a motif placement index, not a set of commitments —
                # contributed 97 rows that no drafting could ever clear, because
                # those tables have no Status column and `Appearance` was mapped
                # onto status for want of one. The file said what it was; the
                # parser was not listening.
                continue
            cols = None
            for line in text.splitlines():
                if not line.lstrip().startswith("|"):
                    cols = None  # a table ends where the pipes stop
                    continue
                head = _header_map(line)
                if head:
                    cols = head
                    continue
                if not cols:
                    continue
                cells = _cells(line)
                if len(cells) <= max(cols["book"], cols["ch"]):
                    continue
                book = cells[cols["book"]]
                if set(book) <= {"-", ":", " "}:  # separator row
                    continue
                get = lambda k, d="": cells[cols[k]] if k in cols and cols[k] < len(cells) else d
                status = get("status", "planned")
                if status.lower() == "exempt":
                    # Explicit opt-out, per CLAUDE.md: background characters tagged
                    # "historical reference only" and process/reference files carry a
                    # single `| — | — | ... | exempt |` row instead of a tracker. It is
                    # a declaration that nothing here is meant to reach the page, not
                    # an unassigned element.
                    continue
                yield (path.relative_to(ROOT), get("element", "(unnamed row)"),
                       book, cells[cols["ch"]], get("detail"), status)


def key(book, ch):
    try:
        return (book, int(ch))
    except ValueError:
        return None


# --- the three loading mechanisms -------------------------------------------
#
# A chapter does not load only its `context:` list. Reachability is membership
# in the union of three sets, and a guard that knew only the first would call
# ~20 correctly-loaded files unreachable on its first run and be switched off.
# All three are read out of the book's own outline.md: a hardcoded copy here
# would be a fourth hand-maintained list, which is the defect this closes.

CTX_LINE = re.compile(r"^\*\*context:\*\*\s*(.+)$", re.I)
CH_HEAD = re.compile(r"^##\s*Ch\.\s*(\d+)")
# The whole Level field, up to the `|` that starts POV. Reading only the first
# word loses the declared secondary level of a cross-level chapter, and without
# it --illegal-load reports every authorized cross-level load as a finding.
LEVEL_LINE = re.compile(r"^\*\*Level:\*\*\s*([^|]+)")
# Built from the level directories, so the parser and the register rule cannot
# disagree about which words are levels. Longest first: a two-word level name
# must not be half-matched by a one-word one.
LEVEL_TOKEN = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in sorted(LEVEL_DIRS, key=len, reverse=True)) + r")\b"
) if LEVEL_DIRS else re.compile(r"(?!)")
# A level named OUTSIDE parentheses is co-primary: the chapter is equally at
# both levels and can carry either one's canon as a full scene. A level named
# inside parentheses is an incursion — a flash, an intercut, an edge-feed, a
# residue — and authorizes the load without opening a placement slot. The
# corpus keeps the two apart with punctuation and always has: `Ark + Reality`
# (B3 Ch.33, rotating POV) against `Ark (Reality residue)` (B3 Ch.31) and
# `Dome (Ark intercut + Reality edge-feed)` (B3 Ch.25). Note the second `+` is
# inside the parentheses, so the spans have to be stripped before the names are
# read, not the plus signs counted.
PARENTHETICAL = re.compile(r"\([^)]*\)")
ALWAYS_LINE = "**Always-loaded reference"
TEXTURE_LINE = "**Texture-palette proxy:"
MD_TOKEN = re.compile(r"[\w./-]+\.md")


class OutlineError(Exception):
    """A context entry that names no file, or more than one."""


def _split_context(text):
    """Split a `context:` list on the commas that separate entries.

    Entries carry trailing parentheticals and those parentheticals contain
    commas of their own, so splitting on every comma shreds the line into
    fragments that resolve to nothing. Track depth and split only at the top.
    """
    out, depth, cur = [], 0, []
    for c in text:
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        if c == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    out.append("".join(cur))
    return [e for e in (x.strip() for x in out) if e]


def _clean(entry):
    """Drop the trailing note and the backticks; keep the path."""
    return re.sub(r"\([^()]*\)\s*$", "", entry).strip().strip("`").strip()


def _md_files():
    return [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.md")
            if "archive" not in p.parts and not any(d.startswith(".") for d in p.parts)]


def _resolve(entry, index, where):
    """Map one context entry onto a repo-relative path.

    The same line mixes four styles — bare (`soundscapes.md`), level-relative
    (`level-0-reality/blocs.md`), repo-relative (`world/context-legal-doctrines.md`)
    and character paths. Try the path as written, then as a unique suffix.
    An entry that matches nothing, or more than one file, is a finding about the
    outline and is raised rather than skipped: swallowing it would silently drop
    a loading mechanism and turn every row in that file into a false MISSING.
    """
    if (ROOT / entry).is_file():
        return entry
    hits = [p for p in index if p.endswith("/" + entry)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise OutlineError(f"{where}: '{entry}' resolves to no file in the repo")
    raise OutlineError(f"{where}: '{entry}' is ambiguous — {', '.join(hits)}")


def outlines():
    """Parse per book: always-loaded set, texture-palette set, per-chapter level + context.

    Returns {book: {"always": set, "texture": set, "reality": [n, ...],
    "chapters": {n: (level, extra, set)}}}, where extra is the tuple of
    secondary levels the chapter declares and "reality" is the list of chapters
    at Level-0 as a full register (see PARENTHETICAL).
    Chapter keys are integers only; the Book 3 Epilogue carries a context list but
    no number, and tracker rows targeting it land in the non-numeric bucket, so
    there is nothing to join it against.
    """
    index = _md_files()
    books = {}
    for n in BOOK_NUMBERS:
        book = f"B{n}"
        path = ROOT / f"chapters/book-{n}/outline.md"
        always, texture, chapters, reality = set(), set(), {}, set()
        cur, level, extra = None, None, ()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(ALWAYS_LINE):
                # The list ends at the em dash; the prose after it names files
                # already in the list, sometimes by an ambiguous bare basename.
                head = line.split("—")[0]
                for tok in re.findall(r"`([^`]+\.md)`", head):
                    always.add(_resolve(tok, index, f"{book} always-loaded"))
            elif line.startswith(TEXTURE_LINE):
                # Reached transitively through writing-notes.md, which is itself
                # always-loaded. §Context Tags declares rows in these files valid
                # without per-chapter inclusion.
                for tok in MD_TOKEN.findall(line):
                    texture.add(_resolve(tok, index, f"{book} texture-palette"))
            head = CH_HEAD.match(line)
            if head:
                cur, level, extra = int(head.group(1)), None, ()
                continue
            if line.startswith("## "):
                cur = None
                continue
            if cur is None:
                continue
            lvl = LEVEL_LINE.match(line)
            if lvl:
                # The field names one level, or a primary plus the level the
                # chapter crosses into. Two forms are in use — `Dome (Ark flash
                # → Gate)` (B1 Ch.27) and `Ark + Reality` (B3 Ch.33) — so read
                # every level name in the field and treat the first as primary.
                # An unrecognized value is carried verbatim rather than dropped:
                # a level nobody modelled should surface as a finding, not pass.
                names = LEVEL_TOKEN.findall(lvl.group(1))
                level = names[0] if names else lvl.group(1).strip()
                extra = tuple(dict.fromkeys(names[1:]))
                if LEVEL_ZERO in LEVEL_TOKEN.findall(PARENTHETICAL.sub("", lvl.group(1))):
                    reality.add(cur)
                continue
            ctx = CTX_LINE.match(line)
            if ctx:
                files = {_resolve(_clean(e), index, f"{book} Ch{cur:02d} context")
                         for e in _split_context(ctx.group(1))}
                chapters[cur] = (level, extra, files)
        # Only chapters that also carry a context list: a `reality` entry with no
        # chapters[] row would offer a placement slot the join cannot reach.
        books[book] = {"always": always, "texture": texture, "chapters": chapters,
                       "reality": sorted(reality & set(chapters))}
    return books


def own_level_dir(path, level):
    """Does this file sit in the chapter's own level directory?

    If it does, the chapter reaches it whether or not the outline lists it:
    `chapter-writer.md` Step 1 loads that directory selectively, opening exactly
    the files whose tracker holds a row for this Book+Ch. The rule is derived
    rather than hand-maintained, so it cannot drift the way a context list can.

    Modelling it is not optional. Without this clause the guard reported 314
    unreachable rows in this corpus when 88 were unreachable; the other 226 sat
    in the chapter's own level directory and had always been loaded. Two
    independent passes then "corroborated" the inflated figure, because both
    asked the same wrong question — is the file in the context list — instead of
    asking whether the chapter reaches it.
    """
    want = LEVEL_DIRS.get(level)
    return bool(want) and path.startswith(want)


def legal_for(path, level):
    """Is this file loadable by a chapter at this level?

    world/ root, plot/ and characters/ are level-neutral. The three level
    directories are exclusive: a Dome chapter loading world/level-0-reality/
    would leak register, which the tracker row alone cannot authorize.
    """
    if not path.startswith(ALL_LEVEL_DIRS):
        return True
    want = LEVEL_DIRS.get(level)
    return bool(want) and path.startswith(want)


def level_of(path):
    """Which level directory this file sits in, or "" for the level-neutral rest."""
    for name, prefix in LEVEL_DIRS.items():
        if path.startswith(prefix):
            return name
    return ""


CH_HEAD = re.compile(r"^## Ch\. (\d+) — (.+?)(?:\s*\[|$)", re.M)


def renumbered(ref="HEAD"):
    """Chapter slots whose title moved to a different slot since `ref`.

    A tracker row keys on a chapter NUMBER. Renumbering a book silently
    re-points every row naming an affected slot, and nothing notices, because
    the row still names a real chapter -- the same failure shape as a stale line
    citation, one level up.

    Measured over this corpus's whole history, 2026-07-26: three renumbering
    events, not one. Book 1 shifted Ch.28-30 (096bf9d), Book 2 swapped Ch.14
    with Ch.15 (13ece5e), and Book 3 cascaded Ch.17 through Ch.33 down by one
    (c18e854). Only the Book 2 swap left stale rows -- 5 of them, all in
    level-neutral files where the register check cannot see them. Book 1's 35
    affected rows and Book 3's 409 were every one written AFTER their shift.

    That is timing, not safety. Both shifts landed before the trackers were
    populated. Book 1 is now drafted through Ch.09 and its rows are dense, so
    the same edit today would strand hundreds. Hence a detector that runs at the
    moment of the renumber, against the working tree, rather than an audit after
    the fact.

    A rename in place -- same chapter, new title -- is not reported. Only a
    title that appears at a different number than it did in `ref`, which is what
    invalidates rows.
    """
    out = []
    for book_dir in sorted((ROOT / "chapters").glob("book-*")):
        rel = f"chapters/{book_dir.name}/outline.md"
        before = _git("show", f"{ref}:{rel}")
        if not before:
            continue
        old = {int(n): t.strip() for n, t in CH_HEAD.findall(before)}
        new = {int(n): t.strip() for n, t in CH_HEAD.findall((ROOT / rel).read_text(encoding="utf-8"))}
        old_titles, new_titles = set(old.values()), set(new.values())
        moved = [n for n in sorted(set(old) & set(new))
                 if old[n] != new[n] and new[n] in old_titles and old[n] in new_titles]
        if moved:
            out.append(("B" + book_dir.name.split("-")[1], moved,
                        {n: (old[n], new[n]) for n in moved}))
    return out


def rows_naming(book, slots):
    """Every tracker row in the corpus naming one of these chapter slots."""
    pat = re.compile(r"\| %s \| (%s) \|" % (book, "|".join(f"{n:02d}" for n in slots)))
    hits = []
    for f in sorted(ROOT.rglob("*.md")):
        s = f.relative_to(ROOT).as_posix()
        if s.startswith(".git") or "/archive/" in s:
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").split("\n"), 1):
            if pat.search(line):
                hits.append((s, i, line.strip()))
    return hits


DEVPLAN = "DEVPLAN.md"
OPEN_ITEM = re.compile(r"^- \[ \]")
# Repo-relative paths as the devplan writes them. Matched INSIDE a backtick span
# rather than as the whole span: the corpus writes `./chapter-load.py --stale`
# and `chapters/book-2/outline.md:337` as often as a bare path, and requiring the
# span to be exactly a path left 14 of 15 items unjudgeable on the first run --
# the check under-reporting in precisely the way its own docstring warns about.
BACKTICKED = re.compile(r"`([^`]+)`")
PATHLIKE = re.compile(r"(?:\./)?((?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_.-]+\.(?:md|py|sh|bats))")


def devplan_drift():
    """Open items whose named files were committed after the item was written.

    The close-out failure is mechanical, not attentional: the work is done, often
    by a subagent, then committed, and the tick is a separate edit to a different
    file that forms no part of the work's own completion signal. Nothing
    recouples them, so an item finishes and its box does not follow.

    Measured 2026-07-26: nine such items, four inherited from Phases 87 and 88
    and five produced during Phase 95 -- the phase whose subject was that exact
    defect. The rule is stated in `~/.claude/CLAUDE.md` rule 1 and enforced by
    nothing; forge-flow's loop ends at commit and never ticks; no hook exists.

    The signal: `git blame` dates the item's own line, `git log` dates each file
    it names. A named file newer than the item is evidence the work landed.

    Advisory by construction. Whether an item is actually complete is a judgment
    the dates cannot make -- a file can move for an unrelated reason -- so this
    reports and never fails. Same reasoning `--check` applies to CONFLICT: a
    guard that fails the build gets switched off during the work that resolves it.
    """
    blame = _git("blame", "--line-porcelain", "--", DEVPLAN)
    items, ts = [], None
    for line in blame.split("\n"):
        if line.startswith("author-time "):
            ts = int(line.split()[1])
        elif line.startswith("\t"):
            text = line[1:]
            if OPEN_ITEM.match(text):
                items.append((ts, text))
    flagged, unjudgeable = [], 0
    for item_ts, text in items:
        found = []
        for span in BACKTICKED.findall(text):
            found.extend(PATHLIKE.findall(span))
        paths = [p for p in dict.fromkeys(found) if (ROOT / p).exists()]
        if not paths:
            unjudgeable += 1
            continue
        newer = []
        for rel in paths:
            fts = _commit_ts(rel)
            if fts and item_ts and fts > item_ts:
                newer.append((rel, fts))
        if newer:
            flagged.append((item_ts, text, newer))
    return flagged, unjudgeable, len(items)


TABLE_HEADER = re.compile(r"^\|\s*Element\s*\|\s*Book\s*\|\s*Ch\s*\|")
TABLE_SEP = re.compile(r"^\|[\s|:-]+\|\s*$")


def malformed_rows():
    """Lines sitting inside a Usage Tracker table that are not well-formed rows.

    `ROW` matches five pipe-delimited cells and every mode silently skips what it
    does not match, so a row that is damaged does not become a malformed row --
    it stops existing. Counts drop by one across every mode and every mode still
    reports success.

    Found by causing it on 2026-07-27: an applier script treated the sentinel
    `unchanged` as literal replacement text and overwrote eleven tracker rows
    with that word. Nothing failed. The damage surfaced only because the chapter
    load came out at 3 against a plan that predicted 14.

    A table is entered at its `| Element | Book | Ch |` header and left at the
    first line that is neither a pipe row nor blank-inside-the-block; between
    those, anything that is not a pipe row of the right shape is damage.
    """
    bad = []
    for base in SCAN:
        for f in sorted((ROOT / base).rglob("*.md")):
            rel = f.relative_to(ROOT).as_posix()
            if "/archive/" in rel:
                continue
            inside = False
            for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                if TABLE_HEADER.match(line):
                    inside = True
                    continue
                if not inside:
                    continue
                if not line.strip():
                    inside = False
                    continue
                if TABLE_SEP.match(line) or ROW.match(line):
                    continue
                # A continuation of prose after the table without a blank line is
                # possible, but a line starting with `|` inside a table is always
                # meant to be a row, and a bare word never is.
                bad.append((rel, n, line.strip()[:110]))
                inside = line.startswith("|")
    return bad


# --- single ownership -------------------------------------------------------
#
# A project that scaffolds an information architecture states one rule -- each
# concept has one canonical file, everything else cross-references -- and then
# verifies nothing. A second explanation accretes in a neighbouring file and
# drifts, and every other check here passes, because each file is internally
# consistent. Three defects of that shape were found by hand in `ground-truth`
# on 2026-07-27, all late.
#
# This half is mechanical: who claims what. The judgment half -- whether a
# non-owner *explains* a concept instead of pointing at its owner -- is
# `coherence-check.md` check U, and no static check can do it.

OWNS_TABLE = re.compile(r"^\|\s*Concept\s*\|\s*Slug\s*\|\s*Canonical file\s*\|", re.I)
OWNS_FIELD = re.compile(r"^owns:\s*\[([^\]]*)\]\s*$", re.M)
BACKTICKED_CELL = re.compile(r"`([^`]+)`")
# `characters/<char>.md`, `chapters/book-N/outline.md`, `plot/episode-N.md`: the
# cell names a shape, not a file. Ownership there is per character or per book,
# which is a convention rather than an owner, so it is reported as uncovered
# instead of being faked with twenty files claiming one slug.
PATTERN_CELL = re.compile(r"<[^>]+>|\bbook-N\b|\bepisode-N\b")


def ownership_table():
    """[(slug, canonical cell, is_pattern)] from the project's own concept table.

    Read from the project at run time and never held here: a copy in the tool
    would be the second source of truth this check exists to find.
    """
    rows = []
    for name in ("CLAUDE.md", "README.md", "AGENTS.md"):
        path = ROOT / name
        if not path.is_file():
            continue
        inside = False
        for line in path.read_text(encoding="utf-8").split("\n"):
            if OWNS_TABLE.match(line):
                inside = True
                continue
            if not inside:
                continue
            if not line.startswith("|"):
                inside = False
                continue
            if TABLE_SEP.match(line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            slug = BACKTICKED_CELL.search(cells[1])
            if not slug:
                continue
            rows.append((slug.group(1), cells[2], bool(PATTERN_CELL.search(cells[2]))))
        if rows:
            break
    return rows


def ownership_claims():
    """{slug: [file, ...]} from every `owns:` frontmatter block in the project."""
    claims = defaultdict(list)
    for f in sorted(ROOT.rglob("*.md")):
        rel = f.relative_to(ROOT).as_posix()
        if "archive" in f.parts or any(d.startswith(".") for d in f.parts):
            continue
        head = f.read_text(encoding="utf-8").split("\n---", 1)
        if not head[0].startswith("---\n"):
            continue
        m = OWNS_FIELD.search(head[0])
        if not m:
            continue
        for slug in (s.strip().strip("`") for s in m.group(1).split(",")):
            if slug:
                claims[slug].append(rel)
    return claims


def ownership():
    """(table, claims, findings) -- findings are (kind, slug, detail)."""
    table = ownership_table()
    claims = ownership_claims()
    listed = {slug for slug, _, _ in table}
    findings = []
    for slug, cell, is_pattern in table:
        who = claims.get(slug, [])
        if is_pattern:
            continue
        if len(who) > 1:
            findings.append(("DUPLICATE", slug, ", ".join(who)))
            continue
        if not who:
            findings.append(("UNCLAIMED", slug, cell))
            continue
        named = BACKTICKED_CELL.search(cell)
        if named and named.group(1) != who[0]:
            findings.append(("MISPLACED", slug, f"table says {named.group(1)}, claimed by {who[0]}"))
    for slug, who in sorted(claims.items()):
        if slug not in listed:
            findings.append(("STRAY", slug, ", ".join(who)))
    return table, claims, findings


def illegal_loads(books):
    """(book, ch, level, extra, path, barred_level) for every context entry the level bars.

    The CONFLICT verdict seen from the loading side. `--unreachable` asks whether
    a tracker row's file is reachable from its chapter; this asks whether the
    chapter's `context:` list names a file its own `**Level:**` locks it out of.
    Neither question catches the other, and the gap is not incidental: `_reach`
    returns as soon as the file appears in the context list, so adding the file
    there SILENCES the CONFLICT verdict instead of resolving it. Measured on this
    corpus 2026-07-26: of the ten entries reported here, eight are backed by a
    tracker row in the barred file naming that exact chapter and a ninth by a row
    whose Ch cell names two (`25/28`, so it keys to neither). --unreachable
    reports none of the ten.

    The failure it catches is quiet by construction. An unreachable row is canon
    that never arrives and the guard says so; an illegally loaded file is canon
    that arrives where the POV cannot perceive it, and the writer opens it
    because the outline told them to.

    A chapter that genuinely crosses levels declares the second level in its own
    `**Level:**` field, and loads that declaration authorizes are exempt. The
    declaration has to be read from the field and nowhere else: inferring the
    secondary level from the context list would make the check answer itself.
    """
    rows = []
    for book in sorted(books):
        for ch, (level, extra, context) in sorted(books[book]["chapters"].items()):
            for rel in sorted(context):
                if legal_for(rel, level) or any(legal_for(rel, x) for x in extra):
                    continue
                rows.append((book, ch, level, extra, rel, level_of(rel)))
    return rows


class Join:
    """The one join every mode reads.

    `--check`, `--orphans`, `--written` and `--unreachable` answer four
    questions about the same tracker-row-to-chapter relation. Deriving it once
    is what keeps a mode from disagreeing with the count `--check` prints.
    """

    def __init__(self, rows, books):
        self.planned, self.written = defaultdict(list), defaultdict(list)
        self.unassigned = defaultdict(list)
        self.nonnumeric, self.unreachable, self.offoutline = [], defaultdict(list), []
        self.bookform = []
        for path, el, book, ch, detail, status in rows:
            form = book_form(book)
            if form:
                # Wrong form, not a missing assignment: the row names a book and
                # names it in a shape nothing joins on.
                self.bookform.append((form, path, el, book, ch))
            if book in DASH or ch in DASH:
                # genuinely unassigned: no chapter has been chosen yet
                self.unassigned[path].append((el, detail, status))
                continue
            k = key(book, ch)
            if k is None:
                # a chapter IS named but not as a bare integer (ranges, "Epilogue").
                # Assigned, just not countable per-chapter — never report as unassigned.
                self.nonnumeric.append((path, el, book, ch))
                continue
            (self.written if status == "written" else self.planned)[k].append((path, el, detail))
            self._reach(k, path, el, detail, status, books)
        # Measured capacity: mean rendered rows per drafted chapter.
        self.cap = (round(sum(len(v) for v in self.written.values()) / len(self.written))
                    if self.written else 25)
        # A chapter counts as drafted once it carries at least one rendered row;
        # rows still 'planned' there are canon the draft went past.
        self.orphans = {k: v for k, v in self.planned.items() if k in self.written}

    def _reach(self, k, path, el, detail, status, books):
        book, ch = k
        spec = books.get(book)
        if not spec or ch not in spec["chapters"]:
            # The row names a chapter this book's outline does not declare.
            # Nothing to compare it against — report the count, judge nothing.
            self.offoutline.append((path, el, book, ch))
            return
        level, extra, context = spec["chapters"][ch]
        rel = path.as_posix()
        if rel in context or rel in spec["always"] or rel in spec["texture"]:
            return
        # A declared cross-level chapter counts as being at every level it
        # declares, in BOTH directions. --illegal-load honored `extra` from the
        # start and this side did not, which made the two checks disagree about
        # the same field: declaring B3 Ch.25 `Dome (Ark intercut + Reality
        # edge-feed)` cleared its ILLEGAL-LOAD and left the Reality rows it
        # authorizes still reported CONFLICT here. Closing one direction opened
        # the other, measured 2026-07-26 when CONFLICT rose while ILLEGAL-LOAD
        # reached zero.
        levels = (level,) + tuple(extra)
        if any(own_level_dir(rel, x) for x in levels):
            return  # reached by the selective level-directory load, not the list
        verdict = "MISSING" if any(legal_for(rel, x) for x in levels) else "CONFLICT"
        self.unreachable[k].append((verdict, path, el, detail, status, level))

    def counts(self, verdict):
        return sum(1 for v in self.unreachable.values() for r in v if r[0] == verdict)

    def rows_in(self, book, ch, rel):
        """Tracker rows in `rel` that commit this chapter to render something.

        What decides an ILLEGAL-LOAD triage: a barred file that also holds a row
        naming this chapter is an authored cross-level beat missing its
        declaration, while one with no row is background the POV cannot perceive.
        Rows whose Ch cell names two chapters (`25/28`) key to neither and are
        counted here as zero — they sit in the non-numeric bucket, which is a
        separate defect in the row rather than evidence about the load.
        """
        k = (book, ch)
        return sum(1 for bucket in (self.planned, self.written)
                   for path, _, _ in bucket.get(k, ()) if path.as_posix() == rel)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unassigned", action="store_true")
    ap.add_argument("--chapter")
    ap.add_argument("--free", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="pipeline guard: exit 1 on unassigned rows, orphans on drafted "
                         "chapters, or unreachable-MISSING rows")
    ap.add_argument("--unreachable", action="store_true",
                    help="rows whose owning file the target chapter never loads")
    ap.add_argument("--illegal-load", action="store_true",
                    help="context entries a chapter's own Level bars it from loading")
    ap.add_argument("--devplan-drift", action="store_true",
                    help="open devplan items whose named files moved after the item was written")
    ap.add_argument("--ownership", action="store_true",
                    help="concept slugs claimed twice, claimed by nobody, or claimed off-table")
    ap.add_argument("--renumber", nargs="?", const="HEAD", metavar="REF",
                    help="chapter slots whose title moved since REF (default HEAD), "
                         "and the tracker rows those slots invalidate")
    ap.add_argument("--orphans", action="store_true",
                    help="rows still 'planned' on a chapter already drafted")
    ap.add_argument("--written", action="store_true",
                    help="rows marked 'written', for a fidelity verification pass")
    ap.add_argument("--book-form", action="store_true",
                    help="rows whose Book cell is not B1/B2/B3")
    ap.add_argument("--stale", action="store_true",
                    help="derived artifacts older than the prose they describe")
    args = ap.parse_args()

    if args.stale:
        rows = stale_rows()
        bad_snap = [r for r in rows if r[2] == "snapshot" and r[4]]
        bad_book = [r for r in rows if r[2] == "book" and r[4]]
        n_ch = len({(r[0], r[1]) for r in rows})
        print(f"STALENESS — {n_ch} drafted chapters, artifacts compared against their prose.")
        print("A chapter merged by run-merge-phase.sh is certified by construction. A prose")
        print("edit made outside that path is not, and the artifacts derived from it stay on")
        print("disk looking current. Keyed on the git commit, not mtime: a checkout rewrites")
        print("mtime and would report everything fresh.\n")
        if bad_snap:
            n_stamped = sum(1 for r in bad_snap if r[4] == "STAMPED")
            how = f"{len(bad_snap)} reader-state snapshots are unusable"
            if n_stamped:
                how += f" ({n_stamped} stamped by the pass that invalidated them)"
            print(f"  FAIL  {how}.")
            print("        The snapshot is what the NEXT chapter is drafted from, so a stale")
            print("        one is wrong about what the reader knows. Regenerate ascending")
            print("        (/book snapshot <book> chNN) — reader-state is cumulative.")
            for book, ch, _, art, verdict in bad_snap:
                print(f"          {book} Ch{ch:02d}  {verdict:<6}  {art}")
        if bad_book:
            print(f"  WARN  {len(bad_book)} book-level artifacts older than a chapter they cover.")
            print("        Overwritten per run, so these legitimately lag the last chapter")
            print("        certified. Report-only; read the list, do not gate on it.")
            for book, ch, _, art, verdict in bad_book:
                print(f"          {book} Ch{ch:02d}  {verdict:<6}  {art}")
        if not bad_snap:
            print("  OK    every drafted chapter's snapshot is at least as new as its prose.")
            return 0
        return 1

    try:
        books = outlines()
    except OutlineError as exc:
        print(f"outline parse failure — {exc}", file=sys.stderr)
        print("A context entry that names no file is a defect in the outline, not a "
              "parse detail to skip: every row in that file would read as unreachable.",
              file=sys.stderr)
        return 2

    j = Join(scan(), books)
    planned, written, unassigned = j.planned, j.written, j.unassigned
    nonnumeric, cap = j.nonnumeric, j.cap

    if args.unassigned:
        total = sum(len(v) for v in unassigned.values())
        print(f"UNASSIGNED — {total} rows with no chapter. These are invisible to drafting:")
        print("the chapter-writer loads a canon file only if that file has a row for the")
        print("chapter being written, so a row left at '—' may never reach the page.\n")
        for path in sorted(unassigned, key=lambda p: -len(unassigned[p])):
            print(f"  {path}  ({len(unassigned[path])})")
            for el, detail, _ in unassigned[path]:
                print(f"      [{detail:^6}] {el[:96]}")
            print()
        return

    if args.chapter:
        book, _, ch = args.chapter.partition(":")
        k = (book, int(ch))
        items = planned.get(k, [])
        done = written.get(k, [])
        print(f"{book} Ch{int(ch):02d} — {len(items)} pending, {len(done)} rendered "
              f"(measured capacity ~{cap})\n")
        by_file = defaultdict(list)
        for path, el, detail in items:
            by_file[path].append((el, detail))
        for path in sorted(by_file):
            print(f"  {path}")
            for el, detail in by_file[path]:
                print(f"      [{detail:^6}] {el[:96]}")
        return

    if args.unreachable:
        n_miss, n_conf = j.counts("MISSING"), j.counts("CONFLICT")
        print(f"UNREACHABLE — {n_miss + n_conf} rows whose owning file the target chapter "
              f"never loads ({n_miss} MISSING, {n_conf} CONFLICT).")
        print("A tracker row says 'this element belongs in B1 Ch07'; the chapter's context")
        print("list decides what B1 Ch07 loads. Where they disagree the row is dead: the")
        print("element cannot reach the page because the writer never opens the file.\n")
        print("  MISSING   the file is legal for the chapter's level — add it to the context list.")
        print("  CONFLICT  the file is level-locked away from the chapter. Either the row targets")
        print("            the wrong chapter or the content sits in the wrong file. Never")
        print("            auto-resolved: the register outranks the tracker.\n")
        for k in sorted(j.unreachable):
            book, ch = k
            rows = j.unreachable[k]
            level = rows[0][5]
            miss = sum(1 for r in rows if r[0] == "MISSING")
            print(f"  {book} Ch{ch:02d}  ({level}) — {miss} MISSING, {len(rows) - miss} CONFLICT")
            by_file = defaultdict(list)
            for verdict, path, el, detail, status, _ in rows:
                by_file[(verdict, path)].append((el, detail, status))
            for verdict, path in sorted(by_file, key=lambda x: (x[0], str(x[1]))):
                items = by_file[(verdict, path)]
                print(f"      {verdict:8s} {path}  ({len(items)})")
                for el, detail, status in items:
                    print(f"          [{status:^8}] {el[:88]}")
            print()
        if j.offoutline:
            print(f"  {len(j.offoutline)} rows target a chapter the outline does not declare; "
                  f"not judged.")
        return 0

    if args.illegal_load:
        rows = illegal_loads(books)
        n_cross = sum(1 for spec in books.values()
                      for _, extra, _ in spec["chapters"].values() if extra)
        print(f"ILLEGAL-LOAD — {len(rows)} context entries a chapter's own Level bars it "
              f"from loading.")
        print("--unreachable asks whether a tracker row's file is reachable from its chapter.")
        print("This asks the reverse, and the two do not overlap: _reach stops as soon as the")
        print("file is in the context list, so listing a level-barred file there silences the")
        print("CONFLICT verdict rather than resolving it. Every entry below is invisible to")
        print("--unreachable, and the writer opens the file because the outline named it.\n")
        print("  Cross-level chapters declare the second level in their own `**Level:**` field")
        print(f"  — a primary level, then every further level name in the same field, whether")
        print(f"  joined (`A + B`) or parenthesized (`A (B flash)`). {n_cross} chapters do; the loads")
        print("  those declarations authorize are exempt and not listed.\n")
        print("  The rightmost column is the triage: a barred file that also holds tracker rows")
        print("  for this chapter is an authored cross-level beat whose `**Level:**` never")
        print("  declared it. One with none is background the POV cannot perceive.\n")
        by_ch = defaultdict(list)
        for book, ch, level, extra, rel, barred in rows:
            by_ch[(book, ch, level, extra)].append((rel, barred))
        for book, ch, level, extra in sorted(by_ch):
            declared = level + (f" + {'/'.join(extra)}" if extra else "")
            entries = by_ch[(book, ch, level, extra)]
            print(f"  {book} Ch{ch:02d}  ({declared}) — {len(entries)} "
                  f"{'entry' if len(entries) == 1 else 'entries'}")
            for rel, barred in entries:
                n = j.rows_in(book, ch, rel)
                claim = (f"{n} tracker row{'' if n == 1 else 's'} names this chapter"
                         if n else "no tracker row here")
                print(f"      {barred:<8} {rel}  ({claim})")
            print()
        # Book-wide loads, listed and not counted. The always-loaded paragraph is
        # book-scoped, so a level directory promoted into it loads for every
        # chapter of the book including the two thirds its level bars. That is a
        # promotion decision argued in the outline's own paragraph, not a
        # per-chapter context entry, so it is not the same finding.
        wide = [(book, rel) for book in sorted(books)
                for rel in sorted(books[book]["always"] | books[book]["texture"])
                if level_of(rel)]
        if wide:
            print(f"  {len(wide)} level-directory files sit in a book-wide always-loaded set "
                  f"rather than any")
            print("  chapter's context list, so they load for every chapter of that book. Listed, "
                  "not counted:")
            for book, rel in wide:
                print(f"      {book}  {level_of(rel):<8} {rel}")
        return 0

    if args.ownership:
        table, claims, findings = ownership()
        if not table:
            print("OWNERSHIP — no `| Concept | Slug | Canonical file |` table in the project.")
            print("This check reads the project's own concept table at run time and holds no")
            print("copy, so with no table there is nothing to check. Add one to CLAUDE.md.")
            return 0
        patterns = [(s, c) for s, c, p in table if p]
        print(f"OWNERSHIP — {len(table)} concepts declared, {len(findings)} finding(s).")
        print("Each concept has one canonical file and every other file cross-references it.")
        print("This half is who claims what; whether a non-owner *explains* a concept instead")
        print("of pointing at its owner is coherence-check.md check U, which is a judgment.\n")
        print("  DUPLICATE  two files claim the slug — one is the owner, the other must point at it.")
        print("  UNCLAIMED  the table names a concept no file declares in `owns:`.")
        print("  MISPLACED  the claimant is not the file the table names.")
        print("  STRAY      a file claims a slug the table does not list.\n")
        for kind, slug, detail in findings:
            print(f"  {kind:<10} {slug}")
            print(f"             {detail}")
        if patterns:
            print(f"\n  {len(patterns)} row(s) name a pattern rather than a file and are NOT covered.")
            print("  Ownership there is per character or per book — a convention, not an owner.")
            print("  Listed rather than faked: a slug claimed by twenty files is not ownership.")
            for slug, cell in patterns:
                print(f"      {slug:<28} {cell}")
        return 1 if findings else 0

    if args.devplan_drift:
        import datetime
        flagged, unjudgeable, total = devplan_drift()
        d = lambda s: datetime.datetime.fromtimestamp(s).strftime("%Y-%m-%d")
        print(f"DEVPLAN-DRIFT — {len(flagged)} of {total} open item(s) name a file that was "
              f"committed after the item was written.")
        print("Evidence that the work landed and the box did not follow. Advisory: whether an")
        print("item is complete is a judgment these dates cannot make, so this never fails.")
        if unjudgeable:
            print(f"  {unjudgeable} item(s) name no file and are NOT judged — stated rather than")
            print("  dropped, because a check that silently ignores what it cannot see is the")
            print("  defect it was built to catch.")
        for item_ts, text, newer in flagged:
            print()
            print(f"  item written {d(item_ts)}")
            print(f"    {text[:150]}")
            for rel, fts in newer:
                print(f"      {rel} last committed {d(fts)}")
        return 0

    if args.renumber:
        events = renumbered(args.renumber)
        if not events:
            print(f"RENUMBER — no chapter title moved slots since {args.renumber}.")
            return 0
        total = 0
        print(f"RENUMBER — {len(events)} book(s) where a chapter title moved to a different "
              f"slot since {args.renumber}.")
        print("A tracker row keys on the chapter NUMBER, so every row naming an affected slot")
        print("now points at different content. It does not fail: the row still names a real")
        print("chapter. Measured over this corpus's history — three such events, and only the")
        print("Book 2 swap left stale rows, because the other two landed before the trackers")
        print("were populated. That is timing, not safety.")
        for book, slots, titles in events:
            print()
            print(f"  {book} — slots {', '.join(f'Ch.{n:02d}' for n in slots)}")
            for n in slots:
                was, now = titles[n]
                print(f"      Ch.{n:02d}  {was!r} -> {now!r}")
            rows = rows_naming(book, slots)
            total += len(rows)
            print(f"      {len(rows)} tracker row(s) name these slots and need re-checking:")
            for rel, ln, text in rows[:40]:
                print(f"        {rel}:{ln}  {text[:96]}")
            if len(rows) > 40:
                print(f"        ... and {len(rows) - 40} more")
        return 1 if total else 0

    if args.orphans:
        n_or = sum(len(v) for v in j.orphans.values())
        print(f"ORPHANS — {n_or} rows still 'planned' on chapters already drafted.")
        print("The draft went past them. Each is either an element the chapter should have")
        print("carried and did not, or a row that belongs on a later chapter.\n")
        for k in sorted(j.orphans, key=lambda x: -len(j.orphans[x])):
            book, ch = k
            by_file = defaultdict(list)
            for path, el, detail in j.orphans[k]:
                by_file[path].append((el, detail))
            print(f"  {book} Ch{ch:02d}  ({len(j.orphans[k])} never rendered)")
            for path in sorted(by_file):
                print(f"      {path}  ({len(by_file[path])})")
                for el, detail in by_file[path]:
                    print(f"          [{detail:^6}] {el[:88]}")
            print()
        return 0

    if args.written:
        n_w = sum(len(v) for v in written.values())
        print(f"WRITTEN — {n_w} rows marked 'written' across {len(written)} drafted chapters.")
        print("A 'written' mark is an assertion that the element reached the prose. No static")
        print("join can confirm it; this lists the rows so /book fidelity has something to")
        print("check against the page rather than a count.\n")
        for k in sorted(written):
            book, ch = k
            by_file = defaultdict(list)
            for path, el, detail in written[k]:
                by_file[path].append((el, detail))
            print(f"  {book} Ch{ch:02d}  ({len(written[k])} rendered)")
            for path in sorted(by_file):
                print(f"      {path}  ({len(by_file[path])})")
                for el, detail in by_file[path]:
                    print(f"          [{detail:^6}] {el[:88]}")
            print()
        return 0

    if args.book_form:
        bare = [r for r in j.bookform if r[0] == "BARE"]
        ranges = [r for r in j.bookform if r[0] == "RANGE"]
        print(f"BOOK-FORM — {len(bare)} rows whose Book cell is not B1, B2 or B3.")
        print("The header parser reads whichever column the table calls Book, so this covers")
        print("every table shape in the corpus, including the eleven that put Book first. A")
        print("row in the wrong form keys against no outline: it matches no chapter and is")
        print("dropped from the unreachable, orphan and capacity verdicts without comment.\n")
        for _, path, el, book, ch in bare:
            print(f"      [{book:^6}] {path}  Ch{ch}  {el[:80]}")
        if ranges:
            print(f"  {len(ranges)} rows name two books rather than one, so no single B-form "
                  f"applies. Listed, not counted:")
            for _, path, el, book, ch in ranges:
                print(f"      [{book:^6}] {path}  Ch{ch}  {el[:80]}")
        return 0

    if args.check:
        # Three silent failure modes, all invisible to the existing pipeline.
        n_un = sum(len(v) for v in unassigned.values())
        orphans = {k: len(v) for k, v in j.orphans.items()}
        n_or = sum(orphans.values())
        n_miss, n_conf = j.counts("MISSING"), j.counts("CONFLICT")
        print(f"tracker check — capacity ~{cap}/chapter")
        if n_un:
            print(f"  FAIL  {n_un} rows have no chapter. Canon that no chapter will load.")
        if orphans:
            print(f"  FAIL  {n_or} rows still 'planned' on chapters already drafted:")
            for (book, ch), n in sorted(orphans.items(), key=lambda x: -x[1]):
                print(f"          {book} Ch{ch:02d}  {n} never rendered")
        if n_miss:
            # Same loss the two failures above catch: canon that never reaches a
            # reader. Here the row is assigned and the chapter simply does not
            # load the file that holds it.
            print(f"  FAIL  {n_miss} rows unreachable-MISSING: the owning file is legal for the "
                  f"chapter's level but absent from its context list (run --unreachable).")
        bad = malformed_rows()
        if bad:
            # FAIL rather than WARN, and unlike CONFLICT this is not a content
            # judgment waiting on a human: the file has been damaged. `ROW` skips
            # what it cannot match, so a destroyed row does not read as malformed
            # -- it stops existing, every count drops by one, and every mode still
            # reports success. Eleven rows were overwritten this way on
            # 2026-07-27 and nothing failed.
            print(f"  FAIL  {len(bad)} malformed line(s) inside a Usage Tracker table — a damaged "
                  f"row is invisible to every other mode, so this is the only place it surfaces:")
            for rel, n, text in bad[:10]:
                print(f"          {rel}:{n}  {text}")
            if len(bad) > 10:
                print(f"          ... and {len(bad) - 10} more")
        if n_conf:
            # A warning, not a failure: resolving one means moving content between
            # files, a human decision. A guard that failed here would be switched
            # off for the duration of exactly the work that fixes it.
            print(f"  WARN  {n_conf} rows unreachable-CONFLICT: the owning file is level-locked "
                  f"away from the chapter. Needs a content move, not a context-list edit.")
        own = [f for f in ownership()[2] if f[0] in ("DUPLICATE", "MISPLACED", "STRAY")]
        if own:
            # FAIL on the same grounds as a malformed row: these three are
            # mechanical. Two files claiming one concept, a claimant the table
            # does not name, a slug the table does not list -- none of them needs
            # a judgment to be wrong. UNCLAIMED is left out deliberately: a
            # concept nobody has claimed yet is a project mid-adoption, not a
            # defect, and failing there would gate every run until the last file
            # was annotated.
            print(f"  FAIL  {len(own)} ownership finding(s) — a concept the project declares "
                  f"canonical is claimed twice, off-table, or by the wrong file (run --ownership):")
            for kind, slug, detail in own[:10]:
                print(f"          {kind:<10} {slug}  —  {detail}")
        n_ill = len(illegal_loads(books))
        if n_ill:
            # A warning on the same reasoning as CONFLICT, which it is the other
            # half of. The fix is either a `**Level:**` edit declaring a
            # cross-level beat the chapter already carries or a decision to drop
            # the file — both authorial, and both would be done with the guard
            # switched off if it failed here.
            print(f"  WARN  {n_ill} context entries a chapter's Level bars: the outline loads a "
                  f"file the register locks out (run --illegal-load).")
        hot = [(len(v), k) for k, v in planned.items() if len(v) > 2 * cap]
        if hot:
            print(f"  WARN  {len(hot)} chapters at more than 2x capacity:")
            for n, (book, ch) in sorted(hot, reverse=True)[:5]:
                print(f"          {book} Ch{ch:02d}  {n} pending ({n / cap:.1f}x)")
        if not (n_un or orphans or n_miss or bad or own):
            print("  OK    every row has a chapter; no orphans on drafted chapters; "
                  "every row's file is loaded by its chapter; every tracker table is intact; "
                  "every declared concept has one owner.")
            return 0
        return 1

    if args.free:
        print(f"LEVEL-0 CHAPTERS BY ROOM (measured capacity ~{cap} rendered elements)\n")
        rank = []
        for book in sorted(books):
            for ch in books[book]["reality"]:
                k = (book, ch)
                if k in WRITTEN_CHAPTERS:
                    continue
                rank.append((len(planned.get(k, [])), book, ch))
        for n, book, ch in sorted(rank):
            room = cap - n
            flag = "FULL" if room <= 0 else f"room {room}"
            print(f"  {book} Ch{ch:02d}   pending {n:3d}   {flag}")
        return

    print(f"CHAPTER LOAD — measured capacity ~{cap} rendered elements per chapter")
    print(f"(from {sum(len(v) for v in written.values())} rows already written across "
          f"{len(written)} drafted chapters)\n")
    over = [(len(v), k) for k, v in planned.items() if len(v) > cap]
    for n, (book, ch) in sorted(over, reverse=True):
        print(f"  {book} Ch{ch:02d}   {n:4d} pending   {n / cap:.1f}x capacity")
    print(f"\n  {len(over)} chapters over capacity; "
          f"{sum(len(v) for v in planned.values())} rows pending in total; "
          f"{sum(len(v) for v in unassigned.values())} unassigned "
          f"(run --unassigned); {len(nonnumeric)} assigned to a non-numeric chapter.")


if __name__ == "__main__":
    sys.exit(main())
