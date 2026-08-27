# W4 RESULTS — ESP-NOW herd (host simulation)

*Run 2026-08-27, per REGISTRATION.md Addendum A (sealed in commit 5c1bc12,
before any results were generated). 55 points = 11 channel noise levels × 5
copy-fidelity levels, 2000 trials each, fixed seeds (base 20260827).
Script: `w4_herd_sim.py`. Data: `results.json` / `results.csv`.*

## Verdict vs pre-registered prediction

**PREDICTION (sealed): herd > best single cell at HIGH noise; tie at p=0.**

**RESULT: NEGATIVE as literally stated — with a real, clean positive in the
low-to-moderate noise regime.**

- At p=0.05 (perfect copies, f=0): herd 0.816 vs best single 0.738
  (95% CIs separated: [0.798, 0.834] vs [0.718, 0.757]). Herd also wins
  CI-separated at f=0.02, p=0.05 (0.812 vs 0.731). **2/55 CI-separated
  herd wins over best-single, both at p=0.05.**
- At high channel noise (p ≥ 0.15) everything collapses toward chance and
  herd never CI-separates above best-single. At p = 0.5 the bit-flip channel
  carries zero information; majority vote cannot resurrect it.
- Herd > mean single at 35/55 points; the herd's edge concentrates where
  per-cell accuracy is still above ~60%.
- Copy infidelity (f axis) degrades the herd faster than singles: at f=0.05,
  p=0, herd = 1.000 while mean single = 0.834 — majority vote REPAIRS copy
  errors for free at zero channel noise (cells' copy errors are independent,
  so 2-of-3 agreement recovers the true rule verdict). At f ≥ 0.10 combined
  with p ≥ 0.10, everything is at chance.

## Mechanism read

Majority vote buys accuracy only while the per-cell error events stay
independent and per-cell accuracy stays meaningfully above 50%. The gain
peak is at low noise (p≈0.05), not high noise — the sealed prediction had
the regime wrong. "High noise" is where the herd has nothing left to vote
with. Also note: best-single is selected post-hoc as max of 3 cells per
block (upward selection bias), making this a conservative comparison — and
the herd still clears it at p=0.05.

## Numbers that matter

| f | p | herd | best | mean |
|---|---|------|------|------|
| 0.00 | 0.00 | 1.000 | 1.000 | 1.000 |
| 0.00 | 0.05 | **0.816** | 0.738 | 0.722 |
| 0.00 | 0.10 | 0.634 | 0.603 | 0.586 |
| 0.00 | 0.15 | 0.551 | 0.546 | 0.533 |
| 0.05 | 0.00 | **1.000** | 1.000 | 0.834 |
| 0.05 | 0.05 | 0.605 | 0.702 | 0.568 |

Kill gate check: herd DOES beat best-single beyond CI overlap at some noise
points (p=0.05), so the kill gate is not triggered; but the sealed
"high-noise" prediction is honestly filed as wrong-regime.
