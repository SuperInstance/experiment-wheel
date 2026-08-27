# W8 — THE REVISER'S BLIND SIDE: verdict

*Registration sealed at commit 1ced4d2 BEFORE any call. Seeds sealed at
c69abd6 (G0 guard). 28 experimental calls of a 60 cap (4 seed draws +
24 revisions, single pass, no re-rolls, kimi never 403'd — no fallback
needed; the origin event's model ran the full cross). Checker ported
verbatim from W7 and replay-verified against W7's stored poems (0
mismatches). Engineering via opencode logged separately as yard tools.*

## The corpus (as drawn, no redraws needed)

| seed | draw | score | passes |
|---|---|---|---|
| S1 | 20260828-claude-d1 | 4/6 | 12L, c3, c4, c5 |
| S2 | 20260828-flash-d1 | 3/6 | 12L, c4, c5 |

(kimi drew 2/6, wesley 0/6 — recorded in w8-seeds.json.) Baseline
holder cells: **20** (kimi 7, claude 5, flash 4, wesley 4) — the seeds'
pass-states cap this below the falsifier's "≥24" phrasing; noted, not
redrawn.

## P1 — the gap is real: HOLDS, exactly at the bar

**Baseline holder-cell destruction: 3/20 = 15.0%, Wilson 95% CI
[5.2%, 36.0%].** The pre-stated bar was ≥15%. Met to the decimal point.

The three baseline kills:

| cell | constraint | carrier dist | note |
|---|---|---|---|
| S1 wesley | 12_lines | 0.41 | 11-line output |
| S1 wesley | c5_unique_last | 81.0 | full rewrite of final line |
| **S2 kimi** | **c4_no_rhyme** | **6.17** | **the replicated holder-kill** |

**The kimi event replicated, on a different constraint.** kimi holds
c4 solo (W7 vector, on record), the seed passed c4, and kimi's
baseline revision made two line-endings collide ("…same"/"…came" —
cluster 'me' twice). W7 fn.1 killed the seal; W8 kills the rhyme.
Same event class, fresh draw, sealed prediction. And it is
**regime-invariant**: kimi destroyed c4 in ALL THREE arms — baseline
(dist 6.2), minimal-edit (dist 3.9 — a near-touch rewrite), and
verify-then-fix (dist 6.7). The holder-kill survives even when kimi
barely rewrites.

Honest heterogeneity: claude's baseline holder cells were spotless
(0/5), flash 0/4. The baseline gap is carried by wesley (2/4, the
weakest hand) plus the kimi c4 event. "Every reviser has a blind
side" is NOT what the data says; "a holder can destroy a passing
constraint while revising, and one of them did it three ways" is.

## P2 — the mechanism: FAILS both prongs (pre-scored M2 branch)

- **P2a (logistic, pooled 60 holder cells, sealed parse):** slope
  +0.0232, Wald z = 1.92, **p = 0.0550** — positive direction, misses
  the pre-stated p < 0.05. Under the charitable VTF parse (below):
  p = 0.267. No post-hoc relaxation; the bar was sealed.
- **P2b (verify-then-fix halves destruction):** **FAILED — the
  prompt made it WORSE.** Sealed: VTF 7/20 = 35% vs baseline 15%
  (relative "reduction" −133%, no CI separation). Repair-rate loss
  7.1pt (the only sub-clause inside its ≤15pt allowance).

**Format contamination (flagged, both parses reported):** the VTF
listing instruction made claude and flash emit NUMBERED poem lines
("1. Trembling …"), which the pre-stated last-12 parse drops → sealed
degenerate parses. Charitable re-parse (strip "N." prefixes, re-check,
sealed numbers unchanged): flash S1 0/6→3/6 (12L+c5 actually held),
claude S2 1/6→3/6 (12L+c5 actually held). Under the charitable parse
VTF holder destruction = 3/20 = 15% — equal to baseline, still not
halved. **The verdict is robust to the parse question.**

## Mechanistic observations (post-hoc, labeled as such)

- Destruction co-moves with carrier edit distance ACROSS regimes:
  mean carrier distance 7.6 (minimal) / 13.4 (baseline) / 19.2 (VTF)
  vs destruction 3/20 / 3/20 / 7/20 sealed. Directionally M1.
- But the prompt that halved rewriting (minimal-edit: 13.4→7.6) did
  NOT cut destruction (3/20 → 3/20) — and kimi's c4 kill survived a
  3.9-distance minimal rewrite. Shrinkable-by-prompt, M1's actual
  signature, never appeared. VTF's listing LICENSED rewriting
  (distance 19.2, destruction more than doubled at sealed parse).
- claude's non-holder spare-rate on c4: p_destroy 0.17 (spared 5/6) —
  W7's "claude spared kimi's c4" replicates as a RATE. flash|c3
  0.67, wesley|c3 1.00, wesley|c4 0.50 — the W10 p_destroy table is
  in w8-analysis.json.

## VERDICT: M2 — REVISION-MODE WALL (pre-scored branch)

**P1 holds, P2 fails → the gap is real and prompt-irreparable at this
crew and these prompt shapes → M2.** As pre-registered: hold-sets are
solo-mode objects; in revision mode the effective hold-set shrinks
for at least some hands regardless of how little they rewrite.

Fleet doctrine, as the registration pre-scored it:

1. **Verification of passing constraints goes to the mechanical
   checker (fleet-side), never trusted to revising minds.** The
   reviser's own "check every constraint cold" is not an instrument.
2. **Verify-then-fix prompt shape is actively harmful** — it grew
   rewriting, doubled destruction at sealed parse, and contaminates
   output format. Struck from the Waters prompt book.
3. **Minimal-edit is free hygiene** (halves carrier rewriting at no
   repair cost: 4/28 vs 3/28 repairs) but buys no safety for held
   constraints.
4. **For W10:** per-hand p_destroy/spare table delivered
   (w8-analysis.json). Order chains so held constraints are never
   re-exposed to high-p_destroy hands; claude-class strong sparers
   make safe LAST hands for split-ownership constraints they don't
   hold (0.17 p_destroy on c4).

Negative-result ledger, filed per statute 6: the interesting
sub-claim that DIED is M1's prompt-shrinkability — minimal-edit
halved the rewriting and destroyed nothing less. The near-miss
(p = 0.055 sealed) is on record for any future station that wants a
higher-powered re-test (this one was honestly powered at n=60 holder
cells and did not meet its own bar).

*Runs can embarrass us; this one did exactly what it was sealed to
do: it made the fleet's cheapest hoped-for fix (two sentences of
prompt) die honestly, and handed W10 its arithmetic. — W8, fired
2026-08-27, 28/60 calls.*
