#!/usr/bin/env python3
"""Sync canonical evidence without losing the visual catalogue's existing layout."""
import argparse, json
from pathlib import Path
D=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',required=True)
p.add_argument('--workbook-version',required=True,type=int)
p.add_argument('--as-of',required=True)
a=p.parse_args()
source=json.loads(Path(a.source).read_text())
if not isinstance(source,list):raise SystemExit('Canonical source must be a JSON list of records')
data=json.loads((D/'catalogue-data.json').read_text())
byid={r['id']:r for r in source}
if len(byid)!=len(source):raise SystemExit('Duplicate canonical IDs')
if set(byid)!={r['id'] for r in data['rows']}:raise SystemExit('Record ID sets differ. Add new verified versions and previews first; never silently remove history.')
for old in data['rows']:
    record=byid[old['id']]
    if record.get('tmj_url') and not record['tmj_url'].startswith('https://'):raise SystemExit('Unexpected TMJ URL')
    visual={k:old[k] for k in ['row','asset','caption','catalogue_review_note'] if k in old}
    fallback_version=old.get('version')
    old.clear();old.update(record);old.update(visual)
    if not old.get('version') and fallback_version:old['version']=fallback_version
snapshot=Path('sources')/f'testing-workbook-v{a.workbook_version}.json'
(D/snapshot).write_text(json.dumps(source,indent=2,ensure_ascii=False))
data.update(as_of=a.as_of,source_workbook_version=a.workbook_version,source_workbook_path=str(snapshot))
(D/'catalogue-data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
print(f'Synced {len(source)} records. Rebuild and visually inspect every page before replacing Library files.')
