"""Register a retained art study to native gameplay anchors; no camera/avatar scaling."""
from PIL import Image
from pathlib import Path

def apply(root,floor,backs,blocked,seats,tables):
 source=Image.open(root/'source/redesign/section-original.png').convert('RGBA').resize((768,576),Image.Resampling.LANCZOS)
 # Measured structural/table/seat landmarks; mesh preserves authored door geometry.
 sx=[0,24,280,310,462,735,768]
 dx=[0,32,288,320,480,736,768]
 sy=[0,80,110,154,192,200,230,246,272,312,576]
 dy=[0,96,128,178,224,232,266,288,320,352,576]
 mesh=[]
 for j in range(len(sy)-1):
  for i in range(len(sx)-1):
   mesh.append(((dx[i],dy[j],dx[i+1],dy[j+1]),(sx[i],sy[j],sx[i],sy[j+1],sx[i+1],sy[j+1],sx[i+1],sy[j])))
 patch=source.transform((768,576),Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)
 # Register chair groups as separate sprites so all seats remain native tile-centred.
 for box,strip,sprite,dest,size in [
  ((64,226,256,289),(64,289,256,303),(92,226,226,289),(94,226),(100,63)),
  ((512,226,704,289),(512,289,704,303),(539,226,663,289),(543,226),(96,63))]:
  chair_group=patch.crop(sprite).resize(size,Image.Resampling.LANCZOS)
  patch.paste(patch.crop(strip).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS),box)
  patch.alpha_composite(chair_group,dest)
 floor.alpha_composite(patch,(320,1280))
 backs.paste((0,0,0,0),(320,1248,1088,1856))
 # Foreground chair lips are sampled from the same registered art, retaining Woka overlap.
 for x in [112,144,176,560,592,624]:
  backs.alpha_composite(patch.crop((x-14,258,x+14,282)),(320+x-14,1280+258))
 # New lounge front, same two authored seating positions.
 backs.alpha_composite(patch.crop((64,42,128,56)),(384,1322))
 # Remove the old standing whiteboard's blocker: this section now has an open wall gallery.
 blocked.difference_update((x,41) for x in range(28,32))
 blocked.update((x,46) for x in [16,30,31])
 seats[:]=[p for p in seats if p not in [[13,48],[14,48],[15,48],[27,48],[28,48],[29,48]]]+[[13,48],[14,48],[15,48],[27,48],[28,48],[29,48]]
 for t in tables:
  if t[:2]==[13,46]:t[2]=4
  if t[:2]==[27,46]:t[2]=5
 patch.save(root/'review/redesign-section-native.png')
