#!/usr/bin/env python3
"""W3a bench — upgraded judge, G0 guard, two mint rounds, dissent feed.
Implements REGISTRATION.md exactly. Stages checkpoint to disk; rerun skips
completed stages. Fence order: guard -> M1 -> test1 -> dissent -> L2 -> M2
-> test2 -> results. No stage may touch later stages' data.
2026-08-27 engineering patch (registration/protocol unchanged): transient
ollama failures (HTTP 5xx, connection/timeout) retried with backoff;
unrecoverable items recorded as honest ledger nulls, never silently
skipped (>10% null aborts the run); partial ledgers checkpoint to disk
every 25 items so a crash loses at most 25."""
import json, os, re, time, sys, urllib.request, urllib.error
import numpy as np

MODEL = "deepseek-r1:8b"
URL = "http://127.0.0.1:11434/api/chat"
CATS = ["FOG", "SQUALL", "GONGO", "COLD"]
CAT_ID = {c: i for i, c in enumerate(CATS)}
SYSTEM = ("You are the weather watch aboard a small sailing vessel in "
          "Southeast Alaska. You answer strictly one word: YES or NO. "
          "Nothing else.")
NUM_CTX = 4096   # 6GB RTX 4050; W7 spike may share the GPU — tolerate slowness, never restart ollama
NUM_PREDICT = 2048  # r1 is a reasoner: let the <think> trace finish so the final answer token exists
G0_BAR = 0.60
DISSANT_CAP = 60

# 2026-08-27 resilience patch: ollama served HTTP 500s under load and crashed
# the bench twice mid-train1. Retry transient failures; record infra failures
# as honest nulls (never silent skips); abort if nulls exceed 10% of a ledger.
RETRY_SLEEP_S = [5, 10, 20, 40, 80]   # 5 retries, exponential backoff
NULL_ABORT_FRAC = 0.10                # >10% null items in a ledger -> abort
CKPT_EVERY = 25                       # flush partial ledger every N items

# r1 cannot disable reasoning; no protocol switch. Parse: strip <think> spans, take LAST yes/no.
PROTO = {"mode": "reasoner"}

