# W9 — THE NEVER-HELD KERNEL: verdict

*Station 2 of the W8-queue. Sealed in REGISTRATION.md (commit a6fa280)
before any model call; Amendment 1 sealed (c394386) before SH-4's first
call. Four shapes, five yards, 121 model attempts of the 200 cap
(1 engineering + 1 ping + 119 draws; zero kimi 403s, zero wesley
soft-stops, ollama never touched). Single pass, no re-rolls, results as
measured.*

## VERDICT: the kernel never existed

Both cells of the "never-held kernel" were **unsatisfiable by
construction in the W6b/W7 checker**. Not model-class walls. Instrument
bugs. The minds were acquitted by arithmetic, not by prompting:

1. **c2** — the task demands first letters spell `THEEILEENLAUN`
   (13 characters) across a 12-line poem. Twelve first letters can
   never equal a 13-character string. Found in the pre-run instrument
   audit (checker-reuse step), sealed into the registration; fair cell
   **c2'** (first 12 letters = THEEILEENLAU) pre-registered.
2. **c6** — the checker demands `sorted(punc) == ['.', ',']`, but ASCII
   makes `','` (0x2C) sort before `'.'` (0x2E): the sorted form of any
   {comma, period} poem is `[',', '.']`, never `['.', ',']`. **No poem
   could ever hold c6.** Found mid-run when SH-3's dedicated formatting
   passes executed c6 exactly (one comma, one period, line-initial
   caps only — codepoint-verified ASCII) and scored false; Amendment 1
   sealed the fair cell **c6'** before SH-4 fired.

Both bugs are one bug class: **equality against a hand-written literal
instead of a computed or witnessed target.**

## The wall-table (fair cells; see WALL-TABLE.md for full tables)

Mind-only hold rates, per shape × per mind:

| shape | yard | c2' | c6' |
|---|---|---|---|
| SH-1 ensemble (verbatim task, N=16) | claude | **14/16 (88%) MAJ** | **15/16 (94%) MAJ** |
| | kimi | 2/16 | 2/16 |
| | flash | 0/16 | 0/16 |
| | wesley | 0/16 | 0/16 |
| SH-2 scaffold (N=4) | claude | 4/4 (100%) | 4/4 (100%) |
| | opencode | 4/4 (100%) | 4/4 (100%) |
| | flash | 2/4 | 0/4 |
| | kimi | 0/4 | 0/4 |
| SH-3 attorney (finals, live) | opencode | 2/2 | 2/2 (P3: 2/2) |
| | claude | 1/1 live (c2 P3 yard-down) | 1/1 live |
| | flash | 1/2 | 0/2 |
| | kimi | 0/2 | 0/2 |
| SH-4 c6-fix (4/6 seed) | opencode | — | **4/4 fixed** (+c2' gained) |
| | flash | — | 1/4 fixed (that draw = full satisfiable board) |
| | kimi | — | 0/4 |
| | claude | — | yard-down (session limit) |

Pooled fair cells: **c2' 30/86 scoped attempts** (Wilson 95% CI
[25.7%, 45.4%]); **c6' 33/98** (CI [25.1%, 43.5%]). Verbatim c2/c6:
0/86 and 0/98 — as dictated by impossibility, carrying zero evidence
about the crew.

Fleet-selected (any-hold within a yard's N draws — instrument column,
W1 selector precedent): c2' ANY at SH-1: claude, kimi; c6' ANY: claude,
kimi; scaffold lifts flash's c2' to ANY. Mind-only remains the
headline; selection adds nothing the rates don't already show.

## The historical re-read (W6b/W7, mechanical replay)

- **c2' was TRUE in 4 recorded artifacts** scored "c2: false": W6b
  solo claude, W6b braid, W7 solo claude, W7 ASC braid.
- **c6' was TRUE in 2 recorded artifacts** scored "c6: false": W7 solo
  claude, W7 ASC braid.
- Therefore **W7's ascending braid — "5/6, the honest top" — held every
  satisfiable cell**: 12L, c1, c3, c4, c5 verbatim plus c2' and c6'.
  The theater's ceiling was never 5/6; it was the full satisfiable
  board, reached twice before W9 ever ran.
- W6b/W7's "no yard in any condition ever held c2/c6" was true of the
  score and false of the poems.

