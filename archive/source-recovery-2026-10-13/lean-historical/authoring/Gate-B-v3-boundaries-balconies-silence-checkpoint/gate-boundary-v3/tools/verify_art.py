from map_render import MapRenderer,R
from PIL import Image,ImageDraw,ImageChops
import json
A=MapRenderer(R/'baseline/gate-b-v2.tmj');B=MapRenderer(R/'publish/public/butterfly-town/gate-b/v3/gate.tmj')
checks=[]
for ms in(0,600,1800,3600,5400):
 a=A.compose(ms);b=B.compose(ms);diff=ImageChops.difference(a,b);n=sum(any(p[:3])for p in diff.getdata());checks.append({'animationTimeMs':ms,'changedArtworkPixels':n});
 if ms==0:b.save(R/'results/candidate-full-native.png')
# Authored-source composites at native Woka32; every zoomed sheet is clearly a diagnostic crop.
points=[('west-behind-tree',216,968),('west-behind-lamp',268,968),('west-balcony-floor',128,992),('east-behind-tree',740,968),('east-behind-lamp',692,1000),('east-balcony-floor',848,992)]
rows=[]
for name,x,y in points:
 withF=B.compose(0,{'x':x,'y':y});without=B.compose(0,{'x':x,'y':y},False)
 delta=ImageChops.difference(withF,without);n=sum(any(p[:3])for p in delta.crop((x-16,y-16,x+16,y+16)).getdata());rows.append({'id':name,'player':{'x':x,'y':y},'occludedWokaPixels':n})
 box=(max(0,x-64),y-64,min(960,x+64),y+64)
 sheet=Image.new('RGB',(512,302),'#15202e');d=ImageDraw.Draw(sheet);d.text((10,7),name+' | native32 source composite',fill='white');d.text((10,25),'Without foreground (left) / candidate (right)',fill='white');sheet.paste(without.crop(box).resize((256,256),Image.Resampling.NEAREST),(0,46));sheet.paste(withF.crop(box).resize((256,256),Image.Resampling.NEAREST),(256,46));sheet.save(R/f'results/{name}-comparison.png')
# Final grid only as evidence overlay; not shipped as map art.
im=B.compose();overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay);coll=B.m['layers'][0]['data']
for i,g in enumerate(coll):
 if not g:d.rectangle((i%30*32,i//30*32,i%30*32+31,i//30*32+31),fill=(30,245,125,55),outline=(50,255,150,110))
Image.alpha_composite(im,overlay).crop((0,480,960,1440)).save(R/'results/candidate-grid.png')
report={'evidence':'Offline atlas/layer composite using exact unchanged artwork and native32 Woka asset. Not live runtime or iPhone proof.','pixelIdentity':checks,'occlusion':rows};(R/'results/art-layer-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert all(x['changedArtworkPixels']==0 for x in checks)
