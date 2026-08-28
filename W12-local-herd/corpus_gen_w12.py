#!/usr/bin/env python3
"""W12 corpus — W3a generator logic VERBATIM (registration binding), NEW seed
2026082712, 60 items (15/cat) selected to exact global 30 YES / 30 NO.
W9 doctrine: exhibit a concrete YES and NO construction per category,
evaluated by the same gt expressions, and verify both labels appear in
every realized category."""
import json
import numpy as np

SEED = 2026082712
rng = np.random.default_rng(SEED)
N_PER_CAT = 15
# cat -> (yes_quota, no_quota): 8+8+7+7 YES = 30
QUOTA = {"FOG": (8, 7), "SQUALL": (8, 7), "GONGO": (7, 8), "COLD": (7, 8)}

def r1(x):
    return round(float(x), 1)

def gen_fog():
    near = rng.random() < 0.5
    dep = rng.uniform(1.2, 2.8) if near else rng.uniform(0.3, 6.0)
    dep = r1(dep)
    wind = int(rng.integers(3, 10) if near else rng.integers(1, 15))
    gt = dep <= 2.0 and wind <= 6
    dew_bin = 0 if dep <= 2.0 else (1 if dep <= 4.0 else 2)
    wind_bin = 0 if wind <= 6 else (1 if wind <= 10 else 2)
    prompt = (f"Conditions: dew point depression {dep}°C, wind {wind} kt. "
              "Question: is fog likely within the next few hours?")
    return dict(cat="FOG", gt=bool(gt), feats=dict(dep=dep, wind=wind),
                band=[dew_bin, wind_bin], prompt=prompt)

def gen_squall():
    near = rng.random() < 0.5
    cb = bool(rng.random() < 0.5)
    fall = rng.uniform(0.75, 2.25) if near else rng.uniform(0.0, 3.5)
    fall = r1(fall)
    wind = int(rng.integers(4, 20))
    gt = cb and fall >= 1.5
    cb_bin = 1 if cb else 0
    fall_bin = 0 if fall < 1.5 else (1 if fall < 2.5 else 2)
    cbp = ("cumulonimbus towers visible to the west" if cb
           else "no cumulonimbus visible")
    prompt = (f"Conditions: {cbp}, barometer falling {fall} hPa over the "
              f"last 3 hours, wind {wind} kt. Question: is a dangerous "
              "squall likely within the hour?")
    return dict(cat="SQUALL", gt=bool(gt), feats=dict(cb=cb, fall=fall, wind=wind),
                band=[cb_bin, fall_bin], prompt=prompt)

def gen_gongo():
    near = rng.random() < 0.5
    wind = int(rng.integers(13, 27) if near else rng.integers(8, 29))
    seas = rng.uniform(2.5, 7.5) if near else rng.uniform(1.0, 8.0)
    seas = r1(seas)
    vlen = int(rng.integers(22, 33))
    gt = wind >= 22 or seas >= 6.0 or (wind >= 18 and seas >= 4.0)
    wbin = 0 if wind <= 17 else (1 if wind <= 21 else 2)
    sbin = 0 if seas < 4.0 else (1 if seas < 6.0 else 2)
    prompt = (f"Conditions: sustained wind {wind} kt, seas {seas} ft, your "
              f"vessel is {vlen} ft long. Question: should you postpone "
              "departure?")
    return dict(cat="GONGO", gt=bool(gt), feats=dict(wind=wind, seas=seas, vlen=vlen),
                band=[wbin, sbin], prompt=prompt)

def gen_cold():
    near = rng.random() < 0.5
    water = rng.uniform(1.0, 7.0) if near else rng.uniform(0.5, 12.0)
    water = r1(water)
    suits = bool(rng.random() < 0.5)
    air = r1(water + rng.uniform(-3, 5))
    gt = (water <= 5.0 and not suits) or (water <= 2.0 and suits)
    wbin = 0 if water <= 2.0 else (1 if water <= 5.0 else 2)
    sbin = 1 if suits else 0
    prompt = (f"Conditions: water temperature {water}°C, air temperature "
              f"{air}°C, immersion suits aboard: {'yes' if suits else 'no'}. "
              "Question: if someone falls overboard, is severe hypothermia "
              "within 30 minutes a live risk?")
    return dict(cat="COLD", gt=bool(gt), feats=dict(water=water, air=air, suits=suits),
                band=[wbin, sbin], prompt=prompt)