def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def write_json_atomic(path, doc):
    """Write JSON via temp file + rename so a crash never corrupts a ledger."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(doc, f, indent=1)
    os.replace(tmp, path)

def raw_call(system, user):
    """One HTTP attempt -> (content, secs). r1 reasoner: single fixed protocol."""
    payload = dict(model=MODEL, stream=False, keep_alive="30m",
                   messages=[{"role": "system", "content": system},
                             {"role": "user", "content": user}],
                   options={"temperature": 0.3, "num_predict": NUM_PREDICT,
                            "num_ctx": NUM_CTX})
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=900) as r:
        body = json.loads(r.read())
    return body["message"]["content"], time.perf_counter() - t0

def raw_call_retry(system, user, tag):
    """raw_call + retry/backoff on transient ollama failures (HTTP 5xx,
    connection/timeout/body errors): 5 retries sleeping 5/10/20/40/80s.
    4xx is a real client bug and still raises. Returns (content|None, secs,
    last_error|None); content None = infra failure after all retries."""
    last = None
    for attempt in range(len(RETRY_SLEEP_S) + 1):
        try:
            content, dt = raw_call(system, user)
            return content, dt, None
        except urllib.error.HTTPError as e:
            last = e
            if e.code < 500:
                raise
            why = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, OSError,
                json.JSONDecodeError) as e:
            last = e
            why = type(e).__name__
        if attempt < len(RETRY_SLEEP_S):
            print(f"{tag} call failed ({why}), attempt {attempt + 1}/"
                  f"{len(RETRY_SLEEP_S) + 1} - retrying in {RETRY_SLEEP_S[attempt]}s",
                  flush=True)
            time.sleep(RETRY_SLEEP_S[attempt])
    print(f"{tag} INFRA-FAIL: giving up after {len(RETRY_SLEEP_S) + 1} "
          f"attempts ({last!r})", flush=True)
    return None, 0.0, last

def parse_answer(content):
    """Registered reasoner parse: strip <think>...</think> (and reject a
    truncated unclosed trace), then LAST \b(yes|no)\b in what remains."""
    text = re.sub(r"<think>.*?</think>", " ", content, flags=re.S)
    if "<think>" in text:          # unclosed = truncated trace, no final answer
        return None
    matches = re.findall(r"\b(yes|no)\b", text, re.I)
    return matches[-1].lower() if matches else None

def query_item(prompt, tag):
    """Up to 3 parse attempts -> (answer|'UNPARSED'|None, secs, attempts,
    raw80). None = infra failure after all retries -> honest null record."""
    raw = ""; dt = 0.0
    for attempt in (1, 2, 3):
        content, dt, err = raw_call_retry(SYSTEM, prompt, tag)
        if content is None:
            return None, None, None, None
        raw = content
        ans = parse_answer(content)
        if ans:
            return ans, dt, attempt, content[-80:]
    return "UNPARSED", dt, 3, raw[-80:]

def warmup():
    """Warm-up + reasoner parse sanity check (retried; abort only if ollama
    is unreachable after all retries)."""
    probe = ("Conditions: dew point depression 1.5°C, wind 5 kt. "
             "Question: is fog likely within the next few hours?")
    content, dt, err = raw_call_retry(SYSTEM, probe, "warmup")
    if content is None:
        sys.exit(f"warm-up INFRA-FAIL after all retries: {err!r} - "
                 f"ollama unreachable/unstable, not starting the bench")
    ans = parse_answer(content)
    tail = content[-60:].replace(chr(10), " ")
    return (f"warm-up {dt:.1f}s parse={ans!r} tail={tail!r}" if ans
            else f"warm-up {dt:.1f}s UNPARSED tail={tail!r}")

def band_key(cat, band):
    return band[0] * 3 + band[1]

def run_ledger(corpus, split, prefix, out_path, tag):
    items = [x for x in corpus["items"] if x["split"] == split]
    partial_path = out_path + ".partial"
    recs = []
    prev = load(partial_path)
    if prev is not None and prev.get("records"):
        recs = prev["records"]
        assert len(recs) <= len(items), "partial ledger longer than split"
        for j, r in enumerate(recs):
            assert r["id"] == items[j]["id"], f"partial order mismatch at {j}"
        print(f"{tag} resuming: {len(recs)}/{len(items)} recovered from "
              f"{partial_path}", flush=True)

    def flush_partial():
        write_json_atomic(partial_path, dict(
            model=MODEL, temp=0.3, protocol=PROTO["mode"], prefix=bool(prefix),
            n=len(recs), complete=False, records=recs))

    abort_bar = NULL_ABORT_FRAC * len(items)
    for i in range(len(recs), len(items)):
        it = items[i]
        user = (prefix + it["prompt"]) if prefix else it["prompt"]
        ans, dt, att, raw = query_item(user, f"{tag} item {i+1}")
        recs.append(dict(id=it["id"], cat=it["cat"], gt=it["gt"], ans=ans,
                         secs=dt, attempts=att, band=band_key(it["cat"], it["band"]),
                         raw=raw))
        n_null = sum(1 for r in recs if r["ans"] is None)
        if ans is None:
            print(f"{tag} {i+1}/{len(items)} id={it['id']} INFRA-FAIL recorded "
                  f"as null ({n_null} null so far, abort bar {abort_bar:.0f})",
                  flush=True)
        if (i + 1) % CKPT_EVERY == 0 or i + 1 == len(items):
            flush_partial()
            last_s = f"{dt:.2f}s" if isinstance(dt, (int, float)) else "n/a"
            print(f"{tag} {i+1}/{len(items)} ... last {last_s} {ans} "
                  f"[ckpt: {len(recs)} items, {n_null} null]", flush=True)
        if n_null > abort_bar:
            flush_partial()
            sys.exit(f"ABORT {tag}: {n_null}/{len(items)} infra-null items exceed "
                     f"{int(NULL_ABORT_FRAC * 100)}% of the {len(items)}-item "
                     f"ledger - ollama too unstable; partial ledger kept at "
                     f"{partial_path}")
    n_null = sum(1 for r in recs if r["ans"] is None)
    doc = dict(model=MODEL, temp=0.3, protocol=PROTO["mode"], prefix=bool(prefix),
               n=len(recs), n_null=n_null, records=recs)
    write_json_atomic(out_path, doc)
    try:
        os.remove(partial_path)
    except FileNotFoundError:
        pass
    return doc

def mint_from(ledger_path, out_path):
    ledger = load(ledger_path)
    stats = {c: {b: dict(n=0, yes=0) for b in range(9)} for c in CATS}
    cat_tot = {c: dict(n=0, yes=0) for c in CATS}
    for r in ledger["records"]:
        if r["ans"] not in ("yes", "no"):  # UNPARSED (protocol) or null (infra)
            continue
        y = 1 if r["ans"] == "yes" else 0
        stats[r["cat"]][r["band"]]["n"] += 1
        stats[r["cat"]][r["band"]]["yes"] += y
        cat_tot[r["cat"]]["n"] += 1
        cat_tot[r["cat"]]["yes"] += y
    fallback = {c: (1 if cat_tot[c]["yes"] * 2 > cat_tot[c]["n"] else 0)
                for c in CATS}
    table = np.full((4, 9), -1, dtype=np.int8)
    sealed = np.zeros((4, 9), dtype=bool)
    matrix = []
    for c in CATS:
        for b in range(9):
            s = stats[c][b]
            if s["n"] == 0:
                label, seal, why = fallback[c], False, "empty->cat-majority"
            elif s["yes"] * 2 == s["n"]:
                label, seal, why = fallback[c], False, "tie->cat-majority"
            else:
                rate = s["yes"] / s["n"]
                label = 1 if rate > 0.5 else 0
                seal = s["n"] >= 5 and max(rate, 1 - rate) >= 0.9
                why = "majority" + (" sealed" if seal else "")
            table[CAT_ID[c], b] = label
            sealed[CAT_ID[c], b] = seal
            matrix.append(dict(cat=c, band=b, n=s["n"], judge_yes_rate=(
                round(s["yes"] / s["n"], 3) if s["n"] else None),
                label=("YES" if label else "NO"), sealed=bool(seal), rule=why))
    mint = dict(frozen_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                source_ledger=ledger_path, table=table.tolist(),
                sealed=sealed.tolist(), matrix=matrix)
    with open(out_path, "w") as f:
        json.dump(mint, f, indent=1)
    ns = sum(1 for m in matrix if m["sealed"] and m["n"] > 0)
    occ = sum(1 for m in matrix if m["n"] > 0)
    print(f"{out_path} frozen: {ns}/{occ} occupied bands sealed", flush=True)
    return mint

def mint_latency(mint, corpus):
    table = np.array(mint["table"], dtype=np.int8)
    test_items = [x for x in corpus["items"] if x["split"] == "test"]
    cat = np.array([CAT_ID[it["cat"]] for it in test_items])
    raw = [dict(it["feats"]) for it in test_items]

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
    one = raw[3]
    ts = []
    for _ in range(1000):
        t0 = time.perf_counter()
        i1 = bin_all([one])
        lab = table[cat[3], i1[0]]
        ts.append(time.perf_counter() - t0)
    for it, j in zip(test_items, idx):
        assert int(j) == band_key(it["cat"], it["band"]), f"band mismatch id={it['id']}"
    return (t_vec / len(test_items)) * 1000.0, float(np.median(ts)) * 1000.0

def heldout_eval(test_ledger, mint):
    table = np.array(mint["table"], dtype=np.int8)
    parsed = [r for r in test_ledger["records"] if r["ans"] in ("yes", "no")]
    unp = len(test_ledger["records"]) - len(parsed)
    infra_null = sum(1 for r in test_ledger["records"] if r["ans"] is None)
    def mlab(r):
        return "yes" if table[CAT_ID[r["cat"]], r["band"]] == 1 else "no"
    j_ok = [r["ans"] == ("yes" if r["gt"] else "no") for r in parsed]
    m_ok = [mlab(r) == ("yes" if r["gt"] else "no") for r in parsed]
    agree = [mlab(r) == r["ans"] for r in parsed]
    dis = dict(n=0, mint_right=0, judge_right=0, both_wrong=0,
               by_cat={c: dict(n=0, mint_right=0, judge_right=0, both_wrong=0)
                       for c in CATS})
    for r in parsed:
        if mlab(r) == r["ans"]:
            continue
        m_r = mlab(r) == ("yes" if r["gt"] else "no")
        j_r = r["ans"] == ("yes" if r["gt"] else "no")
        d = dis; d["n"] += 1
        bc = dis["by_cat"][r["cat"]]; bc["n"] += 1
        if m_r and not j_r: d["mint_right"] += 1; bc["mint_right"] += 1
        elif j_r and not m_r: d["judge_right"] += 1; bc["judge_right"] += 1
        else: d["both_wrong"] += 1; bc["both_wrong"] += 1
    per_cat = {}
    for c in CATS:
        sub = [r for r in parsed if r["cat"] == c]
        per_cat[c] = dict(
            n=len(sub),
            judge_acc=float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in sub])) if sub else None,
            mint_acc=float(np.mean([mlab(r) == ("yes" if r["gt"] else "no") for r in sub])) if sub else None,
            yes_rate=float(np.mean([r["gt"] for r in sub])) if sub else None)
    lat = np.array([r["secs"] for r in parsed])
    return dict(n=len(test_ledger["records"]), unparsed=unp, infra_null=infra_null,
                judge_acc=float(np.mean(j_ok)), mint_acc=float(np.mean(m_ok)),
                accuracy_ratio=float(np.mean(m_ok) / np.mean(j_ok)) if np.mean(j_ok) else None,
                agreement_rate=float(np.mean(agree)),
                per_cat=per_cat,
                latency_ms=dict(judge_mean=float(np.mean(lat)) * 1000.0,
                                judge_median=float(np.median(lat)) * 1000.0),
                disagreements=dis)

def stage_results(corpus):
    t1 = load("w3b-ledger-train1.json"); s1 = load("w3b-ledger-test1.json")
    m1 = load("w3b-mint1.json")
    t2 = load("w3b-ledger-train2.json"); s2 = load("w3b-ledger-test2.json")
    m2 = load("w3b-mint2.json"); dis = load("w3b-dissent.json")

    tp1 = [r for r in t1["records"] if r["ans"] in ("yes", "no")]
    g0 = float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in tp1]))
    tp2 = [r for r in t2["records"] if r["ans"] in ("yes", "no")]
    l2_acc = float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in tp2]))
    tab1 = np.array(m1["table"], dtype=np.int8)
    l2_agree_m1 = float(np.mean([
        ("yes" if tab1[CAT_ID[r["cat"]], r["band"]] == 1 else "no") == r["ans"]
        for r in tp2]))

    r1 = heldout_eval(s1, m1)
    r2 = heldout_eval(s2, m2)
    m1_vec, m1_single = mint_latency(m1, corpus)
    m2_vec, _ = mint_latency(m2, corpus)
    r1["latency_ms"]["mint_vectorized_mean_per_item"] = m1_vec
    r1["latency_ms"]["mint_single_item_median"] = m1_single
    r2["latency_ms"]["mint_vectorized_mean_per_item"] = m2_vec
    r1["speedup"] = r1["latency_ms"]["judge_mean"] / m1_vec
    r2["speedup_prefix"] = r2["latency_ms"]["judge_mean"] / m2_vec

    # sealed-band error rate vs ground truth on train (canonization meter)
    def sealed_err(mint, ledger):
        out = {}
        for c in CATS:
            tot = err = 0
            for r in ledger["records"]:
                if r["cat"] != c or r["ans"] not in ("yes", "no"):
                    continue
                ci, b = CAT_ID[c], r["band"]
                if mint["sealed"][ci][b]:
                    tot += 1
                    lab = "yes" if mint["table"][ci][b] == 1 else "no"
                    if lab != ("yes" if r["gt"] else "no"):
                        err += 1
            out[c] = dict(n=err and tot or tot, err=err,
                          rate=round(err / tot, 3) if tot else None)
        return out

    dM = r2["mint_acc"] - r1["mint_acc"]
    dJ = r2["judge_acc"] - r1["judge_acc"]
    delta_class = ("IMPROVE" if dM >= 0.03 else
                   "DEGRADE" if dM <= -0.03 else "NULL")
    g1 = r1["mint_acc"] >= 0.90 * r1["judge_acc"] and g0 >= G0_BAR
    g2 = r1["speedup"] >= 100.0

    results = dict(
        meta=dict(experiment="W3b — the upgraded judge, second cast: dissent-fed mints (deepseek-r1:8b)",
                  station=2, model=MODEL, temp=0.3, seed=20260827,
                  protocol=t1["protocol"],
                  run_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                  registered="REGISTRATION.md (2026-08-27, sealed before run)",
                  replaces="W3a (G0 negative 0.59) — second cast, judge deepseek-r1:8b",
                  patch="2026-08-27 engineering fix: ollama retry/backoff (5 retries, "
                        "5-80s), infra-nulls recorded honestly (>10% aborts), "
                        "partial-ledger checkpoints every 25 items; protocol unchanged"),
        corpus=dict(n=300, split="200/100", balance=corpus["balance"]),
        guard=dict(G0_train_judge_acc=g0, bar=G0_BAR, passed=bool(g0 >= G0_BAR)),
        round1=dict(train=dict(n=len(t1["records"]),
                               unparsed=len(t1["records"]) - len(tp1),
                               infra_null=t1.get("n_null", 0)),
                    mint1=dict(frozen_at=m1["frozen_at"], matrix=m1["matrix"],
                               sealed_fraction=sum(1 for m in m1["matrix"] if m["sealed"] and m["n"] > 0) /
                               max(1, sum(1 for m in m1["matrix"] if m["n"] > 0))),
                    heldout=r1),
        dissent=dict(n_full=dis["n_full"], n_fed=dis["n_fed"], capped=dis["n_full"] > dis["n_fed"],
                     yes_labels=dis["yes_labels"], no_labels=dis["no_labels"]),
        round2=dict(train=dict(n=len(t2["records"]),
                               unparsed=len(t2["records"]) - len(tp2),
                               infra_null=t2.get("n_null", 0),
                               acc_vs_gt=l2_acc, agreement_with_M1_labels=l2_agree_m1),
                    mint2=dict(frozen_at=m2["frozen_at"], matrix=m2["matrix"],
                               sealed_fraction=sum(1 for m in m2["matrix"] if m["sealed"] and m["n"] > 0) /
                               max(1, sum(1 for m in m2["matrix"] if m["n"] > 0))),
                    heldout=r2),
        deltas=dict(dM=round(dM, 4), dJ=round(dJ, 4), class_=delta_class,
                    binomial_sigma_note="n=100, sigma~0.04; coarse"),
        canonization=dict(sealed_err_M1=sealed_err(m1, t1),
                          sealed_err_M2=sealed_err(m2, t2)),
        gates=dict(G0=bool(g0 >= G0_BAR), G1_accuracy=bool(g1), G2_speed=bool(g2),
                   verdict="PASS" if (g0 >= G0_BAR and g1 and g2) else "FAIL"))
    with open("RESULTS.json", "w") as f:
        json.dump(results, f, indent=1)
    print(json.dumps(dict(guard=results["guard"], gates=results["gates"],
                          r1=dict(judge=r1["judge_acc"], mint=r1["mint_acc"],
                                  speedup=r1["speedup"]),
                          r2=dict(judge=r2["judge_acc"], mint=r2["mint_acc"]),
                          deltas=results["deltas"]), indent=1))

def file_negative_guard(corpus, t1):
    tp = [r for r in t1["records"] if r["ans"] in ("yes", "no")]
    acc = float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in tp]))
    res = dict(
        meta=dict(experiment="W3b — the upgraded judge, second cast: dissent-fed mints (deepseek-r1:8b)",
                  station=2, model=MODEL, temp=0.3, seed=20260827,
                  protocol=t1["protocol"],
                  run_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                  registered="REGISTRATION.md (2026-08-27, sealed before run)"),
        corpus=dict(n=300, split="200/100", balance=corpus["balance"]),
        guard=dict(G0_train_judge_acc=acc, bar=G0_BAR, passed=False),
        filing="NEGATIVE-INCONCLUSIVE — G0 guard failed; stopped before minting per registration")
    with open("RESULTS.json", "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res["guard"], indent=1))

def main():
    corpus = load("w3b-corpus.json")
    if corpus is None:
        sys.exit("no corpus — w3b-corpus.json must be present (copy of w3a)")
    print("warm-up:", warmup(), flush=True)
    # Stage 0: G0 guard train ledger
    t1 = load("w3b-ledger-train1.json")
    if t1 is None:
        t1 = run_ledger(corpus, "train", None, "w3b-ledger-train1.json", "train1")
    tp = [r for r in t1["records"] if r["ans"] in ("yes", "no")]
    g0 = float(np.mean([r["ans"] == ("yes" if r["gt"] else "no") for r in tp]))
    print(f"G0: judge train acc {g0:.3f} (bar {G0_BAR})", flush=True)
    if g0 < G0_BAR:
        file_negative_guard(corpus, t1)
        print("G0 FAILED — filed negative, stopping")
        return
    # Round 1
    if load("w3b-mint1.json") is None:
        mint_from("w3b-ledger-train1.json", "w3b-mint1.json")
    if load("w3b-ledger-test1.json") is None:
        run_ledger(corpus, "test", None, "w3b-ledger-test1.json", "test1")
    # Dissent set
    dis = load("w3b-dissent.json")
    if dis is None:
        m1 = load("w3b-mint1.json")
        tab1 = np.array(m1["table"], dtype=np.int8)
        rows = []
        for r in t1["records"]:
            if r["ans"] not in ("yes", "no"):
                continue
            bl = "yes" if tab1[CAT_ID[r["cat"]], r["band"]] == 1 else "no"
            if bl != r["ans"]:
                rows.append(dict(id=r["id"], cat=r["cat"], judge=r["ans"], band=bl))
        n_full = len(rows)
        if n_full > DISSANT_CAP:
            rng = np.random.default_rng(20260828)
            keep = set(rng.permutation(n_full)[:DISSANT_CAP].tolist())
            rows = [rows[i] for i in range(n_full) if i in keep]
            rows.sort(key=lambda x: x["id"])
        by_id = {it["id"]: it for it in corpus["items"]}
        lines, ys = [], 0
        for d in rows:
            lab = d["band"].upper(); ys += 1 if lab == "YES" else 0
            lines.append(f"— {by_id[d['id']]['prompt']} → {lab}")
        prefix = ("Standing orders from the ship's log — settled answers:\n"
                  + "\n".join(lines)
                  + "\nNow answer today's question the same way, strictly "
                    "one word: YES or NO.\n\n")
        dis = dict(n_full=n_full, n_fed=len(rows), yes_labels=ys,
                   no_labels=len(rows) - ys, prefix=prefix, dissents=rows)
        with open("w3b-dissent.json", "w") as f:
            json.dump(dis, f, indent=1)
        print(f"dissent set: {n_full} found, {len(rows)} fed "
              f"(YES {ys} / NO {len(rows)-ys})", flush=True)
    # Round 2
    prefix = dis["prefix"]
    if load("w3b-ledger-train2.json") is None:
        run_ledger(corpus, "train", prefix, "w3b-ledger-train2.json", "train2")
    if load("w3b-mint2.json") is None:
        mint_from("w3b-ledger-train2.json", "w3b-mint2.json")
    if load("w3b-ledger-test2.json") is None:
        run_ledger(corpus, "test", prefix, "w3b-ledger-test2.json", "test2")
    stage_results(corpus)
    print("bench complete")

if __name__ == "__main__":
    main()
