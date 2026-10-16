"""Native registration for the separately authored illustrated brand-reset study."""
from PIL import Image

def apply(root,floor,backs,blocked,seats,tables):
 source=Image.open(root/'source/brand_reset/section-original.png').convert('RGBA').resize((768,576),Image.Resampling.LANCZOS)
 sx=[0,32,118,156,196,288,324,472,569,607,644,736,768]
 dx=[0,32,112,144,176,288,320,480,560,592,624,736,768]
 sy=[0,89,119,174,201,214,228,251,268,296,328,576]
 dy=[0,96,128,178,224,232,240,268,288,320,352,576]
 mesh=[((dx[i],dy[j],dx[i+1],dy[j+1]),(sx[i],sy[j],sx[i],sy[j+1],sx[i+1],sy[j+1],sx[i+1],sy[j])) for j in range(len(sy)-1) for i in range(len(sx)-1)]
 patch=source.transform((768,576),Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)
 floor.alpha_composite(patch,(320,1280));backs.paste((0,0,0,0),(320,1248,1088,1856))
 # Only the low front lip overlaps the avatar's feet, not its torso.
 for x in [112,144,176,560,592,624]:backs.alpha_composite(patch.crop((x-14,274,x+14,286)),(320+x-14,1554))
 backs.alpha_composite(patch.crop((64,50,128,56)),(384,1330))
 blocked.difference_update((x,41) for x in range(28,32));blocked.update((x,46) for x in [16,30,31])
 for t in tables:
  if t[:2]==[13,46]:t[2]=4
  if t[:2]==[27,46]:t[2]=5
 patch.save(root/'review/brand-section-native.png')
