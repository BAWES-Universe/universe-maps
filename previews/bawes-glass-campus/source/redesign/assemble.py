"""Register a retained art study to native gameplay anchors; no camera/avatar scaling."""
from PIL import Image
from pathlib import Path

def apply(root,floor,backs,blocked,seats,tables):
 patch=Image.open(root/'source/redesign/section-registered-original.png').convert('RGBA').resize((768,576),Image.Resampling.LANCZOS)
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
