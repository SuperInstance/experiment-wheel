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
