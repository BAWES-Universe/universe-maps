from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';j=json.loads((P/'source/layout.json').read_text());
import subprocess,sys
subprocess.run([sys.executable,str(R/'tools/render_runtime_proofs.py')],check=True)
out=Image.open(P/'review/exterior-occupied-native.png').convert('RGBA')
mask=Image.new('L',out.size);d=ImageDraw.Draw(mask)
for f in j['protectedFixtures']:
 x,y,x2,y2=f['solidXYXY'];d.rectangle((x,y,x2-1,y2-1),fill=255)
mask.save(P/'source/protected-fixture-footprints.png');(P/'validation/fixture-mask-scope.json').write_text(json.dumps(dict(scope='Explicit conservative whole-fixture footprint bounds copied from r6 plus new exterior bench/planter/garden bounds. This is an authored mask to inspect against artwork, not automatic semantic detection.',source='source/layout.json protectedFixtures',mask='source/protected-fixture-footprints.png',requiresVisualReview=True),indent=2)+'\n')
print('Decoded outdoor proof and fixture bounds updated')
