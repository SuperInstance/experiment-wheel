import json
import os
import sys

import re
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


ACROSTIC = 'THEEILEENLAUN'
CONSTRAINTS = ('c1_growth', 'c2_acrostic', 'c3_seal', 'c4_no_rhyme', 'c5_last_word_unique', 'c6_punctuation')


def extract_lines(poem):
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    return [l for l in lines if not l.startswith('#') and not l.startswith('```')]


def qualifies(n, line):
    return len(line.split()) == n and line[0].upper() == ACROSTIC[n - 1]


def local_score(c):
    return int(c['c1_growth']) + int(c['c2_acrostic'])


def global_score(c):
    return int(c['c3_seal']) + int(c['c4_no_rhyme']) + int(c['c5_last_word_unique']) + int(c['c6_punctuation'])


def rank_key(p):
    return (-p['score'], p['k'])


def fuse(parents):
    ranked = sorted(parents, key=rank_key)
    extracted = {p['k']: extract_lines(p['poem']) for p in ranked}
    lines_out = []
    provenance = []
    for n in range(1, 13):
        donor = None
        chosen = None
        qualified = False
        for p in ranked:
            cand = extracted[p['k']][n - 1]
            if qualifies(n, cand):
                donor = p
                chosen = cand
                qualified = True
                break
        if donor is None:
            donor = ranked[0]
            chosen = extracted[donor['k']][n - 1]
            qualified = False
        lines_out.append(chosen)
        provenance.append({'n': n, 'source_k': donor['k'], 'qualified': qualified, 'line': chosen})
    return '\n'.join(lines_out), provenance


def self_test():
    poem = '\n'.join([
        'Time',
        'Hollow rivers',
        'Emerald tides drift',
        'Evening holds 8721b4bd042a close',
        'Islands rise from quiet mists',
        'Lanterns flicker above the calm, bay',
        'Echoes wander where the soft winds',
        'Each season turns the old hills toward dusk',
        'Northern lights bend above the frozen lake at midnight',
        'Long shadows stretch across the valley while stars awaken slowly',
        'Amber dusk settles over rooftops as the harbor lights begin glowing',
        'Under bright mornings the village children chase silver kites until dusk falls.',
    ])
    c = check(poem)
    try:
        assert c['score'] == 7 and all(c[k] for k in CONSTRAINTS)
    except AssertionError:
        failed = [k for k in CONSTRAINTS if not c[k]]
        print('SELF-TEST FAILED: check() on all-six-constraints synthetic poem: score=%d (want 7); failed constraints: %s; full check: %s' % (c['score'], failed, c), file=sys.stderr)
        sys.exit(2)

    def toy_parent(k, score, line3, line12):
        body = [
            'one',
            'two two',
            line3,
            'four four four four',
            'five five five five five',
            'six six six six six six',
            'seven seven seven seven seven seven seven',
            'eight eight eight eight eight eight eight eight',
            'nine nine nine nine nine nine nine nine nine',
            'ten ten ten ten ten ten ten ten ten ten',
            'eleven eleven eleven eleven eleven eleven eleven eleven eleven eleven',
            line12,
        ]
        return {'k': k, 'poem': '\n'.join(body), 'score': score}

    pa = toy_parent(1, 6, 'Emerald tides drift', 'Ll m n o p q r s t u v')
    pb = toy_parent(2, 4, 'three three three', 'Zz a b c d e f g h i j k')
    fused, prov = fuse([pa, pb])
    try:
        assert prov[2]['source_k'] == 1 and prov[2]['qualified'] is True and prov[2]['line'] == 'Emerald tides drift'
        assert prov[11]['source_k'] == 1 and prov[11]['qualified'] is False and prov[11]['line'] == 'Ll m n o p q r s t u v'
        assert fused.split('\n')[2] == 'Emerald tides drift' and fused.split('\n')[11] == 'Ll m n o p q r s t u v'
    except AssertionError:
        print('SELF-TEST FAILED: fuse() two-parent toy case: provenance=%s' % prov, file=sys.stderr)
        sys.exit(2)


