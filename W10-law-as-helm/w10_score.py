#!/usr/bin/env python3
"""
W10 — LAW AS HELM, scorer.

Scores the sealed w10-predictions.json ({tag: {L1: {cell: bool}, L4:
{cell: bool}}}) against each chain's final verbatim check(), per chain
and pooled over the seven check cells; CH-C must reproduce the
intersection floor exactly (reproduction control). The frozen
algorithms predict_L1 (intersection) and predict_L4 (last-holder-
spare forward simulation, sealed non-holder rulings) are re-run from
the measured phase-0 hold-sets — any disagreement with the sealed
file is flagged, never silently repaired. Writes w10-verdict-data.json.

--selftest: replay W7 artifacts through the ported check() (0
mismatches required) and assert the frozen simulation on W7's
published hold-sets for ASC/DESC.
"""
import argparse, json, os
from w10_lib import check, CONSTRAINTS, hold_set

HERE = os.path.dirname(os.path.abspath(__file__))
W7_RESULTS = os.path.join(HERE, '..', 'W7-ordered-braid', 'w7-results.json')
W8_ANALYSIS = os.path.join(HERE, '..', 'W8-reviser-blind-side', 'w8-analysis.json')

W7_HOLDS = {
    'claude': {'12_lines', 'c1_growth', 'c3_seal', 'c5_last_word_unique'},
    'kimi': {'12_lines', 'c3_seal', 'c4_no_rhyme', 'c5_last_word_unique'},
    'flash': {'12_lines', 'c5_last_word_unique'},
    'wesley': {'12_lines', 'c5_last_word_unique'},
}

# REGISTRATION.md's frozen rule applied to W8's five measured non-holder
# cells: spare iff p_spare >= 0.5 (wesley|c4 0.50 SPARES per the explicit
# note; flash|c4 0.67 SPARES — corrected 2026-08-27: opencode's initial
# port carried an unauthorized destroy override on flash|c4 to force the
# CH-C floor; the sealed rule wins over the CH-C expectation, and the
# consequence is accepted: L4's frozen rule predicts c4 surviving W7-DESC
# where the floor was observed — an honest pre-stated L4 cell risk)
SEALED_NONHOLDER = {
    'claude|c4_no_rhyme': True,
    'flash|c3_seal': False,
    'flash|c4_no_rhyme': True,
    'wesley|c3_seal': False,
    'wesley|c4_no_rhyme': True,
}

def csort(cells):
    return [c for c in CONSTRAINTS if c in cells]

def predict_L1(order, holds):
    # L1, all-touch relevance: the intersection of every hand's solo hold-set
    out = None
    for h in order:
        s = set(holds.get(h, set()))
        out = s if out is None else out & s
    return out if out is not None else set()

def _spares(hand, cell, p_table):
    ruling = SEALED_NONHOLDER.get(hand + '|' + cell)
    if ruling is not None:
        return ruling
    m = p_table.get(hand + '|' + cell)
    if m:
        return m.get('p_spare', 0.0) >= 0.5
    return False  # W5 flat prior: p_spare = 1/13 -> destroy

def predict_L4(order, holds, p_table=None):
    # L4, last-holder-spare: holder re-holds while revising; a held cell
    # survives a non-holder iff that hand spares it
    p_table = p_table or {}
    held = set(holds.get(order[0], set()))
    for h in order[1:]:
        hs = set(holds.get(h, set()))
        nxt = set(hs)
        for c in held:
            if c not in hs and _spares(h, c, p_table):
                nxt.add(c)
        held = nxt
    return held

