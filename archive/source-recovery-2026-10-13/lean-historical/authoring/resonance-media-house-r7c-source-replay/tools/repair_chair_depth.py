from build_maps import *
import math
# Reuse the approved Mission Control rear-facing low-lumbar asset; screen chairs retain their own art.
def repair(m):
 ns={'__file__':str(R/'tools/rebuild.py'),'__name__':'media_chair_clean_base'}
 prefix=(R/'tools/rebuild.py').read_text().split('seats=[]')[0]
 exec(compile(prefix,str(R/'tools/rebuild.py'),'exec'),ns)
 clean=ns['m'].base;exceptions=[];rows=[]
 for a in m.anchors:
  if not (a['id'].startswith('editor-') or a['id'].startswith('screen-viewer-')):continue
  x,oy=a['x'],a['y'];task=a['id'].startswith('editor-')
  oldbox=(x-16,oy-17,x+16,oy+19) if task else (x-15,oy-12,x+15,oy+20)
  ox,oy0,ox2,oy2=oldbox;m.base.paste(clean.crop((ox-128,oy0-192,ox2-128,oy2-192)),(ox,oy0));exceptions.append(oldbox)
  a['y']=303 if task else 527
  y=a['y'];left=x-16 if task else x-15;top=y-12 if task else y
  if task:
   full=rgba(S/'chair-lowback-full-native.png');below=rgba(S/'chair-lowback-below-native.png');rail=rgba(S/'chair-lowback-rail-native.png')
  else:
   original=rgba(S/'screen-chair.png');full=Image.new('RGBA',original.size);full.paste(original.crop((0,13,30,32)),(0,13));full.alpha_composite(original.crop((0,0,30,13)).resize((16,13),Image.Resampling.LANCZOS),(7,0));rail=Image.new('RGBA',full.size);rail.paste(full.crop((7,4,23,13)),(7,4));below=full.copy();below.paste((0,0,0,0),(7,4,23,13))
  m.base.alpha_composite(below,(left,top));m.above.alpha_composite(rail,(left,top));exceptions.append((left,top,left+full.width,top+full.height))
  backY=(y//32+1)*32;back=(math.floor((left-(8 if task else 0))/32)*32,backY,math.ceil((left+full.width+(8 if task else 0))/32)*32,backY+32);m.protect(a['id']+'-rear-footprint',back)
  rows.append(dict(id=a['id'],oldAnchor=[x,oy],anchor=[x,y],belowOrigin=[left,top],railLocalBox=[4,14,28,24] if task else [7,4,23,13],groundRear=back,railAlphaPixels=sum(v>32 for v in rail.getchannel('A').getdata()),asset='Mission Control native rear lowback' if task else 'Existing Media screen chair slim upper back; original lower legs/feet exact'))
 # Four inherited seats are translated to the engine's stable native body endpoint.
 for a in m.anchors:
  if not (a['id'].startswith('keyboard-') or a['id'].startswith('listen-')):continue
  x,oy=a['x'],a['y'];keyboard=a['id'].startswith('keyboard-');im=rgba(S/('keyboard-stool.png' if keyboard else 'listening-chair-east.png'))
  if a['direction']=='west':im=ImageOps.mirror(im)
  left=x-im.width//2;oldtop=oy-12;oldbox=(left,oldtop,left+im.width,oldtop+im.height);m.base.paste(clean.crop((left-128,oldtop-192,left+im.width-128,oldtop+im.height-192)),(left,oldtop));exceptions.append(oldbox)
  a['y']=480 if keyboard else 544;top=a['y']-12;m.base.alpha_composite(im,(left,top));exceptions.append((left,top,left+im.width,top+im.height));rows.append(dict(id=a['id'],oldAnchor=[x,oy],anchor=[x,a['y']],artTranslation=[0,a['y']-oy],oldArtBox=oldbox,newArtBox=[left,top,left+im.width,top+im.height],asset='unchanged native keyboard stool' if keyboard else 'unchanged native listening chair',reason='Authored anchor now equals native fitBodyWithinTile endpoint'))
 jw(m.r/'validation/chair-depth-repair-spec.json',dict(chairs=rows,exceptionRects=exceptions,standingFramesOnly=True,wholeChairMask=False,feetErased=False,scope='Six backrest corrections plus four native-arrival-aligned seat translations; no room-scale change'))
 return exceptions
