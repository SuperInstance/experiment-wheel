#!/usr/bin/env python3
"""
W6b — THE BRAID AT THE DEMANDING HAND (Station 1, second cast)

W6a's lesson (the regime law applied to itself): the hand must be hard
enough that every solo yard scores ZERO — otherwise the braid has nothing
to add. This cast's hand: interlocking constraints with a verifier the
yards never see. All constraints mechanically checked; no model knows
the checker.

THE HAND: a 12-line 'chamber' poem where:
  C1: lines alternate STRICTLY: odd lines are one word longer than the
      line before them? NO — stricter and less self-checkable by feel:
      line n contains exactly n words for n=1..12 (a growing chamber).
  C2: the FIRST letters of the 12 lines spell THEEILEENLAUN (12 letters).
  C3: exactly one line contains a 12-hex seal; the line's word-count
      equals the seal's first hex-digit pair mod 12 + 1 (verifiable).
  C4: no line's last word rhymes with any other line's last word.
  C5: the final line's single word must appear NOWHERE else in the poem.
  C6: total poem contains exactly one comma, one period, nothing else
      punctuated; no capital letters except line-initial.

Score = 6 checks. Expectation: solo yards score 0-1 (the constraints
interlock — satisfying C1 fights C2 fights C3). Then: copies (flash x4)
vs braid-of-different (kimi -> claude -> flash -> wesley), 3 rounds.
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

if __name__ == '__main__':
    res = {}
    t0 = time.time()
    # SOLO — expectation 0-1/6 per yard
    for name, fn in [('claude', claude), ('kimi', kimi), ('flash', lambda p: deepseek(p, KEY)), ('wesley', wesley)]:
        try:
            p = fn(TASK); res.setdefault('solo', {})[name] = {'check': check(p), 'poem': p}
            print('solo', name, res['solo'][name]['check']['score'], '/6')
        except Exception as e:
            res.setdefault('solo', {})[name] = {'error': str(e)[:80]}; print('solo', name, 'FAIL', str(e)[:50])
    # COPIES: flash self-revising x4
    p = TASK
    for r in range(4):
        p = deepseek("Your previous attempt follows. Check every constraint cold; fix ALL violations. Attempt:\n\n" + p.split('Output ONLY')[-1][:1500] + "\n\nFull constraints: " + TASK, KEY)
    res['copies'] = {'check': check(p), 'poem': p}
    print('copies flash x4:', res['copies']['check']['score'], '/6')
    # BRAID: kimi -> claude -> flash -> wesley -> flash(final polish), full task visible each hand
    try:
        d = kimi(TASK)
        d = claude("A different model wrote this attempt at the task below. Apply YOUR judgment to THEIR state: check every constraint cold, fix violations, keep what passes. State nothing; output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+d)
        d = deepseek("Another model revised this. Check every constraint cold; fix ALL violations. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+d, KEY)
        d = wesley("You are the fourth hand. Check the constraints and fix what you can. Output only 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+d)
        d = deepseek("Final polish hand. Every constraint checked cold. Output only the 12 lines.\n\nTASK:\n"+TASK+"\n\nATTEMPT:\n"+d, KEY)
        res['braid'] = {'check': check(d), 'poem': d}
        print('braid 4-model:', res['braid']['check']['score'], '/6')
    except Exception as e:
        res['braid'] = {'error': str(e)[:200]}; print('braid FAIL', str(e)[:120])
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open('w6b-results.json', 'w'), indent=2)
    print('saved w6b-results.json', res['seconds'], 's')
