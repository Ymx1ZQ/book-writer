"""Frontmatter convention (DEVPLAN Phase 18).

Root SKILL.md is the ONLY frontmatter carrier (agentskills.io: name +
description). instructions/*.md files carry no YAML frontmatter and open
with an H1 title. No external YAML dependency: the block is checked with
line-level parsing so the suite stays stdlib-only (CI installs pytest only).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
INSTRUCTIONS = ROOT / "instructions"


def _frontmatter_lines(text: str) -> list[str]:
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", "SKILL.md must open with ---"
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:i]
    raise AssertionError("SKILL.md frontmatter block is not closed by ---")


def _key_has_value(fm: list[str], key: str) -> bool:
    """True if `key:` carries a non-empty inline value, or (block-scalar
    style: >-, |, etc.) a non-empty indented continuation line."""
    for i, line in enumerate(fm):
        if not line.startswith(f"{key}:"):
            continue
        inline = line.split(":", 1)[1].strip()
        if inline and inline not in (">", ">-", ">+", "|", "|-", "|+"):
            return True
        return i + 1 < len(fm) and fm[i + 1].startswith(" ") and bool(fm[i + 1].strip())
    return False


def test_skill_md_frontmatter_valid():
    fm = _frontmatter_lines(SKILL.read_text(encoding="utf-8"))
    assert _key_has_value(fm, "name"), "SKILL.md frontmatter needs a non-empty name"
    assert _key_has_value(fm, "description"), "SKILL.md frontmatter needs a non-empty description"


def test_instruction_files_have_no_frontmatter():
    offenders = [
        p.relative_to(ROOT)
        for p in sorted(INSTRUCTIONS.rglob("*.md"))
        if p.read_text(encoding="utf-8").lstrip().startswith("---")
    ]
    assert not offenders, f"instruction files must not carry frontmatter: {offenders}"


def test_instruction_files_open_with_h1():
    offenders = []
    for p in sorted(INSTRUCTIONS.glob("*.md")):
        first = next((l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()), "")
        if not first.startswith("# "):
            offenders.append(p.relative_to(ROOT))
    assert not offenders, f"instruction files must open with an H1 title: {offenders}"
