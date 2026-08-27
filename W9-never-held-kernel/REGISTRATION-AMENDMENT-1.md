# W9 — REGISTRATION AMENDMENT 1: the second unsatisfiable cell (c6)

*Sealed and committed BEFORE SH-4's first model call. Mid-run discovery
at SH-3, handled under the queue's own statute: "no exceptions without
a new sealed amendment on record."*

## What happened

SH-3's dedicated formatting passes (P3) produced outputs from claude
(chain 1) and opencode (chains 1, 2) that contain exactly one comma and
one period (ASCII 0x2C/0x2E, codepoint-verified), no other punctuation,
and capitals only line-initial — i.e. c6 executed as instructed — yet
the verbatim checker scored `c6_punctuation: false`.

## Root cause (arithmetic)

The W6b/W7 checker tests `sorted(punc) == ['.', ',']`. In ASCII,
`','` (0x2C) < `'.'` (0x2E): **the sorted form of any {comma, period}
set is `[',', '.']` — dot-first can never occur.** c6 was unsatisfiable
by construction from birth, exactly like c2 (13-letter acrostic asked
of 12 lines). The never-held kernel's BOTH cells are instrument
artifacts. No model-class wall was ever measured by them.

## c6' (amended cell, fleet-side, no model ever sees it)

`c6'` = 12 lines AND `sorted(punc) == [',', '.']` (exactly one comma
and one period, nothing else) AND capitals only line-initial
(len(caps) == len(uppercase-initial lines)). Added to w9_check.py as
`c6_amended()`; verbatim `check()` untouched, still primary for
comparability; every table reports verbatim c2/c6 as impossibility
columns alongside c2'/c6' as fair cells.

## Mechanical recomputation over committed records (no re-rolls, outputs untouched)

- **Historical (context):** c6' TRUE in 2 recorded W6b/W7 artifacts —
  W7 solo claude and the W7 ASC braid final — both scored "c6: false"
  at the time. Combined with the c2' replay (4 artifacts), the W7 ASC
  "5/6" was a PERFECT satisfiable board (all six satisfiable cells).
- **SH-1 (64 draws):** c6' 17/64 — claude 15/16 (94% solo, verbatim
  task), kimi 2/16, flash 0/16, wesley 0/16.
- **SH-2 (16 draws):** c6' 8/16 — claude 4/4, opencode 4/4, flash 0/4,
  kimi 0/4.
- **SH-3 (7 executed P3 passes):** c6' 3/7 — opencode 2/2, claude 1/2,
  flash 0/1, kimi 0/2.

**c6' has therefore already fallen at every shape it touched**, with
majority rates for the strong hands. The registration's "c6 falls"
bar transfers to c6' (met); verbatim c6 stays as the impossibility
column.

## SH-4 seed rule (amended before SH-4 fires)

SH-4 fixes ONLY punctuation/caps; a seed that already holds c6' makes
the cell meaningless. Amended seed rule: **best-scoring SH-1 draw that
FAILS c6'** (fallback: best ≥3/6 regardless of c6', then W7 ASC draft).
Seed and its full check state committed before SH-4 draws run.

## Prediction added on record (sealed here)

- SH-4 c6' hold rate ≥ 1/8 pooled, with claude/opencode ≥ 2/4 each and
  kimi ≤ 1/4 (mind-dependence without a wall).
- SH-4 collateral: c2' of the seed is NOT destroyed by the formatting
  pass in ≥ 6/8 yard-draws (formatting is line-local; the letters
  should ride through).

## Standing guards unchanged

Verbatim checker primary; single pass; no re-rolls; results as
measured; ledgers committed before analysis; cap 200 attempts (105
used at seal time); wesley/GPU guards moot from here (SH-4 uses no
ollama); mind-only vs fleet-separated reporting extended to c2'/c6'.
