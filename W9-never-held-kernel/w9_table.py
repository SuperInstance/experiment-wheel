#!/usr/bin/env python3
"""W9 wall-table builder — reads ledgers, emits WALL-TABLE.md. Zero model calls."""
import glob, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'ledgers')
CELLS = ('c2_acrostic', 'c6_punctuation')  # verbatim kernel cells
KEY = {'c2_acrostic': 'c2', 'c6_punctuation': 'c6', 'c2p': "c2'"}

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, max(0.0, (c - h) / d), min(1.0, (c + h) / d))

def hold(d, cell):
    if 'check' not in d: return None
    if cell == 'c2p': return bool(d.get('c2_amended'))
    return bool(d['check'].get(cell))

def sh1_stats():
    rows = []
    for f in sorted(glob.glob(os.path.join(L, 'sh1-*.json'))):
        led = json.load(open(f)); yard = led['yard']; ds = led.get('draws', [])
        n = sum(1 for d in ds if 'check' in d)
        row = {'yard': yard, 'n': n, 'fail': len(ds) - n, 'cells': {}, 'mean_score': None}
        if n:
            row['mean_score'] = round(sum(d['check']['score'] for d in ds) / n, 2)
            for cell in CELLS + ('c2p',):
                ks = [hold(d, cell) for d in ds]
                k = sum(1 for x in ks if x)
                row['cells'][KEY[cell]] = {'k': k, 'n': n, 'rate': round(k / n, 3),
                                           'any': k > 0, 'majority': k * 2 > n,
                                           'wilson': tuple(round(x, 3) for x in wilson(k, n))}
            # full vector for context
            row['vector'] = {kk: sum(1 for d in ds if d['check'].get(kk)) for kk in
                             ('12_lines', 'c1_growth', 'c2_acrostic', 'c3_seal', 'c4_no_rhyme',
                              'c5_last_word_unique', 'c6_punctuation')}
        rows.append(row)
    return rows

def sh2_stats():
    rows = []
    for f in sorted(glob.glob(os.path.join(L, 'sh2-*.json'))):
        led = json.load(open(f)); ds = led.get('draws', [])
        n = sum(1 for d in ds if 'check' in d)
        row = {'yard': led['yard'], 'n': n, 'fail': len(ds) - n, 'cells': {}}
        if n:
            for cell in CELLS + ('c2p',):
                k = sum(1 for d in ds if hold(d, cell))
                row['cells'][KEY[cell]] = {'k': k, 'n': n, 'rate': round(k / n, 3), 'any': k > 0,
                                           'wilson': tuple(round(x, 3) for x in wilson(k, n))}
        rows.append(row)
    return rows

def sh3_stats():
    rows = []
    for f in sorted(glob.glob(os.path.join(L, 'sh3-*.json'))):
        led = json.load(open(f))
        row = {'yard': led['yard'], 'chains': []}
        for ch in led.get('chains', []):
            entry = {'chain': ch['chain'], 'passes': []}
            final = None
            for p in ch['passes']:
                if 'skipped' in p:
                    entry['passes'].append({'pass': p['pass'], 'skipped': p['skipped']})
                else:
                    c = {'pass': p['pass'], 'score': p['check']['score'],
                         'c2': p['check'].get('c2_acrostic'), "c2'": p.get('c2_amended'),
                         'c6': p['check'].get('c6_punctuation')}
                    entry['passes'].append(c)
                    if p['pass'] == 'P3_formatting': final = c
            entry['final'] = final
            row['chains'].append(entry)
        rows.append(row)
    return rows

def sh4_stats():
    rows = []
    for f in sorted(glob.glob(os.path.join(L, 'sh4-*.json'))):
        led = json.load(open(f))
        ds = led.get('draws', [])
        n = sum(1 for d in ds if 'check' in d)
        row = {'yard': led['yard'], 'seed_source': led.get('seed_source'),
               'seed_score': led.get('seed_check', {}).get('score'),
               'n': n, 'fail': len(ds) - n,
               'c6_holds': sum(1 for d in ds if d.get('c6_after')),
               'deltas': [d.get('score_delta') for d in ds if 'check' in d]}
        rows.append(row)
    return rows

