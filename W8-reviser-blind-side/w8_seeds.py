#!/usr/bin/env python3
"""
W8 — THE REVISER'S BLIND SIDE, phase 1: seed draw.

One solo pass per yard on TASK; keep the two best drafts with score>=3
(ties: W7 solo score, then claude before kimi). Failing yards redraw
(-d2, -d3; max 2 extra per yard, 8 draws total). Kill gate exits
nonzero if fewer than 2 eligible drafts survive the caps.
"""
import json
from w8_lib import RUN, TASK, check, CONSTRAINTS

YARDS = ['kimi', 'claude', 'flash', 'wesley']
W7_SOLO = {'claude': 4, 'kimi': 4, 'flash': 2, 'wesley': 2}
PREF = {'claude': 0, 'kimi': 1, 'flash': 2, 'wesley': 3}

def main():
    draws = []
    ndraws = {y: 0 for y in YARDS}

    def draw(yard):
        ndraws[yard] += 1
        did = '20260828-%s-d%d' % (yard, ndraws[yard])
        rec = {'draw_id': did, 'yard': yard}
        try:
            poem = RUN[yard](TASK)
            rec.update(poem=poem, check=check(poem))
            print('draw', did, '->', rec['check']['score'], '/6', flush=True)
        except Exception as e:
            rec['error'] = str(e)[:120]
            print('draw', did, 'ERROR', str(e)[:80], flush=True)
        draws.append(rec)

    for y in YARDS:
        draw(y)

    def best(yard):
        ok = [d for d in draws if d['yard'] == yard and 'check' in d]
        return max(ok, key=lambda d: d['check']['score']) if ok else None

    def eligible(yard):
        b = best(yard)
        return b is not None and b['check']['score'] >= 3

    while sum(ndraws.values()) < 8:
        if sum(1 for y in YARDS if eligible(y)) >= 2:
            break
        failing = [y for y in YARDS if not eligible(y) and ndraws[y] < 3]
        if not failing:
            break
        for y in failing:
            if sum(ndraws.values()) >= 8:
                break
            draw(y)

    elig = [y for y in YARDS if eligible(y)]
    if len(elig) < 2:
        json.dump({'draws': draws, 'kill_gate': True}, open('w8-seeds.json', 'w'), indent=2)
        raise SystemExit('KILL GATE: fewer than 2 eligible drafts (score>=3) after caps')

    ranked = sorted((best(y) for y in elig),
                    key=lambda d: (-d['check']['score'], -W7_SOLO[d['yard']], PREF[d['yard']]))
    chosen = [{'seed_id': sid, 'draw_id': d['draw_id'], 'yard': d['yard'],
               'poem': d['poem'], 'check': d['check']}
              for sid, d in zip(('S1', 'S2'), ranked[:2])]
    seed_pass = {c['seed_id']: {k: bool(c['check'].get(k)) for k in CONSTRAINTS} for c in chosen}
    out = {'draws': draws, 'chosen': chosen, 'seed_pass': seed_pass,
           'chosen_seeds': ['S1', 'S2']}
    json.dump(out, open('w8-seeds.json', 'w'), indent=2)
    print('seeds:', [(c['seed_id'], c['draw_id'], c['check']['score'], '/6') for c in chosen])
    print('saved w8-seeds.json')

if __name__ == '__main__':
    main()
