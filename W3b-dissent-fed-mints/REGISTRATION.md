# W3b — THE UPGRADED JUDGE, second cast: dissent-fed mints, deepseek-r1:8b

*Amended registration — Experiment Wheel, W3a re-armed with the second
recommended judge. Station 2 (bench, RTX 4050). Registered 2026-08-27
before any bench query. Provenance: W3a filed NEGATIVE-INCONCLUSIVE
(commit 4e9a670) — judge qwen3:8b scored 0.59 vs the 0.60 G0 bar on the
200-item train ledger and the pre-registered guard stopped the run
before minting. W2's verdict named two candidates: qwen3:8b (fired,
fell 0.01 short) and deepseek-r1:8b. This is the second cast: same
corpus, same split, same protocol skeleton, same G0 guard, same
mint/dissent design. Only the judge changes (plus its serving knobs and
its reasoner parse rule). If this judge also fails G0, that is two
judges below the bar and Station 2's premise dies for now — also a
result, filed honestly.*

---

## Question (one — unchanged from W3a)

Does a judge that clears the 0.60 discrimination guard mint bands that
hold their OWN accuracy (error canonization avoided) — and when the
frozen bands' answers are fed back to the judge as labeled dissents and
the mint re-struck, does dissent-feeding improve the mint, degrade it,
or do nothing?

## The mind under test (AMENDED)

Judge = `deepseek-r1:8b` on Ollama (127.0.0.1:11434), temperature 0.3,
**num_ctx 4096** (6GB RTX 4050 constraint; another bench may share the
GPU concurrently — tolerate slowness, never restart ollama),
keep_alive 30m, chat endpoint, non-streaming.

deepseek-r1 is a REASONER: it cannot disable its `<think>` trace. The
strict one-word protocol is therefore run at the ANSWER level, not the
token level: **num_predict 2048** (generous — the reasoning trace is
allowed to finish so the final answer token exists), and the parse rule
is: strip any `<think>...</think>` spans (including an unclosed trailing
`<think>` = truncated trace → UNPARSED for that attempt), then take the
**LAST** `\b(yes|no)\b` match (case-insensitive) in the remaining
content. Up to 3 attempts; final failure → UNPARSED, excluded from all
accuracy/agreement denominators (count reported; >5% of any ledger →
interpretability flag in verdict). System prompt unchanged from
W2/W3a: "You are the weather watch aboard a small sailing vessel in
Southeast Alaska. You answer strictly one word: YES or NO. Nothing
else."

## Corpus (UNCHANGED — W3a's corpus reused verbatim)

`w3b-corpus.json` is a byte-identical copy of `w3a-corpus.json` (seed
20260827, 300 items, 4 categories × 75, same generator, same ground
rules by fiat, same 200/100 stratified split, same realized YES rates
— FOG 11/6, SQUALL 18/9, GONGO 28/9, COLD 17/10 train/test). No
re-rolls, no redraws: the second judge faces the exact first corpus, so
G0 comparisons across judges are apples-to-apples.

## Stage 0 — G0 guard (unchanged, gates everything)

Judge answers all 200 train items (plain protocol, no prefix). Guard:
judge train accuracy vs ground rules (parsed subset) **≥ 0.60**. If
not: **FILE NEGATIVE-INCONCLUSIVE and STOP** — no mint, no held-out
queries, no dissent round. Second judge below bar = Station 2's premise
(killable local judges exist on this bench) is dead for now; that
filing names it.

## The mints, Round 1, Round 2 — ALL UNCHANGED from W3a's registration

Band keys, minting rule (band majority, tie/empty → category global
majority, tie → NO; sealing n ≥ 5 AND ≥90% consistency), M1 freeze
before any held-out query, round-1 held-out pass with G1 (M1 ≥ 0.90×J1)
and G2 (judge mean latency ≥ 100× mint vectorized mean), dissent set
D = train items where M1 band label ≠ judge round-1 answer, cap 60
(rng 20260828), fixed feedback prefix labeled with the BAND's answer
(never ground truth), L2 → M2 (identical minting rule), held-out
re-query with same prefix. Ground truth appears nowhere in round-2
inputs. Reproduced in code from W3a verbatim except judge model,
num_predict, and the reasoner parse rule.

## Round-2 metrics and pre-named interpretations (unchanged)

ΔM = M2 − M1 held-out: ≥ +0.03 IMPROVE; ≤ −0.03 DEGRADE; else NULL
(n=100, σ≈0.04, coarse — stated). ΔJ = J2 − J1. Train-side L2 accuracy
and L2-vs-M1 agreement. Sealed-band error rate M1 vs M2 (canonization
meter). Pre-named: IMPROVE + ΔJ ≥ 0 → distillation win, scale the W3
line. DEGRADE → canonization pressure confirmed above the 0.60 bar;
dissent-feeding dies. NULL → file honestly, no rescue. ΔJ < 0 with
ΔM ≥ 0 → bands as shock absorbers.

## Filing

RESULTS.json (guard, corpus balance, both train ledgers, both agreement
matrices, both held-out passes per-category, disagreement adjudications
both rounds, latencies, gates, dissent deltas), VERDICT.md, raw
artifacts (w3b-corpus.json, w3b-ledger-train{1,2}.json,
w3b-ledger-test{1,2}.json, w3b-mint{1,2}.json, w3b-dissent.json),
committed to experiment-wheel master, registration committed BEFORE the
bench runs (sealed-before-run). Honest numbers only.
