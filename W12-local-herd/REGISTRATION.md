# W12 — THE LOCAL HERD (registration, sealed before any model call)

*Station: local silicon. Lane: LOCAL-HERD. W4 proved the herd law in
simulation (majority vote repairs copy errors free in calm water). This
experiment asks whether the law holds on REAL chips we own: a skill
ladder of five small local models, one GPU (RTX 4050), no cloud.*

## The question

Can 3-voter majority voting across a ladder of small local models beat
the best single model on a fixed binary weather-watch corpus? And what
does the herd cost or gain when the weakest voter is barely (or not)
above chance — and when voters share a family (correlated errors)
versus come from different lineages?

## Pre-registered predictions (sealed before run)

- **P-GUARD (W2's guard):** a trio will not beat best-single if its
  weakest member's solo accuracy is below chance (<0.50). Herding with
  a sub-chance voter drags the vote toward noise.
- **P-DIV (diversity):** cross-family trios (3 distinct model families)
  outperform same-family-pair trios (2 members from one family) —
  correlated errors waste votes.
- **P-MAIN (conjunction):** herd > best-single ONLY where P-GUARD and
  P-DIV conditions both hold for that trio.
- **FALSIFIER:** if no trio, in any condition, beats best-single by the
  pre-registered margin, the herd law is simulation-only at this scale —
  file honestly as a negative.

## Corpus

W3a corpus generator, logic VERBATIM (registration binding: FOG / SQUALL
/ GONGO / COLD rules unchanged), with:
- NEW seed: 2026082712 (never used by W3a seed 20260827).
- 60 items: 15 per category, selected to exact global 30 YES / 30 NO.
- **Satisfiability (W9 doctrine):** the generator must EXHIBIT a
  concrete YES construction and a NO construction per category (probes
  evaluated by the same gt expression, not hand-asserted), AND the
  realized 60-item corpus must contain both labels in every category.

## Minds (ollama, 127.0.0.1:11434) — the skill ladder

| rank | model | params | family |
|------|-------|--------|--------|
| 1 | qwen2.5:0.5b | 0.5B | Qwen2.5 (weakest, expected) |
| 2 | Liquid-LFM2.5-2.6B | 2.6B | Liquid |
| 3 | qwen2.5:3b | 3B | Qwen2.5 |
| 4 | phi3:3.8b | 3.8B | Phi-3 |
| 5 | mistral:7b | 7B | Mistral |

Ladder order is by parameter count; ACTUAL skill is measured by solo
accuracy (that is a result, not an assumption).

## Solo pass (identical for all minds)

- Prompt: the corpus item's `prompt` verbatim; system prompt verbatim
  from W3a/W3b: "You are the weather watch aboard a small sailing vessel
  in Southeast Alaska. You answer strictly one word: YES or NO. Nothing
  else."
- ollama `/api/chat`, temp 0.3, num_ctx 2048, num_predict 8.
- Parse: LAST `\b(yes|no)\b` (case-insensitive) in the reply; up to 3
  attempts; then honest UNPARSED (excluded from scoring denominators,
  counted separately). Infra failures retried 5×/backoff (W3b patch
  pattern); unrecoverable = honest ledger null; >10% null/UNPARSED in a
  ledger aborts that mind's pass.
- **Checkpoint-in-teeth:** ledger flushed (atomic write) every 10 items;
  rerun resumes from partial.
- **Serial GPU discipline:** weakest→strongest order; one model resident
  at a time (keep_alive 30m during a pass; explicit unload
  `keep_alive=0` + settle before next mind loads).

## Herd conditions (offline replay on the solo ledgers — no extra GPU)

1. **Random trios:** ALL C(5,3)=10 combinations (census, no sampling).
2. **Skill-stratified trios (designated):** param-adjacent windows
   {0.5b, LFM2.6, 3b}, {LFM2.6, 3b, phi3}, {3b, phi3, 7b} PLUS the
   design-named {0.5b, 3b, phi3}, {3b, phi3, 7b} (dup ok), {0.5b, 3b,
   3.8b-style span}.
3. **Best-single:** max solo accuracy (parsed-subset) — the bar.

Vote rule: majority of 3 cast votes (2-1 or 3-0 decides). Missing vote
(UNPARSED/null) = abstention: 2 cast votes decide only if unanimous,
else (and with 1 cast vote) the trio is UNRESOLVED on that item —
excluded from that trio's denominator, counted separately.

## Scoring & decision rule

- Solo acc = correct / parsed, per mind (CI: Wilson).
- Trio acc = majority-correct / decided, per trio.
- **BEAT = trio_acc − best_single_acc ≥ 2/60 (≥ 3.33pp)**, primary;
  paired bootstrap (10k resamples over items, seed 2026082712) for the
  headline trio reported as context (n=60 is small; margin rule is the
  sealed primary).
- P-GUARD evaluated per trio on its weakest member's solo acc.
- P-DIV: mean trio acc, cross-family (3 distinct) vs same-family-pair.

## GPU encounter log (honesty)

2026-08-27 18:39 AKDT: pre-flight found the W3b bench (deepseek-r1:8b)
DEAD, not running — log stale since 12:27 (stalled "train1 100/200",
no 'bench complete'), no ollama process, port 11434 refusing
connections, GPU idle. The wait-guard applies to a LIVE bench; nothing
to wait for. Following the W3b lane's own precedent (their log: ollama
"fully down, connection refused" → started detached as eileen), ollama
serve was started the same way at 18:39. W3b files were NOT touched.
All five W12 minds are confirmed present in `ollama list`.

## Fence order

Registration commit → corpus gen (+ satisfiability exhibit) → solo
passes weakest→strongest, incremental ledger commits → herd analysis →
VERDICT.md. Push with rebase discipline.
