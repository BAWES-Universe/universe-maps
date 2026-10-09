from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,math
R=Path(__file__).resolve().parents[1];d=json.loads((R/'module.json').read_text());base=Image.open(R/'layers/court-base.png').convert('RGBA')
walk=Image.new('L',base.size);dr=ImageDraw.Draw(walk)
for p in d['walkablePolygons']:dr.polygon([tuple(v) for v in p],fill=255)
fgmask=ImageChops.invert(walk)
# Keep the entire raised fountain/water receiver BELOW motion and characters. Never cover its animated water with a broad nonwalkable canopy.
ImageDraw.Draw(fgmask).ellipse((332,176,648,424),fill=0)
fg=base.copy();fg.putalpha(fgmask);fg.save(R/'layers/court-canopy.png');walk.save(R/'layers/court-walkable-mask.png')
# Exact authored masks are separate from the native art; diagnostic only, not an illustration replacement.
overlay=base.copy();q=Image.new('RGBA',base.size);qd=ImageDraw.Draw(q)
for p in d['walkablePolygons']:qd.polygon([tuple(v) for v in p],fill=(70,230,190,50))
for o in d['obstacles']:
 if o['type']=='ellipse':qd.ellipse((o['cx']-o['rx'],o['cy']-o['ry'],o['cx']+o['rx'],o['cy']+o['ry']),fill=(255,40,75,90))
 elif o['type']=='circle':qd.ellipse((o['cx']-o['radius'],o['cy']-o['radius'],o['cx']+o['radius'],o['cy']+o['radius']),fill=(255,40,75,90))
 else:qd.polygon([tuple(v) for v in o['points']],fill=(255,40,75,90))
overlay.alpha_composite(q);overlay.save(R/'docs/court-geometry-review.png')
