import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_path, json_path, limit=None):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            rows.append({
                'title': row.get('title') or row.get('Title') or '',
                'genre': row.get('genre') or row.get('Genre') or '',
                'year': row.get('year') or row.get('Year') or '',
                'description': row.get('description') or row.get('Description') or '',
            })
    with open(json_path, 'w', encoding='utf-8') as out:
        json.dump(rows, out, indent=2, ensure_ascii=False)
    print(f'Wrote {len(rows)} records to {json_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python csv_to_json.py path/to/movies_initial.csv path/to/movies.json [limit]')
        sys.exit(1)
    csv_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2])
    limit = int(sys.argv[3]) if len(sys.argv) >= 4 else None
    csv_to_json(csv_path, json_path, limit)
