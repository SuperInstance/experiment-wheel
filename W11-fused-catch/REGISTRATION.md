# W11 — THE FUSED CATCH: registration

*Pre-registered BEFORE any W11 call. Committed and pushed before
execution. This file is the contract; the falsifiers are on record
here before any number exists. Grows from W8-queue/DESIGN.md Station
W11, which is the argument layer — this is the sealed spec.*

## Station

Verbatim voting is degenerate on poems: five different drafts never
repeat a line, so W4's bit-level majority vote has no literal form at
the artifact level. What survives the translation are the two
aggregation rules that CAN act on artifacts — and they are the two
doctrines the wheel already banked elsewhere:

- **SELECTION (best-of-K)** — run K braids, a fleet-side selector keeps
  the best catch by the mechanical checker. W1's selector precedent:
  no model ever sees the checker or any score.
- **FUSION (line-inheritance)** — the mechanical crossover. W1's
  sexual mode at artifact level: recombination instead of revision.
  Rule frozen below, verbatim from the design, before any run.

**The law candidate this station exists to test — LOCALITY:** the herd
can aggregate what is line-LOCAL (c1 word counts, c2 first letters —
each line independently checkable); global constraints (c3 seal
placement, c4 rhyme, c5 last-word uniqueness, c6 whole-text
punctuation) have no line-index home, so fusion cannot target them and
may break them by stitching lines from different parents.

## The hand

