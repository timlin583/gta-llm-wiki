import os, re, sys, glob, collections
root = sys.argv[1]
W = os.path.join(root, 'wiki')
R = os.path.join(root, 'raw')

def norm(t):
    return t.replace('\xa0', ' ').replace('‍', '').replace('​', '')

pages = {}
for p in glob.glob(os.path.join(W, '**', '*.md'), recursive=True):
    name = os.path.splitext(os.path.basename(p))[0]
    pages[name] = (os.path.relpath(p, W).replace('\\', '/'), open(p, encoding='utf-8').read())

raws = {}
for p in sorted(glob.glob(os.path.join(R, '*.md'))):
    n = os.path.basename(p)[:2]
    raws[n] = norm(open(p, encoding='utf-8').read())

link_re = re.compile(r'\[\[([^\]]+)\]\]')
tag_re = re.compile(r'\[raw/(\d{2})\]')

print('PAGES:', len(pages), {k: sum(1 for v in pages.values() if v[0].startswith(k + '/')) for k in ['games', 'concepts', 'entities', 'sources']})

# A. structural
inbound = collections.defaultdict(set)
broken = []
for name, (rel, txt) in pages.items():
    for t in link_re.findall(txt):
        if t not in pages:
            broken.append((rel, t))
        elif t != name:
            inbound[t].add(name)
print('\n== A1 ORPHANS (no inbound besides index/log)')
for name, (rel, _) in sorted(pages.items()):
    if name in ('index', 'log'):
        continue
    src = inbound[name] - {'index', 'log'}
    if not src:
        print('  ', rel)
print('== A2 BROKEN LINKS:', sorted(set(broken)))
idx = pages['index'][1]
print('== A3 NOT IN INDEX:', [rel for n, (rel, _) in pages.items() if n not in ('index', 'log') and f'[[{n}]]' not in idx])

print('\n== A4 raw files vs source pages')
for n in raws:
    sp = [k for k in pages if k.startswith(n + '-')]
    cited_by = [rel for k, (rel, t) in pages.items() if k not in ('index', 'log') and not rel.startswith('sources/') and f'[raw/{n}]' in t]
    print(f'  raw/{n}: source page={bool(sp)}, cited by {len(cited_by)} non-source pages')

print('\n== B FRONTMATTER sources vs body tags')
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log'):
        continue
    m = re.search(r'sources: \[(.*?)\]', txt)
    fm = set(re.findall(r'raw/(\d{2})-', m.group(1))) if m else set()
    body_tags = set(tag_re.findall(txt))
    extra = body_tags - fm
    missing = fm - body_tags
    if extra or missing:
        print(f'  {rel}: body cites but not in frontmatter={sorted(extra)}; frontmatter but never cited in body={sorted(missing)}')

# C. combined citation triage
def tokens(seg):
    toks = set()
    for m in re.finditer(r'\d[\d,]*\.?\d*', seg):
        s = m.group(0).replace(',', '')
        if len(s.replace('.', '')) >= 3:
            toks.add(s)
    for m in re.finditer(r"[A-Za-z][A-Za-z'’\-]{3,}", seg):
        toks.add(m.group(0))
    return toks

stop = {'raw', 'Metacritic', 'GameRankings', 'million', 'billion', 'Online', 'Grand', 'Theft', 'Auto'}
print('\n== C COMBINED CITATIONS: segments with >=2 distinct raw tags whose checkable tokens are missing from at least one cited raw')
flag_count = 0
total_comb = 0
rows = []
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    for ln_no, line in enumerate(body.split('\n'), 1):
        pos = 0
        for m in re.finditer(r'((?:\[raw/\d{2}\])+)', line):
            cluster = m.group(1)
            ids = sorted(set(re.findall(r'\d{2}', cluster)))
            seg = line[pos:m.start()]
            pos = m.end()
            if len(ids) < 2:
                continue
            total_comb += 1
            toks = {t for t in tokens(seg) if t not in stop and not t.startswith('http')}
            if not toks:
                continue
            miss = {}
            for i in ids:
                rawtxt = raws.get(i, '')
                low = rawtxt.lower()
                mm = [t for t in toks if (t.lower() not in low)]
                if mm:
                    miss[i] = mm
            if miss:
                flag_count += 1
                rows.append((rel, seg.strip()[-90:], ids, miss))
print(f'  total combined-tag segments: {total_comb}; flagged (some token missing in some cited raw): {flag_count}')
for rel, seg, ids, miss in rows:
    print(f'  {rel} | ...{seg} | tags={ids} | missing={ {k: v[:6] for k, v in miss.items()} }')

