# W11 — SEALED AMENDMENT 1: the instrument's blind kernel

*Sealed BEFORE phase 2 ran. w11-results.json did not exist when this
was committed. Precedent: W5's REGISTRATION-sealed-amendment.md.*

## The discovery (found during engine verification, before any number)

OPENCODE wrote the phase-2 engine from the registration spec and, in
its self-test construction, surfaced two properties of the FROZEN
W6b/W7 checker. Both independently verified by the fleet (proof
commands on record in the run log):

1. **c2_acrostic is unsatisfiable by construction.** The target
   `THEEILEENLAUN` is **13 letters**; the checker requires exactly 12
   lines and compares the 12 joined first letters to the 13-char
   string — always False, for every possible poem. The TASK string
   itself demands a 13-letter acrostic of 12 lines: the hand was never
   fairly asked.
2. **c6_punctuation is unsatisfiable by construction.** The checker
   asserts `sorted(punc) == ['.', ',']`, but `sorted` always yields
   `[',', '.']` (U+002C < U+002E). A poem with exactly one comma and
   one period can never pass.

Consequences, stated plainly: the **never-held kernel (c2+c6)** —
never held by any yard in any condition across W6b/W7 — is at least
partly an INSTRUMENT artifact, not (necessarily) a model-class wall.
The "5/6 honest ceiling" is the checker's ceiling, not the crew's.
All W6b/W7/W11 measured scores STAND as measured (the instrument was
frozen and identical across all of them — comparability is intact);
what changes is INTERPRETATION. W9 (never-held kernel station) is
contaminated as designed: it must not burn 200 calls on a bug.

## What does NOT change (primary adjudication)

Phase 2 runs exactly as registered: frozen checker, frozen fusion
rule, frozen SELECTION/LOO/P1/P2/P3. P1 is now known-structurally
capped: every braid's LOCAL score is 1 (c1 held, c2 impossible), and
no fusion can exceed 1 — **P1 will read 0/5 for instrumental
reasons**, and the verdict will say so rather than pretend locality
was fairly tested on c2. No re-rolls, no substitutions, results as
measured. The engine's self-test is amended to assert the SYNTHETIC
all-constraints poem scores {12L,c1,c3,c4,c5}=True, c2=c6=False under
the frozen checker (documenting the structural ceiling), plus the
unchanged fuse toy-case checks.

## What is ADDED (diagnostic layer, flagged post-hoc instrument)

A corrected lens over the SAME single-pass artifacts, zero new model
calls, reported as separate numbers that NEVER replace the primary:

- **c2'** (acrostic, corrected): joined 12 first letters equal
  `THEEILEENLAU` — the first 12 letters, which is exactly what the
  frozen fusion rule's `qualifies()` already targets at every line.
- **c6'** (punctuation, corrected): punc multiset == {one comma, one
  period} (i.e. `sorted(punc) == [',','.']`), caps rule unchanged.
- LOCAL' = c1+c2', GLOBAL' = c3+c4+c5+c6'. P1'/P2'/P3' recomputed on
  the same LOO fusions under this lens — the honest answer to "did
  fusion actually assemble what no single chain held, once the
  instrument can see it."

## Ledger

Phase 2 model calls: zero (unchanged). OPENCODE's engine-writing is
code-from-spec, logged separately, and opencode has still never seen
any braid output or score.
