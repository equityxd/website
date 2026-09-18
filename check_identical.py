#!/usr/bin/env python3
"""Verify that the CUST CV keeps the v1 contact block + competencies grid byte-identical."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

v1 = open('source/SONG Ernest - CV v1.typ', encoding='utf8').read().splitlines()
cust = open('custom_cv/CV-20260912-0005_CV1.typ', encoding='utf8').read().splitlines()


def block_after(lines, start_marker, end_markers):
    i = next(k for k, l in enumerate(lines) if start_marker in l)
    j = i
    while j < len(lines):
        if any(em in lines[j] for em in end_markers):
            return lines[i:j + 1]
        j += 1
    return lines[i:]


# Contact block: from "BLOCK 2" comment until the full-width rule line
contact_v1 = block_after(v1, 'BLOCK 2', ['#line(length: 100%, stroke: (thickness: 0.75pt))'])
contact_cust = block_after(cust, 'BLOCK 2', ['#line(length: 100%, stroke: (thickness: 0.75pt))'])
print('CONTACT BLOCK byte-identical:', contact_v1 == contact_cust)
if contact_v1 != contact_cust:
    import difflib
    for l in difflib.unified_diff(contact_v1, contact_cust, 'v1', 'cust', lineterm=''):
        print('  ' + l)

# Competencies grid: from "Column 2 : Competencies" to the grid's closing bracket
def grid_after(lines, start_marker):
    i = next(k for k, l in enumerate(lines) if start_marker in l)
    # find the '#grid(' then capture until the matching '          ]\n'
    g = next(k for k in range(i, len(lines)) if lines[k].startswith('        #grid('))
    j = g + 1
    while j < len(lines) and not lines[j].startswith('          ]'):
        j += 1
    return lines[i:j + 1]


grid_v1 = grid_after(v1, 'Column 2 : Competencies')
grid_cust = grid_after(cust, 'Column 2 : Competencies')
print('COMPETENCIES GRID byte-identical:', grid_v1 == grid_cust)
if grid_v1 != grid_cust:
    import difflib
    for l in difflib.unified_diff(grid_v1, grid_cust, 'v1', 'cust', lineterm=''):
        print('  ' + l)
