from pathlib import Path
import json
from PIL import Image,ImageDraw
import build_templates as b
from build_environments import desk,foreground_polygon
b.C,b.N,b.W,b.H=48,32,1536,1024
def cowork():
 m=b.Map('timber-design-studio-r2','Timber & Stone Design Studio','Work',b.P);m.base=b.A['cowork-environment-final'].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
 for rr in [(5,5,38,9),(4,6,41,8),(21,5,6,22),(19,18,11,5),(6,18,11,6),(31,18,12,6),(17,19,4,3),(27,19,5,3),(22,24,4,8)]:m.block(*rr,0)
 m.block(18,12,3,6);m.block(27,12,3,6) # visible central stone piers are solid
 m.block(18,0,3,7);m.block(27,0,3,7) # north column bases
 m.block(4,6,2,4);m.block(42,6,3,4);m.block(4,12,2,2);m.block(42,12,3,2) # plant footprints
 m.block(21,23,1,6);m.block(26,23,1,6);m.block(16,21,2,4);m.block(30,21,2,4) # entry shoulders
 m.block(6,18,2,5);m.block(41,18,2,5);m.block(6,23,12,1);m.block(30,23,13,1) # complete lower window/plant perimeter
 m.block(4,5,3,9);m.block(42,5,3,9);m.block(7,5,1,2);m.block(40,5,2,2) # complete upper side ledges and corner plants
 for i,(x,y) in enumerate([(7,7),(15,7),(7,11),(15,11),(31,7),(39,7),(31,11),(39,11)]):desk(m,x,y,'desk-'+str(i+1))
 for name,x in [('Meeting A',10),('Meeting B',36)]:
  m.zone(name,x-3,18,9,6);m.anchor(name+' approach',x+3,21)
 m.anchor('west studio entry',19,10);m.anchor('east studio entry',29,10);m.anchor('materials gallery',24,6);m.anchor('central hall',24,20);m.anchor('arrival',24,29)
 foreground_polygon(m,[(96,448),(579,448),(579,487),(96,487)])
 foreground_polygon(m,[(965,448),(1442,448),(1442,487),(965,487)])
 m.cropboxes=[('desk-west',(160,192,608,448)),('desk-east',(928,192,1376,448)),('meeting',(192,544,1376,768))];m.finish();return m

if __name__=='__main__':
 m=cowork()
 p=b.R/m.slug
 audit=json.loads((p/'VALIDATION.json').read_text());audit.update(deskCount=8,lowerRoomSeats=0,lowerRoomTables=0);b.js(p/'VALIDATION.json',audit)
 (p/'GUIDE.md').write_text("""# Timber & Stone Design Studio r2

The accepted original Timber studio with both lower rooms cleared of all seats and tables. Eight individual upper work desks are retained exactly. Timber, stone, floors, windows, garden, lighting and central medallion remain unchanged. The original r1 is immutable.

## Runtime
Host the complete map32 folder together. Native32 map.tmj includes collision, spawn and single-cell spawn silence. map.wam retains two bounded optional lower-room conversation areas; this is room configuration, not a live-tested conferencing connection.

Desk seating is walk-to visual seating with native foreground backrails. No custom sit animation or live media feature is implemented. Lower rooms are empty, open and walkable; removed furniture has no remaining seat targets or collision.

## Rebuild and checks
Run python tools/build_studio.py, then node tools/verify_native_routes.cjs timber-design-studio-r2 and python tools/check_head_geometry.py timber-design-studio-r2. Python3, Pillow, NumPy and Node.js required. Frozen reused original art and unmodified pinned native movement fixtures are included. No network, paid services or engine changes needed. Previews are runtime-atlas static occupied proofs, not live screenshots.
""")
