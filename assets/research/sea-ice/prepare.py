"""Derive the teaching CSV from the two unmodified NSIDC snapshots beside this file."""
import csv
from pathlib import Path
root = Path(__file__).resolve().parent
rows = []
for month in (3, 9):
    with (root / f'raw-N_{month:02}_extent_v4.0.csv').open() as source:
        for raw in csv.DictReader(source, skipinitialspace=True):
            row = {k.strip(): v.strip() for k, v in raw.items()}
            if 1979 <= int(row['year']) <= 2024:
                rows.append({'year': int(row['year']), 'month': int(row['mo']),
                             'extent_million_km2': '' if float(row['extent']) < 0 else float(row['extent']),
                             'area_million_km2': '' if float(row['area']) < 0 else float(row['area']),
                             'source_dataset': row['source_dataset']})
rows.sort(key=lambda r: (r['month'], r['year']))
assert len(rows) == 92 and len({(r['year'], r['month']) for r in rows}) == 92
with (root / 'data.csv').open('w', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
