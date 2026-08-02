#!/usr/bin/env bash
set -euo pipefail

# book skill installer
# Copies the skill files into ~/.claude/skills/book/.
#
# Local mode:  ./install.sh [OPTIONS]
# Remote mode: bash <(curl -fsSL https://raw.githubusercontent.com/Ymx1ZQ/book-writer/main/install.sh)

REPO_URL="${BOOK_REPO_URL:-https://github.com/Ymx1ZQ/book-writer.git}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FORCE=false
CHECK=false
CLEANUP_DIR=""

cleanup_temp() {
    if [ -n "$CLEANUP_DIR" ] && [ -d "$CLEANUP_DIR" ]; then
        rm -rf "$CLEANUP_DIR"
    fi
}
trap cleanup_temp EXIT

usage() {
    cat <<'EOF'
Usage: ./install.sh [OPTIONS]

Install the `book` skill into ~/.claude/skills/book/.

OPTIONS:
  --force   Overwrite existing installation without prompting; also skip the
            interactive dependency-warning prompt.
  --check   Compare the installed payload (claude + codex judge variant) against
            the source (no writes); exit 1 and report DRIFT on a difference or
            missing install.
  --help    Show this help message

REMOTE INSTALL (no clone needed):
  bash <(curl -fsSL https://raw.githubusercontent.com/Ymx1ZQ/book-writer/main/install.sh)

ENVIRONMENT:
  BOOK_REPO_URL   Override the repo URL used in remote mode
                  (default: https://github.com/Ymx1ZQ/book-writer.git)
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        --force) FORCE=true; shift ;;
        --check) CHECK=true; shift ;;
        --help|-h) usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
    esac
done

# --- Resolve source: local checkout or remote clone ---

if [ -f "$SCRIPT_DIR/SKILL.md" ] && [ -d "$SCRIPT_DIR/instructions" ]; then
    SRC_ROOT="$SCRIPT_DIR"
else
    if ! command -v git >/dev/null 2>&1; then
        echo "Error: git is required for remote install but is not on \$PATH." >&2
        exit 1
    fi
    CLEANUP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/book-install-XXXXXX")"
    echo "Cloning book-writer into temporary directory..."
    git clone --depth 1 --quiet "$REPO_URL" "$CLEANUP_DIR/repo"
    SRC_ROOT="$CLEANUP_DIR/repo"
    if [ ! -f "$SRC_ROOT/SKILL.md" ]; then
        echo "Error: SKILL.md not found in the cloned repo." >&2
        exit 1
    fi
fi

DEST="$HOME/.claude/skills/book"
CODEX_DEST="$HOME/.codex/skills/book"
# Phase 101 M9 (ground-truth) — third target. The two OpenRouter judge lanes
# (DeepSeek, Gemini) run under opencode rather than Claude Code, because
# OpenRouter takes provider routing and reasoning effort as request-BODY fields
# that Claude Code's Anthropic-shaped path cannot send. Same judge-only
# SKILL.md as the codex variant: it already describes itself as one lane of a
# four-model ensemble and names all four families, so it needs no per-CLI fork.
OPENCODE_DEST="$HOME/.config/opencode/skills/book"

# --- Drift check (no writes) ---

if [ "$CHECK" = true ]; then
    STATUS=0
    check_path() {  # <src> <dest> <label>
        if [ ! -e "$2" ]; then
            echo "DRIFT: $3 not installed at $2"; STATUS=1; return
        fi
        local out
        out="$(diff -r --exclude=__pycache__ --exclude='*.pyc' --exclude=.installed-from "$1" "$2" 2>&1)" || true
        if [ -n "$out" ]; then
            echo "DRIFT: $3 differs from source ($2):"; echo "$out" | head -10; STATUS=1
        else
            echo "OK: $3 matches source ($2)"
        fi
    }
    check_path "$SRC_ROOT/SKILL.md"      "$DEST/SKILL.md"      "claude SKILL.md"
    check_path "$SRC_ROOT/instructions"  "$DEST/instructions"  "claude instructions/"
    [ -d "$SRC_ROOT/scripts" ] && check_path "$SRC_ROOT/scripts" "$DEST/scripts" "claude scripts/"
    if [ -f "$SRC_ROOT/codex/SKILL.md" ]; then
        check_path "$SRC_ROOT/codex/SKILL.md" "$CODEX_DEST/SKILL.md" "codex judge SKILL.md"
        check_path "$SRC_ROOT/codex/SKILL.md" "$OPENCODE_DEST/SKILL.md" "opencode judge SKILL.md"
    fi
    exit "$STATUS"
