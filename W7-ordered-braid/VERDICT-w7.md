# W7 — THE ORDERED BRAID: verdict

*Station 1, third cast. The Weak-Link Law's pre-registered falsifier.
Same task, same checker, same crew as W6b. 622 seconds. Prediction was
on record in REGISTRATION.md (commit d6e1bb6) before this run.*

## The numbers

| mode | score | order / notes |
|---|---|---|
| solo claude | 4/6 | held 12L, c1, c3, c5 |
| solo kimi | 4/6 | held 12L, c3, c4, c5 |
| solo flash | 2/6 | held 12L, c5 |
| solo wesley | 2/6 | held 12L, c5 |
| **ASCENDING braid** (weakest→best) | **5/6** | wesley→flash→kimi→claude; per-hand 2→2→4→5 |
| **DESCENDING braid** (contrast) | **2/6** | claude→kimi→flash→wesley; per-hand 4→2→2→2 |

Fresh draw, and the solo vector landed exactly on W6b's seeding:
4/4/2/2. The measured-rank tiebreak (W6b order) resolved the tie pairs
the same way the registration predicted: wesley first, claude closes.

## VERDICT: law CONFIRMED

The registration's first pre-scored outcome, hit on both prongs:

- **ASC (5/6) ≥ best solo (4/6)** — the ascending braid didn't just
  hold the best hand's level, it EXCEEDED it by a point. Highest score
  any condition has ever reached on this task (W6b ceiling: 4, solo
  claude/kimi).
- **DESC (2/6) < best solo (4/6)** — reversed chain sank, exactly as
  the law predicted.

Order was the operative variable in W6b — not extra-hand degradation,
not prompt wording, not noise. Same crew, same task, same checker,
same solo vector; flip the order, flip the outcome (5 vs 2).

## Constraint survival vs W6b

| constraint | W6b solo (cl/ki/fl/we) | W6b braid | W7 solo | W7 ASC | W7 DESC |
|---|---|---|---|---|---|
| 12_lines | Y Y Y Y | **Y** | Y Y Y Y | **Y** | **Y** |
| c1_growth | . . . . | . | Y . . . | **Y** (claude closes it) | . (kimi kills claude's) |
| c2_acrostic | . . . . | . | . . . . | . | . |
| c3_seal | Y Y . . | . (lost) | Y Y . . | **Y** (kimi recovers) | . (kimi kills it) |
| c4_no_rhyme | . Y . . | . (lost) | . Y . . | **Y** (kimi recovers) | . |
| c5_unique_last | Y Y Y Y | **Y** | Y Y Y Y | **Y** | **Y** |
| c6_punctuation | . . . . | . | . . . . | . | . |

Read the mechanisms:

- **W7 ASC held exactly the constraints its LAST hands could hold**
  (kimi recovers seal+rhyme, claude adds c1) — weak hands touched the
  draft first and lost nothing that mattered, because capable hands
  came after and repaired. Order lets fixes STICK.
- **W7 DESC died exactly as W6b did, in the same cells**: claude's
  opening catch (c1, c3) was destroyed by kimi's reviser hand and never
  came back; flash and wesley held the floor at their own solo level
  (12L + c5 = 2/6) — the *identical* survivor set as W6b's braid.
  Reproduced floor: hands that can't hold a constraint solo cannot
  carry it in transit, and they finish the draft.

Two honest footnotes:

1. **Reviser-mode ≠ solo-mode.** kimi holds c3 and c4 solo, yet as
   DESC hand-2 he *broke* claude's passing seal. As ASC hand-3 he
   *recovered* both from a broken draft. A hand fixes what it notices
   broken and damages what it rewrites blind — the draft it receives
   decides which. The law survives this nuance (capability set still
   bounds everything), but "weak-link" is about the ceiling, not a
   guarantee of repair.
2. **The permanent kernel stands.** c2_acrostic and c6_punctuation
   were never held by anyone in any condition across W6b + W7 (fresh
   draws, braids, all hands). No ordering can buy what no hand can
   hold. Task is not too easy — no ceiling effect; 5/6 is the honest
   top.

## What it means

The Weak-Link Law is now bidirectional with a confirmed falsifier
survived: **the hands that touch a draft LAST set its ceiling; order
the chain ascending and the crew's best becomes the floor.** W6b's
practical doctrine ("ascending skill, or same-water yards") is
validated, not just inferred. Copies-decompose (W6a/b) and weak-link
(W6b/W7) now form a coherent pair: self-revision decays, unequal
backwards chains decay, ascending mixed chains gain.

For the fleet doctrine (Waters): place each mind where its skill is
real — AND sequence the relay so the strongest hands are the last
ones to touch the catch.

## Disposition

Filed: W7 complete. Law banked bidirectionally. W5 (case-law math,
pre-registered at 0707863) wanted W7's contrast as input — it now has
it: ASC 5/6 / DESC 2/6 at identical solo vectors is the cleanest
hold-set pair the arithmetic could ask for. No re-rolls taken; single
pass per condition, scores as measured.
