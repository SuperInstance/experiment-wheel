#!/usr/bin/env python3
"""W12 solo pass runner. Serial GPU discipline: one mind at a time,
weakest->strongest. Checkpoint ledger every 10 items, resume from partial.
Parse: LAST \\b(yes|no)\\b case-insensitive; up to 3 attempts; else UNPARSED.
Infra retry 5x backoff (W3b pattern); unrecoverable -> null."""
import json, os, sys, time, urllib.request, urllib.error, re

BASE = "http://127.0.0.1:11434"
SYS = ("You are the weather watch aboard a small sailing vessel in Southeast "
       "Alaska. You answer strictly one word: YES or NO. Nothing else.")
MINDS = [  # weakest -> strongest by params
    ("qwen0.5b", "qwen2.5:0.5b"),
    ("lfm2.6",   "Liquid-LFM2.5-2.6B:latest"),
    ("qwen3b",   "qwen2.5:3b"),
    ("phi3",     "phi3:3.8b"),
    ("mistral7b","mistral:7b"),
]
PAT = re.compile(r"\b(yes|no)\b", re.I)

def raw_call(model, prompt, keep_alive):
    body = json.dumps({
        "model": model, "stream": False,
        "messages": [
            {"role": "system", "content": SYS},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0.3, "num_ctx": 2048, "num_predict": 8},
        "keep_alive": keep_alive,
    }).encode()
    req = urllib.request.Request(BASE + "/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())

def raw_call_retry(model, prompt, keep_alive):
    delays = [5, 10, 20, 40, 80]
    last = None
    for attempt in range(6):
        try:
            return raw_call(model, prompt, keep_alive)
        except Exception as e:
            last = e
            if attempt < 5:
                time.sleep(delays[attempt])
    raise last

def unload(model):
    body = json.dumps({"model": model, "keep_alive": 0}).encode()
    req = urllib.request.Request(BASE + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            r.read()
    except Exception:
        pass

def parse_answer(text):
    if not text:
        return None
    ms = PAT.findall(text)
    if not ms:
        return None
    return ms[-1].upper() == "YES"

def run_mind(name, model, items):
    ledger_path = f"w12-solo-{name}.json"
    partial_path = ledger_path + ".partial"
    rows = []
    if os.path.exists(partial_path):
        rows = json.load(open(partial_path))
        print(f"[resume] {name}: {len(rows)} items from partial")
    t0 = time.time()
    for i in range(len(rows), len(items)):
        it = items[i]
        ans, unparsed, null = None, False, False
        try:
            for attempt in range(3):
                resp = raw_call_retry(model, it["prompt"], keep_alive="30m")
                ans = parse_answer(resp.get("message", {}).get("content", ""))
                if ans is not None:
                    break
            if ans is None:
                unparsed = True
        except Exception as e:
            null = True
            print(f"[NULL] {name} item {i}: {e}")
        rows.append(dict(id=it["id"], cat=it["cat"], gt=it["gt"],
                         ans=ans, unparsed=unparsed, null=null))
        if (i + 1) % 10 == 0:
            tmp = partial_path + ".tmp"
            with open(tmp, "w") as f:
                json.dump(rows, f)
            os.replace(tmp, partial_path)
            el = time.time() - t0
            print(f"{name} {i+1}/60 ... {el:.0f}s elapsed [ckpt]", flush=True)
    n_null = sum(r["null"] for r in rows)
    n_unp = sum(r["unparsed"] for r in rows)
    parsed = [r for r in rows if r["ans"] is not None]
    acc = sum(r["ans"] == r["gt"] for r in parsed) / len(parsed) if parsed else 0.0
    summary = dict(mind=name, model=model, n=len(rows), n_null=n_null,
                   n_unparsed=n_unp, n_parsed=len(parsed), solo_acc=round(acc, 4))
    with open(ledger_path, "w") as f:
        json.dump(summary | dict(rows=rows), f)
    if os.path.exists(partial_path):
        os.remove(partial_path)
    print(f"DONE {name}: acc={acc:.4f} parsed={len(parsed)} null={n_null} unparsed={n_unp}")
    return summary

def main():
    corpus = json.load(open("w12-corpus.json"))
    items = corpus["items"]
    # warmup check: ollama reachable
    urllib.request.urlopen(BASE + "/api/tags", timeout=10).read()
    summaries = []
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, model in MINDS:
        if only and name != only:
            continue
        s = run_mind(name, model, items)
        summaries.append(s)
        unload(model)  # serial discipline: free the GPU before next mind
        time.sleep(20)  # settle
    if summaries:
        with open("w12-solo-summary.json", "w") as f:
            json.dump(summaries, f, indent=1)
        print(json.dumps(summaries, indent=1))

if __name__ == "__main__":
    main()
