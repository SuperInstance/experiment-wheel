#!/usr/bin/env python3
"""
W8 — THE REVISER'S BLIND SIDE, phase 2: regime passes.

For each seed (S1,S2) x reviser (kimi,claude,flash,wesley) x regime
(baseline, minimal_edit, verify_then_fix): one pass, check, constraint
report vs seed. Each cell is appended immediately to w8-revisions.jsonl
(crash-safe). Errors are recorded and spent — no re-roll. kimi retries
the same call after sleep 60, up to 3 attempts (403 quota backoff).
"""
import json, os, re, time
from w8_lib import RUN, kimi, check, regime_prompt, constraint_report

SEEDS = ['S1', 'S2']
REVISERS = ['kimi', 'claude', 'flash', 'wesley']
REGIMES = ['baseline', 'minimal_edit', 'verify_then_fix']

def parse_vtf(out):
    keep = []
    for l in out.split('\n'):
        s = l.strip()
        if not s or re.match(r'\s*\d+[.\)]', s) or 'PASS' in s or 'FAIL' in s:
            continue
        keep.append(s)
    return '\n'.join(keep[-12:])

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

def call(reviser, prompt):
    if reviser == 'kimi':
        return call_kimi(prompt)
    return RUN[reviser](prompt)

def main():
    if not os.path.exists('w8-seeds.json'):
        raise SystemExit('w8-seeds.json missing — run w8_seeds.py first')
    seeds = json.load(open('w8-seeds.json'))
    bysid = {c['seed_id']: c for c in seeds['chosen']}
    n = 0
    for sid in SEEDS:
        seed = bysid[sid]
        seed_poem, seed_check = seed['poem'], check(seed['poem'])
        for reviser in REVISERS:
            for regime in REGIMES:
                prompt = regime_prompt(reviser, regime, seed_poem)
                cell = {'seed_id': sid, 'reviser': reviser, 'regime': regime,
                        'draw_id': seed['draw_id'], 'prompt': prompt}
                try:
                    raw = call(reviser, prompt)
                    parsed = parse_vtf(raw) if regime == 'verify_then_fix' else raw
                    ck = check(parsed)
                    cell.update(raw_output=raw, parsed_poem=parsed, rev_check=ck,
                                constraint_report=constraint_report(seed_poem, parsed, seed_check, ck))
                    print(sid, reviser, regime, '->', ck['score'], '/6', flush=True)
                except Exception as e:
                    cell['error'] = str(e)[:200]
                    print(sid, reviser, regime, 'ERROR', str(e)[:100], flush=True)
                with open('w8-revisions.jsonl', 'a') as f:
                    f.write(json.dumps(cell) + '\n')
                    f.flush()
                n += 1
    print('done:', n, 'cells -> w8-revisions.jsonl')

if __name__ == '__main__':
    main()
