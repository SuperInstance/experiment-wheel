# W9 — THE NEVER-HELD KERNEL: registration

*Pre-registered BEFORE any W9 model call. Committed before execution.
This file is the contract. Grows from W7 footnote 2 (c2_acrostic and
c6_punctuation held by NO yard in ANY condition across W6b + W7) and
the W8-queue DESIGN.md Station W9 spec (commit f6df86c).*

## PRE-RUN INSTRUMENT AUDIT — c2 IS UNSATISFIABLE (found before any call)

Preparing the mandated verbatim checker reuse (W6b/W7 `check()` byte-
identical, so scores stay comparable), the audit found:

> `'THEEILEENLAUN'` is **13 characters**. A 12-line poem yields exactly
> 12 first letters. `c2_acrostic` requires
> `''.join(first letters).upper() == 'THEEILEENLAUN'` — a 12-character
> string can never equal a 13-character string. When `12_lines` is
> false, c2 is set false explicitly. **No output can ever hold c2.**

Consequences, pre-stated here rather than discovered post-hoc:

1. **The verbatim c2 cell stays in every ledger** (comparability with
   W6b/W7), but it measures impossibility, not model class. Expected
   result: 0/N everywhere, trivially.
2. The queue's original prediction clause "c2 stands 0/≥48, CI upper
   ≈ 6.1%" is **void as evidence** — 0/N from an impossible event
   carries no information about the crew. The c2 half of the
   never-held kernel DISSOLVES as an instrument artifact.
3. **Amended cell c2' (pre-registered, fleet-side scoring only, no
   model ever sees any checker):** `first-letters joined, uppercased,
   first 12 chars == 'THEEILEENLAU'` — the only 12-line reading of
   the task's own string (drop the trailing N). c2' is scored on
   every draw of every shape, SH-1 included. The substantive question
   — can ANY shape of this crew execute the acrostic×growth
   interlock? — now has a fair instrument.

The task text handed to models stays VERBATIM (W6b string, including
the 13-letter word) in every shape except where the shape's own
protocol presents the worksheet rows (SH-2, SH-3 pass 2), which list
12 rows T,H,E,E,I,L,E,E,N,L,A,U — the satisfiable reading of an
impossible instruction, mapping pre-stated here.

## The question (one, amended by the audit)

Original: are c2 and c6 model-class walls or artifacts of one prompt
shape? Amended: **c6 — wall or workflow?** (untouched by the audit).
**c2' — can any shape execute the 12-letter acrostic under the growth
constraint, now that the instrument is fair?** The never-held kernel's
c2 half is already reclassified (instrument artifact) by arithmetic;
this run measures what the crew can actually do.

## Shapes (pre-stated; spec-verbatim except where noted)

- **SH-1 — ensemble at N=16:** 16 independent draws per yard on the
  VERBATIM W6b task string, temperature as W6b (flash 0.75, wesley
  0.7, CLI yards as-run). Crew: claude, kimi, flash, wesley (all four,
  spec-verbatim). Seeds tagged 20260829+k per draw (ledger tags;
  sampling randomness as-run — CLI yards expose no seed parameter).
