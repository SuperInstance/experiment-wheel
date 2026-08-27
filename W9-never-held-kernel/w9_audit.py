#!/usr/bin/env python3
"""
W9 audit - replay W6/W6b/W7 recorded poems through the byte-identical
check() and prove the verbatim c2_acrostic is unsatisfiable by
construction; written by opencode, reviewed by W9.
"""
import json
import os

from w9_check import check

SOURCES = [
    # W9 registration scope: replay against W6b + W7 recordings only.
    # (W6a's w6-results.json is a DIFFERENT task with its own different checker —
    #  13-line/16-hex flags lines_13/order_ok/ends_keel — incomparable by design.)
    '../W6-the-braid/w6b-results.json',
    '../W7-ordered-braid/w7-results.json',
]


def walk(node, path='$'):
    if isinstance(node, dict):
        if isinstance(node.get('poem'), str) and isinstance(node.get('check'), dict):
            yield path, node['poem'], node['check']
        for k, v in node.items():
            yield from walk(v, path + '.' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + '[%d]' % i)


def replay(source):
    rows = []
    with open(source) as f:
        data = json.load(f)
    for path, poem, recorded in walk(data):
        recomputed = check(poem)
        flag_rows = []
        all_match = True
        for key in sorted(set(recorded) | set(recomputed)):
            if key == 'score':
                continue
            rec, new = recorded.get(key, '<missing>'), recomputed.get(key, '<missing>')
            match = rec == new
            all_match = all_match and match
            flag_rows.append((key, rec, new, match))
        score_rec = recorded.get('score', '<missing>')
        score_new = recomputed.get('score', '<missing>')
        score_match = score_rec == score_new
        rows.append({
            'source': source,
            'path': path,
            'score_rec': score_rec,
            'score_new': score_new,
            'score_match': score_match,
            'flags': flag_rows,
            'all_match': all_match and score_match,
        })
    return rows


def c2_impossibility():
    target = 'THEEILEENLAUN'
    demo = '\n'.join('w%d %s' % (n + 1, 'x' * n) for n in range(12))
    lines = [l.strip() for l in demo.strip().split('\n') if l.strip()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('```')]
    letters = ''.join(l[0] for l in lines)
    ok_len_target = len(target) == 13
    ok_12_lines = len(lines) == 12
    ok_12_letters = len(letters) == 12
    print("len('%s') == 13 : %s" % (target, ok_len_target))
    print('a 12-line poem yields exactly 12 first letters : %s (demo: %d lines -> %d letters)'
          % (ok_12_lines and ok_12_letters, len(lines), len(letters)))
    unsatisfiable = ok_len_target and ok_12_lines and ok_12_letters
    return unsatisfiable, target


def main():
    rows = []
    for source in SOURCES:
        rows.extend(replay(source))

    unsatisfiable, target = c2_impossibility()

    out = []
    out.append('# W9 Audit Report')
    out.append('')
    out.append('Every recorded artifact replayed through the byte-identical `check()` from'
               ' `../W6-the-braid/w6b_spike.py` (reused verbatim in `w9_check.py`).')
    out.append('')
    out.append('## Replayed artifacts')
    out.append('')
    out.append('| source file | json path | recorded score | recomputed score | per-flag match |')
    out.append('|---|---|---|---|---|')
    for r in rows:
        flags_ok = all(f[3] for f in r['flags'])
        per_flag = 'ALL MATCH' if flags_ok else 'MISMATCH: ' + ', '.join(
            '%s rec=%s new=%s' % (k, rec, new) for k, rec, new, m in r['flags'] if not m)
        out.append('| %s | `%s` | %s | %s | %s |' % (
            os.path.basename(r['source']), r['path'], r['score_rec'], r['score_new'], per_flag))
    out.append('')
    out.append('## c2 impossibility proof')
    out.append('')
    out.append('- `%s` has length **%d**.' % (target, len(target)))
    out.append("- Any poem passing `12_lines` has exactly 12 lines, so `''.join(l[0] for l in lines)`"
               ' yields exactly **12** first letters (demonstrated on a synthetic 12-line poem:'
               ' 12 lines -> 12 letters).')
    out.append('- 12 letters can never equal a 13-letter string, so the verbatim'
               " `c2_acrostic` (`''.join(l[0] for l in lines).upper() == '%s'`) is"
               ' **unsatisfiable by construction**: no poem can ever score it, regardless of model.'
               % target)
    out.append('- `c2_amended` truncates to the first 12 letters (`[:12] == \'THEEILEENLAU\'`),'
               ' which is satisfiable; `check()` itself was NOT modified.')
    out.append('')
    n_match = sum(1 for r in rows if r['all_match'])
    out.append('## Verdict')
    out.append('')
    out.append('- artifacts replayed: %d' % len(rows))
    out.append('- artifacts matched (score and every flag): %d' % n_match)
    out.append('- artifacts mismatched: %d' % (len(rows) - n_match))
    out.append('')
    with open('audit-report.md', 'w') as f:
        f.write('\n'.join(out) + '\n')

    if all(r['all_match'] for r in rows) and unsatisfiable and len(rows) > 0:
        with open('audit-report.md', 'a') as f:
            f.write('AUDIT: PASS\n')
        print('AUDIT: PASS (%d/%d artifacts matched, c2 proven unsatisfiable)' % (n_match, len(rows)))
    else:
        for r in rows:
            if not r['all_match']:
                print('MISMATCH', r['source'], r['path'],
                      'score rec=%s new=%s' % (r['score_rec'], r['score_new']),
                      ['%s rec=%s new=%s' % (k, rec, new) for k, rec, new, m in r['flags'] if not m])
        print('AUDIT: FAIL')


if __name__ == '__main__':
    main()
