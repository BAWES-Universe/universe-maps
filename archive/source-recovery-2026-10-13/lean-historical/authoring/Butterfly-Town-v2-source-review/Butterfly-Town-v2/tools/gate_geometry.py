"""Gate revision: exact world registration, immutable painted atlas, code-native masks."""
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import math,json
GATE_ORIGIN=(0,128)
FX_ORIGIN=(576,640)
FX_SIZE=(928,1184)
# Coordinates are WORLD pixels, visually registered to the shipped2048px painting.
CASCADES=[
 {'id':'west-high','bounds':[700,700,52,150],'flow':[(715,713),(735,711),(736,819),(731,835),(711,835),(709,817)],'basin':[724,837,24,11]},
 {'id':'east-high','bounds':[1296,700,52,150],'flow':[(1309,713),(1331,715),(1332,824),(1325,835),(1307,835),(1305,819)],'basin':[1320,837,24,11]},
 {'id':'west-upper','bounds':[596,1056,72,142],'flow':[(604,1080),(624,1085),(649,1079),(648,1169),(642,1184),(610,1184),(602,1171)],'basin':[628,1183,32,12]},
 {'id':'east-upper','bounds':[1388,1056,70,142],'flow':[(1398,1080),(1419,1086),(1444,1080),(1445,1172),(1437,1185),(1406,1185),(1398,1170)],'basin':[1422,1184,32,12]},
 {'id':'west-middle','bounds':[600,1266,74,144],'flow':[(619,1294),(650,1285),(653,1398),(619,1403)],'basin':[636,1400,26,8]},
 {'id':'east-middle','bounds':[1382,1266,70,144],'flow':[(1393,1289),(1428,1296),(1431,1400),(1393,1403)],'basin':[1412,1400,26,8]},
 {'id':'west-lower','bounds':[620,1584,68,216],'flow':[(638,1610),(665,1603),(671,1640),(671,1738),(659,1766),(635,1752),(634,1640)],'basin':[653,1765,33,18]},
 {'id':'east-lower','bounds':[1358,1584,62,216],'flow':[(1376,1609),(1407,1604),(1409,1645),(1406,1751),(1384,1768),(1373,1747)],'basin':[1390,1765,31,18]},
]
# Filled from independent paving/rim trace. Each knot: worldy,left,right.
PAVING_PROFILE=[(864, 936, 1112), (896, 924, 1124), (928, 916, 1132), (960, 896, 1152), (992, 888, 1160), (1024, 888, 1160), (1056, 896, 1152), (1088, 884, 1164), (1120, 876, 1172), (1152, 872, 1176), (1184, 880, 1168), (1216, 892, 1156), (1248, 892, 1156), (1280, 864, 1184), (1312, 848, 1200), (1344, 848, 1200), (1376, 836, 1212), (1408, 828, 1220), (1440, 816, 1232), (1472, 816, 1232), (1504, 808, 1240), (1536, 808, 1240), (1568, 828, 1220), (1600, 844, 1204), (1632, 844, 1204), (1664, 856, 1192), (1696, 872, 1176), (1728, 864, 1184), (1760, 844, 1204), (1792, 816, 1232), (1824, 808, 1240), (1856, 800, 1248), (1888, 800, 1248), (1920, 784, 1264), (1952, 784, 1264), (1984, 776, 1272), (2016, 768, 1280), (2048, 784, 1264), (2080, 784, 1264), (2112, 768, 1280), (2144, 760, 1288), (2176, 752, 1296)]

def bounds_at(y):
 for (y0,l0,r0),(y1,l1,r1) in zip(PAVING_PROFILE,PAVING_PROFILE[1:]):
  if y0<=y<=y1:
   t=(y-y0)/(y1-y0);return l0+(l1-l0)*t,r0+(r1-r0)*t
 return (944,1104) if y<PAVING_PROFILE[0][0] else (752,1296)

def environment_masks(source):
 """Move only real cool foliage pixels near the traced raised border to foreground.
 The same pixels are removed from ground, so there is no duplicate baked plant.
 No source scaling/sharpening or floor-coloured opaque rectangular crop is used.
 """
 W,H=source.size;mask=Image.new('L',(W,H));mp=mask.load();sp=source.load()
 for y in range(736,H):
  wy=y+128;l,r=bounds_at(wy)
  for a,b in [(int(l-100),int(l+28)),(int(r-28),int(r+100))]:
   for x in range(max(0,a),min(W,b)):
    red,green,blue,alpha=sp[x,y]
    leaf=(blue>red*1.48 and green>red*1.18 and blue>38) or (green>red*1.48 and blue>red*.88 and green>35)
    if leaf:mp[x,y]=255
 # One-pixel fringe follows fine leaves/flowers; bounded bands never reach cascades.
 mask=mask.filter(ImageFilter.MaxFilter(3))
 # Exclude actual cascade/basin surface even if a future path profile approaches it.
 md=ImageDraw.Draw(mask)
 for fall in CASCADES:
  x,y,w,h=fall['bounds'];md.rectangle((x-4,y-128-4,x+w+4,y+h-128+4),fill=0)
 foreground=Image.new('RGBA',source.size);foreground.paste(source,(0,0),mask)
 ground=source.copy();ground.paste((0,0,0,0),(0,0,W,H),mask)
 # Smooth rectangle-edge atmosphere, with no repeated motif in the world beyond it.
 fogAlpha=Image.new('L',source.size);fd=ImageDraw.Draw(fogAlpha)
 for inset in range(160):
  t=inset/160;opacity=round(255*(1-t)*(1-t));fd.rectangle((inset,inset,W-1-inset,H-1-inset),outline=opacity)
 fog=Image.new('RGBA',source.size,(9,18,34,0));fog.putalpha(fogAlpha)
 foreground.putalpha(ImageChops.multiply(foreground.getchannel('A'),ImageChops.invert(fogAlpha)))
 return ground,foreground,fog,mask