## Prediction scoring (honest)

- **Queue's original (undersold): "c6 falls, c2 stands 0/≥48."** Under
  the verbatim cells both halves are vacuous (impossibility). Under
  the fair cells: **both fell, hard** — c6' fell at every shape it
  touched (17/64 solo ensemble!), c2' fell at SH-1 with a majority
  hold. The prediction's spirit (formatting = workflow problem,
  promptable) is confirmed; its fear (acrostic = planning limit) is
  refuted for this crew: claude plans THEEILEENLAU at 88% solo on the
  verbatim task.
- **W9's sealed #2 (c6):** "falls ≥1/8 in some shape; SH-1 ≤2/64." —
  Falls: confirmed everywhere. The ≤2/64 clause: wrong even in spirit
  (17/64) — claude was holding formatting all along, invisibly.
- **W9's sealed #3 (c2'):** "SH-1 ≤1/64" — FALSIFIED (16/64, claude
  14). "SH-2 ≤1/16" — FALSIFIED (10/16). "SH-3 ≥1 chain" — CONFIRMED
  (4/6 live finals). "total ≤3 holds" — FALSIFIED (30). The
  underselling was wrong in the direction it feared least.
- **Amendment 1's SH-4 pred:** pooled c6' fix ≥1/8 — confirmed (5/12
  live); opencode ≥2/4 — confirmed (4/4); claude ≥2/4 — unmeasured
  (yard-down, session limit; not counted as failure); kimi ≤1/4 —
  confirmed (0/4).

## What the fleet learns

1. **There are no model-class walls at this task in this crew.** There
   are kernel-strong minds (claude 88%/94% solo on the verbatim task;
   opencode 100%/100% on scaffold and 4/4 on the isolated fix), a
   presentation-rescued mind (flash: c2' 0/16 → 2/4 under scaffold),
   and kernel-weak minds (kimi: c2' ~5%, c6' ~8% pooled; wesley 0).
   Mind-dependence is real; walls were not. Doctrine: **assign kernel
   cells to kernel-strong hands or instruments; rescue flash-class
   hands with scaffolds; never spend kimi-class hands on them.**
2. **The G0 guard extends to checkers.** "Held by nobody in any
   condition across two stations" was a property OF THE INSTRUMENT.
   New statute candidate: **no "wall" claim is bankable without a
   satisfiability witness for the cell** (a constructive pass or an
   exhaustive argument). The wheel nearly wrote a wall table out of a
   sort order.
3. **W10 (law as helm) inherits a wider design space than designed
   for**, exactly as the spec's c2-falls branch anticipated: engineered
   chains can target c2' (last-holder arithmetic with claude/opencode
   closers), and W10's phase-0 solo vectors MUST be re-measured under
   c2'/c6' — W6b/W7's recorded hold-sets understate every strong hand
   (W7 solo claude was 6-of-7-satisfiable, recorded 4/6).
4. **W11 (fused catch)** — its pre-noted risk ("if c2 truly never-held,
   P1 rides on c1 alone") dissolves: fusion can vote on c2' lines
   (claude/opencode/flash-scaffold lines carry correct letters);
   c6' has line-global structure (whole-text counts) and stays a
   single-mind or post-processor cell, consistent with locality.
5. **Crew notes.** opencode (new yard, GLM-5.3-labeled) debuted as the
   strongest scaffold hand (mean 4.50) and the only 4/4 fixer; its
   "fix-only" pass over-fixed productively (gained c2', +1 score).
   kimi ran clean via `kimi -p` all session — zero 403s, zero backoffs.
   wesley: 16 sequential num_ctx-4096 calls sharing the GPU with the
   W3b bench, zero incidents, ollama never restarted. claude's evening
   ended at its session limit — 5 cells yard-down, recorded as such,
   not scored.

## Disposition

Filed: W9 complete. The never-held kernel is DISSOLVED — both cells
instrument artifacts, both fair cells held at majority rates by the
strong hands, the historical ceiling re-read as a perfect satisfiable
board. Negatives-as-results cut both ways: the station's most
interesting finding embarrassed the instrument, which is the method
working. Checker satisfiability witness becomes a standing guard
recommendation for SYNTHESIS. No re-rolls taken; every number above is
a single-pass draw from the committed ledgers.
