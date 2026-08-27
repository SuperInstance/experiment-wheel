# SPEC for the W11 amendment patch + w11_diagnostic.py

Two jobs, both mechanical, no model calls, no reading of
w11-braids.json contents by you (the code you write reads it at
runtime; you never need to).

## Job 1 — patch w11_fusion.py's self-test ONLY (leave every frozen rule and the checker byte-identical)

Replace the self-test's `assert score==7` expectation: the synthetic
all-constraints poem (the one you already construct, which holds all
six constraints as constructible) must yield, under the VERBATIM
frozen checker, exactly `12_lines/c1_growth/c3_seal/c4_no_rhyme/
c5_last_word_unique` True and `c2_acrostic/c6_punctuation` False
(total score 5) — the frozen checker's structural ceiling, per sealed
amendment 1. Assert that. Keep your existing fuse toy-case asserts
unchanged. Change nothing else in the file.

## Job 2 — write w11_diagnostic.py (the corrected lens, sealed amendment 1)

Standalone, stdlib only, deterministic, no network. Reads
`w11-results.json` (produced by w11_fusion.py) and `w11-braids.json`.
It re-scores artifacts under a CORRECTED lens — this NEVER modifies
w11-results.json; it writes `w11-diagnostic.json` and prints a summary.

Corrected constraint functions (applied to the same 12-line extraction
as the frozen checker):

```python
def check2(poem):  # corrected lens: c2' and c6' repaired, rest identical in spirit
    # reuse the frozen checker's line extraction
    # c2': ''.join(first letters).upper() == 'THEEILEENLAU'
    # c6': sorted(punctuation_chars) == [',', '.'] AND capitals only line-initial
    # all other cells: recompute exactly as the frozen checker does
```

Implement check2 by copying the frozen check() and repairing ONLY the
two comparisons (c2 target string sliced to 12 letters; c6 sorted
literal corrected to `[',', '.']`). Score' = count of True among the
same seven booleans.

Compute and write to w11-diagnostic.json:
- check2 for every solo poem and every braid final poem (report
  score', and per-constraint deltas vs frozen: which cells flipped).
- For each LOO record already in w11-results.json: re-check2 the
  stored fused poem; recompute LOCAL' = c1+c2', GLOBAL' = c3+c4+c5+c6'
  for fusion and for each of the four parents (parents = braid poems
  by k, re-check2'd); recompute p1'/p1'_strict/p2'/p2'_strict exactly
  as the primary definitions but on primed scores; counts p1'_count
  etc.; and per-constraint fused-vs-best-parent table.
- p3' = max braid score' >= mean braid score' + 1 (report numbers).
- A top-level note quoting: "diagnostic lens per REGISTRATION-sealed-
  amendment-1.md; primary numbers live in w11-results.json and are
  never replaced by these."

Include a self-test in __main__ before real work: the same synthetic
all-constraints poem (reconstruct it the same way you did in
w11_fusion.py) must score 7/7 under check2 with every cell True; and a
poem with one comma+one period but a mid-line capital must fail c6'.
Exit 2 with a message if any assert fails.

Run as `python3 w11_diagnostic.py`. When done with both jobs run:
`python3 -m py_compile w11_fusion.py w11_diagnostic.py && echo AMEND-ENGINE-OK`
