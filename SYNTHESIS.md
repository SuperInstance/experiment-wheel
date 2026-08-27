# SYNTHESIS — the wheel's first sweep (W1–W7)

*Experiment Wheel, 2026-08-26 → 2026-08-27 (~32 hours, seven turns).
This document states what is verified and links to the evidence files.
Nothing here is stronger than its weakest cited file. Design doc:
[EXPERIMENT-WHEEL.md](../../ai-writings/essays/EXPERIMENT-WHEEL.md)
(canon copy; identical to the workspace original).
W3b was in flight when this was written — placeholder in §6.*

---

## 1. The story on one page

The wheel asked whether a standing structure — pre-registration, sealed
predictions, kill gates, verdicts as first-class outputs — turns concepts
into trials more reliably than instinct. It then ran its first seven turns
against three real questions of the fleet:

**Q1 — Does recombination compound at scale?** (W1) Yes, with a caveat
that became a law: mating wins when the hand is demanding, asexual
copying wins when the hand is loose. The paper's appendix curve did not
reproduce (filed negative); the thesis survived on honest numbers.

**Q2 — Can a mind be distilled into lookup bands?** (W2, W3a, W3b) The
mechanics work — 49,905× speed at 104% accuracy retention, and the one
cue the substrate actually reads (SQUALL's cumulonimbus) was preserved
and *improved* (0.80 → 0.88). But both minds run so far sat below the
0.60 discrimination bar, and both pre-registered guards fired. A mind at
chance cannot be distilled; the question stands until a judge clears it.

**Q3 — What does a chain of different models compute that copies
cannot?** (W6a, W6b, W5, W7) The densest answer of the sweep. Copies
decompose (confirmed twice). A braid holds approximately the
intersection of its hands' solo hold-sets (consolidated 12/13 = 92%,
zero fitting parameters). And order is operative: with the identical
crew and solo scores, the ascending chain scored 5/6 — the first
condition ever to beat the best single hand — while the descending
chain sank to 2/6. The weak-link law survived its pre-registered
falsifier on both prongs.

**Q4 (bonus, bottom tier) — Does a cheap herd beat its best cell?**
(W4) In calm water, yes (CI-separated at low noise; majority vote
repairs copy errors for free at zero channel noise). In storms, no —
the sealed prediction had the regime wrong, and was filed wrong-regime.

### The index (every turn, one line, evidence-linked)

| turn | question | verdict | evidence |
|---|---|---|---|
| W1 | mating at 10,000 pairs | **PASS** + regime law; E2 appendix filed negative | [VERDICT.md](W1-mating-at-scale/VERDICT.md) |
| W2 | Wesley's first mint | **NEGATIVE-inconclusive** (guard: 0.49 < 0.60); SQUALL CB exception | [VERDICT.md](W2-wesley-first-mint/VERDICT.md) |
| W3a | stronger judge (qwen3:8b) | **NEGATIVE-inconclusive** (G0: 0.59 < 0.60, stopped before mint) | [RESULTS.json](W3a-dissent-fed-mints/RESULTS.json) |
| W3b | second-cast judge (deepseek-r1:8b) | **PENDING** — in flight, separate lane | [REGISTRATION.md](W3b-dissent-fed-mints/REGISTRATION.md) |
| W4 | ESP-NOW herd (host sim) | **wrong-regime negative** + calm-water positive | [RESULTS.md](W4-espnow-herd/RESULTS.md) |
| W5 | case-law math (hold-set arithmetic) | **CONSOLIDATION** — L1 12/13 = 92%, zero fitting | [VERDICT.md](W5-case-law-math/VERDICT.md) |
| W6a | braid of different (easy hand) | copies-decompose confirmed; kill gate not reached | [VERDICT.md](W6-the-braid/VERDICT.md) |
| W6b | braid at the demanding hand | weak-link law found (evidence pair); copies-decompose ×2 | [VERDICT-b.md](W6-the-braid/VERDICT-b.md) |
| W7 | the ordered braid | **law CONFIRMED**, both prongs; ASC 5/6 > best solo 4/6, DESC 2/6 | [VERDICT-w7.md](W7-ordered-braid/VERDICT-w7.md) |

### The honest scorecard

