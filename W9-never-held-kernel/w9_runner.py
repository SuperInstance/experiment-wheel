#!/usr/bin/env python3
"""
W9 runner — THE NEVER-HELD KERNEL (sealed: REGISTRATION.md commit a6fa280)

Shapes (see registration):
  sh1 <yard>  — ensemble N=16, verbatim TASK, yards: claude|kimi|flash|wesley
  sh2 <yard>  — worksheet scaffold, 4 draws, yards: claude|kimi|flash|opencode
  sh3 <yard>  — attorney decomposition, 2 chains x 3 passes, yards: claude|kimi|flash|opencode
  sh4 <yard>  — c6 minimal-fix on committed seed, 4 draws, yards: claude|kimi|flash|opencode

Ledgers: ledgers/<shape>-<yard>.json (attempt-level, poems included, resume-safe).
Attempt cap: HARD 200 total model attempts across the station (ledgers/attempts.json).
No re-rolls of completed draws. Failures != draws. No model sees the checker:
opencode generation calls run in an empty scratch dir with a no-files instruction.
"""
import json, os, re, shutil, subprocess, sys, time, urllib.request, fcntl

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGERS = os.path.join(HERE, 'ledgers')
os.makedirs(LEDGERS, exist_ok=True)
SEED_BASE = 20260829
CAP = 200
WESLEY_SOFTSTOP_S = 180.0

from w9_check import TASK, check, c2_amended, c6_amended

# ---------------- attempt accounting (hard cap, multi-process safe) ----------------
def _with_lock(fn):
    lp = os.path.join(LEDGERS, '.attempts.lock')
    with open(lp, 'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            return fn()
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)

def _count_locked(kind, yard, note):
    p = os.path.join(LEDGERS, 'attempts.json')
    st = json.load(open(p)) if os.path.exists(p) else {'attempts': 0, 'log': []}
    st['attempts'] += 1
    st['log'].append({'t': round(time.time(), 1), 'kind': kind, 'yard': yard, 'note': str(note)[:140]})
    json.dump(st, open(p, 'w'), indent=1)
    n = st['attempts']
    if n >= CAP:
        print(f'!! attempt count {n} >= CAP {CAP} — this was the last allowed attempt', flush=True)
    return n

def count_attempt(kind, yard, note=''):
    return _with_lock(lambda: _count_locked(kind, yard, note))

def attempts_left():
    p = os.path.join(LEDGERS, 'attempts.json')
    st = json.load(open(p)) if os.path.exists(p) else {'attempts': 0, 'log': []}
    return CAP - st['attempts']

# ---------------- yards ----------------
KEY = re.search(r'export DEEPSEEK_API_KEY="([^"]+)"',
                open(os.path.expanduser('~/.bashrc')).read()).group(1).strip()

def flash(prompt, t=0.75):
    body = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
            "temperature": t, "max_tokens": 700}
    req = urllib.request.Request('https://api.deepseek.com/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())['choices'][0]['message']['content']

def wesley(prompt):
    body = {'model': 'granite3.1-dense:2b', 'prompt': prompt + '\n\n12 lines only:',
            'stream': False, 'options': {'temperature': 0.7, 'num_ctx': 4096}}
    r = urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/generate',
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300)
    return json.loads(r.read())['response']

def claude(prompt):
    return subprocess.run(['claude', '-p', prompt + ' Output ONLY the 12 lines.'],
                          capture_output=True, text=True, timeout=300).stdout

def kimi_last12(out):
    ls = [l for l in out.split('\n') if l.strip() and not l.startswith('•')]
    return '\n'.join(ls[-12:]) if len(ls) >= 12 else out