IDENTICAL to W6b/W7, verbatim: the 12-line chamber poem, six
interlocking constraints (line n has n words; acrostic
THEEILEENLAUN; one 12-hex seal with mod-12 word-count coupling; no
rhyming line-endings; unique final word; strict punctuation). Same
TASK string, same mechanical check(), same per-yard reviser prompt
wording (W7's REVISE dict), no model ever sees the checker. Scores
directly comparable to W6b/W7.

**Score convention (house, matches W6b/W7 arithmetic):** score = count
of True cells among the seven booleans {12_lines, c1..c6} (computed
max 7), reported "/6" per house convention; every gate below uses the
computed integer. (W7's ASC "5/6" = 12_lines+c1+c3+c4+c5 = 5.)

## Crew (one delta from the design, on record)

- **flash** — deepseek-chat via api.deepseek.com (key from ~/.bashrc,
  W7's extraction). Primary artifact generator: the K fresh first
  drafts. t=0.75, max_tokens 700, W7 settings.
- **kimi** — `kimi -p`, last-12-lines parse (W7 form). If kimi 403s:
  document the failure, kimi drops out, braids run as 2-hand
  flash→claude chains. No substitution.
- **claude** — `claude -p` (W7 form), the closer.
- **wesley — EXCLUDED this cast, recorded:** wesley is an ollama local
  model and the GPU is reserved for the W3b bench; this station is
  CPU/API-only by standing order. Crew delta from DESIGN.md, not
  hidden. Consequence: 3-hand braids (15 braid calls, not 20), well
  under the ≤30 cap.

## Protocol

1. **Phase 0 (nominal seed 20260831):** fresh solo pass, all three
   yards, single call each. Doubles as the yard availability check
   (no separate pings; a transport failure here = yard drops out,
   recorded). deepseek receives seed=20260831; kimi/claude CLIs are
   unseeded — their own sampling, recorded as such.
2. **Phase 1:** K = 5 independent ascending braids (braid k = 1..5,
   nominal seed 20260831+k passed to deepseek; kimi/claude unseeded).
   Chain order fixed by MEASURED phase-0 solo score, weakest first,
   best solo closes; ties broken by W7's W6B_RANK (flash < kimi <
   claude). First hand gets the TASK alone; later hands get the W7
   reviser prompt with the prior attempt. Single pass per hand, no
   re-rolls, whatever it scores.
3. **G0 guard:** all five braid outputs + per-hand checks committed and
   pushed BEFORE any aggregation is computed (W3/W7 pattern: the raw
   catches go on record before the instrument touches them).
4. **Phase 2 (mechanical only, ZERO model calls):** on the five braid
   outputs compute SELECTION and FUSION (rule below), plus the five
   leave-one-out fusions (fuse four, hold one out). Score everything
   under the verbatim checker. The fusion engine + checker are
   written by OPENCODE (`opencode run --auto`) from this spec ONLY —
   opencode never sees any braid output, score, or check result; the
   engine is syntax-checked (py_compile) and its embedded checker is
   verified to reproduce W7's check() identically on every W11
   artifact before any fusion number is trusted.

## The FUSION rule (frozen here, verbatim intent from the design)

For line n (1..12): candidates are line n of each parent braid output,
aligned by index; a parent whose extracted line count ≠ 12 ABSTAINS
entirely (provides no candidates, is not a source in any branch).
Line extraction is the checker's own (strip; drop empties, `#` and
``` lines). A line-n candidate "qualifies" iff it satisfies BOTH
line-local constraints: exactly n words, and first letter (case
insensitive) = THEEILEENLAUN[n-1].

- Among qualifying candidates: take line n from the highest-scoring
  qualifying parent.
- If no candidate qualifies: inherit line n from the highest-scoring
  non-abstaining parent outright.

"Highest-scoring" = checker score; ties broken by lower braid index k
(deterministic, frozen). No repair, no model in the loop, rule frozen
here — uniform crossover with local-constraint selection.

## PREDICTIONS (on record before any run)

Per LOO fusion i (parents = the four braids with k ≠ i): "best parent"
= highest-scoring parent by (score, then lower k). LOCAL score = c1+c2
(0–2). GLOBAL score = c3+c4+c5+c6 (0–4).

- **P1 (locality):** fusion LOCAL score ≥ best parent's LOCAL score
  + 1, in ≥ 3 of 5 LOO fusions. (Strict secondary reading, reported:
  ≥ max over ALL parents' LOCAL + 1.)
- **P2 (global):** fusion GLOBAL score does NOT exceed the best
  parent's GLOBAL score, in ≥ 3 of 5 LOO fusions. (Strict secondary:
  ≤ max over ALL parents' GLOBAL.) Breaking a global the best parent
  held is EXPECTED under locality, not a violation of P2 — only
  EXCEEDING counts against it.
- **P3 (selection, near-free):** best-of-5 ≥ mean braid score + 1.

## Bars, kill gate, falsifiers

- **Kill gate (storm):** if fewer than 3 of 5 braids score ≥ 3 → STOP
  after phase 1, file the negative: fusion is underpowered, the pool
  has nothing local to inherit, W4's storm regime and the ≥60%
  per-unit-accuracy threshold extend from bits to artifacts.
- **Falsifier of locality:** P1 fails while braids had local
  violations to fix → locality dies as a law candidate; aggregation
  across braids is dead weight, single-chain doctrine stands. P2
  violated upward (fusion EXCEEDS best-parent global in ≥ 3/5) →
  stitching bought what has no line-index home — the harsher branch
  against locality, noted either way.
- **Honest headline risk (pre-noted):** if c2 is truly never-held
  (W9's wall), no pool line satisfies position-n's letter and fusion's
  c2 gain is structurally capped — P1 then rides on c1 alone. No
  post-hoc re-reading of a 1-point gain.

## Budget (hard cap ≤ 30 model calls; ledger kept in results)

Planned: 3 solo + 15 braid hands = 18. Transport-level failures only
(HTTP 5xx / timeout / CLI crash with no output) may be retried once,
counted; a completed generation is NEVER re-rolled. Phase 2 is zero
model calls (opencode's engine-writing is code from spec, not calls on
the hand, and is itself logged separately).

## What the verdict MEANS for the fleet

If locality holds: Waters crews run parallel braids and MATE the
catches — checker-guided line-inheritance becomes a standing fleet
instrument for line-local work while global constraints keep a single
mind (the closer). W1's regime law and W4's herd law fused into one
artifact-level doctrine. If it fails: the braid stays single-thread,
the herd stays bit-level, both doctrines survive unmerged — also worth
knowing before the fleet builds parallel crews.
