"""Tests for the chapter-load guard (Phase 97 M9).

The guard shipped as a project-side script for three days and grew eight modes
there, where no other project could reach it and where a partial reimplementation
had already cost one consuming repo a 314-versus-226 miscount. These tests run it
against a synthetic project built in a tmpdir, so they pin the model rather than
one corpus: the four reachability routes, the level register, the co-primary /
parenthetical distinction in the `**Level:**` field, and the two derivations that
replaced hand-maintained constants.

The consuming project keeps its own suite. That one is a regression record of
defects measured in its corpus and cannot move here; this one is what a freshly
scaffolded project runs.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "chapter_load.py"


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin", "BOOK_PROJECT_ROOT": str(root)},
    )


def verdicts(out: str) -> tuple[int, int]:
    """(MISSING, CONFLICT) from the --unreachable header.

    Parsed rather than grepped: both words appear in the legend the mode prints
    under the header, so `"CONFLICT" in out` is true even at zero.
    """
    m = re.search(r"\((\d+) MISSING, (\d+) CONFLICT\)", out)
    assert m, out
    return int(m.group(1)), int(m.group(2))


def tracker(*rows: str) -> str:
    head = ("## Usage Tracker\n\n"
            "| Element | Book | Ch | Detail | Status |\n"
            "|---------|------|----|--------|--------|\n")
    return head + "".join(rows) + "\n"


def scaffold(root: Path, *, level_line: str = "**Level:** Reality | **POV:** A",
             context: str = "**context:** world/anchors.md") -> None:
    """The minimum a project needs for the guard to have anything to join."""
    for d in ("world/level-0-reality", "world/level-1-ark", "plot", "characters",
              "chapters/book-1"):
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "chapters/book-1/outline.md").write_text(
        "# Book 1 — Outline\n\n"
        "**Always-loaded reference files:** `world/overview.md`\n\n"
        f"## Ch. 01 — Opening\n{level_line}\n{context}\n\n"
        "## Ch. 02 — Second\n**Level:** Ark | **POV:** B\n"
        "**context:** world/anchors.md\n",
        encoding="utf-8")
    (root / "world/overview.md").write_text("# Overview\n", encoding="utf-8")
    (root / "world/anchors.md").write_text(
        "# Anchors\n\n" + tracker("| A reachable element | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")


# --- the empty case: a project that has just been scaffolded ------------------

def test_empty_corpus_passes(tmp_path: Path) -> None:
    for d in ("world", "plot", "characters", "chapters"):
        (tmp_path / d).mkdir()
    r = run(tmp_path, "--check")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK" in r.stdout


def test_scaffolded_corpus_passes(tmp_path: Path) -> None:
    scaffold(tmp_path)
    r = run(tmp_path, "--check")
    assert r.returncode == 0, r.stdout + r.stderr


# --- the four reachability routes ---------------------------------------------

def test_row_absent_from_the_context_list_is_missing(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "world/loose.md").write_text(
        "# Loose\n\n" + tracker("| An unreachable element | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")
    r = run(tmp_path, "--check")
    assert r.returncode == 1
    assert "unreachable-MISSING" in r.stdout


def test_always_loaded_set_reaches_every_chapter(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "world/overview.md").write_text(
        "# Overview\n\n" + tracker("| Element in the always-loaded set | B1 | 02 | accent | planned |\n"),
        encoding="utf-8")
    r = run(tmp_path, "--check")
    assert r.returncode == 0, r.stdout


def test_own_level_directory_reaches_without_a_context_entry(tmp_path: Path) -> None:
    # The fourth route, and the one a partial reimplementation drops: the writer
    # lists the chapter's own level directory and opens the files whose rows name
    # this chapter, so those rows need no context entry.
    scaffold(tmp_path)
    (tmp_path / "world/level-0-reality/streets.md").write_text(
        "# Streets\n\n" + tracker("| Element in the chapter's own level dir | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")
    r = run(tmp_path, "--check")
    assert r.returncode == 0, r.stdout


# --- the level register --------------------------------------------------------

def test_row_in_a_barred_level_directory_is_a_conflict(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "world/level-1-ark/hull.md").write_text(
        "# Hull\n\n" + tracker("| Ark element aimed at a Reality chapter | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")
    assert verdicts(run(tmp_path, "--unreachable").stdout) == (0, 1)
    # A conflict is never fixable by a context entry, so --check must not count
    # it among the MISSING rows it fails on.
    assert run(tmp_path, "--check").returncode == 0


def test_declared_secondary_level_authorizes_the_row(tmp_path: Path) -> None:
    scaffold(tmp_path, level_line="**Level:** Reality (Ark flash) | **POV:** A")
    (tmp_path / "world/level-1-ark/hull.md").write_text(
        "# Hull\n\n" + tracker("| Ark element in a declared cross-level chapter | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")
    assert verdicts(run(tmp_path, "--unreachable").stdout) == (0, 0)


def test_context_entry_a_level_bars_is_reported(tmp_path: Path) -> None:
    # The reverse direction. Listing a barred file silences the CONFLICT verdict
    # instead of resolving it, so the two checks have to read the same field.
    scaffold(tmp_path, context="**context:** world/anchors.md, world/level-1-ark/hull.md")
    (tmp_path / "world/level-1-ark/hull.md").write_text("# Hull\n", encoding="utf-8")
    r = run(tmp_path, "--illegal-load")
    assert "level-1-ark/hull.md" in r.stdout


def test_declared_secondary_level_exempts_the_context_entry(tmp_path: Path) -> None:
    scaffold(tmp_path, level_line="**Level:** Reality (Ark flash) | **POV:** A",
             context="**context:** world/anchors.md, world/level-1-ark/hull.md")
    (tmp_path / "world/level-1-ark/hull.md").write_text("# Hull\n", encoding="utf-8")
    r = run(tmp_path, "--illegal-load")
    assert "level-1-ark/hull.md" not in r.stdout, r.stdout


# --- co-primary versus parenthetical -------------------------------------------

def test_co_primary_level_opens_a_placement_slot(tmp_path: Path) -> None:
    scaffold(tmp_path, level_line="**Level:** Ark + Reality | **POV:** A")
    out = run(tmp_path, "--free").stdout
    assert "B1 Ch01" in out, out


def test_parenthetical_level_opens_no_placement_slot(tmp_path: Path) -> None:
    scaffold(tmp_path, level_line="**Level:** Ark (Reality residue) | **POV:** A")
    out = run(tmp_path, "--free").stdout
    assert "B1 Ch01" not in out, out


# --- the derivations that replaced hand-maintained constants --------------------

def test_level_directories_are_read_off_the_tree(tmp_path: Path) -> None:
    # A level the tool was never told about must still be a register, not a
    # level-neutral directory every chapter may load.
    scaffold(tmp_path)
    (tmp_path / "world/level-3-garden").mkdir()
    (tmp_path / "world/level-3-garden/flora.md").write_text(
        "# Flora\n\n" + tracker("| Element at a level nobody declared | B1 | 01 | accent | planned |\n"),
        encoding="utf-8")
    assert verdicts(run(tmp_path, "--unreachable").stdout) == (0, 1)


def test_books_are_read_off_the_tree(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "world/anchors.md").write_text(
        "# Anchors\n\n" + tracker("| Element in a second book | B2 | 01 | accent | planned |\n"),
        encoding="utf-8")
    assert "world/anchors.md" in run(tmp_path, "--book-form").stdout
    (tmp_path / "chapters/book-2").mkdir()
    (tmp_path / "chapters/book-2/outline.md").write_text(
        "# Book 2 — Outline\n\n## Ch. 01 — Opening\n**Level:** Reality | **POV:** A\n"
        "**context:** world/anchors.md\n", encoding="utf-8")
    assert "world/anchors.md" not in run(tmp_path, "--book-form").stdout


# --- structural damage ---------------------------------------------------------

def test_a_destroyed_row_is_reported_not_skipped(tmp_path: Path) -> None:
    # The row parser skips what it cannot match, so a damaged row does not become
    # malformed -- it stops existing, every count drops by one, and every mode
    # still reports success.
    scaffold(tmp_path)
    (tmp_path / "world/anchors.md").write_text(
        "# Anchors\n\n"
        "## Usage Tracker\n\n"
        "| Element | Book | Ch | Detail | Status |\n"
        "|---------|------|----|--------|--------|\n"
        "unchanged\n\n", encoding="utf-8")
    r = run(tmp_path, "--check")
    assert r.returncode == 1
    assert "malformed line(s) inside a Usage Tracker table" in r.stdout


def test_a_context_entry_naming_no_file_is_raised(tmp_path: Path) -> None:
    # Swallowing it would turn every row in that file into a false MISSING.
    scaffold(tmp_path, context="**context:** world/anchors.md, world/does-not-exist.md")
    r = run(tmp_path, "--check")
    assert r.returncode == 2
    assert "resolves to no file" in r.stderr


# --- the read-only contract ----------------------------------------------------

def test_the_guard_never_writes(tmp_path: Path) -> None:
    scaffold(tmp_path)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    for mode in ("--check", "--unreachable", "--illegal-load", "--free",
                 "--unassigned", "--orphans", "--written", "--book-form"):
        run(tmp_path, mode)
    after = {p: p.read_bytes() for p in tmp_path.rglob("*.md")}
    assert before == after


# --- single ownership ----------------------------------------------------------

def concept_table(*rows: str) -> str:
    head = ("## Information Architecture\n\n"
            "| Concept | Slug | Canonical file |\n"
            "|---------|------|----------------|\n")
    return head + "".join(rows) + "\n"


def test_ownership_clean_when_each_slug_has_one_owner(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n"), encoding="utf-8")
    anchors = tmp_path / "world/anchors.md"
    anchors.write_text("---\nowns: [timeline]\n---\n" + anchors.read_text(encoding="utf-8"),
                       encoding="utf-8")
    r = run(tmp_path, "--ownership")
    assert r.returncode == 0, r.stdout
    assert "1 concepts declared, 0 finding(s)" in r.stdout


def test_ownership_catches_a_second_claimant(tmp_path: Path) -> None:
    # The defect this exists for: a second explanation accretes in a neighbouring
    # file and drifts, and every other check passes because each file is
    # internally consistent.
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n"), encoding="utf-8")
    for rel in ("world/anchors.md", "world/overview.md"):
        p = tmp_path / rel
        p.write_text("---\nowns: [timeline]\n---\n" + p.read_text(encoding="utf-8"),
                     encoding="utf-8")
    r = run(tmp_path, "--ownership")
    assert r.returncode == 1
    assert "DUPLICATE" in r.stdout
    # and it fails the pipeline guard, not only the listing mode
    assert run(tmp_path, "--check").returncode == 1


def test_ownership_catches_a_claim_the_table_does_not_list(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n"), encoding="utf-8")
    for rel, slug in (("world/anchors.md", "timeline"), ("world/overview.md", "invented")):
        p = tmp_path / rel
        p.write_text(f"---\nowns: [{slug}]\n---\n" + p.read_text(encoding="utf-8"),
                     encoding="utf-8")
    r = run(tmp_path, "--ownership")
    assert r.returncode == 1
    assert "STRAY" in r.stdout and "invented" in r.stdout


def test_ownership_unclaimed_is_reported_but_does_not_fail_the_guard(tmp_path: Path) -> None:
    # A concept nobody has annotated yet is a project mid-adoption, not a defect.
    # Failing here would gate every run until the last file was annotated.
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n"), encoding="utf-8")
    assert "UNCLAIMED" in run(tmp_path, "--ownership").stdout
    assert run(tmp_path, "--check").returncode == 0


def test_ownership_reads_the_table_from_the_project(tmp_path: Path) -> None:
    # The done-when for the whole check: adding a row to the project's table, and
    # nothing else, changes what the check reports. A copy of the slug list in
    # the tool would be the second source of truth this check exists to find.
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n"), encoding="utf-8")
    anchors = tmp_path / "world/anchors.md"
    anchors.write_text("---\nowns: [timeline]\n---\n" + anchors.read_text(encoding="utf-8"),
                       encoding="utf-8")
    assert "1 concepts declared, 0 finding(s)" in run(tmp_path, "--ownership").stdout
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| The timeline | `timeline` | `world/anchors.md` |\n",
                      "| The tone | `tone` | `world/overview.md` |\n"), encoding="utf-8")
    out = run(tmp_path, "--ownership").stdout
    assert "2 concepts declared, 1 finding(s)" in out
    assert "UNCLAIMED" in out and "tone" in out


def test_ownership_pattern_rows_are_reported_as_uncovered(tmp_path: Path) -> None:
    scaffold(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        concept_table("| Per-character flashbacks | `flashbacks` | `characters/<char>.md` |\n",
                      "| Chapter detail | `chapter-detail` | `chapters/book-N/outline.md` |\n"),
        encoding="utf-8")
    r = run(tmp_path, "--ownership")
    assert r.returncode == 0, r.stdout
    assert "2 row(s) name a pattern rather than a file and are NOT covered" in r.stdout


def test_ownership_with_no_table_checks_nothing(tmp_path: Path) -> None:
    scaffold(tmp_path)
    r = run(tmp_path, "--ownership")
    assert r.returncode == 0
    assert "no `| Concept | Slug | Canonical file |` table" in r.stdout


# --- --chapter X --written: the rendered rows for one chapter -----------------
#
# /book fidelity audits the claim that a row marked `written` reached the page,
# and needs the files carrying those rows for ONE chapter. Until 2026-08-03 the
# combination printed only the summary line -- `--chapter` returned before
# `--written` was ever consulted -- so the rows were reachable only through bare
# `--written`, which prints every drafted chapter at once. The instruction
# reached for a graph query instead, and inherited a staleness failure mode for
# a question the trackers already answer.

def rendered_scaffold(root: Path) -> None:
    scaffold(root)
    (root / "world/anchors.md").write_text(
        "# Anchors\n\n" + tracker(
            "| Still queued | B1 | 01 | accent | planned |\n",
            "| Already on the page | B1 | 01 | accent | written |\n",
            "| Also rendered | B1 | 01 | scene | written |\n",
            "| A later chapter's | B1 | 02 | accent | written |\n",
        ),
        encoding="utf-8")


def test_chapter_written_lists_the_rendered_rows(tmp_path: Path) -> None:
    rendered_scaffold(tmp_path)
    r = run(tmp_path, "--chapter", "B1:01", "--written")
    assert r.returncode == 0, r.stderr or r.stdout
    assert "1 pending, 2 rendered" in r.stdout
    assert "Already on the page" in r.stdout
    assert "Also rendered" in r.stdout
    # The pending row must not leak into the rendered list, or the caller
    # verifies elements against the page that were never claimed to be there.
    assert "Still queued" not in r.stdout


def test_chapter_without_written_still_lists_the_pending_rows(tmp_path: Path) -> None:
    rendered_scaffold(tmp_path)
    r = run(tmp_path, "--chapter", "B1:01")
    assert "Still queued" in r.stdout
    assert "Already on the page" not in r.stdout


def test_chapter_written_does_not_bleed_across_chapters(tmp_path: Path) -> None:
    # Both halves are needed. Asserting only that ch02's row is absent from
    # ch01's output passes against the pre-2026-08-03 script too, which listed
    # ch01's PENDING rows and so excluded it for the wrong reason. The pairing
    # is what shows the rendered set is being selected per chapter.
    rendered_scaffold(tmp_path)
    first = run(tmp_path, "--chapter", "B1:01", "--written").stdout
    second = run(tmp_path, "--chapter", "B1:02", "--written").stdout
    assert "Already on the page" in first and "A later chapter's" not in first
    assert "A later chapter's" in second and "Already on the page" not in second


def test_chapter_written_names_the_file_carrying_each_row(tmp_path: Path) -> None:
    # The point of the mode is the file list -- a count sends the caller nowhere.
    rendered_scaffold(tmp_path)
    out = run(tmp_path, "--chapter", "B1:01", "--written").stdout
    assert "world/anchors.md" in out
    assert "(2)" in out, "the per-file count is missing"


def test_chapter_written_on_a_chapter_with_nothing_rendered(tmp_path: Path) -> None:
    rendered_scaffold(tmp_path)
    out = run(tmp_path, "--chapter", "B1:02", "--written").stdout
    assert "0 pending, 1 rendered" in out
