# W8-queue — THE NEXT STATIONS: design

*Design only. Nothing in this document has been run. Every station below
grows from a NAMED finding already on record — shipwright doctrine, every
piece has a reason. Each station gets its own sealed REGISTRATION.md
before it fires; this doc is the queue's argument for what deserves to
run next and what each run can teach the fleet, whichever way it lands.*

---

## What is already banked (the stock these stations grow from)

One paragraph of case law, all committed, none reinterpreted here:

- **W1 — the regime law:** mating (crossover) wins when the hand is
  demanding (tol 0.02: 1.65% vs 0%); asexual wins loose (tol 0.2:
  25.3% vs 13.8%). Cross-iteration is what hard years are for.
- **W2/W3a/W3b — G0 guards:** a mind below the bar cannot be distilled
  from; guards stop the line before noise gets canonized. W3b is sealed
  under its own protocol and is NOT touched by this queue.
- **W4 — the herd law:** majority vote repairs copy errors free in calm
  water (f=0.05, p=0: herd 1.000 vs mean 0.834; CI-separated win at
  p=0.05), and dies in storms (p≥0.15) — the edge lives where per-cell
  accuracy stays above ~60%.
- **W5 — the intersection law (L1), consolidated 12/13 = 92%:** a braid
  holds ≈ the intersection of its hands' solo hold-sets, zero fitting.
  Two honest misses: last-hand prose falsified at constraint level, and
  destruction is probabilistic (c5 survived two non-holding hands).
- **W6a/W6b — copies-decompose ×2:** self-revision loses constraints
  INSIDE the reviser's own solo hold-set. Unconsolidated as law.
- **W7 — the ordered braid, both prongs:** ascending chain 5/6 vs best
  solo 4/6 — the first condition ever to beat the best single hand;
  descending sank to 2/6 at the identical solo vector (4/4/2/2).
  Weak-Link Law banked bidirectionally. Two footnotes carry the next
  questions: **(1) reviser-mode ≠ solo-mode** (kimi holds seal+rhyme
  solo yet BROKE claude's passing seal as a descending reviser — and
  recovered both as an ascending one); **(2) the never-held kernel**
  (c2 acrostic + c6 punctuation: held by NO yard in ANY condition
  across W6b+W7 — no ceiling effect; 5/6 is the honest top).

And one observation this queue names explicitly because W7's own numbers
force it (worked through in Station W10 below): **the consolidated
intersection law L1, applied to W7's ascending braid, predicted 2/6 and
observed 5/6** — a 3-cell violation (c1, c3, c4 all held above the
intersection of solo hold-sets, which is {12_lines, c5}). L1 survived
W7's DESCENDING arm exactly ({12L, c5} predicted, {12L, c5} observed).
The law as written is a *backward-chain* law. Order bought repair that
intersection forbids. That is not a scandal; that is the next station.

## The queue at a glance

| station | grows from | the question | headline prediction | cap |
|---|---|---|---|---|
| **W8 — the reviser's blind side** | W7 fn.1 + W5 miss 1 | why does a hand break a constraint it holds SOLO when revising? | destruction tracks blind rewriting; verify-then-fix prompts cut it ≥50% at ≤15pt repair cost | ≤60 calls |
| **W9 — the never-held kernel** | W7 fn.2 | are c2/c6 model-class walls or artifacts of one prompt shape? | c6 falls to some shape; c2 stands at 0/≥48 (CI upper ≈6%) | ≤200 calls |
| **W10 — law as helm** | W5 L1 92% + W7's 3-cell violation | can hold-set arithmetic ENGINEER braid outcomes before spending a call? | an order-aware amendment (L4: last-holder + spare) predicts engineered chains at ≥80% cell accuracy | ≤30 calls |
| **W11 — the fused catch** | W4 × W7 × W1 | what does herd aggregation do ACROSS braids, where voting is not bit-level? | checker-guided line fusion gains line-LOCAL constraints (c1/c2), not global ones — locality is the new law candidate | ≤30 calls |

