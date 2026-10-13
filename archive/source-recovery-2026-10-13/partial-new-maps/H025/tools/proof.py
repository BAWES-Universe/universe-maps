from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];L=json.loads((R/'source/layout.json').read_text());routes=json.loads((R/'validation/native-routes.json').read_text());meta=json.loads((R/'source/ACTOR-PROVENANCE.json').read_text())['actors'];base=Image.open(R/'review/decoded-ground.png').convert('RGBA');above=Image.open(R/'review/decoded-foreground.png').convert('RGBA');dirs=['south','west','east','north'];frame={'south':1,'west':4,'east':7,'north':10};records=[];occupied=base.copy();staged=base.copy()
for i,s in enumerate(L['seats']):
 m=meta[i%len(meta)];p=R/'source/actors'/m['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['raw_sheet_sha256'];sheet=Image.open(p).convert('RGBA');r=next(q for q in routes['rows']if q['name']==s['name']);x,y=r['arrival']['final'];di=dirs[r['arrival']['finalDirection']];f=frame[di];sprite=sheet.crop(((f%3)*32,(f//3)*32,(f%3)*32+32,(f//3)*32+32));occupied.alpha_composite(sprite,(round(x)-16,round(y)-16));manual=frame[s['direction']];sprite=sheet.crop(((manual%3)*32,(manual//3)*32,(manual%3)*32+32,(manual//3)*32+32));staged.alpha_composite(sprite,(s['anchor'][0]-16,s['anchor'][1]-16));records.append(dict(name=s['name'],room=s['room'],arrival=[x,y],target=s['anchor'],exactArrival=r['exactArrival'],direction=di,frame=f,actor=m['file'],claim='Actual native-source replay arrival using unchanged standing frame; no sitting/facing implementation.'))
occupied=Image.alpha_composite(occupied,above);staged=Image.alpha_composite(staged,above);occupied.save(R/'review/occupied-native-arrival.png');empty=Image.alpha_composite(base,above)
for r in L['rooms']:
 x,y,w,h=r['bounds'];
 if r['seats']:occupied.crop((x,y,x+w,y+h)).save(R/'review'/f"{r['id']}-occupied-native-arrival.png");
 for i,s in enumerate(r['seats']):
  x,y=s['anchor'];out=Image.new('RGB',(768,384),'#18252d');dr=ImageDraw.Draw(out)
  for j,im in enumerate([empty,occupied,staged]):
   crop=im.crop((x-32,y-32,x+32,y+64)).resize((256,384),Image.Resampling.NEAREST);out.paste(crop,(j*256,0));dr.text((j*256+4,3),['empty','actual native arrival','manual facing only'][j],fill='white')
  out.save(R/'review'/f"{r['id']}-seat-{i+1}-4x.png")
(R/'validation/actor-proof.json').write_text(json.dumps(records,indent=2)+'\n')
