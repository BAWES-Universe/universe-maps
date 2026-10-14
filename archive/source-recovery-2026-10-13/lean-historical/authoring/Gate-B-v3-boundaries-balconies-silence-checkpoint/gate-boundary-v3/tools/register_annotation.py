from PIL import Image
import numpy as np,json
from scipy.ndimage import map_coordinates,gaussian_filter
from scipy.optimize import least_squares
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=np.asarray(Image.open(R/'baseline/art-composite.png').convert('RGB'),dtype=float)
b=np.asarray(Image.open('/workspace/shared/gate-user-boundary-feedback/marked-gate.png').convert('RGB'),dtype=float)
# Stable scenery across the screenshot; discard saturated markup and lower-center player/HUD.
y,x=np.mgrid[3:b.shape[0]-3:3,3:b.shape[1]-3:3]; sel=~((x>325)&(x<475)&(y>545)&(y<660)); col=b[y,x]; sel&=~((col[:,:,0]>col[:,:,1]*1.5)&(col[:,:,0]>150)); sel&=~((col[:,:,1]>col[:,:,0]*1.5)&(col[:,:,1]>110)); x=x[sel];y=y[sel]
p=np.array([.932,.932,50.,394.])
for sigma in (4,2,1):
 ga=gaussian_filter(a.mean(axis=2),sigma);gb=gaussian_filter(b.mean(axis=2),sigma); target=gb[y,x]
 def error(p):return (map_coordinates(ga,[(y+p[3])/p[1],(x+p[2])/p[0]],order=1,mode='nearest')-target)
 fit=least_squares(error,p,loss='soft_l1',f_scale=8,max_nfev=80,diff_step=.0001);p=fit.x; print(sigma,p,np.median(abs(error(p))))
rects=[('green-upper-stair',(311,97,364,218)),('green-middle-landing',(303,224,370,263)),('green-middle-stair',(278,268,408,343)),('green-lower-stair',(255,393,330,453)),('green-west-balcony',(31,524,101,563)),('green-east-balcony',(706,525,778,563)),('red-east-middle-lamp',(518,286,560,355)),('red-east-lower-lamp',(542,391,594,506)),('red-east-tree-edge',(525,644,663,760)),('red-east-bottom-lamp',(573,758,613,822))]
sx,sy,tx,ty=p
result={'method':'Robust least-squares image registration of unchanged native atlas composite to annotated screenshot, excluding colored markup and user HUD; no assumed screenshot/world scale.','screenFromWorld':{'sx':sx,'sy':sy,'offsetX':-tx,'offsetY':-ty},'medianGrayscaleResidual':float(np.median(abs(error(p)))),'sourceComposite':str(R/'baseline/art-composite.png'),'regions':[{'id':name,'screenshotRect':rect,'worldRect':[(rect[0]+tx)/sx,(rect[1]+ty)/sy,(rect[2]+tx)/sx,(rect[3]+ty)/sy]} for name,rect in rects]}
(R/'results/annotation-registration.json').write_text(json.dumps(result,indent=2)+'\n')
xx,yy=np.meshgrid(np.arange(b.shape[1]),np.arange(b.shape[0])); w=np.stack([map_coordinates(a[:,:,c],[(yy+ty)/sy,(xx+tx)/sx],order=1,mode='nearest') for c in range(3)],axis=-1).astype('uint8');Image.fromarray(w).save(R/'results/registered-art.png')
print(json.dumps(result,indent=2))
