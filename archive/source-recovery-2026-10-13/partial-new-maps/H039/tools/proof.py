from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];L=json.loads((R/'source/layout.json').read_text());D=json.loads((R/'source/design.json').read_text());routes=json.loads((R/'validation/native-routes.json').read_text());meta=json.loads((R/'source/ACTOR-PROVENANCE.json').read_text())['actors'];base=Image.open(R/'review/decoded-ground.png').convert('RGBA');above=Image.open(R/'review/decoded-foreground.png').convert('RGBA');base=Image.alpha_composite(base,Image.open(R/'review/decoded-wet-0.png').convert('RGBA'));base=Image.alpha_composite(base,Image.open(R/'review/decoded-print-0.png').convert('RGBA'));fs={'south':1,'west':4,'east':7,'north':10};dirs=['south','west','east','north']
def actor(sheet,di):
 f=fs[di];return sheet.crop(((f%3)*32,(f//3)*32,(f%3)*32+32,(f//3)*32+32))
records=[]
def scene(actual):
 out=base.copy()
 for i,s in enumerate(L['seats']):
  m=meta[i%len(meta)];sheet=Image.open(R/'source/actors'/m['file']).convert('RGBA');assert hashlib.sha256((R/'source/actors'/m['file']).read_bytes()).hexdigest()==m['raw_sheet_sha256'];r=next(r for r in routes['rows']if r['name']==s['name']);x,y=r['arrival']['final']if actual else s['anchor'];di=dirs[r['arrival']['finalDirection']]if actual else s['direction'];out.alpha_composite(actor(sheet,di),(int(x)-16,int(y)-16));
  if actual:records.append(dict(name=s['name'],arrival=[x,y],direction=di,actor=m['file'],frame=fs[di],claim='Unmodified native32 standing frame at actual source-replay arrival, no automatic sitting or facing.'))
 return Image.alpha_composite(out,above)
actual=scene(True);actual.save(R/'review/occupied-native-arrival.png');manual=scene(False);manual.save(R/'review/occupied-manually-faced.png');empty=Image.alpha_composite(base,above)
contact=Image.new('RGB',(768,1152),'#14292c');dr=ImageDraw.Draw(contact)
for i,s in enumerate(L['seats']):
 x,y=s['anchor']
 for j,im in enumerate([empty,actual,manual]):
  crop=im.crop((x-48,y-40,x+48,y+56)).resize((384,384),Image.Resampling.NEAREST);contact.paste(crop,(i*384,j*384));dr.text((i*384+5,j*384+5),['empty beech stool','actual native arrival','manual facing only'][j],fill='white')
contact.save(R/'review/seat-contact-4x.png');(R/'validation/actor-proof.json').write_text(json.dumps(records,indent=2))
# Make collision legible: alpha overlay composited over actual decoded map.
over=Image.new('RGBA',empty.size);d=ImageDraw.Draw(over)
for y,row in enumerate(L['collision']):
 for x,blocked in enumerate(row):
  if blocked:d.rectangle((x*32,y*32,x*32+31,y*32+31),fill=(205,20,47,105))
dbg=Image.alpha_composite(empty,over);d=ImageDraw.Draw(dbg)
for s in L['seats']+L['anchors']:
 x,y=s['anchor'];d.rectangle((x-8,y,x+7,y+15),outline='#00ffff');d.text((x+9,y-10),s['name'],fill='white')
dbg.save(R/'review/collision-readable.png')
# Native32 scale at every interaction point with unmodified standing frames.
points=base.copy()
for i,s in enumerate([a for a in L['anchors']if 'id'in a]):
 m=meta[i%len(meta)];sheet=Image.open(R/'source/actors'/m['file']).convert('RGBA');r=next(r for r in routes['rows']if r['name']==s['name']);x,y=r['arrival']['final'];di=dirs[r['arrival']['finalDirection']];points.alpha_composite(actor(sheet,di),(int(x)-16,int(y)-16))
Image.alpha_composite(points,above).save(R/'review/controls-native32-arrival.png')
