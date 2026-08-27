#!/usr/bin/env python3
"""
W11 — THE FUSED CATCH (phases 0 + 1)

Registration: W11-fused-catch/REGISTRATION.md (sealed & pushed BEFORE
this ran). TASK and check() are W6b/W7's, VERBATIM. Reviser prompts are
W7's REVISE dict verbatim for the three yards in this cast
(flash/kimi/claude; wesley excluded — GPU reserved for W3b bench).

Phase 0: fresh solo vector (3 calls). Phase 1: K=5 independent
ascending braids (15 calls). All outputs committed as w11-braids.json
BEFORE any aggregation (G0 guard). Phase 2 lives in w11_fusion.py
(written by OPENCODE from the registration spec only).
"""
import json, re, subprocess, sys, time, urllib.request

TASK = """Write EXACTLY 12 lines of a poem called 'the chamber'. Constraints (ALL checked mechanically; they interlock — plan the whole poem before writing):
1. Line n contains exactly n words (line 1 = 1 word, line 12 = 12 words).
2. The FIRST letters of the 12 lines, in order, spell: THEEILEENLAUN
3. Exactly one line contains a 12-character lowercase hex seal (like 8721b4bd042a). That line's word count must equal (first two hex chars as a number mod 12) + 1. Choose your seal so it lands on a line you want.
4. No two lines may end with rhyming words.
5. The final line's last word must appear NOWHERE else in the poem.
6. Punctuation: exactly one comma and one period in the whole poem, no other punctuation; no capitals except the first letter of any line.
Output ONLY the 12 lines."""

def check(poem):
    c = {}
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    c['12_lines'] = len(lines) == 12
    if c['12_lines']:
        wc = [len(l.split()) for l in lines]
        c['c1_growth'] = wc == list(range(1, 13))
        c['c2_acrostic'] = ''.join(l[0] for l in lines).upper() == 'THEEILEENLAUN'
        seals = re.findall(r'\b[0-9a-f]{12}\b', poem)
        c['c3_seal'] = False
        if len(seals) == 1:
            sl = [l for l in lines if seals[0] in l]
            if sl:
                n = len(sl[0].split())
                want = int(seals[0][:2], 16) % 12 + 1
                c['c3_seal'] = n == want
        c['c5_last_word_unique'] = False
        last_w = re.sub(r'[^a-z]', '', lines[-1].split()[-1].lower()) if lines[-1].split() else ''
        body = ' '.join(lines[:-1]).lower()
        c['c5_last_word_unique'] = last_w != '' and last_w not in body
        punc = re.sub(r'[a-zA-Z0-9\s]', '', poem)
        c['c6_punctuation'] = sorted(punc) == ['.', ',']
        caps = re.findall(r'[A-Z]', poem)
        firsts = [l[0] for l in lines if l and l[0].isupper()]
        c['c6_punctuation'] = c['c6_punctuation'] and len(caps) == len(firsts)
    else:
        for k in ('c1_growth','c2_acrostic','c3_seal','c5_last_word_unique','c6_punctuation'): c[k] = False
    # c4 rhyme: crude last-vowel-cluster check
    try:
        lastv = []
        for l in lines:
            w = re.sub(r'[^a-z]', '', l.split()[-1].lower())
            lastv.append(w[-2:] if len(w) >= 2 else w)
        c['c4_no_rhyme'] = len(set(lastv)) == len(lastv)
    except Exception:
        c['c4_no_rhyme'] = False
    c['score'] = sum(v for k, v in c.items() if k != 'score' and v is True)
    return c

def deepseek(prompt, key, t=0.75, seed=None):
    body = {"model":"deepseek-chat","messages":[{"role":"user","content":prompt}],"temperature":t,"max_tokens":700}
    if seed is not None: body["seed"] = seed
    req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}','Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())['choices'][0]['message']['content']

def claude(prompt):
    return subprocess.run(['claude','-p',prompt+' Output ONLY the 12 lines.'],capture_output=True,text=True,timeout=240).stdout

def kimi(prompt):
    out = subprocess.run(['kimi','-p',prompt+' Output ONLY the 12 lines.'],capture_output=True,text=True,timeout=240).stdout
    ls = [l for l in out.split('\n') if l.strip() and not l.startswith('•')]
    return '\n'.join(ls[-12:]) if len(ls) >= 12 else out

KEY = re.search(r'export DEEPSEEK_API_KEY="([^"]+)"', open('/home/eileen/.bashrc').read()).group(1).strip()

