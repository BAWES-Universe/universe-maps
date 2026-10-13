from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];layout=json.loads((R/'evidence/layout.json').read_text());routes=json.loads((R/'evidence/native-routes.json').read_text())['rows'];sheet=Image.open(R/'source/woka-proof.png').convert('RGBA');out=Image.new('RGB',(800,960),(17,23,28));label=ImageDraw.Draw(out);results=[]
for i,seat in enumerate(layout['seats']):
 room=layout['rooms'][seat['room']];ox,oy=room['offset'];x,y=seat['anchor'];painting=Image.open(R/'runtime'/f"{seat['room']}.png").convert('RGBA');mask=Image.new('1',painting.size);ImageDraw.Draw(mask).polygon([tuple(p)for p in seat['surfacePolygon']],fill=1)
 arrivals=[row for row in routes if row['id'].endswith('-to-'+seat['name'])];assert arrivals and all(row['pass']and row['final']==[ox+x,oy+y]for row in arrivals)
 directions=sorted(set(row['direction']for row in arrivals));contact=[]
 for direction in directions:
  frame=sheet.crop((32,direction*32,64,direction*32+32));points=[(x+sx-16,y+sy-16)for sy in range(25,28)for sx in range(12,21)if frame.getpixel((sx,sy))[3]];assert len(points)==27
  outside=[list(p)for p in points if not mask.getpixel(p)];contact.append(dict(direction=direction,realOpaquePelvisPixels=len(points),outsideTracedSurface=outside,**{"pass":not outside}))
 box=(x-30,y-30,x+30,y+50);base=painting.crop(box);row=i//2;col=i%2;cx=col*400;cy=row*480;label.text((cx+4,cy+5),seat['name'],fill='white');label.text((cx+4,cy+20),f'Exact native origin {x},{y}; pelvis y{y+9}..{y+11}',fill='white')
 out.paste(base.resize((180,240),Image.Resampling.NEAREST),(cx,cy+45))
 actor=base.copy();direction=directions[0];frame=sheet.crop((32,direction*32,64,direction*32+32));actor.alpha_composite(frame,(14,14));out.paste(actor.resize((180,240),Image.Resampling.NEAREST),(cx+195,cy+45))
 detail=painting.crop((x-16,y,x+16,y+18)).resize((256,144),Image.Resampling.NEAREST);d=ImageDraw.Draw(detail)
 for sy in range(9,12):d.rectangle((12*8,sy*8,21*8-1,(sy+1)*8-1),outline=(255,245,80),width=1)
 out.paste(detail,(cx+60,cy+300));label.text((cx+4,cy+450),'Real lower torso patch over decoded cushion; no sitting animation',fill='white')
 results.append(dict(name=seat['name'],nativeAnchor=[ox+x,oy+y],floorClick=[ox+seat['floorClick'][0],oy+seat['floorClick'][1]],surfacePolygon=seat['surfacePolygon'],arrivalCount=len(arrivals),directions=contact,**{"pass":all(c['pass']for c in contact)}))
report=dict(allPass=all(r['pass']for r in results),scope='Actual unchanged native arrival coordinates and directions, real pinned32 sprite central lower torso columns12..20 rows25..27, and visually traced full cushion surface polygons. Not a seated-animation, automatic-facing or live-render proof. The surrounding garment may overhang a stool; the27 opaque central pelvis pixels establish contact.',spriteSHA256=hashlib.sha256((R/'source/woka-proof.png').read_bytes()).hexdigest(),rows=results)
(R/'evidence/seat-contact.json').write_text(json.dumps(report,indent=2));out.save(R/'review/seat-contact-4x.png');print(json.dumps(report,indent=2));assert report['allPass']
