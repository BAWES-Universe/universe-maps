from pathlib import Path
import json,hashlib,sys
R=Path(sys.argv[1]).resolve()if len(sys.argv)>1 else Path(__file__).resolve().parents[1];D=json.loads((R/'source/design.json').read_text());L=json.loads((R/'source/layout.json').read_text());S=json.loads((R/'NATIVE-SPAWN-CHECKS.json').read_text());V=json.loads((R/'validation/state-layers.json').read_text());states=[x['layer']for x in V['forms']];rooms=[]
for region in D['rooms']:
 rid=region['id'];bounds=region['bounds'];spawn=region['spawn'];anchors=[a for a in L['anchors']if a['room']==rid];seats=[s for s in L['seats']if s['room']==rid];doors=[]
 for door in D['doors']:
  if door['room']!=rid:continue
  other=next(a for a in D['anchors']if a['id']==door['to']);doors.append(dict(door,name=door['id'],label=door['name'],destinationRoom=other['room'],destinationSpawn=other['anchor'],returnDoor=door['to']))
 rooms.append(dict(id=rid,physicalRegion=rid,tmj='runtime/map.tmj',tmj_sha256=hashlib.sha256((R/'runtime/map.tmj').read_bytes()).hexdigest(),bounds=bounds,spawn=spawn,spawnOutcomes=S['distinct']if rid=='mill-yard'else[spawn],returnAnchor=spawn,returnClick=[spawn[0],spawn[1]+16],headMask='source/native-head-union.json',visibleFloor=[dict(name=a['name'],origin=a['anchor'])for a in anchors],visiblePaths=[p for p in D['visiblePaths']if p['room']==rid],fixtureNegatives=[p for p in D['fixtureNegatives']if p['room']==rid],seats=seats,anchors=anchors,doors=doors,showLayers=['wet-0','print-0'],hideLayers=[x for x in states if x not in ['wet-0','print-0']]))
variations=[dict(name=v['name'],showLayers=v['showLayers'],hideLayers=[s for s in states if s not in v['showLayers']])for v in V['logicalViews']]
q=dict(freeze=R.name,root=str(R),authorProposed=True,coverageNote='Two disjoint physical regions, mill yard/canal/bridge and entered pattern room. Every admitted cell belongs to exactly one bound.',rooms=rooms,additionalVisibilityStates=variations,stateInventory='validation/state-layers.json');(R/'qa-spec.json').write_text(json.dumps(q,indent=2)+'\n')
