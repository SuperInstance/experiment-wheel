#!/usr/bin/env python3
"""
W9b — THE FAIR-INSTRUMENT RE-SCORE (OPERATIONS-DOCTRINE mid-term queue item)

Re-scores the RECORDED artifacts of W6b and W7 under the fair cells
c2' (THEEILEENLAU acrostic, W9 pre-registered) and c6' (one comma + one
period, ASCII-correct sort, W9 Amendment 1) exported by
W9-never-held-kernel/w9_check.py.

THIS IS AN INSTRUMENT CORRECTION, NOT A NEW EXPERIMENT.
  - zero model calls (pure local compute; no network, no GPU/ollama)
  - recorded artifacts are READ, never modified
  - sealed predictions are NOT re-scored — only artifact scores
  - frozen (verbatim-checker) numbers STAND as measured; fair-lens
    numbers are reported ALONGSIDE, never replacing them

Stages (each must pass before the next runs):
  1. INSTRUMENT IDENTITY — embedded check()/c2_amended()/c6_amended()
     asserted byte-identical (source-line level) to w9_check.py, and
     check() to W6b's and W7's spikes (re-verifying W9's audit claim).
  2. SATISFIABILITY WITNESSES (doctrine: no cell scores anything until
     it has a witness) — constructions exhibiting c2' and c6' TRUE, a
     FULL-BOARD witness (all 7 cells true under the fair lens), and
     mechanical impossibility proofs for verbatim c2/c6.
  3. VERIFY VS W9 RECORDINGS — replay every poem in W9's ledgers;
     replayed verbatim check and fair cells must equal every recorded
     flag, zero mismatches, before any W6b/W7 number is produced.
  4. RESCORE W6b/W7 — every surviving poem artifact: replay old check
     (chain of custody), apply c2'/c6' mechanically, new score =
     old + c2' + c6' (c2/c6 verbatim asserted False everywhere).
  5. W11 CROSSCHECK COMPARISON — confirm or correct each row of
     W11's corrected-lens table with this independent mechanical pass.

Output: RESCORE.json (this directory).
"""
import ast, glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W9 = os.path.join(ROOT, 'W9-never-held-kernel')
W6 = os.path.join(ROOT, 'W6-the-braid')
W7 = os.path.join(ROOT, 'W7-ordered-braid')
W11 = os.path.join(ROOT, 'W11-fused-catch')

# ---------------------------------------------------------------------------
# STAGE 1 — THE INSTRUMENT (ported; identity asserted below before use)
# ---------------------------------------------------------------------------

TASK = """Write EXACTLY 12 lines of a poem called 'the chamber'. Constraints (ALL checked mechanically; they interlock — plan the whole poem before writing):
1. Line n contains exactly n words (line 1 = 1 word, line 12 = 12 words).
2. The FIRST letters of the 12 lines, in order, spell: THEEILEENLAUN
3. Exactly one line contains a 12-character lowercase hex seal (like 8721b4bd042a). That line's word count must equal (first two hex chars as a number mod 12) + 1. Choose your seal so it lands on a line you want.
4. No two lines may end with rhyming words.
5. The final line's last word must appear NOWHERE else in the poem.
6. Punctuation: exactly one comma and one period in the whole poem, no other punctuation; no capitals except the first letter of any line.
Output ONLY the 12 lines."""

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
    # c4 rhyme: crude last-vowel-cluster check
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

def c2_amended(poem):
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    return ''.join(l[0] for l in lines).upper()[:12] == 'THEEILEENLAU'

