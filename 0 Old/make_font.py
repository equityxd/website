from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.name_table import Name
import os

woff = 'node_modules/@fontsource/source-sans-3/files/source-sans-3-latin-400-normal.woff'
out = 'C:/MyDev/MyCV/Temp/SourceSans3-Regular.ttf'

font = TTFont(woff)
# ensure a name table with family + full name so typst can resolve "Source Sans 3"
if 'name' not in font:
    from fontTools.ttLib.tables name_table  # placeholder
nt = font.getOrCreateName()
nt.names = []
nt.append(3, 1, 0x0409, 0, 1, 'Source Sans 3')       # family name
nt.append(3, 1, 0x0409, 0, 4, 'Source Sans 3 Regular')  # full name
font.save(out)
print('wrote', os.path.getsize(out), 'bytes')
# verify
t = TTFont(out)
for n in t['name'].table.names:
    print('nameID', n.nameID, '=>', n.get_text())
