#!/usr/bin/env python3
"""
W8 — THE REVISER'S BLIND SIDE, phase 3: analysis (offline, no network).

Holder vectors are W7-on-record, pre-stated in REGISTRATION.md.
P1: baseline holder-cell destruction rate (Wilson 95% CI) + breakdowns.
P2a: logistic destroyed ~ carrier_edit_distance over ALL regimes' holder
     cells; Newton-Raphson MLE in pure numpy (scipy used only if importable).
P2b: baseline vs verify_then_fix destruction (Wilson CIs, relative
     reduction, CI separation) + repair-rate absolute loss (points).
Plus p_destroy/p_spare by (reviser, constraint) over nonholder cells (W10).
"""
import json, math
import numpy as np

CONSTRAINTS = ['12_lines', 'c1_growth', 'c2_acrostic', 'c3_seal', 'c4_no_rhyme',
               'c5_last_word_unique', 'c6_punctuation']
HOLDERS = {
    'claude': {'12_lines', 'c1_growth', 'c3_seal', 'c5_last_word_unique'},
    'kimi': {'12_lines', 'c3_seal', 'c4_no_rhyme', 'c5_last_word_unique'},
    'flash': {'12_lines', 'c5_last_word_unique'},
    'wesley': {'12_lines', 'c5_last_word_unique'},
}
Z95 = 1.959963984540054

try:
    from scipy.stats import norm as _sp_norm
except Exception:
    _sp_norm = None

def wilson(k, n):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1.0 + Z95 * Z95 / n
    c = (p + Z95 * Z95 / (2 * n)) / d
    h = Z95 * math.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / d
    return [c - h, c + h]

def _sf(x):
    if _sp_norm is not None:
        return float(_sp_norm.sf(x))
    return 0.5 * math.erfc(x / math.sqrt(2.0))

def rate(cells, key):
    n = len(cells)
    k = sum(1 for c in cells if c[key])
    lo, hi = wilson(k, n)
    return {'n': n, 'k': k, 'p': (k / n) if n else None, 'wilson95': [lo, hi]}

def logit_nr(X, y):
    beta = np.zeros(X.shape[1])
    for _ in range(200):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        W = mu * (1.0 - mu)
        H = X.T @ (X * W[:, None]) + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - mu))
        beta = beta + step
        if np.max(np.abs(step)) < 1e-10:
            break
    return beta

def fit_logistic(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) < 3 or np.ptp(x) == 0.0 or len(set(y.tolist())) < 2:
        return {'error': 'degenerate (n<3, constant distance, or no variation in outcome)'}
    X = np.column_stack([np.ones(len(x)), x])
    beta = logit_nr(X, y)
    eta = X @ beta
    mu = 1.0 / (1.0 + np.exp(-eta))
    W = mu * (1.0 - mu)
    cov = np.linalg.inv(X.T @ (X * W[:, None]) + 1e-9 * np.eye(X.shape[1]))
    slope = float(beta[1])
    se = float(math.sqrt(cov[1, 1]))
    z = slope / se if se > 0 else float('inf')
    return {'slope': slope, 'se': se, 'wald_z': float(z), 'p_value': 2.0 * _sf(abs(z)),
            'intercept': float(beta[0]), 'n': int(len(x)),
            'p_engine': 'scipy.stats.norm' if _sp_norm is not None else 'math.erfc'}

def build_cells(revisions, seed_pass):
    cells = []
    for rev in revisions:
        if 'error' in rev or 'rev_check' not in rev:
            continue
        for c in CONSTRAINTS:
            sp = bool(seed_pass.get(rev['seed_id'], {}).get(c))
            rp = bool(rev['rev_check'].get(c))
            holds = c in HOLDERS.get(rev['reviser'], set())
            ctype = 'repair' if not sp else ('holder' if holds else 'nonholder')
            cells.append({'seed_id': rev['seed_id'], 'reviser': rev['reviser'],
                          'regime': rev['regime'], 'constraint': c, 'cell_type': ctype,
                          'seed_pass': sp, 'rev_pass': rp,
                          'destroyed': sp and not rp, 'repaired': (not sp) and rp,
                          'carrier_edit_distance': rev.get('constraint_report', {})
                          .get(c, {}).get('carrier_edit_distance')})
    return cells