- **SH-2 — scaffold (worksheet):** identical constraint information,
  worksheet presentation — 12 explicit rows ("line 1: one word, begins
  with T; … line 12: twelve words, begins with U") plus c3/c4/c5/c6
  rules verbatim. Crew: claude, kimi, flash, opencode × 4 draws each.
- **SH-3 — attorney decomposition:** three specialized hands in
  sequence, each seeing a REDUCED task: (P1) free 12-line poem (no
  constraints listed); (P2) letter-and-count pass ("rewrite each line
  to begin with the required letter and contain the required word
  count; change nothing else" — 12 rows given); (P3) formatting pass
  (c6 only: "exactly one comma, one period, no other punctuation,
  capitals only line-initial; change nothing else"). Crew: claude,
  kimi, flash, opencode × 2 chains × 3 passes. Composite checked at
  every pass boundary; the final composite is the chain's cell. This
  is the intersection law's boundary test (does a hold-set GROW when
  the task shrinks?). Note: the reduced chain never carries c3/c4/c5
  information — those cells ride along as measured, expected low.
- **SH-4 — c6 minimal-fix:** take one otherwise ≥3/6 seed draft from
  SH-1's committed ledger (best score, tiebreak fewest prior fixes);
  pre-stated fallback: W7 ASC final draft (5/6, on record in
  w7-results.json). The hand fixes ONLY punctuation/caps ("change
  NOTHING else"). Crew: claude, kimi, flash, opencode × 4 draws each.
  Scored: c6 before/after + full collateral vector.

## Crew (yards, all one-shot, single pass)

- **claude** — `claude -p` (W6b/W7 adapter verbatim).
- **kimi** — `kimi -p` ONLY (the one form; W6b/W7 adapter verbatim,
  last-12-lines parse). 403/rate-limit → backoff 60/120/240s, max 3
  retries per draw; a draw that still fails is recorded `failed`
  (failed ≠ draw; attempts counted against cap).
- **flash** — deepseek-chat via api.deepseek.com, t=0.75 (W6b
  adapter verbatim; key from ~/.bashrc export).
- **wesley** — ollama granite3.1-dense:2b, 127.0.0.1:11434 (W6b
  adapter + explicit num_ctx 4096). GPU GUARD: W3b bench (deepseek-
  r1:8b) shares the GPU — wesley runs strictly sequential, capped at
  SH-1's 16 draws, soft-stop rule: any wesley call > 180s or ollama
  error → wesley's ensemble stops at the last completed draw, N
  recorded. **Never restart ollama.** wesley sits out SH-2/3/4 (spec:
  2-point ceiling adds little).
- **opencode** — NEW yard this station (label 'opencode' in every
  ledger), `opencode run` one-shot (GLM-5.3 via OpenCode — a
  different lane than the Z.ai chat lane, honestly labeled). One
  availability ping before first use (counted). Output capture: final
  message text; same fence/`#` stripping as the checker. Used for
  SH-2/SH-3/SH-4 generation cells AND (before any generation call)
  the checker write/verify task — never as a judge of its own or
  others' outputs.

## Budget (hard cap 200 total model attempts)

Planned draws: SH-1 64 (16×4) + SH-2 16 (4×4) + SH-3 24 (4×2×3) +
SH-4 16 (4×4) + opencode ping 1 = **121**. Headroom 79 for kimi 403
retries and yard errors. Every API/CLI/ollama invocation toward a
model counts as an attempt (draws ⊆ attempts). Checker work,
scaffold building, scoring, fusion arithmetic: zero model calls
(opencode's checker task is its one non-generation call, counted).

## Scoring

- Primary instrument: W6b/W7 `check()` **byte-identical** (verified
  before any run by replaying every poem recorded in W6b/W7 results
  JSONs — scores must match exactly; syntax-checked first).
- Cells reported: c2 (verbatim), c2' (amended), c6 (verbatim), plus
  the full vector for context.
- **Mind-only rate:** holds/draws per shape × per mind. The headline
  number.
- **Fleet-selected rate:** any-hold within a shape×mind's N draws
  (checker picks the passing draft — W1 selector precedent).
  Legitimate fleet-side instrument, a DIFFERENT claim, reported as a
  separate column, flagged.
- SH-1 also reports per-yard majority (≥8/16) per constraint.
- Wilson 95% CIs on all pooled rates.

## Bars (pre-stated)

- **c6 falls** (promptable) if ANY shape holds it ≥ 1/8 within that
  shape (pooled across that shape's attempts) → formatting discipline
  is a workflow problem. Else c6 = wall; post-processor owns it.
- **c2 verbatim:** expected 0 everywhere — impossibility, recorded as
  the instrument finding. Not scored as a wall.
- **c2' falls** if ANY shape holds it ≥ 1/8 within that shape → the
  kernel's substantive half falls; the crew CAN do the acrostic at
  some shape.
- **c2' stands (wall)** if 0 holds across all c2'-scoped attempts
  (SH-1 64 + SH-2 16 + SH-3 8 chains = 88 planned) → acrostic×growth
  interlock is a genuine planning wall at this crew, now fairly
  measured (0/88 → CI upper ≈ 3.4%, rule of three).
- If SH-1's 64-draw baseline alone holds c6 or c2', later shapes
  still run (rate estimation — spec-verbatim).

## PREDICTION (on record, sealed with this file)

1. **Queue's original (undersold):** c6 falls; c2 stands 0/≥48. The
   c2 clause is now known-trivial (audit above); it stands or falls
   as written but MEANS "impossible", not "wall".
2. **c6:** falls — ≥1/8 in at least one shape; best odds SH-3's
   formatting pass (P3) and SH-4's isolated fix; SH-1 solo ensemble
   stays low (≤2/64).
3. **c2':** SH-1 solo ensemble ≤ 1/64; SH-2 scaffold ≤ 1/16; **SH-3
   attorney decomposition holds c2' in ≥1 of 8 chains** (the letter
   pass isolates exactly the mechanics; coding-strong yards should
   execute a 12-row mechanical rewrite). Point prediction: c2' total
   holds across all shapes ≤ 3. If c2' = 0 everywhere → the
   substantive wall is real and now honestly measured.
4. SH-4 collateral: median fixed draft retains ≥ seed score − 1.

## Kill gates / guards

- Yard down (draw-1-as-ping fails through backoff): yard drops out,
  recorded as such; SH-1 needs ≥2 live API yards else STOP, file.
- SH-4 needs a ≥3/6 seed (SH-1 ledger; fallback W7 ASC draft on
  record — effectively guaranteed).
- Single pass, no re-rolls of completed draws, ever. Results as
  measured. No model sees the checker. Ledgers JSON on disk,
  committed per shape BEFORE that shape's analysis. Registration
  committed and pushed BEFORE any model call (sealed-before-run).
  Incremental push: registration → checker verification → per shape
  → verdict.
- GPU shared with W3b bench: no ollama-heavy work; wesley capped as
  above; ollama never restarted.

## Deliverables

`w9_check.py` + `w9_audit.py` + audit report (checker write/verify by
opencode, replayed against W6b/W7 records) · `w9_runner.py` ·
`ledgers/sh1-ensemble.json`, `sh2-scaffold.json`, `sh3-attorney.json`,
`sh4-c6fix.json` (attempt-level, poems included) · `WALL-TABLE.md`
(per shape × per mind × c2/c2'/c6 mind-only + fleet-selected rates) ·
`VERDICT-w9.md` vs the sealed predictions.

*Sealed at W9-never-held-kernel/REGISTRATION.md, 2026-08-27, before
the first model call. Undersold on purpose; the audit found first.*
