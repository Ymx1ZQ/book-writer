"""Tests for the graph-recall doctrine and who is wired to it.

The graph is an optional accelerator: consumers query it instead of loading
canon in bulk. Three invariants keep that from going wrong, and each one has
already failed once in the field:

1. **coldread-enum must never consume it.** It is canon-blind by design, and
   that constraint is the check — it simulates a reader who knows only what the
   book has told them. Measured on ground-truth ch10 (2026-08-02) it returned 40
   findings on a chapter where six canon-aware detectors each returned zero. A
   later pass "completing the rollout" would wire it up and quietly delete that
   capability, so the exclusion is asserted here. The doctrine has carried a
   §Canon-blind exclusions section since Phase 40 — these tests pin it rather
   than restating it elsewhere, which is the mistake the first draft of this
   file made.

2. **The freshness gate must count only what the graph contains.** It globbed
   world/ characters/ plot/ chapters/ wholesale, so process ledgers the pipeline
   rewrites at every step marked the graph stale: six of the eight files that
   did so after the ch10 merge were ledgers. Every consumer fell back to
   whole-file loading, silently.

3. **Declared consumers and cross-referencing files must agree.** graph-recall
   is the single source of truth; a file that queries the graph without
   appearing in the consumer list is a doctrine that does not know its own
   readers.
"""
from __future__ import annotations

import re
from pathlib import Path

INSTRUCTIONS = Path(__file__).resolve().parent.parent / "instructions"
RECALL = INSTRUCTIONS / "graph-recall.md"

EXPECTED_CONSUMERS = {
    "chapter-writer", "coherence-check", "continuity-check", "motif",
    "adjacency", "fidelity", "sniff", "reviewer",
    # Added 2026-08-02: each does a corpus-wide lookup the graph can serve.
    "factcheck", "sensitivity", "coldread-filter", "readability",
}

# Never wire these. See the module docstring and graph-recall's own section.
FORBIDDEN_CONSUMERS = {"coldread-enum", "judge"}

# Ledger and build paths the graph does not index, so the gate must not count
# them. Kept in step with the consuming project's .graphifyignore.
GATE_EXCLUSIONS = ["SMELL", "REVIEW", "PROOFREAD", "COLDREAD",
                   "DEVPLAN", "archive", "coldread-state", "pub"]


def recall_text() -> str:
    return RECALL.read_text(encoding="utf-8")


def consumer_list() -> set[str]:
    """The names inside the opening paragraph's `Consumers (...)` parenthetical.

    Parsed from that parenthetical specifically, not from "everything before
    the exclusions heading": an earlier version did the latter, and when the
    heading was absent it silently fell back to scanning the whole file and
    reported coldread-enum as a declared consumer. A test that fails for the
    wrong reason is worse than no test.
    """
    text = recall_text()
    m = re.search(r"Consumers \(([^)]*)\)", text)
    assert m, "graph-recall.md has no `Consumers (...)` declaration"
    return {x.group(1) for x in re.finditer(r"`([a-z-]+)\.md`", m.group(1))}


# --- (1) the canon-blind invariant ---

def test_coldread_enum_is_never_a_declared_consumer():
    assert "coldread-enum" not in consumer_list()


def test_coldread_enum_does_not_query_the_graph():
    body = (INSTRUCTIONS / "coldread-enum.md").read_text(encoding="utf-8")
    assert "graphify query" not in body
    assert "graph-recall" not in body


def test_coldread_enum_still_declares_itself_canon_blind():
    # The exclusion above is only justified while this holds. If the skill ever
    # stops being canon-blind, the exclusion needs re-deciding, not preserving.
    body = (INSTRUCTIONS / "coldread-enum.md").read_text(encoding="utf-8")
    assert "canon-blind by design" in body


def test_the_exclusions_are_written_down_with_reasons():
    text = recall_text()
    assert "## Canon-blind exclusions" in text
    excl = text.split("## Canon-blind exclusions")[1].split("\n## ")[0]
    for name in FORBIDDEN_CONSUMERS:
        assert name in excl, f"{name} exclusion is not in the exclusions section"
    # A bare list would not survive a future rollout pass; the reasons must be there.
    assert "canon-blindness" in excl or "canon-blind" in excl
    assert "outside Claude Code" in excl, "the judge lane reason is not recorded"
    assert "enumerate blind, triage informed" in excl


# --- (2) the freshness gate counts only indexed files ---

def test_gate_excludes_every_ledger_class():
    text = recall_text()
    gate = text.split("## Freshness gate")[1].split("##")[0]
    for token in GATE_EXCLUSIONS:
        assert token in gate, f"gate does not exclude {token}"


def test_gate_still_scopes_to_canon_directories():
    gate = recall_text().split("## Freshness gate")[1].split("##")[0]
    for d in ("world/", "characters/", "plot/", "chapters/"):
        assert d in gate


def test_gate_and_graphifyignore_are_declared_as_one_decision():
    # The two lists drift apart silently otherwise: a file the graph indexes but
    # the gate ignores goes stale unnoticed.
    text = recall_text()
    assert ".graphifyignore" in text
    assert "Change one, change the other." in text


# --- (3) declared consumers match reality ---

def test_declared_consumers_are_exactly_the_expected_set():
    declared = consumer_list()
    assert declared == EXPECTED_CONSUMERS, (
        f"missing: {EXPECTED_CONSUMERS - declared} | "
        f"unexpected: {declared - EXPECTED_CONSUMERS}"
    )


def test_every_declared_consumer_cross_references_the_doctrine():
    for name in sorted(EXPECTED_CONSUMERS):
        f = INSTRUCTIONS / f"{name}.md"
        assert f.exists(), f"{name}.md does not exist"
        body = f.read_text(encoding="utf-8")
        assert "graph-recall" in body, f"{name}.md does not cross-reference the doctrine"


def test_no_undeclared_file_queries_the_graph():
    declared = consumer_list()
    for f in sorted(INSTRUCTIONS.glob("*.md")):
        if f.name == "graph-recall.md":
            continue
        body = f.read_text(encoding="utf-8")
        if "graphify query" in body:
            assert f.stem in declared, (
                f"{f.name} queries the graph but is not a declared consumer"
            )


def test_new_consumers_declare_index_mode():
    # Answer mode is forbidden on a stale graph; index mode can never serve
    # stale content because the disk read is the final word. All four additions
    # are lookups, so all four are index mode.
    for name in ("factcheck", "sensitivity", "coldread-filter", "readability"):
        body = (INSTRUCTIONS / f"{name}.md").read_text(encoding="utf-8")
        assert "index mode" in body.lower(), f"{name}.md does not declare its mode"
