"""Source-owned Yoga Retreat variant. Original environmental raster is never modified.
All additions are deterministic authored canvas sprites rendered at native scale.
"""
from pathlib import Path
import json,hashlib,random
from PIL import Image,ImageDraw,ImageFilter
import build_templates as b
from build_environments import foreground_polygon
b.C,b.N,b.W,b.H=48,32,1536,1024
R=b.R
m=b.Map('timber-yoga-retreat-r1','Timber & Stone Yoga Retreat','Wellness',b.P)
original=b.A['cowork-environment-final'].copy();m.base=original.copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
for rr in [(5,5,38,9),(4,6,41,8),(21,5,6,22),(19,18,11,5),(6,18,11,6),(31,18,12,6),(17,19,4,3),(27,19,5,3),(22,24,4,8)]:m.block(*rr,0)
m.block(18,12,3,6);m.block(27,12,3,6) # visible central stone piers are solid
m.block(18,0,3,7);m.block(27,0,3,7) # north column bases
m.block(4,6,2,4);m.block(42,6,3,4);m.block(4,12,2,2);m.block(42,12,3,2) # plant footprints
m.block(21,23,1,6);m.block(26,23,1,6);m.block(16,21,2,4);m.block(30,21,2,4) # entry shoulders
m.block(6,18,2,5);m.block(41,18,2,5);m.block(6,23,12,1);m.block(30,23,13,1) # complete lower window/plant perimeter
m.block(4,5,3,9);m.block(42,5,3,9);m.block(7,5,1,2);m.block(40,5,2,2) # complete upper side ledges and corner plants
changes=[]
def paste(im,x,y,kind):
 m.base.alpha_composite(im,(x,y));changes.append(dict(kind=kind,rect=[x,y,im.width,im.height]))
