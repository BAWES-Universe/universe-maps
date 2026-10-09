from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
R=Path(__file__).resolve().parents[1];g=json.loads((R/'garden-manifest.json').read_text());base=Image.open(R/'layers/garden-base.png').convert('RGBA');sheet=Image.open(R/'preview/greg-gulf-woka-v3.png').convert('RGBA');fg=Image.open(R/'layers/garden-foreground.png').convert('RGBA')
allSeats=base.copy();checks=[]
for b in g['benches']:
 x,y=b['seat']['x'],b['seat']['y'];sprite=sheet.crop((32,b['spriteRow']*32,64,b['spriteRow']*32+32));im=base.copy();im.alpha_composite(sprite,(x-16,y-16));before=im.copy();mask=Image.new('L',(1024,1024),0);d=ImageDraw.Draw(mask);d.rectangle(b['occlusion'],fill=255);d.rectangle((x-16,y-16,x+15,y+2),fill=0);over=fg.copy();alpha=np.minimum(np.array(fg.getchannel('A')),np.array(mask));over.putalpha(Image.fromarray(alpha));im.alpha_composite(over)
 headBox=(x-16,y-16,x+16,y+3);headUnchanged=np.array_equal(np.array(before.crop(headBox)),np.array(im.crop(headBox)))
 rawmask=np.zeros((1024,1024),dtype=np.uint8);rawmask[y-16:y+16,x-16:x+16]=np.array(sprite.getchannel('A'));occluded=int(np.count_nonzero((alpha>0)&(rawmask>0)))
 checks.append({'bench':b['id'],'nativeAvatarFrame':[32,32],'headPixelsPreserved':headUnchanged,'opaqueBodyPixelsBehindBenchRim':occluded,'spriteRow':b['spriteRow'],'center':b['seat'],'sittingAnimation':False})
 im.crop((320,340,660,690)).save(R/f"docs/seat-{b['id']}-native.png")
 allSeats.alpha_composite(sprite,(x-16,y-16));allSeats.alpha_composite(over)
allSeats.crop((320,340,660,690)).save(R/'docs/four-cardinal-seats-native.png')
result={'passed':all(c['headPixelsPreserved'] and c['opaqueBodyPixelsBehindBenchRim']>0 for c in checks),'scope':'pixel-accurate offline map render of four functional bench-position slots, not a browser screenshot or invented sitting animation','checks':checks}
(R/'docs/seat-occlusion-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