RUN = {
    'flash':  lambda p, seed: deepseek(p, KEY, seed=seed),
    'kimi':   lambda p, seed: kimi(p),
    'claude': lambda p, seed: claude(p),
}
# per-model reviser prompts — W7's REVISE dict VERBATIM for the three yards in this cast
REVISE = {
    'claude': lambda prior: "A different model wrote this attempt at the task below. Apply YOUR judgment to THEIR state: check every constraint cold, fix violations, keep what passes. State nothing; output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'kimi':   lambda prior: "Another model wrote this attempt at the task below. Check every constraint cold; fix ALL violations; keep what passes. Output ONLY the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'flash':  lambda prior: "Another model revised this. Check every constraint cold; fix ALL violations. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
}
# W7 tiebreak rank without wesley (W6B_RANK: wesley 0, flash 1, kimi 2, claude 3)
W6B_RANK = {'flash': 1, 'kimi': 2, 'claude': 3}

LEDGER = {'calls': 0, 'retries': 0, 'events': []}
def call(name, prompt, seed, tag):
    """Single logical call; transport failure (no output) retried ONCE, counted."""
    for attempt in (1, 2):
        LEDGER['calls'] += 1
        try:
            out = RUN[name](prompt, seed)
            if not out or not out.strip():
                raise RuntimeError('empty output')
            return out
        except Exception as e:
            LEDGER['events'].append(f'{tag} {name} attempt{attempt} transport-error: {str(e)[:100]}')
            print(tag, name, f'TRANSPORT-ERR a{attempt}:', str(e)[:80], flush=True)
            if attempt == 2:
                raise
            LEDGER['retries'] += 1
            time.sleep(3)

def braid(order, k):
    d, trace, poems = None, [], []
    for i, name in enumerate(order):
        prompt = TASK if i == 0 else REVISE[name](d)
        d = call(name, prompt, 20260831 + k, f'B{k}')
        sc = check(d)
        trace.append({'hand': name, 'check': sc, 'poem': d})
        print(f'B{k}', 'hand', i+1, name, '->', sc['score'], '/6', flush=True)
    return {'k': k, 'order': order, 'trace': trace, 'check': check(d), 'poem': d}

if __name__ == '__main__':
    res, t0 = {'ledger': LEDGER}, time.time()
    # ---- PHASE 0: solo vector (3 calls) — doubles as availability check
    res['solo'] = {}
    for name in ('flash', 'kimi', 'claude'):
        try:
            p = call(name, TASK, 20260831, 'SOLO')
            res['solo'][name] = {'check': check(p), 'poem': p}
            print('solo', name, res['solo'][name]['check']['score'], '/6', flush=True)
        except Exception as e:
            res['solo'][name] = {'error': str(e)[:120]}
            print('solo', name, 'YARD DOWN:', str(e)[:80], flush=True)
    ok = [n for n in ('flash', 'kimi', 'claude') if 'check' in res['solo'].get(n, {})]
    if len(ok) < 2:
        res['aborted'] = 'fewer than 2 solo yards survived'
        json.dump(res, open('w11-braids.json', 'w'), indent=2); raise SystemExit('aborted')
    # ---- order: ascending measured solo, ties by W6B rank
    ascending = sorted(ok, key=lambda n: (res['solo'][n]['check']['score'], W6B_RANK[n]))
    res['order'] = {'ascending': ascending}
    res['yards_down'] = [n for n in ('flash','kimi','claude') if n not in ok]
    print('ORDER ascending:', ' -> '.join(ascending), flush=True)
    json.dump(res, open('w11-braids.json', 'w'), indent=2)  # G0: partials survive crashes
    # ---- PHASE 1: K=5 braids, single pass, no re-rolls
    res['braids'] = []
    for k in range(1, 6):
        res['braids'].append(braid(ascending, k))
        res['ledger'] = LEDGER; res['seconds'] = round(time.time() - t0, 1)
        json.dump(res, open('w11-braids.json', 'w'), indent=2)  # G0: commit each braid as measured
    scores = [b['check']['score'] for b in res['braids']]
    res['braid_scores'] = scores
    res['best_solo'] = max(res['solo'][n]['check']['score'] for n in ok)
    res['seconds'] = round(time.time() - t0, 1); res['ledger'] = LEDGER
    json.dump(res, open('w11-braids.json', 'w'), indent=2)
    print('braids:', scores, '| best solo', res['best_solo'], '| calls', LEDGER['calls'], f"| {res['seconds']}s", flush=True)
