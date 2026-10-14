"""Prepare a sibling native TMJ with only return-action metadata; never modify its source."""
from pathlib import Path
import argparse, copy, hashlib, json
HERE=Path(__file__).resolve().parent
PATCH=json.loads((HERE/'metadata-patch.json').read_text())
def prepare(source):
    output=copy.deepcopy(source)
    properties=output.setdefault('properties',[])
    for desired in PATCH['mapProperties']:
        old=next((p for p in properties if p['name']==desired['name']),None)
        if old and old.get('value')!=desired['value']:
            raise ValueError(f"Existing {desired['name']} differs; compose with the existing script/config explicitly")
        if old is None:properties.append(copy.deepcopy(desired))
    layer=next((l for l in output['layers'] if l['name']==PATCH['objectLayer'] and l['type']=='objectgroup'),None)
    if layer is None:raise ValueError('Expected existing campus-zones-offline object layer')
    existing=next((o for o in layer['objects'] if o.get('name')==PATCH['object']['name']),None)
    expected=copy.deepcopy(PATCH['object'])
    if existing:
        if {k:v for k,v in existing.items() if k!='id'}!=expected:raise ValueError('Existing return pad differs')
    else:
        max_id=max((o.get('id',0) for l in output['layers'] for o in l.get('objects',[])),default=0)
        expected['id']=max(max_id+1,output.get('nextobjectid',1));layer['objects'].append(expected)
        output['nextobjectid']=max(expected['id']+1,output.get('nextobjectid',1))
    return output

def check_geometry(source,grid):
    pad=PATCH['object'];arrival=PATCH['arrival'];blocked=set(grid['blockedIndices']);T=grid['tileSize'];W=grid['width']
    assert not source['infinite'] and source['width']*source['tilewidth']==3200 and source['height']*source['tileheight']==3072
    start=next(o for l in source['layers'] for o in l.get('objects',[]) if o['name']=='start')
    # Closed-interval separation: no shared point with the initial native start area.
    assert pad['x']>start['x']+start['width'] or start['x']>pad['x']+pad['width'] or pad['y']>start['y']+start['height'] or start['y']>pad['y']+pad['height']
    def in_pad(x,y):return pad['x']<=x<=pad['x']+pad['width'] and pad['y']<=y+16<=pad['y']+pad['height']
    assert not in_pad(arrival['x'],arrival['y'])
    def clear(x,y):
        return all(ty*W+tx not in blocked for ty in range(y//T,(y+15)//T+1) for tx in range((x-8)//T,(x+7)//T+1))
    cases=0
    for y in range(pad['y']-16,pad['y']+pad['height']-16+1):
        for x in range(pad['x'],pad['x']+pad['width']+1):assert clear(x,y),(x,y);cases+=1
    for x in range(arrival['x'],1536+1):assert clear(x,arrival['y']),(x,arrival['y']);cases+=1
    return {'pass':True,'scope':'Native permanent16px collision grid, all integer pad origins and continuous1px arrival-to-pad sweep','pad':pad,'arrival':arrival,'start':start,'gapFromStartPixels':pad['x']-(start['x']+start['width']),'nativeBodyOriginChecks':cases,'automaticNavigation':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input',type=Path,required=True);parser.add_argument('--collision-grid',type=Path,required=True);parser.add_argument('--output',type=Path);parser.add_argument('--check-report',type=Path);args=parser.parse_args()
    source=json.loads(args.input.read_text());grid=json.loads(args.collision_grid.read_text());output=prepare(source);report=check_geometry(source,grid)
    assert [l for l in source['layers'] if l['type']=='tilelayer']==[l for l in output['layers'] if l['type']=='tilelayer']
    assert source['tilesets']==output['tilesets'];assert prepare(output)==output
    report['metadataIdempotent']=True;report['tileLayersAndTilesetsUnchanged']=True;report['sourceMapSha256']=hashlib.sha256(args.input.read_bytes()).hexdigest();report['scriptSha256']=hashlib.sha256((HERE/'campus-return.js').read_bytes()).hexdigest()
    if args.output:
        if args.output.resolve()==args.input.resolve():raise ValueError('Use a sibling output path and review before replacing the source')
        if args.output.parent.resolve()!=args.input.parent.resolve():raise ValueError('Output must be a sibling TMJ so the unchanged relative atlas paths remain valid')
        scripts=args.output.parent/'scripts';target=scripts/'campus-return.js';script=(HERE/'campus-return.js').read_bytes()
        if target.exists() and target.read_bytes()!=script:raise ValueError('Existing campus-return.js differs; review before replacing')
        scripts.mkdir(exist_ok=True);target.write_bytes(script)
        args.output.write_text(json.dumps(output,separators=(',',':')))
    if args.check_report:args.check_report.write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
