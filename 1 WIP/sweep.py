import re, subprocess, os, io, sys

with open("SONG Ernest - CV v1.typ", encoding="utf-8") as f:
    orig = f.read()

def overflow_at(contact, size):
    cpat = re.compile(r"columns:\s*\(\s*[0-9.]+fr,\s*[0-9.]+fr\s*\)")
    new = cpat.sub("columns: (%.2ffr, %.2ffr)" % (contact, 4.0 - contact), orig, count=1)
    new = re.sub(r'#text\(size: [0-9.]+pt', "#text(size: %fpt" % (size), new, count=1)
    open("sweep.tmp.typ","w",encoding="utf-8").write(new)
    if os.path.exists("sweep.tmp.pdf"):
        try: os.remove("sweep.tmp.pdf")
        except OSError: pass
    subprocess.run(["typst","compile","sweep.tmp.typ","sweep.tmp.pdf"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists("sweep.tmp.pdf"):
        return None
    import pymupdf
    page = pymupdf.open("sweep.tmp.pdf")[0]
    x1max = 0.0
    for block in page.get_text('dict')['blocks']:
        for line in block['lines']:
            x0,y0,x1,y1 = line['bbox']
            if 60 <= y0 <= 116:
                x1max = max(x1max, x1)
    return x1max - 566.55

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
for contact in [0.8, 1.0, 1.2]:
    for size in [5.0, 5.5, 6.0]:
        ov = overflow_at(contact, size)
        if ov is None:
            print("contact=%.2f size=%g -> COMPILE-ERROR" % (contact, size))
        else:
            print("contact=%.2f size=%g -> overflow=%.2f" % (contact, size, ov))
