# `/book judge` — Cross-Model Chapter Comparator

This command ranks N parallel chapter drafts of the same outline beat against a brilliance-oriented rubric, in a model-agnostic way. **Output is a strict JSON file written to the path passed as the second argument — no prose, no commentary, no explanations outside the JSON inside the file.** Aggregation downstream parses the file with `jq` and will fail on extraneous content.

You are one of 4 judges (codex / Anthropic Claude / Gemini / DeepSeek) participating in an ensemble. Your rankings will be combined via Borda count. Output **rank-only** — never absolute scores — because different judges have different score calibrations and a `7/10` from one model is not the same as a `7/10` from another.

> This is the **Claude** judge variant. The Codex variant of the same rubric is the codex-side `book` skill (`codex/SKILL.md` in the skill repo, installed to `~/.codex/skills/book/`); the two bodies are identical except for the hardcoded lane-identification table.

## Invocation

```
/book judge <manifest-path> <output-path>
```

`<output-path>` is the absolute path of a file you must create (or overwrite) with the JSON described under "Output schema" below. Do not print the JSON to stdout — write it to the file. Use your Write tool. After writing, you may print a one-line status message confirming the file path and byte size; nothing else.

The manifest is a JSON file with shape:
```json
{
  "book": "book-1",
  "chapter": "ch01",
  "drafts": [
    {"id": "A", "path": "/abs/path/to/draft-A/ch01.md"},
    {"id": "B", "path": "/abs/path/to/draft-B/ch01.md"},
    {"id": "C", "path": "/abs/path/to/draft-C/ch01.md"}
  ]
}
```

The current working directory is the project root.

## Protocol

1. **Read every draft in full, in alphabetical id order (A → B → C → ...), before scoring any dimension.** Do not partially read one draft and start ranking. You must have the whole manuscript of each draft in mind before judging any axis. This avoids primacy/recency and order-bias artifacts.

2. **Read these rubric files** (paths relative to project root):
   - `world/writing-checklists.md` — sensory anchor expectations per level
   - `world/pacing-rules.md` — pacing rules
   - `world/prose-rules.md` — prose-quality patterns
   - `world/tones.md` — Dome/Ark/Reality registers
   - `characters/notes/voice-samples.md` — POV character voice samples
   - `chapters/<book>/outline.md` — outline beats for the specific chapter (the section matching `<chapter>`)

3. **Rank the N drafts on each of the 10 dimensions below.** Strict ranking, no ties — if you genuinely cannot separate two drafts on a dimension, pick the one you would marginally favor and move on. Ties poison Borda aggregation.

4. **Produce an `overall_ranking`** — your holistic synthesis. This is NOT a numeric sum of per-dimension ranks; it is your best judgment of "which draft I would publish first, second, last." Per-dimension rankings inform but do not mechanically determine `overall_ranking`.

5. **Extract anchors from losers.** For each draft ranked 2nd-or-worse in `overall_ranking`, identify 1–3 specific micro-elements where it BEATS the overall winner. An anchor is a concrete, liftable handle — a line, an image, a structural move, an outline-beat execution. **If a loser has no observable advantage, output zero anchors for it. Do not pad.**

6. **Write strict JSON to `<output-path>`.** Use your Write tool. Do not print the JSON to stdout — only a one-line confirmation.

## The 10 dimensions

### Canonical compliance (5)

1. **voice** — POV character voice match. Compare each draft's POV passages against the samples in `characters/notes/voice-samples.md`. Rank by faithfulness to the character's diction, syntactic tics, mental texture.

2. **sensory** — Level-appropriate sensory anchor density per `world/writing-checklists.md`. Rank by which draft hits the level's sensory palette most fully without overstuffing or genericism.

3. **pacing** — Adherence to `world/pacing-rules.md`. Rank by which draft's rhythm, scene-length distribution, and breath placement best matches the rules.

4. **tone** — Register fidelity per `world/tones.md` (Dome / Ark / Reality each have distinct registers). Rank by which draft sustains the correct register most consistently.

5. **beats_execution** — Quality of outline beats per `chapters/<book>/outline.md`. Each draft converged so all beats are present; rank by *execution quality* — which draft lands each beat with the most force, the cleanest setup, the strongest payoff.

