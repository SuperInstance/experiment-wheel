# W10 — LAW AS HELM: VERDICT

*16/30 calls (4 phase-0 + 12 chain hands), single pass, no re-rolls,
kimi never 403'd (no backoff spent). Everything committed as measured.
Sealed contract: REGISTRATION.md (aafb0d5) + SEALED-PREDICTIONS.md,
both pushed before any chain call.*

## The sealed bar, and what happened

**Bar (verbatim from REGISTRATION): L4 ≥ 80% pooled cell accuracy AND
CH-C exact.**

| chain | order | observed | L1 pred | L4 pred | L1 | L4 |
|---|---|---|---|---|---|---|
| CH-A repair-max | wesley→claude→flash→kimi | {12L,c3,c4,c5} | ∅ | {12L,c3,c4,c5} | 3/7 | **7/7** |
| CH-B spare-test | wesley→claude→kimi→flash | {12L,c5} | ∅ | {12L,c4,c5} | 5/7 | 6/7 |
| CH-C descent | kimi→flash→claude→wesley | {12L} | ∅ | {c4} | 6/7 | 5/7 |
| **pooled** | | | | | **14/21 = 66.7%** | **18/21 = 85.7%** |

- **L4 ≥ 80% pooled: PASSED** (85.7%, W5's own bar).
- **CH-C exact: FAILED.** Observed {12L}; L1 predicted ∅, L4 predicted
  {c4}. Neither law reproduced its set. The miss is ABOVE the floor
  (wesley — empty solo hold-set — HELD 12L as final reviser), the same
  direction as W7-ASC's violation, not instrument error (checker
  replay-verified 0 mismatches before fire).

**VERDICT: the conjunctive sealed bar FAILS. Per the sealed
falsifier, the arithmetic-crew-design program STOPS as a doctrine;
the honest downgrade is filed: the braid outcome on this crew is
cheaper to MEASURE than to PREDICT.** That sentence is now proven
twice over, in both directions: L1 cannot see repair (W7-ASC, 5/6 vs
2/6); L4's deterministic point-sim cannot see the noise floor under
spare/repair rates measured at n=3–6.

## What the run actually showed (the honest full picture)

1. **L4 beat L1 head-to-head and it wasn't close on the engineered
   cells.** 8 sealed arbitration cells (L1=F, L4=T): L4 took 6/8
   (CH-A 4/4, CH-B 2/3, CH-C 0/1). CH-A — pure engineering, weakest
   first, best last — landed **7/7 exact**, L4's single best result
   in theater history. When the last hand is the strongest holder,
   the arithmetic IS the outcome.
2. **The two misses are both the same miss: revision noise under
   small-n point estimates.** (a) CH-B: flash (measured p_spare(c4) =
   0.67) destroyed kimi's c4 — the 0.67 didn't realize; worse, kimi
   at hand-3 DROPPED c4 it holds solo (holder-does-not-always-re-hold
   — the W8 M2 wall showing up inside L4's own statute). (b) CH-C:
   wesley destroyed c4 (0.50 coin, lost) and simultaneously held 12L
   from a hold-set of ∅. W8's table has 3–6 exposures per cell; one
   evening's rates do not transfer as point estimates.
3. **L1's home turf cracked.** W7-DESC reproduced the floor to the
   cell; tonight's descent EXCEEDED it. The intersection floor is a
   strong prior, not a guarantee — "backward-chain law" is itself now
   12/15 cells rather than law.
4. **c2' observational (W9's fair acrostic): 0/7 tonight** (4 solos +
   3 finals). No new information beyond W9's own ledger; recorded,
   excluded from the bar as sealed.

## Doctrine outcome (filed, not argued)

- **L4 does NOT graduate to helm.** Crew design does not become
  arithmetic tonight. The falsifier fires as written.
- What survives as heuristics, on record: **strongest-holder-last
  (CH-A shape) is 7/7 once and cheap to compute** — W7's "ascending
  order" heuristic is now 2-for-2 on its home shape; and **spare
  rates are real but wide** — report them as intervals (W8's Wilson
  CIs), never as points.
- For the fleet: chain outcomes on this crew remain cheaper to
  measure (4 calls) than to predict (16 calls bought a 6/21-edge over
  L1 and still missed the control). **Measure, don't predict.**

*Committed 2026-08-27. Raw material: w10-phase0.json, w10-chains.json,
w10-calls.jsonl, w10-predictions.json, w10-verdict-data.json — all on
record before this file was written.*
