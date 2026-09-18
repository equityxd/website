from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.name_table import Name
import os

path = 'C:/MyDev/MyCV/Temp/SourceSans3-Regular.ttf'
font = TTFont(path)
nt = font['name'].table
nt.names = []
nt.names.append(Name(3, 1, 0x0409, 0, 1, 'Source Sans 3'))       # family
nt.names.append(Name(3, 1, 0x0409, 0, 4, 'Source Sans 3 Regular'))  # full
font.save(path)
print('fixed names; size', os.path.getsize(path))
for n in nt.names:
    print('nameID', n.nameID, '=>', n.get_text())
