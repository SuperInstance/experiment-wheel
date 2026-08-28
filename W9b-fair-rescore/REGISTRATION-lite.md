# W9b — THE FAIR-INSTRUMENT RE-SCORE (registration-lite)

*An OPERATIONS-DOCTRINE.md mid-term queue item, executed 2026-08-27 by the
TECH-WATCH lane. This is a REGISTRATION-lite, not a full registration:
nothing is being run, predicted, or sealed — an already-recorded corpus is
being re-scored under a corrected instrument. The wheel's precedents:
W9's pre-registered c2′ and Amendment-1 c6′ (W9-never-held-kernel/),
W11's sealed amendment 1 (corrected-lens diagnostic, same spirit).*

## What is being re-scored, and why

W9 proved the W6b/W7 checker's **c2** (13-letter acrostic `THEEILEENLAUN`
demanded of 12 lines) and **c6** (`sorted(punc) == ['.', ',']`, impossible
under ASCII 0x2C < 0x2E) were **unsatisfiable by construction** — the
"never-held kernel" was instrument blindness, not a crew wall. W9 exported
the fair cells **c2′** (first 12 letters spell `THEEILEENLAU`) and **c6′**
(one comma + one period, correct sort, caps line-initial, 12 lines).

This station re-scores the **recorded artifacts of W6b and W7** — the two
stations whose scores were produced by the blind instrument — under those
fair cells. **Instrument correction, not a new experiment.**

## What this is NOT

- **The predictions are NOT re-sealed.** W6b/W7's sealed predictions were
  about conditions and order, scored under the then-frozen instrument;
  they stand exactly as filed. Only **artifact scores** are recomputed.
- **Not a re-roll.** Zero model calls (pure local compute; no network, no
  GPU/ollama). Recorded artifacts are read-only; their bytes are untouched.
- **Not a replacement of the frozen numbers.** Frozen scores stand as
  measured (the instrument was identical across every condition ever run —
  comparability intact). Fair-lens scores are reported **alongside**.

## Corpus (chain of custody)

- `W6-the-braid/w6b-results.json` — 6 artifacts: solos (claude, kimi,
  flash, wesley), copies (flash ×4, final), braid final
  (kimi→claude→flash→wesley→flash). Single committed version (ac264ff);
  disk == HEAD == git, byte-identical (verified).
- `W7-ordered-braid/w7-results.json` — 6 artifacts with surviving text:
  solos ×4, braid ASC final, braid DESC final. Single committed version
  (f578593). The 8 intermediate braid-hand drafts survive as **scores
  only** (no poem text was recorded) — listed as not-preserved, not
  re-scored.
- **Excluded:** W6a (`w6-results.json`) — different task (13-line
  boat-pieces) and different checker, incomparable by design (W9 audit
  precedent). W10/W11 artifacts — their own stations; W11 already carries
  its own corrected-lens numbers; W10's re-measure is W9's doctrine item,
  not this one.

## Instrument (rescore.py, five gated stages)

1. **Identity** — `check()`, `c2_amended()`, `c6_amended()` ported from
   `W9-never-held-kernel/w9_check.py` and asserted **byte-identical at the
   source-line level** (and `check()` identical to `w6b_spike.py` /
   `w7_spike.py` — W9's audit claim re-verified) before anything runs.
2. **Satisfiability witnesses** (doctrine: no cell scores until it has a
   witness) — constructions exhibiting c2′ TRUE and c6′ TRUE; a
   **full-board witness** holding all 7 cells under the fair lens; and the
   mechanical impossibility proofs for verbatim c2/c6. The same perfect
   poem scores 5/7 under the frozen instrument — the blindness exhibited
   in one construction.
3. **Verification against W9's own recordings first** — all 119 W9 ledger
   poems replayed: 119 check-dict + 119 c2′-flag + 16 c6′-flag
   comparisons, zero mismatches, gate to proceed.
4. **Re-score** — every W6b/W7 artifact: frozen check replayed (must equal
   the recorded check — custody intact), c2/c6 asserted False (impossibility),
   c2′/c6′ applied mechanically. New score = old + c2′ + c6′.
5. **W11 crosscheck comparison** — each row of
   `W11-fused-catch/w11-crosscheck-w6w7.json` confirmed or corrected by
   this independent pass.

Outputs: `RESCORE.json` (per-artifact: old score, new score, cells
changed, poem sha-256/12), `VERDICT-w9b.md` (corrected scoreboard).
SYNTHESIS.md receives a dated appended correction note only — history is
not rewritten.
