from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];M=R/'map16';m=json.loads((M/'magical-campus.tmj').read_text());cfg=json.loads((M/'audio/configuration.json').read_text())
areas=[o for l in m['layers'] if l['type']=='objectgroup'for o in l['objects'] if o.get('name','').startswith('ambient-')]
def props(p):
 q={};x,y=p[0],p[1]+16
 for a in areas:
  if a['x']<=x<=a['x']+a['width'] and a['y']<=y<=a['y']+a['height']:q.update({t['name']:t['value']for t in a['properties']})
 return q
checks={}
checks['sixClassifiedAreas']=len(areas)==6 and all(a['class']=='area'for a in areas)
checks['nativeOnly']=not any(p['name']=='script'for p in m.get('properties',[]))
checks['sameTileObjectCost']=len([l for l in m['layers']if l['type']=='tilelayer'])==4
checks['quietFacilities']=all(not props((x,y))for rx,ry,rw,rh in cfg['quietZones']for x in range(rx,rx+rw+1,16)for y in range(ry,ry+rh+1,16))
checks['noConversationSilence']=all(p['name']!='silent'for l in m['layers']for o in l.get('objects',[])for p in o.get('properties',[]))
checks['relativeAssets']=all((M/s['url']).is_file()and not s['url'].startswith(('http:','https:'))for s in cfg['sources'])
checks['loopAndSafeMax']=all({p['name']:p['value']for p in a['properties']}['audioLoop']is True and 0<{p['name']:p['value']for p in a['properties']}['audioVolume']<=1 for a in areas)
reports=[]
for s in cfg['sources']:
 x,y,w,h=s['bounds'];cy=y+h/2-16
 path=[(x-1,cy),(x+1,cy),(x+49,cy),(x+97,cy),(x+w/2,cy),(x+w-49,cy),(x+w+1,cy)]
 states=[props(p)for p in path];urls=[a.get('playAudio')for a in states];changes=[urls[i]for i in range(len(urls))if i==0 or urls[i]!=urls[i-1]]
 checks[s['id']+'SingleSourceEntryExit']=changes==[None,s['url'],None]
 checks[s['id']+'GainBands']=[states[i].get('audioVolume')for i in [1,2,3]]==[0.35,0.7,1]
 checks[s['id']+'Reentry']=[props(p).get('playAudio')for p in [path[0],path[4],path[-1],path[4]]]==[None,s['url'],None,s['url']]
 reports.append({'source':s['id'],'route':path,'properties':states,'nativePlayAudioChanges':changes})
# Areas must be disjoint across emitters; gain-only changes should not restart unchanged URL.
a,b=cfg['sources'];ax,ay,aw,ah=a['bounds'];bx,by,bw,bh=b['bounds'];checks['emittersDisjoint']=ax+aw<bx or bx+bw<ax or ay+ah<by or by+bh<ay
result={'pass':all(checks.values()),'scope':'Source map/property transition verification; actual browser and physical device playback not asserted. Native y+16 area query and unchanged-property filtering traced in fork source.','mapSha256':hashlib.sha256((M/'magical-campus.tmj').read_bytes()).hexdigest(),'checks':checks,'routes':reports}
(R/'docs/native-audio08-source-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pass':result['pass'],'checks':checks},indent=2));assert result['pass']