def w7_replay():
    res = json.load(open(W7_RESULTS, encoding='utf-8'))
    bad, n = [], 0
    for name, v in res.get('solo', {}).items():
        if 'poem' not in v:
            continue
        n += 1
        fresh = check(v['poem'])
        for k, val in v['check'].items():
            if fresh.get(k) != val:
                bad.append(('solo', name, k, val, fresh.get(k)))
    for b in ('braid_ascending', 'braid_descending'):
        if b in res and 'poem' in res[b]:
            n += 1
            fresh = check(res[b]['poem'])
            for k, val in res[b]['check'].items():
                if fresh.get(k) != val:
                    bad.append((b, 'final', k, val, fresh.get(k)))
    return n, bad

def selftest():
    p_table = {}
    if os.path.exists(W8_ANALYSIS):
        p_table = json.load(open(W8_ANALYSIS, encoding='utf-8')).get('nonholder_table', {})
    asc, desc = ['wesley', 'flash', 'kimi', 'claude'], ['claude', 'kimi', 'flash', 'wesley']
    l1a, l1d = predict_L1(asc, W7_HOLDS), predict_L1(desc, W7_HOLDS)
    l4a, l4d = predict_L4(asc, W7_HOLDS, p_table), predict_L4(desc, W7_HOLDS, p_table)
    floor = {'12_lines', 'c5_last_word_unique'}
    assert l1a == floor, sorted(l1a)
    assert l1d == floor, sorted(l1d)
    assert l4a == {'12_lines', 'c1_growth', 'c3_seal', 'c4_no_rhyme', 'c5_last_word_unique'}, sorted(l4a)
    # Sealed-rule consequence (honest): on W7's DESC order the frozen L4
    # rule predicts c4 surviving (flash 0.67, wesley 0.50 both spare);
    # W7 observed the floor. Recorded, not overridden.
    assert l4d == {'12_lines', 'c4_no_rhyme', 'c5_last_word_unique'}, sorted(l4d)
    n, bad = w7_replay()
    assert not bad, bad
    print('selftest OK')
    print('  L1 ASC  = %s' % ','.join(csort(l1a)))
    print('  L1 DESC = %s' % ','.join(csort(l1d)))
    print('  L4 ASC  = %s  (floor + c1,c3,c4)' % ','.join(csort(l4a)))
    print('  L4 DESC = %s  (floor)' % ','.join(csort(l4d)))
    print('  W7 replay: %d stored poems re-checked, 0 mismatches vs stored check dicts' % n)

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def score(solo, chains, sealed, p_table):
    holds = {y: hold_set(v['check']) for y, v in solo.items() if 'check' in v}
    per_chain, pooled, mism = {}, {'L1': [0, 0], 'L4': [0, 0]}, []
    for ch in chains:
        tag = ch['tag']
        obs = {c: bool(ch['final_check'].get(c)) for c in CONSTRAINTS}
        alg = {'L1': predict_L1(ch['order'], holds), 'L4': predict_L4(ch['order'], holds, p_table)}
        correct = {}
        for law in ('L1', 'L4'):
            pred = sealed.get(tag, {}).get(law)
            if pred is None:
                mism.append({'tag': tag, 'law': law, 'cell': '<all>', 'sealed': 'MISSING', 'algorithm': csort(alg[law])})
                pred = {}
            k = 0
            for c in CONSTRAINTS:
                sp = pred.get(c)
                if sp is not None and bool(sp) != (c in alg[law]):
                    mism.append({'tag': tag, 'law': law, 'cell': c, 'sealed': bool(sp), 'algorithm': c in alg[law]})
                pooled[law][1] += 1
                if sp is not None and bool(sp) == obs[c]:
                    k += 1
                    pooled[law][0] += 1
            correct[law] = k
        per_chain[tag] = {'order': ch['order'],
                          'observed_held': csort({c for c in CONSTRAINTS if obs[c]}),
                          'algorithm': {law: csort(alg[law]) for law in alg},
                          'correct': correct, 'n_cells': len(CONSTRAINTS)}
    chc = None
    for ch in chains:
        if ch['tag'] != 'CH-C':
            continue
        obs = {c for c in CONSTRAINTS if ch['final_check'].get(c)}
        l1 = predict_L1(ch['order'], holds)
        l4 = predict_L4(ch['order'], holds, p_table)
        chc = {'tag': 'CH-C', 'order': ch['order'], 'observed': csort(obs),
               'L1_floor': csort(l1), 'L4_pred': csort(l4),
               'exact_L1': obs == l1, 'exact_L4': obs == l4, 'exact': obs == l1 == l4}
        break
    verdict = {
        'n_chains': len(chains),
        'holds_measured': {y: csort(holds[y]) for y in sorted(holds)},
        'per_chain': per_chain,
        'pooled': {law: {'correct': pooled[law][0], 'n': pooled[law][1],
                         'accuracy': round(pooled[law][0] / pooled[law][1], 4) if pooled[law][1] else None}
                   for law in ('L1', 'L4')},
        'chc': chc,
        'sealed_vs_algorithm_mismatches': mism,
    }
    p4 = verdict['pooled']['L4']
    verdict['bar'] = {
        'L4_pooled_ge_080': bool(p4['n'] and p4['accuracy'] >= 0.8),
        'chc_exact': bool(chc and chc['exact']),
        'met': bool(p4['n'] and p4['accuracy'] >= 0.8 and chc and chc['exact']),
    }
    return verdict

