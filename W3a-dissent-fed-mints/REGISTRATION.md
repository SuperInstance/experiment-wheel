# W3a — THE UPGRADED JUDGE: dissent-fed mints: registration

*Experiment Wheel, third formal turn (replaces W3 as designed). Station 2
(bench, RTX 4050). Registered 2026-08-26 23:17 AKDT — BEFORE any corpus
generation or query. Provenance: direct re-fire of W2's own recommendation.
W2 filed negative-inconclusive: Wesley (granite3.1-dense:2b) sat at 0.49
held-out accuracy — a constant-YES watchman on 3/4 categories — so nothing
above him could be interpreted. W2's cross-check named the cure: "W3a —
same registration, stronger judge (qwen3:8b or deepseek-r1:8b, both on the
bench, must clear 0.60 on this same corpus before any minting)." This is
that experiment, plus the dissent-feeding loop W2 could not test because
Wesley's bias would canonize. The mint learns from the JUDGE'S answers
only, never from ground truth — unchanged from W2.*

---

## Question (one)

Does a judge that clears the 0.60 discrimination guard mint bands that
hold their OWN accuracy (error canonization avoided) — and when the
frozen bands' answers are fed back to the judge as labeled dissents and
the mint re-struck, does dissent-feeding improve the mint, degrade it,
or do nothing?

## The mind under test

Judge = `qwen3:8b` on Ollama (127.0.0.1:11434), temperature 0.3,
num_predict 8, keep_alive 30m, chat endpoint, non-streaming. Primary
protocol: API flag `"think": false` (disable qwen3 hybrid thinking;
bench runs ollama 0.32.15 which supports it). Fallback tree (registered,
applied uniformly per-run, protocol recorded in every ledger): if the
API rejects the `think` key with HTTP 400, or if the warm-up reply shows
thinking rather than a strict answer, switch the whole run to
`/no_think` appended to the system prompt with no `think` key. Strict
answer protocol: one word YES or NO. Parse = first `\b(yes|no)\b` match
(case-insensitive); up to 3 attempts; final failure → UNPARSED, excluded
from all accuracy/agreement denominators (count reported; >5% of any
ledger → interpretability flag in verdict). System prompt unchanged in
substance from W2: "You are the weather watch aboard a small sailing
vessel in Southeast Alaska. You answer strictly one word: YES or NO.
Nothing else."

Why qwen3:8b and not deepseek-r1:8b: r1 cannot disable its reasoning
trace, so a strict 8-token one-word protocol is unrunnable without
abandoning the registered answer format; qwen3 is first choice in the
tasking order anyway.

## Corpus — 300 weather-watch binary items, 4 categories × 75

**Identical generator logic to W2** (`corpus_gen.py`, copied verbatim
except: seed **20260827**, output `w3a-corpus.json`). Ground rules truth
by fiat, exactly as W2:

| cat | item gives | YES iff |
|---|---|---|
| FOG | dew-point depression (°C, 1dp), wind (kt) | dep ≤ 2.0 AND wind ≤ 6 |
| SQUALL | cumulonimbus visible (y/n), 3-h barometer fall (hPa, 1dp), wind (kt, context only) | CB visible AND fall ≥ 1.5 |
| GO/NO-GO | sustained wind (kt), seas (ft, 1dp), vessel length (ft, context only) | wind ≥ 22 OR seas ≥ 6.0 OR (wind ≥ 18 AND seas ≥ 4.0) |
| COLD | water temp (°C, 1dp), air temp (°C, context), immersion suits aboard (y/n) | (water ≤ 5 AND no suits) OR (water ≤ 2 AND suits) |

Boundary mixture p=0.5 near-window per category, ranges, rounding, exact
phrasing templates: W2 REGISTRATION.md §Corpus (binding, reproduced in
W3a corpus_gen.py verbatim). New seed only — fresh draw, no re-rolls,
realized YES rates reported whatever they are.

## Split

Seeded shuffle within category → **200 train / 100 held-out** (25 per
category, stratified). Held-out is never queried, binned, or inspected
before M1 is frozen; it is queried twice in total (round 1 and round 2,
see below) and its items never enter any prompt prefix.

## Stage 0 — G0 guard (new, gates the whole experiment)

Judge answers all 200 train items (plain protocol, no prefix). Guard:
judge train accuracy vs ground rules (parsed subset) **≥ 0.60**. If not:
**FILE NEGATIVE-INCONCLUSIVE and STOP** — no mint, no held-out queries,
no dissent round. A mind below the bar cannot be distilled, and its
dissent is the noise of a coin (W2's lesson, now pre-registered as a
hard gate).

## The mints (bands from the agreement matrix — W2's, unchanged)

Band keys at the operational thresholds:

