import os, re, sys, glob
root = sys.argv[1]
W = os.path.join(root, 'wiki')
out = []
n = 0
for p in sorted(glob.glob(os.path.join(W, '**', '*.md'), recursive=True)):
    rel = os.path.relpath(p, W).replace('\\', '/')
    name = os.path.splitext(os.path.basename(p))[0]
    if name in ('index', 'log') or rel.startswith('sources/'):
        continue
    txt = open(p, encoding='utf-8').read()
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    for ln, line in enumerate(body.split('\n'), 1):
        pos = 0
        for m in re.finditer(r'((?:\[raw/\d{2}\])+)', line):
            ids = sorted(set(re.findall(r'\d{2}', m.group(1))))
            seg = line[pos:m.start()]
            pos = m.end()
            if len(ids) >= 2:
                n += 1
                s = re.sub(r'\[raw/\d{2}\]', '', seg).strip(' -|')
                out.append(f'{n:02d} {rel} :: {s[-170:]} :: {ids}')
print('\n'.join(out))
