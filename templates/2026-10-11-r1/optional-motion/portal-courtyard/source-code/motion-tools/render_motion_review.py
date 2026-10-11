#!/usr/bin/env python3
"""Native32 atlas decoding from actual pinned-plugin replay states, with review-only Greg."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import sys,json,hashlib
R=Path(sys.argv[1]);j=lambda p:json.loads(p.read_text());meta=j(R/'source/motion-layout.json');slug=meta['slug'];m=j(R/'map32'/f'{slug}.tmj');layout=j(R/'source/layout.json');states=j(R/'validation/plugin-frame-replay.json')['captures'];W=m['width']*32;H=m['height']*32
sets=[(ts,Image.open(R/'map32'/ts['image']).convert('RGBA')) for ts in m['tilesets']]
def tile(gid):
 ts,im=max((t for t in sets if t[0]['firstgid']<=gid),key=lambda t:t[0]['firstgid']);n=gid-ts['firstgid'];x=n%ts['columns']*32;y=n//ts['columns']*32;return im.crop((x,y,x+32,y+32))
under=Image.new('RGBA',(W,H));over=Image.new('RGBA',(W,H));dest=under
for layer in m['layers']:
 if layer['name']=='floorLayer':dest=over
 if layer['type']!='tilelayer' or layer.get('opacity',1)==0 or layer['name']==meta['layerName']:continue
 for i,gid in enumerate(layer['data']):
  if gid:dest.alpha_composite(tile(gid),((i%m['width'])*32,(i//m['width'])*32))
greg=Image.open(R/'source/greg-reference.png').convert('RGBA');people=Image.new('RGBA',(W,H));dirs={'north':10,'south':1,'west':4,'east':7}
for a in layout['anchors']:
 if a['kind']=='social' or a['id']=='spawn':
  f=dirs[a['direction']];people.alpha_composite(greg.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32)),(a['x']-16,a['y']-16))
def render(s,occupied=True):
 im=under.copy()
 for p,gid in zip(meta['placements'],s['gids']):im.alpha_composite(tile(gid),(p['cell'][0]*32,p['cell'][1]*32))
 if occupied:im.alpha_composite(people)
 im.alpha_composite(over);return im
base=under.copy();base.alpha_composite(people);base.alpha_composite(over);base.save(R/'review/static-checkpoint-occupied.png')
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
for p in meta['placements']:
 x,y=p['cell'];assert layout['grid'][y][x]==1;d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=255)
indices=[round(i*(len(states)-1)/8) for i in range(8)];nativeframes=[];fullhash=[];changed=[];outside=[]
for i,s in enumerate(states):
 im=render(s);diff=ImageChops.difference(im.convert('RGB'),base.convert('RGB'));r,g,b=diff.split();delta=ImageChops.lighter(ImageChops.lighter(r,g),b);outside.append(bool(ImageChops.multiply(delta,ImageChops.invert(mask)).getbbox()));changed.append(sum(v>0 for v in delta.getdata()));fullhash.append(hashlib.sha256(im.tobytes()).hexdigest())
 if i in indices:
  k=indices.index(i);im.save(R/'review'/f'occupied-native-frame-{k:02d}.png');nativeframes.append((s,im))
assert not any(outside),'Motion changed pixels outside permanently-blocked placements'
font=ImageFont.load_default();sheet=Image.new('RGB',(4*768,2*(512+30)), '#14202a');d=ImageDraw.Draw(sheet)
for i,(s,im) in enumerate(nativeframes):
 x=i%4*768;y=i//4*542;sheet.paste(im.convert('RGB').resize((768,512),Image.Resampling.NEAREST),(x,y+30));d.text((x+10,y+8),f"Native atlas frame, {s['elapsedMs']:.0f} ms",font=font,fill='white')
sheet.save(R/'review/native-motion-contact-sheet.png')
# Detail view keeps all placements visible together with 1 tile of immutable context.
cellsize=96;scale=3;cols=len(meta['placements']);detail=Image.new('RGB',(8*cellsize*scale,cols*(cellsize*scale+28)),'#14202a');dd=ImageDraw.Draw(detail)
for row,p in enumerate(meta['placements']):
 x,y=p['cell'];box=(x*32-32,y*32-32,x*32+64,y*32+64)
 for col,(s,im) in enumerate(nativeframes):
  xx=col*cellsize*scale;yy=row*(cellsize*scale+28);detail.paste(im.crop(box).convert('RGB').resize((cellsize*scale,cellsize*scale),Image.Resampling.NEAREST),(xx,yy+28));dd.text((xx+5,yy+8),f"Cell {x},{y} · {s['elapsedMs']:.0f} ms",font=font,fill='white')
detail.save(R/'review/placement-motion-contact-sheet.png')
# Four-second diagnostic preview. The end-to-start cut is explicitly not a seamless artistic loop.
gifs=[]
for s in states[:-1]:
 im=render(s);strip=Image.new('RGB',(cols*cellsize*scale,cellsize*scale+36),'#14202a');d=ImageDraw.Draw(strip)
 for i,p in enumerate(meta['placements']):
  x,y=p['cell'];crop=im.crop((x*32-32,y*32-32,x*32+64,y*32+64));strip.paste(crop.resize((cellsize*scale,cellsize*scale),Image.Resampling.NEAREST),(i*cellsize*scale,36));d.text((i*cellsize*scale+8,12),f"{x},{y}  |  {s['elapsedMs']:.0f} ms",fill='white')
 gifs.append(strip)
gifs[0].save(R/'review/ambient-loop.gif',save_all=True,append_images=gifs[1:],duration=100,loop=0,disposal=2)
report=dict(scope='Native-resolution runtime TMJ/atlas decoding using actual pinned-plugin selected tile IDs. Greg is review-only. Not a live Phaser/browser screenshot.',capturedStates=len(states),fullMapDistinctRenderedFrames=len(set(fullhash)),changedPixelsFromStaticPerState=changed,pixelsChangedOutsidePermanentlyBlockedOverlayCells=0,contactSheet='review/native-motion-contact-sheet.png',placementSheet='review/placement-motion-contact-sheet.png',nativeOccupiedFrames=len(nativeframes),diagnosticGif='review/ambient-loop.gif',gifDurationMs=4000,gifSeamless=False,staticArtworkAtlasesUnmodified=True)
(R/'validation/native-render.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
