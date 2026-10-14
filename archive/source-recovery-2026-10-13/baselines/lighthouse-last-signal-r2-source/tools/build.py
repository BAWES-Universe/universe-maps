from pathlib import Path
import json, shutil, wave, struct, math
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]; O=R/'runtime'
B=R/'source/base'
m=json.loads((B/'lighthouse-festival-island.tmj').read_text()); gid=max(t['firstgid']+t['tilecount'] for t in m['tilesets'])
a=Image.new('RGBA',(128,128)); d=ImageDraw.Draw(a)
# Original transparent inlaid brass rings: dormant, tuned, beacon, invisible carrier.
for off,col in [(0,'#e7c77e'),(32,'#89f4d3'),(64,'#ffe9a4')]:
 d.ellipse((off+3,3,off+28,28),outline='#28383c',width=5);d.ellipse((off+4,4,off+27,27),outline=col,width=2)
 for x,y in [(16,3),(16,28),(3,16),(28,16)]:d.rectangle((off+x-1,y-1,off+x+1,y+1),fill=col)
 if off: d.polygon([(off+16,9),(off+20,16),(off+16,23),(off+12,16)],fill=col)
# A warm original optical glow, split into nine standard tiles. No collision and no art replacement.
glow=Image.new('RGBA',(96,96));pix=glow.load()
for yy in range(96):
 for xx in range(96):
  r=math.hypot(xx-48,yy-48); alpha=int(110*max(0,1-r/48)**2)
  if r<7:alpha=180
  pix[xx,yy]=(255,222,121,alpha)
for i in range(9):a.alpha_composite(glow.crop(((i%3)*32,(i//3)*32,(i%3+1)*32,(i//3+1)*32)),(((i+4)%4)*32,((i+4)//4)*32))
a.save(O/'signal-inlays.png')
m['tilesets'].append(dict(firstgid=gid,name='signal-inlays',image='signal-inlays.png',imagewidth=128,imageheight=128,tilewidth=32,tileheight=32,columns=4,tilecount=16,margin=0,spacing=0))
stations=[('dock',784,800),('tide',272,672),('wind',752,256),('prism',1296,576),('beacon',336,288)]
def layer(name,points,visible=True,properties=None):
 data=[0]*(m['width']*m['height'])
 for x,y,t in points:data[(y//32)*m['width']+x//32]=gid+t
 l=dict(id=m['nextlayerid'],name=name,type='tilelayer',width=m['width'],height=m['height'],x=0,y=0,opacity=1,visible=visible,data=data);m['nextlayerid']+=1
 if properties:l['properties']=properties
 m['layers'].insert(next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer'),l)
layer('signal-rings',[(x,y+16,0)for _,x,y in stations])
for name,x,y in stations[1:4]:layer('signal-'+name,[(x,y+16,1)],False)
layer('signal-beacon',[(288+(i%3)*32,32+(i//3)*32,4+i)for i in range(9)],False)
beacon=next(l for l in m['layers'] if l['name']=='signal-beacon');m['layers'].remove(beacon);m['layers'].append(beacon)
layer('signal-audio',[(x*32,y*32,3)for y in range(m['height'])for x in range(m['width'])])
objects=[]
for name,x,y in stations:
 objects.append(dict(id=m['nextobjectid'],name='signal-popup-'+name,type='',x=max(16,x-144),y=max(16,y-156),width=288,height=116,rotation=0,visible=True));m['nextobjectid']+=1
m['layers'].append(dict(id=m['nextlayerid'],name='signal-popups',type='objectgroup',visible=True,opacity=1,x=0,y=0,objects=objects));m['nextlayerid']+=1
m['properties']=[p for p in m['properties']if p['name']not in ('name','status','script')]+[dict(name='name',type='string',value='Lighthouse: The Last Signal'),dict(name='script',type='string',value='signal.js')]
(O/'lighthouse-last-signal.tmj').write_text(json.dumps(m,separators=(',',':')))
wam=json.loads((B/'lighthouse-festival-island.wam').read_text());wam['mapUrl']='./lighthouse-last-signal.tmj';(O/'lighthouse-last-signal.wam').write_text(json.dumps(wam,indent=2))
for f in ['lighthouse-festival-island.tmj','lighthouse-festival-island.wam']:
 if (O/f).exists():(O/f).unlink()
(O/'audio').mkdir(exist_ok=True)
# Entirely original synthesized sine/bell signal, 8s exact loop; no recording/sample/service.
for filename,silent in [('silent-carrier.wav',True),('tide-signal.wav',False)]:
 samples=[];sr=22050
 for i in range(sr*8):
  t=i/sr; value=0
  if not silent:
   for start,freq in [(0.5,220),(1.3,330),(2.1,440)]:
    q=t-start
    if 0<=q<1.1:value+=.18*min(q/.025,1)*math.exp(-4*q)*(math.sin(2*math.pi*freq*q)+.18*math.sin(2*math.pi*2*freq*q))
  samples.append(struct.pack('<h',round(max(-1,min(1,value))*32767)))
 with wave.open(str(O/'audio'/filename),'wb')as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(samples))
print('Built additive variant; original geometry unchanged.')