# D. unsourced numeric lines
print('\n== D UNSOURCED FACT LINES (digit present, no [raw/ tag, no 待查), excluding headings/links-only/slide suggestions)')
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    sec = ''
    for ln_no, line in enumerate(body.split('\n'), 1):
        s = line.strip()
        if s.startswith('#'):
            sec = s
            continue
        if not s or s.startswith('|---') or s.startswith('>'):
            continue
        if '簡報素材' in sec or '相關頁' in sec:
            continue
        if re.search(r'\d', s) and '[raw/' not in s and '待查' not in s and not re.fullmatch(r'[-\s\[\]A-Za-z0-9一-鿿、，；：（）()／/ ]*\[\[.*', s):
            if re.search(r'\[\[', s) and len(re.sub(r'\[\[[^\]]*\]\]', '', s).strip('-、，；：\s ')) < 6:
                continue
            print(f'  {rel}: {s[:110]}')

# E. 截至 dates
print('\n== E 截至 DATE USAGE')
cnt = collections.Counter()
for name, (rel, txt) in sorted(pages.items()):
    if name == 'log':
        continue
    for d in re.findall(r'截至 (\d{4}(?:-\d{2}(?:-\d{2})?)?(?: 年 \d+ 月)?)', txt):
        cnt[d] += 1
print('  ', dict(cnt))
print('  GTA VI page 截至 2026-11-18 count:', pages['GTA VI'][1].count('截至 2026-11-18'))

# F. game pages
print('\n== F GAME PAGES: 待查 count, per-section 待查')
fields = ['## 1.', '## 2.', '## 3.', '## 4.', '## 5.', '## 6.', '## 7.', '## 8.']
for name, (rel, txt) in sorted(pages.items()):
    if not rel.startswith('games/'):
        continue
    missing = [f for f in fields if f not in txt]
    srcs = re.search(r'sources: \[(.*?)\]', txt).group(1)
    nsrc = len(re.findall(r'raw/\d{2}', srcs))
    secs = re.split(r'\n(?=## )', txt)
    pend = {}
    for s in secs:
        h = s.split('\n', 1)[0][:14]
        c = s.count('待查')
        if c:
            pend[h] = c
    era = '時代]]' in txt
    print(f'  {rel}: missing={missing} sources={nsrc} 待查={txt.count("待查")} {pend} era_link={era}')

# H. contradictions
print('\n== H CONTRADICTION MARKERS (⚠) per page; lines saying 並陳 without ⚠')
for name, (rel, txt) in sorted(pages.items()):
    if name == 'log':
        continue
    n = txt.count('⚠')
    bad = [l.strip()[:70] for l in txt.split('\n') if '並陳' in l and '⚠' not in l and not l.strip().startswith('|')]
    if n or bad:
        print(f'  {rel}: ⚠={n}; 並陳 w/o ⚠: {len(bad)}')
        for b in bad[:3]:
            print('       ', b)

# J. superlatives w/o 截至
print('\n== J SUPERLATIVES/RANKINGS without 截至 (and not tied to an explicit year/date on the line)')
sup = re.compile(r'史上|最高分|最暢銷|最快|最成功|最大|最貴|第[0-9一二三四五]+(?:高|名)|並列第|排第|首次|第一款|第一位')
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    for line in txt.split('\n'):
        if sup.search(line) and '截至' not in line and '[raw/' in line:
            if re.search(r'(19|20)\d{2}', line):
                continue
            print(f'  {rel}: {line.strip()[:105]}')

# I. terms
print('\n== I TERMS: first occurrence not followed by a parenthetical/colon explanation (page-level heuristic)')
terms = ['開放世界', '沙盒', '資料片', 'HUD', '引擎', 'DLC', 'ESRB', 'Metacritic', 'GameRankings', 'mod', '預載', '第三人稱', '第一人稱', 'GTA clone', '宇宙', '限時獨占', '移植', '重製版', '外傳', '分級', '主線', '支線', 'heist', '搶案', 'NPC', '內購', '動態捕捉', '重啟']
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    out = []
    for t in terms:
        i = body.find(t)
        if i < 0:
            continue
        window = body[i:i + len(t) + 45]
        if '（' not in window[len(t):len(t)+3] and '：' not in window[len(t):len(t)+2] and '(' not in window[len(t):len(t)+3]:
            out.append(t)
    if out:
        print(f'  {rel}: {out}')

# K. log structure
print('\n== K LOG ENTRIES')
lg = pages['log'][1]
for m in re.finditer(r'^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \| (.*)$', lg, re.M):
    print('  ', m.group(1), m.group(2), '|', m.group(3)[:60])
blank_manual = lg.count('- 人工檢查：…（由使用者補寫）')
print('  ingest entries with unfilled 人工檢查 placeholder:', blank_manual)
