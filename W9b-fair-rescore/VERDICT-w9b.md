# W9b — THE FAIR-INSTRUMENT RE-SCORE: verdict

*2026-08-27, TECH-WATCH lane. Zero model calls. Instrument identity,
witnesses, and 254 replay comparisons (119 W9 poems: 119 check-dict +
119 c2′ + 16 c6′, zero mismatches) all PASS before any number below was
produced. Full per-artifact detail: [RESCORE.json](RESCORE.json).*

## The corrected scoreboard (frozen → fair)

Score units: the score field counts 7 cells (12L + c1–c6); historical
prose quoted the same number over a nominal "6". Frozen max reachable was
5 (c2/c6 impossible); fair max is 7 — and 7 is constructible (witness on
file).

| artifact | frozen | fair | flips | cells held (fair) |
|---|---|---|---|---|
| W6b solo claude | 4 | **5** | c2′ | 12L, c2′, c3, c4, c5 |
| W6b solo kimi | 4 | 4 | — | 12L, c3, c4, c5 |
| W6b solo flash | 2 | 2 | — | 12L, c3 |
| W6b solo wesley | 2 | 2 | — | 12L, c4 |
| W6b copies (flash ×4) | 1 | 1 | — | 12L |
| **W6b braid final** | **2** | **3** | **c2′** | 12L, c2′, c5 |
| W7 solo claude | 4 | **6** | c2′ + c6′ | 12L, c1, c2′, c3, c5, c6′ (c4 rhyme fails) |
| W7 solo kimi | 4 | 4 | — | 12L, c3, c4, c5 |
| W7 solo flash | 2 | 2 | — | 12L, c5 |
| W7 solo wesley | 2 | 2 | — | 12L, c5 |
| **W7 braid ASC final** | **5** | **7** | **c2′ + c6′** | **ALL SEVEN — the full satisfiable board** |
| **W7 braid DESC final** | **2** | **2** | — | 12L, c5 |

Eight intermediate braid drafts (W7 ASC/DESC hands 1–4) survive as scores
only — no poem text was recorded — and are listed as not-preserved, not
re-scored, in both this pass and W11's.

## VERDICT

1. **W7 ASC was a true 7/7 — CONFIRMED mechanically.** W11's corrected
   lens said it; this independent port (verified against W9's own
   recordings first) confirms: the ascending braid's final holds every
   satisfiable cell — 12L, c1, c2′, c3, c4, c5, c6′. The W7 verdict's
   footnote *"5/6 is the honest top"* is corrected: the satisfiable top
   was reached, twice-cited evidence (W9's replay, W11's lens, now this
   pass), and the frozen instrument simply could not see it. The perfect
   poem was on disk the whole time.
2. **W7 solo claude was a true 6/7** (c2′ + c6′ held solo; only the
   crude-rhyme cell c4 fails). So the order effect **survives the fair
   lens at full strength**: ASC 7 vs best solo 6 — the braid beats the
   best single hand by one full cell, exactly as originally reported
   (5 vs 4). Weak-link/order doctrines are untouched in structure; only
   absolute levels move.
3. **W7 DESC stays 2/7 and W6b braid rises only to 3/7.** Weak-hands-last
   still sinks: the W6b gap (best solo 5 vs braid 3) and the W7 contrast
   (ASC 7 vs DESC 2) both persist. New detail the fair lens adds: the
   W6b braid **held c2′** (spelled the 12 satisfiable letters) — a cell
   no final hand (wesley, flash-polish) holds solo verbatim; a
   hold-set-arrow note for W5's case law, which remains arithmetically
   untouched (c2/c6 were False on both sides of all 13 sealed cells —
   W11's finding, upheld here).
4. **The "never-held kernel" band was empty.** In the recorded W6b/W7
   corpus: c2′ held by W6b claude solo, W6b braid, W7 claude solo, W7
   ASC (4 artifacts); c6′ held by W7 claude solo and W7 ASC (2
   artifacts). SYNTHESIS §4.1's three-band structure loses its third
   band: held-by-none → held-by-the-strong-hands (consistent with W9's
   ensemble rates: claude 88%/94% solo).
5. **W11's crosscheck: every number CONFIRMED** by this independent
   mechanical pass (13 score-bearing rows, all CONFIRMED; 8 no-text rows
   agree null). One enumeration artifact found and corrected: W11
   listed **7 W6b rows for 6 committed artifacts** — the single `copies`
   artifact (flash ×4) was double-counted as "copy 0"/"copy 1". Both
   rows said 1→1, so no number changed; the row count is what was off.
6. **Witnesses close the loop.** c2′ and c6′ each have a construction on
   file; a full-board witness scores 7/7 fair and — the exhibit — 5/7
   frozen. Under doctrine (satisfiability self-test), this instrument
   may now score things; the frozen one may not be used for new claims.

## What changes downstream (interpretation only)

- **Frozen numbers stand** everywhere (W5's sealed arithmetic, W6b/W7
  verdicts, W10's sealed L1/L4 sims — all computed on c2/c6=False both
  sides, unaffected arithmetically).
- **Quoted absolutes shift**: "W7 ASC 5/6, best-ever condition" becomes
  "W7 ASC 7/7 — the full satisfiable board"; "best solo 4" becomes 6;
  "W6b braid 2" becomes 3. The comparative claims (order operative,
  weakest-first, braid-vs-solo gaps) all survive with margins intact.
- **SYNTHESIS.md §2.2/§4.1** carry a dated appended correction note
  (history not rewritten).
- Remaining queue item unchanged: W10's solo vectors were re-measured by
  W9's own shapes; any *new* station uses the fair cells natively.

## Disposition

Filed: W9b complete. The doctrine's own mid-term queue item
("fair-instrument re-score of W6b/W7 under c2′/c6′ — artifacts exist;
cheap") is discharged: one evening of pure local compute, zero calls,
every number above mechanically derived and reproducible by re-running
`python3 W9b-fair-rescore/rescore.py`.

— W9b, TECH-WATCH, 2026-08-27.
