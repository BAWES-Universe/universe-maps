from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];P=R/'celestial-transit-garden-calm-draft';j=json.loads((P/'source/layout.json').read_text());m=json.loads((P/'map32/celestial-transit-garden-calm-draft.tmj').read_text());wam=json.loads((P/'map32/celestial-transit-garden-calm-draft.wam').read_text());routes=json.loads((P/'validation/native-routes.json').read_text());g=np.array(j['grid']);fixture=[];arrivals=[]
for f in j['protectedFixtures']:
 x,y,x2,y2=f['solidXYXY'];cells=g[y//32:math.ceil(y2/32),x//32:math.ceil(x2/32)];fixture.append(dict(**f,allOverlappedCellsBlocked=bool(cells.all()),coveredCells=int(cells.size)))
for a in j['areas']:
 w=next(x for x in wam['areas']if x['id']==a['id']);legs=[r for r in routes['rows']if r['id']=='spawn-to-'+a['id']];ends=[]
 for leg in legs:
  x,y=leg['final'];ends.append(dict(input=leg['input'],actualNativeFinal=leg['final'],insideAuthored=a['x']<=x<a['x']+a['width'] and a['y']<=y<a['y']+a['height'],insideWAM=w['x']<=x<w['x']+w['width'] and w['y']<=y<w['y']+w['height'],passNative=leg['pass']))
 arrivals.append(dict(id=a['id'],arrivals=ends,allPass=len(ends)>=2 and {e['input']for e in ends}=={'desktop','touch'} and all(e['insideAuthored']and e['insideWAM']and e['passNative'] for e in ends)))
report=dict(physicalPortalFootGroups=fixture,actualPortalArrivals=arrivals,allPass=all(f['allOverlappedCellsBlocked']for f in fixture)and all(a['allPass']for a in arrivals));(P/'validation/fixtures-and-arrivals.json').write_text(json.dumps(report,indent=2))
assert report['allPass']
# Independently decode actual TMJ atlases. Never substitute the source composite as an occupied base.
sets=[(t,Image.open(P/'map32'/t['image']).convert('RGBA'))for t in m['tilesets']];lo=Image.new('RGBA',(2048,1536));hi=Image.new('RGBA',lo.size);dst=lo
for l in m['layers']:
 if l['name']=='floorLayer':dst=hi
 if l['type']!='tilelayer' or l.get('opacity',1)==0:continue
 for i,gid in enumerate(l['data']):
  if not gid:continue
  ts,im=max((t for t in sets if t[0]['firstgid']<=gid),key=lambda t:t[0]['firstgid']);k=gid-ts['firstgid'];x=k%ts['columns']*32;y=k//ts['columns']*32;dst.alpha_composite(im.crop((x,y,x+32,y+32)),((i%64)*32,(i//64)*32))
master=Image.open(R/'source/calm-master-native.png').convert('RGBA');assert Image.alpha_composite(lo,hi).tobytes()==master.tobytes()
sheet=Image.open(R/'source/greg-reference.png').convert('RGBA');north=sheet.crop((32,96,64,128));south=sheet.crop((32,0,64,32));occ=lo.copy();selected=[]
for ai,a in enumerate(j['anchors']):
 legs=[r for r in routes['rows']if r['id']=='spawn-to-'+a['id']and r['input']=='desktop'];assert legs
 xy=list(map(round,legs[0]['final']));direction='south'if a['direction']=='south'else'north';f=Image.open(R/f'source/proof-actors/{ai%8}-{direction}.png').convert('RGBA');occ.alpha_composite(f,(xy[0]-16,xy[1]-16));selected.append(dict(id=a['id'],nativeFinal=xy,proofActorIndex=ai%8,direction=direction))
occ.alpha_composite(hi);occ.save(P/'review/actual-native-arrivals.png')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
card=Image.new('RGB',(1280,620),'#131a2b');d=ImageDraw.Draw(card);d.text((18,12),'Actual source-native arrivals · decoded TMJ layers · unchanged 32 px avatar',font=FB,fill='#ede9dc')
for i,a in enumerate(selected):
 x,y=a['nativeFinal'];px=(i%4)*320;py=48+(i//4)*282;crop=occ.crop((x-152,y-160,x+152,y+64));card.paste(crop,(px+8,py));d.text((px+8,py+230),a['id'],font=FB,fill='#ede9dc');d.text((px+8,py+250),f"Native final ({x}, {y})",font=F,fill='#b9c4d7')
card.save(P/'review/actual-arrival-contact-sheet.png')
(P/'validation/decoded-proof.json').write_text(json.dumps(dict(sourceCompositeEqualsDecodedRuntime=True,foregroundAlphaPixels=int(np.count_nonzero(np.asarray(hi)[:,:,3])),avatarNativeFrame=[32,32],body=[16,16],scale=1,actualNativeTargets=selected,masterSHA256=hashlib.sha256((R/'source/calm-master-native.png').read_bytes()).hexdigest(),tmjSHA256=hashlib.sha256((P/'map32/celestial-transit-garden-calm-draft.tmj').read_bytes()).hexdigest()),indent=2))
print('Fixture groups',len(fixture),'all blocked; all 5 desktop/touch native final targets inside actualareas; decoded proof byte exact.')
