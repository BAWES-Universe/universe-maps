from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
wam=json.loads((R/'companion-stage/magical-campus.wam').read_text())
m=json.loads((R/'sources/civic/module.json').read_text())
stage,audience=wam['areas']
def contains(a,x,y):return a['x']<=x<=a['x']+a['width'] and a['y']<=y<=a['y']+a['height']
rows=[]
for s in m['audience']:
 x,y=s['center'];y+=1136
 pts=[(x,y+16)]
 r=m['nativePracticalFloorClickRectangles'][s['id']]
 pts += [(r['x']+dx,r['y']+dy)for dx in [0,(r['width']-1)/2,r['width']-1]for dy in [0,(r['height']-1)/2,r['height']-1]]
 rows.append({'seat':s['id'],'footpointsChecked':len(pts),'allInAudienceOnly':all(contains(audience,x,y)and not contains(stage,x,y)for x,y in pts)})
sx,sy=m['speaker']['center'];sy+=1136
speaker=contains(stage,sx,sy+16)and not contains(audience,sx,sy+16)
exterior=[(608,2104),(688,2104),(656,1568),(936,1584)]
report={'pass':len(rows)==24 and all(r['allInAudienceOnly']for r in rows)and speaker and all(not contains(audience,x,y)and not contains(stage,x,y)for x,y in exterior),'scope':'Static native x,y+16 feet membership and schema-linked two-role configuration. No successful media join, broadcast, reconnect, browser or live multiplayer claim.','audienceRows':rows,'nominalSpeakerInPodiumOnly':speaker,'exteriorFootpointsOutsideRoles':exterior,'roleRectangles':[{k:a[k]for k in ['name','x','y','width','height']}for a in wam['areas']],'mapSha256':hashlib.sha256((R/'map32/magical-campus.tmj').read_bytes()).hexdigest(),'wamSha256':hashlib.sha256((R/'companion-stage/magical-campus.wam').read_bytes()).hexdigest()}
(R/'companion-stage/membership-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pass':report['pass'],'audienceSeats':len(rows),'footpointChecks':sum(r['footpointsChecked']for r in rows),'speaker':speaker}))
assert report['pass']