def shade(c,n):return tuple(max(0,min(255,i+n)) for i in c)
def mat(x,y,name,c=(105,121,94),instructor=False):
 # Soft bevel, woven texture, double stitched edge; 1.4 by 2.3 native tiles.
 w,h=(62,46) if instructor else (44,74);im=Image.new('RGBA',(w+8,h+8));d=ImageDraw.Draw(im)
 d.rounded_rectangle((5,5,w+5,h+5),radius=5,fill=(49,32,22,70));d.rounded_rectangle((1,1,w,h),radius=4,fill=shade(c,-35));d.rounded_rectangle((2,1,w-1,h-3),radius=4,fill=c)
 for yy in range(4,h-5):
  d.line((4,yy,w-3,yy),fill=shade(c,5 if yy%3==0 else -3))
 d.rounded_rectangle((5,5,w-4,h-7),radius=2,outline=shade(c,27));d.line((3,2,w-3,2),fill=shade(c,40));d.line((3,h-3,w-2,h-3),fill=shade(c,-22))
 for xx in range(7,w-6,4):
  d.point((xx,7),fill=shade(c,-22));d.point((xx,h-9),fill=shade(c,-22))
 if not instructor:
  d.line((w//2,13,w//2,h-16),fill=shade(c,10));d.ellipse((w//2-3,10,w//2+3,16),outline=shade(c,30))
 px=x*32+16-w//2;py=y*32+16-h//2;paste(im,px,py,'instructor mat' if instructor else 'practice mat');m.anchor(name,x,y)
 return [px,py,w,h]
def cushion(x,y,name,c=(165,119,71)):
 im=Image.new('RGBA',(38,30));d=ImageDraw.Draw(im);d.ellipse((3,7,37,29),fill=(40,29,18,75));d.ellipse((1,5,34,26),fill=shade(c,-38));d.ellipse((1,2,34,23),fill=c);d.ellipse((4,4,31,20),outline=shade(c,22));d.arc((7,6,29,19),0,180,fill=shade(c,-19));d.ellipse((15,10,19,14),fill=shade(c,-25));paste(im,x*32-2,y*32+5,'meditation cushion');m.anchor(name,x,y)
def storage(x,y,w,h,kind):
 # Tight replacements inside existing book cubbies: retain original shelf framing.
 im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im);d.rectangle((0,0,w-1,h-1),fill='#4d3927');d.line((0,h-1,w-1,h-1),fill='#b48752')
 if kind=='rolled mats':
  colors=[(115,130,105),(168,136,101),(111,131,133)]
  for i,xx in enumerate(range(2,w-7,10)):
   c=colors[i%3];d.rounded_rectangle((xx,3,xx+8,h-3),radius=3,fill=c,outline=shade(c,-35));d.line((xx+2,6,xx+2,h-5),fill=shade(c,25));d.arc((xx+1,2,xx+7,8),10,340,fill=shade(c,-28))
 else:
  for yy in range(h-7,1,-6):
   d.rounded_rectangle((3,yy,w-4,yy+5),radius=2,fill='#b9aa8b',outline='#82725a');d.line((5,yy+1,w-7,yy+1),fill='#c8b99a');d.line((w-10,yy+2,w-10,yy+4),fill='#948367')
 paste(im,x,y,kind)
# Book cubby contents only. Timber, stone, plants, light sources and flooring stay exact.
for box in [(413,119,63,26),(288,122,31,23),(1051,122,29,23),(1316,106,28,36),(687,96,19,21),(1280,516,38,22)]:storage(*box,'rolled mats')
for box in [(220,111,48,35),(760,80,45,10),(942,128,22,16),(1118,524,27,11),(420,544,36,13),(216,512,43,25)]:storage(*box,'folded towels')
# Two aligned banks with 52px clear side-by-side spacing; all student rows face the front instructor.
for wing,xs in [('west',[8,11,14]),('east',[33,36,39])]:
 for row,y in enumerate([8,11],1):
  for col,x in enumerate(xs,1):mat(x,y,f'{wing} practice mat {row}-{col}',(109,125,99) if wing=='west' else (141,123,100))
mat(24,6,'instructor position',(162,139,92),True)
# Side alcoves welcome conversation before/after practice; never globally silent.
for wing,points in [('tea',[(8,19),(13,19),(11,21)]),('rest',[(33,19),(38,19),(36,21)])]:
 for i,(x,y) in enumerate(points):cushion(x,y,f'{wing} cushion {i+1}',(163,122,78) if wing=='tea' else (110,127,107))
# Original native tea tables reused at unchanged sprite scale.
m.smalltable(10,19);m.smalltable(35,19)
m.zone('Yoga instructor broadcast',22,5,4,3,'speaker')
m.zone('Aligned yoga students',6,8,36,6,'listener')
m.zone('Tea and arrival conversation',7,18,10,6)
m.zone('Rest and reflection gathering',31,18,11,6)
for name,x,y in [('west practice entry',19,10),('east practice entry',29,10),('prop storage approach',24,5),('central medallion',24,11),('central social hall',24,20),('tea alcove approach',17,20),('rest alcove approach',31,20),('arrival',24,29)]:m.anchor(name,x,y)
foreground_polygon(m,[(96,448),(579,448),(579,487),(96,487)])
foreground_polygon(m,[(965,448),(1442,448),(1442,487),(965,487)])
m.cropboxes=[('practice-west',(160,176,608,448)),('practice-east',(928,176,1376,448)),('instructor',(640,176,896,448)),('gathering',(192,544,1376,768))]
m.finish()
out=R/m.slug
# Exact preservation test outside explicit additive sprite rectangles.
import numpy as np
mask=np.zeros((1024,1536),bool)
for c in changes:
 x,y,w,h=c['rect'];mask[y:y+h,x:x+w]=True
for x,y in [(10*32,19*32),(35*32,19*32)]:
 w,h=b.A['low-lounge-table'].size;mask[y:y+h,x:x+w]=True
changed=np.any(np.array(original)!=np.array(m.base),axis=2)
assert not np.any(changed&~mask)
assert not np.any(changed[286:437,678:859]),'Central medallion altered'
report=dict(originalSourceSha256=hashlib.sha256((R/'source-assets/cowork-environment-final.png').read_bytes()).hexdigest(),architectureOutsideAdditionsPixelExact=True,centralMedallionPixelExact=True,sourcePixelsUnchanged=int((~changed).sum()),totalPixels=1536*1024,changedPixels=int(changed.sum()),desks=0,practiceMats=12,instructorMats=1,gatheringCushions=6,teaTables=2,additions=changes,poses='Standing native reference only; no yoga animation or sit interaction implemented')
b.js(out/'SOURCE-PRESERVATION.json',report)
(out/'GUIDE.md').write_text('''# Timber & Stone Yoga Retreat\n\nExact architectural source of the accepted Timber & Stone Design Studio, with separate native-scale furniture layers replaced. The studio release is unchanged.\n\n12 aligned practice mats in two compact six-mat banks, front instructor mat, original central medallion, two lower tea/rest alcoves, six walk-to cushions and towel/rolled-mat cubbies. Two native tea tables are visual artwork. No desks remain.\n\n## Runtime\nHost the entire map32 folder together. map.tmj is native32; map.wam is an editor companion with a bounded instructor speaker area and student listener area referencing the instructor's exact area ID, plus separate alcove conversation areas. Only the one spawn cell is silent. General circulation and practice floors remain social.\n\nMats and cushions are walk-to visual destinations. Previews use standing reference avatars; no yoga pose or sitting animation is implemented. Native instructor broadcast properties are configured; live broadcast audio, classes, media and conferencing are not live-tested.\n\n## Source and rebuild\nRun python tools/build_yoga.py from the source bundle root, then node tools/verify_native_routes.cjs timber-yoga-retreat-r1 and python tools/check_head_geometry.py timber-yoga-retreat-r1. Dependencies: Python3, Pillow, NumPy and Node.js. All added cloth/prop sprites are deterministic source-authored canvas artwork; reused environment and tea table are frozen existing assets. No generation, network, engine changes or paid services are needed.\n\nThe preserved architectural source remains byte-identical. SOURCE-PRESERVATION.json verifies every pixel outside enumerated additive sprite regions and the whole central medallion. Preview renders are reconstructed from runtime atlases, not screenshots of a live room.\n''')
print(json.dumps({k:v for k,v in report.items() if k!='additions'},indent=2))