def md():
    s1, s2, s3, s4 = sh1_stats(), sh2_stats(), sh3_stats(), sh4_stats()
    out = ['# W9 WALL-TABLE — per shape × per mind × kernel cells\n',
           '*Mind-only = holds/draws (headline). Fleet-selected = any-hold within the',
           "yard's N draws (checker-picked best-of-N; W1 selector precedent; flagged as",
           'instrument). c2 = verbatim cell (unsatisfiable by construction — see audit).',
           "c2' = amended fleet-side cell (THEEILEENLAU).*\n"]
    out.append('## SH-1 — ensemble N=16 (verbatim task)\n')
    out.append('| yard | draws | fail | mean score | c2 k/n (any/maj) | c6 k/n (any/maj) | c2\' k/n (any/maj) |')
    out.append('|---|---|---|---|---|---|---|')
    for r in s1:
        c = r['cells'] if r['n'] else {}
        def fmt(x):
            if not c or x not in c: return '—'
            e = c[x]; maj = '/maj' if e.get('majority') else ''
            return f"{e['k']}/{e['n']} ({'ANY' if e['any'] else '—'}{maj})"
        out.append(f"| {r['yard']} | {r['n']} | {r['fail']} | {r.get('mean_score','—')} | "
                   f"{fmt('c2')} | {fmt('c6')} | {fmt(\"c2'\")} |")
    # SH-1 pooled
    alld = []
    for f in glob.glob(os.path.join(L, 'sh1-*.json')):
        alld += [d for d in json.load(open(f)).get('draws', []) if 'check' in d]
    if alld:
        out.append(f'\nSH-1 pooled: {len(alld)} draws · ' + ' · '.join(
            f"{k}: {sum(1 for d in alld if hold(d, cell))}/{len(alld)}"
            for cell, k in (('c2_acrostic','c2'), ('c6_punctuation','c6'), ('c2p',"c2'"))))
    out.append('\nSH-1 context vectors (holds/yard of 16): ' +
               '; '.join(f"{r['yard']}: {r.get('vector')}" for r in s1 if r.get('vector')) + '\n')
    out.append('## SH-2 — worksheet scaffold\n')
    out.append('| yard | draws | fail | c2 k/n | c6 k/n | c2\' k/n |')
    out.append('|---|---|---|---|---|---|')
    for r in s2:
        c = r['cells'] if r['n'] else {}
        def fmt2(x):
            if not c or x not in c: return '—'
            e = c[x]; return f"{e['k']}/{e['n']}"
        out.append(f"| {r['yard']} | {r['n']} | {r['fail']} | {fmt2('c2')} | {fmt2('c6')} | {fmt2(\"c2'\")} |")
    all2 = []
    for f in glob.glob(os.path.join(L, 'sh2-*.json')):
        all2 += [d for d in json.load(open(f)).get('draws', []) if 'check' in d]
    if all2:
        out.append(f"\nSH-2 pooled: {len(all2)} draws · " + ' · '.join(
            f"{k}: {sum(1 for d in all2 if hold(d, cell))}/{len(all2)}"
            for cell, k in (('c2_acrostic','c2'), ('c6_punctuation','c6'), ('c2p',"c2'"))) + '\n')
    out.append('## SH-3 — attorney decomposition (chains; final = composite cell)\n')
    for r in s3:
        for ch in r['chains']:
            ps = ' -> '.join(f"{p.get('pass','?').split('_')[0]}:" +
                             (f"{p.get('score','skip')}/{p.get('c2','-')}/{p.get(chr(99)+chr(50)+chr(39),'-')}/{p.get('c6','-')}"
                              if 'skipped' not in p else 'skipped') for p in ch['passes'])
            out.append(f"- {r['yard']} chain {ch['chain']}: {ps}  (format score/c2/c2\\'/c6)")
    out.append('')
    out.append('## SH-4 — c6 minimal-fix (seed from committed SH-1/W7 record)\n')
    out.append('| yard | seed | draws | c6 holds | score deltas |')
    out.append('|---|---|---|---|---|')
    for r in s4:
        out.append(f"| {r['yard']} | {r.get('seed_source')} ({r.get('seed_score')}/6) | {r['n']} (+{r['fail']} fail) | "
                   f"{r['c6_holds']}/{r['n']} | {r['deltas']} |")
    # pooled kernel math
    out.append('\n## Pooled kernel arithmetic\n')
    c2p_pool = []
    for pat, filt in (('sh1-*', lambda d: True), ('sh2-*', lambda d: True)):
        for f in glob.glob(os.path.join(L, pat)):
            c2p_pool += [d for d in json.load(open(f)).get('draws', []) if 'check' in d and filt(d)]
    for f in glob.glob(os.path.join(L, 'sh3-*.json')):
        for ch in json.load(open(f)).get('chains', []):
            for p in ch['passes']:
                if 'pass' in p and 'check' in p and p['pass'] == 'P3_formatting':
                    c2p_pool.append(p)
    k2p = sum(1 for d in c2p_pool if hold(d, 'c2p'))
    n2p = len(c2p_pool)
    p, lo, hi = wilson(k2p, n2p)
    ru3 = round(3 / n2p, 4) if n2p else None
    out.append(f"- c2' scoped attempts: {n2p} (SH-1 draws + SH-2 draws + SH-3 finals) · holds {k2p} · "
               f"Wilson 95% CI [{lo:.3f}, {hi:.3f}] · rule-of-three upper {ru3*100:.1f}%" if n2p else "- c2': no data yet")
    c6pool = []
    for pat in ('sh1-*', 'sh2-*'):
        for f in glob.glob(os.path.join(L, pat)):
            c6pool += [d for d in json.load(open(f)).get('draws', []) if 'check' in d]
    for f in glob.glob(os.path.join(L, 'sh3-*.json')):
        for ch in json.load(open(f)).get('chains', []):
            for p in ch['passes']:
                if 'pass' in p and 'check' in p and p['pass'] == 'P3_formatting':
                    c6pool.append(p)
    for f in glob.glob(os.path.join(L, 'sh4-*.json')):
        c6pool += [d for d in json.load(open(f)).get('draws', []) if 'check' in d]
    k6 = sum(1 for d in c6pool if hold(d, 'c6_punctuation')); n6 = len(c6pool)
    if n6:
        p6, lo6, hi6 = wilson(k6, n6)
        out.append(f"- c6 all-shape scoped attempts: {n6} · holds {k6} · Wilson 95% CI [{lo6:.3f}, {hi6:.3f}]")
    open(os.path.join(HERE, 'WALL-TABLE.md'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))

if __name__ == '__main__':
    md()