def cascade_frames(source,n=12):
 """Downward phase travel inside exact polygons; small bounded basin mist."""
 ox,oy=FX_ORIGIN;W,H=FX_SIZE;flowmask=Image.new('L',(W,H));basinmask=Image.new('L',(W,H));fd=ImageDraw.Draw(flowmask);bd=ImageDraw.Draw(basinmask)
 for c in CASCADES:
  fd.polygon([(x-ox,y-oy) for x,y in c['flow']],fill=255)
  x,y,rx,ry=c['basin'];bd.ellipse((x-rx-ox,y-ry-oy,x+rx-ox,y+ry-oy),fill=255)
 # Mist stays on visibly blue basin/splash pixels, never adjacent gold rails/plants.
 bp=basinmask.load();sp=source.load()
 for y in range(H):
  for x in range(W):
   if bp[x,y]:
    r,g,b,a=sp[x+ox,y+oy-128]
    if not (b>r*1.14 and b>g*1.04 and b>70):bp[x,y]=0
 flowpixels=[(x,y) for y in range(H) for x in range(W) if flowmask.getpixel((x,y))]
 mistpixels=[(x,y) for y in range(H) for x in range(W) if basinmask.getpixel((x,y))]
 flows=[];mists=[]
 for f in range(n):
  flow=Image.new('RGBA',(W,H));mist=Image.new('RGBA',(W,H));fp=flow.load();mp=mist.load()
  for x,y in flowpixels:
   # phase(y-4f) is explicitly downward;12frames wrap a48px wavelength exactly.
   streak=.45+.55*math.sin(x*.77)**2;wave=max(0,math.sin((y-4*f)*math.pi/24))**5
   thin=max(0,math.sin((y-4*f+11)*math.pi/24))**16
   a=round((22+58*wave+30*thin)*streak);fp[x,y]=(132,232,255,a)
  for x,y in mistpixels:
   p=(math.sin(x*.19+y*.22-f*math.pi/6)+1)/2;a=round(5+16*p);mp[x,y]=(170,227,250,a)
  flows.append(flow);mists.append(mist)
 return flows,mists,flowmask,basinmask

def world_fade(image,origin,map_size=(4608,3072),width=192):
 """Fade map-edge pixels to transparency, respecting the room's actual backdrop."""
 w,h=image.size;ox,oy=origin;mw,mh=map_size
 def value(d):
  t=max(0,min(1,d/width));return round(255*t*t*(3-2*t))
 ax=Image.new('L',(w,1));ax.putdata([value(min(ox+x,mw-1-ox-x)) for x in range(w)])
 ay=Image.new('L',(1,h));ay.putdata([value(min(oy+y,mh-1-oy-y)) for y in range(h)])
 alpha=ImageChops.darker(ax.resize((w,h),Image.Resampling.NEAREST),ay.resize((w,h),Image.Resampling.NEAREST))
 result=image.copy();result.putalpha(ImageChops.multiply(image.getchannel('A'),alpha));return result

def midnight_field(tile_width,tile_height):
 """Uniform interior plus unique edge-alpha tiles; no recurring texture motifs."""
 indices=[];variants={};tiles=[];border=6
 for ty in range(tile_height):
  for tx in range(tile_width):
   kx=tx if tx<border else tile_width-1-tx+border if tx>=tile_width-border else 2*border
   ky=ty if ty<border else tile_height-1-ty+border if ty>=tile_height-border else 2*border
   key=(kx,ky)
   if key not in variants:
    variants[key]=len(tiles);tile=Image.new('RGBA',(32,32),(9,18,34,255));tiles.append(world_fade(tile,(tx*32,ty*32),(tile_width*32,tile_height*32)))
   indices.append(variants[key])
 columns=16;atlas=Image.new('RGBA',(columns*32,math.ceil(len(tiles)/columns)*32))
 for i,tile in enumerate(tiles):atlas.paste(tile,((i%columns)*32,(i//columns)*32))
 return atlas,indices
