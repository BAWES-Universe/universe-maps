"""Regression for the captured y=1024 texture edge at the recorded .32768 camera."""
from pathlib import Path
from PIL import Image
import json
r=Path(__file__).resolve().parents[2]/'review';results={}
for name in ['north-seam-baseline','north-seam-padded','mobile-edge-north','optimized-north-seam-padded']:
 im=Image.open(r/(name+'.png')).convert('RGB');line=im.getpixel((200,246));near=im.getpixel((200,247));delta=max(abs(a-b) for a,b in zip(line,near));results[name]={'pixel':line,'neighbor':near,'maximumChannelDifference':delta}
assert results['north-seam-baseline']['maximumChannelDifference']>20
assert all(v['maximumChannelDifference']<4 for k,v in results.items() if k!='north-seam-baseline')
(r/'seam-pixel-checks.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
