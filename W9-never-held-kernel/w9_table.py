#!/usr/bin/env python3
"""W9 wall-table builder v2 — c2/c6 verbatim (impossibility columns) + c2'/c6' fair cells.
Excludes yard_down entries. Zero model calls."""
import glob, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w9_check import check, c2_amended, c6_amended

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'ledgers')

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, max(0.0, (c - h) / d), min(1.0, (c + h) / d))

def cells(d):
    """Return dict of kernel cells for a draw record (recompute c6' for pre-amendment ledgers)."""
    c = d.get('check', {})
    return {'c2': c.get('c2_acrostic'), 'c6': c.get('c6_punctuation'),
            'c2p': d.get('c2_amended', c2_amended(d['poem']) if 'poem' in d else None),
            'c6p': d.get('c6_amended', c6_amended(d['poem']) if 'poem' in d else None)}

def live(ds):
    return [d for d in ds if 'check' in d and not d.get('yard_down')]

def rate(ds, cell):
    n = len(ds)
    k = sum(1 for d in ds if cells(d).get(cell))
    return k, n

def fmt(k, n, bar=None):
    if n == 0: return '—'
    p, lo, hi = wilson(k, n)
    s = f'{k}/{n} ({p*100:.0f}%)'
    if bar == 'any': s += ' ANY' if k else ''
    if bar == 'maj': s += (' **MAJ**' if 2 * k > n else '')
    return s

out = ['# W9 WALL-TABLE — THE NEVER-HELD KERNEL (all four shapes, sealed protocol)',
       '',
       '*Verbatim c2/c6 = the W6b/W7 checker\'s cells — both proven unsatisfiable by',
       'construction (c2: 13-letter acrostic vs 12 lines; c6: the checker demands the',
       'punctuation multiset sorted dot-first, but ASCII 0x2C < 0x2E forces comma-first).',
       'They are reported as impossibility columns. c2\' (THEEILEENLAU, 12 letters) and c6\' (one comma + one',
       'period, correct sort) are the pre-registered / sealed-amendment FAIR cells. Mind-only',
       '= holds/draws. Fleet-selected = any-hold within a yard\'s N draws (instrument).',
       'claude cells after its session-limit hit (sh3 c2 P3, all sh4) are yard-down, excluded.*',
       '']

# ---------- SH-1 ----------
out += ['## SH-1 — ensemble N=16, verbatim task (64 draws)', '',
        '| yard | draws | mean | c2 (imp.) | c2\' | c6 (imp.) | c6\' |',
        '|---|---|---|---|---|---|---|']
s1 = {}
for f in sorted(glob.glob(os.path.join(L, 'sh1-*.json'))):
    led = json.load(open(f)); ds = live(led.get('draws', [])); s1[led['yard']] = ds
    mean = sum(d['check']['score'] for d in ds) / len(ds) if ds else 0
    out.append(f"| {led['yard']} | {len(ds)} | {mean:.2f} | {fmt(*rate(ds,'c2'))} | "
               f"{fmt(*rate(ds,'c2p'),'maj')} | {fmt(*rate(ds,'c6'))} | {fmt(*rate(ds,'c6p'),'maj')} |")
pool = [d for y in s1.values() for d in y]
out += ['', f'SH-1 pooled: {len(pool)} draws · ' + ' · '.join(
    f'{c}: {rate(pool, cc)[0]}/{len(pool)}' for c, cc in (('c2','c2'),('c2\'','c2p'),('c6','c6'),('c6\'','c6p')))]
vec = {k: sum(1 for d in pool if d['check'].get(k)) for k in
       ('12_lines','c1_growth','c3_seal','c4_no_rhyme','c5_last_word_unique')}
out += [f'SH-1 context (pooled holds): {vec}', '',
        'Fleet-selected (any-hold best-of-16 per yard): c2\' ANY: ' +
        ', '.join(f'{y} {rate(ds,"c2p")[0]>0}' for y, ds in s1.items()) + ' · c6\' ANY: ' +
        ', '.join(f'{y} {rate(ds,"c6p")[0]>0}' for y, ds in s1.items()), '']

# ---------- SH-2 ----------
out += ['## SH-2 — worksheet scaffold (16 draws)', '',
        '| yard | draws | mean | c2 (imp.) | c2\' | c6 (imp.) | c6\' |',
        '|---|---|---|---|---|---|---|']
s2 = {}
for f in sorted(glob.glob(os.path.join(L, 'sh2-*.json'))):
    led = json.load(open(f)); ds = live(led.get('draws', [])); s2[led['yard']] = ds
    mean = sum(d['check']['score'] for d in ds) / len(ds) if ds else 0
    out.append(f"| {led['yard']} | {len(ds)} | {mean:.2f} | {fmt(*rate(ds,'c2'))} | "
               f"{fmt(*rate(ds,'c2p'),'maj')} | {fmt(*rate(ds,'c6'))} | {fmt(*rate(ds,'c6p'),'maj')} |")
