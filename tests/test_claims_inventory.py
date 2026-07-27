"""Tests for the claims inventory (Phase 27 M1).

The pass it serves compresses prose, so the guard has to discriminate between a
rewording (fine) and a dropped instruction (not). These pin that discrimination
and, as importantly, pin the limitation: the exact half is a set, so it sees the
loss of a token's LAST mention and not the loss of one of several. That case is
reported as THINNED rather than failed, and this file says so out loud because
the negative test found it after the script was already written.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "claims_inventory.py"

DOC = """# Title

## Section one
- Read `world/timeline.md` before starting.
- Flag anything over 5 chapters as WARNING.

## Section two
Every run MUST exit 0. See `registers.md` for the rule.
"""


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_a_file_against_itself_reports_no_loss(tmp_path: Path) -> None:
    f = write(tmp_path, "a.md", DOC)
    r = run(str(f), str(f))
    assert r.returncode == 0, r.stdout
    assert "No exact claim was lost" in r.stdout


def test_rewording_without_losing_a_claim_passes(tmp_path: Path) -> None:
    # The whole point: prose changes, claims do not.
    before = write(tmp_path, "b.md", DOC)
    after = write(tmp_path, "c.md", DOC.replace(
        "Every run MUST exit 0.", "Runs MUST exit 0, without exception."))
    r = run(str(before), str(after))
    assert r.returncode == 0, r.stdout


def test_a_deleted_instruction_fails(tmp_path: Path) -> None:
    before = write(tmp_path, "d.md", DOC)
    after = write(tmp_path, "e.md", DOC.replace(
        "- Flag anything over 5 chapters as WARNING.\n", ""))
    r = run(str(before), str(after))
    assert r.returncode == 1
    assert "LOST" in r.stdout
    assert "5 chapters" in r.stdout


def test_a_deleted_cross_reference_fails(tmp_path: Path) -> None:
    before = write(tmp_path, "f.md", DOC)
    after = write(tmp_path, "g.md", DOC.replace(" See `registers.md` for the rule.", ""))
    r = run(str(before), str(after))
    assert r.returncode == 1
    assert "registers.md" in r.stdout


def test_a_deleted_section_fails(tmp_path: Path) -> None:
    before = write(tmp_path, "h.md", DOC)
    after = write(tmp_path, "i.md", DOC.split("## Section two")[0])
    r = run(str(before), str(after))
    assert r.returncode == 1
    assert "Section two" in r.stdout


def test_losing_one_of_several_mentions_is_thinned_not_failed(tmp_path: Path) -> None:
    # The limitation, pinned rather than hidden. Found by the negative test on
    # 2026-07-27: deleting a sentence that referenced `chapter-writer.md`
    # changed nothing, because the file was referenced four more times.
    doubled = DOC + "\nAlso read `world/timeline.md` at the end.\n"
    before = write(tmp_path, "j.md", doubled)
    after = write(tmp_path, "k.md", DOC)
    r = run(str(before), str(after))
    assert r.returncode == 0, r.stdout
    assert "THINNED" in r.stdout
    assert "world/timeline.md" in r.stdout


def test_added_instruction_is_reported_and_does_not_fail(tmp_path: Path) -> None:
    before = write(tmp_path, "l.md", DOC)
    after = write(tmp_path, "m.md", DOC + "\n- Never skip `scripts/build_pdf.py`.\n")
    r = run(str(before), str(after))
    assert r.returncode == 0, r.stdout
    assert "GAINED" in r.stdout


def test_fenced_examples_are_not_claims(tmp_path: Path) -> None:
    # Example blocks churn freely and would swamp the diff with false losses.
    before = write(tmp_path, "n.md", DOC + "\n```\nrm -rf `something.md`\n```\n")
    after = write(tmp_path, "o.md", DOC + "\n```\ndifferent example entirely\n```\n")
    r = run(str(before), str(after))
    assert r.returncode == 0, r.stdout
