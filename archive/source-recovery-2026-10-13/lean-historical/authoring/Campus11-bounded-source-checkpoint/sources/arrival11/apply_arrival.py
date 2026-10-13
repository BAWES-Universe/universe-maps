"""Apply the bounded Campus11 arrival art and area edit to a candidate only.

Run after exterior10/apply_exterior.py and before compile32.py. The original
wayfinding08 source remains preserved. This script does not touch a WAM.
"""
from pathlib import Path
from PIL import Image
import argparse,json
import numpy as np

HERE=Path(__file__).resolve().parent
def apply(root):
    root=Path(root).resolve()
    if root.name=='magical-campus-current32-10-24seats':
        raise ValueError('The published Campus10 baseline is read-only')
    meta=json.loads((HERE/'placement.json').read_text())
    x,y=meta['world']; sign=Image.open(HERE/'court-sign.png').convert('RGBA')
    box=(x,y,x+sign.width,y+sign.height)
    mask=np.asarray(sign)[:,:,3]>0
    base=Image.open(root/'layers/campus-base.png').convert('RGBA')
    base.alpha_composite(sign,(x,y));base.save(root/'layers/campus-base.png')
    above=Image.new('RGBA',base.size)
    for name in ['foreground','glass','shade']:
        path=root/f'layers/campus-{name}.png'
        im=Image.open(path).convert('RGBA')
        crop=np.asarray(im.crop(box)).copy();crop[mask]=0
        im.paste(Image.fromarray(crop),box);im.save(path);above.alpha_composite(im)
    above.save(root/'layers/campus-above.png')
    for rel in ['map/magical-campus.tmj','map32/magical-campus.tmj']:
        path=root/rel
        if not path.exists():continue
        m=json.loads(path.read_text())
        objs=[o for l in m['layers'] for o in l.get('objects',[])]
        starts=[o for o in objs if o.get('name')=='start']
        quiet=[o for o in objs if o.get('name')=='spawn-quiet-start']
        assert len(starts)==len(quiet)==1
        assert starts[0]['width']==starts[0]['height']==32
        starts[0].update(x=1232,y=1520)
        quiet[0].update(x=1200,y=1504,width=96,height=96)
        path.write_text(json.dumps(m,separators=(',',':'))+'\n')
    return {'sign':meta['world']+meta['nativeSize'],'spawnCenter':[1248,1536],
            'spawnFeet':[1248,1552],'silentRectangle':[1200,1504,96,96],
            'WAMChanged':False,'collisionChanged':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('candidate');a=p.parse_args()
    print(json.dumps(apply(a.candidate)))
