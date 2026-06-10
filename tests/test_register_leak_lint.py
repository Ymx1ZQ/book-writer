"""Tests for the deterministic register-leak linter (Phase 14 M4 / Phase 15 M1).

Covers the exit-code contract, per-level gating, the `not`-guard, and the
documented motivating bug (`the lines were the lines` slipping past the LLM).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "register_leak_lint.py"
sys.path.insert(0, str(REPO / "scripts"))

import register_leak_lint as lint_mod  # noqa: E402


def run_cli(chapter: Path, level: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(chapter), "--level", level],
        capture_output=True, text=True,
    )


# --- the lint() function directly (deterministic, no exit-code) ---

def test_noun_repeat_tautology_detected(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("She watched the road. The lines were the lines, and nothing moved.\n")
    hits = lint_mod.lint(str(f), "reality")
    assert len(hits) == 1
    assert "the lines were the lines" in hits[0][1].lower()


def test_not_guard_suppresses_meaningful_negation(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("His voice was not the voice he had meant to use.\n")
    assert lint_mod.lint(str(f), "reality") == []


def test_kept_its_and_where_the_x_forms(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text(
        "The wall kept its wall.\n"
        "The chair was where the chair had always stood — no: the chair was where the chair.\n"
    )
    hits = lint_mod.lint(str(f), "reality")
    names = " ".join(h[2] for h in hits)
    assert "kept-its-X" in names
    assert "where-the-X" in names


def test_compliance_vocab_leak_in_reality(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("A compliance nudge moved through the crowd; everything stayed within parameters.\n")
    hits = lint_mod.lint(str(f), "reality")
    assert len(hits) == 2  # "compliance nudge" + "within parameters"


def test_dome_level_skips_deterministic_checks(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("The lines were the lines. A compliance nudge passed.\n")
    # Dome's forbidden list is semantic — the linter applies no deterministic patterns.
    assert lint_mod.lint(str(f), "dome") == []


# --- the CLI exit-code contract ---

def test_cli_exit1_on_leak(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("The lines were the lines.\n")
    r = run_cli(f, "reality")
    assert r.returncode == 1
    assert "LEAK" in r.stdout


def test_cli_exit0_on_clean(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("The road unspooled ahead, and she drove until the light gave out.\n")
    r = run_cli(f, "reality")
    assert r.returncode == 0
    assert "clean" in r.stdout


def test_cli_exit0_on_dome_no_patterns(tmp_path: Path) -> None:
    f = tmp_path / "ch.md"
    f.write_text("The lines were the lines.\n")
    r = run_cli(f, "dome")
    assert r.returncode == 0
    assert "no deterministic patterns" in r.stdout
