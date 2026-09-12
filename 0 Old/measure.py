import sys, pymupdf
pdf = sys.argv[1]
doc = pymupdf.open(pdf)
page = doc[0]
print('page content region: x 24 .. 566.55 (width 542.55)')
for block in page.get_text('dict')['blocks']:
    for line in block['lines']:
        full = ''.join(span['text'] for span in line['spans'])
        x0, y0, x1, y1 = line['bbox']
        tag = ''
        if 'Rue' in full or 'B-1000' in full or 'globe' in full or 'device-mobile' in full:
            tag = '<CONTACT>'
        elif len(full) > 40:
            tag = '<QUOTE>'
        if tag:
            safe = full.encode('ascii', 'ignore').decode('ascii')
            print('%-8s x=%.1f-%.1f y=%.1f  |%s|' % (tag, x0, x1, y0, safe[:60]))
