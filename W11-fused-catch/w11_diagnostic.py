import json
import os
import re
import sys


CONSTRAINTS = ('c1_growth', 'c2_acrostic', 'c3_seal', 'c4_no_rhyme', 'c5_last_word_unique', 'c6_punctuation')
CELLS = ('12_lines',) + CONSTRAINTS
NOTE = ('diagnostic lens per REGISTRATION-sealed-amendment-1.md; primary numbers live in '
        'w11-results.json and are never replaced by these.')


def check(poem):
    # frozen checker, verbatim copy from w11_fusion.py (for delta comparison only)
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


def check2(poem):
    # corrected lens per sealed amendment 1: copy of the frozen check() with
    # ONLY the c2 target sliced to 12 letters and the c6 sorted literal repaired
    c = {}
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    c['12_lines'] = len(lines) == 12
    if c['12_lines']:
        wc = [len(l.split()) for l in lines]
        c['c1_growth'] = wc == list(range(1, 13))
        c['c2_acrostic'] = ''.join(l[0] for l in lines).upper() == 'THEEILEENLAU'  # c2' repaired
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
        c['c6_punctuation'] = sorted(punc) == [',', '.']  # c6' repaired
        caps = re.findall(r'[A-Z]', poem)
        firsts = [l[0] for l in lines if l and l[0].isupper()]
        c['c6_punctuation'] = c['c6_punctuation'] and len(caps) == len(firsts)
    else:
        for k in ('c1_growth','c2_acrostic','c3_seal','c5_last_word_unique','c6_punctuation'): c[k] = False
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


def local_score(c):
    return int(c['c1_growth']) + int(c['c2_acrostic'])


def global_score(c):
    return int(c['c3_seal']) + int(c['c4_no_rhyme']) + int(c['c5_last_word_unique']) + int(c['c6_punctuation'])


def synthetic_poem():
    return '\n'.join([
        'Time',
        'Hollow rivers',
        'Emerald tides drift',
        'Evening holds 8721b4bd042a close',
        'Islands rise from quiet mists',
        'Lanterns flicker above the calm, bay',
        'Echoes wander where the soft winds sigh',
        'Each season turns the old hills toward dusk',
        'Northern lights bend above the frozen lake at midnight',
        'Long shadows stretch across the valley while stars awaken slowly',
        'Amber dusk settles over rooftops as the harbor lights begin glowing',
        'Under bright mornings the village children chase silver kites until dusk falls.',
    ])


def lens(poem):
    frozen = check(poem)
    corrected = check2(poem)
    flipped = {}
    for k in CELLS:
        if bool(frozen[k]) != bool(corrected[k]):
            flipped[k] = {'frozen': bool(frozen[k]), 'corrected': bool(corrected[k])}
    return {
        'score_frozen': frozen['score'],
        'score_prime': corrected['score'],
        'flipped': flipped,
        'frozen_check': frozen,
        'corrected_check': corrected,
    }


def self_test():
    poem = synthetic_poem()
    c = check2(poem)
    try:
        assert c['score'] == 7 and all(c[k] for k in CELLS)
    except AssertionError:
        failed = [k for k in CELLS if not c[k]]
        print("SELF-TEST FAILED: check2() on all-constraints synthetic poem: score=%d (want 7); failed cells: %s; full check2: %s" % (c['score'], failed, c), file=sys.stderr)
        sys.exit(2)

    bad = poem.replace('Lanterns flicker above the calm, bay', 'Lanterns flicker Above the calm, bay')
    cb = check2(bad)
    try:
        assert not cb['c6_punctuation']
    except AssertionError:
        print("SELF-TEST FAILED: check2() c6' on one-comma+one-period poem with a mid-line capital should be False; full check2: %s" % cb, file=sys.stderr)
        sys.exit(2)


