#!/usr/bin/env python3
"""
W8 — THE REVISER'S BLIND SIDE (station library)

What does a reviser do to constraints it does not hold? Holders are
pre-registered in REGISTRATION.md (on record BEFORE this run).
TASK and check() are W7's, VERBATIM, for comparability. Callers
claude/kimi/flash(deepseek)/wesley are W7's (wesley gains num_ctx 4096).
"""
import json, re, subprocess, urllib.request

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
# per-model reviser prompts — wording identical to W6b/W7
REVISE = {
    'claude': lambda prior: "A different model wrote this attempt at the task below. Apply YOUR judgment to THEIR state: check every constraint cold, fix violations, keep what passes. State nothing; output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'kimi':   lambda prior: "Another model wrote this attempt at the task below. Check every constraint cold; fix ALL violations; keep what passes. Output ONLY the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'flash':  lambda prior: "Another model revised this. Check every constraint cold; fix ALL violations. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
    'wesley': lambda prior: "You are a later hand in the relay. Check the constraints and fix what you can. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+prior,
}

REGIME_EXTRA = {
    'minimal_edit': 'Change as few characters as possible. Touch ONLY lines that violate a constraint.',
    'verify_then_fix': 'First list each numbered constraint with PASS or FAIL for this attempt, then output the corrected 12 lines.',
}

def regime_prompt(name, regime, prior):
    if regime == 'baseline':
        return REVISE[name](prior)
    head = _re.search(r'^(.*?)\n\nTASK:', REVISE[name](''), re.S).group(1)
    return head + "\n\n" + REGIME_EXTRA[regime] + "\n\nTASK:\n" + TASK + "\n\nATTEMPT:\n" + prior

CONSTRAINTS = ['12_lines','c1_growth','c2_acrostic','c3_seal','c4_no_rhyme','c5_last_word_unique','c6_punctuation']

def char_levenshtein(a, b):
    if a == b: return 0
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def per_line_edit_distance(seed_lines, rev_lines):
    ds = []
    for i in range(max(len(seed_lines), len(rev_lines))):
        a = seed_lines[i] if i < len(seed_lines) else None
        b = rev_lines[i] if i < len(rev_lines) else None
        if a is None and b is None: ds.append(0)
        elif a is None: ds.append(len(b))
        elif b is None: ds.append(len(a))
        else: ds.append(char_levenshtein(a, b))
    return ds

def carrier_lines(constraint, seed_check, lines):
    n = len(lines)
    if constraint == 'c3_seal':
        idx = [i for i, l in enumerate(lines) if re.search(r'\b[0-9a-f]{12}\b', l)]
        return [idx[0]] if len(idx) == 1 else list(range(n))
    if constraint == 'c5_last_word_unique':
        return [n - 1] if n else []
    return list(range(n))

def last_words(lines):
    out = []
    for l in lines:
        t = l.split()
        out.append(t[-1] if t else '')
    return out

def poem_lines(poem):
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    return [l for l in lines if not l.startswith('#') and not l.startswith('```')]

def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def constraint_report(seed_poem, rev_poem, seed_check, rev_check):
    sl, rl = poem_lines(seed_poem), poem_lines(rev_poem)
    per_line = per_line_edit_distance(sl, rl)
    rep = {}
    for c in CONSTRAINTS:
        if c in ('c6_punctuation', '12_lines'):
            a, b = ' '.join(sl), ' '.join(rl)
            dist = char_levenshtein(a, b) / max(len(a), len(b), 1)
        elif c == 'c4_no_rhyme':
            dist = _mean(per_line_edit_distance(last_words(sl), last_words(rl)))
        else:
            idx = carrier_lines(c, seed_check, sl)
            dist = _mean([per_line[i] for i in idx])
        rep[c] = {'seed_pass': bool(seed_check.get(c)), 'rev_pass': bool(rev_check.get(c)),
                  'carrier_edit_distance': dist}
    return rep
