#!/usr/bin/env python3
"""W5 case-law math: predict braid constraint survival from solo hold-sets.
No fitting. Laws pre-stated in REGISTRATION-sealed-amendment.md (commit 1d51ed5).
Reads W6a/W6b results from git record (w6-results.json, w6b-results.json).
"""
import json

ROOT = "/home/eileen/projects/experiment-wheel"
W6A = json.load(open(f"{ROOT}/W6-the-braid/w6-results.json"))["modes"]
W6B = json.load(open(f"{ROOT}/W6-the-braid/w6b-results.json"))

def hold(check):  # hold-set = set of constraints with True, excluding 'score'
    return {k for k, v in check.items() if k != "score" and v is True}

# ---- W6a: chain kimi -> claude -> flash -> wesley ----
a_solo = {y: hold(W6A["solo"][y]["check"]) for y in ["kimi", "claude", "flash", "wesley"]}
a_chain = ["kimi", "claude", "flash", "wesley"]
a_observed = hold(W6A["braid"]["wesley"]["check"])  # final hand's output
a_C = set(W6A["solo"]["claude"]["check"]) - {"score"}

# ---- W6b: chain kimi -> claude -> flash -> wesley -> flash ----
b_solo = {y: hold(W6B["solo"][y]["check"]) for y in ["kimi", "claude", "flash", "wesley"]}
b_chain = ["kimi", "claude", "flash", "wesley", "flash"]
b_observed = hold(W6B["braid"]["check"])
b_C = set(W6B["solo"]["claude"]["check"]) - {"score"}

def L1(solo, chain):  # intersection of ALL hands' hold-sets
    s = None
    for y in chain:
        s = solo[y] if s is None else s & solo[y]
    return s

def L2(solo, chain):  # last hand only
    return solo[chain[-1]]

def L3(solo, chain):  # last two hands
    return solo[chain[-1]] & solo[chain[-2]]

LAWS = {"L1_intersection_all": L1, "L2_last_hand": L2, "L3_last_two": L3}

rows, totals = [], {n: [0, 0, 0, 0] for n in LAWS}  # per-law [a_hit, a_n, b_hit, b_n]
for name, exp, solo, chain, obs, C in [
    ("W6a", "W6a", a_solo, a_chain, a_observed, a_C),
    ("W6b", "W6b", b_solo, b_chain, b_observed, b_C),
]:
    print(f"\n=== {exp} ===")
    print("solo hold-sets:")
    for y, h in solo.items():
        print(f"  {y:7s} holds: {sorted(h)}")
    print(f"chain: {' -> '.join(chain)}")
    print(f"observed braid held: {sorted(obs)}")
    preds = {n: f(solo, chain) for n, f in LAWS.items()}
    print(f"{'constraint':22s} {'obs':4s} " + " ".join(f"{n[:12]:>13s}" for n in LAWS))
    for c in sorted(C):
        line = f"{c:22s} {'HELD' if c in obs else 'lost':4s} "
        for n in LAWS:
            p = c in preds[n]
            hit = p == (c in obs)
            totals[n][0 if exp == "W6a" else 2] += hit
            totals[n][1 if exp == "W6a" else 3] += 1
            line += f"{'HELD' if p else 'lost':>7s}{'+ ' if hit else 'MISS':>6s}"
        print(line)

print("\n=== POOLED VERDICT (bar: >=80% consolidation; 60-79% descriptive; <60% falsified) ===")
for n in LAWS:
    a, b = totals[n][0], totals[n][2]
    pooled = (a + b) / 13
    print(f"{n:22s} W6a {a}/6  W6b {b}/7  pooled {a+b}/13 = {pooled:.0%}  -> "
          + ("CONSOLIDATION" if pooled >= .8 else "DESCRIPTIVE" if pooled >= .6 else "FALSIFIED"))

# ---- bonus context: copies-decompose (not a braid law; separate check) ----
print("\n=== copies check (context, not scored) ===")
print("W6a flash x4 rounds held:", sorted(hold(W6A["copies"]["flash_4rounds"]["check"])),
      "| flash solo held:", sorted(a_solo["flash"]))
print("W6b flash x4 rounds held:", sorted(hold(W6B["copies"]["check"])),
      "| flash solo held:", sorted(b_solo["flash"]))
