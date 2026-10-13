"""Deterministic native32 north-context translation. No old map is edited."""
from pathlib import Path
import json,shutil,hashlib,copy,sys
from PIL import Image
R=Path(__file__).resolve().parents[1]
J=lambda p:json.loads(p.read_text())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
DY=192;ROWS=6;W=1536;H=1216
SLUGS={'academy':'olive-academy-context-r5b','studio':'timber-studio-context-r3','yoga':'timber-yoga-context-r2','gym':'timber-gym-context-r2'}
def decode(root,m):
 images={s['firstgid']:Image.open(root/'map32'/s['image']).convert('RGBA') for s in m['tilesets']}
 below=Image.new('RGBA',(W,H));above=Image.new('RGBA',(W,H));dest=below
 for l in m['layers']:
  if l['name']=='floorLayer':dest=above
  if l['type']!='tilelayer' or not l.get('visible',True) or l.get('opacity',1)==0:continue
  for i,gid in enumerate(l['data']):
   if not gid:continue
   s=max((s for s in m['tilesets'] if s['firstgid']<=gid),key=lambda s:s['firstgid']);n=gid-s['firstgid'];x=n%s['columns']*32;y=n//s['columns']*32
   dest.alpha_composite(images[s['firstgid']].crop((x,y,x+32,y+32)),(i%48*32,i//48*32))
 return below,above

def build(id):
 src=R/'inputs'/id;out=R/'maps'/SLUGS[id]
 for folder in ['assets','map32','source','review']:(out/folder).mkdir(parents=True,exist_ok=True)
 m=J(src/'map32/map.tmj');old=copy.deepcopy(m);layout=J(src/'source/layout.json');oldlayout=copy.deepcopy(layout);wam=J(src/'map32/map.wam');oldwam=copy.deepcopy(wam)
 assert m['width']==48 and m['height']==32 and m['tilewidth']==m['tileheight']==32
 for p in (src/'map32').glob('*.png'):shutil.copy(p,out/'map32'/p.name)
 strip=Image.open(R/'source-assets'/(id+'-north.png')).convert('RGBA');assert strip.size==(1536,192);strip.save(out/'map32/north-context.png')
 gid=max(s['firstgid']+s['tilecount'] for s in m['tilesets'])
 m['tilesets'].append(dict(firstgid=gid,name='north-context',image='north-context.png',imagewidth=1536,imageheight=192,tilewidth=32,tileheight=32,margin=0,spacing=0,columns=48,tilecount=288))
 collisiongid=next(s['firstgid']+t['id'] for s in old['tilesets'] for t in s.get('tiles',[]) if any(p['name']=='collides' and p['value'] for p in t.get('properties',[])))
 m['height']=38
 approachCells=[(x,y) for y in range(5,9) for x in [31,32]]
 for l in m['layers']:
  if l['type']=='tilelayer':
   prefix=[collisiongid if l['name']=='collision' else 0]*(48*6);l['data']=prefix+l['data'];l['height']=38
  for o in l.get('objects',[]):o['y']+=DY
 for l in m['layers']:
  if l['name']=='collision':
   for x,y in approachCells:l['data'][y*48+x]=0
 north=dict(id=m['nextlayerid'],name='north-context',type='tilelayer',x=0,y=0,width=48,height=38,visible=True,opacity=1,data=list(range(gid,gid+288))+[0]*(48*32));m['nextlayerid']+=1;m['layers'].insert(0,north)
 save(out/'map32/map.tmj',m)
 for a in wam['areas']:a['y']+=DY
 assert not wam['entities'];save(out/'map32/map.wam',wam)
 layout['spawn'][1]+=ROWS
 layout['collision']=[[1]*48 for _ in range(ROWS)]+layout['collision']
 for x,y in approachCells:layout['collision'][y][x]=0
 for a in layout['seats']+layout['anchors']:
  if 'cell' in a:a['cell'][1]+=ROWS
  for k in ['anchor','floorClick']:
   if k in a:a[k][1]+=DY
 for z in layout['zones']:z['rect'][1]+=DY
 layout['anchors'].append({'name':'closed north garden gate approach','cell':[32,5]})
 save(out/'source/layout.json',layout)
 for name in ['base','above']:
  a=Image.open(src/'assets'/(name+'.png')).convert('RGBA');canvas=Image.new('RGBA',(W,H));canvas.paste(a,(0,DY));canvas.save(out/'assets'/(name+'.png'));assert canvas.crop((0,DY,W,H)).tobytes()==a.tobytes()
 below,above=decode(out,m);empty=Image.alpha_composite(below,above);empty.save(out/'review/empty-native.png')
 # Preserve the approved native proof actors/furniture; added rows contain no actors.
 occupied=empty.copy();occupied.paste(Image.open(src/'review/occupied-native.png').convert('RGBA'),(0,DY));occupied.save(out/'review/occupied-native.png');occupied.save(out/'review/overview.png')
 # Strict translation invariants, including every existing pixel and property.
 restored=copy.deepcopy(layout);restored['anchors']=[a for a in restored['anchors'] if a['name']!='closed north garden gate approach'];restored['spawn'][1]-=ROWS;restored['collision']=restored['collision'][ROWS:]
 for a in restored['seats']+restored['anchors']:
  if 'cell' in a:a['cell'][1]-=ROWS
  for k in ['anchor','floorClick']:
   if k in a:a[k][1]-=DY
 for z in restored['zones']:z['rect'][1]-=DY
 for y in range(3):
  for x in [31,32]:restored['collision'][y][x]=oldlayout['collision'][y][x]
 assert restored==oldlayout
 rw=copy.deepcopy(wam)
 for a in rw['areas']:a['y']-=DY
 assert rw==oldwam
 assert empty.crop((0,DY,W,H)).tobytes()==Image.open(src/'review/empty-native.png').convert('RGBA').tobytes()
 checks=dict(native32=True,dimensions=[48,38],northPixels=192,offset=[0,192],allAcceptedPixelsExact=True,allOriginalCollisionExactExceptApprovedGateApproach=True,approvedApproachCells=approachCells,allOriginalAnchorsExact=True,allWamPropertiesExact=True,newSceneryBlockedExceptVisibleGateApproach=True,gateBarrierRows=[3,4],noRawAvatarSheets=True,sourceMapSha256=sha(src/'map32/map.tmj'),runtimeMapSha256=sha(out/'map32/map.tmj'))
 save(out/'TRANSLATION-CHECK.json',checks)
 (out/'GUIDE.md').write_text(f'''# {SLUGS[id]}\n\nA192px northern continuation of the approved map: complete rear architecture and grounded garden/woodland. No visible functional labels. Every accepted interior pixel, seat, target and WAM property is unchanged apart from exact Y+192 translation. Collision changes only in the eight approved garden-gate approach cells. The newly closed garden gate is solid. Only eight visibly clear approach cells are opened to remove the inherited invisible stop. Original atlases are reused byte-for-byte.\n\nHost the complete map32 directory. The native map is48x38tiles at32px,1536x1216pixels. No engine changes, external integrations or publication. Existing WAM meeting/broadcast configuration is preserved, including its permission defaults. No live browser/device or multi-user media test.\n\nRun python tools/build_contexts.py {id} from the source bundle to rebuild. Requires Python3 and Pillow; no network, API or image generation. Native motion verification requires Node.js. Raw avatar sheets are excluded; the preserved occupied proof is a composited image, and runtime contains no avatars.\n''')
 print(id,out)
if __name__=='__main__':
 for id in (sys.argv[1:] or list(SLUGS)):build(id)
