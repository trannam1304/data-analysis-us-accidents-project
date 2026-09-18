import json
import sys

with open('notebooks/01_data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('nb1_dump.txt', 'w', encoding='utf-8') as out:
    for i, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if any(k in source.lower() for k in ['drop', 'usecols', 'keep', 'select']):
            out.write(f"\n=== Cell {i} ({cell['cell_type']}) ===\n")
            out.write(source + "\n")
