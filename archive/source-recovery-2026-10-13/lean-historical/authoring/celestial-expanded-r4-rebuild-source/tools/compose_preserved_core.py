from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import distance_transform_edt,maximum_filter,gaussian_filter
R=Path(__file__).resolve().parents[1];S=R/'source';old=np.asarray(Image.open(S/'portal-environment-garden-boundaries-master.png').convert('RGBA'));new=np.asarray(Image.open(S/'generated-healed-context.png').convert('RGBA').resize((2048,1536),Image.Resampling.LANCZOS)).copy();g=np.array(json.loads((S/'layout.json').read_text())['grid']);walk=(g==0).repeat(32,0).repeat(32,1)
y,x=np.indices(walk.shape);edge=np.minimum.reduce([x,y,1535-x,1023-y]);a=np.clip(edge/112,0,1);a=a*a*(3-2*a)
# Restore all original walkable pixels and the native body/architecture around paths exactly.
dist=distance_transform_edt(~walk);guard=np.clip((48-dist)/24,0,1);a=np.maximum(a,guard)
# Restore portal arches with a soft perimeter, except the previously cropped uppermost crown.
for x0,y0,x1,y1 in [(640,32,896,224),(208,64,448,304),(1088,64,1344,304),(144,416,448,704),(1088,416,1392,704)]:
 m=np.zeros(walk.shape,bool);m[y0:y1,x0:x1]=1;d=distance_transform_edt(~m);a=np.maximum(a,np.clip((32-d)/32,0,1))
core=new[256:1280,256:1792].astype(float);core=old.astype(float)*a[:,:,None]+core*(1-a[:,:,None]);new[256:1280,256:1792]=np.rint(core).astype('uint8');Image.fromarray(new).save(S/'final-composite.png');Image.fromarray(np.rint(a*255).astype('uint8')).save(S/'preservation-alpha.png');Image.fromarray(new).save(R/'final-composite-preview.png')
assert np.array_equal(new[256:1280,256:1792][walk],old[walk]);print('exact walkable pixels',int(walk.sum()),'all original pixels retained',int((a==1).sum()))
