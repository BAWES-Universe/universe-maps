from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
import build_templates as b
from build_environments import clip_foreground_heads,foreground_polygon
b.C,b.N,b.W,b.H=60,40,1920,1280
DX,DY=192,160
R=b.R
S=R/'source-assets'
if 'greg-reference' not in b.A:b.A['greg-reference']=Image.new('RGBA',(96,128))

def kit():
 src=Image.open(S/'art-deco-original-furniture.png').convert('RGBA')
 boxes={'desk-n':((0,0,665,400),(88,44)),'desk-s':((680,0,1312,400),(88,44)), 'chair-n':((110,415,590,805),(40,36)),'chair-s':((745,410,1210,815),(40,36)),'coffee':((0,815,720,1199),(80,36))}
 a={}
 for name,(box,size) in boxes.items():
  q=src.crop(box);q=q.crop(q.getbbox()).resize(size,Image.Resampling.LANCZOS);q.save(S/(name+'.png'));a[name]=q
 return a

def architecture():
 gen=Image.open(S/'city-extension-generated.png').convert('RGBA').resize((1920,1280),Image.Resampling.LANCZOS)
 old=Image.open(S/'sales-environment-flat.png').convert('RGBA')
 mask=Image.new('L',old.size);d=ImageDraw.Draw(mask)
 # Exact accepted interior silhouette; added city art remains strictly outside.
 poly=[(134,12),(1402,12),(1402,83),(1481,83),(1481,226),(1500,375),(1519,826),(1519,899),(1445,939),(995,963),(887,963),(887,945),(639,945),(639,965),(540,965),(92,939),(18,902),(18,819),(37,531),(50,83),(134,83)]
 d.polygon(poly,fill=255)
 gen.paste(old,(DX,DY),mask)
 gen.save(S/'sales-panorama-composite.png')
 b.js(S/'INTERIOR-PRESERVATION.json',dict(original='sales-environment-flat.png',offset=[DX,DY],maskPolygon=poly,method='Original accepted pixels pasted unscaled inside explicit silhouette. Generated panorama only outside silhouette.',preservedPixels=int((np.array(mask)>0).sum())))
 return gen
A=kit()
def seat(m,x,y,name,direction='north'):
 x+=6;y+=5;px,py=x*32+16,y*32+15
 im=A['chair-n' if direction=='north' else 'chair-s'];top=py-12 if direction=='north' else py-24
 m.base.alpha_composite(im,(px-20,top))
 cut=16 if direction=='north' else 31
 m.above.alpha_composite(im.crop((0,cut,40,36)),(px-20,top+cut))
 m.block(x,y+(1 if direction=='north' else -1),1,1)
 m.seats.append(dict(name=name,cell=[x,y],anchor=[px,py],floorClick=[px,py+16],direction=direction,chairRect=[px-20,top,40,36],seatPan=[px,py+1],nativeFrame='row3-middle' if direction=='north' else 'row0-middle'))
def desk(m,x,y,name):
 px=(x+6)*32+16;py=(y+5)*32
 m.base.alpha_composite(A['desk-n'],(px-44,py-12));m.block(x+5,y+4,3,2);seat(m,x,y+1,name)
