# `/book pdf` — render chapters to PDF

Render Markdown chapters to a book-quality PDF using WeasyPrint.

## Usage

```
/book pdf <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`, `book-2`, `book-3`).
- `chNN` — optional. If provided, renders only that chapter; otherwise renders the whole book (all `chNN.md` concatenated, with a title page).

## Output

- single chapter → `chapters/<book>/pub/chNN.pdf`
- whole book → `chapters/<book>/pub/<book>.pdf`

The `pub/` subdirectory (shared with `/book epub` — rendered publication artifacts live together) is created automatically. The user's project should add `chapters/*/pub/` to its `.gitignore` (one-time project-side setup; not the skill's responsibility) — the artifacts are compiled output, regenerable from the Markdown sources.

## Steps

1. Verify `chapters/<book>/` exists in the project working directory. If missing, stop and tell the user.
2. Run the build script (self-bootstraps Python deps via `uv` shebang — first invocation resolves them and caches the env; subsequent runs are instant):
   ```
   ~/.claude/skills/book/scripts/build_pdf.py <project_root>/chapters/<book> [--chapter chNN]
   ```
3. The script prints `wrote <path>` on success — surface that path to the user.
4. If invocation fails with `command not found: uv` (or equivalent), surface the install hint and stop:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Do NOT attempt to install dependencies automatically.

## Metadata (optional `meta.yaml`)

`build_pdf.py` reads four keys from `chapters/<book>/meta.yaml` — the same file `/book epub` reads:

```yaml
title: The Real Title of the Book
subtitle: Book One
author: Author Name
language: it-IT
```

All keys are optional. `title` and `subtitle` set the title page; without them the title falls back to `outline.md`'s first `# ...` heading, which is an internal-doc heading and not the book title.

`language` is the one with an effect on every page. It becomes the `lang` attribute of the rendered document, and `book.css` justifies every paragraph with `hyphens: auto` — WeasyPrint hyphenates only when the document declares a language. Set it wrong and the text hyphenates by the wrong dictionary; omit it and the default `en` applies, which for a book in another language means justified text that never breaks a word and opens the word spacing to fill the line.

## Notes

- Typography lives in `~/.claude/skills/book/scripts/book.css` (A5, Georgia 11pt, justified, drop-cap, scene-break ornament, page numbers). Edit that file to adjust look-and-feel — no code changes needed.
- Whole-book mode takes the title from `meta.yaml` when present, else the first `# ...` heading of `chapters/<book>/outline.md`, else the directory name.
- Chapter order in whole-book mode is `sorted(glob("ch*.md"))` — names like `ch01.md`, `ch02.md`, ... must be zero-padded for correct ordering.
- This command is on-demand: it is NOT part of the canonical writing pipeline (init / setup / coherence / write / review / proofread / revise / compact / continuity).
