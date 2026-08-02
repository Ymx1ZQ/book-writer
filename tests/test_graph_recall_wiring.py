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


# --- (4) no instruction may name a synthetic per-chapter node id ---
#
# fidelity.md queried `chapters_book_N_outline_chNN` against
# `chapters_book_N_chNN` for months. Neither id has ever existed in a built
# graph, so its triage never ran, and the step's own "node missing -> skip
# silently" clause meant nothing reported it. Measured on a freshly rebuilt
# ground-truth graph (5,965 nodes, 182/182 documents): rendered prose gets
# 19-47 nodes per chapter file reliably, while outline granularity differs
# BETWEEN BOOKS from the same run -- book-3 got per-chapter nodes, book-1 got
# zero. So the id cannot be repaired by renaming; the planned side is read from
# disk instead.

SYNTHETIC_CHAPTER_NODE = re.compile(r"`?chapters_book_[N\d]+_(outline_)?ch(NN|\d+)`?")


def test_no_instruction_names_a_synthetic_per_chapter_node_id():
    offenders = []
    for f in sorted(INSTRUCTIONS.glob("*.md")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not SYNTHETIC_CHAPTER_NODE.search(line):
                continue
            # The prohibition itself has to name the shape to forbid it.
            if "Do not reintroduce" in line or "never existed" in line:
                continue
            offenders.append(f"{f.name}:{i}")
    assert not offenders, (
        "these lines name a per-chapter graph node id that the extractor does "
        f"not produce: {offenders}"
    )


def test_fidelity_reads_the_planned_side_from_disk():
    body = (INSTRUCTIONS / "fidelity.md").read_text(encoding="utf-8")
    assert "Read it from disk, never query it" in body
    # And says why, so the next author does not "optimise" it back into a query.
    assert "inconsistent between books" in body.lower()


def test_gate_forbids_deriving_freshness_from_the_manifest():
    # graphify-out/manifest.json lists every path ever scanned, including those
    # .graphifyignore keeps out of the graph, so comparing it against disk
    # reports ledgers as changes to a graph that never held them. A fidelity run
    # on 2026-08-02 did exactly that and reported "stale - 128 content files
    # changed" eleven minutes after a rebuild, with the git gate returning 0.
    gate = recall_text().split("## Freshness gate")[1].split("\n## ")[0]
    assert "manifest.json" in gate
    assert "never derive freshness" in gate.lower()


# --- (5) Phase 30 — a skip that narrows coverage must be declared ---
#
# Three defects over 2026-08-01/02 were invisible for as long as they existed,
# all hidden by the same construct: revise skipped by a guard that matched
# nothing, fidelity's triage querying nodes that never existed, a session-limit
# probe reading a file nobody writes. None produced an error. The countermeasure
# that worked within one run was making the step declare which path it took.

SKIP_DECLARERS = {
    "fidelity", "coherence-check", "adjacency", "reviewer", "factcheck",
    "sensitivity", "readability", "coldread-filter", "motif", "continuity-check",
}


def test_the_skip_declaration_doctrine_exists_and_carries_its_evidence():
    f = INSTRUCTIONS / "skip-declaration.md"
    assert f.exists()
    body = f.read_text(encoding="utf-8")
    # The rule without the measurements is a preference; with them it is a finding.
    assert "revise skipped" in body or "revise` skipped" in body
    assert "node ids no graph has ever produced" in body
    assert "reads a file nothing writes" in body or "read a file nothing writes" in body
    # And it must say what it is NOT, or it reads as permission to skip.
    assert "not a licence to skip" in body.lower()


def test_every_skipping_detector_references_the_contract():
    missing = []
    for name in sorted(SKIP_DECLARERS):
        f = INSTRUCTIONS / f"{name}.md"
        assert f.exists(), f"{name}.md does not exist"
        if "skip-declaration.md" not in f.read_text(encoding="utf-8"):
            missing.append(name)
    assert not missing, f"these detectors can skip but do not declare it: {missing}"


def test_coldread_enum_is_not_asked_to_declare_a_graph_skip():
    # It has no graph path to skip, and adding the contract there would imply
    # one exists. Its canon-blindness is a property, not a skipped path.
    body = (INSTRUCTIONS / "coldread-enum.md").read_text(encoding="utf-8")
    assert "skip-declaration.md" not in body
