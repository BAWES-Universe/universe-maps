"""Read-only source composition, tile budget and proof. No artwork authoring here."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
O=Path(__file__).parent; R=Path('/workspace/shared/magical-campus-standard32-09'); spec=json.loads((O/'effects/effects.json').read_text()); B=Image.open(R/'layers/campus-base.png').convert('RGBA'); A=Image.open(R/'layers/campus-above.png').convert('RGBA'); T=32; stats=[]
for e in spec['effects']:
 x,y=e['origin'];w,h=e['size'];f=[Image.open(O/p).convert('RGBA') for p in e['frames']];box=(x,y,x+w,y+h);base=B.crop(box);above=A.crop(box);post=[]
 for im in f:
  pre=Image.new('RGBA',(w,h),(12,32,41,255));pre.alpha_composite(base)
  if e['layer']=='below':pre.alpha_composite(im);pre.alpha_composite(above)
  else:pre.alpha_composite(above);pre.alpha_composite(im)
  post.append(pre.convert('RGB'))
 pix=np.stack([np.asarray(z) for z in post]).astype('int16');diff=np.ptp(pix,axis=0).max(2);arr=np.stack([np.asarray(z) for z in f]);union=arr[:,:,:,3].max(0)>0
 mask=Image.fromarray(np.uint8(union)*255);mask.save(O/f'source/{e["name"]}-pixel-owner-union.png')
 # Shared-palette exact-native timed visual, with lossless PNG phases authoritative.
 pal=Image.fromarray(np.concatenate([np.asarray(z) for z in post],0)).quantize(colors=256);g=[z.quantize(palette=pal,dither=Image.Dither.NONE) for z in post];g[0].save(O/f'proof/{e["name"]}-native-timed.gif',save_all=True,append_images=g[1:],duration=e['duration'],loop=0,disposal=2,optimize=False)
 # APNG is lossless, native, exact timing.
 post[0].save(O/f'proof/{e["name"]}-native-timed.png',save_all=True,append_images=post[1:],duration=e['duration'],loop=0)
 for k in [0,3,7]:post[k].save(O/f'proof/{e["name"]}-t{k*e["duration"]:04}-native.png')
 if h<300:
  sheet=Image.new('RGB',(w*4,(h+18)*2),(12,22,29));d=ImageDraw.Draw(sheet)
  for c,k in enumerate([int(k*(len(f)-1)/7) for k in range(8)]):xx=(c%4)*w;yy=(c//4)*(h+18);sheet.paste(post[k],(xx,yy+18));d.text((xx+3,yy+2),f'{k*e["duration"]}ms',fill='white')
  sheet.save(O/f'proof/{e["name"]}-phases-native.png')
 # Actual world-aligned32 cells, with per-pixel dedup.
 ex=x//32*32;ey=y//32*32;ew=math.ceil((x-ex+w)/32)*32;eh=math.ceil((y-ey+h)/32)*32;fs=[]
 for im in f:
  pad=Image.new('RGBA',(ew,eh));pad.paste(im,(x-ex,y-ey));fs.append(pad)
 cells=[];lookup={};static=0;nonempty=0
 for ty in range(0,eh,32):
  for tx in range(0,ew,32):
   tiles=[im.crop((tx,ty,tx+32,ty+32)).tobytes() for im in fs]
   if not any(t[3::4].strip(b'\0') for t in tiles):continue
   nonempty+=1
   if len(set(tiles))==1:static+=1;continue
   ids=[]
   for t in tiles:
    if t not in lookup:lookup[t]=len(lookup)
    ids.append(lookup[t])
   cells.append({'cell':[(ex+tx)//32,(ey+ty)//32],'frameIds':ids})
 s={'name':e['name'],'origin':e['origin'],'size':e['size'],'layer':e['layer'],'frames':len(f),'distinctSourceFrames':len({im.tobytes() for im in f}),'distinctVisibleFrames':len({im.tobytes() for im in post}),'durationMs':e['duration'],'loopMs':e['duration']*len(f),'ownerPixels':int(union.sum()),'visiblePixelsChangingOver3Rgb':int((diff>3).sum()),'visiblePixelsChangingOver16Rgb':int((diff>16).sum()),'medianRgbSwing':float(np.median(diff[diff>3])),'someAboveOnOwner':int(((np.asarray(above)[:,:,3]>0)&union).sum()),'nonemptyCells':nonempty,'varyingCells':len(cells),'unchangedNonemptyCells':static,'uniqueFrameTiles':len(lookup),'naiveFrameTiles':len(cells)*len(f),'framesPngBytes':sum((O/p).stat().st_size for p in e['frames']),'cells':cells}
 stats.append(s)
(O/'proof/motion-audit.json').write_text(json.dumps({'scope':'Offline native reconstruction from frozen09 static sources plus SVG-authored Campus10 overlays; final integrated TMJ and browser playback not asserted','effects':stats},indent=2)+'\n')
print(json.dumps([{k:v for k,v in s.items() if k!='cells'} for s in stats],indent=2))
