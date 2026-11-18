import os, re, sys, glob, collections
root = sys.argv[1]
W = os.path.join(root, 'wiki')
pages = {}
for p in glob.glob(os.path.join(W, '**', '*.md'), recursive=True):
    name = os.path.splitext(os.path.basename(p))[0]
    pages[name] = (os.path.relpath(p, W).replace('\\', '/'), open(p, encoding='utf-8').read())

link_re = re.compile(r'\[\[([^\]]+)\]\]')
inbound = collections.defaultdict(set)
broken = []
for name, (rel, txt) in pages.items():
    for t in link_re.findall(txt):
        if t not in pages:
            broken.append((rel, t))
        elif t != name:
            inbound[t].add(name)

print('== 1. ORPHANS (no inbound from any page except index/log)')
for name, (rel, _) in sorted(pages.items()):
    if name in ('index', 'log'):
        continue
    src = inbound[name] - {'index', 'log'}
    if not src:
        print('  ORPHAN', rel, '(index only)' if 'index' in inbound[name] else '(not even index)')
print('== 1b. BROKEN LINKS')
for b in sorted(set(broken)):
    print('  BROKEN', b)
print('== 1c. NOT IN INDEX')
idx = pages['index'][1]
for name, (rel, _) in sorted(pages.items()):
    if name not in ('index', 'log') and f'[[{name}]]' not in idx:
        print('  NOT IN INDEX', rel)

print('== 2. UNSOURCED FACT LINES (has digit, no [raw/ tag) excluding headings/frontmatter/simple meta)')
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    for i, line in enumerate(body.split('\n')):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('|---'):
            continue
        if re.search(r'\d', s) and '[raw/' not in s and '待查' not in s:
            print(f'  {rel}: {s[:110]}')

print('== 3. CONTRADICTION MARKERS (⚠)')
for name, (rel, txt) in sorted(pages.items()):
    if name == 'log':
        continue
    n = txt.count('⚠')
    if n:
        print(f'  {rel}: {n}')

print('== 4. 截至 DATES')
for name, (rel, txt) in sorted(pages.items()):
    if name == 'log':
        continue
    ds = re.findall(r'截至 (\d{4}(?:-\d{2})?(?:-\d{2})?|\d{4} 年 \d+ 月)', txt)
    if ds:
        print(f'  {rel}: {collections.Counter(ds).most_common()}')

print('== 5. GAME PAGES: fields + 待查 count + sources')
fields = ['## 1.', '## 2.', '## 3.', '## 4.', '## 5.', '## 6.', '## 7.', '## 8.']
for name, (rel, txt) in sorted(pages.items()):
    if not rel.startswith('games/'):
        continue
    missing = [f for f in fields if f not in txt]
    srcs = re.search(r'sources: \[(.*?)\]', txt).group(1)
    nsrc = len([s for s in srcs.split(',') if s.strip()])
    print(f'  {rel}: missing={missing} 待查={txt.count("待查")} sources={nsrc} era_link={"時代]]" in txt}')

print('== 6. TERMS: first occurrence explained? (heuristic: followed by （ within 40 chars, or explained in a nearby clause)')
terms = ['開放世界', '沙盒', '資料片', 'HUD', '引擎', 'DLC', 'ESRB', 'Metacritic', 'GameRankings', 'mod', '預載', '第三人稱', '第一人稱', 'GTA clone', '宇宙', '限時獨占', '移植', '重製版', '外傳', '分級', '主線', '支線', 'heist', '搶案']
for name, (rel, txt) in sorted(pages.items()):
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    out = []
    for t in terms:
        i = body.find(t)
        if i < 0:
            continue
        window = body[i:i + len(t) + 40]
        if '（' not in window and '：' not in window[len(t):len(t)+3]:
            out.append(t)
    if out:
        print(f'  {rel}: {out}')
