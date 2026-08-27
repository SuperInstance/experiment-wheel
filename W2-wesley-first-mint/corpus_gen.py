#!/usr/bin/env python3
"""W2 corpus generator — 300 weather-watch binary items, seed 20260826.
Implements REGISTRATION.md exactly. No Wesley involved."""
import json
import numpy as np

SEED = 20260826
rng = np.random.default_rng(SEED)
N_PER = 75

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

items = []
for cat, gen in GENS.items():
    for _ in range(N_PER):
        it = gen()
        it["id"] = len(items)
        items.append(it)

# stratified split: shuffle within category, first 50 train / next 25 test
for cat in GENS:
    idx = [i for i, it in enumerate(items) if it["cat"] == cat]
    order = rng.permutation(len(idx))
    for rank, pos in enumerate(order):
        items[idx[pos]]["split"] = "train" if rank < 50 else "test"

bal = {}
for cat in GENS:
    for sp in ("train", "test"):
        sub = [it for it in items if it["cat"] == cat and it["split"] == sp]
        bal[f"{cat}/{sp}"] = dict(n=len(sub), yes=sum(it["gt"] for it in sub))

out = dict(seed=SEED, n_per_category=N_PER, balance=bal, items=items)
with open("w2-corpus.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps(bal, indent=1))
tot_yes = sum(it["gt"] for it in items)
print(f"total: {len(items)} items, YES rate {tot_yes/len(items):.3f}")
print(f"train: {sum(1 for it in items if it['split']=='train')}, "
      f"test: {sum(1 for it in items if it['split']=='test')}")
