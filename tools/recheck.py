import os, re, sys, glob
root = sys.argv[1]
W = os.path.join(root, 'wiki'); R = os.path.join(root, 'raw')
raws = {os.path.basename(p)[:2]: open(p, encoding='utf-8').read().replace('\xa0', ' ').lower() for p in glob.glob(os.path.join(R, '*.md'))}
pairs = {
    'Tommy Vercetti': 'vercetti', '東歐': 'eastern europe', '重啟': 'reboot', 'CJ': r'carl|cj', 'Google Maps': 'google maps',
    '人口普查': 'census', 'Bonnie': 'bonnie', '不說話': 'silent', '健身房': 'gym', 'Freedom from Torture': 'freedom from torture',
    '政治評論': 'political commentary', '品味不佳': 'poor taste', '幫派尊重度': r'respect|loyalty', '第 8 部': 'eighth',
    '雙主角': 'duo', '分開行動': 'split', 'Rockstar North 開發': 'rockstar north', '角色創建': 'character', '第 10 屆': '10th',
}
bad = 0; checked = 0
for p in sorted(glob.glob(os.path.join(W, '**', '*.md'), recursive=True)):
    rel = os.path.relpath(p, W).replace('\\', '/')
    if rel in ('index.md', 'log.md') or rel.startswith('sources/'):
        continue
    for ln, line in enumerate(open(p, encoding='utf-8').read().split('\n'), 1):
        pos = 0
        for m in re.finditer(r'((?:\[raw/\d{2}\])+)', line):
            ids = sorted(set(re.findall(r'\d{2}', m.group(1))))
            seg = line[pos:m.start()]; pos = m.end()
            for zh, en in pairs.items():
                if zh in seg:
                    checked += 1
                    for i in ids:
                        if not re.search(en, raws[i]):
                            bad += 1
                            print(f'MISSING: {rel}:{ln} term "{zh}" cited raw/{i} lacks "{en}" | ...{seg[-60:]}')
print('checked', checked, 'missing', bad)