def main():
    self_test()

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'w11-braids.json'), encoding='utf-8') as f:
        data = json.load(f)
    with open(os.path.join(here, 'w11-results.json'), encoding='utf-8') as f:
        results = json.load(f)

    solo = data.get('solo', {})
    braids = data['braids']

    solo_diag = {}
    for yard in solo:
        entry = solo[yard]
        d = lens(entry['poem'])
        d['stored_check'] = entry.get('check')
        solo_diag[yard] = d

    braid_diag = {}
    corrected_by_k = {}
    for b in braids:
        d = lens(b['poem'])
        braid_diag[b['k']] = d
        corrected_by_k[b['k']] = d['corrected_check']

    loo_diag = []
    for r in results['loo']:
        fc = check2(r['fused_poem'])
        fl = local_score(fc)
        fg = global_score(fc)
        four = [{'k': k, 'score': corrected_by_k[k]['score'], 'check': corrected_by_k[k]}
                for k in sorted(int(k) for k in r['parent_scores'])]
        bp = sorted(four, key=lambda p: (-p['score'], p['k']))[0]
        pl = local_score(bp['check'])
        pg = global_score(bp['check'])
        p1 = fl >= pl + 1
        p1_strict = fl >= max(local_score(p['check']) for p in four) + 1
        p2 = fg <= pg
        p2_strict = fg <= max(global_score(p['check']) for p in four)
        deltas = {}
        for key in CONSTRAINTS:
            deltas[key] = {
                'fused': bool(fc[key]),
                'best_parent': bool(bp['check'][key]),
                'delta': int(bool(fc[key])) - int(bool(bp['check'][key])),
            }
        loo_diag.append({
            'held_out': r['held_out'],
            'parent_scores_prime': {p['k']: p['score'] for p in four},
            'fusion_score_prime': fc['score'],
            'fusion_local_prime': fl,
            'fusion_global_prime': fg,
            'best_parent_k_prime': bp['k'],
            'parent_local_prime': pl,
            'parent_global_prime': pg,
            'p1_prime': p1,
            'p1_prime_strict': p1_strict,
            'p2_prime': p2,
            'p2_prime_strict': p2_strict,
            'constraint_deltas_prime': deltas,
        })

    counts = {
        'p1_prime_count': sum(1 for r in loo_diag if r['p1_prime']),
        'p1_prime_strict_count': sum(1 for r in loo_diag if r['p1_prime_strict']),
        'p2_prime_count': sum(1 for r in loo_diag if r['p2_prime']),
        'p2_prime_strict_count': sum(1 for r in loo_diag if r['p2_prime_strict']),
    }

    prime_scores = [corrected_by_k[b['k']]['score'] for b in braids]
    max_prime = max(prime_scores)
    mean_prime = sum(prime_scores) / len(prime_scores)
    p3 = {'max_score_prime': max_prime, 'mean_score_prime': mean_prime, 'holds_prime': max_prime >= mean_prime + 1}

    diagnostic = {
        'note': NOTE,
        'solo': solo_diag,
        'braids': braid_diag,
        'loo_prime': loo_diag,
        'counts_prime': counts,
        'p3_prime': p3,
    }

    with open(os.path.join(here, 'w11-diagnostic.json'), 'w', encoding='utf-8') as f:
        json.dump(diagnostic, f, indent=2, ensure_ascii=False)
        f.write('\n')

    for yard, d in solo_diag.items():
        print('SOLO %s score frozen=%d prime=%d flipped=%s' % (yard, d['score_frozen'], d['score_prime'], sorted(d['flipped'])))
    for k, d in braid_diag.items():
        print('BRAID k=%s score frozen=%d prime=%d flipped=%s' % (k, d['score_frozen'], d['score_prime'], sorted(d['flipped'])))
    for r in loo_diag:
        print('LOO held_out=%d parent_scores_prime=%s best_parent(k=%d local=%d global=%d) fusion(score=%d local=%d global=%d) p1=%s p2=%s' % (
            r['held_out'], r['parent_scores_prime'], r['best_parent_k_prime'], r['parent_local_prime'], r['parent_global_prime'],
            r['fusion_score_prime'], r['fusion_local_prime'], r['fusion_global_prime'], r['p1_prime'], r['p2_prime']))
    print('counts p1_prime=%d p1_prime_strict=%d p2_prime=%d p2_prime_strict=%d' % (
        counts['p1_prime_count'], counts['p1_prime_strict_count'], counts['p2_prime_count'], counts['p2_prime_strict_count']))
    print('p3_prime max=%s mean=%s holds=%s' % (p3['max_score_prime'], p3['mean_score_prime'], p3['holds_prime']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
