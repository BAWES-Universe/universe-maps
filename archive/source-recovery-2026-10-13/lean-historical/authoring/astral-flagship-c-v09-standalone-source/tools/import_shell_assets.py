"""Import frozen proportional source exports without resizing."""
from pathlib import Path
from PIL import Image
import shutil,hashlib,json
R=Path(__file__).resolve().parents[1];A=R/'source-prototype/full-study/assets';F=R/'source/frozen-b'
for name in ['hall-shadow','foyer-shadow','hall-shell','foyer-wings','foyer-roof','foyer-front']:
 shutil.copy2(A/(name+'.png'),R/'assets'/(name+'.png'))
base=Image.open(A/'interior-and-expanded-exterior-base.png').convert('RGBA');base.alpha_composite(Image.open(A/'permanent-threshold-base.png').convert('RGBA'));base.save(R/'assets/runtime-base.png')
shutil.copy2(A/'interior-above-preserved.png',R/'assets/runtime-above.png')
for name in ['greg-reference.png','garden-leaf-accent-native.png']:shutil.copy2(F/name,R/'assets'/name)
files={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in (R/'assets').glob('*.png')}
(R/'source/imported-art-manifest.json').write_text(json.dumps({'worldPixels':[2816,2432],'resizing':False,'acceptedBaseException':{'worldXYWH':[832,2028,128,4],'source':'source-prototype/full-study/assets/permanent-threshold-base.png','intent':'Approved south doorway threshold, permanent below actors; all other translated B base pixels remain exact.'},'files':files},indent=2)+'\n')
