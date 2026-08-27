# W9 Audit Report

Every recorded artifact replayed through the byte-identical `check()` from `../W6-the-braid/w6b_spike.py` (reused verbatim in `w9_check.py`).

## Replayed artifacts

| source file | json path | recorded score | recomputed score | per-flag match |
|---|---|---|---|---|
| w6b-results.json | `$.solo.claude` | 4 | 4 | ALL MATCH |
| w6b-results.json | `$.solo.kimi` | 4 | 4 | ALL MATCH |
| w6b-results.json | `$.solo.flash` | 2 | 2 | ALL MATCH |
| w6b-results.json | `$.solo.wesley` | 2 | 2 | ALL MATCH |
| w6b-results.json | `$.copies` | 1 | 1 | ALL MATCH |
| w6b-results.json | `$.braid` | 2 | 2 | ALL MATCH |
| w7-results.json | `$.solo.claude` | 4 | 4 | ALL MATCH |
| w7-results.json | `$.solo.kimi` | 4 | 4 | ALL MATCH |
| w7-results.json | `$.solo.flash` | 2 | 2 | ALL MATCH |
| w7-results.json | `$.solo.wesley` | 2 | 2 | ALL MATCH |
| w7-results.json | `$.braid_ascending` | 5 | 5 | ALL MATCH |
| w7-results.json | `$.braid_descending` | 2 | 2 | ALL MATCH |

## c2 impossibility proof

- `THEEILEENLAUN` has length **13**.
- Any poem passing `12_lines` has exactly 12 lines, so `''.join(l[0] for l in lines)` yields exactly **12** first letters (demonstrated on a synthetic 12-line poem: 12 lines -> 12 letters).
- 12 letters can never equal a 13-letter string, so the verbatim `c2_acrostic` (`''.join(l[0] for l in lines).upper() == 'THEEILEENLAUN'`) is **unsatisfiable by construction**: no poem can ever score it, regardless of model.
- `c2_amended` truncates to the first 12 letters (`[:12] == 'THEEILEENLAU'`), which is satisfiable; `check()` itself was NOT modified.

## Verdict

- artifacts replayed: 12
- artifacts matched (score and every flag): 12
- artifacts mismatched: 0

AUDIT: PASS
