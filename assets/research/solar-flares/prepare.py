"""Select documented columns; preserve missing values and every event in the raw 2003 NOAA snapshot."""
import csv
from pathlib import Path
root = Path(__file__).resolve().parent
fields = ['time', 'start_time', 'end_time', 'flare_id', 'xrsb_irrad', 'flare_class',
          'xrsb_irrad_source', 'background_irrad', 'sequential_flare_num', 'peak_saturated']
with (root / 'raw-sci_xrsf-l2-flrpt_geo_y2003_v1-0-1.csv').open() as source:
    rows = [{key: row[key] for key in fields} for row in csv.DictReader(source)]
assert len(rows) == 3662 and sum(r['peak_saturated'] == '1' for r in rows) == 2
with (root / 'data.csv').open('w', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