KIMI_BACKOFF = [60, 120, 240]
def kimi(prompt):
    """kimi -p ONLY. 403/rate-limit -> backoff retries (documented). Returns (text|None, tries)."""
    for i in range(len(KIMI_BACKOFF) + 1):
        if i > 0:
            print(f'   kimi backoff {KIMI_BACKOFF[i-1]}s before retry {i}', flush=True)
            time.sleep(KIMI_BACKOFF[i - 1])
        count_attempt('draw', 'kimi', f'try {i+1}')
        try:
            p = subprocess.run(['kimi', '-p', prompt + ' Output ONLY the 12 lines.'],
                               capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            print('   kimi TIMEOUT', flush=True); continue
        out = (p.stdout or '') + (p.stderr or '')
        bad = (p.returncode != 0 or not p.stdout or not p.stdout.strip()
               or '403' in out[:600] or 'rate limit' in out[:400].lower()
               or 'quota' in out[:400].lower())
        if not bad:
            return kimi_last12(p.stdout), i + 1
        print(f'   kimi rejected (rc={p.returncode}): {out[:160]!r}', flush=True)
    return None, len(KIMI_BACKOFF) + 1

OPENCODE_SCRATCH = '/tmp/w9-opencode-gen'
def opencode(prompt):
    """opencode run one-shot in an EMPTY scratch dir; no repo/checker visibility."""
    d = OPENCODE_SCRATCH
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d, exist_ok=True)
    full = ('Answer directly in your reply. Do NOT read, write, or search any files; '
            'no tools. Output only what is asked.\n\n' + prompt)
    p = subprocess.run(['opencode', 'run', '--auto', full], capture_output=True,
                       text=True, timeout=600, cwd=d)
    out = p.stdout.strip()
    if not out:
        raise RuntimeError(f'opencode empty (rc={p.returncode}): {(p.stderr or "")[:200]}')
    return out

def last12(out):  # generic fence-safe tail extraction (opencode decorations)
    ls = [l.strip() for l in out.split('\n') if l.strip()]
    ls = [l for l in ls if not l.startswith('```') and not l.startswith('#')]
    return '\n'.join(ls[-12:]) if len(ls) >= 12 else out

# ---------------- shapes ----------------
ROWS = ("Line 1: one word, begins with T\nLine 2: two words, begins with H\n"
        "Line 3: three words, begins with E\nLine 4: four words, begins with E\n"
        "Line 5: five words, begins with I\nLine 6: six words, begins with L\n"
        "Line 7: seven words, begins with E\nLine 8: eight words, begins with E\n"
        "Line 9: nine words, begins with N\nLine 10: ten words, begins with L\n"
        "Line 11: eleven words, begins with A\nLine 12: twelve words, begins with U")

EXTRA_RULES = ("3. Exactly one line contains a 12-character lowercase hex seal (like 8721b4bd042a). "
"That line's word count must equal (first two hex chars as a number mod 12) + 1. Choose your seal so it lands on a line you want.\n"
"4. No two lines may end with rhyming words.\n"
"5. The final line's last word must appear NOWHERE else in the poem.\n"
"6. Punctuation: exactly one comma and one period in the whole poem, no other punctuation; no capitals except the first letter of any line.")

SCAFFOLD = ("Write EXACTLY 12 lines of a poem called 'the chamber' by filling this worksheet EXACTLY "
"(all rows checked mechanically; they interlock — plan the whole poem before writing):\n" + ROWS +
"\nAdditional rules (checked mechanically):\n" + EXTRA_RULES +
"\nOutput ONLY the 12 lines (no row numbers).")

ATT_P1 = "Write EXACTLY 12 lines of a poem called 'the chamber'. You choose everything else. Output ONLY the 12 lines."
def ATT_P2(draft):
    return ("Rewrite each line of the poem below so it begins with the required letter and contains the required "
            "word count. Change NOTHING else.\n" + ROWS + "\n\nPOEM:\n" + draft + "\n\nOutput ONLY the 12 lines.")
def ATT_P3(draft):
    return ("Fix ONLY punctuation and capitalization in the poem below. Rules: exactly one comma and one period "
            "in the whole poem, no other punctuation; no capitals except the first letter of any line. "
            "Change NOTHING else.\n\nPOEM:\n" + draft + "\n\nOutput ONLY the 12 lines.")

