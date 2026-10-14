from pathlib import Path
import json,copy,hashlib
R=Path(__file__).resolve().parents[1];S=R/'source';j=lambda p:json.loads(p.read_text());w=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
c=j(S/'pavilion-collision-delta-contract.json');ids=set(c['removeOrReplaceFurnitureIds']);h=j(S/'frozen-a/collision-grid.json');cfg=j(S/'frozen-a/runtime-layout.json');garden=j(S/'frozen-a/garden-layout.json')
old=copy.deepcopy(h['grid'])
for x,y in c['collisionDelta']['addCells']:
 if h['grid'][y][x]:raise ValueError('Table delta already blocked in accepted A')
 h['grid'][y][x]=1
for x,y in c['collisionDelta']['removeCells']:h['grid'][y][x]=0
for obj in [h,cfg,garden]:obj['socialAnchors']=[a for a in obj['socialAnchors']if a['id']not in ids]+copy.deepcopy(c['socialAnchors'])
for obj in [cfg,garden]:obj['informalPairs']=[a for a in obj['informalPairs']if a['id']not in ['garden-pair-1','garden-pair-2']]+copy.deepcopy(c['informalPairs'])
cfg['furniture']=[p for p in cfg['furniture']if p['id']not in ids]+copy.deepcopy(c['furniture']);cfg['solidTileRectangles']=[p for p in cfg['solidTileRectangles']if p['id']not in ids]+[{'id':p['id'],'xywh':p['solidFootprintXYWH']}for p in c['furniture']]
garden['objects']=[p for p in garden['objects']if p['id']not in ids]+copy.deepcopy(c['furniture']);garden['pavilionUpdate']={'collisionContract':'source/pavilion-collision-delta-contract.json','centralClearPassageXYWH':c['centralClearPassageXYWH'],'addedSolidCells':c['collisionDelta']['addCells'],'chairArtworkNative':True,'pairAnchorDistancePx':48};cfg['garden']=copy.deepcopy(garden)
cfg['gardenB']={'status':'compiled candidate pending full validation','changes':'Exterior materials, approved pavilion tables and native decorative animation','quietCells':16,'hallAndFoyerGeometryPreserved':True,'pavilionPassageXYWH':c['centralClearPassageXYWH']}
for n,obj in [('collision-grid.json',h),('runtime-layout.json',cfg),('garden-layout.json',garden)]:w(S/n,obj)
actual=[[x,y]for y,row in enumerate(h['grid'])for x,v in enumerate(row)if v!=old[y][x]]
if sorted(actual)!=sorted(c['collisionDelta']['addCells']):raise ValueError('Unexpected geometry delta')
w(R/'validation/pavilion-geometry-integration.json',{'pass':True,'changedCells':actual,'allAddedOnly':True,'openCells':sum(v==0 for row in h['grid']for v in row),'centralClearPassageXYWH':c['centralClearPassageXYWH'],'sourceA':str(S/'frozen-a'),'mapRuntimeNotYetVerified':True})
print('Pavilion geometry: four new table cells; no other grid changes')
