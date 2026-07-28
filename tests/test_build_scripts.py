"""Smoke tests for the PEP723 build scripts (build_pdf.py / build_epub.py).

They import heavy deps (markdown, weasyprint, ebooklib) at module top, so a
bare `python3 build_pdf.py --help` can't run without those installed. We
guarantee statically that each script is valid Python, declares its PEP723
dependency block, and wires argparse — and, when `uv` is present, actually run
`uv run --script ... --help` (uv resolves the deps) for a real exit-0 smoke.
"""
from __future__ import annotations

import ast
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
BUILD_SCRIPTS = ["build_pdf.py", "build_epub.py"]
NEEDS_UV = pytest.mark.skipif(
    shutil.which("uv") is None, reason="uv not on PATH — real render skipped"
)


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


# --- document language (skill Phase 28) -----------------------------------
#
# Both builders read `language` from meta.yaml. Until Phase 28 the EPUB wrote a
# hardcoded lang="en" into every chapter document and the PDF wrote no lang at
# all, so an Italian book was narrated in an English voice and no PDF this
# script ever produced was hyphenated — `hyphens: auto` needs a declared
# language to key on.


def _book(tmp_path: Path, meta: str | None) -> Path:
    d = tmp_path / "book-1"
    d.mkdir()
    (d / "ch01.md").write_text("# Ch. 01 — Uno\n\nUn paragrafo di prova.\n")
    (d / "ch02.md").write_text("# Ch. 02 — Due\n\nUn altro paragrafo di prova.\n")
    if meta is not None:
        (d / "meta.yaml").write_text(meta)
    return d


def _render(script: str, book_dir: Path, out: Path, *extra: str) -> None:
    r = subprocess.run(
        ["uv", "run", "--script", str(SCRIPTS / script), str(book_dir),
         "--out", str(out), *extra],
        capture_output=True, text=True, timeout=600,
    )
    assert r.returncode == 0, r.stderr
    assert out.is_file() and out.stat().st_size > 0


@NEEDS_UV
@pytest.mark.parametrize(
    "meta,expected",
    [("title: T\nauthor: A\nlanguage: it-IT\n", "it-IT"), (None, "en")],
    ids=["meta-language", "default-when-no-meta"],
)
def test_epub_documents_declare_the_book_language(tmp_path, meta, expected) -> None:
    out = tmp_path / "o.epub"
    _render("build_epub.py", _book(tmp_path, meta), out)
    with zipfile.ZipFile(out) as z:
        docs = [n for n in z.namelist() if n.endswith(".xhtml")]
        # Two chapters plus the nav: a narrating reader hits the nav first.
        assert len(docs) == 3, docs
        for name in docs:
            tag = re.search(r"<html[^>]*>", z.read(name).decode()).group()
            assert f'lang="{expected}"' in tag, f"{name}: {tag}"


@NEEDS_UV
def test_pdf_declares_the_book_language(tmp_path) -> None:
    out = tmp_path / "o.pdf"
    _render("build_pdf.py", _book(tmp_path, "title: T\nlanguage: it-IT\n"), out)
    assert out.read_bytes().startswith(b"%PDF")


@NEEDS_UV
def test_pdf_single_chapter_reads_meta(tmp_path) -> None:
    # render_single had no meta.yaml path at all before Phase 28, so a
    # single-chapter PDF stayed unhyphenated even once render_book was fixed.
    out = tmp_path / "ch01.pdf"
    _render("build_pdf.py", _book(tmp_path, "title: T\nlanguage: it-IT\n"), out,
            "--chapter", "ch01")
    assert out.read_bytes().startswith(b"%PDF")


def test_pdf_emits_no_language_less_html_element() -> None:
    # The regression this phase closes is a literal, and it renders without
    # error — nothing but the source pins it.
    src = (SCRIPTS / "build_pdf.py").read_text()
    assert "<html>" not in src, "build_pdf.py emits an <html> element with no lang"
    assert re.search(r"def wrap\(body: str, language", src), "wrap() takes no language"


# --- remap_citations (skill Phase 26) -------------------------------------
#
# A prose edit shifts every line citation below it, silently: the stale citation
# still points at a real line that now says something else. These tests pin the
# three behaviours that make the remapper safe to run unattended -- it shifts
# what moved, it refuses to guess at what was rewritten, and it never touches a
# historical record.

import subprocess as _sp
import sys as _sys
from pathlib import Path as _Path

_SCRIPTS = _Path(__file__).resolve().parent.parent / "scripts"
_sys.path.insert(0, str(_SCRIPTS))


def _repo(tmp_path, chapter_text, note_text, smell_text="historical ch07.md:4\n"):
    _sp.run(["git", "init", "-q", "."], cwd=tmp_path, check=True)
    (tmp_path / "chapters" / "book-1").mkdir(parents=True)
    (tmp_path / "world").mkdir()
    (tmp_path / "chapters" / "book-1" / "ch07.md").write_text(chapter_text)
    (tmp_path / "chapters" / "book-1" / "SMELL.md").write_text(smell_text)
    (tmp_path / "world" / "note.md").write_text(note_text)
    _sp.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    _sp.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
             "commit", "-qm", "init"], cwd=tmp_path, check=True)
    return tmp_path


def _run(root, *chapters):
    return _sp.run(
        [_sys.executable, str(_SCRIPTS / "remap_citations.py"), str(root), *chapters],
        capture_output=True, text=True,
    )


def test_insertion_shifts_citations_and_ranges(tmp_path):
    root = _repo(tmp_path, "a\nb\nc\nd\ne\n", "at ch07.md:4 and range ch07.md:3-5\n")
    (root / "chapters" / "book-1" / "ch07.md").write_text("a\nX\nY\nb\nc\nd\ne\n")
    r = _run(root, "chapters/book-1/ch07.md")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (root / "world" / "note.md").read_text() == "at ch07.md:6 and range ch07.md:5-7\n"


def test_historical_files_are_never_rewritten(tmp_path):
    root = _repo(tmp_path, "a\nb\nc\nd\ne\n", "at ch07.md:4\n")
    (root / "chapters" / "book-1" / "ch07.md").write_text("a\nX\nY\nb\nc\nd\ne\n")
    _run(root, "chapters/book-1/ch07.md")
    # The SMELL entry cites the line it examined on its own date. Rewriting it
    # would falsify the record rather than repair it.
    assert (root / "chapters" / "book-1" / "SMELL.md").read_text() == "historical ch07.md:4\n"


def test_deleted_target_is_reported_not_guessed(tmp_path):
    root = _repo(tmp_path, "a\nb\nZZZ\nd\ne\n", "deleted target ch07.md:3\n")
    (root / "chapters" / "book-1" / "ch07.md").write_text("a\nb\nd\ne\n")
    r = _run(root, "chapters/book-1/ch07.md")
    assert r.returncode == 1, r.stdout
    assert "Needs a decision" in r.stdout
    assert (root / "world" / "note.md").read_text() == "deleted target ch07.md:3\n"
