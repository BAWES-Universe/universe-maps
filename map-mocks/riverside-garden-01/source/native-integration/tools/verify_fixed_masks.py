from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
N=Path(__file__).resolve().parents[1];R=N.parent;g=json.loads((N/'native-manifest.json').read_text());base=Image.open(R/'layers/garden-base.png').convert('RGBA');fg=Image.open(N/'masks/benches-fixed-foreground.png').convert('RGBA');mask=np.array(fg.getchannel('A'));greg=Image.open(R/'preview/greg-gulf-woka-v3.png').convert('RGBA');proof=base.copy();checks=[]
for s in g['spots']:
 x,y=s['position']['x'],s['position']['y'];samples=[]
 for col in range(3):
  sprite=greg.crop((col*32,s['spriteRow']*32,col*32+32,s['spriteRow']*32+32));a=np.array(sprite.getchannel('A'));region=mask[y-16:y+16,x-16:x+16];heads=int(np.count_nonzero((region[:19]>0)&(a[:19]>0)));body=int(np.count_nonzero((region[19:]>0)&(a[19:]>0)));samples.append({'frame':col,'opaqueHeadPixelsCovered':heads,'opaqueLowerBodyPixelsCovered':body})
 sprite=greg.crop((32,s['spriteRow']*32,64,s['spriteRow']*32+32));one=base.copy();one.alpha_composite(sprite,(x-16,y-16));one.alpha_composite(fg);one.crop((320,340,660,690)).save(N/f"docs/{s['id']}-static-seat-native.png");proof.alpha_composite(sprite,(x-16,y-16));checks.append({'id':s['id'],'headClearAtFixedPosition':all(c['opaqueHeadPixelsCovered']==0 for c in samples),'samples':samples})
# Every foreground pixel is identical regardless of how many avatars are drawn or where.
proof.alpha_composite(fg);proof.crop((320,340,660,690)).save(N/'docs/four-static-bench-positions-native.png');proof.save(N/'docs/static-bench-composition-native.png')
result={'passed':all(c['headClearAtFixedPosition'] for c in checks),'scope':'fixed architectural masks over original unchanged32×32 facing sprites at permanent grid positions; no per-avatar erased rectangle and no stateful collision','fixedMaskSha256':hashlib.sha256((N/'masks/benches-fixed-mask.png').read_bytes()).hexdigest(),'checks':checks,'sittingAnimation':False};(N/'docs/fixed-mask-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