fi

# --- Dependency probes (UX layer; the skill installs even if missing) ---

MISSING=()
command -v python3 >/dev/null 2>&1 || MISSING+=("python3")
command -v uv >/dev/null 2>&1 || MISSING+=("uv  (https://docs.astral.sh/uv/getting-started/installation/ — needed for /book pdf and /book epub)")

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "Warning — missing dependencies on \$PATH:"
    for m in "${MISSING[@]}"; do
        echo "  - $m"
    done
    echo ""
    echo "Core /book commands (init, setup, write, review, ...) work without these."
    echo "Only /book pdf and /book epub need uv; Python deps (markdown, weasyprint,"
    echo "ebooklib, pyyaml) are auto-resolved by uv at first run via PEP 723 inline"
    echo "script metadata."
    if [ "$FORCE" != true ]; then
        echo ""
        printf "Continue installing? [y/N] "
        read -r reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 0
        fi
    fi
fi

# --- Confirm overwrite if not --force ---

if [ -d "$DEST" ] && [ "$FORCE" != true ]; then
    printf "book skill already exists at %s\nOverwrite? [y/N] " "$DEST"
    read -r reply
    if [[ ! "$reply" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# --- Install: copy only the runtime payload ---

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"

cp "$SRC_ROOT/SKILL.md" "$DEST/SKILL.md"
[ -f "$SRC_ROOT/README.md" ] && cp "$SRC_ROOT/README.md" "$DEST/README.md"
cp -r "$SRC_ROOT/instructions" "$DEST/instructions"
[ -d "$SRC_ROOT/scripts" ] && cp -r "$SRC_ROOT/scripts" "$DEST/scripts"

# Make Python build scripts executable (defensive)
[ -f "$DEST/scripts/build_pdf.py" ] && chmod +x "$DEST/scripts/build_pdf.py"
[ -f "$DEST/scripts/build_epub.py" ] && chmod +x "$DEST/scripts/build_epub.py"

# Stamp the source git short SHA so "what version is deployed?" has an answer.
SRC_SHA="$(git -C "$SRC_ROOT" rev-parse --short HEAD 2>/dev/null || true)"
[ -n "$SRC_SHA" ] && printf '%s\n' "$SRC_SHA" > "$DEST/.installed-from"

echo ""
echo "Installed book skill → $DEST"

# --- Codex-side install: the `judge` subcommand (cross-CLI merge-phase lane) ---
# The `book` pipeline is a Claude Code skill; under Codex the skill exposes only
# the `judge` subcommand (the codex lane of the parallel-pipeline judge ensemble).
if [ -f "$SRC_ROOT/codex/SKILL.md" ]; then
    rm -rf "$CODEX_DEST"
    mkdir -p "$CODEX_DEST"
    cp "$SRC_ROOT/codex/SKILL.md" "$CODEX_DEST/SKILL.md"
    [ -d "$SRC_ROOT/codex/agents" ] && cp -r "$SRC_ROOT/codex/agents" "$CODEX_DEST/agents"
    [ -n "$SRC_SHA" ] && printf '%s\n' "$SRC_SHA" > "$CODEX_DEST/.installed-from"
    echo "Installed book skill (codex variant — judge subcommand) → $CODEX_DEST"

    # opencode gets the same judge-only skill: it is the CLI for the two
    # OpenRouter lanes, which need body-level provider routing.
    rm -rf "$OPENCODE_DEST"
    mkdir -p "$OPENCODE_DEST"
    cp "$SRC_ROOT/codex/SKILL.md" "$OPENCODE_DEST/SKILL.md"
    [ -n "$SRC_SHA" ] && printf '%s\n' "$SRC_SHA" > "$OPENCODE_DEST/.installed-from"
    echo "Installed book skill (opencode variant — judge subcommand) → $OPENCODE_DEST"
fi

echo ""
echo "Run /book help in Claude Code for the full command list."
