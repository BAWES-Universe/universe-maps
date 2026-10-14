from pathlib import Path
from PIL import Image
import json,re,hashlib
R=Path(__file__).resolve().parents[1];BASE=R/'source-inputs';SHIFT=1024;TX=32
p=R/'map/butterfly-campus.tmj';m=json.loads(p.read_text());oldw=m['width'];H=m['height'];W=160
assert oldw==128,'Rebuild effects against base before composing stage'
collision=next(l for l in m['layers'] if l['name']=='permanent-collisions')
marker=next(v for v in collision['data'] if v)
for l in m['layers']:
 if l['type']=='tilelayer':
  old=l['data']; default=marker if l['name']=='permanent-collisions' else (old[0] if l['name']=='campus-audio-control' else 0)
  l['data']=[default]*(W*H)
  for y in range(H):l['data'][y*W+TX:y*W+TX+oldw]=old[y*oldw:(y+1)*oldw]
  l['width']=W
 elif l['type']=='objectgroup':
  for o in l.get('objects',[]):o['x']+=SHIFT
# Arrival is real clear paving south of the fountain; no collision/furniture has changed.
for o in (o for l in m['layers'] for o in l.get('objects',[])):
 if o['name']=='campus-spawn':o['y']=1632
 elif o['name']=='campus-entry':o['y']=1600
 elif o['name']=='campus-guide-stop':o['y']=1664
m['width']=W;m['backgroundcolor']='#0d1a24'
# Finite scenic negative space supplies the native camera's framing room, not off-map repeat art.
first=max(t['firstgid']+t['tilecount'] for t in m['tilesets'])
atlas=Image.new('RGBA',(160,32));atlas.paste((13,26,36,255),(0,0,32,32))
for i,a in enumerate([64,128,196,255]):atlas.paste((7,18,27,a),((i+1)*32,0,(i+2)*32,32))
atlas.save(R/'map/tilesets/gate-stage-controls.png')
m['tilesets'].append({'firstgid':first,'name':'gate-stage-controls','image':'tilesets/gate-stage-controls.png','imagewidth':160,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':5,'tilecount':5,'margin':0,'spacing':0})
back=[0]*(W*H)
for y in range(36,H):
 for x in range(0,100):back[y*W+x]=first
m['layers'].insert(3,{'name':'gate-night-stage','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':back})
for i in range(4):m['layers'].append({'name':f'journey-veil-{i+1}','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':False,'data':[first+i+1]*(W*H),'properties':[{'name':'presentationOnly','type':'bool','value':True}]})
for i,l in enumerate(m['layers'],1):l['id']=i
m['nextlayerid']=len(m['layers'])+1
for prop in m['properties']:
 if prop['name']=='campusVersion':prop['value']='3-gate-journey-review'
p.write_text(json.dumps(m,separators=(',',':')))
l=json.loads((BASE/'layout.json').read_text())
def shift(v):
 if isinstance(v,dict):
  for k,a in v.items():
   if k=='x' and isinstance(a,(int,float)):v[k]+=SHIFT
   else:shift(a)
 elif isinstance(v,list):
  for a in v:shift(a)
shift(l)
for point in l['proofPositions'].values():point[0]+=SHIFT
l['mapWidth']=W;l['phase']='gate journey experiential revision';l['campus']['spawn']['y']=1632;l['proofPositions']['campus-entry'][1]=1632
(R/'layout.json').write_text(json.dumps(l,indent=2))
# The optional audio policy remains disabled, but its bounded coordinates follow the translation.
a=R/'map/scripts/campus-audio.mjs';s=(BASE/'map/scripts/campus-audio.mjs').read_text();s=re.sub(r'\bx: (\d+)',lambda z:'x: '+str(int(z[1])+SHIFT),s);s=s.replace('Math.max(32,','Math.max(1056,').replace(': 608;',': 1632;').replace('? 448 :','? 1472 :').replace('Math.min(992,','Math.min(2016,');a.write_text(s)
print(json.dumps({'world':[W*32,H*32],'allOriginalContentTranslatedX':SHIFT,'gate':l['gate'],'campusSpawn':l['campus']['spawn'],'baseCollisionCells':sum(bool(x)for x in collision['data']),'mapSha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
