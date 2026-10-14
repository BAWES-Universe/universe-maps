from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,itertools,numpy as np
from offline_audit_lib import load_map
R=Path(__file__).resolve().parents[1];L=json.loads((R/'evidence/layout.json').read_text());rows=[]
def exact(im,w,h):
 a=np.asarray(im);x=((2*np.arange(w)+1)*im.width)//(2*w);y=((2*np.arange(h)+1)*im.height)//(2*h);return Image.fromarray(a[y[:,None],x[None,:]])
def scales(room,active,label):
 m,g,im,fg,layers,_=load_map(R/'runtime/mechanical-orchard.tmj',active,[x for x in L['feedbackLayers']if x not in active]);ox,oy=L['rooms'][room]['offset'];w,h=L['rooms'][room]['size'];box=(ox,oy,ox+w,oy+h);ref=im.crop(box);local=[v.crop(box)for _,v in layers];out=[];assert np.array_equal(g,np.array(L['grid'],bool));assert ref.getextrema()[3]==(255,255)
 for scale in [.5,.75,1,1.25,1.5,2]:
  t=round(32*scale);dw=w//32*t;dh=h//32*t;dest=Image.new('RGBA',(dw,dh));xx=(np.arange(dw)//t)*32+((2*(np.arange(dw)%t)+1)*32)//(2*t);yy=(np.arange(dh)//t)*32+((2*(np.arange(dh)%t)+1)*32)//(2*t)
  for v in local:
   a=np.array(v);dest=Image.alpha_composite(dest,Image.fromarray(a[yy[:,None],xx[None,:]]))
  whole=exact(ref,*dest.size);delta=int(np.any(np.asarray(dest)!=np.asarray(whole),axis=2).sum());assert delta==0
  out.append(dict(scale=scale,tileSize=t,differentPixels=delta,transparentPixels=int((np.asarray(dest)[:,:,3]<255).sum()),**{'pass':True}))
 rows.append(dict(room=room,label=label,active=active,decodedSHA256=hashlib.sha256(ref.tobytes()).hexdigest(),collisionInvariant=True,scales=out,**{'pass':True}));return ref
scales('house',[],'house')
for p in itertools.product(range(3),repeat=3):scales('orchard',[tree+'-phase-'+str(n)for tree,n in zip(['petal','leaf','fruit'],p)if n],str(p))
report=dict(allPass=True,scope='Author exact emitted TMJ decoded layer composition versus whole-scene fixed-origin rational-nearest sampling. Six scales for interior and all27 independent tree combinations, including actual branch foreground. Numeric source raster equality only; visual state registration, independent image review, GPU filtering, fractional camera offsets, browser zoom and live controls are separate.',compositions=len(rows),scalesEach=6,rows=rows);(R/'evidence/six-scale-states.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='rows'},indent=2))