Seven turns produced: one consolidated quantitative law (W5), one
law confirmed against a pre-registered falsifier (W7), one law
confirmed twice (copies-decompose), two single-cast laws (mating
regime, herd calm-water), four first-class negatives or wrong-regime
filings (W2, W3a, W4-prediction, W1-E2), one instrument correction
(W6a → W6b design), and one question still open pending W3b. Every
turn was registered before running; every verdict was committed with
its raw data. No rescue attempts, no re-rolls. The wheel's own meta
from W1 held to the end: *the structure pays for itself.*

---

## 2. The laws on record (ranked by evidence strength)

Five statutes survived the sweep. They are ranked by how much sealed,
pre-registered evidence stands behind them — strongest first. Each entry
states the law, the evidence, and what would break it.

### 2.1 The intersection-of-all law (consolidated, quantitative)

**Statement.** A braid of chains holds constraint *c* if and only if
every hand in the chain holds *c* solo — the braid's hold-set is
approximately the intersection of its hands' solo hold-sets. Hands
destroy constraints outside their hold-set with high but not perfect
probability.

**Evidence.** [W5 VERDICT.md](W5-case-law-math/VERDICT.md): pooled
12/13 = 92% against a pre-registered ≥80% consolidation bar, computed
from solo hold-sets alone with **zero fitting parameters**. Laws,
scoring rule, and verdict rule were sealed in
[REGISTRATION-sealed-amendment.md](W5-case-law-math/REGISTRATION-sealed-amendment.md)
(commit 1d51ed5) before any arithmetic. Inputs: W6a (near-equal crew,
braid held 5/6) and W6b (mixed crew, braid sank to 2/6).

**The honest misses (on record in W5):** one survival of a constraint no
final hand holds solo (c5_unique, 1 case in 13) — destruction is a
strong prior, not an axiom; and the strict last-hand phrasing of W6b's
prose was falsified at constraint level (see 2.2).

**Scope note.** The sealed consolidation covers W6a + W6b only — both
chains run weak-hands-last. W7's ascending chain had not been through
the sealed scoring rule when W5 closed (the W5 lane explicitly sealed
itself to W6a+W6b), and W7's own table suggests ascending order stresses
this law: the ASC braid held c1/c3/c4 that its weak early hands cannot
hold solo. A quick unscored read gives L1 3/6 on W7-ASC vs the
last-hand reading 5/6. That is not sealed arithmetic — re-running the
W5 scoring with W7's chains added is the natural next cast (§5.1).

**Breaks if:** an ascending chain routinely holds constraints its
weakest hand cannot hold solo, at scale, under the sealed rule.

### 2.2 The weak-link law (confirmed against a pre-scored falsifier; score-level)

**Statement.** The hands that touch a draft last set its ceiling: a
braid's score sinks to the level of its final hands, and constraints
those hands cannot hold solo are lost in transit. Order the chain
ascending and the crew's best becomes the floor.