GENS = {"FOG": gen_fog, "SQUALL": gen_squall, "GONGO": gen_gongo, "COLD": gen_cold}

# ---- selection: stream candidates per cat until quota met (first-k, deterministic) ----
items = []
for cat, gen in GENS.items():
    yq, nq = QUOTA[cat]
    picked_y, picked_n = [], []
    while len(picked_y) < yq or len(picked_n) < nq:
        it = gen()
        if it["gt"] and len(picked_y) < yq:
            picked_y.append(it)
        elif not it["gt"] and len(picked_n) < nq:
            picked_n.append(it)
    items.extend(picked_y + picked_n)

for i, it in enumerate(items):
    it["id"] = i

# ---- W9 satisfiability exhibit: probes run through the SAME gt expressions ----
def fog_gt(dep, wind): return dep <= 2.0 and wind <= 6
def squall_gt(cb, fall): return cb and fall >= 1.5
def gongo_gt(wind, seas): return wind >= 22 or seas >= 6.0 or (wind >= 18 and seas >= 4.0)
def cold_gt(water, suits): return (water <= 5.0 and not suits) or (water <= 2.0 and suits)

SAT = {
    "FOG":   {"YES": dict(dep=1.5, wind=4),  "NO": dict(dep=5.0, wind=12)},
    "SQUALL": {"YES": dict(cb=True, fall=1.8), "NO": dict(cb=False, fall=1.0)},
    "GONGO": {"YES": dict(wind=25, seas=3.0), "NO": dict(wind=10, seas=2.0)},
    "COLD":  {"YES": dict(water=4.0, suits=False), "NO": dict(water=8.0, suits=False)},
}
GT_FN = {"FOG": (fog_gt, ("dep", "wind")),
         "SQUALL": (squall_gt, ("cb", "fall")),
         "GONGO": (gongo_gt, ("wind", "seas")),
         "COLD": (cold_gt, ("water", "suits"))}
sat_ok = True
sat_report = {}
for cat, probes in SAT.items():
    fn, argorder = GT_FN[cat]
    rep = {}
    for label, kw in probes.items():
        args = tuple(kw[a] for a in argorder)
        val = bool(fn(*args))
        rep[label] = dict(probe=kw, gt=val, expect=label == "YES")
        if val != (label == "YES"):
            sat_ok = False
    # realized-corpus check: both labels present in this cat
    lab = sorted({it["gt"] for it in items if it["cat"] == cat})
    rep["realized_labels"] = lab
    if lab != [False, True]:
        sat_ok = False
    sat_report[cat] = rep

bal = {}
for cat in GENS:
    sub = [it for it in items if it["cat"] == cat]
    bal[cat] = dict(n=len(sub), yes=sum(it["gt"] for it in sub),
                    no=sum(not it["gt"] for it in sub))
tot_yes = sum(it["gt"] for it in items)

out = dict(seed=SEED, n_items=len(items), n_per_category=N_PER_CAT,
           global_yes=tot_yes, global_no=len(items) - tot_yes,
           satisfiability_ok=sat_ok, satisfiability=sat_report,
           balance=bal, items=items)
with open("w12-corpus.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps(bal, indent=1))
print(f"total: {len(items)} items, YES {tot_yes} / NO {len(items)-tot_yes}")
print(f"satisfiability_ok = {sat_ok}")
for cat, rep in sat_report.items():
    print(f"  {cat}: YES probe gt={rep['YES']['gt']} NO probe gt={rep['NO']['gt']} realized={rep['realized_labels']}")
if not sat_ok or tot_yes != 30:
    raise SystemExit("SUITABILITY/BALANCE FAILED — do not run")
