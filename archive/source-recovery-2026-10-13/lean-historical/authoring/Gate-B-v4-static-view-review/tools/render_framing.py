import sys,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from map_render import MapRenderer
R=Path(__file__).resolve().parents[1];root=R/'framing';d=json.loads((root/'COMPOSITIONS.json').read_text());renderer=MapRenderer(R/'publish/public/butterfly-town/gate-b/v4/gate.tmj')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';small=ImageFont.truetype(font,13);normal=ImageFont.truetype(font,16);title=ImageFont.truetype(font,21)
def panel(s,c,label):
 w,h=s['screen']['width'],s['screen']['height'];gh=s['gameHeight'];top=s['reserve']['top'];v=c['view'];im=Image.new('RGB',(w,h+72),'#131825');art=renderer.compose(0,player=c['player']);view=art.transform((w,gh),Image.Transform.AFFINE,(v['width']/w,0,v['x'],0,v['height']/gh,v['y']),resample=Image.Resampling.BILINEAR);im.paste(view.convert('RGB'),(0,46+top));draw=ImageDraw.Draw(im);draw.text((8,10),label,font=normal,fill='white')
 if top:draw.rectangle((0,46,w,46+top),fill='#1e2434');draw.text((8,48),'Status reserve',font=small,fill='#b6bfce')
 if s['reserve']['dock']:
  y=46+h-s['reserve']['dock']-s['reserve']['hud'];draw.rectangle((0,y,w,46+h),fill='#1e2434');draw.text((8,y+7),'HUD + dock reserve',font=small,fill='#b6bfce')
 draw.text((8,h+50),f"Woka {c['avatarCss']:.1f} CSS px | {c['mode']}",font=small,fill='#cad0dd');return im
for s in d['screens']:
 scale=min(1,360/s['screen']['width']);pw=round(s['screen']['width']*scale);ph=round((s['screen']['height']+72)*scale);out=Image.new('RGB',(pw*6+40,ph+112),'#0b101b');draw=ImageDraw.Draw(out);draw.text((16,12),s['screen']['name']+' | static v4 camera candidate',font=title,fill='white');draw.text((16,43),'Native source-class simulation; exact map pixels. Gray reserves are not the live HUD.',font=normal,fill='#b6c3d7');draw.text((16,70),'No cinematic transitions. One mobile setup, then native follow and user-selected zoom.',font=normal,fill='#b6c3d7')
 for i,c in enumerate(s['captures']):out.paste(panel(s,c,c['label']).resize((pw,ph),Image.Resampling.LANCZOS),(20+i*pw,102))
 out.save(root/(s['screen']['name']+'-static-journey.png'))
reference=d['screens'][0];desktop=d['screens'][3];parts=[(reference,reference['normal'],'Phone native baseline'),(reference,reference['captures'][0],'Phone v4 wide setup'),(desktop,desktop['normal'],'Desktop native baseline'),(desktop,desktop['captures'][0],'Desktop v4, no camera calls')];panels=[]
for s,c,label in parts:
 p=panel(s,c,label);scale=min(1,430/p.width);panels.append(p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS))
out=Image.new('RGB',(sum(p.width for p in panels)+50,max(p.height for p in panels)+115),'#0b101b');draw=ImageDraw.Draw(out);draw.text((16,12),'Gate B v4 | phone and desktop arrival comparison',font=title,fill='white');draw.text((16,43),'Same v3 geometry/art. Phone scale matches v3 opening, centered on player. Desktop view is unchanged.',font=normal,fill='#b6c3d7');draw.text((16,70),'Offline source-camera composition, not a screenshot of the live game.',font=normal,fill='#b6c3d7');x=10
for p in panels:out.paste(p,(x,102));x+=p.width+10
out.save(root/'arrival-comparison.png');print('Saved four static journey strips and arrival comparison.')
