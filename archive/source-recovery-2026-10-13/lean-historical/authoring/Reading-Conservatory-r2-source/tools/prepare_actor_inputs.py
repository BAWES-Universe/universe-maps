from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'source-assets';O=R/'candidate';cache=R.parent/'native-woka-cache';l=json.load(open(O/'source/layout.json'))
files=['Female 04-1.png','Male 09-4.png','Female 12-1.png','Male 02-3.png','Female 22-1.png','Male 03-3.png','Female 19-4.png','Male 15-2.png','Male 01-4.png','Female 03-3.png']
dirs=['south','west','east','north'];meta=[];overlays=[Image.new('RGBA',(768,512)) for _ in dirs]
for seat,fn in zip(l['seats'],files):
 p=cache/fn;im=Image.open(p).convert('RGBA');assert im.size==(96,128);x,y=seat['anchor'];r={'seat':seat['name'],'anchor':seat['anchor'],'file':fn,'repository':'BAWES-Universe/workadventure-universe','repoCommit':'90a148c03e03401e26d236eaac9bea4123b42c57','path':'play/public/resources/characters/pipoya/'+fn,'raw_sheet_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'frames':{}}
 for k,d in enumerate(dirs):
  fr=im.crop((32,k*32,64,k*32+32));overlays[k].alpha_composite(fr,(x-16,y-16));r['frames'][d]={'index':k*3+1,'rgba_sha256':hashlib.sha256(fr.tobytes()).hexdigest()}
 meta.append(r)
for d,im in zip(dirs,overlays):im.save(S/f'proof-actors-{d}.png')
(S/'ACTOR-PROVENANCE.json').write_text(json.dumps({'scope':'Native32 unmodified idle frames, compiled at actual map anchors for reproducible review overlays. No raw sheets or sprites in runtime.','actors':meta},indent=2))
