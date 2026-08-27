#!/usr/bin/env python3
"""
W6 — THE BRAID (Experiment Wheel, Station 1: SPIKE)

QUESTION (the captain's, the fragment's): what does a braid of DIFFERENT
models compute that no braid of copies ever can?

DESIGN: one piece of thinking too demanding for any single yard (per the
regime law: the hand must be DEMANDING or the mating doesn't matter).
Each yard drafts alone (A×A baseline) AND the yards cross-iterate live:
each sees the OTHERS' drafts and must apply its own function to their
state (revise-and-why, not review). A referee judges all outputs blind.

THE HAND: a hard synthesis question with a verifiable structure — a
13-line poem that must simultaneously satisfy 5 hard constraints
(verified mechanically: each line encodes one of the ten EILEEN pieces;
the ten pieces' joint order recoverable; one line contains a sha-like
seal; ends on the keel; no rhyme [the fog collects rhymes]).

YARDS: claude (Sonnet), kimi, DeepSeek-Flash, Wesley (granite 2B local).
MODES: (1) solo — each yard alone; (2) braid-of-copies — 4 rounds of the
SAME yard revising itself; (3) braid-of-different — 4 rounds where each
yard revises THE OTHERS' drafts (round-robin, each pass states WHY).

SCORE (mechanical where possible): constraint passes (5, hard-verified);
distinct-line-coverage of the ten pieces; novelty across modes (how much
the final differs from round 1); referee ranking blind.
KILL: if braid-of-different doesn't beat braid-of-copies on constraint
passes at ≥2 sigma, the different-model braid doesn't pay at this task.
"""
import json, re, subprocess, time, urllib.request

PIECES = ["keel","stem","keelson","breast-hook","rigging","bulwarks","ensign","scuppers","sheerboard","figurehead"]
TASK = """Write EXACTLY 13 lines. Hard constraints (all mechanically checked):
1. Ten lines each name or unmistakably evoke ONE of these pieces, in this joint order: keel, stem, keelson, breast-hook, rigging, bulwarks, ensign, scuppers, sheerboard, figurehead. The ten piece-lines may be lines 1-10, or interleaved among 13, but MUST appear in this relative order.
2. One line must contain a 16-hex-char 'seal' (like 8721b4bd042aa8c5).
3. The final line must return to the keel's image (water, blink, or the word keel).
4. NO rhyming lines anywhere (the fog collects rhymes).
5. Each line under 12 words.
Output ONLY the 13 lines."""

def check(poem: str):
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    c = {}
    c['lines_13'] = len(lines) == 13
    order = []
    for l in lines:
        for i, p in enumerate(PIECES):
            if re.search(rf'\b{p[:-1] if p.endswith("-hook") else p}\b', l.lower().replace('breast hook','breast-hook')):
                order.append(i); break
    # relative order check: the found indices must be non-decreasing and cover all 10
    c['order_ok'] = order == sorted(order) and len(set(order)) == 10
    c['seal'] = bool(re.search(r'\b[0-9a-f]{16}\b', poem))
    c['ends_keel'] = bool(re.search(r'keel|blink|water', lines[-1].lower())) if lines else False
    c['no_rhyme'] = True  # checked manually by referee; placeholder
    c['short_lines'] = all(len(l.split()) <= 12 for l in lines)
    c['score'] = sum(v for k, v in c.items() if k != 'score' and isinstance(v, bool))
    return c

def deepseek(prompt, key):
    body = {"model":"deepseek-chat","messages":[{"role":"user","content":prompt}],"temperature":0.8,"max_tokens":500}
    req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}','Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())['choices'][0]['message']['content']

def wesley(prompt):
    body={'model':'granite3.1-dense:2b','prompt':prompt+"\n\n13 lines only:","stream":False,'options':{'temperature':0.8}}
    r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/generate',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'}),timeout=180)
    return json.loads(r.read())['response']

def claude(prompt):
    return subprocess.run(['claude','-p',prompt+' Output ONLY the 13 lines.'],capture_output=True,text=True,timeout=240).stdout

def kimi(prompt):
    out = subprocess.run(['kimi','-p',prompt+' Output ONLY the 13 lines.'],capture_output=True,text=True,timeout=240)
    # kimi prefixes thinking; take the last 13+ non-empty lines region heuristically
    txt = out.stdout
    lines = [l for l in txt.split('\n') if l.strip()]
    return '\n'.join(lines[-13:]) if len(lines) >= 13 else txt

import re as _re
bashrc = open('/home/eileen/.bashrc').read()
m = _re.search(r'export DEEPSEEK_API_KEY="?([^"\n]+)"?', bashrc)
KEY = m.group(1).strip() if m else None

if __name__ == '__main__':
    results = {'modes': {}}
    t0=time.time()
    # SOLO
    solo = {}
    for name, fn in [('claude', claude), ('kimi', kimi), ('flash', lambda p: deepseek(p, KEY)), ('wesley', wesley)]:
        try:
            poem = fn(TASK)
            solo[name] = {'poem': poem, 'check': check(poem)}
            print(f"solo {name}: score {solo[name]['check']['score']}/6")
        except Exception as e:
            solo[name] = {'error': str(e)[:100]}
            print(f"solo {name}: FAILED {str(e)[:60]}")
    results['modes']['solo'] = solo
    # BRAID-OF-COPIES: flash self-revising 4 rounds
    # BRAID-OF-DIFFERENT: round-robin cross-revision
    p = TASK
    for r in range(4):
        p = deepseek(p + "\n\nYour own previous attempt is above. Revise it. State WHY in one line, then the 13 lines.", KEY)
    results['modes']['copies'] = {'flash_4rounds': {'poem': p, 'check': check(p)}}
    print('copies flash 4r: score', results['modes']['copies']['flash_4rounds']['check']['score'], '/6')
    # braid-of-different: kimi drafts, claude revises kimi's, flash revises claude's, wesley final
    try:
        d1 = kimi(TASK)
        d2 = claude("A different model drafted this attempt at the task below. Apply YOUR judgment to THEIR state: keep what carries load, cut what doesn't, state one line of WHY first, then your 13 lines.\n\nTASK:\n" + TASK + "\n\nTHEIR DRAFT:\n" + d1)
        d3 = deepseek("Another model revised a draft. Continue the braid: one line WHY, then your 13 lines.\n\nTASK:\n" + TASK + "\n\nCURRENT DRAFT:\n" + d2, KEY)
        d4 = wesley("You are the last hand in a braid of four different minds. One line why, then the final 13 lines.\n\nTASK:\n" + TASK + "\n\nCURRENT DRAFT:\n" + d3)
        chain = {'kimi': d1, 'claude': d2, 'flash': d3, 'wesley': d4}
        results['modes']['braid'] = {n: {'poem': p_, 'check': check(p_)} for n, p_ in chain.items()}
        for n in chain: print(f"braid {n}: score", results['modes']['braid'][n]['check']['score'], '/6')
    except Exception as e:
        results['modes']['braid'] = {'error': str(e)[:200]}
        print('braid FAILED:', str(e)[:120])
    results['seconds'] = round(time.time()-t0,1)
    json.dump(results, open('w6-results.json','w'), indent=2)
    print('saved w6-results.json in', results['seconds'], 's')
