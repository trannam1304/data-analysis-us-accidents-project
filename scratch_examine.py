import json
import sys

with open('notebooks/02_descriptive_diagnostic.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('nb2_dump.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total cells: {len(nb['cells'])}\n")
    for i, cell in enumerate(nb['cells']):
        out.write(f"\n==================== CELL {i} ({cell['cell_type']}) ====================\n")
        source = ''.join(cell['source'])
        out.write(source + "\n")

