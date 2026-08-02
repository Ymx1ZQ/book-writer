# `/book factcheck` — active real-world accuracy pass

Extract every real-world factual claim in the chapter and **actively verify it** — against the project's canon and against real-world knowledge — instead of waiting for one to *look* suspicious. This is the dedicated batch verifier; `sniff` §5/§5.a is the reactive in-prose guardrail. Together they close the gap through which a plausible-sounding but factually wrong detail ships unchallenged.

## What this check is, and what it is NOT

| What | Where it lives |
|---|---|
| Reactive "this specific detail smells wrong" flag, line-by-line | `sniff.md` §5 / §5.a |
| In-world numbers implying an undefined system | `sniff.md` §3 + `coherence-check.md` §System-audit |
| Anachronism as a nose-wrinkle | `sniff.md` §1 |
| **Systematic extract-every-claim → verify each → declare the verdict** | **THIS check** |

The difference from sniff §5.a is *posture*: sniff flags what looks suspicious as it scans (reactive, charitable to unflagged claims); factcheck **enumerates the full claim set first**, then adjudicates each, so a confidently-worded falsehood cannot pass by simply not looking suspicious. **Do not duplicate** sniff's per-line objections; this pass produces a claim ledger and routes only the claims that fail or cannot be verified.

**Milestone format:** see `instructions/milestone-format.md`. Routing: prose-fixable falsehood → `SMELL.md` (`Source: factcheck`, INLINE); in-world override the project should canonicalize → `DEVPLAN.md` (ANCHOR-NEEDED); unverifiable-at-agent → `Flagging: VERIFY` surfaced to `SMELL-PENDING.md` for human/web confirmation.

## Usage

```
/book factcheck <book> [chNN]
```

## Output

**Skip declaration (mandatory — see `instructions/skip-declaration.md`).** Any path this check declines to run — a stale graph, an absent input, a deferred sub-check — is stated in the report below with its reason, on its own line, before the findings. A skip that narrows coverage and is not declared is indistinguishable from a path that is quietly broken; all three defects that rule was written for were found by accident, late.

- Findings → `chapters/<book>/SMELL.md` (`Source: factcheck`); canon → `DEVPLAN.md`.
- A mandatory **"Fact-Check Audit"** section in SMELL.md: the full claim ledger with each claim's bucket.

## Step 0 — Load the reality baseline

**Graph-assisted anchor lookup (optional — gating in `instructions/graph-recall.md`, index mode).** The expensive half of this check is not the enumeration, it is adjudicating each claim against whatever canon anchors it: a chapter can raise twenty external-world claims scattered across `world/`, and finding each one's anchor by reading is what costs. When `graphify-out/graph.json` exists and the freshness gate passes, resolve anchors by query instead:

```bash
graphify query "<claim subject> — where is this anchored in world/ or characters/"
```

**Index mode only: the query returns *pointers*, and every pointer is then read from disk before a verdict.** A claim is never adjudicated from graph content. An empty result is never evidence that no anchor exists — it sends you to the file reads below, which are the authority. Graph absent or stale → this subsection is a no-op and Step 0 proceeds exactly as written.

1. `world/timeline.md` — the in-world year and the macro trajectory (climate, technology, economy, society) from the present-day baseline. Every period-plausibility judgment is relative to this year, not 2024.
2. `world/canon-hierarchy.md` — resolution doctrine for ANCHOR-NEEDED.
3. The level files for the scene's setting, and any `consumer-anchors.md` / economic-anchor files — the real-world numbers the project has already canonicalized (prices, distances, tech availability).

## Procedure — enumerate, then adjudicate

**Phase A — enumerate.** Read the chapter and list **every** assertion that depends on knowledge external to the project's invented canon. Categories to sweep (generic across the trilogy):

- **Places & geography** — real streets, neighborhoods, landmarks, cities, country facts, relative positions, climate. A named real city inherits its real geography unless the project canonicalizes an override.
- **Technology & chains** — model/connector/version names, hardware compatibility, source→display chains, software stacks. Period plausibility: does it exist at the in-world year; was it in actual use then; is the compatibility chain physically realizable in the stated direction.
- **Physics, biology, medicine** — checkable mechanisms (a body doing what the prose says; a dose, an injury, a recovery time; a physical process).
- **Law, finance, economics** — institutions, procedures, prices, currencies, units (judged at the in-world year + trajectory).
- **Language in proper nouns** — French/Italian/Spanish/etc. grammar in named proper nouns (contractions, gender, accents), regardless of in-world terminal capitalization.
- **Brands, dates, units** — real named things must be real.

**Phase B — adjudicate.** Put each enumerated claim in exactly one bucket:

