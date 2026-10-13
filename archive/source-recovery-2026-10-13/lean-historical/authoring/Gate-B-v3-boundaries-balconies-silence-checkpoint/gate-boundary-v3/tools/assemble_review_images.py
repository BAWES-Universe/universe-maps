from map_render import MapRenderer,R
from PIL import Image,ImageDraw
import json
m=MapRenderer(R/'publish/public/butterfly-town/gate-b/v3/gate.tmj');im=m.compose();over=Image.new('RGBA',im.size);d=ImageDraw.Draw(over)
for i,v in enumerate(m.m['layers'][0]['data']):
 x,y=i%30*32,i//30*32
 if not v:d.rectangle((x,y,x+31,y+31),fill=(0,240,130,45),outline=(0,255,160,170))
reg=json.load(open(R/'results/annotation-registration.json'))
for r in reg['regions']:d.rectangle(r['worldRect'],outline=(255,60,50,255)if r['id'].startswith('red')else(40,255,90,255),width=3)
d.rectangle((448,1088,544,1184),fill=(150,90,255,35),outline=(200,145,255,255),width=2)
base=Image.alpha_composite(im,over);base.save(R/'results/registered-boundary-overlay-world.png')
t=reg['screenFromWorld'];mapped=base.transform((834,822),Image.Transform.AFFINE,(1/t['sx'],0,-t['offsetX']/t['sx'],0,1/t['sy'],-t['offsetY']/t['sy']),Image.Resampling.BICUBIC)
sheet=Image.new('RGB',(1668,868),'#142031');sheet.paste(Image.open('/workspace/shared/gate-user-boundary-feedback/marked-gate.png'),(0,46));sheet.paste(mapped,(834,46));d=ImageDraw.Draw(sheet);d.text((16,12),'User feedback (left) | candidate collision cells + registered feedback (right)',fill='white');d.text((850,28),'Green tint = open cells; purple = spawn conversation-silent zone',fill='white');sheet.save(R/'results/annotation-boundary-comparison.png')
files=['west-behind-tree','west-behind-lamp','west-balcony-floor','east-behind-tree','east-behind-lamp','east-balcony-floor'];contact=Image.new('RGB',(1024,906),'#142031')
for i,n in enumerate(files):contact.paste(Image.open(R/f'results/{n}-comparison.png'),(i%2*512,i//2*302))
contact.save(R/'results/native32-occlusion-contact-sheet.png')
