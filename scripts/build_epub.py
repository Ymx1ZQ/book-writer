#!/usr/bin/env python3
"""Render book chapters from Markdown to EPUB.

Usage:
    build_epub.py <book_dir> [--chapter chNN] [--out OUT]

Modes:
    single chapter : --chapter chNN  -> <book_dir>/epub/chNN.epub
    whole book     : (no --chapter)  -> <book_dir>/epub/<book_name>.epub
"""
import argparse
import re
import sys
import uuid
from pathlib import Path

import markdown
from ebooklib import epub

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CSS = SCRIPT_DIR / "epub.css"


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "smarty"])


def first_h1_title(md_text: str) -> str:
    for line in md_text.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    return ""


def book_title(book_dir: Path) -> str:
    outline = book_dir / "outline.md"
    if outline.is_file():
        t = first_h1_title(outline.read_text(encoding="utf-8"))
        if t:
            return t
    return book_dir.name


def load_meta(book_dir: Path) -> dict:
    """Read optional meta.yaml. Keys: title, author, identifier, language."""
    meta: dict = {}
    meta_path = book_dir / "meta.yaml"
    if not meta_path.is_file():
        return meta
    try:
        import yaml
    except ImportError:
        print(
            "warning: PyYAML not installed; ignoring meta.yaml. "
            "Install with: pip install --user pyyaml",
            file=sys.stderr,
        )
        return meta
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    for k in ("title", "author", "identifier", "language"):
        if k in data and data[k]:
            meta[k] = str(data[k])
    return meta


def deterministic_uuid(book_dir: Path, scope: str) -> str:
    """Stable UUID across re-renders so KDP keeps the same EPUB id."""
    key = f"book://{book_dir.resolve()}/{scope}"
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, key)}"


def make_book(title: str, author: str, identifier: str, language: str) -> epub.EpubBook:
    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    return book


def add_default_css(book: epub.EpubBook) -> epub.EpubItem:
    css_item = epub.EpubItem(
        uid="style",
        file_name="style.css",
        media_type="text/css",
        content=DEFAULT_CSS.read_text(encoding="utf-8"),
    )
    book.add_item(css_item)
    return css_item


def make_chapter_item(filename: str, title: str, html_body: str) -> epub.EpubHtml:
    chap = epub.EpubHtml(title=title, file_name=filename, lang="en")
    chap.content = (
        "<?xml version='1.0' encoding='utf-8'?>"
        "<!DOCTYPE html>"
        "<html xmlns='http://www.w3.org/1999/xhtml'>"
        f"<head><title>{title}</title>"
        "<link rel='stylesheet' type='text/css' href='style.css'/>"
        f"</head><body>{html_body}</body></html>"
    )
    return chap


def render_single(book_dir: Path, ch: str, out: Path) -> Path:
    src = book_dir / f"{ch}.md"
    if not src.is_file():
        sys.exit(f"error: chapter source not found: {src}")
    md_text = src.read_text(encoding="utf-8")
    chapter_title = first_h1_title(md_text) or ch
    html_body = md_to_html(md_text)

    meta = load_meta(book_dir)
    title = meta.get("title", chapter_title)
    author = meta.get("author", "Unknown Author")
    language = meta.get("language", "en")
    identifier = meta.get("identifier", deterministic_uuid(book_dir, ch))

    book = make_book(title, author, identifier, language)
    add_default_css(book)
    chap = make_chapter_item(f"{ch}.xhtml", chapter_title, html_body)
    book.add_item(chap)
    book.toc = (chap,)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chap]

    out.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out), book)
    return out


def render_book(book_dir: Path, out: Path) -> Path:
    chapters = sorted(book_dir.glob("ch*.md"))
    if not chapters:
        sys.exit(f"error: no chapter files (ch*.md) found in {book_dir}")

    meta = load_meta(book_dir)
    title = meta.get("title", book_title(book_dir))
    author = meta.get("author", "Unknown Author")
    language = meta.get("language", "en")
    identifier = meta.get("identifier", deterministic_uuid(book_dir, "book"))

    book = make_book(title, author, identifier, language)
    add_default_css(book)

    items = []
    for src in chapters:
        md_text = src.read_text(encoding="utf-8")
        ch_title = first_h1_title(md_text) or src.stem
        html_body = md_to_html(md_text)
        chap = make_chapter_item(f"{src.stem}.xhtml", ch_title, html_body)
        book.add_item(chap)
        items.append(chap)

    book.toc = tuple(items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + items

    out.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out), book)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Render book chapters to EPUB")
    ap.add_argument("book_dir", help="path to chapters/book-N")
    ap.add_argument("--chapter", help="single chapter id, e.g. ch01")
    ap.add_argument("--out", help="output EPUB path (default: <book_dir>/epub/...)")
    args = ap.parse_args()

    book_dir = Path(args.book_dir).resolve()
    if not book_dir.is_dir():
        sys.exit(f"error: book directory not found: {book_dir}")

    if args.chapter:
        out = Path(args.out) if args.out else book_dir / "epub" / f"{args.chapter}.epub"
        result = render_single(book_dir, args.chapter, out)
    else:
        out = Path(args.out) if args.out else book_dir / "epub" / f"{book_dir.name}.epub"
        result = render_book(book_dir, out)

    print(f"wrote {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
