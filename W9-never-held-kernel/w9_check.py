#!/usr/bin/env python3
"""
W9 checker - W6b/W7 check() reused BYTE-IDENTICAL for comparability;
written by opencode, reviewed by W9.
"""
import re

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
