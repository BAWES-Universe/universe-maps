from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];base=Image.open(R/'layers/campus-base.png').convert('RGBA');above=Image.open(R/'layers/campus-above.png').convert('RGBA');greg=Image.open(R/'validation/greg.png').convert('RGBA');read=lambda p:json.loads(p.read_text())
# Render the real first animation frames between base and above layers.
for e in read(R/'effects/effects.json')['effects']:base.alpha_composite(Image.open(R/e['frames'][0]).convert('RGBA'),tuple(e['origin']))
routes=read(R/'docs/integrated-office-routes10.json')['rows'];ends={x['id']:x['final']for x in routes if x['direction']=='arrival'}
anchors=read(R/'office-input/anchors.json');face={a['id']:a.get('facing','south')for a in anchors};frame={'north':10,'south':1,'west':4,'east':7}
work=[a['id']for a in anchors if a['kind']=='work-seat'and a.get('workSide')=='left'];staff=['reception-staff-1','reception-staff-2','reception-visitor-1'];trace=next(x['trace']for x in read(R/'docs/compiled-public-route-traces10.json')if x['id']=='booth1-arrival');shorePoint=min(trace,key=lambda p:(p[0]-2680)**2+(p[1]-2192)**2);panes=[('Eight-seat office | left four shown',(816,224,1328,608),[(ends[k]['x'],ends[k]['y'],frame[face[k]])for k in work]),('Two reception positions | visitor approach',(1280,640,1792,1024),[(ends[k]['x'],ends[k]['y'],frame[face[k]])for k in staff]),('Fountain loop | unchanged native Greg',(680,1256,1192,1640),[(936,1568,10)]),('Shore-to-market route | native scale',(2368,1888,2880,2272),[(shorePoint[0],shorePoint[1],1)])]
out=Image.new('RGBA',(1024,864),(17,29,35,255));d=ImageDraw.Draw(out)
for i,(label,box,people)in enumerate(panes):
 im=base.crop(box)
 for x,y,fr in people:im.alpha_composite(greg.crop((fr%3*32,fr//3*32,fr%3*32+32,fr//3*32+32)),(round(x-box[0])-16,round(y-box[1])-16))
 im.alpha_composite(above.crop(box));x=(i%2)*512;y=(i//2)*416;out.alpha_composite(im,(x,y+28));d.text((x+8,y+8),label,fill='white')
d.text((8,838),'STATIC NATIVE-SOURCE PROOF | Greg32 at1:1 | source-route checks only; live client unverified',fill='white');out.save(R/'docs/native32-player-scale-review.png')
ov=Image.open(R/'docs/Campus10-compiled-half.png').convert('RGB');card=Image.new('RGB',(ov.width,ov.height+42),(17,29,35));card.paste(ov,(0,0));ImageDraw.Draw(card).text((14,ov.height+13),'Lush Campus10 | compiled native32 candidate | source routes checked; live acceptance pending',fill='white');card.save(R/'docs/Lush-Campus10-compiled-overview.png')