def main():
    seeds = json.load(open('w8-seeds.json'))
    seed_pass = seeds['seed_pass']
    revisions = [json.loads(l) for l in open('w8-revisions.jsonl') if l.strip()]
    n_err = sum(1 for r in revisions if 'error' in r or 'rev_check' not in r)
    cells = build_cells(revisions, seed_pass)
    revisers = sorted({c['reviser'] for c in cells})

    base_h = [c for c in cells if c['regime'] == 'baseline' and c['cell_type'] == 'holder']
    p1 = {'overall': rate(base_h, 'destroyed'),
          'by_reviser': {r: rate([c for c in base_h if c['reviser'] == r], 'destroyed') for r in revisers},
          'by_constraint': {cn: rate([c for c in base_h if c['constraint'] == cn], 'destroyed') for cn in CONSTRAINTS}}

    h_all = [c for c in cells if c['cell_type'] == 'holder' and c['carrier_edit_distance'] is not None]
    p2a = fit_logistic([c['carrier_edit_distance'] for c in h_all],
                       [1 if c['destroyed'] else 0 for c in h_all])

    vtf_h = [c for c in cells if c['regime'] == 'verify_then_fix' and c['cell_type'] == 'holder']
    b, v = rate(base_h, 'destroyed'), rate(vtf_h, 'destroyed')
    b_r = rate([c for c in cells if c['regime'] == 'baseline' and c['cell_type'] == 'repair'], 'repaired')
    v_r = rate([c for c in cells if c['regime'] == 'verify_then_fix' and c['cell_type'] == 'repair'], 'repaired')
    rel = ((b['p'] - v['p']) / b['p']) if (b['p'] not in (None, 0) and v['p'] is not None) else None
    sep = None
    if b['wilson95'][0] is not None and v['wilson95'][0] is not None:
        sep = b['wilson95'][0] > v['wilson95'][1] or v['wilson95'][0] > b['wilson95'][1]
    p2b = {'baseline': b, 'verify_then_fix': v, 'relative_reduction': rel,
           'wilson_ci_separated': sep,
           'repair_rate_baseline': b_r, 'repair_rate_vtf': v_r,
           'repair_rate_abs_loss': (b_r['p'] - v_r['p'])
           if (b_r['p'] is not None and v_r['p'] is not None) else None}

    nh = {}
    for c in cells:
        if c['cell_type'] != 'nonholder':
            continue
        key = c['reviser'] + '|' + c['constraint']
        d = nh.setdefault(key, {'n': 0, 'destroyed': 0})
        d['n'] += 1
        d['destroyed'] += 1 if c['destroyed'] else 0
    for d in nh.values():
        d['p_destroy'] = d['destroyed'] / d['n'] if d['n'] else None
        d['p_spare'] = 1.0 - d['p_destroy'] if d['p_destroy'] is not None else None

    out = {'n_revisions': len(revisions), 'n_error_cells': n_err, 'p1': p1, 'p2a': p2a,
           'p2b': p2b, 'nonholder_table': nh, 'cells': cells}
    json.dump(out, open('w8-analysis.json', 'w'), indent=2)

    def fmt(r):
        return '%d/%d = %s CI %s' % (r['k'], r['n'],
                                     'NA' if r['p'] is None else round(r['p'], 3),
                                     [None if x is None else round(x, 3) for x in r['wilson95']])
    print('P1 baseline holder-cell destruction:', fmt(p1['overall']))
    for r in revisers:
        print('  reviser %-7s' % r, fmt(p1['by_reviser'][r]))
    for c in CONSTRAINTS:
        print('  constr  %-20s' % c, fmt(p1['by_constraint'][c]))
    print('P2a logistic destroyed~dist:', p2a)
    print('P2b baseline :', fmt(b))
    print('P2b vtf      :', fmt(v))
    print('P2b relative_reduction:', rel, '| CI separated:', sep)
    print('P2b repair-rate baseline %.3f vs vtf %.3f | abs loss %s' %
          (b_r['p'] or 0, v_r['p'] or 0, p2b['repair_rate_abs_loss']))
    print('nonholder p_destroy (for W10):')
    for k in sorted(nh):
        print('  %-28s p_destroy=%.3f (n=%d)' % (k, nh[k]['p_destroy'], nh[k]['n']))
    print('saved w8-analysis.json')

if __name__ == '__main__':
    main()