# --- W9 AMENDMENT 1 (sealed before SH-4): c6' — the ASCII-correct punctuation cell.
# Verbatim c6 is unsatisfiable: sorted([',','.']) can never equal ['.', ','] (0x2C < 0x2E).
def c6_amended(poem):
    """Exactly one comma AND one period (ASCII), no other punctuation,
    capitals only line-initial, 12 lines. Fleet-side scoring; check() untouched."""
    lines = [l.strip() for l in poem.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    if len(lines) != 12:
        return False
    punc = re.sub(r'[a-zA-Z0-9\s]', '', poem)
    if sorted(punc) != [',', '.']:
        return False
    caps = re.findall(r'[A-Z]', poem)
    firsts = [l[0] for l in lines if l and l[0].isupper()]
    return len(caps) == len(firsts)

def fn_src(path, name):
    """Exact source lines of function `name` in file `path` (line-level identity)."""
    src = open(path).read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return src.splitlines()[node.lineno - 1:node.end_lineno]
    return None

def stage1_identity():
    emb = {'check': fn_src(__file__, 'check'),
           'c2_amended': fn_src(__file__, 'c2_amended'),
           'c6_amended': fn_src(__file__, 'c6_amended')}
    w9 = {k: fn_src(os.path.join(W9, 'w9_check.py'), k) for k in emb}
    w6b = fn_src(os.path.join(W6, 'w6b_spike.py'), 'check')
    w7 = fn_src(os.path.join(W7, 'w7_spike.py'), 'check')
    assert emb['check'] == w9['check'], 'check() != w9_check.check()'
    assert emb['c2_amended'] == w9['c2_amended'], 'c2_amended != w9_check.c2_amended()'
    assert emb['c6_amended'] == w9['c6_amended'], 'c6_amended != w9_check.c6_amended()'
    assert emb['check'] == w6b, 'check() != w6b_spike.check()'
    assert emb['check'] == w7, 'check() != w7_spike.check()'
    print('STAGE 1 PASS — instrument byte-identical (line-level) to w9_check.py '
          '(check, c2_amended, c6_amended) and to W6b/W7 spikes (check).')
    return True

# ---------------------------------------------------------------------------
# STAGE 2 — SATISFIABILITY WITNESSES + IMPOSSIBILITY PROOFS
# ---------------------------------------------------------------------------

# Witness for c2': 12 lines whose first letters spell THEEILEENLAU (the 12
# satisfiable letters of the task's 13-letter target).
W_C2P = "\n".join([
    "Threshold", "Halls of echo", "empty rooms", "each stone keeps",
    "its own silence", "locked under everything", "else the dark",
    "endures without witness", "name by name the vault", "lets its last light go",
    "and the air forgets", "us too, in time.",
])

# Witness for c6': 12 lines, exactly one comma and one period (ASCII-correct
# sort), capitals line-initial only.
W_C6P = "\n".join([
    "Threshold", "Hushed halls,", "and nothing else", "belongs to noon",
    "or to the long", "afternoon of stone", "where every echo", "learns to wait",
    "for what the dark", "keeps and will not", "give back to anyone", "who asks it kindly.",
])

# FULL-BOARD witness: all 7 cells TRUE under the fair lens — the fair
# instrument's ceiling (7/7) is constructible. Built by hand, verified by code.
W_ALL = "\n".join([
    "Threshold",                                             # 1 word,  T
    "Hushed halls,",                                         # 2 words, H  (the one comma)
    "echoes descend below",                                  # 3 words, e
    "every stone remembers silence",                         # 4 words, e
    "inside the vault nothing stirs",                        # 5 words, i
    "lanterns dim as shadows lean near",                     # 6 words, l
    "each hour folds seal 06c0ffeeb0ba in water",            # 7 words, e  (seal: 06 -> 6%12+1 = 7)
    "empty corridors keep the old dark close tonight",       # 8 words, e
    "no voice returns to name what the silence took",        # 9 words, n
    "light thins to a thread against the far stone wall",    # 10 words, l
    "all that was hidden waits beneath the hush without a sound",  # 11 words, a
    "under everything the quiet chamber holds one final vow and then sleeps.",  # 12 words, u (the one period)
])

def stage2_witnesses():
    # --- impossibility proofs (verbatim cells), mechanical:
    assert len('THEEILEENLAUN') == 13, 'c2 target length claim'
    assert 'THEEILEENLAU' == 'THEEILEENLAUN'[:12], 'c2 prime is first 12 letters'
    # any 12-line poem joins exactly 12 first letters; 12 != 13, always False:
    assert len(''.join(l[0] for l in W_ALL.splitlines())) == 12 and 12 != 13
    assert sorted([',', '.']) == [',', '.'] and ['.', ','] != [',', '.'], \
        'ASCII 0x2C < 0x2E: the checker literal can never equal sorted() output'
    # --- witnesses (fair cells), mechanical:
    assert c2_amended(W_C2P) is True, 'c2 prime witness FAILED'
    assert c6_amended(W_C6P) is True, 'c6 prime witness FAILED'
    full = check(W_ALL)
    fair = dict(full)
    fair.pop('score')
    fair['c2_acrostic'] = c2_amended(W_ALL)
    fair['c6_punctuation'] = c6_amended(W_ALL)
    assert all(v is True for v in fair.values()), f'full-board witness FAILED: {fair}'
    # and the same perfect poem under the FROZEN instrument scores 5/7 (c2=c6=False):
    frozen = check(W_ALL)
    assert frozen['c2_acrostic'] is False and frozen['c6_punctuation'] is False
    assert frozen['score'] == 5, frozen['score']
    print('STAGE 2 PASS — witnesses: c2\' TRUE (construction on file), c6\' TRUE '
          '(construction on file), full board 7/7 TRUE (construction on file); '
          'verbatim c2/c6 proven unsatisfiable (13!=12; ASCII sort). '
          'The perfect poem scores 5/7 under the frozen instrument — blindness exhibited.')
    return {'w_c2p': W_C2P, 'w_c6p': W_C6P, 'w_all': W_ALL,
            'w_all_frozen_score': 5, 'w_all_fair_score': 7}

# ---------------------------------------------------------------------------
# STAGE 3 — VERIFY THE PORT AGAINST W9'S OWN RECORDINGS
# ---------------------------------------------------------------------------

def stage3_verify_w9():
    poems, cmp_check, cmp_c2p, cmp_c6p = 0, 0, 0, 0
    mism = []
    def vfy(tag, poem, rec_check, rec_c2p=None, rec_c6p=None):
        nonlocal poems, cmp_check, cmp_c2p, cmp_c6p
        poems += 1
        got = check(poem)
        if got != rec_check:
            mism.append(f'{tag}: check replay mismatch\n  rec={rec_check}\n  got={got}')
        cmp_check += 1
        if rec_c2p is not None:
            if c2_amended(poem) != rec_c2p:
                mism.append(f'{tag}: c2_amended replay {c2_amended(poem)} != recorded {rec_c2p}')
            cmp_c2p += 1
        if rec_c6p is not None:
            if c6_amended(poem) != rec_c6p:
                mism.append(f'{tag}: c6_amended replay {c6_amended(poem)} != recorded {rec_c6p}')
            cmp_c6p += 1

    for f in sorted(glob.glob(os.path.join(W9, 'ledgers', 'sh[12]-*.json')) +
                    glob.glob(os.path.join(W9, 'ledgers', 'sh4-*.json'))):
        led = json.load(open(f))
        for d in led.get('draws', []):
            if 'poem' in d and 'check' in d:
                vfy(f"{os.path.basename(f)}::{d.get('seed_tag')}", d['poem'], d['check'],
                    d.get('c2_amended'), d.get('c6_amended'))
    for f in sorted(glob.glob(os.path.join(W9, 'ledgers', 'sh3-*.json'))):
        led = json.load(open(f))
        for ch in led.get('chains', []):
            for p in ch.get('passes', []):
                if 'poem' in p and 'check' in p:
                    vfy(f"{os.path.basename(f)}::{ch.get('chain')}::{p.get('pass')}",
                        p['poem'], p['check'], p.get('c2_amended'), p.get('c6_amended'))
    # sh4 seeds carry recorded fair flags but no poem; match them to their sh1 source draw.
    for f in sorted(glob.glob(os.path.join(W9, 'ledgers', 'sh4-*.json'))):
        led = json.load(open(f))
        if 'seed_c2_amended' not in led:
            continue
        cands = []
        for g in glob.glob(os.path.join(W9, 'ledgers', 'sh1-*.json')):
            for d in json.load(open(g)).get('draws', []):
                if d.get('check') == led.get('seed_check') and 'poem' in d:
                    cands.append((g, d))
        if len(cands) == 1:
            g, d = cands[0]
            tag = f'{os.path.basename(f)}::seed(from {os.path.basename(g)})'
            vfy(tag, d['poem'], led['seed_check'], led.get('seed_c2_amended'), led.get('seed_c6_amended'))
    if mism:
        print('STAGE 3 FAIL — %d mismatch(es):' % len(mism))
        print('\n'.join(mism)); sys.exit(1)
    print(f'STAGE 3 PASS — {poems} W9 poems replayed: {cmp_check} check-dict comparisons, '
          f'{cmp_c2p} c2\' flag comparisons, {cmp_c6p} c6\' flag comparisons — ZERO mismatches.')
    return {'poems': poems, 'check_comparisons': cmp_check,
            'c2p_comparisons': cmp_c2p, 'c6p_comparisons': cmp_c6p, 'mismatches': 0}

# ---------------------------------------------------------------------------
# STAGE 4 — RESCORE THE W6b/W7 RECORDED ARTIFACTS
# ---------------------------------------------------------------------------

def sha12(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]

def rescore(tag, srcfile, poem, rec_check):
    got = check(poem)
    assert got == rec_check, f'{tag}: frozen replay mismatch (chain of custody broken)'
    assert rec_check['c2_acrostic'] is False and rec_check['c6_punctuation'] is False, \
        f'{tag}: verbatim c2/c6 assumed False (impossibility) — violated'
    c2p, c6p = c2_amended(poem), c6_amended(poem)
    new = dict(rec_check)
    new['c2_acrostic'] = c2p
    new['c6_punctuation'] = c6p
    new_score = rec_check['score'] + int(c2p) + int(c6p)
    changed = []
    if c2p: changed.append('c2_acrostic -> c2_prime TRUE')
    if c6p: changed.append('c6_punctuation -> c6_prime TRUE')
    return {
        'tag': tag, 'source': srcfile, 'poem_sha256_12': sha12(poem),
        'old_score': rec_check['score'], 'old_cells': {k: v for k, v in rec_check.items() if k != 'score'},
        'c2_prime': bool(c2p), 'c6_prime': bool(c6p),
        'new_score': new_score,
        'new_cells': {k: v for k, v in new.items() if k != 'score'},
        'changed_cells': changed,
    }

def stage4_rescore():
    out, notext = [], []
    w6b = json.load(open(os.path.join(W6, 'w6b-results.json')))
    src = 'W6-the-braid/w6b-results.json'
    for yard in ('claude', 'kimi', 'flash', 'wesley'):
        a = w6b['solo'][yard]
        out.append(rescore(f'W6b solo {yard}', src, a['poem'], a['check']))
    a = w6b['copies']
    out.append(rescore('W6b copies (flash x4, final)', src, a['poem'], a['check']))
    a = w6b['braid']
    out.append(rescore('W6b braid final (kimi>claude>flash>wesley>flash)', src, a['poem'], a['check']))

    w7 = json.load(open(os.path.join(W7, 'w7-results.json')))
    src = 'W7-ordered-braid/w7-results.json'
    for yard in ('claude', 'kimi', 'flash', 'wesley'):
        a = w7['solo'][yard]
        out.append(rescore(f'W7 solo {yard}', src, a['poem'], a['check']))
    for key, label in (('braid_ascending', 'W7 braid ASC final (wesley>flash>kimi>claude)'),
                       ('braid_descending', 'W7 braid DESC final (claude>kimi>flash>wesley)')):
        a = w7[key]
        out.append(rescore(label, src, a['poem'], a['check']))
        for t in a.get('trace', []):
            notext.append(f"{label} :: intermediate hand {t['hand']} "
                          f"(recorded score {t['check']['score']}/7-cell; poem text not preserved)")
    # W6a exclusion is by design: different task (13-line boat-pieces), different checker —
    # incomparable; W9's audit excluded it for the same reason. Nothing to re-score.
    print(f'STAGE 4 — {len(out)} artifacts re-scored '
          f'(W6b 6: 4 solos + copies + braid; W7 6: 4 solos + ASC + DESC). '
          f'{len(notext)} intermediate drafts survive as scores only (no poem text on record).')
    return out, notext

# ---------------------------------------------------------------------------
# STAGE 5 — CONFIRM/CORRECT THE W11 CROSSCHECK
# ---------------------------------------------------------------------------

def stage5_compare(resc):
    x = json.load(open(os.path.join(W11, 'w11-crosscheck-w6w7.json')))
    # deterministic tag map: W11 crosscheck row -> this station's artifact tag.
    # W6b 'copy 0'/'copy 1' BOTH map to the single committed copies artifact
    # (flash x4) — the double-map itself is recorded as an enumeration finding.
    rowmap = {
        'W6b solo claude': 'W6b solo claude', 'W6b solo kimi': 'W6b solo kimi',
        'W6b solo flash': 'W6b solo flash', 'W6b solo wesley': 'W6b solo wesley',
        'W6b copy 0': 'W6b copies (flash x4, final)',
        'W6b copy 1': 'W6b copies (flash x4, final)',
        'W6b braid final': 'W6b braid final (kimi>claude>flash>wesley>flash)',
        'W7 solo claude': 'W7 solo claude', 'W7 solo kimi': 'W7 solo kimi',
        'W7 solo flash': 'W7 solo flash', 'W7 solo wesley': 'W7 solo wesley',
        'W7 ASC final': 'W7 braid ASC final (wesley>flash>kimi>claude)',
        'W7 DESC final': 'W7 braid DESC final (claude>kimi>flash>wesley)',
    }
    rows, issues = [], []
    by_tag = {r['tag']: r for r in resc}
    def confirm(tag_w11, frozen, prime, flips):
        has_c2 = 'c2_acrostic' in flips
        has_c6 = 'c6_punctuation' in flips
        if tag_w11 not in rowmap:
            # intermediate-hand rows: W11 recorded nulls (no poem text survives) — this pass agrees.
            rows.append({'w11_row': tag_w11, 'frozen': frozen, 'prime': prime,
                         'status': 'NO-TEXT (both lenses: poem not preserved)',
                         'detail': 'intermediate draft; scores only in the braid trace'})
            return
        r = by_tag[rowmap[tag_w11]]
        ok = (r['old_score'] == frozen and r['new_score'] == prime
              and r['c2_prime'] == has_c2 and r['c6_prime'] == has_c6)
        rows.append({'w11_row': tag_w11, 'frozen': frozen, 'prime': prime,
                     'status': 'CONFIRMED' if ok else 'CORRECTED',
                     'mechanical': {'old': r['old_score'], 'new': r['new_score'],
                                    'c2_prime': r['c2_prime'], 'c6_prime': r['c6_prime'],
                                    'artifact': r['tag']}})
        if not ok:
            issues.append(f'{tag_w11}: W11 said {frozen}->{prime} flips={flips}; '
                          f"mechanical pass says {r['old_score']}->{r['new_score']} "
                          f"c2'={r['c2_prime']} c6'={r['c6_prime']}")
    for e in x.get('w6b', []):
        confirm(e['tag'], e['frozen'], e['prime'], e['flips'])
    for e in x.get('w7', []):
        confirm(e[0], e[1], e[2], e[3])
    # enumeration audit: W11 lists 7 w6b rows; the committed artifact file holds 6.
    n_w6b_rows = len(x.get('w6b', []))
    if n_w6b_rows != 6:
        copies_rows = [r for r in x.get('w6b', []) if 'copy' in r['tag']]
        issues.append(f"W11 crosscheck enumerates {n_w6b_rows} W6b rows for 6 committed artifacts; "
                      f"the single recorded 'copies' artifact (flash x4) was double-counted as "
                      f"{[r['tag'] for r in copies_rows]} (both rows 1->1; no number changed)")
    return rows, issues

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    stage1_identity()
    wit = stage2_witnesses()
    ver = stage3_verify_w9()
    resc, notext = stage4_rescore()
    rows, issues = stage5_compare(resc)
    doc = {
        'station': 'W9b-fair-rescore',
        'date': '2026-08-27',
        'nature': ('instrument correction, not a new experiment; zero model calls; '
                   'recorded artifacts untouched; sealed predictions NOT re-scored — '
                   'artifact scores only; frozen numbers stand as measured'),
        'instrument': ('check()/c2_amended()/c6_amended() ported byte-identical from '
                       'W9-never-held-kernel/w9_check.py; check() identical to W6b/W7 spikes'),
        'witnesses': {
            'c2_prime_witness_satisfiable': True,
            'c6_prime_witness_satisfiable': True,
            'full_board_witness': {'fair_score': 7, 'frozen_score': 5,
                                   'note': 'the perfect poem scores 5/7 under the frozen instrument'},
            'verbatim_c2_impossible': 'THEEILEENLAUN is 13 chars vs 12 first-letters',
            'verbatim_c6_impossible': "sorted([',','.']) can never equal ['.',','] (ASCII 0x2C < 0x2E)",
            'constructions': wit,
        },
        'verification_vs_w9_recordings': ver,
        'rescore': resc,
        'not_preserved': notext,
        'exclusions': [
            'W6a (w6-results.json): different task (13-line boat-pieces) and checker — '
            'incomparable by design (W9 audit precedent)',
            'W10/W11 artifacts: own stations, out of scope for this correction '
            '(W11 already carries its own corrected-lens numbers)',
        ],
        'w11_crosscheck_comparison': {'rows': rows, 'issues': issues},
        'score_units': ('score field counts 7 cells (12L + c1..c6); historical prose quoted '
                        'the same number as "x/6". Old max reachable was 5 (c2/c6 impossible); '
                        'fair-lens max is 7.'),
    }
    with open(os.path.join(HERE, 'RESCORE.json'), 'w') as f:
        json.dump(doc, f, indent=1)
    print('\n=== FAIR RE-SCORE (old -> new | cells flipped) ===')
    for r in resc:
        fl = ('+' if r['c2_prime'] else '-') + 'c2\'' + (' +' if r['c6_prime'] else ' -') + 'c6\''
        print(f"  {r['tag']:55s} {r['old_score']} -> {r['new_score']}   [{fl}]")
    print('\n=== W11 CROSSCHECK ===')
    for row in rows:
        print(f"  {row['w11_row']:28s} {row['status']:12s} "
              f"(w11 {row['frozen']}->{row['prime']})")
    for i in issues:
        print('  ISSUE:', i)
    print('\nsaved RESCORE.json')