pool2 = [d for y in s2.values() for d in y]
out += ['', f'SH-2 pooled: {len(pool2)} draws · ' + ' · '.join(
    f'{c}: {rate(pool2, cc)[0]}/{len(pool2)}' for c, cc in (('c2','c2'),('c2\'','c2p'),('c6','c6'),('c6\'','c6p'))), '']

# ---------- SH-3 ----------
out += ['## SH-3 — attorney decomposition (chains: P1 content → P2 letters/counts → P3 formatting)', '',
        'Per-pass kernel cells (live passes only):', '']
s3_rows = []
for f in sorted(glob.glob(os.path.join(L, 'sh3-*.json'))):
    led = json.load(open(f))
    for ch in led.get('chains', []):
        cellsx = {'yard': led['yard'], 'chain': ch['chain'], 'passes': []}
        for p in ch['passes']:
            if p.get('yard_down'):
                cellsx['passes'].append((p['pass'], 'YARD-DOWN'))
            elif 'skipped' in p:
                cellsx['passes'].append((p['pass'], 'skipped'))
            else:
                cl = cells(p)
                cellsx['passes'].append((p['pass'],
                    f"{p['check']['score']}/6 c2'{int(bool(cl['c2p']))} c6'{int(bool(cl['c6p']))}"))
        s3_rows.append(cellsx)
for r in s3_rows:
    out.append(f"- **{r['yard']}** chain {r['chain']}: " + ' → '.join(f'{n}: {v}' for n, v in r['passes']))
p3_live = []
for f in sorted(glob.glob(os.path.join(L, 'sh3-*.json'))):
    led = json.load(open(f))
    for ch in led.get('chains', []):
        for p in ch['passes']:
            if p.get('pass') == 'P3_formatting' and 'check' in p and not p.get('yard_down'):
                p3_live.append(p)
out += ['', f"P3 formatting passes (live): {len(p3_live)} · c6' held {sum(1 for p in p3_live if cells(p)['c6p'])}/{len(p3_live)}"
        f" · c2' carried into finals {sum(1 for p in p3_live if cells(p)['c2p'])}/{len(p3_live)}", '']

# ---------- SH-4 ----------
out += ['## SH-4 — c6 minimal-fix (seed: best c6\'-failing SH-1 draw, 4/6, committed)', '',
        '| yard | draws | c6\' fixed | c2\' gained/kept | score deltas | notes |',
        '|---|---|---|---|---|---|']
for f in sorted(glob.glob(os.path.join(L, 'sh4-*.json'))):
    led = json.load(open(f)); ds = live(led.get('draws', [])); allb = led.get('draws', [])
    note = 'yard-down: session limit' if len(ds) < len(allb) else ''
    if ds:
        fixed = sum(1 for d in ds if d.get('c6p_after'))
        kept = sum(1 for d in ds if d.get('c2p_after'))
        deltas = [d.get('score_delta') for d in ds]
        out.append(f"| {led['yard']} | {len(ds)} | {fixed}/{len(ds)} | {kept}/{len(ds)} | {deltas} | {note} |")
    else:
        out.append(f"| {led['yard']} | 0 | — | — | — | {note or 'no live draws'} |")
out += ['', 'Seed: 4/6 verbatim {12L, c3, c4, c5}, c2\'=False, c6\'=False (an SH-1 draw). '
        'opencode fixed c6\' 4/4 and GAINED c2\' (4→5/6); flash 1/4 (that draw gained c2\' too, '
        'a full satisfiable board); kimi 0/4 (structure kept, punctuation unfixed); claude '
        'yard-down (session limit).', '']

# ---------- pooled kernel arithmetic ----------
out += ['## Pooled kernel arithmetic (fair cells)', '']
scope = pool + pool2 + p3_live  # c2'-scoped attempts per registration: SH-1 + SH-2 + SH-3 finals
k2p, n2p = rate(scope, 'c2p')
_, lo, hi = wilson(k2p, n2p)
out += [f"- c2' scoped attempts {n2p} (SH-1 64 + SH-2 16 + SH-3 finals {len(p3_live)}) · holds {k2p} "
        f"· Wilson 95% CI [{lo:.3f}, {hi:.3f}] · rate-of-three upper {300/n2p:.1f}%"]
sh4_live = []
for f in sorted(glob.glob(os.path.join(L, 'sh4-*.json'))):
    led = json.load(open(f))
    sh4_live += live(led.get('draws', []))
c6scope = pool + pool2 + p3_live + sh4_live
k6p, n6p = rate(c6scope, 'c6p')
_, lo6, hi6 = wilson(k6p, n6p)
out += [f"- c6' all-shape scoped attempts {n6p} · holds {k6p} · Wilson 95% CI [{lo6:.3f}, {hi6:.3f}]"]
out += [f"- verbatim c2 and c6: 0/{n2p} and 0/{n6p} — as dictated by impossibility (instrument columns).", '']

open(os.path.join(HERE, 'WALL-TABLE.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
