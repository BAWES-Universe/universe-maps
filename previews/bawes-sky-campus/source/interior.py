"""Approved-family interior. Executed by build.py; native world pixels, separate foregrounds."""
from PIL import ImageOps
candidate=Image.open(R/'source/interior-candidates/objects.png').convert('RGBA')
extractions={
 'reception':((32,24,454,408),256), 'desk-paper':((500,75,804,242),112),
 'desk-laptop':((834,75,1132,242),112), 'project':((488,260,818,451),160),
 'meeting':((858,264,1138,431),144), 'sofa':((56,450,423,625),128),
 'side':((452,480,580,620),48), 'plant':((618,450,792,636),48),
 'planter':((802,454,1240,636),224),
 'chair-down':((72,638,216,790),None), 'chair-up':((264,636,408,790),None),
 'chair-right':((450,636,590,790),None), 'chair-left':((620,636,752,790),None)}
asset_audit=[]
for name,(box,width) in extractions.items():
 im=candidate.crop(box);bb=im.getchannel('A').point(lambda a:255 if a>=180 else 0).getbbox();im=im.crop(bb)
 # Eliminate only near-transparent residue, preserving source edge alpha.
 aa=im.getchannel('A').point(lambda a:0 if a<12 else a);im.putalpha(aa)
 scale=(width/im.width) if width else 40/im.height
 size=(round(im.width*scale),round(im.height*scale));small=im.resize(size,Image.Resampling.LANCZOS)
 if name.startswith('chair'):
  out=Image.new('RGBA',(48,64));out.alpha_composite(small,((48-small.width)//2,16 if name=='chair-down' else 8))
 else:
  out=Image.new('RGBA',(math.ceil(size[0]/16)*16,math.ceil(size[1]/16)*16));out.alpha_composite(small)
 sprites['in-'+name]=out;out.save(A/('in-'+name+'.png'))
 asset_audit.append(dict(name=name,sourceBox=box,alphaBounds=bb,trimmedSource=list(im.size),uniformScale=scale,rasterSize=size,paddedSize=list(out.size)))
(R/'review/interior-asset-calibration.json').write_text(json.dumps(asset_audit,indent=2)+'\n')
# Reconstruct continuous native-detail stone using only an unoccupied material region
# from the matching clean-floor candidate. Measured inlays replace unregistered ones.
clean=Image.open(R/'source/interior-candidates/clean-floor.png').convert('RGBA')
stone=clean.crop((640,192,880,432));tile=Image.new('RGBA',(480,480));tile.alpha_composite(stone)
tile.alpha_composite(ImageOps.mirror(stone),(240,0));tile.alpha_composite(ImageOps.flip(stone),(0,240));tile.alpha_composite(ImageOps.flip(ImageOps.mirror(stone)),(240,240))
floor=Image.new('RGBA',(OW,OH))
for yy in range(0,OH,480):
 for xx in range(0,OW,480):floor.alpha_composite(tile,(xx,yy))
fd=ImageDraw.Draw(floor)
# Restrained same-family stone inlay, aligned to project setting and arrival spine.
for inset in (0,7):fd.ellipse((208+inset,64+inset,480-inset,336-inset),outline='#efdab7',width=2)
for xx in (976,1168):fd.line((xx,80,xx,OH-16),fill='#efdab7',width=3)
cutaway_ground=floor
walls=Image.new('RGBA',(OW,OH));wallD=ImageDraw.Draw(walls)
glazing=Image.new('RGBA',(OW,OH));gd=ImageDraw.Draw(glazing)
office_fronts=Image.new('RGBA',(OW,OH))
exec((R/'source/architecture.py').read_text())
# Only two individual desks; no rows or borrowed carpet blocks.
for name,x in [('desk-paper',80),('desk-laptop',512)]:
 item('in-'+name,OX+x,OY+112,(OX+x,OY+128,112,48));chair(OX+x+56,OY+208,'up','focus')
item('in-project',OX+256,OY+208,(OX+256,OY+224,160,64))
for dx in (40,120):chair(OX+256+dx,OY+176,'down','project');chair(OX+256+dx,OY+320,'up','project')
# Matched outward-facing sofas; front clear route is 96px inside the perimeter wall.
for xx in (96,448):
 item('in-sofa',OX+xx,OY+416,(OX+xx,OY+416,128,16))
 for dx in (40,88):seats.append(dict(x=OX+xx+dx,y=OY+448,group='outward-lounge',facing='down'))
 item('in-side',OX+xx+144,OY+416,(OX+xx+144,OY+432,48,32))
# Curved reception remains left of the unobstructed arrival spine.
item('in-reception',OX+704,OY+64)
rectwalk((OX+704,OY+64,64,176),0);rectwalk((OX+704,OY+224,256,80),0)
chair(OX+848,OY+192,'down','reception')
item('in-planter',OX+960,OY+32,(OX+960,OY+96,224,32))
for px in (80,448,1456,1856):
 item('in-planter',OX+px,OY+16,(OX+px,OY+64,224,32))
# Two complete rooms, with 96px front doors and 96px between-room circulation.
for i,xx in enumerate((1392,1792)):
 yy=64;ww=304;hh=400
 stone_wall(xx,yy,ww,48)
 for px in (xx,xx+ww-40):architecture_post(px,yy-16)
 for px in (xx,xx+ww-40):architecture_post(px,yy+hh-83)
 glass_run(xx,yy+48,16,hh-48);glass_run(xx+ww-16,yy+48,16,hh-48)
 for dx,width in [(0,96),(192,ww-192)]:glass_run(xx+dx,yy+hh-16,width,16)
 # Front rail rises above the floor in its own transparent foreground plane.
 for dx,width in [(0,96),(192,ww-192)]:glass_run(xx+dx,yy+hh-48,width,32,False)
 door=dict(id=f'meeting-{i+1}',box=[OX+xx+96,OY+yy+hh-16,96,16],inside=[OX+xx+16,OY+yy+48,ww-32,hh-64],lock=f'meetingLock{i+1}')
 doors.append(door);rooms.append(dict(id=door['id'],box=door['inside']))
 item('in-meeting',OX+xx+80,OY+yy+160,(OX+xx+80,OY+yy+176,144,64))
 for dx in (112,192):chair(OX+xx+dx,OY+yy+128,'down','meeting');chair(OX+xx+dx,OY+yy+256,'up','meeting')
 item('in-plant',OX+xx+32,OY+yy+48,(OX+xx+32,OY+yy+96,48,16))
 for px in (xx+16,xx+ww-64):item('in-plant',OX+px,OY+368,(OX+px,OY+416,48,16))
for im,px,py in architecture_posts:glazing.alpha_composite(im,(px,py))
for xx,yy in [(32,224),(32,400),(656,368)]:item('in-plant',OX+xx,OY+yy,(OX+xx,OY+yy+48,48,16))
doors.append(dict(id='office-front',box=[OX+976,OY+OH-16,192,16],inside=[OX+16,OY+48,OW-32,OH-64]))
# Extract matching foreground strips from the same sprites, not alternate art.
for name,x,y in placements:
 im=sprites[name];mask=Image.new('L',im.size);md=ImageDraw.Draw(mask)
 if name.startswith('in-chair-'):
  top=40 if name=='in-chair-up' else 45
  md.rectangle((0,top,im.width-1,55 if name=='in-chair-down' else 47),fill=255)
 elif name=='in-sofa':md.rectangle((0,44,im.width-1,im.height-1),fill=255)
 elif name=='in-reception':md.rectangle((0,178,im.width-1,im.height-1),fill=255)
 else:continue
 piece=im.copy();piece.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel('A')),np.asarray(mask))))
 office_fronts.alpha_composite(piece,(x-OX,y-OY))
for obj in objects:
 assert OX+16<=obj['x'] and OY<=obj['y'] and obj['x']+obj['width']<=OX+OW-16 and obj['y']+obj['height']<=OY+OH-16,obj
