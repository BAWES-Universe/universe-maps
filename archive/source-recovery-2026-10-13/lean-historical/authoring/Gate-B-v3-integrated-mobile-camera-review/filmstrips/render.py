import json,math
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path(__file__).parent
data=json.loads((root/'COMPOSITIONS.json').read_text())
art=Image.open(root/'assets/unchanged-map-pixels.png').convert('RGBA')
sheet=Image.open(root/'assets/example-32px-sprite.png').convert('RGBA')
avatar=sheet.crop((32,96,64,128))
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(font,16);big=ImageFont.truetype(font,21);small=ImageFont.truetype(font,13)
def phone_frame(s,c):
 w,h=s['screen']['width'],s['screen']['height'];gh=s['gameHeight'];top=s['reserve']['top'];v=c['view']
 im=Image.new('RGBA',(w,h),(17,19,30));view=art.transform((w,gh),Image.Transform.AFFINE,(v['width']/w,0,v['x'],0,v['height']/gh,v['y']),resample=Image.Resampling.BILINEAR)
 im.alpha_composite(view,(0,top));scale=w/v['width'];px=(c['player']['x']-v['x'])*scale;py=top+(c['player']['y']-v['y'])*gh/v['height'];sz=max(1,round(32*scale));spr=avatar.resize((sz,sz),Image.Resampling.NEAREST);im.alpha_composite(spr,(round(px-sz/2),round(py-sz/2)))
 draw=ImageDraw.Draw(im);# outline marks the actual 32px sprite frame, not a larger avatar
 draw.rectangle((px-sz/2-1,py-sz/2-1,px+sz/2+1,py+sz/2+1),outline=(255,216,73),width=1)
 if top:draw.rectangle((0,0,w,top),fill=(25,27,39));draw.text((10,max(0,top/2-7)),'Status area reserve',font=small,fill='#b8bdd0')
 if s['reserve']['dock']:
  y=h-s['reserve']['dock']-s['reserve']['hud'];draw.rectangle((0,y,w,h),fill=(30,31,46));draw.text((10,y+10),'HUD + dock reserve',font=small,fill='#c7ccdc')
  draw.rounded_rectangle((w*.84,h*.63,w-8,y-8),radius=12,fill=(34,35,53));draw.text((w*.85,h*.66),'UI',font=small,fill='#c7ccdc')
 return im.convert('RGB')
def panel(s,c,label):
 w,h=s['screen']['width'],s['screen']['height'];im=Image.new('RGB',(w,h+70),'#131825');im.paste(phone_frame(s,c),(0,45));d=ImageDraw.Draw(im);d.text((8,8),label,font=f,fill='white');d.text((8,h+48),f"Woka {c['avatarCss']:.1f} CSS px | {c['mode']}",font=small,fill='#d1d7e8');return im
for s in data['screens']:
 selected=[s['captures'][i] for i in [0,1,2,3,5]];w,h=s['screen']['width'],s['screen']['height'];scale=min(1,360/w);pw=round(w*scale);ph=round((h+70)*scale);out=Image.new('RGB',(pw*5+40,ph+126),'#0b101b');d=ImageDraw.Draw(out);d.text((16,12),s['screen']['name']+' | mobile arrival option, source-camera simulation',font=big,fill='white');d.text((16,43),'Unchanged map pixels. Gray areas reserve phone UI space; this is not a live game or touch test.',font=f,fill='#b4c2dd');d.text((16,69),'Yellow outline = 32px sprite frame. Later retreat keeps the wider zoom; cinematic does not re-arm.',font=f,fill='#b4c2dd')
 for i,c in enumerate(selected):out.paste(panel(s,c,c['label']).resize((pw,ph),Image.Resampling.LANCZOS),(20+i*pw,110))
 out.save(root/(s['screen']['name']+'-journey.png'))
 if s['screen']['width']<s['screen']['height']:
  variants=[(s['normal'],'Native arrival'),(s['captures'][0],'Wider establishing view'),(s['readable'],'Readability-capped view')];pw=w;ph=h+70;out=Image.new('RGB',(pw*3+40,ph+126),'#0b101b');d=ImageDraw.Draw(out);d.text((16,12),s['screen']['name']+' | arrival composition comparison',font=big,fill='white');d.text((16,43),'Source-camera simulation with estimated phone UI reserves, not live HUD validation.',font=f,fill='#b4c2dd');d.text((16,69),'The readable crop shows less of the upper gate; the wider view briefly makes the avatar smaller.',font=f,fill='#b4c2dd')
  for i,(c,label) in enumerate(variants):out.paste(panel(s,c,label),(20+i*pw,110))
  out.save(root/(s['screen']['name']+'-arrival-options.png'))
print('Saved 5 journey filmstrips and 3 arrival comparisons.')
