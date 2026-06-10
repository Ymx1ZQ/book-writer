#!/usr/bin/env bash
set -euo pipefail

# Install smoke for the book skill (Phase 15 M1 + M3).
# Run: bash tests/test_install.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_SH="$REPO_ROOT/install.sh"
PASS=0
FAIL=0

assert_file() { if [ -f "$1" ]; then echo "  PASS: $2"; PASS=$((PASS+1)); else echo "  FAIL: $2 — missing $1"; FAIL=$((FAIL+1)); fi; }
assert_dir()  { if [ -d "$1" ]; then echo "  PASS: $2"; PASS=$((PASS+1)); else echo "  FAIL: $2 — missing $1"; FAIL=$((FAIL+1)); fi; }
assert_exec() { if [ -x "$1" ]; then echo "  PASS: $2"; PASS=$((PASS+1)); else echo "  FAIL: $2 — not executable $1"; FAIL=$((FAIL+1)); fi; }

assert_run() {  # <expected_exit> <needle> <label> -- <args...>
    local exp="$1" needle="$2" label="$3"; shift 3; [ "$1" = "--" ] && shift
    local out rc=0
    out="$(env HOME="$H" bash "$INSTALL_SH" "$@" 2>&1)" || rc=$?
    if [ "$rc" -eq "$exp" ] && printf '%s' "$out" | grep -qF "$needle"; then
        echo "  PASS: $label"; PASS=$((PASS+1))
    else
        echo "  FAIL: $label — exit=$rc (want $exp); output:"; printf '%s\n' "$out" | head -4; FAIL=$((FAIL+1))
    fi
}

echo "=== install smoke ==="
H="$(mktemp -d)"
trap 'rm -rf "$H"' EXIT
env HOME="$H" bash "$INSTALL_SH" --force >/dev/null 2>&1

D="$H/.claude/skills/book"
assert_file "$D/SKILL.md"                 "claude: SKILL.md installed"
assert_dir  "$D/instructions"             "claude: instructions/ installed"
assert_file "$D/instructions/writer.md"   "claude: an instruction file landed"
assert_dir  "$D/scripts"                  "claude: scripts/ installed"
assert_exec "$D/scripts/build_pdf.py"     "claude: build_pdf.py executable"
assert_exec "$D/scripts/build_epub.py"    "claude: build_epub.py executable"

CD="$H/.codex/skills/book"
assert_file "$CD/SKILL.md"                "codex: judge variant SKILL.md installed"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ]
