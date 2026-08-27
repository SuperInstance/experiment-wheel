#!/usr/bin/env python3
"""
W10 — LAW AS HELM, runner.

phase0: one solo draw per yard (claude, kimi, flash, wesley), TASK
verbatim, single pass, no re-rolls, nothing model-side seeded; every
call appended crash-safe to w10-calls.jsonl with wall times; hold-
sets land in w10-phase0.json BEFORE any chain fires (G0 guard).
chain: relay under one tag — hand 1 gets TASK verbatim through its
caller (caller-side suffixes stay exactly as the lib defines), later
hands get that yard's W7 REVISE wording; checked after every hand
(trace), hands appended to w10-calls.jsonl, the chain appended to
w10-chains.json.
"""
import argparse, json, os, time
from w10_lib import TASK, RUN, REVISE, YARDS, call_kimi, check, check2p, hold_set

CALLS = 'w10-calls.jsonl'
CHAINS = 'w10-chains.json'

def call(hand, prompt):
    return call_kimi(prompt) if hand == 'kimi' else RUN[hand](prompt)

def log(rec):
    with open(CALLS, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
        f.flush()

def phase0():
    solo = {}
    for hand in YARDS:
        t0 = time.time()
        rec = {'phase': 'phase0', 'hand': hand, 'mode': 'solo', 'prompt': TASK, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S')}
        try:
            poem = call(hand, TASK)
            rec.update(poem=poem, check=check(poem), check2p=check2p(poem))
            solo[hand] = {'check': rec['check'], 'check2p': rec['check2p'], 'poem': poem}
        except Exception as e:
            rec['error'] = str(e)[:200]
            solo[hand] = {'error': str(e)[:200]}
            print('solo', hand, 'FAIL', str(e)[:80], flush=True)
        rec['secs'] = round(time.time() - t0, 1)
        log(rec)
        if 'check' in solo[hand]:
            print('solo', hand, solo[hand]['check']['score'], '/6', 'in', rec['secs'], 's', flush=True)
    with open('w10-phase0.json', 'w', encoding='utf-8') as f:
        json.dump({'solo': solo}, f, indent=2)
    print('hold-sets (W10 instrument, verbatim check):')
    for hand in YARDS:
        s = solo[hand]
        if 'check' in s:
            extra = ' | c2p HELD (observational)' if s['check2p'] else ''
            print(' ', hand, sorted(hold_set(s['check'])), extra)
        else:
            print(' ', hand, 'ERROR — excluded from hold-sets')
    print('wrote w10-phase0.json')

def chain(order, tag):
    d, trace = None, []
    for i, hand in enumerate(order):
        prompt = TASK if i == 0 else REVISE[hand](d)
        t0 = time.time()
        try:
            poem = call(hand, prompt)
        except Exception as e:
            log({'phase': 'chain', 'tag': tag, 'i': i, 'hand': hand, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'error': str(e)[:200]})
            print(tag, 'hand', i + 1, hand, 'ERROR', str(e)[:100], flush=True)
            raise
        rec = {'phase': 'chain', 'tag': tag, 'i': i, 'hand': hand, 'poem': poem,
               'check': check(poem), 'check2p': check2p(poem), 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
               'secs': round(time.time() - t0, 1)}
        log(rec)
        trace.append({'i': i, 'hand': hand, 'check': rec['check'], 'check2p': rec['check2p']})
        print(tag, 'hand', i + 1, hand, '->', rec['check']['score'], '/6', sorted(hold_set(rec['check'])), 'in', rec['secs'], 's', flush=True)
        d = poem
    entry = {'tag': tag, 'order': order, 'trace': trace,
             'final_check': check(d), 'final_check2p': check2p(d), 'poem': d}
    chains = []
    if os.path.exists(CHAINS):
        with open(CHAINS, encoding='utf-8') as f:
            chains = json.load(f)
    chains.append(entry)
    with open(CHAINS, 'w', encoding='utf-8') as f:
        json.dump(chains, f, indent=2)
    print(tag, 'per-hand scores:', [t['check']['score'] for t in trace])
    print(tag, 'final', entry['final_check']['score'], '/6', sorted(hold_set(entry['final_check'])),
          '| c2p', entry['final_check2p'], '| appended to', CHAINS)

def main():
    ap = argparse.ArgumentParser(description='W10 — LAW AS HELM runner')
    sub = ap.add_subparsers(dest='mode', required=True)
    sub.add_parser('phase0', help='one solo draw per yard, TASK verbatim, single pass')
    cp = sub.add_parser('chain', help='relay chain: hand 1 TASK, later hands W7 REVISE wording')
    cp.add_argument('--order', default='claude,kimi,flash,wesley', help='comma-separated hand order')
    cp.add_argument('--tag', required=True, help='chain tag, e.g. CH-A')
    a = ap.parse_args()
    if a.mode == 'phase0':
        phase0()
        return
    order = [x.strip() for x in a.order.split(',') if x.strip()]
    bad = [h for h in order if h not in YARDS]
    if bad:
        raise SystemExit('unknown yards: %s (known: %s)' % (bad, YARDS))
    if len(order) < 2:
        raise SystemExit('a chain needs at least 2 hands')
    chain(order, a.tag)

if __name__ == '__main__':
    main()
