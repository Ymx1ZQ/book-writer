"""Smoke tests for the PEP723 build scripts (build_pdf.py / build_epub.py).

They import heavy deps (markdown, weasyprint, ebooklib) at module top, so a
bare `python3 build_pdf.py --help` can't run without those installed. We
guarantee statically that each script is valid Python, declares its PEP723
dependency block, and wires argparse — and, when `uv` is present, actually run
`uv run --script ... --help` (uv resolves the deps) for a real exit-0 smoke.
"""
from __future__ import annotations

import ast
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
BUILD_SCRIPTS = ["build_pdf.py", "build_epub.py"]


@pytest.mark.parametrize("name", BUILD_SCRIPTS)
def test_script_is_valid_python(name: str) -> None:
    src = (SCRIPTS / name).read_text()
    ast.parse(src)  # raises SyntaxError on a broken script


@pytest.mark.parametrize("name", BUILD_SCRIPTS)
def test_pep723_block_and_argparse(name: str) -> None:
    src = (SCRIPTS / name).read_text()
    assert "# /// script" in src and "# ///" in src, f"{name}: missing PEP723 metadata block"
    assert "dependencies" in src, f"{name}: PEP723 block declares no dependencies"
    assert "argparse" in src, f"{name}: no argparse wiring"
    assert "def main" in src, f"{name}: no main()"


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not on PATH — real render smoke skipped")
@pytest.mark.parametrize("name", BUILD_SCRIPTS)
def test_uv_run_help(name: str) -> None:
    r = subprocess.run(
        ["uv", "run", "--script", str(SCRIPTS / name), "--help"],
        capture_output=True, text=True, timeout=300,
    )
    assert r.returncode == 0, r.stderr
    assert "usage" in (r.stdout + r.stderr).lower()
