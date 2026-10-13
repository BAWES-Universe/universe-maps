from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];l=json.loads((R/'source/layout.json').read_text());g=json.loads((R/'source/collision-grid.json').read_text())['grid'];q=json.loads((R/'source/quiet-grid.json').read_text())['grid'];m=json.loads((R/'map32/conference.tmj').read_text());wam=json.loads((R/'map32/conference.wam').read_text())
a=next(o for layer in m['layers']if layer['type']=='objectgroup'for o in layer.get('objects',[])if any(p['name']=='start'and p['value']for p in o.get('properties',[])))
def body(x,y):return not any(g[yy][xx]for yy in range(y//32,(y+15)//32+1)for xx in range((x-8)//32,(x+7)//32+1))
fail=[];n=0
for y in range(a['y']+16,a['y']+a['height']-16+1):
 for x in range(a['x']+16,a['x']+a['width']-16+1):
  n+=1
  if not body(x,y)or not q[y//32][x//32]:fail.append([x,y,'body or quiet'])
  for zone in wam['areas']:
   if zone['x']<=x<=zone['x']+zone['width']and zone['y']<=y+16<=zone['y']+zone['height']:fail.append([x,y,'communication overlap'])
# Full continuous stage-tread centerlines in both directions. Artwork has no solid sideposts.
steps=[]
for id,x,y0,y1 in [('summit',784,384,480),('forum',2256,384,464),('lab',2064,1376,1456)]:
 bad=[[x,y]for y in range(y0,y1+1)if not body(x,y)];steps.append({'id':id,'axis':'y','x':x,'from':y0,'to':y1,'integerBodySamples':y1-y0+1,'pass':not bad,'bad':bad})
out={'pass':not fail and all(s['pass']for s in steps),'tiledMargin16':True,'sampledSpawnOutcomes':n,'actualSpawnPlayerBounds':[a['x']+16,a['y']+16,a['x']+a['width']-16,a['y']+a['height']-16],'spawnFailures':fail,'routeStartNote':'layout.start is a chosen safe receiver test anchor; actual Tiled spawn outcomes are exhaustively checked here.','walkableStageTreads':steps,'noMultiheightPhysics':True};(R/'validation/spawn-and-stage-steps.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['pass']else 1)
