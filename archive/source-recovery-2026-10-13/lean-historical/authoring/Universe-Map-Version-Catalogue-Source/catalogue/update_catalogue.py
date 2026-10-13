#!/usr/bin/env python3
"""Merge a verified canonical row and its source preview without editing prior versions."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--row-json',required=True,help='One canonical testing-sheet row as JSON')
p.add_argument('--image',required=True,help='Exact existing source preview; no image is invented')
p.add_argument('--family',required=True)
p.add_argument('--caption',required=True)
p.add_argument('--make-latest',action='store_true')
p.add_argument('--as-of',required=True)
a=p.parse_args(); row=json.loads(Path(a.row_json).read_text());data=json.loads((D/'catalogue-data.json').read_text());provenance=json.loads((D/'asset-provenance.json').read_text())
required=['id','title','version','decision','source_validation','live_playtest','publication']
for field in required:
 if field not in row:raise SystemExit('Missing canonical field: '+field)
if row.get('tmj_url') and not row['tmj_url'].startswith('https://'):raise SystemExit('A published TMJ must use the exact HTTPS URL in the canonical sheet')
existing=next((r for r in data['rows'] if r['id']==row['id']),None)
number=existing['row'] if existing else max(r['row'] for r in data['rows'])+1
src=Path(a.image);im=Image.open(src).convert('RGB');native=list(im.size);im.thumbnail((1200,1000),Image.Resampling.LANCZOS);asset=Path('assets')/f'{number:02d}-{row["id"]}.jpg';im.save(D/asset,quality=76,subsampling=0,optimize=True)
row.update(row=number,asset=str(asset),caption=a.caption)
if existing:existing.update(row)
else:data['rows'].append(row)
f=next((f for f in data['families'] if f['name']==a.family),None)
if f is None:
 f={'name':a.family,'rows':[number],'latest':number,'archived':False};data['families'].insert(next((i for i,x in enumerate(data['families']) if x['archived']),len(data['families'])),f)
elif number not in f['rows']:f['rows'].append(number)
if a.make_latest:f['latest']=number
entry={'row':number,'id':row['id'],'source_path':str(src.resolve()),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dimensions':native,'asset':str(asset),'asset_sha256':hashlib.sha256((D/asset).read_bytes()).hexdigest(),'catalogue_dimensions':list(im.size)}
provenance=[q for q in provenance if q.get('id')!=row['id']]+[entry]
data['as_of']=a.as_of
(D/'catalogue-data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False));(D/'asset-provenance.json').write_text(json.dumps(provenance,indent=2))
print(f'Updated {row["id"]}. Run build_catalogue.py, render every page, inspect, then replace the existing Library PDF with version protection.')
