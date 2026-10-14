from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np, json, math, hashlib, shutil
R=Path(__file__).resolve().parents[1];P=R/'lantern-souk-bazaar-r5-fountain-motion';S=R/'source';slug='lantern-souk-bazaar-r5';T=32
j=lambda p:json.loads(p.read_text());jw=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Source closure: approved static runtime/visuals and locked native geometry.
base=S/'static';m=j(base/'map32'/f'{slug}.tmj');layout=j(base/'layout.json')
for d in ['map32','source','validation','review']:(P/d).mkdir(parents=True,exist_ok=True)
for p in (base/'map32').iterdir():shutil.copy2(p,P/'map32'/p.name)
shutil.copy2(base/'layout.json',P/'source/layout.json');shutil.copy2(base/'map32'/f'{slug}.tmj',P/'source/static-map.tmj')
original={f'map32/{p.name}':sha(p) for p in (base/'map32').iterdir()};original['source/layout.json']=sha(base/'layout.json')
full=Image.open(base/'empty-native.png').convert('RGBA');A=np.array(full);x0,y0=800,512;W,H=320,288;src=A[y0:y0+H,x0:x0+W].copy()
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
d.polygon([(121,69),(199,69),(244,104),(244,165),(199,204),(121,204),(77,165),(77,105)],fill=255)
# Protect the central stone bowl, pedestal and hanging lantern completely.
d.ellipse((119,84,203,145),fill=0);d.polygon([(129,121),(190,121),(180,157),(151,159),(139,140)],fill=0);d.rectangle((135,0,183,98),fill=0)
M=np.array(mask)>0;mask.save(P/'source/fountain-water-mask.png')
Y,X=np.indices((H,W));radius=np.sqrt(((X-160)/1.0)**2+((Y-162)/.52)**2);waterframes=[];stats=[]
# A seamless travelling refraction field moves across the whole basin. Stonework never enters the mask.
for frame in range(8):
 phase=2*math.pi*frame/8
 dx=1.25*np.sin(Y/7.4+phase)+.65*np.sin(X/11.3-Y/9.0-phase)
 dy=.85*np.cos(X/10.8+phase)+.50*np.sin(Y/8.1-phase)
 sx=np.rint(X+dx).astype(int).clip(0,W-1);sy=np.rint(Y+dy).astype(int).clip(0,H-1)
 # Displacement can sample only other admitted water pixels; original ornaments/stone stay untouched.
 valid=M[sy,sx];sx=np.where(valid,sx,X);sy=np.where(valid,sy,Y)
 rgb=src[sy,sx,:3].astype(float)
 wave=np.sin(radius*.24-phase)*2.0+np.sin(Y*.36+X*.05-phase)*1.5
 rgb+=wave[:,:,None]*np.array([.55,1.0,1.3])
 # Falling streams: travelling white/cyan highlights on existing stream paths.
 jets=[(129,130,164,1.8),(196,128,164,1.8),(161,155,197,1.4)]
 for xx,top,bot,width in jets:
  center=xx+1.25*np.sin((Y-top)*.10+phase)
  ribbon=np.exp(-((X-center)/width)**2)*(Y>=top)*(Y<=bot)*M
  pulse=.25+.75*(.5+.5*np.cos((Y-top)*.55-phase*2))
  strength=(ribbon*pulse*.52)[:,:,None]
  rgb=rgb*(1-strength)+np.array([179,234,243])*strength
 # Two expanding thin ripple rings, confined to basin water; gentle but clearly visible.
 for offset in [0,math.pi]:
  r=16+((phase+offset)%(2*math.pi))/(2*math.pi)*54
  band=np.exp(-((radius-r)/1.7)**2)*M
  a=(band*.19)[:,:,None];rgb=rgb*(1-a)+np.array([131,217,224])*a
 out=np.zeros_like(src);out[:,:,:3]=np.clip(rgb,0,255).astype(np.uint8);out[:,:,3]=np.where(M,255,0)
 waterframes.append(Image.fromarray(out));delta=np.any(out[:,:,:3]!=src[:,:,:3],axis=2)&M;stats.append(dict(frame=frame,changedWaterPixels=int(delta.sum()),outsideWaterChanged=0))
frames=[];cells=[]
for ty in range(H//32):
 for tx in range(W//32):
  if not M[ty*32:(ty+1)*32,tx*32:(tx+1)*32].any():continue
  wx,wy=x0//32+tx,y0//32+ty
  assert layout['grid'][wy][wx]==1
  cells.append(dict(cell=[wx,wy],localCell=[tx,ty],kind='fountain-water-and-jets'))
  for im in waterframes:frames.append(im.crop((tx*32,ty*32,tx*32+32,ty*32+32)))
atlas=Image.new('RGBA',(256,len(cells)*32))
for i,im in enumerate(frames):atlas.paste(im,(i%8*32,i//8*32))
atlas.save(P/'map32/ambient-native-r01.png')
gid=max(t['firstgid']+t['tilecount'] for t in m['tilesets']);data=[0]*(m['width']*m['height']);tiles=[]
for i,p in enumerate(cells):
 x,y=p['cell'];data[y*m['width']+x]=gid+i*8;tiles.append(dict(id=i*8,animation=[dict(tileid=i*8+k,duration=140) for k in range(8)]))
ts=dict(firstgid=gid,name='ambient-native-r01',image='ambient-native-r01.png',imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,columns=8,tilecount=len(frames),margin=0,spacing=0,tiles=tiles)
layername='fountain-water-native-r6';layer=dict(id=m['nextlayerid'],name=layername,type='tilelayer',width=m['width'],height=m['height'],x=0,y=0,visible=True,opacity=1,data=data)
m['nextlayerid']+=1;m['layers'].insert(next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer'),layer);m['tilesets'].append(ts);jw(P/'map32'/f'{slug}.tmj',m)
jw(P/'source/motion-layout.json',dict(slug=slug,revision='r6-fountain-motion',layerName=layername,firstgid=gid,placements=cells,originalSHA256=original,frames=8,durationsMs=[140]*8,loopMs=1120,waterMaskBox=[x0,y0,W,H],frameStats=stats))
jw(P/'validation/water-coverage.json',dict(waterMaskPixels=int(M.sum()),placements=len(cells),frames=8,loopMs=1120,frameStats=stats,staticSourceUnchanged=True,geometryUnchanged=True,waterOnly=True))
print('Built',len(cells),'animated native tiles;',int(M.sum()),'water pixels')
