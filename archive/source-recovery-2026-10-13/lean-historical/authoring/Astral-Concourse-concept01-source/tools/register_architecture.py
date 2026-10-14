"""Compile generated architectural materials to authored native-grid regions.
Furniture and avatars are not resized. Blueprint coordinates are authoritative.
"""
from PIL import Image
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
src=Image.open(R/'source/grand-hall-shell-v02.png').convert('RGBA')
normalized=src.resize((1536,1280),Image.Resampling.LANCZOS)
out=normalized.copy()
# Generated source has unequal bank widths. Register the lower hall and its
# doorway openings to the same precise native-grid span table.
old=[0,192,528,624,912,1024,1344,1536]
new=[0,192,512,608,928,1024,1344,1536]
for a,b,c,d in zip(old,old[1:],new,new[1:]):
 piece=normalized.crop((a,400,b,1280)).resize((d-c,880),Image.Resampling.LANCZOS)
 out.paste(piece,(c,400))
out.save(R/'assets/hall-architecture.png')
(R/'source/architecture-registration.json').write_text(json.dumps({'source':'grand-hall-shell-v02.png','sourceSize':list(src.size),'runtimeSize':[1536,1280],'stageAbove400UnchangedAfterNormalization':True,'lowerHallOldX':old,'lowerHallNewX':new,'reason':'Register unequal generated carpet/bank geometry and aligned rear portals to native32 grid. Architecture only; Woka and furniture source pixels untouched.','resampling':'Lanczos','mapTileSize':32,'wokaScale':1},indent=2)+'\n')
