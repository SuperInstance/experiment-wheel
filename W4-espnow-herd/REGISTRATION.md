# W4 — THE ESP-NOW HERD (registration draft, pre-run)

*Station 3 (metal). Status: DESIGNED, not yet run. Requires Casey to
flash 2+ ESP32s (he flashes; COM14).*

## The question

W6 measured braiding on cloud yards. W4 asks the herd question on
metal: can 3 ESP32 cells running identical reflex-arc firmware, linked
by ESP-NOW (no WiFi, radio-dark except the herd channel), reach BETTER
collective verdicts than any single cell — by simple majority vote on
noisy sensor readings? This is the braid doctrine at the bottom tier:
same opcodes, same laws, cheap hands, MANY of them.

## Design (to seal before flashing)

- 3× ESP32 (any variant on hand), each running the reflex-arc firmware
  with a noise-injected synthetic sensor stream (same seed).
- Each tick: cell broadcasts its verdict; after hearing all peers (or
  timeout), each applies majority vote; verdict = herd vote.
- Host replay verifies: single-cell accuracy vs herd accuracy across
  500+ ticks at 3 noise levels.
- PREDICTION (to seal): herd beats best single cell at high noise;
  at zero noise they tie (nothing to correct).
- KILL: herd ≤ single at high noise = negative filed (three cheap
  hands don't beat one).

## Status

Awaiting hardware window + Casey's flashing hands. Firmware sketch can
be pre-built on host replay first (the quilt-esp32 replay harness
already exists — reuse).

## Addendum A — host simulation (sealed before run, 2026-08-27)

Hardware window unavailable; per the "host replay first" clause above, the
sealed pre-registered run is now a pure local simulation (numpy, no GPU, no
API, no ollama):

- Task: 12-bit binary input, fixed rule (label = parity of a weighted mask
  seeded at 0; rule fixed for all runs). Each trial draws a fresh random
  12-bit input.
- Each of 3 cells holds a noisy copy of the decision rule (copy infidelity:
  probability f that a rule bit is flipped at copy time; sampled once per
  cell per trial-block).
- Channel: ESP-NOW lossy link modeled as per-bit flip probability p on the
  12-bit payload, swept 0 → 0.5 (11 points: 0, .05, ..., .5).
- Second axis: copy infidelity f ∈ {0, .02, .05, .1, .2}.
- Per point: 2000 trials, fixed seed derived from (p, f) for exact repro.
- Metrics: herd majority-vote accuracy vs best-single-cell accuracy vs mean
  single-cell accuracy (with binomial 95% CIs).
- PREDICTION (sealed): herd > best single cell at high channel noise p;
  herd ≈ singles at p = 0.
- KILL GATE: if herd never beats best-single at any noise point beyond CI
  overlap, file negative honestly.

Locked. No edits after results are generated.
