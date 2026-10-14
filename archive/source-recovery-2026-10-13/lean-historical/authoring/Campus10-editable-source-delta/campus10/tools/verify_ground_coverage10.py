"""Audit source-ground alpha over every native walk cell and enclosed hole."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from scipy import ndimage

R = Path(__file__).resolve().parents[1]
p = R/'layers/campus-base.png'
alpha = np.asarray(Image.open(p).convert('RGBA'))[:,:,3]
g = json.loads((R/'map32/collision-grid.json').read_text())
blocked = np.zeros((g['height'],g['width']), dtype=bool)
blocked.flat[g['blockedIndices']] = True
walk = ~blocked.repeat(32,0).repeat(32,1)
results = []
for threshold in [1,16,255]:
    missing = alpha < threshold
    labels, count = ndimage.label(missing)
    exterior = set(np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]])))
    holes = []
    for label, sl in enumerate(ndimage.find_objects(labels),1):
        if sl is None or label in exterior:
            continue
        selected = labels[sl] == label
        pixels = int(selected.sum())
        if pixels < 16:
            continue
        ys,xs = sl
        holes.append({'bbox':[xs.start,ys.start,xs.stop,ys.stop], 'pixels':pixels,
                      'onWalkablePixels':int((selected & walk[sl]).sum())})
    results.append({'alphaBelow':threshold, 'walkablePixelsBelowThreshold':int((walk&missing).sum()),
                    'significantEnclosedComponents':holes})
report = {'scope':'All native32 walkable cells, plus significant enclosed alpha components. Connected outer void is intentional finite background; opaque material seams still require visual review.',
          'baseSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),
          'walkableWorldPixels':int(walk.sum()), 'results':results}
(R/'docs/ground-coverage10.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert results[0]['walkablePixelsBelowThreshold'] == 0, 'Transparent ground inside a walkable cell'