**Evidence.** The evidence pair: W6a (solo 5,5,5,4 → braid held 5/6) vs
W6b (solo 4,4,2,2 → braid 2/6, losing exactly the constraints its final
hands can't hold). Then
[W7 VERDICT-w7.md](W7-ordered-braid/VERDICT-w7.md): the falsifier was
pre-registered in [REGISTRATION.md](W7-ordered-braid/REGISTRATION.md)
(commit d6e1bb6) before the run — *ascending ≥ best solo AND descending
< best solo* — and both prongs hit. Same crew, same task, same checker,
identical solo vector (4/4/2/2, a fresh draw that landed exactly on
W6b's seeding): ASC 5/6, DESC 2/6. Order was the only operative
variable. ASC's 5/6 is the highest score any condition has reached on
this task, and the first time any braid beat the best single hand.

**Downgrade on record (from W5):** the *constraint-level* last-hand
phrasing was falsified in W6b — the braid lost c3_seal (which final
hand flash holds solo) and kept c5_unique (which no final hand holds).
The law survives at score level; the constraint-level mechanism belongs
to the intersection law (2.1). Hence: *score-level shadow*.

**Breaks if:** a descending chain holds its best hand's score, or an
ascending chain fails to reach best-solo, at scale.

### 2.3 Copies-decompose (confirmed twice, qualitative)

**Statement.** A model revising its own output loses constraints —
including ones it holds solo on a cold attempt. Self-revision decays;
the hold-set under self-revision is strictly smaller than the solo
hold-set.

**Evidence.** W6a: flash ×4 rounds, 5/6 solo → 3/6, losing seal and
line-length (both inside flash's solo hold-set). W6b: same protocol at
the demanding hand, 2/6 → 1/6. Two confirmations across two different
hands (easy and demanding), one evening.
([W6 VERDICT.md](W6-the-braid/VERDICT.md),
[W6b VERDICT-b.md](W6-the-braid/VERDICT-b.md))

**Formalization gap (on record in W5):** copies-decompose is *not*
covered by the braid intersection law and remains its own case law;
hold-set arithmetic under self-revision has not been measured.

**Breaks if:** self-revision chains hold score or gain, at scale.

### 2.4 The mating regime law (single cast, clean structure)

**Statement.** Sexual recombination (cross-iteration) wins exactly when
the hand is demanding; cheap asexual mutation wins when the hand is
loose. The bar matters precisely when the sea is hard.

**Evidence.** [W1 VERDICT.md](W1-mating-at-scale/VERDICT.md): 10,000
pairs, pre-registered kill gate passed (4.32% real offspring vs 0%
asexual at tol 0.05). The tolerance sweep gives the regime structure:
tol 0.02 → sexual 1.65% vs 0%; tol 0.20 → asexual 25.3% vs 13.8%. One
cast, but monotone and falsifiable across the whole axis. Material
footnote: CPU beat GPU 2.2× at this scale — know your materials.

**Breaks if:** the crossover point moves or vanishes at other
dimensions/scales, or metal (.qm) implementation disagrees.

### 2.5 The herd calm-water law (single cast, host simulation)

**Statement.** A majority-vote herd of cheap identical cells beats the
best single cell at low-to-moderate noise, and repairs independent copy
errors for free at zero channel noise. At high noise everything
collapses toward chance — the herd has nothing left to vote with.

**Evidence.** [W4 RESULTS.md](W4-espnow-herd/RESULTS.md): 55 points
(11 noise × 5 copy-fidelity levels), 2,000 trials each, sealed design
(commit 5c1bc12). Herd 0.816 vs best-single 0.738, CI-separated at
p=0.05 (and at f=0.02); at p=0, f=0.05: herd 1.000 vs mean 0.834 —
majority vote recovers true verdicts from independent copy errors.
The sealed high-noise prediction was wrong and is filed as such (§3).

**Caveats:** host simulation, not metal — the ESP32 run is pending
hardware. Best-single is selected post-hoc (upward bias), making the
comparison conservative.

**Breaks if:** the real-cell run disagrees, or the win vanishes when
cells' errors correlate.

---

## 3. The negatives (first-class results — what they rule out)

The wheel files negatives as results, not embarrassments. Four filings
matter:

### 3.1 W2 — Wesley's first mint: the discrimination bar is real

**Filed:** NEGATIVE-inconclusive, by pre-registered guard.
([W2 VERDICT.md](W2-wesley-first-mint/VERDICT.md))

The mint worked perfectly and it still doesn't count. G1 required the
substrate ≥ 0.60 accuracy; Wesley scored 0.49 — a coin. The registration
said so in advance: *"a mind at chance cannot be distilled."* The kill
gate fired exactly as designed; no rescue attempted.

**What it rules out:** minting a mind that doesn't discriminate. Wesley
is a constant-YES watchman on 3 of 4 categories (GONGO 49 yes / 1 no;
COLD 50 / 0 — accuracy equals the ground YES rate, which is what
answering always-YES scores). The question was never "can bands copy a
mind" — it was "is there a mind to copy," and on 75% of the corpus there
wasn't.

**Error canonization, witnessed.** The mint sealed the constant-YES into
~10 bands — hardening a flaw into scripture, the exact failure mode the
registration pre-named. *A mint is a mirror, not a mind.* Roughly a
third of the seals are canonized bias.

**The exception that validates the mechanics:** SQUALL's cumulonimbus cue
— the one binary signal Wesley actually reads — survived minting and
improved under it (0.80 → 0.88, majority-vote denoising; 92% agreement,
104% accuracy retention, 49,905× speed). Where the mind discriminates,
the mint preserves and improves it. The negative is about the substrate,
not the machinery.

### 3.2 The two guards below the 0.60 bar

The same discrimination bar stopped two turns, at two different points
in the pipeline — the guard design is doing its job:

- **W2 G1 (substrate):** Wesley 0.49 < 0.60 → filed negative, mint
  struck but not counted.
- **W3a G0 (judge):** qwen3:8b scored 0.59 < 0.60 on the 200-item train
  ledger → **stopped before any minting**, per registration.
  ([W3a RESULTS.json](W3a-dissent-fed-mints/RESULTS.json)) *"A mind
  below the bar cannot be distilled; the dissent question stands
  unanswered until a judge clears it."*

**What this rules out so far:** firing the dissent-fed-mint design with
any tested mind. W2's verdict already redesignated W3 ("do not fire as
designed") — feeding back the dissent of a constant is re-canonizing
bias, faster. W3b is the second cast of the judge (§6, pending); its own
registration states the stake plainly: if that judge also fails G0, that
is two judges below the bar and Station 2's premise dies for now —
*also a result*.

### 3.3 W4 — the storm regime: sealed prediction, wrong regime

**Filed:** wrong-regime negative as literally stated, with a clean
positive elsewhere. ([W4 RESULTS.md](W4-espnow-herd/RESULTS.md))

The sealed prediction said the herd beats best-single at HIGH noise. It
doesn't — at p ≥ 0.15 everything collapses toward chance, and at p=0.5
the bit-flip channel carries zero information that no vote can
resurrect. The herd's real edge is calm water (§2.5).

**What it rules out:** "three cheap hands beat one in a storm." Majority
vote buys accuracy only while per-cell errors stay independent and
per-cell accuracy stays meaningfully above 50%. The gain peak is where
there is still signal to vote with.

### 3.4 W1-E2 and W6a — the smaller honest filings

- **W1 E2 (appendix non-reproduction):** the paper's claimed rising
  cross/self-relevance curve (0.000 → 0.234) is 0.0000 at every measured
  step at 10,000 cells with honest random init — presumably a
  tuned-init artifact. Filed negative, kept in canon with the verdict.
  Second confirmed theater element in Paper 219's evidence; the thesis
  survives on E1's honest numbers.
- **W6a (kill gate not reached):** the braid didn't beat copies at ≥2σ
  because the task's ceiling (5/6) was reachable solo — the hand wasn't
  demanding. The regime law (§2.4) explains it post-hoc. The spike's
  real output was an instrument correction: *to measure the braid, the
  hand must fail every solo yard* — which became W6b's design and
  produced the weak-link evidence pair. The wheel correcting its own
  instrument is the sweep working as intended.

---

## 4. The open kernel (what no turn has answered)

Three things survived every cast. They are listed in order of how
sharply they are defined.

### 4.1 The never-held constraints: c2 acrostic + c6 punctuation

Across W6b and W7 — fresh draws, four solo yards, copies, braids in both
orders — **no hand has ever held the acrostic (THEEILEENLAUN) or the
strict-punctuation constraint, in any condition.**
([W7 VERDICT-w7.md](W7-ordered-braid/VERDICT-w7.md), constraint table.)

This is not a ceiling effect: 5/6 is reachable and was reached (W7 ASC,
once). It is a floor-of-capability effect: no ordering can buy what no
hand can hold — W7's own conclusion. Until some yard holds either
constraint, 5/6 is the honest top of this task, and claims about braid
composition above the intersection are unmeasurable on it.

Corollary for the laws: the chamber task's constraint set divides into
three bands — held-by-all (12L, c5), held-by-some (c1, c3, c4), and
held-by-none (c2, c6). The laws in §2 are calibrated on the first two
bands only. The third band has never produced a single data point.

### 4.2 Reviser-mode ≠ solo-mode

W7's first footnote, and the sharpest single observation of the sweep:
kimi holds c3 (seal) and c4 (no-rhyme) solo — yet as DESC hand-2 he
*broke* claude's passing seal, and as ASC hand-3 he *recovered* both
from a broken draft. Same hand, same task, same checker; the draft he
received decided whether he repaired or damaged.

What this means: the solo hold-set bounds what a hand can carry (the
ceiling law is intact — a hand cannot preserve in transit what it
cannot hold cold), but holding solo does not *guarantee* preserving as
a reviser. "Weak-link" is about the ceiling, not a promise of repair.
One hand, one observation, n=1 — unmeasured.

### 4.3 Dissent-feeding: the question W3 was born to ask, still unanswered

Does boundary evidence re-teach the bulk? The design (feed the frozen
bands' disagreements back as labeled dissents, re-strike the mint:
improve, degrade, or nothing?) has never executed:

- W2's substrate failed the guard → W3 redesignated before firing.
- W3a's judge failed G0 by 0.01 → stopped before minting.
- W3b is the second cast, in flight (§6).

The registration's own stake: two judges below the bar kills Station
2's premise for now. Either way the guard fired before the question was
contaminated — which is the wheel working, but the question is now
three turns old and still virgin.

---

## 5. What W8+ should ask (sketched, not sealed)

Sketches only. Nothing below is registered; each needs its own
pre-registration before it runs. Ordered by how directly the sweep
pointed at them.

**5.1 Re-open the W5 arithmetic with W7's chains.** The sealed
consolidation (12/13) covers W6a+W6b — both weak-hands-last chains.
W7 supplied exactly the contrast the W5 lane said it wanted: ASC 5/6 /
DESC 2/6 at an identical solo vector. The open question is regime
structure: is intersection-of-all the descending-chain law, with
last-hand (or a compose/union law — "order lets fixes stick") governing
ascending chains? W7-ASC held c1/c3/c4 that its weak early hands cannot
hold solo, which intersection-of-all forbids. Pre-register the same
≥80% rule over W6a+W6b+W7's three chains (13+6+6 constraint outcomes),
re-run, file whichever way it lands.

**5.2 Break the kernel, or build a yard that can.** c2_acrostic and
c6_punctuation have zero holds in any condition. Two honest paths:
(a) a yard that holds them cold (bigger mind, or a scaffold that puts
the constraint in-context without showing the checker) — after which
the braid laws become measurable above the intersection; or (b) accept
the three-band structure and design W8's hand so every constraint sits
in the held-by-some band, where the laws have signal.

**5.3 The reviser-mode experiment.** One hand, two drafts, n=1. Cast:
same yard as solo vs as reviser on passing vs broken drafts, per-round
checks, enough rounds to count. Question: is repair-vs-damage decided
by the received draft (W7's reading), and is solo hold-set the ceiling
in both modes?

**5.4 W3c (if W3b's judge clears G0):** the original dissent-feeding
design finally fires — frozen bands, labeled dissents fed back, mint
re-struck: improve / degrade / nothing. If W3b also fails G0: Station
2's premise is dead at this scale; the honest next move is a bigger
judge or a simpler corpus, registered as a new cast, not a rescue.

**5.5 Metal, twice over.** W1's disposition already queues Station 3:
the regime law's tolerance bands as a .qm table — the selector judging
offspring in nanoseconds, tight/loose as two sealable band-sets. W4's
herd wants the real ESP32s at the *calm-water* regime the sim found
(p≈0.05, and the copy-error-repair cell at p=0) — not the storm regime
it was originally sealed for. Cross-resolution check is the gate:
metal must agree with its parents.

**5.6 Copies-decompose, formalized.** W5 left this open on purpose:
hold-set under self-revision has never been measured. Cast:
self-revision chains with per-round mechanical checks, per-constraint
— is H_self strictly shrinking, and at what rate per round? Until
then it stays case law, twice-confirmed but unformalized.

---

## 6. W3b — second-cast judge (PENDING — placeholder)

> **Status: IN FLIGHT, run by a separate lane. Not evaluated here.
> This section is a placeholder to be filled by that lane's verdict.**
>
> Registered and sealed before running
> ([REGISTRATION.md](W3b-dissent-fed-mints/REGISTRATION.md), commit
> 21546c6): same corpus verbatim (byte-identical to W3a's, seed
> 20260827), same 200/100 split, same G0 bar 0.60, same mint/dissent
> design; only the judge changes — deepseek-r1:8b, num_ctx 4096,
> num_predict 2048, reasoner parse (strip `<think>`, take the LAST
> yes/no). If the judge clears G0, the dissent-feeding question (§4.3)
> gets its first real test. If not: two judges below the bar — Station
> 2's premise dies for now, also a result, filed honestly.

---

## Coda

Seven turns, ~32 hours, one bench script per turn. The wheel's law held
under its own weight: nothing skipped stations, every prediction was
sealed before its run, and the two times the structure was wrong
(W4's regime, W6a's easy hand) it was the structure that caught it.
The doctrine stands as filed: **verdicts are first-class, negatives are
first-class, and the arithmetic is sealed before it runs.**

*Synthesis written 2026-08-27 by the WHEEL-SYNTH lane. Sources: all
REGISTRATION/VERDICT/RESULTS files in this repo, git log (commits
100ecbf → f578593), and the EXPERIMENT-WHEEL.md design doc (canon
copy). No station files were modified.*
