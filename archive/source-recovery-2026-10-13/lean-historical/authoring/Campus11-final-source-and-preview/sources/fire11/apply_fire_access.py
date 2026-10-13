"""Apply the bounded authored bench repair and fixed per-object layer ownership.

The source fine grid is replaced independently in sources/garden. Native32
compilation retains the ordinary max-coalescing rule, without dynamic collision.
"""
from pathlib import Path
import argparse, json, hashlib
from PIL import Image
import numpy as np

HERE = Path(__file__).resolve().parent

def apply(root):
    root = Path(root).resolve()
    if not (root/'BASELINE-CAMPUS10.json').is_file():
        raise ValueError('This repair requires an isolated Campus11 baseline marker')
    origin = (1904, 1248)
    base_path = root/'layers/campus-base.png'
    base = Image.open(base_path).convert('RGBA')
    patch = Image.open(HERE/'garden-functional-repair-patch.png').convert('RGBA')
    before = np.asarray(base).copy()
    base.alpha_composite(patch, origin)
    base.save(base_path)
    old = np.asarray(Image.open(root/'sources/garden/bench-and-foliage-fixed-foreground.png').convert('RGBA'))
    new = np.asarray(Image.open(HERE/'garden-fixed-foreground.png').convert('RGBA'))
    changed = np.any(old != new, axis=2)
    fg_path = root/'layers/campus-foreground.png'
    fg = Image.open(fg_path).convert('RGBA')
    x,y = origin
    box = (x,y,x+1024,y+1024)
    region = np.asarray(fg.crop(box)).copy()
    region[changed] = new[changed]
    fg.paste(Image.fromarray(region), box)
    fg.save(fg_path)
    above = Image.new('RGBA',base.size)
    for name in ['foreground','glass','shade']:
        above.alpha_composite(Image.open(root/f'layers/campus-{name}.png').convert('RGBA'))
    above.save(root/'layers/campus-above.png')
    result = {'worldOrigin':list(origin),'artChangedPixels':int(np.any(before!=np.asarray(base),axis=2).sum()),
              'fixedForegroundOwnershipPixels':int(changed.sum()),'dynamicMasks':False,
              'fireEffectMoved':False,'noPoseOrSnap':True,
              'gridSource':str(root/'sources/garden/collision-grid-8px.json')}
    (root/'docs/fire-access11-integration.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('candidate')
    print(json.dumps(apply(parser.parse_args().candidate)))
