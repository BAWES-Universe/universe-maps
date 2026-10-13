from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
R=Path(__file__).resolve().parents[1];P=R/'lantern-souk-bazaar-r5-fountain-motion';S=R/'source/static';j=lambda p:json.loads(p.read_text())
meta=j(P/'source/motion-layout.json');m=j(P/'map32'/f"{meta['slug']}.tmj");captures=j(P/'validation/plugin-frame-replay.json')['captures'];ts=m['tilesets'][-1];atlas=Image.open(P/'map32'/ts['image']).convert('RGBA');base=Image.open(S/'empty-native.png').convert('RGBA');occupied=Image.open(S/'occupied-native.png').convert('RGBA');mask=np.zeros((base.height,base.width),bool);wm=np.array(Image.open(P/'source/fountain-water-mask.png'))>0;mask[512:800,800:1120]=wm
selected={}
for c in captures:
 k=(c['gids'][0]-ts['firstgid'])%8
 if k not in selected:selected[k]=c
assert set(selected)==set(range(8))
frames=[];stats=[];thumbs=[]
for k in range(8):
 c=selected[k];layer=Image.new('RGBA',base.size)
 for p,gid in zip(meta['placements'],c['gids']):
  local=gid-ts['firstgid'];tile=atlas.crop((local%ts['columns']*32,local//ts['columns']*32,local%ts['columns']*32+32,local//ts['columns']*32+32));layer.alpha_composite(tile,(p['cell'][0]*32,p['cell'][1]*32))
 full=Image.alpha_composite(base,layer);occ=Image.alpha_composite(occupied,layer);diff=np.any(np.array(full)!=np.array(base),axis=2);assert not (diff&~mask).any();stats.append(dict(frame=k,changedPixels=int(diff.sum()),outsideWaterChanged=0,actualPluginCaptureTick=c['tick']))
 occ.save(P/'review'/f'occupied-native-frame-{k:02}.png');detail=occ.crop((800,528,1120,784));frames.append(detail.resize((640,512),Image.Resampling.NEAREST));thumbs.append(detail)
palette=frames[0].convert('RGB').quantize(colors=256,dither=Image.Dither.NONE)
quant=[f.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
quant[0].save(P/'review/fountain-water-loop.gif',save_all=True,append_images=quant[1:],duration=140,loop=0,disposal=2,optimize=False)
contact=Image.new('RGB',(1280,576),'#112729');d=ImageDraw.Draw(contact)
for k,im in enumerate(thumbs):
 x=k%4*320;y=k//4*288;contact.paste(im,(x,y+24));d.text((x+10,y+7),f'Native frame {k+1} / 8',fill='white')
contact.save(P/'review/fountain-frame-contact-sheet.png');(P/'validation/native-render.json').write_text(json.dumps(dict(scope='Runtime atlas rendering uses actual pinned plugin selected global IDs; not a live browser screenshot.',frames=stats,allOutsideWaterPixelsExact=True,meaningfulWaterPixelCoverage=min(s['changedPixels'] for s in stats),sourceStaticReferenceUnchanged=True,allPass=True),indent=2)+'\n');print(stats)