### Brilliance (5)

6. **memorable_lines** — Count and quality of lines that would survive being quoted out of context (epigraph, pull-quote, embedded in another text). Rank by N-of-strong-lines per draft.

7. **surprise** — Instances of *intentional* deviation from the rules that work. A pause where pacing says push; an image not required by the checklist that lands; a structural choice that breaks expectation without breaking sense. Rank by intentionality + payoff. Sloppy deviation does not count.

8. **subtext** — Density of unsaid-but-felt. Moments where a character reacts to something not on the page; emotional currents that surface only via implication; tension carried by what is withheld. Rank by depth + integration.

9. **compression** — Passages where one line does the work of a paragraph. Rank by density of high-compression moments. Compression ≠ brevity; it is information-per-word. A short sentence that says nothing is not compressed.

10. **ai_prose_penalty** — Count of generic LLM cadences: triadic rhythms ("X, Y, and Z" stacking three abstract nouns), "non solo X ma anche Y" frames, conclusory sentences that summarize the scene's emotional state for the reader, overuse of "the way..." constructions, abstract-noun-soup transitions, perfectly balanced paragraph endings. **Higher count = WORSE.** Rank with the cleanest draft (lowest count) at 1°.

## Anchor schema

Each anchor object:
```json
{
  "from": "A",
  "type": "concept|line|image|move|beat",
  "excerpt": "literal text, or a paragraph reference if too long to quote",
  "rationale": "one sentence on why this beats the winner on this micro-element"
}
```

Types:
- `concept` — a framing/idea (e.g. "the box opens with the same gesture as a hospital cabinet" — a thematic pairing the others miss)
- `line` — a quotable sentence
- `image` — a specific sensory rendering
- `move` — a structural choice (a pause, a transition, a beat-break, a sentence-fragment paragraph that works)
- `beat` — an outline beat executed better in a loser draft

## Output schema (strict)

```json
{
  "judge_id": "claude-default | openrouter-deepseek | openrouter-gemini",
  "model": "claude-opus-4-7 | deepseek-v4-pro | gemini-3.1-pro",
  "book": "book-1",
  "chapter": "ch01",
  "rankings_per_dimension": {
    "voice":             ["B","A","C"],
    "sensory":           ["A","B","C"],
    "pacing":            ["A","B","C"],
    "tone":              ["A","B","C"],
    "beats_execution":   ["A","B","C"],
    "memorable_lines":   ["A","B","C"],
    "surprise":          ["A","B","C"],
    "subtext":           ["A","B","C"],
    "compression":       ["A","B","C"],
    "ai_prose_penalty":  ["A","B","C"]
  },
  "overall_ranking": ["B","A","C"],
  "anchors_from_losers": [
    {"from": "A", "type": "line",  "excerpt": "...", "rationale": "..."},
    {"from": "C", "type": "image", "excerpt": "...", "rationale": "..."}
  ]
}
```

**Hardcoded lane identification** — pick `judge_id` and `model` from this table (check env vars; if uncertain, default to claude-default):

| Detect | judge_id | model |
|---|---|---|
| `$ANTHROPIC_BASE_URL` unset (or empty) | `claude-default` | `claude-opus-4-7` |
| `$ANTHROPIC_MODEL` contains `deepseek` | `openrouter-deepseek` | `deepseek-v4-pro` |
| `$ANTHROPIC_MODEL` contains `gemini` | `openrouter-gemini` | `gemini-3.1-pro` |

Emit these canonical values verbatim — do NOT emit OpenRouter slugs like `google/gemini-3.1-pro-preview` or full provider paths. The downstream aggregator keys on `judge_id`; non-canonical values break the dedup of anchor pools and the Borda consensus computation.

## Self-check before writing

Before writing to `<output-path>`, verify:
- Valid JSON (matched brackets/quotes, no trailing commas)
- Each per-dimension array contains every draft id exactly once
- `overall_ranking` contains every draft id exactly once
- All anchors reference a `from` id that is NOT the overall winner
- No anchor has an empty `excerpt` or `rationale`

Fix the JSON before writing if any check fails. The file content must be the JSON only — no surrounding text, no markdown fences.
