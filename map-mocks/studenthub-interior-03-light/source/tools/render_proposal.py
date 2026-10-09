from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];P=R;W,H=704,576
sheet=Image.open(R/'art-source/furniture-original.png').convert('RGBA');old=Image.open(R/'art-source/interiors-empty-floor.png').convert('RGBA');oldprops=Image.open(R/'art-source/interiors-furniture-alpha.png').convert('RGBA')
def shrink(im,size):
 im=im.crop(im.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox());im=im.convert('RGBa');im.thumbnail(size,Image.Resampling.LANCZOS);return im.convert('RGBA')
props={}
for name,box,size in [('desk',(45,143,488,413),(64,44)),('chair_n',(683,157,943,443),(26,32)),('chair_s',(1157,113,1403,459),(24,34)),('reception',(5,548,573,936),(144,92)),('table',(600,602,1028,901),(112,64)),('rug',(1048,563,1535,908),(192,140))]:
 props[name]=shrink(sheet.crop(box),size);props[name].save(R/'assets'/f'{name}.png')
props['plant']=shrink(oldprops.crop((47,326,119,416)),(32,40));props['smallplant']=shrink(oldprops.crop((57,418,142,488)),(32,36))
for n in ['couch_s','couch_n','couch_w','coffee']:
 props[n]=Image.open(P/'assets'/f'{n}.png').convert('RGBA')
# Original accepted v1 pale wall/bookcase identity, expanded as separate structures.
back=old.crop((72,43,829,210)).resize((W,112),Image.Resampling.LANCZOS)
front=old.crop((75,483,348,532));side=front.transpose(Image.Transpose.ROTATE_90).resize((24,240),Image.Resampling.LANCZOS)
pillar=old.crop((344,438,403,540)).resize((36,62),Image.Resampling.LANCZOS)
floor=Image.new('RGBA',(W,H));stone=Image.open(R/'art-source/sandstone-floor-original.png').convert('RGBA').resize((W-48,H-80),Image.Resampling.LANCZOS);floor.alpha_composite(stone,(24,80))
d=ImageDraw.Draw(floor);d.rectangle((28,104,W-29,H-18),outline=(139,167,144,255),width=3);d.rectangle((32,108,W-33,H-22),outline=(205,181,120,255),width=1)
floor.alpha_composite(back,(0,0));base=Image.new('RGBA',(W,H));over=Image.new('RGBA',(W,H));placed=[]
for yy in [104,344]:
 hh=min(240,H-yy);base.alpha_composite(side.crop((0,0,24,hh)),(0,yy));base.alpha_composite(side.transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,0,24,hh)),(W-24,yy))
for x,w in [(0,288),(416,288)]:
 a=front.resize((w,38),Image.Resampling.LANCZOS);base.alpha_composite(a.crop((0,22,w,38)),(x,H-16));over.alpha_composite(a.crop((0,0,w,22)),(x,H-38))
for xx in [264,404]:
 base.alpha_composite(pillar.crop((0,42,36,62)),(xx,H-20));over.alpha_composite(pillar.crop((0,0,36,42)),(xx,H-62))
def put(name,x,y,cut=16):
 im=props[name];w,h=im.size;z=max(0,h-cut)
 sh=Image.new('RGBA',(w+12,18));sd=ImageDraw.Draw(sh);sd.ellipse((2,4,w+10,16),fill=(80,61,27,45));floor.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)),(x-6,y+h-12))
 base.alpha_composite(im.crop((0,z,w,h)),(x,y+z));over.alpha_composite(im.crop((0,0,w,z)),(x,y));placed.append({'asset':name,'x':x,'y':y,'width':w,'height':h})
# A pair of useful wall-backed workstations, close chairs, one open approach on each side.
for x in [80,208]:put('desk',x,140);put('chair_n',x+18,184)
put('plant',40,144);put('smallplant',272,112)
# Meeting nook: the chairs belong to the table, with light floor between groups.
floor.alpha_composite(props['rug'],(424,136))
put('table',464,182)
for x in [470,522]:put('chair_s',x,145);put('chair_n',x,249)
put('plant',632,152);put('smallplant',632,258)
# Welcoming reception is beside the arrival route, not across it.
put('reception',88,362,24);put('chair_s',148,328)
put('plant',44,356);put('smallplant',240,384)
# A compact waiting chair ties reception to the entry, without entering the central lane.
put('chair_s',84,464);put('smallplant',44,468)
# Cream carpet/sofas: open from the central lane, with conversational spacing.
floor.alpha_composite(props['rug'],(448,354));put('couch_s',480,332,24);put('couch_w',592,402,24);put('couch_n',480,480,24);put('coffee',505,413,20)
put('plant',648,466);put('smallplant',416,472)
# Original32px Greg references at entry and a real workstation approach. No new Woka art.
avatar=Image.open(P/'qa/greg.png').convert('RGBA');av=Image.new('RGBA',(W,H));av.alpha_composite(avatar.crop((32,0,64,32)),(352-16,550-16));av.alpha_composite(avatar.crop((32,32,64,64)),(288-16,174-16))
room=floor.copy();room.alpha_composite(base);room.alpha_composite(av);room.alpha_composite(over)
canvas=Image.new('RGBA',(768,664),(239,236,224,255));shadow=Image.new('RGBA',canvas.size);ImageDraw.Draw(shadow).rounded_rectangle((28,26,742,614),12,fill=(75,60,26,46));canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)));canvas.alpha_composite(room,(32,24))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);dd=ImageDraw.Draw(canvas);dd.text((32,625),'Interior proposal  ·  light sandstone + teal  ·  original 32px avatar references',font=font,fill=(63,88,77))
canvas.save(R/'evidence/StudentHub-light-interior-proposal.png');room.save(R/'evidence/room-native.png')
json.dump({'status':'Visual proposal only; owner approval required before production changes','worldDimensions':[704,576],'mainArrivalLane':{'x':304,'y':112,'width':96,'height':464},'placements':placed,'avatarReferences':[{'x':352,'y':550,'size':32},{'x':288,'y':174,'size':32}],'productionCollisionAndRoutes':'Not propagated or accepted; review composition first'},open(R/'evidence/composition.json','w'),indent=2)
print('Saved single light-room proposal; no campus changes.')
