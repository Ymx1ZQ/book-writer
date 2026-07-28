#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "markdown",
#     "weasyprint>=60",
#     "pyyaml",
# ]
# ///
"""Render book chapters from Markdown to PDF.

Usage:
    build_pdf.py <book_dir> [--chapter chNN] [--out OUT]

Modes:
    single chapter : --chapter chNN  -> <book_dir>/pub/chNN.pdf
    whole book     : (no --chapter)  -> <book_dir>/pub/<book_name>.pdf
"""
import argparse
import re
import sys
from pathlib import Path

import markdown
import yaml
from weasyprint import HTML, CSS

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSS = SCRIPT_DIR / "book.css"


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "smarty"])


def book_title(book_dir: Path) -> str:
    outline = book_dir / "outline.md"
    if outline.is_file():
        for line in outline.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^#\s+(.+?)\s*$", line)
            if m:
                return m.group(1)
    return book_dir.name


def book_subtitle(book_dir: Path) -> str:
    m = re.match(r"book-(\d+)$", book_dir.name)
    if not m:
        return ""
    n = int(m.group(1))
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}
    return f"Book {words.get(n, str(n))}"


def load_meta(book_dir: Path) -> dict:
    """Read optional meta.yaml. Keys: title, subtitle, author, language.
    Symmetric with build_epub.py — the title page must not fall back to
    outline.md's internal-doc H1 when real publication metadata exists."""
    meta: dict = {}
    meta_path = book_dir / "meta.yaml"
    if not meta_path.is_file():
        return meta
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    for k in ("title", "subtitle", "author", "language"):
        if k in data and data[k]:
            meta[k] = str(data[k])
    return meta


def wrap(body: str, language: str = "en") -> str:
    # `lang` is what makes `hyphens: auto` in book.css do anything: WeasyPrint
    # hyphenates only when the document declares a language, and the stylesheet
    # justifies every paragraph. Without it the text is justified and never
    # broken, which opens the word spacing on an A5 page.
    return (
        "<!doctype html>"
        f"<html lang='{language}'><head><meta charset='utf-8'></head>"
        f"<body>{body}</body></html>"
    )


def render_single(book_dir: Path, ch: str, out: Path) -> Path:
    src = book_dir / f"{ch}.md"
    if not src.is_file():
        sys.exit(f"error: chapter source not found: {src}")
    body = md_to_html(src.read_text(encoding="utf-8"))
    language = load_meta(book_dir).get("language", "en")
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=wrap(body, language)).write_pdf(
        str(out), stylesheets=[CSS(filename=str(DEFAULT_CSS))]
    )
    return out


def render_book(book_dir: Path, out: Path) -> Path:
    # Glob `ch[0-9][0-9].md` (exactly chNN.md) to exclude planning/auxiliary
    # files like ch04-plan.md that would otherwise be rendered as chapters.
    chapters = sorted(book_dir.glob("ch[0-9][0-9].md"))
    if not chapters:
        sys.exit(f"error: no chapter files (chNN.md) found in {book_dir}")

    meta = load_meta(book_dir)
    title = meta.get("title") or book_title(book_dir)
    subtitle = meta.get("subtitle") or book_subtitle(book_dir)
    author = meta.get("author")
    parts = [
        "<div class='titlepage'>",
        f"<div class='title'>{title}</div>",
    ]
    if subtitle:
        parts.append(f"<div class='subtitle'>{subtitle}</div>")
    if author:
        parts.append(f"<div class='author'>{author}</div>")
    parts.append("</div>")
    parts.append("<div class='chapter-break'></div>")

    for i, ch in enumerate(chapters):
        parts.append(md_to_html(ch.read_text(encoding="utf-8")))
        if i < len(chapters) - 1:
            parts.append("<div class='chapter-break'></div>")

    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=wrap("".join(parts), meta.get("language", "en"))).write_pdf(
        str(out), stylesheets=[CSS(filename=str(DEFAULT_CSS))]
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Render book chapters to PDF")
    ap.add_argument("book_dir", help="path to chapters/book-N")
    ap.add_argument("--chapter", help="single chapter id, e.g. ch01")
    ap.add_argument("--out", help="output PDF path (default: <book_dir>/pub/...)")
    args = ap.parse_args()

    book_dir = Path(args.book_dir).resolve()
    if not book_dir.is_dir():
        sys.exit(f"error: book directory not found: {book_dir}")

    if args.chapter:
        out = Path(args.out) if args.out else book_dir / "pub" / f"{args.chapter}.pdf"
        result = render_single(book_dir, args.chapter, out)
    else:
        out = Path(args.out) if args.out else book_dir / "pub" / f"{book_dir.name}.pdf"
        result = render_book(book_dir, out)

    print(f"wrote {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
