# SPEC for w11_fusion.py (W11 phase 2 — mechanical engine, ZERO model calls)

You are writing a standalone mechanical Python script. Stdlib only, no
network, deterministic. It implements EXACTLY the rules below — do not
improve, repair, reinterpret, or extend them. The poems it processes are
model outputs; it must never modify, "fix", or reflow any line. It only
selects, inherits, and scores.

## Input

Reads `w11-braids.json` in the same directory. Relevant structure:
- `solo`: {yard: {check: {...}, poem: str}}
- `braids`: list of {k: int (1..5), order: [...], trace: [...], check: {...}, poem: str}
- `braid_scores`: [int x5], `best_solo`: int

## Embedded checker (VERBATIM — copy character-for-character, do not touch)

```python
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
```

## Definitions (frozen by registration)

- `extract_lines(poem)`: the checker's own extraction — `[l.strip() for l in poem.strip().split('\n') if l.strip()]`, then drop lines starting with `#` or ` ``` `.
- `qualifies(n, line)`: `len(line.split()) == n` AND `line[0].upper() == 'THEEILEENLAUN'[n-1]` (n is 1-based; line non-empty by construction).
- LOCAL score of a check dict = int(c1_growth) + int(c2_acrostic). GLOBAL score = int(c3_seal) + int(c4_no_rhyme) + int(c5_last_word_unique) + int(c6_punctuation).
- Parent list: for each braid, RECOMPUTE `sc = check(braid['poem'])` from the poem (do not trust stored checks; store both and note any mismatch). A parent ABSTAINS iff `len(extract_lines(poem)) != 12` — it provides no line candidates and is excluded from ranking entirely. Expected: none abstain.
- Parent ranking key: `(-score, k)` — higher score first; ties → lower k. Frozen.

## FUSION rule (frozen)

`fuse(parents)` where parents = list of dicts {k, poem, score} (all
non-abstaining):
1. Rank parents by (-score, k). For n in 1..12:
2. Walk the ranked parents in order; the first parent whose extracted
   line n `qualifies(n, line)` DONATES line n (record provenance:
   source k, qualified=True).
3. If no parent's line n qualifies: the TOP-RANKED parent donates its
   line n outright (provenance: source k, qualified=False).
4. Fused poem = '\n'.join(the 12 chosen lines). Return poem + full
   provenance list. No repair, no whitespace changes, no dedup.

## Aggregations to compute

1. `selection`: best braid by (-score, k) over all five — report its k,
   score, and poem (descriptive: selection ties the best braid by
   construction).
2. `fusion_all5`: fuse(all five parents) — descriptive.
3. LEAVE-ONE-OUT (the pre-registered instrument): for held_out k in
   1..5, parents = the other four braids. Compute:
   - fused poem, `fused_check = check(fused)`, fusion_local,
     fusion_global, provenance per line (and how many lines were
     fallbacks).
   - best_parent = max(parents, key=(-score, k)); parent_local,
     parent_global of that best parent.
   - `p1` = fusion_local >= parent_local + 1
     `p1_strict` = fusion_local >= max(all four parents' local) + 1
   - `p2` = fusion_global <= parent_global
     `p2_strict` = fusion_global <= max(all four parents' global)
   - per-constraint deltas: for each of the six constraints, whether
     fused holds it, and whether best parent holds it.
4. `p1_count` = #LOO with p1 True; same for p1_strict, p2, p2_strict.
5. `p3` = (max braid score) >= (mean of the five braid scores) + 1
   (report both numbers; floats allowed in the mean).

## Output

Write `w11-results.json` containing: input solo/braid summaries
(recomputed scores + any stored-vs-recomputed mismatch notes),
selection, fusion_all5 (poem + check + provenance), all five LOO
records, the four counts, p3 detail. Also print a compact human summary
to stdout: per LOO — held-out k, parent scores, best parent k/local/
global, fusion score/local/global, p1/p2 flags; then the counts and p3.

## Self-test before use (include in __main__ before real work)

- verify the embedded check() on a 12-line synthetic poem that holds
  ALL SIX constraints (construct one: line n has n words, first letters
  spelling THEEILEENLAUN, one line containing `8721b4bd042a` chosen so
  its mod-12 coupling matches that line's word count — e.g. put it on a
  line where you pick the first two hex chars so `int(hex[:2],16)%12+1`
  equals n; one comma and one period total and capitals ONLY as first
  letters of lines; all line-final two-letter clusters distinct; last
  word unique) — assert score==7 and every constraint True. Then assert
  the frozen-rule function `fuse` on a two-parent toy case picks the
  qualifying line from the higher-scoring parent and falls back to the
  top-ranked parent when nothing qualifies. If any assert fails, exit 2
  with a clear message.

Run as `python3 w11_fusion.py`. No CLI args. Exit 0 on success.
