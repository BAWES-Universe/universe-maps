"""New environment-first Sales Atelier and Inventor Sandbox maps, native32."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
import build_templates as b
b.C,b.N,b.W,b.H=48,32,1536,1024
R=b.R

def new_map(slug,title,category,art,spawn,outer):
 m=b.Map(slug,title,category,dict(b.P,outer=outer));m.base=b.A[art].copy();m.d=ImageDraw.Draw(m.base);m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=spawn;return m

def foreground_polygon(m,points):
 mask=Image.new('L',(b.W,b.H));ImageDraw.Draw(mask).polygon(points,fill=255);patch=m.base.copy();patch.putalpha(mask);m.above.alpha_composite(patch)

def desk(m,x,y,name):
 m.base.alpha_composite(b.A['light-desk'],(x*32-16,y*32-8));m.block(x-1,y,3,1);m.seat(x,y+1,name)

def taskseat(m,x,y,name):
 px,py=x*32+16,y*32+15;im=b.A['industrial-chair40-native'];m.base.alpha_composite(im,(px-20,py-24));m.above.alpha_composite(im.crop((6,23,34,39)),(px-14,py-1));m.block(x,y+1,1,1);m.seats.append(dict(name=name,cell=[x,y],anchor=[px,py],floorClick=[px,py+16],direction='north'))

def clip_foreground_heads(m):
 # Preserve the composite artwork byte-for-byte while making every tangent
 # body-clear position safe across the union of all twelve native avatar heads.
 blocked=np.array(m.g,dtype=bool).repeat(32,0).repeat(32,1);Y,X=np.indices(blocked.shape);ii=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)));xa=np.maximum(0,X-8);xb=np.minimum(b.W,X+8);yb=np.minimum(b.H,Y+16);clear=(ii[yb,xb]-ii[Y,xb]-ii[yb,xa]+ii[Y,xa]==0)&(X>=8)&(X+8<=b.W)&(Y+16<=b.H)
 greg=np.array(b.A['greg-reference']);head=np.zeros((14,32),bool)
 for rr in range(4):
  for cc in range(3):head|=greg[rr*32:rr*32+14,cc*32:cc*32+32,3]>32
 swept=np.zeros_like(clear)
 for yy,xx in np.argwhere(head):
  dx,dy=int(xx)-16,int(yy)-16;x0=max(0,-dx);x1=min(b.W,b.W-dx);y0=max(0,-dy);y1=min(b.H,b.H-dy);swept[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
 fg=np.array(m.above);unsafe=(fg[:,:,3]>0)&swept;before=Image.alpha_composite(m.base,m.above);transfer=fg.copy();transfer[~unsafe]=0;m.base.alpha_composite(Image.fromarray(transfer));fg[unsafe]=0;m.above=Image.fromarray(fg);assert Image.alpha_composite(m.base,m.above).tobytes()==before.tobytes()
 return dict(transferredPixels=int(unsafe.sum()),combinedArtworkByteExact=True,method='Exhaustive native16x16 body-clear integer placements, union of 12 native32 head frames; only head-unsafe foreground transferred below avatars')

def finalize(m,description,details):
 safety=clip_foreground_heads(m);m.finish();out=R/m.slug;b.js(out/'source/foreground-safety.json',safety)
 # Amend metadata with only implemented behavior and an explicit interaction contract.
 b.js(out/'source/interaction-contract.json',dict(description=description,stations=details,mode='Native collision and editor-ready native WAM area definitions only',seating='Walk-to visual seating, not sitting animation',screens='Decorative placeholders: no CRM, research, AI, bot, tool or media integrations activated',spawnSilence='Every random start position lies in the sole silent spawn tile; ordinary social circulation remains nonsilent',livePlaytest=False))
 (out/'GUIDE.md').write_text(f'''# {m.title}\n\n{description}\n\nCategory: {m.category}. 48×32 tiles at native32 scale (1536×1024 pixels). {len(m.seats)} walk-to visual seats.\n\n## Using this template\nHost the complete map32 folder together. map.tmj contains the architecture, furniture, collision, safe spawn, and spawn-only silent layer. map.wam adds native editor-ready room-area semantics; its mapUrl is relative. Import or review these areas in your Universe editor before deployment. No service was activated.\n\n{details}\n\n## What is functional\n- Tile collision, connected circulation, random spawn containment, and local spawn-only silence are authored in the TMJ.\n- Seats use the current native32 reference body and walk-to floor-click positions. No invented seated animation, sprite scale change, custom engine behavior, or player is baked into the map.\n- Meeting areas use current native WAM room definitions. Media, multi-user audio/video, and editor import have not been tested live.\n- Screens, research desks, creation pads and tool areas are editor-ready decorative destinations. No CRM connection, AI bot, research service, external tool, or data feed is active. Add only your own approved links and services.\n\n## Verification\nVALIDATION.json reports the source/atlas round trip and authored anchor checks. NATIVE-ROUTES.json replays actual pinned source-derived native moveTo, path fitting, return, same-cell and sequential routes at 60 Hz with body samples at ≤0.5 pixels. HEAD-GEOMETRY.json decodes the actual TMJ and checks exhaustive integer native-body placements against all 12 reference avatar head frames. Static occupied images are compiled-atlas renders, not live room screenshots. See each check's exact scope.\n\n## Rebuild\nThe self-contained rebuild ZIP contains frozen original art, compiler, avatar review fixture and pinned native movement fixtures. Install Python3, Pillow and NumPy, plus Node.js for native route tests. From its root run python tools/build_environments.py {('sales' if 'sales' in m.slug else 'maker')}, then node tools/verify_native_routes.cjs {m.slug}, then python tools/check_head_geometry.py {m.slug}. This rebuild requires no API, credential, paid provider, network request, engine patch or generation call.\n\nOriginal architectural art was generated with the built-in image tool; existing approved native furniture is documented in ASSET-PROVENANCE.md. No publication or existing project overwrite occurred.\n''')
 return m

def sales():
 m=new_map('art-deco-sales-atelier','Art Deco Sales Atelier','Work','sales-environment-flat',(24,28),'#10151e')
 for r in [(6,13,37,13),(7,6,10,6),(10,12,4,1),(31,6,11,6),(34,12,4,1),(22,7,4,6),(21,25,6,4)]:m.block(*r,0)
 m.block(42,13,1,2);m.block(15,25,6,1);m.block(27,25,6,1)
 # Two independent client lounges. Furniture retains its approved native dimensions.
 for name,x in [('Client west',11),('Client east',35)]:
  m.smalltable(x,8);m.seat(x,10,name+' seat A');m.seat(x+1,10,name+' seat B');m.zone(name,x-3,6,10,6);m.anchor(name+' entrance',x+1,12);m.anchor(name+' host',x+3,9)
 # Two parquet research wings: eight individual native laptop desks.
 for i,(x,y) in enumerate([(8,17),(13,17),(8,22),(13,22),(35,17),(40,17),(35,22),(40,22)]):desk(m,x,y,'research-'+str(i+1))
 for x in [23,24]:m.seat(x,9,'briefing-'+str(x-22))
 m.zone('Research west - editor placeholder',6,16,10,9,'placeholder');m.zone('Research east - editor placeholder',33,16,10,9,'placeholder');m.zone('Private briefing',22,7,4,5);m.anchor('briefing presenter',23,7);m.anchor('briefing entrance',23,12)
 m.anchor('west research aisle',10,20);m.anchor('east research aisle',37,20);m.anchor('flat compass inlay',24,19);m.anchor('arrival',24,28)
 foreground_polygon(m,[(94,864),(489,864),(489,932),(94,932)])
 foreground_polygon(m,[(1045,864),(1441,864),(1441,932),(1045,932)])
 m.cropboxes=[('client-west',(192,160,576,416)),('client-east',(960,160,1376,416)),('research',(192,512,1408,800)),('briefing',(672,192,864,416))]
 return finalize(m,'A brass, teal and walnut urban sales atelier with two private client bays, eight research desks, and an intimate briefing alcove.', 'The central compass is a flush floor inlay. Client bays each have two native lounge seats and a low brass table. Eight laptop desks support research work; the northern board and two briefing seats form a small presentation destination. Broad central circulation remains social and nonsilent.')

def maker():
 m=new_map('inventors-sandbox-workshop','Inventor’s Sandbox Workshop','Sandbox','maker-environment-open',(11,28),'#293b32')
 for r in [(7,7,31,18),(6,7,1,8),(38,12,6,2),(40,6,5,3),(41,9,2,3),(38,14,2,1),(36,19,3,3),(37,19,8,6),(8,25,6,4)]:m.block(*r,0)
 # Southern pier/plant remain solid; doorway is actual edited artwork, never a wall walk-through.
 m.block(36,22,1,3);m.block(34,23,2,2);m.block(35,15,3,4)
 # Six tool-bench chairs face the existing illustrated northern workbench.
 for i,x in enumerate([9,14,19,24,29,34]):taskseat(m,x,7,'toolbench-'+str(i+1))
 # Native table and low-backed workshop task chairs in the wood-floor collaboration corner.
 m.table(39,19);taskseat(m,40,22,'collaboration-A');taskseat(m,42,22,'collaboration-B');m.zone('Collaboration corner',37,18,8,7)
 # The three colored pad surfaces are intentionally open, flexible creation floors.
 for name,x,y in [('Coral creation pad',13,9),('Mint creation pad',26,9),('Ochre creation pad',20,18)]:m.zone(name+' - editor placeholder',x,y,6,5,'placeholder')
 m.zone('Idea board - editor placeholder',40,6,5,3,'placeholder')
 m.anchor('creation pad coral',16,11);m.anchor('creation pad mint',29,11);m.anchor('creation pad ochre',22,19)
 m.anchor('north tool aisle',23,9);m.anchor('west materials aisle',7,17);m.anchor('northeast idea board',42,8);m.anchor('idea board doorway',42,11);m.anchor('collaboration doorway',36,20);m.anchor('collaboration host',43,20);m.anchor('arrival',11,28)
 foreground_polygon(m,[(495,835),(1087,835),(1087,904),(495,904)])
 foreground_polygon(m,[(1173,835),(1487,835),(1487,905),(1173,905)])
 m.cropboxes=[('toolbenches',(224,128,1184,320)),('creation-pads',(352,224,1120,800)),('collaboration',(1120,544,1472,832)),('idea-board',(1216,128,1472,384))]
 return finalize(m,'A bright brick inventor workshop with three flexible creation pads, six native tool-bench seats, an idea-board bay, and a two-seat collaboration corner.', 'Coral, mint and ochre creation circles are flat walkable floor paint. Built-in north and west tools/benches remain solid and reachable from the hall. The southeast wood nook has a real broad doorless opening on its left. The idea board, workbench tools and creation pads are decorative editor-ready placeholders; no tools, bots or services run automatically.')

if __name__=='__main__':
 makers={'sales':sales,'maker':maker}
 if len(sys.argv)>1:makers[sys.argv[1]]()
 else:
  for fn in makers.values():fn()
