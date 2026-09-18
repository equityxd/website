#!/usr/bin/env python3
"""Compare exact vertical positions of text on page 1 between v1 and CUST."""
import sys, os, pymupdf
sys.stdout.reconfigure(encoding='utf-8')


def positions(path):
    pdf = pymupdf.open(path); pg = pdf[0]
    out = []
    for blk in pg.get_text('dict')['blocks']:
        if blk.get('type', 0) != 0:
            continue
        for ln in blk['lines']:
            for span in ln['spans']:
                b = span['bbox']
                txt = span['text'].strip()
                if not txt or txt in ('1 of 1', 'Competencies'):
                    continue
                y = round((b[1] + b[3]) / 2, 2)
                x = round(b[0], 2)
                out.append((y, x, txt[:55], round(span['size'], 1)))
    out.sort(key=lambda r: (r[0], r[1]))
    return out


v1 = positions('./v1_fresh.pdf') if os.path.exists('./v1_fresh.pdf') else None
if v1 is None:
    os.system('typst compile "source/SONG Ernest - CV v1.typ" ./v1_fresh.pdf >/dev/null 2>&1')
    v1 = positions('./v1_fresh.pdf')
cust = positions('custom_cv/CV-20260912-0005_CV1.pdf')

vy = sorted(set(round(v[0], 2) for v in v1))
print(f"{'Y':>7} {'v1_x':>7} {'v1_text':<52} {'|':<3} {'cust_x':>7} {'cust_text':<52} {'MATCH'}")
print('=' * 150)
matches = 0
tot = 0
for y in vy[:25]:
    vx = [v for v in v1 if abs(v[0] - y) < 0.75]
    cx = [c for c in cust if abs(c[0] - y) < 0.75]
    if not vx:
        continue
    v = vx[0]; c = cx[0] if cx else None
    tot += 1
    if c is not None and abs(v[1] - c[1]) < 0.5 and v[2] == c[2] and abs(v[3] - c[3]) < 0.5:
        matches += 1
        m = 'ok '
    else:
        m = '!!'
    vxf = f'{v[1]:7.2f}'
    cxf = f'{c[1]:7.2f}' if c else '----'
    vxf2 = f'{v[3]:4}pt'
    cxf2 = f'{c[3]:4}pt' if c else '----'
    print(f'{y:7.2f} {vxf}   {v[2]:<52} | {cxf}   {c[2] if c else "----":<52} {m} {vxf2}/{cxf2}' if c else f'{y:7.2f} {vxf}   {v[2]:<52} | {"----":<7} {"----":<52} !!')
print(f'\n{matches}/{tot} top lines match exactly (x, text, size)')
