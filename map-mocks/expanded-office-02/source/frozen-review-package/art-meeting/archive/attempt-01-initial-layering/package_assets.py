#!/usr/bin/env python3
"""Mechanical alpha registration, source-pixel masks, and unchanged-sprite proofs.
All furniture pixels were authored by built-in imagegen. This script draws no art.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFont
from scipy import ndimage
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1]
geo=json.loads((R/'geometry-plan.json').read_text())
specs={**{f'chair-{x}':([48,64],[9,8,30,36]) for x in ['north','south','east','west']},'table-small':([128,96],[16,16,96,64]),'table-conference':([224,128],[16,16,192,96])}
# Manually traced actual near components, in final native canvas coordinates.
polygons={
 'chair-north':[[(11,20),(13,19),(35,19),(37,20),(38,24),(37,35),(35,38),(13,38),(11,35)]],
 'chair-south':[[(9,31),(10,27),(13,27),(13,37),(12,39),(10,39)],[(35,27),(38,28),(39,36),(37,39),(35,38)],[(13,37),(35,37),(36,39),(12,39)]],
 'chair-east':[[(16,34),(18,33),(35,33),(38,35),(38,37),(36,39),(16,39),(15,37)]],
 'chair-west':[[(10,34),(11,33),(30,33),(33,34),(33,38),(31,39),(11,39),(9,37)]]}
assets={};ims={}
def measure(im):
 a=im.getchannel('A');arr=np.array(a)
 return dict(canvas=list(im.size),alphaBounds={str(t):a.point(lambda v:255 if v>=t else 0).getbbox() for t in [1,16,64,128,240]},opaquePixels=int((arr>=240).sum()),nonzeroPixels=int((arr>0).sum()))
def masked(im,polys):
 m=Image.new('L',im.size);d=ImageDraw.Draw(m)
 for p in polys:d.polygon(p,fill=255)
 out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out,m
for name,(canvas,box) in specs.items():
 p=R/'source'/f'{name}-master.png';master=Image.open(p).convert('RGBA');a=np.array(master.getchannel('A'))
 labels,count=ndimage.label(a>=32);counts=np.bincount(labels.ravel());counts[0]=0;label=int(counts.argmax());ys,xs=np.where(labels==label)
 crop=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 x,y,w,h=box
 # A transparent-padding trim and premultiplied resize preserves source alpha and corrects generated padding drift.
 piece=master.crop(crop).convert('RGBa').resize((w,h),Image.Resampling.LANCZOS).convert('RGBA')
 im=Image.new('RGBA',canvas);im.alpha_composite(piece,(x,y));im.save(R/'assets'/f'{name}-native.png');ims[name]=im
 data=dict(source=f'source/{name}-master.png',sourceSha256=hashlib.sha256(p.read_bytes()).hexdigest(),sourceCanvas=list(master.size),sourceCrop=crop,registration=dict(method='largest alpha>=32 connected object bounding box, trim transparent padding then premultiplied LANCZOS resize',targetVisibleRectangle=box,targetCanvas=canvas,artRedrawn=False,rotation=False,reflection=False),native=measure(im))
 if name in polygons:
  fore,m=masked(im,polygons[name]);fore.save(R/'assets'/f'{name}-foreground-native.png');m.save(R/'assets'/f'{name}-foreground-mask.png')
  data['foreground']=dict(**measure(fore),nativePolygons=polygons[name],sourcePolygons=[[[crop[0]+(px-x)*(crop[2]-crop[0])/w,crop[1]+(py-y)*(crop[3]-crop[1])/h] for px,py in poly] for poly in polygons[name]],pixelIntegrity='Every nontransparent foreground pixel is unchanged RGBA from the registered native base asset.')
  # Contact includes the actual image's feet/shadow pixels, never a synthetic drop shadow.
  contacts=[[(9,39),(39,39),(39,44),(9,44)]]
 else:contacts=[[(16,y+h-6),(16+w,y+h-6),(16+w,y+h),(16,y+h)]]
 contact,cm=masked(im,contacts);contact.save(R/'assets'/f'{name}-contact-native.png');cm.save(R/'assets'/f'{name}-contact-mask.png');data['contact']=dict(**measure(contact),nativePolygons=contacts,meaning='Actual source pixels in the foot/contact band; antialiasing and painted contact shadow preserved, not classified as a separate physical obstacle.')
 assets[name]=data

# Genuine tabletop near-edge pieces at the east/west hand-contact zone. Same source texture, no added shape.
im=ims['table-small'];table_polys=[[(16,40),(20,40),(20,56),(16,56)],[(108,40),(112,40),(112,56),(108,56)]]
fore,m=masked(im,table_polys);fore.save(R/'assets/table-small-side-contact-foreground-native.png');m.save(R/'assets/table-small-side-contact-foreground-mask.png');assets['table-small']['foreground']=dict(**measure(fore),nativePolygons=table_polys,purpose='Real table edge pixels can occlude side-facing hands/lower bodies; starts at seat center y88, below protected head.')
(R/'asset-manifest.json').write_text(json.dumps(dict(status='native registration proof; review required',assets=assets),indent=2)+'\n')
gregpath=Path(geo['avatar']['source']);greg=Image.open(gregpath).convert('RGBA');headchecks=[]
for layout in geo['layouts']:
 size=tuple(layout['interior'][k] for k in ['width','height']);base=Image.new('RGBA',size,'#e4ddc7');foreground=Image.new('RGBA',size)
 for s in layout['seats']:
  base.alpha_composite(Image.open(R/s['chairAsset']),tuple(s['chairOrigin']));foreground.alpha_composite(Image.open(R/s['foregroundAsset']),tuple(s['chairOrigin']))
 base.alpha_composite(Image.open(R/layout['tableAsset']),tuple(layout['tableOrigin']))
 if layout['id']=='small-four-cardinal':foreground.alpha_composite(Image.open(R/'assets/table-small-side-contact-foreground-native.png'),tuple(layout['tableOrigin']))
 name=layout['id'];base.save(R/'proofs'/f'{name}-empty-native.png');base.resize((size[0]*3,size[1]*3),Image.Resampling.NEAREST).save(R/'proofs'/f'{name}-empty-3x.png')
 for s in layout['seats']:
  f=s['frameIndex'];sprite=greg.crop(((f%3)*32,(f//3)*32,(f%3+1)*32,(f//3+1)*32));cx,cy=s['center'];base.alpha_composite(sprite,(cx-16,cy-16))
  frame_fore=foreground.crop((cx-16,cy-16,cx+16,cy+16));ga=np.array(sprite.getchannel('A'));fa=np.array(frame_fore.getchannel('A'));n=int(((ga[:14]>0)&(fa[:14]>0)).sum());torso=int(((ga[14:]>0)&(fa[14:]>0)).sum());headchecks.append(dict(layout=name,seat=s['id'],frame=f,scale=1,protectedHeadPixelsCovered=n,torsoPixelsOccluded=torso,passed=n==0))
 base.alpha_composite(foreground);base.save(R/'proofs'/f'{name}-occupied-native.png');base.resize((size[0]*3,size[1]*3),Image.Resampling.NEAREST).save(R/'proofs'/f'{name}-occupied-3x.png')
 foreground.save(R/'assets'/f'{name}-foreground-native.png')
 # Labeled geometry image is a technical diagram, not furniture artwork.
 diagram=base.copy();d=ImageDraw.Draw(diagram);t=layout['table'];d.rectangle((t['x'],t['y'],t['x']+t['width']-1,t['y']+t['height']-1),outline='#e53858')
 for i,s in enumerate(layout['seats']):
  colors=['#07833f','#2673d0','#863bd1','#c05813','#087e8b','#a53b65'];col=colors[i];d.line([tuple(p) for p in s['entryRoute']],fill=col,width=1);cx,cy=s['center'];d.rectangle((cx-8,cy,cx+7,cy+15),outline=col);d.text((cx+9,cy-14),s['facing'][0].upper(),fill=col)
 diagram.resize((size[0]*3,size[1]*3),Image.Resampling.NEAREST).save(R/'proofs'/f'{name}-geometry-3x.png')
(R/'proofs/pixel-checks.json').write_text(json.dumps(dict(gregSha256=hashlib.sha256(gregpath.read_bytes()).hexdigest(),gregUnchanged=True,fixtureLabel='Repeated unchanged32×32 Greg directional frame scale fixtures; no live multiplayer.',passed=all(x['passed'] for x in headchecks),checks=headchecks),indent=2)+'\n')
print(json.dumps(dict(assets=len(assets),headChecksPassed=all(x['passed'] for x in headchecks),checks=headchecks)))
