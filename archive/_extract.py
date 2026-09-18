import zipfile, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def docx_text(path):
    z=zipfile.ZipFile(path)
    data=z.read('word/document.xml').decode('utf-8')
    text=re.sub(r'<w:t[^>]*>(.*?)</w:t>', lambda m: m.group(1), data)
    text=re.sub(r'</w:p>\s*', '\n', text)
    text=re.sub(r'<[^>]+>', '', text)
    return text

path = sys.argv[1]
print(docx_text(path))
