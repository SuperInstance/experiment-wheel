#!/usr/bin/env python3
"""W4 — ESP-NOW herd, host simulation per REGISTRATION.md Addendum A.

Bit-flip channel on a 12-bit payload; 3 cells with noisy copies of a fixed
rule; majority vote vs best single cell. Pure numpy, fixed seeds.
"""
import json
import numpy as np

BITS = 12
N_CELLS = 3
TRIALS = 2000
P_SWEEP = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
F_SWEEP = [0.0, 0.02, 0.05, 0.10, 0.20]
SEED_BASE = 20260827

rng_master = np.random.default_rng(SEED_BASE)
TRUE_MASK = (rng_master.integers(0, 2, BITS)).astype(np.uint8)  # fixed rule


def ci95(acc, n):
    se = np.sqrt(max(acc * (1 - acc), 1e-12) / n)
    return acc - 1.96 * se, acc + 1.96 * se


def run_point(p, f, seed):
    rng = np.random.default_rng(seed)
    # per-cell noisy copy of the rule mask (sampled fresh for this block)
    flips = rng.random((N_CELLS, BITS)) < f
    cell_masks = TRUE_MASK[None, :] ^ flips.astype(np.uint8)

    # inputs: each cell sees the SAME input (shared sensor stream), but each
    # link to each cell carries it over its own bit-flip channel. (Cells are
    # spatially separate radios; "best single cell" = oracle-best after the
    # fact over the run block.)
    x = (rng.random((TRIALS, BITS)) < 0.5).astype(np.uint8)

    labels = (x @ TRUE_MASK) & 1  # weighted parity

    # channel flips per cell per bit per trial
    chan = rng.random((TRIALS, N_CELLS, BITS)) < p
    rx = np.broadcast_to(x[:, None, :], (TRIALS, N_CELLS, BITS)) ^ chan

    votes = (np.einsum('tnb,nb->tn', rx, cell_masks) & 1).astype(np.int8)
    correct = (votes == labels[:, None]).astype(np.int8)

    herd = ((votes.sum(axis=1) * 2) > N_CELLS).astype(np.int8)
    herd_acc = float((herd == labels).mean())
    cell_accs = correct.mean(axis=0)
    return {
        "herd_acc": herd_acc,
        "herd_ci95": list(ci95(herd_acc, TRIALS)),
        "cell_accs": [float(a) for a in cell_accs],
        "best_single": float(cell_accs.max()),
        "best_single_ci95": list(ci95(cell_accs.max(), TRIALS)),
        "mean_single": float(cell_accs.mean()),
        "best_single_idx": int(cell_accs.argmax()),
    }


def main():
    results = []
    for f in F_SWEEP:
        for p in P_SWEEP:
            seed = SEED_BASE + int(p * 1000) * 100 + int(f * 1000) * 7
            r = run_point(p, f, seed)
            r.update({"p_channel": p, "f_infidelity": f})
            lo, hi = r["herd_ci95"]; blo, bhi = r["best_single_ci95"]
            separated = (lo > bhi) or (blo > hi)
            r["beats_best_single_CI"] = bool(r["herd_acc"] > r["best_single"] and separated)
            results.append(r)
            print(f"f={f:.2f} p={p:.2f} herd={r['herd_acc']:.4f} "
                  f"best={r['best_single']:.4f} mean={r['mean_single']:.4f} "
                  f"CI-separated-win={r['beats_best_single_CI']}")

    with open("W4-espnow-herd/results.json", "w") as fh:
        json.dump({"true_mask": TRUE_MASK.tolist(), "trials": TRIALS,
                   "n_cells": N_CELLS, "p_sweep": P_SWEEP, "f_sweep": F_SWEEP,
                   "seed_base": SEED_BASE, "results": results}, fh, indent=1)
    # CSV
    with open("W4-espnow-herd/results.csv", "w") as fh:
        fh.write("f_infidelity,p_channel,herd_acc,best_single,mean_single,"
                 "herd_ci_lo,herd_ci_hi,best_ci_lo,best_ci_hi,ci_win\n")
        for r in results:
            fh.write(f"{r['f_infidelity']},{r['p_channel']},{r['herd_acc']:.5f},"
                     f"{r['best_single']:.5f},{r['mean_single']:.5f},"
                     f"{r['herd_ci95'][0]:.5f},{r['herd_ci95'][1]:.5f},"
                     f"{r['best_single_ci95'][0]:.5f},{r['best_single_ci95'][1]:.5f},"
                 f"{int(r['beats_best_single_CI'])}\n")

    wins = [r for r in results if r["beats_best_single_CI"]]
    print(f"\nCI-separated herd-wins: {len(wins)}/{len(results)} points")


if __name__ == "__main__":
    main()
