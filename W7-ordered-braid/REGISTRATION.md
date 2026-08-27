# W7 — THE ORDERED BRAID: registration

*Pre-registered BEFORE any W7 run. Committed before execution. This file
is the falsifier on record.*

## Station

Station 1, third cast. W6b banked the **Weak-Link Law**: a braid holds
only what its weakest RELEVANT hand can hold — the hands that touch a
draft LAST set its ceiling. Evidence pair: W6a (near-equal yards) →
braid held 5/6; W6b (mixed crew, weak hands last) → braid sank to 2/6
against a 4/6 best solo, losing exactly the constraints (seal, rhyme)
its final hands couldn't hold solo.

W6b's doctrine said: braid order should be ascending skill — weakest
drafts first, strongest closes. That is a prediction, and this cast
tests it.

## The hand

IDENTICAL to W6b, verbatim: the 12-line chamber poem, six interlocking
constraints (line n has n words; acrostic THEEILEENLAUN; one 12-hex
seal with mod-12 word-count coupling; no rhyming line-endings; unique
final word; strict punctuation — one comma, one period, no other).
Same TASK string, same mechanical check(), no model ever sees the
checker. Scores 0–6, directly comparable to W6b.

## Crew

claude (claude -p) · kimi (kimi -p, last 12 lines) · flash
(deepseek-chat via api.deepseek.com) · wesley (ollama
granite3.1-dense:2b at 127.0.0.1:11434).

## Protocol

1. **Solo pass first** — all four yards attempt the task cold. Scores
   measured fresh (W6b seeded 4,4,2,2 but this is a new draw).
2. **Ordered (ascending) braid** — chain by MEASURED solo score,
   weakest first, best solo closes (predicted shape: wesley → flash →
   kimi → claude, adjusted to measured ranks; ties broken by W6b rank).
   First hand gets the full task alone; every later hand gets full
   task + prior attempt, same per-model prompt wording as W6b.
3. **Descending braid (contrast pair)** — same crew, reversed: best
   solo first, weakest last. The law predicts this one SINKS.

## PREDICTION (on record before the run)

With the ASCENDING-skill chain (weakest drafts first, strongest
closes), the ordered braid scores **≥ best solo score** of the crew.

## Falsifier

If the ascending braid scores **< best solo**, the Weak-Link Law is
FALSIFIED: order was not the operative variable in W6b — something
else (any-extra-hand degradation, prompt wording, mere noise) sank the
mixed braid, and "ascending order" is not a fix.

Possible outcomes, scored honestly:

- **ascending ≥ best solo AND descending < best solo** → law CONFIRMED
  (order is the variable, both directions).
- **ascending < best solo** → law FALSIFIED as stated.
- **both braids ≥ best solo** → law COMPLICATED (task too easy this
  draw, or any braid survives; ceiling effects noted, verdict honest).

## Guards

- No re-rolls: single pass per condition, whatever it scores.
- Registration committed before execution; results committed after,
  unedited.
