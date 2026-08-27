# W5 — CASE-LAW MATH: verdict

*Sealed amendment (commit 1d51ed5) fixed the laws, scoring, and verdict
rules BEFORE any arithmetic. Lane sealed to W6a+W6b; W7 untouched. Zero
fitting parameters. Run: `python3 W5-case-law-math/w5_caselaw.py`.*

## The formalized laws (from solo hold-sets alone)

- **L1 — INTERSECTION-OF-ALL:** braid holds c ⟺ every hand in the chain
  holds c solo. (All-touch weak-link ceiling: relevance = rewrites the
  draft, which at 85–94% novelty is every hand.)
- **L2 — LAST-HAND LAW:** braid holds c ⟺ the final hand holds c solo.
  (The literal W6b verdict phrasing.)
- **L3 — INTERSECTION-OF-LAST-TWO.**

## Prediction vs observed

**W6a** (kimi→claude→flash→wesley; solo 5,5,5,4; braid 4/6):

| constraint | observed | L1 | L2 | L3 |
|---|---|---|---|---|
| lines_13 | lost | lost ✓ | lost ✓ | lost ✓ |
| order_ok | lost | lost ✓ | lost ✓ | lost ✓ |
| seal | HELD | HELD ✓ | HELD ✓ | HELD ✓ |
| ends_keel | HELD | HELD ✓ | HELD ✓ | HELD ✓ |
| no_rhyme | HELD | HELD ✓ | HELD ✓ | HELD ✓ |
| short_lines | HELD | HELD ✓ | HELD ✓ | HELD ✓ |

All laws 6/6. (Uninformative between laws: wesley is both weakest AND last.)

**W6b** (kimi→claude→flash→wesley→flash; solo 4,4,2,2; braid 2/6):

| constraint | observed | L1 | L2 | L3 |
|---|---|---|---|---|
| 12_lines | HELD | HELD ✓ | HELD ✓ | HELD ✓ |
| c1_growth | lost | lost ✓ | lost ✓ | lost ✓ |
| c2_acrostic | lost | lost ✓ | lost ✓ | lost ✓ |
| c3_seal | **lost** | lost ✓ | **HELD ✗** | lost ✓ |
| c4_no_rhyme | lost | lost ✓ | lost ✓ | lost ✓ |
| c5_unique | **HELD** | lost ✗ | lost ✗ | lost ✗ |
| c6_punct | lost | lost ✓ | lost ✓ | lost ✓ |

## Pooled verdict (pre-registered bar: ≥80% = consolidation)

| law | W6a | W6b | pooled |
|---|---|---|---|
| **L1 intersection-of-all** | 6/6 | 6/7 | **12/13 = 92% → CONSOLIDATION** |
| L2 last-hand | 6/6 | 5/7 | 11/13 = 85% → consolidation |
| L3 last-two | 6/6 | 6/7 | 12/13 = 92% → consolidation |

L1 and L3 tie; **L1 wins by Occam** — L3's "two" is a free cutoff that
L1 doesn't need (in W6a last-two ≡ all because the weakest hand is near
the end; in W6b they differ only on constraints nobody's last-two hold).
**The statute: a braid holds exactly the intersection of its hands'
solo hold-sets — and hands destroy outside their hold-set with high but
not perfect probability.**

## The two honest misses

1. **W6b's prose claim is FALSIFIED at constraint level.** "Constraints
   lost in transit are exactly what the final hands couldn't hold solo"
   is wrong twice: the braid LOST `c3_seal` (which final hand flash
   holds solo) and KEPT `c5_unique` (which no final hand holds solo).
   The prose survives only at score level (2/6 ≈ last hands' 2/6). The
   strict last-hand law is a coarser shadow of the intersection law.
2. **Destruction is probabilistic, not certain.** `c5_unique` surviving
   two hands that can't hold it solo (1 case in 13) shows hands outside
   their hold-set are a strong prior, not an axiom. The statute reads
   "holds ≈ intersection", not "holds = intersection".

## Copies-decompose stays separate case law

Flash×4 rounds lost constraints INSIDE flash's own solo hold-set both
times (W6a: seal, short_lines; W6b: c3_seal). No braid law covers
self-revision decay — copies-decompose remains its own statute. The
consolidation achieved is: weak-link evidence-pair (W6a 5/6, W6b 2/6)
+ hold-set arithmetic → one intersection law at 92%, no fitting.

## Disposition

Filed: W5 CONSOLIDATION for the braid side (L1, 12/13, ≥80% bar met),
with the last-hand phrasing downgraded to a score-level approximation.
Copies-decompose unconsolidated (needs a different formalization —
hold-set under self-revision is strictly smaller than solo hold-set).