def build():
 m=b.Map('art-deco-sales-atelier-r2','Art Deco Sales Atelier','Work',dict(b.P,outer='#081323'));m.base=architecture();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(30,33)
 for x,y,w,h in [(6,13,37,13),(7,6,10,6),(10,12,4,1),(31,6,11,6),(34,12,4,1),(22,7,4,6),(21,25,6,4)]:m.block(x+6,y+5,w,h,0)
 m.block(27,34,6,2,0) # genuine central doorway and exterior landing, jambs stay blocked
 m.anchor('south threshold',30,34);m.anchor('south landing',30,35)
 for x,y,w,h in [(42,13,1,2),(15,25,6,1),(27,25,6,1)]:m.block(x+6,y+5,w,h)
 for name,x in [('Client west',11),('Client east',35)]:
  px=(x+6)*32+16;py=(8+5)*32
  m.base.alpha_composite(A['coffee'],(px-40,py));m.block(x+5,13,3,1)
  seat(m,x,7,name+' south-facing','south');seat(m,x,9,name+' north-facing','north')
  m.zone(name,x+3,11,10,6);m.anchor(name+' entrance',x+7,17);m.anchor(name+' host',x+9,14)
 for i,(x,y) in enumerate([(8,17),(13,17),(8,22),(13,22),(35,17),(40,17),(35,22),(40,22)]):desk(m,x,y,'research-'+str(i+1))
 for x in [23,24]:seat(m,x,9,'briefing-'+str(x-22))
 m.zone('Research west',12,21,10,9,'placeholder');m.zone('Research east',39,21,10,9,'placeholder');m.zone('Private briefing',28,12,4,5)
 for name,x,y in [('briefing presenter',23,7),('briefing entrance',23,12),('west research aisle',10,20),('east research aisle',37,20),('flat compass inlay',24,19),('arrival',24,28)]:m.anchor(name,x+6,y+5)
 for pts in [[(94,864),(489,864),(489,932),(94,932)],[(1045,864),(1441,864),(1441,932),(1045,932)]]:foreground_polygon(m,[(x+DX,y+DY) for x,y in pts])
 m.cropboxes=[('client-west',(192+DX,160+DY,576+DX,416+DY)),('client-east',(960+DX,160+DY,1376+DX,416+DY)),('research',(192+DX,512+DY,1408+DX,800+DY)),('briefing',(672+DX,192+DY,864+DX,416+DY))]
 # Safety union includes all twelve frames of the eight varied native repository Wokas.
 sheets=[Image.open(p).convert('RGBA') for p in sorted(S.glob('woka-proof-*.png'))];union=np.array(b.A['greg-reference'])
 for sheet in sheets:union[:,:,3]=np.maximum(union[:,:,3],np.array(sheet)[:,:,3])
 head=np.zeros((14,32),bool)
 for rr in range(4):
  for cc in range(3):head|=union[rr*32:rr*32+14,cc*32:cc*32+32,3]>32
 if (S/'native-head-geometry.json').exists():head|=np.array(json.loads((S/'native-head-geometry.json').read_text()),bool)
 b.js(S/'native-head-geometry.json',head.astype(int).tolist())
 for rr in range(4):
  for cc in range(3):union[rr*32:rr*32+14,cc*32:cc*32+32,3]=head.astype('uint8')*255
 original=b.A['greg-reference'];b.A['greg-reference']=Image.fromarray(union)
 safety=clip_foreground_heads(m);b.A['greg-reference']=original;m.finish();out=R/m.slug;b.js(out/'source/foreground-safety.json',safety)
 # Native compositor proof: unchanged 32x32 repo frames, correct direction, all seats occupied.
 occupied=m.base.copy()
 proof=[]
 for i,s in enumerate(m.seats if sheets else []):
  row=3 if s['direction']=='north' else 0;actor=sheets[i%len(sheets)].crop((32,row*32,64,row*32+32));x,y=s['anchor'];occupied.alpha_composite(actor,(x-16,y-16));proof.append(dict(seat=s['name'],woka=i%len(sheets),frame=[1,row],anchor=[x,y],nativeSize=[32,32],seatPan=s['seatPan']))
 occupied.alpha_composite(m.above);occupied.save(out/'review/occupied-native.png');occupied.save(out/'review/overview.png')
 for name,box in m.cropboxes:occupied.crop(box).save(out/'review'/f'{name}-occupied-native.png')
 b.js(out/'source/OCCUPIED-PROOF.json',dict(actors=proof,scope='Static native32 atlas-equivalent composite; not a live room screenshot; actual repository frames, no invented sitting poses',license='Raw Pipoya sprite sheets are private QA fixtures and excluded from distribution'))
 b.js(out/'source/INTERIOR-PRESERVATION.json',json.loads((S/'INTERIOR-PRESERVATION.json').read_text()))
 print(out)
if __name__=='__main__':build()
