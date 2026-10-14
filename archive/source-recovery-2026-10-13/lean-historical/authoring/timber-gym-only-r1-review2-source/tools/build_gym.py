"""Gym-only variant from original generated raster. Raster kept unchanged."""
from PIL import Image,ImageDraw
import hashlib,json
import build_templates as b
b.C,b.N,b.W,b.H=48,32,1536,1024
m=b.Map('timber-gym-only-r1','Timber & Stone Gym','Activities',b.P)
m.base=b.A['gym-only-environment'].copy();m.d=ImageDraw.Draw(m.base)
m.above=Image.new('RGBA',(b.W,b.H));m.a=ImageDraw.Draw(m.above);m.spawn=(24,29)
# Conservative inscribed floor. Full projected equipment/architecture remains
# blocked with a margin; no routes through visible machinery, ledges or piers.
for r in [(13,7,23,9),(12,8,1,1),(12,12,1,1),(12,15,1,1),
          (11,8,1,1),(36,7,1,5),(35,12,2,1),
          (21,7,6,16),(15,16,18,6),
          (8,21,12,2),(15,19,6,2),
          (28,21,6,1),(35,22,6,1),(33,22,2,1),(28,19,5,2),
          (22,23,4,8)]:m.block(*r,0)
m.block(21,22,1,1);m.block(26,22,1,1) # Entry postcap silhouettes, including tangent sprite edges.
# Demo approach deliberately stops below the physical stage and column feet.
# Native avatar stands in front of scenery; no riding/lifting/seat interaction.
for name,x,y in [
 ('instructor position',24,7),('demo audience',24,10),
 ('strength bench north approach',13,10),('strength bench south approach',13,14),
 ('rear rower approach',11,8),('cardio bike north approach',36,8),
 ('cardio bike south approach',36,11),('cardio rower approach',35,14),
 ('west station aisle',15,12),('east station aisle',33,12),
 ('central medallion',24,13),('arrival bench approach',14,21),
 ('water station approach',37,22),('west nook doorway',18,20),
 ('east nook doorway',29,20),('arrival hall',24,22),('arrival',24,29)]:m.anchor(name,x,y)
m.zone('Gym host demonstration',22,7,4,2,'speaker')
m.zone('Gym shared session',14,9,21,7,'listener')
m.zone('Arrival bench conversation',8,21,9,2)
m.zone('Water break conversation',35,22,6,1)
m.cropboxes=[('strength',(96,160,576,528)),('cardio',(1056,128,1440,528)),('arrival-nooks',(192,544,1376,768))]
m.finish()
out=b.R/m.slug
(out/'GUIDE.md').write_text('''# Timber & Stone Gym\n\nGym-only native32 variation. Original mixed activity concept and Yoga map remain separate and unchanged. Two strength benches and weight racks occupy the west edge; two bikes and a rower occupy the east edge; another rower sits at the northwest. The broad medallion center remains open. Arrival bench and water/towel nooks contain no tiny low coffee tables.\n\n## Implemented\n48 x 32 native32 TMJ, exact original generated environment raster compiled into atlases, conservative solid geometry for entire projected equipment and architecture, 17 walk-to approach anchors, spawn and spawn-only silence. Companion WAM includes native instructor/listener areas and separate arrival/water conversation zones. Equipment is scenery: no riding, lifting or exercise animation, machine controls, exercise tracking, instructor service, or media connection is implemented. Reference avatars stand.\n\n## Online use\nMeet an accountability partner, join a host-led session, or talk during a water break. Physical exercise happens in participants' own spaces. Optional audio/video services require deployment/editor setup and are not live-tested. Display artwork is not a connected player.\n\n## Technical limits\nStatic atlas reconstruction, source geometry and pinned route replay are validation gates; they do not establish live browser, keyboard, mobile, network, audio, multi-user or deployment behavior. The raster is a new generated Timber-family environment, not pixel-identical to the original office. Full projected solid silhouettes are blocked conservatively, with routes routed away from machinery, windows, plants and piers.\n\n## Rebuild\npython tools/build_gym.py\nnode tools/verify_native_routes.cjs timber-gym-only-r1\npython tools/check_head_geometry.py timber-gym-only-r1\nRequires Python3, Pillow, NumPy and Node.js. No engine changes or paid services.\n''')
b.js(out/'ASSET-PROVENANCE.json',{'environment':'Original built-in image_gen art; gym-only edit of previously generated Timber Circuit Gym concept','reference':'Accepted Timber Design Studio visual style; not pixel-identical office architecture','sourceSha256':hashlib.sha256((b.R/'source-assets/gym-only-environment.png').read_bytes()).hexdigest(),'sourceUnchanged':m.base.tobytes()==b.A['gym-only-environment'].tobytes(),'equipment':'Visual artwork only, not interactive','avatars':'Existing greg-reference sprite, standing frames only','originalConceptPreserved':True})