def sh4_seed():
    """AMENDMENT-1 rule (sealed before SH-4): best-scoring SH-1 draw that FAILS c6'
    (a c6'-passing seed makes the fix-cell meaningless); fallback best >=3/6 any,
    then W7 ASC final."""
    best_fail, bf_s = None, -1
    best_any, ba_s = None, -1
    for yard in ('claude', 'kimi', 'flash', 'wesley'):
        p = os.path.join(LEDGERS, f'sh1-{yard}.json')
        if not os.path.exists(p): continue
        for d in json.load(open(p)).get('draws', []):
            if 'check' not in d: continue
            s = d['check']['score']
            if s > ba_s: ba_s, best_any = s, d['poem']
            if not c6_amended(d['poem']) and s > bf_s: bf_s, best_fail = s, d['poem']
    if best_fail is not None and bf_s >= 3:
        return best_fail, f'sh1 best c6\'-failing ({bf_s}/6)'
    if best_any is not None and ba_s >= 3:
        return best_any, f'sh1 best ({ba_s}/6)'
    w7 = json.load(open(os.path.join(HERE, '..', 'W7-ordered-braid', 'w7-results.json')))
    return w7['braid_ascending']['poem'], 'W7 ASC fallback (5/6)'

# ---------------- ledger plumbing ----------------
def ledger_path(shape, yard):
    return os.path.join(LEDGERS, f'{shape}-{yard}.json')

def load_ledger(shape, yard):
    p = ledger_path(shape, yard)
    return json.load(open(p)) if os.path.exists(p) else {}

