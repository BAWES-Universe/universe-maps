"""Native registration for the separately authored illustrated brand-reset study."""
from PIL import Image, ImageDraw

def apply(root,floor,backs,blocked,seats,tables):
 source=Image.open(root/'source/brand_reset/section-original.png').convert('RGBA').resize((768,576),Image.Resampling.LANCZOS)
 sx=[0,32,118,156,196,288,324,472,569,607,644,736,768]
 dx=[0,32,112,144,176,288,320,480,560,592,624,736,768]
 sy=[0,89,119,174,201,214,228,251,268,296,328,576]
 dy=[0,96,128,178,224,232,240,268,288,320,352,576]
 mesh=[((dx[i],dy[j],dx[i+1],dy[j+1]),(sx[i],sy[j],sx[i],sy[j+1],sx[i+1],sy[j+1],sx[i+1],sy[j])) for j in range(len(sy)-1) for i in range(len(sx)-1)]
 patch=source.transform((768,576),Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)
 empty=Image.open(root/'source/brand_reset/empty-material-original.png').convert('RGBA').resize((768,576),Image.Resampling.LANCZOS)
 # Tile-map assembly reuses the registered painted material/furniture kit.
 # No new geometry: finish the adjoining tower rooms and arrival court as one district.
 def tile(crop,box):
  im=patch.crop(crop);x,y,w,h=box
  for yy in range(y,y+h,im.height):
   for xx in range(x,x+w,im.width):
    floor.alpha_composite(im.crop((0,0,min(im.width,x+w-xx),min(im.height,y+h-yy))),(xx,yy))
 def put(crop,xy,size=None,target=floor,atlas=patch):
  im=atlas.crop(crop)
  # Native sprite silhouettes avoid copying a rectangular piece of rug under each item.
  if crop==(94,238,130,290):
   mask=Image.new('L',im.size);md=ImageDraw.Draw(mask)
   md.polygon([(13,1),(24,1),(31,7),(35,18),(32,35),(27,42),(26,49),(12,51),(7,46),(9,39),(3,28),(2,12),(6,5)],fill=255)
   im.putalpha(mask)
  if crop==(90,164,228,238):
   mask=Image.new('L',im.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,137,72),12,fill=255);im.putalpha(mask)
  if size:im=im.resize(size,Image.Resampling.LANCZOS)
  target.alpha_composite(im,xy)
 # Finish up to the surrounding street junctions, not a rectangle through a room.
 tile((224,352,256,416),(128,992,1184,1056))
 backs.paste((0,0,0,0),(128,992,1312,2048))
 tile((352,192,448,288),(320,1024,768,608))
 # Structural glass and ink wall faces stay on the original collision footprint.
 for x in (320,1056):
  tile((0,128,32,320),(x,1024,32,256))
 for x in (320,800):tile((32,96,288,128),(x,1024,288,32))
 # Two existing upper work/meeting clusters, using the same rug, table and seat family.
 for x in (384,800):
  put((64,144,256,320),(x,1088),(192,192),atlas=empty)
  put((90,164,228,238),(x+32,1104),(128,80))
  for i in range(4):
   cx=x+48+i*32
   put((94,238,130,290),(cx-18,1198))
   put((98,274,126,286),(cx-14,1234),target=backs)
 # Wall display/storage at the same blocked cells, now a cool glass panel.
 for x in (416,832):put((32,96,128,128),(x,1056))
 # Restore the original reviewed lounge, meeting room and open entry unchanged.
 floor.alpha_composite(patch,(320,1280))
 # Arrival terraces: replace wood and mixed chairs with this same compact kit.
 for tx in (12,28):
  x=tx*32
  put((64,144,256,320),(x-24,1832),(192,184),atlas=empty)
  put((90,164,228,238),(x,1840),(96,64))
  for i in range(3):
   cx=x+i*32+16
   put((94,238,130,290),(cx-18,1902))
   put((98,274,126,286),(cx-14,1938),target=backs)
 # Same illustrated planting family on existing side-bed footprints only.
 for x in (160,1152):
  for y in range(1120,1504,96):put((16,448,112,544),(x,y))
 for x in (256,1056):put((32,448,96,544),(x,1888))
 # End at the existing street junction without a false wall across the routes.

 # Only the low front lip overlaps the avatar's feet, not its torso.
 for x in [112,144,176,560,592,624]:backs.alpha_composite(patch.crop((x-14,274,x+14,286)),(320+x-14,1554))
 backs.alpha_composite(patch.crop((64,50,128,56)),(384,1330))
 blocked.difference_update((x,41) for x in range(28,32));blocked.update((x,46) for x in [16,30,31])
 for t in tables:
  if t[:2]==[13,46]:t[2]=4
  if t[:2]==[27,46]:t[2]=5
 patch.save(root/'review/brand-section-native.png')

 # Bounded image-tool finishing pass repairs paving/planting joins without a new layout.
 finish=Image.open(root/'source/brand_reset/consistency-finish-original.png').convert('RGBA').resize((1184,1056),Image.Resampling.LANCZOS)
 floor.alpha_composite(finish,(128,992))
