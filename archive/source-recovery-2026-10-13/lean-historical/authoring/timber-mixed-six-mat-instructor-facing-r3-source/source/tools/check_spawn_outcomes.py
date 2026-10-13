"""Validate every exact position captured from actual native JavaScript startup.
The compact source carries hash-pinned source lineage/results, not raw engine.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'timber-mixed-six-mat-instructor-facing-r3';load=lambda p:json.loads(p.read_text());m=load(O/'map32/map.tmj');g=load(O/'source/layout.json')['collision'];record=load(R/'source-assets/native-spawn-outcomes.json');starts=[a for l in m['layers'] for a in l.get('objects',[]) if a.get('name')=='start'];assert starts==[record['start']],'Native spawn capture must be refreshed for changed start geometry'
quiet=next(l for l in m['layers'] if l['name']=='spawn-only-silence')['data'];rows=[]
for x,y in record['distinct']:
 cells={(xx//32,yy//32) for xx in range(x-8,x+8) for yy in range(y,y+16)};clear=all(0<=cy<len(g) and 0<=cx<len(g[0]) and not g[cy][cx] for cx,cy in cells);silent=bool(quiet[(y//32)*m['width']+x//32]);rows.append(dict(x=x,y=y,bodyClear=clear,quiet=silent));assert clear and silent,rows[-1]
out=dict(scope='Every distinct actual native JS startup outcome, including floating-point near-one rounding; exact capture source/area lineage attached.',allActualOutcomesSafeAndQuiet=True,rows=rows,capture=record,mapSha256=hashlib.sha256((O/'map32/map.tmj').read_bytes()).hexdigest());(O/'NATIVE-SPAWN-CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print('Actual native spawn outcomes safe/quiet:',len(rows))
