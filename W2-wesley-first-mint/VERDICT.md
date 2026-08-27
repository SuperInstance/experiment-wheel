# W2 — WESLEY'S FIRST MINT: verdict

*Experiment Wheel, second formal turn. Station 2 (bench, RTX 4050).
Pre-registered in REGISTRATION.md (2026-08-26 22:35 AKDT) before any
corpus or query. Raw: RESULTS.json, w2-corpus.json, w2-ledger-{train,
test}.json, w2-mint.json. Code: corpus_gen.py, w2_bench.py.*

## The gates (pre-registered)

| gate | bar | measured | pass |
|---|---|---|---|
| G1 accuracy | mint ≥ 0.90 × Wesley AND Wesley ≥ 0.60 | ratio **1.04**, but Wesley **0.49** | **FAIL** (guard) |
| G2 speed | ≥ 100× | **49,905×** (67.6 ms → 1.35 µs/item) | pass |

**FILED NEGATIVE — inconclusive by the pre-registered guard.** The mint
kept 104% of Wesley's accuracy at fifty-thousand-fold speed, and it
still doesn't count: a mind at 49% on a binary task is a coin, and the
registration said so in advance ("a mind at chance cannot be distilled").
The kill gate fired exactly as designed. No rescue attempted.

## What actually happened (the honest story)

The ledger tells it in one line: **Wesley answered YES 242 / 300 times.**

| category | train answers | test Wesley acc | test mint acc | ground YES rate |
|---|---|---|---|---|
| FOG | 36 yes / 14 no | 0.32 | 0.32 | 0.32 |
| SQUALL | 26 / 24 | **0.80** | **0.88** | 0.44 |
| GONGO | 49 / 1 | 0.56 | 0.56 | 0.56 |
| COLD | 50 / 0 | 0.28 | 0.28 | 0.28 |

On three of four categories the 2B mind is a **constant cautious
watchman**: risk-leaning questions ("should you postpone?", "is severe
hypothermia a live risk?") under uncertainty, without the thresholds,
get YES — accuracy equals the ground YES rate, which is what answering
YES-always scores. GONGO (49/1) and COLD (50/0) are constants, full
stop. This is not noise; it is the rational prior of a small mind
never told the numbers. **The question was never "can bands copy a
mind" — it was "is there a mind to copy," and on 75% of the corpus
there wasn't.**

**The exception proves the mechanics work.** SQUALL is the one category
with a binary cue Wesley can actually read — cumulonimbus visible or
not. The agreement matrix shows it perfectly: without CB his bands run
0% yes (sealed), with CB 93–100% yes (sealed). He ignores the barometer
fall almost entirely, but the one cue he reads, he reads reliably — and
the mint turned 0.80 into **0.88** by majority-vote denoising. Where
the mind discriminates, the mint preserves and improves it.

**Error canonization, witnessed.** The mint sealed COLD's constant-YES
into five sealed bands and GONGO's into five more — hardening a flaw
into scripture, the failure mode the registration pre-named. 14/29
occupied bands sealed; roughly a third of the seals are canonized bias.
A mint is a mirror, not a mind: it reflects the substrate faithfully,
including the emptiness.

## The cross-check (who's right when they disagree)

8 disagreements on the held-out 100: **mint right 5, Wesley right 3,
both wrong 0.** SQUALL: 2–0 mint. FOG: 3–3 even. The direction is
denoising (the band median-filters his per-item wobble), but at n=8 it
is a whisper, not a law. Both-wrong zero is the constant-bias shadow:
when the mint disagrees with Wesley it is usually the band snapping his
rare NO back to YES — right exactly as often as the YES rate allows.

## Material note

granite3.1-dense:2b on the 4050 answers in 61 ms median (8 tokens,
prompt eval included) — the 100× bar was never the risk; 49,905× says
the speed question is closed at this scale. The latency of a mind and
the latency of a lookup table are different physical quantities. W1's
doctrine holds: know your materials. Here the material that failed was
not the silicon — it was the judgment being minted.

## Wheel dispositions

- **W2: FILED NEGATIVE (inconclusive by guard).** Minting mechanics
  validated — 92% agreement, 1.04× accuracy retention, 5×10⁴ speedup,
  sealing behaves as registered — on a substrate that didn't clear the
  interpretability bar.
- **W3 (dissent-fed mints): DO NOT FIRE AS DESIGNED.** The premise —
  feeding boundary disagreements back to re-teach the bulk — requires a
  bulk that discriminates. Wesley's dissent on 3/4 categories is the
  noise of a constant, and re-feeding it would canonize bias faster.
  Redesign, two honest paths: (a) **W3a — same registration, stronger
  judge** (qwen3:8b or deepseek-r1:8b, both on the bench, must clear
  0.60 on this same corpus before any minting), Wesley demoted to
  SQUALL-watch where he actually sees; or (b) **W3b — dissent between
  minds** ( Wesley vs. the 8B on SQUALL-style binary-cue items, bands
  minted from their disagreements rather than from one mind's bulk).
  Recommend W3a; it reuses this corpus, registration template, and
  bench unchanged.
- **Canon:** the YES-watchman result goes in the fleet's model book —
  small cautious minds default to the protective answer on threshold-
  precise tasks; never mint what hasn't cleared the discrimination bar.
