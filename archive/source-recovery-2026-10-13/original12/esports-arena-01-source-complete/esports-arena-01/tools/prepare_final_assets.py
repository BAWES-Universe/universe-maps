from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];m=json.load(open(R/'source/industrial-scale-manifest.json'))
for n,a in m.items():
 im=Image.open(R/a['master']).convert('RGBA').crop(tuple(a['alphaCrop']));im.resize(tuple(a['nativeSize']),Image.Resampling.LANCZOS).save(R/'assets'/('industrial-'+n+'-native.png'))
print('Rebuilt selected native asset variants from included full masters with one aspect-preserving reduction.')
