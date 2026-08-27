# W8 — THE REVISER'S BLIND SIDE: registration

*Pre-registered BEFORE any W8 run — committed before the first model
call of any kind (seed draws, regime arms, engineering passes). This
file is the contract. Grown from W7 footnote 1 (kimi holds seal+rhyme
solo, broke claude's passing seal as DESC hand-2, recovered both as
ASC hand-3) and W5's first honest miss (last-hand prose falsified at
constraint level).*

## Station

W8-queue Station 1 of 4. Fires FIRST in the queue (its
destruction/spare rates feed W10's arithmetic).

## The question (one)

Why does a hand destroy a constraint it demonstrably holds SOLO when
it revises another mind's draft? W7's framing is the hypothesis to
beat: *"a hand fixes what it notices broken and damages what it
rewrites blind — the draft it receives decides which."*

## The two mechanisms (pre-stated, discriminated by this run)

- **M1 — BLIND-REWRITE:** the reviser verifies what it notices broken
  and rewrites the rest without re-checking. Destruction of a passing
  constraint is collateral of rewriting its carrier lines. Signature:
  destruction probability tracks per-line edit distance on the lines
  that carry the constraint, and is shrinkable by prompt.
- **M2 — REVISION-MODE SWITCH:** revising is a different behavior than
  composing; in revision mode the hand's effective hold-set shrinks
  regardless of how much it rewrites. Signature: destruction
  independent of edit distance, unaffected by any prompt regime. (A
  model-class wall, not a workflow bug.)

## The hand, task, crew

Task: VERBATIM W6b/W7 chamber task (12-line poem, six interlocking
constraints) and VERBATIM mechanical check(). No model ever sees the
checker. Scores 0–6.

Crew (identical invocation to W7):

- **kimi** (`kimi -p`, last-12-lines parse) — THE REVISER UNDER TEST.
  W7 fn.1 is this station's origin event: kimi holds seal+rhyme solo
  but broke a passing seal as a descending reviser.
- **claude** (`claude -p`) · **flash** (deepseek-chat via
  api.deepseek.com) — revisers.
- **wesley** (ollama granite3.1-dense:2b at 127.0.0.1:11434,
  num_ctx 4096, ollama NEVER restarted — W3b owns the GPU lane) —
  non-holder control.

**Holder status (pre-stated, W7's on-record measured solo hold-sets):**
claude {12L, c1, c3, c5} · kimi {12L, c3, c4, c5} · flash {12L, c5} ·
wesley {12L, c5}. These define the holder cells. The fresh seed-draw
solo pass (below) is committed alongside as a consistency check and
reported, but does NOT redefine cell membership — one fresh draw is
noise, W7's committed vector is the bank.

## Seed corpus (G0 guard)

Seed base **20260828**. Seeds are regenerated at fire time (W7's
results record per-hand checks, not per-hand drafts):

1. One solo pass per yard (4 draws: kimi, claude, flash, wesley), same
   TASK string and same per-model invocation/temperature as W7.
2. Keep the **two best drafts**; a draft is eligible only at score
   ≥ 3/6. If fewer than two drafts reach 3/6, redraw the failing
   yards — **two more draws per yard max** (total draw cap: 8).
3. **Seeds + their check() states COMMITTED before any regime arm
   runs.** The instrument's raw material goes on record before the
   experiment touches it.

## Protocol — the 4×3 regime cross

Crossed design: reviser {kimi, claude, flash, wesley} × regime {

- **(i) baseline** — W7's revision wording verbatim (per-model REVISE
  strings, identical characters);
- **(ii) minimal-edit** — same task + attempt frame, plus: "Change as
  few characters as possible. Touch ONLY lines that violate a
  constraint.";
- **(iii) verify-then-fix** — same task + attempt frame, plus: "First
  list each numbered constraint with PASS or FAIL for this attempt,
  then output the corrected 12 lines." (Parse last 12 lines — the
  kimi pattern — for every model in this arm.)

} — single pass per (reviser, regime, seed) cell, **no re-rolls**,
every output recorded verbatim. 4 revisers × 3 regimes × 2 seeds =
**24 revisions**.

### Measured quantities

For every revision: full check() state before/after, and **per-line
edit distance** (character-level Levenshtein, seed line i vs revision
line i; revision lines beyond the seed's 12 count as full-length
insertions). Each constraint's carrier lines (spec, pre-stated):
c3 seal → the seal line · c2 acrostic → all lines · c1 growth → all
lines · c5 unique-last → final line · c4 rhyme → line endings ·
c6 punctuation / 12_lines → whole text. Carrier distance for c4 is
computed on the line-ending tokens; for c6/12L on the whole text
normalized by length.

**Cells:**

- **Holder cells** — reviser holds c solo (W7 vector) AND c passes in
  the seed (the W7 kimi event) → destroyed?
- **Repair cells** — c broken in seed → held after revision?
- Non-holder cells ride along, recorded, and become W10's p_destroy
  data (spare/destroy rates by hand × constraint).

## PREDICTION (on record before any run)

- **P1 (the gap is real):** baseline holder-cell destruction rate
  **≥ 15%** per revision. kimi's W7 kill was not a one-off.
- **P2 (M1 is the mechanism):**
  - (a) per-line edit distance on carrier lines predicts destruction
    (logistic slope ≠ 0, p < 0.05, pooled cells);
  - AND (b) verify-then-fix cuts holder-cell destruction **≥ 50%
    relative** with Wilson CI separation, at **≤ 15 points absolute
    loss** in repair rate.

## Bars, kill gate, falsifiers (pre-scored, both branches)

- **Kill gate:** no seed draft ≥ 3/6 after the draw cap → STOP, file
  "nothing passing to destroy."
- **Falsifier of the phenomenon (negative result, filed honestly):**
  P1 fails — 0 holder-cell destructions across ≥ 24 baseline holder
  cells → the reviser-gap was a W7 one-off; the intersection law's
  clean form strengthens; the fleet stops paying for re-verification
  of held constraints. Consolidates W5, embarrasses no one.
- **Falsifier of the mechanism:** P1 holds but P2 fails → the gap is
  real and prompt-irreparable → **M2, a revision-mode wall**.
  Doctrine shifts to instruments: verification of passing constraints
  goes to the mechanical checker (fleet-side), never trusted to
  revising minds.

## Budget and guards

- **Hard cap ≤ 60 model calls:** ≤ 8 seed draws + 24 regime revisions
  = ≤ 32 experimental calls, recorded in a call ledger. Engineering
  passes (opencode writing checker/generators/analysis) are yard
  tools, logged separately and never touching experimental data
  generation.
- **kimi quota protocol:** `kimi -p` is the ONLY working form (no -y,
  no --auto). On 403 quota: back off, wait, retry. If exhausted:
  document, and fall back to `claude -p` for the *regime* calls while
  flagging that the n=1 origin finding was kimi-specific.
- Single pass, no re-rolls, results committed as measured.
- No model ever sees the checker.
- wesley: num_ctx 4096, ollama never restarted (W3b owns the GPU).

## Deliverables

Registration sealed first (this file) → seeds + check states committed
→ regime JSON ledgers → analysis (P1, P2a, P2b with Wilson CIs) →
VERDICT.md adjudicating M1 vs M2 → all committed and pushed to
origin master incrementally.

*Sealed 2026-08-27, before the first call. Undersold on purpose.*
