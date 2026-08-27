# W10 — LAW AS HELM (L4 last-holder-spare): registration

*Pre-registered BEFORE any W10 model call. Committed before execution.
This file is the contract. Grows from W5's L1 consolidation (12/13 =
92%), W7's 3-cell violation (L1 predicted 2/6 on ASC, observed 5/6;
DESC reproduced the intersection floor exactly), and W8's measured
non-holder destruction table. Spec: W8-queue/DESIGN.md Station W10.*

## The statute under test — L4, LAST-HOLDER-SPARE (from DESIGN.md, verbatim intent)

> A braid holds c ⟺ some hand in the chain holds c solo AND every
> hand AFTER the last holder spares c (each non-holder destroys w.p.
> p_destroy(h,c), measured not assumed).

**Deterministic sealed forward-simulation (the prediction algorithm,
frozen here):** a chain runs h1 → h2 → h3 → h4; h1 composes solo,
hi (i>1) revises the draft (W7 revision wording, verbatim per yard).
Predicted state of constraint c after each hand:

- after h1: held(c) = h1 holds c solo.
- after hi (i>1): held(c) = TRUE if hi holds c solo (holder re-holds
  while revising — the W7 kimi hand-3 recovery precedent, statute as
  written); else held(c) = previous state AND hi spares c.

**Spare point-estimate rule (frozen):** if hi holds c solo → p_spare
= 1. Else if (hi,c) is in W8's measured non-holder table → p_spare =
1 − measured p_destroy; predict spare iff p_spare ≥ 0.5. Else → the
W5 flat prior (destruction high but imperfect: one survival in 13
non-holder exposures, p_spare = 1/13) → predict DESTROY.

W8's measured table on record (w8-analysis.json nonholder_table):
claude|c4 0.17 (spare) · flash|c3 0.67 (destroy) · flash|c4 0.33
(destroy) · wesley|c3 1.00 (destroy) · wesley|c4 0.50 (destroy,
tie broken to destroy by the ≥0.5 rule being spare-inclusive at
exactly 0.5? NO — rule reads spare iff p_spare ≥ 0.5, so 0.50
SPARES; stated explicitly to remove ambiguity).

**L1's prediction (frozen):** the intersection of ALL four hands'
solo hold-sets, per chain, all-touch relevance. L1 cannot exceed 2
realistic cells on any draw; CH-A and CH-B are built to make the
laws disagree; CH-C is the reproduction control.

## Which c2 the checker scores (SEALED)

**The primary instrument is the VERBATIM W7 check() — byte-identical,
replay-verified against W7 artifacts before fire.** c2_acrostic as
written is unsatisfiable (13 letters, 12 lines — W9's audit), so
under the verbatim instrument c2 is held by NO yard in ANY condition:
every hold-set carries c2=false, both L1 and L4 always predict c2
not-held, and the cell can never discriminate the laws. It stays in
the pooled bar for comparability with W5/W7/W8 cells (both laws get
it right by construction; 18 pooled cells, 3 always-free).

**Why not W9's c2':** every input to tonight's arithmetic — W5's
consolidation, W7's hold-sets and trace, W8's p_destroy table — was
measured under the verbatim instrument. Swapping the instrument
mid-law would break cell comparability. c2' (first 12 letters ==
'THEEILEENLAU') is computed and recorded for every phase-0 solo and
every final chain output as OBSERVATIONAL data only, flagged
fleet-side, excluded from the bar. If c2' turns up held somewhere,
that is a note for the fleet, not a point for either law.

## Protocol

- **Phase 0 (seed base 20260830):** fresh solo draw, all four yards
  (4 calls, temperature per W7 callers, single pass, no re-rolls).
  Hold-sets committed as measured BEFORE any chain fires (G0 guard).
- **Kill gate:** phase 0 must yield ≥ 3 distinct hold-sets AND ≥ 1
  split-ownership constraint (held by some yards, not others). ONE
  redraw allowed (seed 20260830+1000, pre-stated), then STOP, filed
  underpowered.
- **Phase 1 (sealed before any chain runs):** from the MEASURED
  hold-sets, commit SEALED-PREDICTIONS.md with concrete per-cell
  predictions for both laws on all three chains, THEN fire. Selection
  rules, frozen now:
  - **CH-A repair-max:** ascending by measured phase-0 solo score;
    ties broken by W6b rank (wesley < flash < kimi < claude).
  - **CH-B spare-test:** among split-ownership constraints, pick the
    one whose STRONGEST non-holder (highest phase-0 solo score among
    yards not holding it) is strongest; that non-holder goes LAST;
    the other three yards precede in ascending solo-score order
    (same tiebreak). Target cell: that (non-holder, constraint) pair.
    L1 says the cell dies; L4 says it survives iff p_spare ≥ 0.5
    (measured) — with claude|c4 = 0.83 spare, a claude-last chain
    over a kimi-held c4 is the expected shape.
  - **CH-C deterministic descent:** descending by measured solo score
    (weak hands last). BOTH laws predict the exact intersection
    floor. Reproduction control: a CH-C miss indicts the instrument,
    not the laws.
- **Scoring:** pooled constraint-cell accuracy across the 3 chains ×
  6 cells = 18 cells, L1 vs L4, using the verbatim check on final
  outputs. Chain intermediates also checked per hand (trace), single
  pass, no re-rolls, results committed as measured.
- **Bar:** **L4 ≥ 80% pooled cell accuracy (W5's own bar) AND CH-C
  exact.** Falsifier: L4 < 80% or CH-C misses the floor → the
  arithmetic-crew-design program STOPS; doctrine downgrades to
  "measure the chain, don't predict it."

## Honest asymmetry (pre-stated)

A CH-B survival could be luck (one cell, one pass). It is scored as a
cell, not a law; only the pooled bar carries a verdict. If L1 wins
the arbitration cells or both laws miss the bar, the honest
downgrade is filed as the result. Negatives are results.

## Crew & guards

claude (`claude -p`), kimi (`kimi -p`; 403 → sleep 60 backoff, max 3
attempts, documented — W8's pattern), flash (deepseek-chat,
api.deepseek.com, env key from ~/.bashrc), wesley (ollama
granite3.1-dense:2b, 127.0.0.1:11434, num_ctx 4096, keep_alive 30m;
NEVER restart ollama — bench W3b shares the GPU; slowness tolerated).
No model ever sees the checker. Engineering (checker port, chain
runner, scorer) by opencode; checker replay-verified against W7
artifacts (0 mismatches required) before any call. Budget cap
**≤ 30 calls**: 4 phase-0 + 12 chain hands + ≤4 redraw + slack.

*Sealed 2026-08-27, before any W10 model call.*