def main():
    self_test()

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'w11-braids.json'), encoding='utf-8') as f:
        data = json.load(f)

    solo = data.get('solo', {})
    braids = data['braids']
    braid_scores_stored = data.get('braid_scores')
    best_solo_stored = data.get('best_solo')

    solo_summary = {}
    for yard in solo:
        entry = solo[yard]
        rc = check(entry['poem'])
        solo_summary[yard] = {
            'recomputed_check': rc,
            'stored_check': entry.get('check'),
            'mismatch': entry.get('check') != rc,
        }

    parents = []
    braid_summary = []
    for b in braids:
        rc = check(b['poem'])
        abstains = len(extract_lines(b['poem'])) != 12
        parents.append({'k': b['k'], 'poem': b['poem'], 'score': rc['score'], 'check': rc, 'abstains': abstains})
        has_stored = isinstance(braid_scores_stored, list) and 1 <= b['k'] <= len(braid_scores_stored)
        braid_summary.append({
            'k': b['k'],
            'recomputed_score': rc['score'],
            'recomputed_local': local_score(rc),
            'recomputed_global': global_score(rc),
            'abstains': abstains,
            'stored_check': b.get('check'),
            'check_matches_stored': b.get('check') == rc,
            'stored_braid_scores_entry': braid_scores_stored[b['k'] - 1] if has_stored else None,
            'braid_scores_matches_recomputed': (braid_scores_stored[b['k'] - 1] == rc['score']) if has_stored else None,
        })

    standing = [p for p in parents if not p['abstains']]
    ranked = sorted(standing, key=rank_key)
    selection = ranked[0]

    fused5, prov5 = fuse(standing)
    fused5_check = check(fused5)

    loo = []
    for held_out in range(1, 6):
        four = [p for p in standing if p['k'] != held_out]
        fused, prov = fuse(four)
        fc = check(fused)
        fl = local_score(fc)
        fg = global_score(fc)
        fallbacks = sum(1 for pr in prov if not pr['qualified'])
        bp = sorted(four, key=rank_key)[0]
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
        loo.append({
            'held_out': held_out,
            'parent_scores': {p['k']: p['score'] for p in four},
            'fused_poem': fused,
            'fused_check': fc,
            'fusion_score': fc['score'],
            'fusion_local': fl,
            'fusion_global': fg,
            'provenance': prov,
            'fallbacks': fallbacks,
            'best_parent_k': bp['k'],
            'parent_local': pl,
            'parent_global': pg,
            'p1': p1,
            'p1_strict': p1_strict,
            'p2': p2,
            'p2_strict': p2_strict,
            'constraint_deltas': deltas,
        })

    counts = {
        'p1_count': sum(1 for r in loo if r['p1']),
        'p1_strict_count': sum(1 for r in loo if r['p1_strict']),
        'p2_count': sum(1 for r in loo if r['p2']),
        'p2_strict_count': sum(1 for r in loo if r['p2_strict']),
    }

    five_scores = [p['score'] for p in parents]
    max_score = max(five_scores)
    mean_score = sum(five_scores) / len(five_scores)
    p3 = {'max_score': max_score, 'mean_score': mean_score, 'holds': max_score >= mean_score + 1}

    results = {
        'input': {
            'solo': solo_summary,
            'braids': braid_summary,
            'braid_scores_stored': braid_scores_stored,
            'best_solo_stored': best_solo_stored,
        },
        'selection': {'k': selection['k'], 'score': selection['score'], 'poem': selection['poem']},
        'fusion_all5': {
            'poem': fused5,
            'check': fused5_check,
            'local': local_score(fused5_check),
            'global': global_score(fused5_check),
            'provenance': prov5,
            'fallbacks': sum(1 for pr in prov5 if not pr['qualified']),
        },
        'loo': loo,
        'counts': counts,
        'p3': p3,
    }

    with open(os.path.join(here, 'w11-results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        f.write('\n')

    for r in loo:
        print('LOO held_out=%d parent_scores=%s best_parent(k=%d local=%d global=%d) fusion(score=%d local=%d global=%d) p1=%s p2=%s' % (
            r['held_out'], r['parent_scores'], r['best_parent_k'], r['parent_local'], r['parent_global'],
            r['fusion_score'], r['fusion_local'], r['fusion_global'], r['p1'], r['p2']))
    print('counts p1=%d p1_strict=%d p2=%d p2_strict=%d' % (
        counts['p1_count'], counts['p1_strict_count'], counts['p2_count'], counts['p2_strict_count']))
    print('p3 max=%s mean=%s holds=%s' % (p3['max_score'], p3['mean_score'], p3['holds']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
