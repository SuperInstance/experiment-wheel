#!/usr/bin/env python3
"""
W10 — LAW AS HELM (station library)

L4 last-holder-spare vs L1 intersection, chains CH-A/CH-B/CH-C.
TASK, check() and the callers claude/kimi/flash(deepseek)/wesley are
W8's, VERBATIM (check byte-identical to W7/W8; wesley keeps num_ctx
4096). check2p is W9's amended acrostic (first 12 letters ==
'THEEILEENLAU') — OBSERVATIONAL only, never scored. call_kimi is
W8's 403 backoff pattern. The SOLI helpers freeze the sealed ordering
rules: ascending by measured phase-0 solo score with W6b-rank
tiebreak (CH-A), reversed for CH-C.
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

def check2p(poem):
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    if len(lines) != 12:
        return False
    return ''.join(l[0] for l in lines).upper()[:12] == 'THEEILEENLAU'

def deepseek(prompt, key, t=0.75):
    body = {"model":"deepseek-chat","messages":[{"role":"user","content":prompt}],"temperature":t,"max_tokens":700}
    req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}','Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())['choices'][0]['message']['content']

def wesley(prompt):
    body={'model':'granite3.1-dense:2b','prompt':prompt+'\n\n12 lines only:',"stream":False,'options':{'temperature':0.7,'num_ctx':4096}}
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

def flash(prompt):
    return deepseek(prompt, KEY)

RUN = {'claude': claude, 'kimi': kimi, 'flash': flash, 'wesley': wesley}
# per-model reviser prompts — W7's REVISE wording, verbatim
REVISE = {
    'claude': lambda prior: "A different model wrote this attempt at the task below. Apply YOUR judgment to THEIR state: check every constraint cold, fix violations, keep what passes. State nothing; output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'kimi':   lambda prior: "Another model wrote this attempt at the task below. Check every constraint cold; fix ALL violations; keep what passes. Output ONLY the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'flash':  lambda prior: "Another model revised this. Check every constraint cold; fix ALL violations. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'wesley': lambda prior: "You are a later hand in the relay. Check the constraints and fix what you can. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
}

CONSTRAINTS = ['12_lines','c1_growth','c2_acrostic','c3_seal','c4_no_rhyme','c5_last_word_unique','c6_punctuation']

def call_kimi(prompt):
    err = None
    for attempt in range(3):
        try:
            out = kimi(prompt)
            if out and out.strip():
                return out
        except Exception as e:
            err = e
        if attempt < 2:
            time.sleep(60)
    raise RuntimeError('kimi failed after 3 attempts: %s' % (err or 'empty output'))

YARDS = ['claude', 'kimi', 'flash', 'wesley']
# ascending-skill tiebreak = W6b's measured solo order (wesley 2, flash 2 w/ rhyme fail, kimi 4, claude 4)
W6B_RANK = {'wesley': 0, 'flash': 1, 'kimi': 2, 'claude': 3}

def hold_set(ck):
    return set(c for c in CONSTRAINTS if ck.get(c) is True)

def soli_asc(solo):
    # CH-A rule: ascending by measured solo score, W6b-rank tiebreak (weakest opens, best solo closes)
    return sorted(solo, key=lambda n: (solo[n]['check']['score'], W6B_RANK[n]))

def soli_desc(solo):
    # CH-C rule: the same measured order, reversed (weak hands last)
    return list(reversed(soli_asc(solo)))

if __name__ == '__main__':
    raise SystemExit('library — run w10_run.py / w10_score.py')