def main():
    ap = argparse.ArgumentParser(description='W10 — LAW AS HELM scorer')
    ap.add_argument('--selftest', action='store_true', help='W7 replay + frozen-simulation asserts; no data files needed')
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    need = {'w10-phase0.json': 'run w10_run.py phase0',
            'w10-chains.json': 'run w10_run.py chain',
            'w10-predictions.json': 'seal SEALED-PREDICTIONS.md first'}
    for f, why in need.items():
        if not os.path.exists(f):
            raise SystemExit('missing %s — %s' % (f, why))
    solo = load_json('w10-phase0.json')['solo']
    chains = load_json('w10-chains.json')
    if not chains:
        raise SystemExit('w10-chains.json is empty — run chains first')
    sealed = load_json('w10-predictions.json')
    p_table = load_json(W8_ANALYSIS).get('nonholder_table', {}) if os.path.exists(W8_ANALYSIS) else {}
    v = score(solo, chains, sealed, p_table)
    with open('w10-verdict-data.json', 'w', encoding='utf-8') as f:
        json.dump(v, f, indent=2)
    print('W10 scorecards — cells correct of 7 (sealed predictions vs final verbatim check):')
    print('%-6s  %-27s  L1      L4' % ('tag', 'order'))
    for ch in chains:
        pc = v['per_chain'][ch['tag']]
        print('%-6s  %-27s  %d/7    %d/7' % (ch['tag'], '->'.join(ch['order']), pc['correct']['L1'], pc['correct']['L4']))
    pl, p4 = v['pooled']['L1'], v['pooled']['L4']
    print('pooled: L1 %d/%d (%.1f%%) | L4 %d/%d (%.1f%%)'
          % (pl['correct'], pl['n'], 100 * pl['accuracy'], p4['correct'], p4['n'], 100 * p4['accuracy']))
    chc = v['chc']
    if chc:
        print("CH-C exact-match (observed == both laws' intersection floor):", chc['exact'])
        print('  observed %s | L1 %s | L4 %s'
              % (','.join(chc['observed']) or '-', ','.join(chc['L1_floor']) or '-', ','.join(chc['L4_pred']) or '-'))
    else:
        print('CH-C: not in w10-chains.json — reproduction control not scored')
    mism = v['sealed_vs_algorithm_mismatches']
    if mism:
        print('SEALED vs ALGORITHM MISMATCHES (%d):' % len(mism))
        for m in mism:
            print(' ', m)
    else:
        print('sealed predictions match frozen algorithms on every cell')
    print('bar (L4 pooled >= 80%% AND CH-C exact):', v['bar']['met'])
    print('wrote w10-verdict-data.json')

if __name__ == '__main__':
    main()
