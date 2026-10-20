"""Bounded source preparation only: no island or runtime mutation."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
r=Path(__file__).resolve().parents[2];root=r/'source/cafe-candidates';im=Image.open(root/'cafe-furniture-candidate.png').convert('RGBA');out=root/'extracted';out.mkdir(exist_ok=True)
spec={
 'lounge-front':((40,40,775,360),176), 'lounge-rear':((795,55,1505,360),176),
 'chair-front':((20,395,270,660),48),'chair-rear':((275,400,520,660),48),
 'chair-right':((548,390,750,660),48),'chair-left':((765,390,970,660),48),
 'table-cups':((990,415,1250,650),64),'table-plain':((1260,415,1520,650),64),
 'stool-front':((45,710,210,950),32),'stool-alt':((235,705,415,950),32),
 'bench-front':((475,705,985,955),128),'bench-rear':((1005,705,1520,955),128)}
board=Image.new('RGB',(720,480),'#e8dfcd');d=ImageDraw.Draw(board);audit=[]
for i,(name,(box,width)) in enumerate(spec.items()):
 a=im.crop(box);bb=a.getchannel('A').point(lambda n:255 if n>=180 else 0).getbbox();a=a.crop(bb);scale=width/a.width;a=a.resize((width,round(a.height*scale)),Image.Resampling.LANCZOS);a.save(out/(name+'.png'))
 x=16+(i%3)*240;y=12+(i//3)*116;board.paste(a,(x,y+18),a);d.text((x,y),name,fill='#30281e');d.rectangle((x+190,y+42,x+221,y+73),outline='#704329',width=1);d.text((x+188,y+80),'32px',fill='#30281e')
 audit.append(dict(name=name,sourceBox=box,alphaBounds=bb,scale=scale,rasterSize=list(a.size),status='source sizing proposal only; no occupied-runtime validation'))
board.save(r/'review/cafe-source-calibration.png')
(root/'calibration.json').write_text(json.dumps(audit,indent=2)+'\n')
scope={'candidateCommit':'03de3b07f061d7fbbbb23cf90778e72914b14414','status':'source preparation; not integrated','groundCandidateWholePlateRejected':True,'preserve':'existing pond, waterfall, cliff, bar, bridge and stone connection coordinates','usableTimberSampleCandidateBox':[260,455,620,515],'requiredRegisteredPatch':{'source':'campus-site-cutout.png','referenceBox':[130,720,480,810],'worldBox':[2182,4208,1050,270],'output':'timber deck surface only with transparent exterior; precisely follow current curved stone/deck perimeter and bar base; exclude structural stone connection'},'requiredForegroundMask':{'referenceBox':[262,758,480,826],'worldBox':[2578,4322,654,204],'output':'separate current central lamp/planter, front balustrade and foliage occluders; preserve their positions and antialiased boundary'},'forbidden':'replace whole generated district, move bridges, nonuniformly stretch candidate or paint timber over foreground objects'}
(root/'restoration-patch.json').write_text(json.dumps(scope,indent=2)+'\n')
