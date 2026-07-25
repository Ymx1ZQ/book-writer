# The Three Registers

One planned element is recorded in up to three places, by different commands at different times. Each register is authoritative for its own column and for nothing else; nothing keeps them consistent unless a check does.

| Register | Lives in | Says | Written by | Checked by |
|---|---|---|---|---|
| `## Usage Tracker` | the canon file that owns the element | this element belongs in B1 Ch.07 | `/book setup`, `/book fix`; `/book chapter` Step 5.5 sets `planned` → `written` | `chapter-writer.md` 2.6.c, `coherence-check.md` K, `fidelity.md` class (d) |
| `**context:**` list | the chapter's header in `chapters/<book>/outline.md` | to write B1 Ch.07, load these files | the outline author; `/book chapter` 2.6.a and 2.6.c auto-add | `chapter-writer.md` 2.6.a/2.6.b, `coherence-check.md` K, R, S |
| §Inline Plant Tracking | one table in the book's outline header | this element recurs at #1 Ch.05, #2 Ch.12, #3 Ch.14, #4 Ch.19 | the outline author; `/book fix` on a Chekhov finding | `coherence-check.md` J, `chapter-writer.md` 2.6.c, `fidelity.md` class (e) |

**Reachability set — the rule binding tracker to context.** A chapter reaches a canon file if the file is in the always-loaded set, in the texture-palette proxy, in the chapter's `**context:**` list, **or** in the chapter's own level directory (`world/level-<N>-<this chapter's level>/`) carrying a `## Usage Tracker` row for this Book+Ch. A row whose owning file is outside all four routes for its target chapter can be neither rendered nor ticked.

The first two routes are declared in the outline header §Context Tags and parsed from it at run time, never hardcoded by a consumer. The fourth is a rule rather than a list: `chapter-writer.md` Step 1 lists the chapter's own level directory and opens exactly the files whose tracker rows name this Book+Ch, so those rows need no `context:` entry and 2.6.c does not auto-add them. Every other tracker row does need one — `world/` root files, `plot/` and `characters/` are reached by no rule, and a root file owning a recurring element is unreachable from every chapter that renders it until each one lists it.

The `**context:**` list is therefore authoritative for the chapter's conditional files, not a record of everything the chapter loads.

**Tools that compute reachability.** A project-side script implementing this model must implement all four routes. A three-route implementation reports level-directory rows as unreachable: in `ground-truth`, `chapter-load.py --unreachable` reported 314 rows of which 226 were reachable through the fourth route.

**Level register.** The chapter's `**Level:**` decides which level-scoped directories are legal for it, and outranks the other two registers: a barred file is reported, never auto-added, whatever a tracker row or a plant instance says. A row in a *different* level's directory is reachable by no route — the fix is to move the content or retarget the row, never to add a `context:` entry. → `chapter-writer.md` §Level register.

**Plant-table shape.** One row per plant, one column per chapter carrying an instance; cells numbered `#1`, `#2`, … in chapter order and naming how the instance appears; `—` for no instance; the payoff instance marked as the payoff. A plant carries more than one instance before its payoff — a reader who meets an element once does not retrieve it twenty chapters later. → `init.md` for the scaffold, `coherence-check.md` J for the instance-count and gap checks.
