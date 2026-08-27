#!/usr/bin/env python3
"""W2 bench — Wesley ledgers, mint bands, held-out test, results.
Implements REGISTRATION.md exactly. Stages checkpoint to disk; rerun skips
completed stages. No stage may touch later stages' data (fence order)."""
import json, re, time, sys, urllib.request
import numpy as np

MODEL = "granite3.1-dense:2b"
URL = "http://127.0.0.1:11434/api/chat"
CATS = ["FOG", "SQUALL", "GONGO", "COLD"]
CAT_ID = {c: i for i, c in enumerate(CATS)}
SYSTEM = ("You are Wesley, the weather watch aboard a small sailing vessel "
          "in Southeast Alaska. You answer strictly one word: YES or NO. "
          "Nothing else.")

def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def ask_wesley(prompt):
    """One attempt -> (answer|None, seconds). Registered protocol."""
    payload = json.dumps({
        "model": MODEL, "stream": False, "keep_alive": "30m",
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "options": {"temperature": 0.3, "num_predict": 8},
    }).encode()
    req = urllib.request.Request(URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        body = json.loads(r.read())
    dt = time.perf_counter() - t0
    m = re.search(r"\b(yes|no)\b", body["message"]["content"], re.I)
    return (m.group(1).lower() if m else None), dt, body["message"]["content"]

def query_item(prompt):
    """Up to 3 attempts (registered). -> (answer|'UNPARSED', secs_of_final, attempts, last_raw)"""
    for attempt in (1, 2, 3):
        ans, dt, raw = ask_wesley(prompt)
        if ans:
            return ans, dt, attempt, raw
    return "UNPARSED", dt, 3, raw

def stage_train(corpus):
    warm = query_item("Conditions: dew point depression 1.5°C, wind 5 kt. "
                      "Question: is fog likely within the next few hours?")
    print(f"warm-up: {warm[0]} in {warm[1]:.2f}s", flush=True)
    recs = []
    for i, it in enumerate([x for x in corpus["items"] if x["split"] == "train"]):
        ans, dt, att, raw = query_item(it["prompt"])
        recs.append(dict(id=it["id"], cat=it["cat"], gt=it["gt"], ans=ans,
                         secs=dt, attempts=att, raw=raw[:80]))
        if (i + 1) % 25 == 0:
            print(f"train {i+1}/200 ... last {dt:.2f}s {ans}", flush=True)
    with open("w2-ledger-train.json", "w") as f:
        json.dump(dict(model=MODEL, temp=0.3, n=len(recs), records=recs), f, indent=1)

def band_key(cat, band):
    """band list -> integer index in [0,9). Registered bin orders."""
    if cat == "FOG":    return band[0] * 3 + band[1]
    if cat == "SQUALL": return band[0] * 3 + band[1]
    if cat == "GONGO":  return band[0] * 3 + band[1]
    if cat == "COLD":   return band[0] * 3 + band[1]

def stage_mint(corpus):
    train = load("w2-ledger-train.json")
    # agreement matrix: per cat x band: n, wesley yes-rate
    stats = {c: {b: dict(n=0, yes=0) for b in range(9)} for c in CATS}
    cat_tot = {c: dict(n=0, yes=0) for c in CATS}
    for r in train["records"]:
        if r["ans"] == "UNPARSED":
            continue
        it = corpus["items"][r["id"]]
        k = band_key(r["cat"], it["band"])
        y = 1 if r["ans"] == "yes" else 0
        stats[r["cat"]][k]["n"] += 1
        stats[r["cat"]][k]["yes"] += y
        cat_tot[r["cat"]]["n"] += 1
        cat_tot[r["cat"]]["yes"] += y
    # fallback = category global majority; tie -> NO
    fallback = {c: (1 if cat_tot[c]["yes"] * 2 > cat_tot[c]["n"] else 0)
                for c in CATS}
    table = np.full((4, 9), -1, dtype=np.int8)   # -1 = unreachable
    sealed = np.zeros((4, 9), dtype=bool)
    matrix = []
    for c in CATS:
        for b in range(9):
            s = stats[c][b]
            if s["n"] == 0:
                label, seal = fallback[c], False
                why = "empty->cat-majority"
            else:
                rate = s["yes"] / s["n"]
                if s["yes"] * 2 == s["n"]:       # tie
                    label, seal = fallback[c], False
                    why = "tie->cat-majority"
                else:
                    label = 1 if rate > 0.5 else 0
                    seal = s["n"] >= 5 and max(rate, 1 - rate) >= 0.9
                    why = "majority" + (" sealed" if seal else "")
            table[CAT_ID[c], b] = label
            sealed[CAT_ID[c], b] = seal
            matrix.append(dict(cat=c, band=b, n=s["n"], wesley_yes_rate=(
                round(s["yes"] / s["n"], 3) if s["n"] else None),
                label=("YES" if label else "NO"), sealed=bool(seal), rule=why))
    mint = dict(frozen_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                table=table.tolist(), sealed=sealed.tolist(),
                matrix=matrix)
    with open("w2-mint.json", "w") as f:
        json.dump(mint, f, indent=1)
    ns = sum(1 for m in matrix if m["sealed"] and m["n"] > 0)
    occupied = sum(1 for m in matrix if m["n"] > 0)
    print(f"mint frozen: {ns}/{occupied} occupied bands sealed", flush=True)

def stage_test(corpus):
    mint = load("w2-mint.json")
    table = np.array(mint["table"], dtype=np.int8)
    test_items = [x for x in corpus["items"] if x["split"] == "test"]
    recs = []
    for i, it in enumerate(test_items):
        ans, dt, att, raw = query_item(it["prompt"])
        recs.append(dict(id=it["id"], cat=it["cat"], gt=it["gt"], ans=ans,
                         secs=dt, attempts=att, band=band_key(it["cat"], it["band"])))
        if (i + 1) % 25 == 0:
            print(f"test {i+1}/100 ... last {dt:.2f}s {ans}", flush=True)
    with open("w2-ledger-test.json", "w") as f:
        json.dump(dict(model=MODEL, temp=0.3, n=len(recs), records=recs), f, indent=1)

def mint_latency(corpus):
    """Registered: cold single vectorized pass over the 100 held-out items."""
    mint = load("w2-mint.json")
    table = np.array(mint["table"], dtype=np.int8)
    test_items = [x for x in corpus["items"] if x["split"] == "test"]
    # raw features as arrays (binning happens inside the timed region)
    cat = np.array([CAT_ID[it["cat"]] for it in test_items])
    raw = [dict(it["feats"]) for it in test_items]
    gt_band = {it["id"]: band_key(it["cat"], it["band"]) for it in test_items}

    def bin_all(raw_feats):
        idx = np.empty(len(raw_feats), dtype=np.int64)
        for j, (rf, c) in enumerate(zip(raw_feats, cat)):
            if c == 0:
                b0 = 0 if rf["dep"] <= 2.0 else (1 if rf["dep"] <= 4.0 else 2)
                b1 = 0 if rf["wind"] <= 6 else (1 if rf["wind"] <= 10 else 2)
            elif c == 1:
                b0 = 1 if rf["cb"] else 0
                b1 = 0 if rf["fall"] < 1.5 else (1 if rf["fall"] < 2.5 else 2)
            elif c == 2:
                b0 = 0 if rf["wind"] <= 17 else (1 if rf["wind"] <= 21 else 2)
                b1 = 0 if rf["seas"] < 4.0 else (1 if rf["seas"] < 6.0 else 2)
            else:
                b0 = 0 if rf["water"] <= 2.0 else (1 if rf["water"] <= 5.0 else 2)
                b1 = 1 if rf["suits"] else 0
            idx[j] = b0 * 3 + b1
        return idx

    t0 = time.perf_counter()
    idx = bin_all(raw)
    labels = table[cat, idx]
    t_vec = time.perf_counter() - t0

    # secondary: single-item median over 1000 reps
    one = raw[3]
    ts = []
    for _ in range(1000):
        t0 = time.perf_counter()
        i1 = bin_all([one])
        lab = table[cat[3], i1[0]]
        ts.append(time.perf_counter() - t0)
    t_single = float(np.median(ts))
    # correctness fence: binning here must reproduce registered band keys
    for it, j in zip(test_items, idx):
        assert int(j) == band_key(it["cat"], it["band"]), f"band mismatch id={it['id']}"
    return (t_vec / len(test_items)) * 1000.0, t_single * 1000.0  # ms/item

def gt_band_key_check(corpus, it):
    return band_key(it["cat"], it["band"])

def stage_results(corpus):
    train = load("w2-ledger-train.json")
    test = load("w2-ledger-test.json")
    mint = load("w2-mint.json")
    table = np.array(mint["table"], dtype=np.int8)

    parsed = [r for r in test["records"] if r["ans"] != "UNPARSED"]
    unparsed = len(test["records"]) - len(parsed)

    def mint_label(r):
        return "yes" if table[CAT_ID[r["cat"]], r["band"]] == 1 else "no"

    w_ok = [r["ans"] == ("yes" if r["gt"] else "no") for r in parsed]
    m_ok = [mint_label(r) == ("yes" if r["gt"] else "no") for r in parsed]
    w_acc, m_acc = float(np.mean(w_ok)), float(np.mean(m_ok))
    agree = [mint_label(r) == r["ans"] for r in parsed]

    dis = [r for r in parsed if mint_label(r) != r["ans"]]
    dis_verdict = dict(n=len(dis), mint_right=0, wesley_right=0, both_wrong=0,
                       by_cat={c: dict(n=0, mint_right=0, wesley_right=0, both_wrong=0)
                               for c in CATS})
    for r in dis:
        gt_yes = r["gt"]
        m_r = mint_label(r) == ("yes" if gt_yes else "no")
        w_r = r["ans"] == ("yes" if gt_yes else "no")
        d = dis_verdict
        if m_r and not w_r: d["mint_right"] += 1
        elif w_r and not m_r: d["wesley_right"] += 1
        else: d["both_wrong"] += 1
        bc = d["by_cat"][r["cat"]]
        bc["n"] += 1
        if m_r and not w_r: bc["mint_right"] += 1
        elif w_r and not m_r: bc["wesley_right"] += 1
        else: bc["both_wrong"] += 1

    wl = np.array([r["secs"] for r in parsed])
    m_lat_vec, m_lat_single = mint_latency(corpus)

    train_parsed = [r for r in train["records"] if r["ans"] != "UNPARSED"]
    train_w_acc = float(np.mean([r["ans"] == ("yes" if r["gt"] else "no")
                                 for r in train_parsed]))

    per_cat = {}
    for c in CATS:
        sub = [r for r in parsed if r["cat"] == c]
        per_cat[c] = dict(
            n=len(sub),
            wesley_acc=float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in sub])) if sub else None,
            mint_acc=float(np.mean([mint_label(r) == ("yes" if r["gt"] else "no") for r in sub])) if sub else None,
            yes_rate=float(np.mean([r["gt"] for r in sub])) if sub else None)

    speedup = float(np.mean(wl) * 1000.0 / m_lat_vec)
    g1 = m_acc >= 0.90 * w_acc and w_acc >= 0.60
    g2 = speedup >= 100.0

    results = dict(
        meta=dict(experiment="W2 — Wesley's first mint", station=2,
                  model=MODEL, temp=0.3, seed=20260826,
                  run_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                  registered="REGISTRATION.md (2026-08-26 22:35 AKDT)"),
        corpus=dict(n=300, split="200/100", balance=corpus["balance"]),
        train=dict(n=len(train["records"]), unparsed=len(train["records"]) - len(train_parsed),
                   wesley_acc_vs_gt=train_w_acc),
        mint=dict(frozen_at=mint["frozen_at"], matrix=mint["matrix"],
                  sealed_fraction=sum(1 for m in mint["matrix"] if m["sealed"] and m["n"] > 0) /
                                  max(1, sum(1 for m in mint["matrix"] if m["n"] > 0))),
        test=dict(n=100, unparsed=unparsed,
                  wesley_acc=w_acc, mint_acc=m_acc,
                  accuracy_ratio=m_acc / w_acc if w_acc else None,
                  agreement_rate=float(np.mean(agree)),
                  per_cat=per_cat,
                  latency_ms=dict(wesley_mean=float(np.mean(wl)) * 1000.0,
                                  wesley_median=float(np.median(wl)) * 1000.0,
                                  mint_vectorized_mean_per_item=m_lat_vec,
                                  mint_single_item_median=m_lat_single),
                  speedup_vectorized=speedup,
                  disagreements=dis_verdict),
        gates=dict(G1_accuracy=bool(g1), G2_speed=bool(g2),
                   verdict="PASS" if (g1 and g2) else "FAIL"))
    with open("RESULTS.json", "w") as f:
        json.dump(results, f, indent=1)
    print(json.dumps({k: results[k] for k in ("test", "gates")}, indent=1)[:2500])

if __name__ == "__main__":
    corpus = load("w2-corpus.json")
    if corpus is None:
        sys.exit("no corpus — run corpus_gen.py first")
    if load("w2-ledger-train.json") is None:
        stage_train(corpus)
    if load("w2-mint.json") is None:
        stage_mint(corpus)
    if load("w2-ledger-test.json") is None:
        stage_test(corpus)
    if load("RESULTS.json") is None:
        stage_results(corpus)
    print("bench complete")