def save_ledger(shape, yard, obj):
    obj['updated'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
    json.dump(obj, open(ledger_path(shape, yard), 'w'), indent=1, ensure_ascii=False)

def draw_block(poem, seed_tag, extra=None):
    c = check(poem)
    b = {'seed_tag': seed_tag, 'poem': poem, 'check': c, 'c2_amended': c2_amended(poem),
         'c6_amended': c6_amended(poem)}
    if extra: b.update(extra)
    return b

def gen_one(yard, prompt, seed_tag, tries_note=None):
    """One draw through one yard. Returns draw block or {'failed': ...}."""
    t0 = time.time()
    try:
        if yard == 'kimi':
            text, tries = kimi(prompt)
            if text is None:
                return {'failed': 'kimi rejected after backoff ladder', 'seed_tag': seed_tag}
            extra = {'tries': tries}
        else:
            count_attempt('draw', yard)
            fn = {'claude': claude, 'flash': flash, 'wesley': wesley, 'opencode': opencode}[yard]
            text = fn(prompt)
            if yard == 'opencode': text = last12(text)
            extra = {}
        if tries_note: extra.update(tries_note)
        extra['seconds'] = round(time.time() - t0, 1)
        return draw_block(text, seed_tag, extra)
    except Exception as e:
        return {'failed': f'{type(e).__name__}: {str(e)[:140]}', 'seed_tag': seed_tag,
                'seconds': round(time.time() - t0, 1)}

# ---------------- shape drivers ----------------
def run_sh1(yard):
    led = load_ledger('sh1', yard); draws = led.get('draws', [])
    stop = False
    for k in range(len(draws), 16):
        if stop or attempts_left() <= 0: break
        tag = SEED_BASE + k
        print(f'SH1 {yard} draw {k+1}/16 (seed {tag}) attempts_left={attempts_left()}', flush=True)
        d = gen_one(yard, TASK, tag)
        if yard == 'wesley' and d.get('seconds', 0) > WESLEY_SOFTSTOP_S:
            d['softstop_after'] = True; stop = True
        if 'failed' in d and yard == 'wesley':
            stop = True
        draws.append(d)
        led['draws'] = draws; led['shape'] = 'sh1'; led['yard'] = yard
        save_ledger('sh1', yard, led)
        s = d.get('check', {}).get('score', 'FAIL')
        print(f'   -> score {s}/6 c2\'={d.get("c2_amended")}', flush=True)
    led.setdefault('notes', []).append(f'done {len(draws)} draws' + (' (soft-stopped)' if stop else ''))
    save_ledger('sh1', yard, led)

def run_sh2(yard):
    led = load_ledger('sh2', yard); draws = led.get('draws', [])
    for k in range(len(draws), 4):
        if attempts_left() <= 0: break
        tag = SEED_BASE + 100 + k
        print(f'SH2 {yard} draw {k+1}/4 (seed {tag}) attempts_left={attempts_left()}', flush=True)
        d = gen_one(yard, SCAFFOLD, tag)
        draws.append(d); led['draws'] = draws; led['shape'] = 'sh2'; led['yard'] = yard
        save_ledger('sh2', yard, led)
        print(f'   -> score {d.get("check", {}).get("score", "FAIL")}/6', flush=True)
    save_ledger('sh2', yard, led)

def run_sh3(yard):
    led = load_ledger('sh3', yard); chains = led.get('chains', [])
    for ci in range(len(chains), 2):
        if attempts_left() <= 2: break
        tag_base = SEED_BASE + 200 + ci * 10
        passes = []
        d1 = gen_one(yard, ATT_P1, tag_base)
        passes.append({'pass': 'P1_content', **d1})
        print(f'SH3 {yard} chain {ci+1} P1 -> {d1.get("check", {}).get("score", "FAIL")}/6', flush=True)
        if 'failed' not in d1 and d1['check']['12_lines']:
            d2 = gen_one(yard, ATT_P2(d1['poem']), tag_base + 1)
            passes.append({'pass': 'P2_letters_counts', **d2})
            print(f'SH3 {yard} chain {ci+1} P2 -> {d2.get("check", {}).get("score", "FAIL")}/6', flush=True)
            if 'failed' not in d2 and d2['check']['12_lines']:
                d3 = gen_one(yard, ATT_P3(d2['poem']), tag_base + 2)
                passes.append({'pass': 'P3_formatting', **d3})
                print(f'SH3 {yard} chain {ci+1} P3 -> {d3.get("check", {}).get("score", "FAIL")}/6', flush=True)
            else:
                passes.append({'pass': 'P3_formatting', 'skipped': 'P2 failed/not 12 lines'})
        else:
            passes.append({'pass': 'P2_letters_counts', 'skipped': 'P1 failed/not 12 lines'})
            passes.append({'pass': 'P3_formatting', 'skipped': 'P1 failed/not 12 lines'})
        chains.append({'chain': ci + 1, 'passes': passes,
                       'final': passes[-1] if 'pass' in passes[-1] else None})
        led['chains'] = chains; led['shape'] = 'sh3'; led['yard'] = yard
        save_ledger('sh3', yard, led)
    save_ledger('sh3', yard, led)

def run_sh4(yard):
    led = load_ledger('sh4', yard); draws = led.get('draws', [])
    seed, src = sh4_seed()
    led['seed_source'] = src; led['seed_check'] = check(seed); led['seed_c2_amended'] = c2_amended(seed)
    led['seed_c6_amended'] = c6_amended(seed)
    for k in range(len(draws), 4):
        if attempts_left() <= 0: break
        tag = SEED_BASE + 300 + k
        print(f'SH4 {yard} draw {k+1}/4 (seed {tag}) attempts_left={attempts_left()}', flush=True)
        d = gen_one(yard, ATT_P3(seed), tag)
        if 'check' in d:
            d['c6_before'] = led['seed_check'].get('c6_punctuation')
            d['c6_after'] = d['check'].get('c6_punctuation')
            d['c6p_before'] = led.get('seed_c6_amended')
            d['c6p_after'] = d.get('c6_amended')
            d['c2p_before'] = led.get('seed_c2_amended')
            d['c2p_after'] = d.get('c2_amended')
            d['score_delta'] = d['check'].get('score', 0) - led['seed_check'].get('score', 0)
        draws.append(d); led['draws'] = draws; led['shape'] = 'sh4'; led['yard'] = yard
        save_ledger('sh4', yard, led)
        print(f'   -> c6 {d.get("c6_before")} -> {d.get("c6_after")} score {d.get("check", {}).get("score", "FAIL")}/6', flush=True)
    save_ledger('sh4', yard, led)

if __name__ == '__main__':
    shape, yard = sys.argv[1], sys.argv[2]
    {'sh1': run_sh1, 'sh2': run_sh2, 'sh3': run_sh3, 'sh4': run_sh4}[shape](yard)
    st = json.load(open(os.path.join(LEDGERS, 'attempts.json'))) if os.path.exists(os.path.join(LEDGERS, 'attempts.json')) else {'attempts': 0}
    print('DONE', shape, yard, '| attempts used:', st['attempts'])
