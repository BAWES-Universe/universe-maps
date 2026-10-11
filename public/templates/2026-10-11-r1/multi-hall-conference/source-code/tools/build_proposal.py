from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import json,hashlib,random,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';A=R/'assets';Q=R/'review';G=S/'generated'
F=str(A/'fonts/DejaVuSans.ttf');FB=str(A/'fonts/DejaVuSans-Bold.ttf')
font=lambda n,b=False:ImageFont.truetype(FB if b else F,n)
manifest=[]
def cut(fn,region,name,width):
 im=Image.open(G/fn).convert('RGBA').crop(region);box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();box=(max(0,box[0]-3),max(0,box[1]-3),min(im.width,box[2]+3),min(im.height,box[3]+3));im=im.crop(box);sz=(width,round(im.height*width/im.width));im=im.resize(sz,Image.Resampling.LANCZOS);im.save(A/name);manifest.append({'asset':name,'source':fn,'region':region,'opaqueCropLocal':box,'size':sz,'uniformScale':width/(box[2]-box[0]),'sha256':hashlib.sha256((A/name).read_bytes()).hexdigest()});return im
chairs={}
for direction,region in [('north',(0,0,768,512)),('south',(768,0,1536,512)),('east',(0,512,768,1024)),('west',(768,512,1536,1024))]:chairs[direction]=cut('chair-kit-master.png',region,f'congress-chair-{direction}.png',48)
wall=cut('architecture-kit-master.png',(0,0,1536,450),'congress-wall-horizontal.png',384)
counter=cut('architecture-kit-master.png',(0,450,730,1024),'congress-reception.png',192)
table=cut('architecture-kit-master.png',(730,450,1140,1024),'congress-low-table.png',80)
tree=cut('architecture-kit-master.png',(1140,450,1536,1024),'congress-olive-planter.png',64)
floor=Image.open(G/'terrazzo-master.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);floor.save(A/'terrazzo-native-256.png')
# A source-authored simple felt rug with an unobtrusive stitched perimeter, not ornamental palace art.
rng=random.Random(82);rug=Image.new('RGBA',(384,288),(58,84,70,255));rd=ImageDraw.Draw(rug)
for y in range(288):
 for x in range(384):
  n=rng.choice([-3,-2,-1,0,0,0,1,2,3]);rug.putpixel((x,y),(58+n,84+n,70+n,255))
rd.rectangle((7,7,376,280),outline='#afad90',width=2);rd.rectangle((13,13,370,274),outline='#728772',width=1);rug.save(A/'congress-felt-rug.png')
# Native proof slice: deliberately generous staffed and guest approaches.
W,H=1152,640;base=Image.new('RGBA',(W,H));above=Image.new('RGBA',(W,H))
for y in range(0,H,256):
 for x in range(0,W,256):base.alpha_composite(floor,(x,y))
for x in range(0,W,384):base.alpha_composite(wall,(x,0))
d=ImageDraw.Draw(base);d.rectangle((0,76,W,82),fill='#554633')
def sign(text,box,size=13):
 x,y,w,h=box;d.rounded_rectangle((x,y,x+w,y+h),radius=3,fill='#234938',outline='#b8a486',width=2);bb=d.textbbox((0,0),text,font=font(size,True));d.text((x+(w-bb[2])/2,y+(h-bb[3])/2-2),text,font=font(size,True),fill='#f5ecd5')
sign('REGISTRATION',(116,98,152,26));sign('NETWORKING LOUNGE',(632,98,224,26));sign('SUMMIT  /  FORUM  /  LAB   →',(384,510,384,32),15)
base.alpha_composite(counter,(96,184));base.alpha_composite(tree,(352,164));base.alpha_composite(tree,(992,170));base.alpha_composite(rug,(576,160));base.alpha_composite(table,(728,282))
placements=[('south',744,178, (768,215)),('east',608,266,(638,294)),('west',880,266,(898,294)),('north',744,376,(768,395))]
actors=[]
for dr,x,y,anchor in placements:
 im=chairs[dr];cutY=29 if dr=='north' else (46 if dr=='south' else im.height-7)
 base.alpha_composite(im.crop((0,0,im.width,cutY)),(x,y));above.alpha_composite(im.crop((0,cutY,im.width,im.height)),(x,y+cutY));actors.append((anchor,dr))
# A close casual pair and genuinely adjacent table, away from the broad central lane.
for x in [144,200]:
 im=chairs['north'];base.alpha_composite(im.crop((0,0,48,29)),(x,436));above.alpha_composite(im.crop((0,29,48,im.height)),(x,465));actors.append(((x+24,455),'north'))
base.alpha_composite(table,(284,428))
actors += [((192,166),'south'),((192,352),'north'),((472,384),'east'),((896,528),'west')]
greg=Image.open(A/'greg-reference.png').convert('RGBA');frames={'north':10,'south':1,'east':7,'west':4}
occupied=base.copy()
for (x,y),dr in actors:
 i=frames[dr];occupied.alpha_composite(greg.crop(((i%3)*32,(i//3)*32,(i%3+1)*32,(i//3+1)*32)),(x-16,y-16))
occupied.alpha_composite(above);base.save(Q/'bounded-base-native.png');above.save(Q/'bounded-above-native.png');occupied.save(Q/'bounded-occupied-native32.png')
board=Image.new('RGB',(1184,730),'#172d27');bd=ImageDraw.Draw(board);bd.text((16,12),'LANTERN CONGRESS / NATIVE 1:1 MATERIAL & OCCUPIED SAMPLE',font=font(19,True),fill='#e6d5b4');bd.text((16,42),'New oak, forest-green fabric and terrazzo. 32 px Greg fixture; source composition only.',font=font(14),fill='#c7d4c8');board.paste(occupied,(16,70));board.save(Q/'REVIEW-FIRST-native32.png')
# Full composition is a labelled diagram, not a rendered runtime screenshot.
w,h=3072,2048;scale=.375;plan=Image.new('RGB',(int(w*scale)+64,int(h*scale)+176),'#172d27');p=ImageDraw.Draw(plan);ox,oy=32,96
xy=lambda box:tuple(round(v*scale)+(ox if i%2==0 else oy) for i,v in enumerate(box))
def rect(b,c,outline=None,width=2):p.rectangle(xy(b),fill=c,outline=outline,width=width)
def label(t,x,y,n=15,c='#f3ead6'):p.text((ox+x*scale,oy+y*scale),t,font=font(n,True),fill=c)
rect((64,64,2944,1984),'#d8d4c4');rect((1312,96,1568,1952),'#eee9d9');rect((96,960,2912,1120),'#eee9d9')
rooms=[('SUMMIT / PLENARY',(128,128,1280,960),'#476c58'),('FORUM / PANELS',(1600,128,2752,832),'#746f55'),('LAB / WORKSHOPS',(1600,1152,2752,1888),'#4c6968'),('NETWORKING CONCOURSE',(128,1152,1280,1888),'#b7b69e')]
for name,box,c in rooms:rect(box,c,'#283f34',3);label(name,box[0]+24,box[1]+20,15)
# Stage/podium footprints and meaningful door gaps.
rect((256,224,1152,384),'#ac8752');label('48 seats · three banks',304,416,14)
for row in range(4):
 for bank in range(3):
  for col in range(4):
   x=280+bank*304+col*64;y=512+row*96;rect((x,y,x+40,y+40),'#d4bc8b')
rect((608,928,800,984),'#eee9d9');rect((1264,608,1328,800),'#eee9d9')
rect((1888,224,2464,352),'#ab8e69');label('24 seats · open horseshoe',1750,382,13)
for row in range(3):
 for col in range(4):
  x=1952+col*128;y=480+row*96;rect((x,y,x+40,y+40),'#d4bc8b')
for side in [1728,2592]:
 for row in range(6):
  y=416+row*56;rect((side,y,side+40,y+40),'#d4bc8b')
rect((1584,576,1640,736),'#eee9d9');rect((2112,816,2304,848),'#eee9d9')
rect((1792,1232,2560,1328),'#a08454');label('24 seats · six table pods',1792,1360,13)
for y in [1472,1712]:
 for x in [1824,2144,2464]:
  rect((x-48,y-24,x+48,y+24),'#bdac7b')
  for dx,dy in [(0,-80),(0,80),(-96,0),(96,0)]:rect((x+dx-18,y+dy-18,x+dx+18,y+dy+18),'#e0d6b3')
rect((1584,1440,1640,1632),'#eee9d9')
rect((1264,1632,1328,1824),'#eee9d9');rect((608,1136,800,1176),'#eee9d9')
# Two group squares and three casual pairs avoid the main right-side spine.
for bx in [192,704]:
 rect((bx,1280,bx+384,1568),'#41634d');label('GROUP',bx+116,1390,11)
for x in [272,616,1008]:
 for dx in [-28,28]:rect((x+dx-18,1712,x+dx+18,1752),'#41634d')
rect((192,1808,448,1872),'#84633f');label('COFFEE',225,1830,11);rect((800,1808,1088,1872),'#84633f');label('CHECK-IN',835,1830,11)
rect((1376,1888,1504,2016),'#416968');label('ARRIVAL',1325,1950,11)
label('256 px circulation spine',1300,912,12,c='#224534')
p.text((32,18),'LANTERN CONGRESS / THREE INDEPENDENT TALK ROOMS',font=font(22,True),fill='#e6d5b4');p.text((32,50),'3072 × 2048 px · native32 · warm contemporary conference centre · proposed plan',font=font(15),fill='#c7d4c8');p.text((32,880),'96 hall seats + 8 group seats + 6 casual seats. Seat count is not a concurrency claim.',font=font(14),fill='#c7d4c8');p.text((32,904),'Doors and furniture are schematic here; geometry and native role tests follow after composition review.',font=font(14),fill='#c7d4c8');plan.save(Q/'composition-proposal.png')
(S/'asset-registration.json').write_text(json.dumps({'status':'native sample only; build geometry not frozen','assets':manifest,'floor':'Generated1024-square texture uniformly reduced to256-square; no directional lighting baked in','greg':'Project-authored Greg Gulf-outfit v3, unchanged reference only'},indent=2)+'\n')
