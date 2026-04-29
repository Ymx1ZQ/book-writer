# `/book pdf` — render chapters to PDF

Render Markdown chapters to a book-quality PDF using WeasyPrint.

## Usage

```
/book pdf <book> [chNN]
```

- `<book>` — the book directory under `chapters/` (e.g. `book-1`, `book-2`, `book-3`).
- `chNN` — optional. If provided, renders only that chapter; otherwise renders the whole book (all `chNN.md` concatenated, with a title page).

## Output

- single chapter → `chapters/<book>/pdf/chNN.pdf`
- whole book → `chapters/<book>/pdf/<book>.pdf`

The `pdf/` subdirectory is created automatically. The user's project should add `chapters/*/pdf/` to its `.gitignore` (one-time project-side setup; not the skill's responsibility).

## Steps

1. Verify `chapters/<book>/` exists in the project working directory. If missing, stop and tell the user.
2. Run the build script:
   ```
   python3 ~/.claude/skills/book/scripts/build_pdf.py <project_root>/chapters/<book> [--chapter chNN]
   ```
3. The script prints `wrote <path>` on success — surface that path to the user.
4. If the script fails with `ModuleNotFoundError` for `weasyprint` or `markdown`, surface the install hint and stop:
   ```
   pip install --user weasyprint markdown
   ```
   Do NOT attempt to install dependencies automatically.

## Notes

- Typography lives in `~/.claude/skills/book/scripts/book.css` (A5, Georgia 11pt, justified, drop-cap, scene-break ornament, page numbers). Edit that file to adjust look-and-feel — no code changes needed.
- Whole-book mode pulls the title from the first `# ...` heading of `chapters/<book>/outline.md`; falls back to the directory name if `outline.md` is missing or has no top-level heading.
- Chapter order in whole-book mode is `sorted(glob("ch*.md"))` — names like `ch01.md`, `ch02.md`, ... must be zero-padded for correct ordering.
- This command is on-demand: it is NOT part of the canonical writing pipeline (init / setup / coherence / write / review / proofread / revise / compact / continuity).