Firing order and dependencies: **W8 first** (its destruction/spare rates
feed W10's arithmetic). W9 is independent (can share an evening with W8).
**W10 after W8** (one evening later is fine). W11 independent — cheapest,
fire whenever. Budgets are hard caps, pre-stated per station below, and
every station inherits the standing guards: single pass, no re-rolls,
results committed as measured, registration sealed before execution, no
model ever sees the checker (fleet-side selectors may, flagged as
instruments — the W1 selector precedent).

---

## Station W8 — THE REVISER'S BLIND SIDE

*Grows from: **W7 footnote 1** (kimi holds seal+rhyme solo, broke
claude's passing seal as DESC hand-2, recovered both as ASC hand-3) and
**W5's first honest miss** (last-hand prose falsified at constraint
level — capability sets bound outcomes but do not determine them).*

### The question (one)

Why does a hand destroy a constraint it demonstrably holds SOLO when it
revises another mind's draft? W7's own framing is the hypothesis to
beat: *"a hand fixes what it notices broken and damages what it rewrites
blind — the draft it receives decides which."* If that is right, the
destruction is not capability loss; it is collateral damage from
unverified rewriting, and prompt shape should be able to reach it.

### The two mechanisms (pre-stated, discriminated by this run)

- **M1 — BLIND-REWRITE:** the reviser verifies what it notices broken
  and rewrites the rest without re-checking. Destruction of a passing
  constraint is collateral of rewriting its carrier lines. Signature:
destruction probability tracks per-line edit distance on the lines that
  carry the constraint, and shrinkable by prompt.
- **M2 — REVISION-MODE SWITCH:** revising is a different behavior than
  composing; in revision mode the hand's effective hold-set shrinks
  regardless of how much it rewrites. Signature: destruction independent
  of edit distance, unaffected by any prompt regime. (A model-class
  wall, not a workflow bug.)

### Hand, task, crew

Task: VERBATIM W6b/W7 chamber task and mechanical check(). Crew: kimi,
claude, flash as revisers (each holds 3–4 constraints solo — the holder
cells); wesley as non-holder control. Seed drafts: a fixed corpus of
known-state drafts at score ≥3/6. W7's results record per-hand checks
but NOT per-hand drafts, so seeds are regenerated at fire time:

- **Seed draw (seed base 20260828):** one solo pass per yard; keep the
  two best drafts; if none reaches 3/6, two more draws per yard max
  (pre-stated cap). Seeds + their check() states COMMITTED before any
  regime arm runs — the W3 G0-guard pattern inherited: the instrument's
  raw material goes on record before the experiment touches it.

### Protocol

Crossed design: reviser {kimi, claude, flash, wesley} × regime {
(i) **baseline** — W7's revision wording verbatim; (ii) **minimal-edit**
— "change as few characters as possible; touch ONLY lines that violate
a constraint"; (iii) **verify-then-fix** — "first list each numbered
constraint with PASS or FAIL for this attempt, then output the corrected
12 lines" (parse last 12 lines, the kimi pattern)}. Single pass per
cell, no re-rolls. Every revision recorded with per-line edit distance
on each constraint's carrier lines (c3: seal line; c2: all; c1: all;
c5: final line; c4: line endings; c6: whole text).

Cells: **holder cells** (reviser holds c solo, c passes in seed — the
W7 kimi event) → destroyed? And **repair cells** (c broken in seed) →
held? Non-holder cells ride along and become W10's p_destroy data.

### PREDICTION (on record before any run)

- **P1 (the gap is real):** baseline holder-cell destruction rate ≥ 15%
  per revision. kimi's W7 kill was not a one-off.
- **P2 (M1 is the mechanism):** (a) per-line edit distance on carrier
  lines predicts destruction (logistic slope ≠ 0, p < 0.05, pooled
  cells); AND (b) verify-then-fix cuts holder-cell destruction ≥ 50%
  relative with Wilson CI separation, at ≤ 15 points absolute loss in
  repair rate.

### Bars, kill gate, falsifiers

- **Kill gate:** no seed draft ≥ 3/6 after the draw cap → STOP, file
  "nothing passing to destroy" — cannot study destruction of passing
  constraints without passing constraints.
- **Falsifier of the phenomenon:** P1 fails (0 holder-cell destructions
  across ≥ 24 baseline holder cells) → the reviser-gap was a W7 one-off;
  the intersection law's clean form strengthens and the fleet stops
  paying for re-verification of held constraints. Filed as a NEGATIVE —
  which would consolidate W5, not embarrass anyone.
- **Falsifier of the mechanism:** P1 holds but P2 fails → the gap is
  real and prompt-irreparable → M2, a revision-mode wall. Doctrine
  shifts to instruments: verification of passing constraints goes to
  the mechanical checker (fleet-side), never trusted to revising minds.

### What the verdict MEANS for the fleet

If M1 lands: reviser prompts on the Waters get verify-then-fix and
minimal-edit mandates for passing lines — the cheapest intervention
this whole queue could buy, two sentences of prompt, measured in one
evening. If M2 lands: hold-sets are solo-mode objects only; revision
chains must be ordered so held constraints are never re-exposed, and
the checker becomes the only trusted re-verifier. Either branch feeds
W10 a measured destruction/spare rate per hand — the number the
intersection law's probabilistic clause has been missing.

Budget cap: ≤ 60 model calls (≤ 8 seed draws + 48 revisions), one
evening.

## Station W9 — THE NEVER-HELD KERNEL

*Grows from: **W7 footnote 2** — c2_acrostic and c6_punctuation held by
NO yard in ANY condition across W6b + W7 (fresh draws, solos, copies,
both braids). No ceiling effect: 5/6 is the honest top, and the two
missing points are always the same two.*

### The question (one)

Are c2 and c6 **model-class walls** — constraints no shape of this crew
can hold — or artifacts of ONE prompt shape (the W6b task string) that a
different crew shape breaks? Across W6b+W7 the attempted shapes are:
solo ×8, copies, two braid orders. Never attempted: high-N ensembles,
scaffolded (worksheet-style) presentation, and constraint-attorney
decomposition. Before the fleet routes these constraints to instruments,
someone owes the minds a fair trial at more than one shape.

### The shapes (each pre-stated; no model sees check() ever)

- **SH-1 — ensemble at N:** 16 independent draws per yard on the VERBATIM
  W6b task (temperature as W6b). Answers the small-N objection first:
  was 0/8 solo a thin draw? Pooled 64 draws per constraint.
- **SH-2 — scaffold:** identical constraint INFORMATION, worksheet
  presentation — "line 1: one word, begins with T; line 2: two words,
  begins with H; …" (12 rows listed explicitly). Externalizes the plan;
  changes presentation, not information. The task text already states
c1 and c2 fully, so this leaks nothing new.
- **SH-3 — attorney decomposition:** three specialized hands in sequence,
  each seeing a REDUCED task: content draft (free 12-line poem) →
  letter-and-count pass ("rewrite each line to begin with the required
  letter and contain the required word count; change nothing else") →
  formatting pass (c6 only: "exactly one comma, one period, no other
  punctuation, capitals only line-initial"). This is the intersection
  law's boundary test: does a hand's hold-set GROW when the task
  shrinks? (L1 was consolidated on same-task chains; decomposition
  changes the per-hand task, which the law never covered.)
- **SH-4 — c6 minimal-fix arm:** take an otherwise ≥3/6 seed draft; the
  hand fixes ONLY punctuation/caps. Isolates formatting discipline from
  everything else.

### Crew

All four yards (claude, kimi, flash, wesley) for SH-1; claude + kimi +
flash for SH-2/SH-3/SH-4 (the 4-point hands; wesley's 2-point ceiling
adds little here — noted, not hidden). Yard availability guard: a yard
that fails its CLI/API check drops out, recorded as such.

### Seeds and bars

Seed base 20260829 (draft draws and ensemble seeds; SH-1 uses
20260829+k per draw). **"Holds" = single pass under the W6b checker,
no re-rolls, ever.** Bars pre-stated:

- **c6 falls** if ANY shape holds it ≥ 1/8 within that shape → c6 is
  promptable; formatting discipline is a workflow problem.
- **c2 stands (wall)** if pooled holds = 0 across ≥ 48 shape-attempts →
  model-class wall at this crew, 95% CI upper ≈ 6.1% (rule of three,
  3/48). If c2 is held by ANY shape → the "never-held kernel" was a
  prompt artifact and the queue's later stations inherit a wider
  design space than they were designed for (W10's engineered chains
can target c2; W11's fusion can vote on it).
- Report BOTH rates always: **mind-only** (draft passes unaided) and
  **fleet-selected** (checker picks the passing draft from N — the W1
  selector precedent; legitimate fleet-side instrument, but a different
  claim and reported as a different number).

### PREDICTION (on record)

Undersold: **c6 falls** (SH-3's formatting pass or SH-4 holds it ≥ 1/8);
**c2 stands** (0/≥48 pooled — the acrostic×growth interlock is a
  planning limit, not a presentation limit; scaffolding re-arranges the
  information but the hand still has to execute a 12-line joint plan).

### Kill gate

≤ 200 model calls total, one evening. If SH-1's 64-draw baseline alone
holds c2 or c6, later shapes still run (rate estimation), but the wall
question is already answered NO at the ensemble shape — record it and
let the budget go to measuring, not re-arguing.

### What the verdict MEANS for the fleet

If c6 falls and c2 stands, the Waters doctrine gains a **wall table**:
constraints split into pliable (minds, with the right shape) and walls
(instruments — the post-processor fixes punctuation the way the
SQUALL watchman holds one cue; c2-class joint planning gets decomposed
or abandoned, never assigned to a single mind cold). If BOTH fall, the
never-held kernel dissolves — every "wall" claim in the doctrine gets
re-audited for prompt-shape artifacts before it's allowed to stand. If
NEITHER falls, the kernel is confirmed as this model class's ceiling
and W10/W11 design around it permanently.

## Station W10 — LAW AS HELM

*Grows from: **W5's consolidation** (L1 intersection-of-all, 12/13 =
92%, zero fitting) — and from a fact W7 put on record that the law
cannot survive unamended: applied to W7's ascending chain, L1 predicted
2/6 and observed 5/6.*

### The arithmetic that forces this station

W7's measured solo hold-sets: claude {12L, c1, c3, c5} · kimi {12L,
c3, c4, c5} · flash {12L, c5} · wesley {12L, c5}. Intersection of all
four = **{12L, c5}**. L1 (all-touch relevance at 85–94% novelty) says
any four-hand braid holds exactly that: **2/6**. Observed: ASC 5/6 —
c1, c3, c4 ALL held above the intersection (claude closed c1 at last
position; kimi recovered c3+c4 at hand-3; claude, a non-holder of c4,
SPARED kimi's c4). DESC 2/6 — the exact intersection set, L1's home
turf, reproduced to the cell.

So the consolidated law is a **backward-chain law**: it binds when
weak hands finish the draft. Ascending order buys REPAIR above the
intersection — destruction is capped by order, repair is granted by
order. That is not a refutation of W5; it is the amendment W5's own
probabilistic clause ("destruction with high but not perfect
probability") was reaching for. The candidate statute, pre-stated
here as **L4 — the LAST-HOLDER-SPARE law**:

> A braid holds c ⟺ some hand in the chain holds c solo AND every
> hand AFTER the last holder spares c (each non-holder destroys w.p.
> p_destroy(h,c), measured not assumed).

L4 reduces to L1 on backward chains (last holders are early, the tail
of non-holders destroys), and to the last-hand law when the final hand
holds c. It adds one thing neither had: **a spare-rate for strong
non-holders** — claude spared c4 he cannot hold solo; flash and wesley
(weak non-holders) destroyed c3 twice in W6b. Destruction heterogeneity
by hand strength is the load-bearing new claim.

### The question (one)

Can hold-set arithmetic + L4 ENGINEER braid outcomes — chains picked so
the predicted survivor sets differ, predictions sealed before any chain
runs? The law stops being a description of what happened and becomes a
tool for what will. W7 compared two orders; W10 compares two LAWS on
chains built to make them disagree.

### Protocol

- **Phase 0 (seed 20260830):** fresh draw, solo hold-sets for all four
  yards — 4 calls, committed as measured, whatever the vector is.
- **Phase 1 (sealed before any chain runs):** from the measured
  hold-sets, pick and commit three chains with predictions per cell:
  - **CH-A — repair-max:** ascending by measured solo score. L1 predicts
    the intersection only; L4 predicts intersection ∪ last-hand's
    hold-set ∪ {c recovered by hand n−1 and spared by hand n}. The laws
    disagree on CH-A by construction; the run arbitrates.
  - **CH-B — spare-test:** a STRONG non-holder of a split-ownership
    constraint placed LAST (e.g., if the draw reproduces a
    claude-without-c4 shape: …→kimi→claude). L1 says that cell dies;
    L4 says it survives at claude's spare-rate. The cleanest single
    arbitration cell this theater can build.
  - **CH-C — deterministic descent:** descending order, weak hands last.
    BOTH laws predict the exact intersection floor. This is the
    reproduction control — if CH-C misses, the instrument is broken,
    not the law.
- **Scoring:** constraint-cell accuracy pooled across chains, L1 vs L4,
  with p_destroy from W8's measured rates where available; flat W5
  prior (destruction high but imperfect, one observed survival in 13
  non-holder exposures) if W8 has not fired. Same task, same checker,
single pass, no re-rolls.

### PREDICTION (on record)

**L4 ≥ 80% pooled cell accuracy** (W5's own bar) **and CH-C exact.**
Implicitly: L1 scores CH-A wrong again (it must — the intersection
cannot exceed 2 cells on any realistic draw) and loses the pooled
comparison; L4's spare-rate cells (CH-A's recovered-then-spared, CH-B's
strong-sparer) are where the ≥80% is won or lost.

### Bars, kill gate, falsifiers

- **Kill gate:** phase 0 must yield ≥ 3 distinct hold-sets AND ≥ 1
  split-ownership constraint (some yards hold it, some don't) — else
  there is nothing to engineer with. ONE redraw allowed (seed
  20260830 + 1000, pre-stated), then STOP, filed underpowered.
- **Falsifier:** L4 < 80% pooled, or CH-C fails to reproduce the
  intersection floor → the arithmetic-crew-design program STOPS. The
  law bank keeps ascending-order as an empirical heuristic and the
doctrine honestly downgrades to: *measure the chain, don't predict it.*
- **Honest asymmetry:** a CH-B survival could be luck (one cell, one
  pass). It is scored as a cell, not a law; only the pooled bar
  carries a verdict. This station undersells on purpose.

### What the verdict MEANS for the fleet

If L4 holds: crew design becomes **hold-set tables + arithmetic** — the
manifest computes the chain before the fleet spends a single call on
it; "ascending order" graduates from heuristic to computed optimum,
and W8's per-hand destruction rates become standing fleet data. If L4
fails: ordering doctrine stays empirical, and the honest doctrine is
that braid outcomes are cheaper to measure than to predict — which is
itself a sentence worth having proven.

Budget cap: ≤ 30 calls (4 phase-0 + 16 chain hands + redraw allowance).
Fires AFTER W8 (spare-rate data) but does not require it.

## Station W11 — THE FUSED CATCH (stub)

Grows from W4 (herd) × W7 (braid) × W1 (mating). K independent ascending
braids, then mechanical aggregation: best-of-K selection and checker-guided
line-inheritance fusion (uniform crossover at the artifact level).
Locality law candidate: the herd can vote on what is local; global
constraints need one mind. [Filled in below.]

## What this queue deliberately does NOT run

See the final section — deferred items (copies-decompose formalization,
the W3 mint lane, Station 3's qm tables) with reasons. W3b is sealed
under its own registration and untouched by everything here.
