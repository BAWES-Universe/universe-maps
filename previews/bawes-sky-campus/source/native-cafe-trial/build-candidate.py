"""Isolated native-pixel gameplay trial. Existing campus TMJ/assets/runtime untouched."""
from pathlib import Path
from PIL import Image
import numpy as np,json,bisect,copy,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]; O=P/'playable';O.mkdir(exist_ok=True)
m=json.loads((R/'campus.tmj').read_text()); base=copy.deepcopy(m)
X,Y,W,H=1984,3712,2816,1792
canvas=Image.new('RGBA',(W,H))
canvas.alpha_composite(Image.open(P/'restored-native.png').convert('RGBA'))
canvas.alpha_composite(Image.open(P/'east-restored-native.png').convert('RGBA').crop((128,0,1536,1024)),(1408,0))
canvas.alpha_composite(Image.open(P/'south-restored-native.png').convert('RGBA').crop((0,128,1536,1024)),(0,896))
# Hard registered joins, no resizing, feathering or detail upscaling.
canvas.save(P/'assembled-native.png')
sets=base['tilesets'];starts=[s['firstgid'] for s in sets];cache={};fg=Image.new('L',(W,H))
for layer in m['layers']:
 if layer['name'] not in ['cafe-foreground','campus-chair-fronts','campus-bench-fronts']:continue
 for ty in range(Y//16,(Y+H)//16):
  for tx in range(X//16,(X+W)//16):
   xx,yy=tx*16-X,ty*16-Y
   if not canvas.getpixel((xx,yy))[3]:continue
   k=ty*m['width']+tx;gid=layer['data'][k]
   if not gid:continue
   s=sets[bisect.bisect_right(starts,gid)-1];key=s['image']
   if key not in cache:cache[key]=Image.open(R/key).convert('RGBA')
   n=gid-s['firstgid']; sx=s.get('margin',0)+(n%s['columns'])*(16+s.get('spacing',0));sy=s.get('margin',0)+(n//s['columns'])*(16+s.get('spacing',0))
   tile=cache[key].crop((sx,sy,sx+16,sy+16)).getchannel('A');old=np.array(fg.crop((xx,yy,xx+16,yy+16)))
   fg.paste(Image.fromarray(np.maximum(old,np.array(tile))),(xx,yy));layer['data'][k]=0
front=canvas.copy();front.putalpha(fg);front.save(P/'foreground-trial.png')
for s in m['tilesets']:
 if 'image' in s:s['image']='../../../'+s['image']
for prop in m.get('properties',[]):
 if prop['name']=='script':prop['value']='../../../runtime.js'
nextgid=max(s['firstgid']+s['tilecount'] for s in m['tilesets']);nextid=max(l['id'] for l in m['layers'])+1

def pack(name,im):
 global nextgid,nextid
 data=[0]*(m['width']*m['height'])
 for py in range(0,H,1024):
  for px in range(0,W,1024):
   page=im.crop((px,py,min(px+1024,W),min(py+1024,H)))
   if not page.getchannel('A').getbbox():continue
   nc,nr=page.width//16,page.height//16;filename=f'{name}-{px}-{py}.png';padded=Image.fromarray(np.pad(np.array(page),((1,1),(1,1),(0,0)),mode='edge'));padded.save(O/filename)
   first=nextgid;nextgid+=nc*nr;m['tilesets'].append(dict(firstgid=first,name=filename[:-4],image=filename,imagewidth=page.width+2,imageheight=page.height+2,margin=1,spacing=0,tilewidth=16,tileheight=16,tilecount=nc*nr,columns=nc))
   alpha=np.array(page.getchannel('A')).reshape(nr,16,nc,16).max(axis=(1,3))
   for ry in range(nr):
    for rx in range(nc):
     if alpha[ry,rx]:data[((Y+py)//16+ry)*m['width']+(X+px)//16+rx]=first+ry*nc+rx
 layer=dict(id=nextid,name=name,type='tilelayer',x=0,y=0,width=m['width'],height=m['height'],visible=True,opacity=1,data=data);nextid+=1;return layer
layer=pack('native-cafe-region',canvas);i=next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer');m['layers'].insert(i,layer);m['layers'].append(pack('native-cafe-foreground',front));m['nextlayerid']=nextid
(O/'campus.tmj').write_text(json.dumps(m,separators=(',',':')))
unchanged={name: next(l for l in base['layers'] if l['name']==name)==next(l for l in m['layers'] if l['name']==name) for name in ['persistent-collision','start','office-cover','office-floor','office-furniture','office-front-door','office-front-leaves']}
assert all(unchanged.values())
(P/'candidate-checks.json').write_text(json.dumps({'nativeScale':1,'resampling':False,'worldOrigin':[X,Y],'regionSize':[W,H],'horizontalJoinWorldX':3392,'verticalJoinWorldY':4608,'unchangedLayers':unchanged,'baseMapSha256':hashlib.sha256((R/'campus.tmj').read_bytes()).hexdigest(),'runtimeSha256':hashlib.sha256((R/'runtime.js').read_bytes()).hexdigest(),'foreground':'existing masks reused against new art; runtime visual review required','status':'bounded trial; outer coverage unfinished'},indent=2)+'\n')
print('Candidate built; collision, spawn, accepted office and gate layers unchanged.')