| cat | band key (bins) |
|---|---|
| FOG | dep {≤2, 2–4, >4} × wind {≤6, 7–10, ≥11} → 9 |
| SQUALL | CB {y,n} × fall {<1.5, 1.5–2.5, ≥2.5} → 6 |
| GONGO | wind {≤17, 18–21, ≥22} × seas {<4, 4–6, ≥6} → 6 |
| COLD | water {≤2, 2–5, >5} × suits {y,n} → 6 |

Minting: per band, the judge's TRAIN majority answer is the band's
frozen label. Tie or unseen → category's global train majority
(fallback, baked in; tie → NO). Sealing: n ≥ 5 AND ≥90%
judge-consistency = SEALED. Lookup = pure numpy, bin → index → label
gather. M1 frozen (timestamped) after the round-1 train ledger, before
any held-out query.

## Round 1 — first mint test

Held-out 100: judge answers (plain protocol) → J1; M1 answers → M1.
Gates:

- **G1 ACCURACY:** M1 ≥ 0.90 × J1 on held-out (parsed subset).
- **G2 SPEED:** judge mean per-query latency (round-1 held-out pass,
  end-to-end HTTP, pre-warmed) ≥ 100 × mint vectorized mean latency
  per item (single cold pass over all 100; single-item median over
  1000 reps reported as secondary).
- BOTH must pass. Either fails → negative, filed honestly, no rescue.
  (Dissent round still runs if G0 passed — the W3a question stands even
  if a speed/accuracy gate fails — but the filing names the gate
  failure.)

**Headline cross-check (the canonization question):** M1 vs J1 held-out
accuracy, and every M1≠J1 disagreement adjudicated against the ground
rules (mint right / judge right / both wrong, per category). M1 ≥ J1
with mint-right ≥ judge-right → bands DENOISE the judge: error
canonization avoided at first strike.

## Round 2 — the dissent feed (W3a's own question)

1. Dissent set D = train items (parsed) where **M1's frozen band label
   ≠ the judge's round-1 answer**. |D| reported.
2. If |D| > 60: seeded subsample (np default_rng(20260828), without
   replacement, order by item id) to 60 — keeps the prefix ≤ ~2.5k
   tokens. Registered cap, both counts reported.
3. Feedback prefix (fixed format), prepended to the user turn for ALL
   round-2 queries:
   `Standing orders from the ship's log — settled answers:\n` +
   one line per dissent `— {item prompt} → {YES|NO (M1 band label)}` +
   `\nNow answer today's question the same way, strictly one word: YES
   or NO.` System prompt unchanged. The judge is being shown where his
   own frozen bands overruled him — labeled with the BAND's answer
   (never ground truth).
4. Judge re-answers all 200 train items with prefix → ledger L2 →
   **M2** minted from L2 by the identical rule (same band keys, same
   fallback, same sealing), frozen, timestamped.
5. Held-out 100 re-queried with the SAME prefix → J2, M2.

No ground truth anywhere in round 2's inputs. The only new information
is the judge's own majority-filtered judgment reflected back.

## Round-2 metrics and pre-named interpretations

- **ΔM = M2 − M1** (held-out): ≥ +0.03 IMPROVE; ≤ −0.03 DEGRADE;
  between → NULL. (n=100, binomial σ ≈ 0.04 — coarse; stated.)
- **ΔJ = J2 − J1**: did the feedback teach the mind or hurt it?
- Train-side: L2 accuracy vs ground rules; L2 agreement with M1's
  labels (did the judge absorb his bands?).
- Sealed-band error rate: M1 vs M2 vs ground rules on train bands
  (did canonization shrink?).
- Pre-named: IMPROVE + ΔJ ≥ 0 → dissent-feeding is a distillation
  win (bands teach the mind its own median; W3 line lives — scale it).
  DEGRADE → canonization pressure confirmed even above the 0.60 bar;
  dissent-feeding dies as a technique. NULL → the prefix neither
  teaches nor corrupts at this scale — file honestly, no rescue.
  ΔJ < 0 with ΔM ≥ 0 → the feedback hurt the mind but the re-mint
  absorbed it (bands as shock absorbers).

## Filing

RESULTS.json (guard, corpus balance, both train ledgers, both agreement
matrices, both held-out passes with per-category accuracy, disagreement
adjudications both rounds, latencies, gates, dissent deltas), VERDICT.md,
raw ledgers and mints (w3a-corpus.json, w3a-ledger-train{1,2}.json,
w3a-ledger-test{1,2}.json, w3a-mint{1,2}.json, w3a-dissent.json), all
committed to the experiment-wheel repo. Honest numbers only, including
a Wesley-SQUALL cross-reference (W2's demotion recommendation checked
against the upgraded judge's category profile).
