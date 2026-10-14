from pathlib import Path
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];D=json.load(open(R/'source/design.json'));L=json.load(open(R/'source/layout.json'));routes=json.load(open(R/'validation/native-routes.json'));geo=json.load(open(R/'validation/geometry.json'));meta=json.load(open(R/'source/ACTOR-PROVENANCE.json'))['actors'];W,H=D['world'];base=Image.open(R/'review/decoded-ground.png').convert('RGBA');above=Image.open(R/'review/decoded-foreground.png').convert('RGBA');fs={'south':1,'west':4,'east':7,'north':10};dirs=['south','west','east','north'];records=[]
def scene(actual):
 out=base.copy()
 for i,s in enumerate(L['seats']):
  m=meta[i%len(meta)];sheet=Image.open(R/'source/actors'/m['file']).convert('RGBA');assert hashlib.sha256((R/'source/actors'/m['file']).read_bytes()).hexdigest()==m['raw_sheet_sha256'];r=next(r for r in routes['rows'] if r['name']==s['name']);x,y=r['arrival']['final'] if actual else s['anchor'];di=dirs[r['arrival']['finalDirection']] if actual else s['direction'];f=fs[di];im=sheet.crop((f%3*32,f//3*32,f%3*32+32,f//3*32+32));assert hashlib.sha256(im.tobytes()).hexdigest()==m['frames'][di]['rgba_sha256'];out.alpha_composite(im,(round(x)-16,round(y)-16))
  if actual:records.append(dict(name=s['name'],anchor=s['anchor'],nativeArrival=[x,y],direction=di,frame=fs[di],source=m,standingOnly=True))
 out.alpha_composite(above);return out
actual=scene(True);actual.save(R/'review/occupied-native-arrival.png');manual=scene(False);manual.save(R/'review/occupied-manually-faced.png');(R/'validation/actor-proof.json').write_text(json.dumps(dict(scope='Varied unmodified repository frames between decoded runtime layers; not live screenshot. Actual native arrival facing differs from manual work-facing review.',actors=records),indent=2))
contact=Image.new('RGB',(len(L['seats'])*192,384),'#182126');dr=ImageDraw.Draw(contact)
for i,s in enumerate(L['seats']):
 x,y=s['anchor']
 for j,im in enumerate([actual,manual]):
  crop=im.crop((x-32,y-32,x+32,y+32)).resize((192,192),Image.Resampling.NEAREST);contact.paste(crop,(i*192,j*192));dr.text((i*192+3,j*192+3),'arrival' if j==0 else 'manual facing',fill='white')
contact.save(R/'review/seats-3x.png')
p=R/'review/review.pdf';c=canvas.Canvas(str(p),pagesize=(960,700));c.setTitle(D['title']+' - native32 author review');
for title,img,caption in [('NATIVE32 ARRIVAL PROOF','occupied-native-arrival.png','Actual pinned native arrival coordinates/facing. Standing frames only. Independent and live review unverified.'),('SEAT AND BACKRAIL DEPTH','seats-3x.png','Top: actual arrival facing. Bottom: manually faced work positions. No automatic facing or sitting mechanic.'),('COLLISION AND SCENIC CONTEXT','collision.png','Red cells are solid. Northern fenced instrument ledge and isolated snow pockets are non-navigable scenic context.')]:
 c.setFillColorRGB(.08,.12,.16);c.rect(0,0,960,700,fill=1,stroke=0);c.setFillColorRGB(.95,.92,.82);c.setFont('Helvetica-Bold',22);c.drawString(24,666,D['id']+' / '+D['title']);c.setFont('Helvetica',13);c.drawString(24,640,title);im=Image.open(R/'review'/img);ratio=min(912/im.width,548/im.height);ww,hh=im.width*ratio,im.height*ratio;c.drawImage(ImageReader(im),24+(912-ww)/2,76+(548-hh)/2,ww,hh);c.setFont('Helvetica',9);c.drawString(24,38,caption);c.showPage()
c.save();subprocess.run(['pdftoppm','-scale-to','1400','-png',str(p),str(R/'review/pdf-page')],check=True,stdout=subprocess.DEVNULL)
print('proof and review PDF created',len(records))
