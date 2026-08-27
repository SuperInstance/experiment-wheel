#!/usr/bin/env python3
"""
W7 — THE ORDERED BRAID (Station 1, third cast)

W6b's Weak-Link Law: a braid holds only what its weakest RELEVANT hand
can hold — the hands that touch a draft LAST set its ceiling. W6b ran
the mixed crew backwards (strong early, weak last) and sank to 2/6 vs
4/6 best solo. W7 is the law's falsifier, prediction on record in
REGISTRATION.md BEFORE this run:

  ASCENDING-skill chain (weakest first, best solo closes) -> braid >= best solo.
  If braid < best solo -> Weak-Link Law FALSIFIED.

Contrast pair: one DESCENDING braid (same crew, reversed) — law
predicts it sinks (weak hands last).

TASK and check() are W6b's, VERBATIM, for comparability.
"""
import json, re, subprocess, time, urllib.request

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

def deepseek(prompt, key, t=0.75):
    body = {"model":"deepseek-chat","messages":[{"role":"user","content":prompt}],"temperature":t,"max_tokens":700}
    req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}','Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())['choices'][0]['message']['content']

def wesley(prompt):
    body={'model':'granite3.1-dense:2b','prompt':prompt+'\n\n12 lines only:',"stream":False,'options':{'temperature':0.7}}
    r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/generate',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'}),timeout=240)
    return json.loads(r.read())['response']

def claude(prompt):
    return subprocess.run(['claude','-p',prompt+' Output ONLY the 12 lines.'],capture_output=True,text=True,timeout=240).stdout

def kimi(prompt):
    out = subprocess.run(['kimi','-p',prompt+' Output ONLY the 12 lines.'],capture_output=True,text=True,timeout=240).stdout
    ls = [l for l in out.split('\n') if l.strip() and not l.startswith('•')]
    return '\n'.join(ls[-12:]) if len(ls) >= 12 else out

import re as _re
KEY = _re.search(r'export DEEPSEEK_API_KEY="([^"]+)"', open('/home/eileen/.bashrc').read()).group(1).strip()

RUN = {'claude': claude, 'kimi': kimi, 'flash': lambda p: deepseek(p, KEY), 'wesley': wesley}
# per-model reviser prompts — wording identical to W6b where W6b used that yard as a reviser
REVISE = {
    'claude': lambda prior: "A different model wrote this attempt at the task below. Apply YOUR judgment to THEIR state: check every constraint cold, fix violations, keep what passes. State nothing; output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'kimi':   lambda prior: "Another model wrote this attempt at the task below. Check every constraint cold; fix ALL violations; keep what passes. Output ONLY the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'flash':  lambda prior: "Another model revised this. Check every constraint cold; fix ALL violations. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'wesley': lambda prior: "You are a later hand in the relay. Check the constraints and fix what you can. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
}
# ascending-skill tiebreak = W6b's measured solo order (wesley 2, flash 2 w/ rhyme fail, kimi 4, claude 4)
W6B_RANK = {'wesley': 0, 'flash': 1, 'kimi': 2, 'claude': 3}

def braid(order, tag):
    d, trace = None, []
    for i, name in enumerate(order):
        prompt = TASK if i == 0 else REVISE[name](d)
        d = RUN[name](prompt)
        sc = check(d)
        trace.append({'hand': name, 'check': sc})
        print(tag, 'hand', i+1, name, '->', sc['score'], '/6', flush=True)
    return {'order': order, 'trace': trace, 'check': check(d), 'poem': d}

if __name__ == '__main__':
    res = {}
    t0 = time.time()
    # 1. SOLO — all four yards, fresh draw
    for name in ('claude', 'kimi', 'flash', 'wesley'):
        try:
            p = RUN[name](TASK); res.setdefault('solo', {})[name] = {'check': check(p), 'poem': p}
            print('solo', name, res['solo'][name]['check']['score'], '/6', flush=True)
        except Exception as e:
            res.setdefault('solo', {})[name] = {'error': str(e)[:80]}; print('solo', name, 'FAIL', str(e)[:60], flush=True)
    ok = [n for n in ('claude', 'kimi', 'flash', 'wesley') if 'check' in res['solo'].get(n, {})]
    if len(ok) < 2:
        res['aborted'] = 'fewer than 2 solo yards survived'
        json.dump(res, open('w7-results.json', 'w'), indent=2); raise SystemExit('aborted')
    # 2. measured ranks — ascending = weakest first, best solo closes
    ascending = sorted(ok, key=lambda n: (res['solo'][n]['check']['score'], W6B_RANK[n]))
    descending = list(reversed(ascending))
    res['order'] = {'ascending': ascending, 'descending': descending}
    print('ORDER ascending:', ' -> '.join(ascending), flush=True)
    # 3. the two braids — prediction: ASC >= best solo; law also predicts DESC sinks
    res['braid_ascending'] = braid(ascending, 'ASC')
    res['braid_descending'] = braid(descending, 'DESC')
    best_solo = max(res['solo'][n]['check']['score'] for n in ok)
    res['best_solo'] = best_solo
    res['prediction_asc_ge_best_solo'] = res['braid_ascending']['check']['score'] >= best_solo
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open('w7-results.json', 'w'), indent=2)
    print('best solo', best_solo, '| ASC', res['braid_ascending']['check']['score'], '| DESC', res['braid_descending']['check']['score'], flush=True)
    print('saved w7-results.json', res['seconds'], 's')
