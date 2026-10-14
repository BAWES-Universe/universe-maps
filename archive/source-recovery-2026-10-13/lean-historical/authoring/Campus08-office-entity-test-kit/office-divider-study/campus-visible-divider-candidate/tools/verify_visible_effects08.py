from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parents[1];base=Image.open(R/'layers/campus-base.png').convert('RGBA');above=Image.open(R/'layers/campus-above.png').convert('RGBA');data=json.loads((R/'effects/effects.json').read_text());reports=[]
for e in data['effects']:
 x,y=e['origin'];w,h=e['size'];bg=base.crop((x,y,x+w,y+h));fg=above.crop((x,y,x+w,y+h));renders=[]
 for file in e['frames']:
  rendered=Image.alpha_composite(Image.alpha_composite(bg,Image.open(R/file).convert('RGBA')),fg).convert('RGB');renders.append(np.asarray(rendered,dtype=np.int16))
 diff=np.max(np.abs(np.stack(renders)-renders[0]),axis=(0,3));visible=int((diff>3).sum());peak=int(diff.max());reports.append({'effect':e['name'],'visibleChangedPixelsAfterForeground':visible,'peakChannelChange':peak,'pass':visible>20 and peak>3})
result={'pass':all(r['pass']for r in reports),'scope':'Pixel-composited visible differences through fixed foreground; playback pacing and physical-device smoothness separate.','effects':reports};(R/'docs/visible-effects08.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['pass']
