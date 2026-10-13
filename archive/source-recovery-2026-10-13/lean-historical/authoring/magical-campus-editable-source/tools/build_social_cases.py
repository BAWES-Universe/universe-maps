from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=R.parent/'universe-expanded-office/geometry-work/revision-04-social-egress'
goals=json.loads((S/'checkpoint-manifest-full-canvas.json').read_text())['goals'];routes=json.loads((S/'route-manifest-full-canvas.json').read_text())['routes']
anchors=[{**g,'x':g['x']+480,'y':g['y']+288} for g in goals if g['kind']!='checkpoint']
byid={g['id']:g for g in anchors};rr={r['targetId']:r for r in routes}
def pts(p):return [{'x':v['x']+480,'y':v['y']+288} for v in p]
cases={}
id='studenthub-operations-island-left-north';g=byid[id];r=rr[id];out=pts(r['egressPoints'][:5]);cases['pod']={'id':id,'spawn':{'x':g['x'],'y':g['y']},'points':out+list(reversed(out)),'peerAnchors':[a for a in anchors if a['id']!=id],'intendedPartner':None,'contactDirection':'south','title':'Occupied Operations: leave and return','source':r,'resetPoint':out[2]}
id='reception-visitor-1';g=byid[id];r=rr[id];incoming=pts(r['points']);cases['reception']={'id':id,'spawn':incoming[0],'points':incoming+list(reversed(incoming)),'peerAnchors':[a for a in anchors if a['id']!=id],'intendedPartner':'reception-staff-1','contactDirection':'north','title':'Grand reception: approach, conversation range, leave','source':r,'resetPoint':incoming[1]}
(R/'map16/social-cases.json').write_text(json.dumps({'scope':'Source-derived ordinary human bubble geometry, stationary native peers, no live server sessions.','humanCaptureInclusive':64,'pairPersistenceInclusive':96,'cases':cases},indent=2)+'\n')
print('Built',list(cases),'with',len(anchors),'occupied anchors')