- **Anchored** — supported by a canonical project file. Cite the file. Pass (no finding).
- **Verified (high confidence)** — a real-world fact you can confirm with high confidence (and, with the in-world trajectory applied, remains plausible at the year). Declare it. Pass.
- **Contradicted** — you can confirm with high confidence the claim is wrong (real geography, real physics, real grammar). → finding. INLINE if a prose tweak fixes it; ANCHOR-NEEDED if the project should canonicalize an in-world override (route to DEVPLAN).
- **VERIFY (cannot confirm at agent)** — neither anchored nor confidently real/false; the specificity exceeds your actual confidence. → `Flagging: VERIFY` entry to `SMELL-PENDING.md`. **Do not silently auto-edit** an unverifiable claim, and do not silently pass it — surface it for human/web check.

**Calibration (load-bearing, inherited from sniff §5.a).** Specific-sounding details fail at higher rates than their tone suggests: "model VGA-to-HDMI converter cable", "Rue du Petit Puits". Treat highly-specific technical/geographic assertions with **more** suspicion than general descriptive ones — the failure mode is *plausibly worded → plausibly wrong*. When specificity exceeds confidence, it is VERIFY, not a pass.

## Output — SMELL.md entries

Standard format with `Source: factcheck` and a `Bucket:` field. Example (Contradicted):

```markdown
## #N — <one-line, e.g. "ch01: Rue du Petit Puits placed in Le Panier — real street is in the 2nd, not Le Panier">

- **Source:** factcheck
- **Location:** ch01.md line 30
- **Quote:** "..."
- **Category:** Places & geography
- **Bucket:** Contradicted
- **Verification:** The real Rue du Petit Puits in Marseille is in the 2nd arrondissement; Le Panier (also 2nd, adjacent) is a distinct named quarter — the prose conflates them.
- **Routing:** INLINE   (or ANCHOR-NEEDED if the project wants an in-world override)
- **Flagging:** SAFE-CUT | TRADE-OFF
- **Improvement (if fix applied):** Correct quarter name; the geography now matches a reader who knows Marseille.
- **Loss (if fix applied):** None.
- **Suggested action:** Replace "Le Panier" with the correct quarter, or drop the quarter and keep the street.
```

For **VERIFY** entries, the entry carries `Flagging: VERIFY`, `Routing: INLINE (pending verification)`, and `Suggested action: confirm <claim> against <source type>; if false, <fix>; if true, mark Verified.` revise surfaces VERIFY entries to `SMELL-PENDING.md` (never auto-applies them).

### Fact-Check Audit section (always present)

```markdown
## Fact-Check Audit (Source: factcheck)

In-world year (timeline.md): 2045. Claims enumerated: N.

| # | Claim (short) | Category | Bucket | Note |
|---|---|---|---|---|
| 1 | sardines €2/kg | finance/econ | Contradicted | flagged #N (also sniff §5) |
| 2 | Marseille→Torino by rail | geography | Verified | real corridor; plausible at 2045 |
| 3 | "tier-two filtration" | tech | Anchored | ecology.md §Air Quality |
| 4 | specific drug dosage | medicine | VERIFY | exceeds confidence → SMELL-PENDING |

Buckets: W anchored / X verified / Y contradicted (flagged) / Z VERIFY (surfaced).
```

## Steps for the executing agent

1. Resolve the chapter file. Step 0 — load timeline + anchors + canon-hierarchy.
2. Phase A — enumerate every external-world claim into the ledger.
3. Phase B — adjudicate each into a bucket; for Contradicted, decide INLINE vs ANCHOR-NEEDED; for VERIFY, prepare the surfaced entry.
4. Append SMELL.md entries (`Source: factcheck`, do not overwrite — append) + the Fact-Check Audit ledger.
5. For ANCHOR-NEEDED, append a `## Phase <NN+1> — Factcheck canon fixes (<book> <chNN>)` to DEVPLAN (sniff milestone format; autonomous resolution).
6. Print: `factcheck: enumerated N claims — W anchored / X verified / Y contradicted / Z VERIFY. Appended (Y+Z) entries to SMELL.md; B ANCHOR-NEEDED → DEVPLAN Phase NN.`

## Calibration

- **Enumerate before you judge.** The value of this pass over sniff is completeness — the full ledger, not just what looked wrong.
- **Apply the trajectory.** Every real-world fact is judged at the in-world year with the timeline's climate/tech/economy trajectory applied — not at 2024.
- **VERIFY is a first-class outcome.** Surfacing "I cannot confirm this" is correct and valuable, not a failure to decide. Never auto-edit or silently pass a VERIFY claim.
- **Don't re-do sniff.** If sniff already flagged a claim, reference its entry in the ledger rather than emitting a duplicate; only add what sniff's reactive scan missed.
