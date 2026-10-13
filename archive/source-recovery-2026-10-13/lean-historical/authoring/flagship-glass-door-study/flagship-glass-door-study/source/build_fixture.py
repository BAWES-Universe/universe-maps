from PIL import Image,ImageDraw
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]; O=R/'map32'; W,H,T=28,22,32
ims={}
def canvas():return Image.new('RGBA',(W*T,H*T))
base=canvas();d=ImageDraw.Draw(base);d.rectangle((0,0,W*T,H*T),fill='#152d35')
for y in range(H):
 for x in range(W):
  col=('#e9dec6' if (x+y)%2 else '#e4d8be') if 3<=x<=24 and 7<=y<=13 else ('#405e59' if (x+y)%2 else '#45635d')
  if 10<=x<=17 and y>=14:col='#cbbd9d' if (x+y)%2 else '#d5c8aa'
  d.rectangle((x*T,y*T,(x+1)*T-1,(y+1)*T-1),fill=col)
ims['ground']=base
shell=canvas();d=ImageDraw.Draw(shell)
# Persistent double-height rear glazing; all sprites remain BELOW floorLayer/avatar depth.
for x in range(3,25,3):
 a=x*T;d.rectangle((a,2*T,a+3*T-5,7*T),fill=(73,141,152,180),outline='#d5b76b',width=3)
 d.line((a+8,2*T+15,a+70,6*T+20),fill=(211,247,238,150),width=4)
 d.line((a,4*T,a+3*T-5,4*T),fill='#d5b76b',width=3)
d.rectangle((3*T-5,2*T-10,25*T,2*T),fill='#e5c47c');d.rectangle((3*T-5,7*T-4,25*T,7*T+6),fill='#b59550')
# Slim side piers and low front glazing. Wide center clear portal.
for x in [3,24]:d.rectangle((x*T,7*T,x*T+22,14*T),fill='#c4aa72');d.rectangle((x*T+5,7*T,x*T+10,14*T),fill='#f0d9a1')
for a,b in [(4,12),(16,24)]:
 d.rectangle((a*T,11*T,b*T-1,14*T-1),fill=(86,165,172,105),outline='#c2a668',width=3)
 for x in range(a,b,2):d.line((x*T,11*T,x*T,14*T),fill='#c2a668',width=3)
# Side planting and benches on terrace (outside walking spine).
for x in [5,21]:
 d.rounded_rectangle((x*T,16*T,(x+2)*T,18*T),radius=10,fill='#233d38',outline='#b29864',width=3)
 for dx,dy in [(18,14),(43,21),(25,42)]:d.ellipse((x*T+dx-14,16*T+dy-14,x*T+dx+14,16*T+dy+14),fill='#739472')
ims['persistent-glass-frame']=shell
closed=canvas();d=ImageDraw.Draw(closed)
for a,b in [(13*T,14*T),(14*T,15*T)]:
 d.rectangle((a,11*T,b-1,14*T-1),fill=(73,139,150,175),outline='#e1bc71',width=3)
 d.line((a+6,11*T+9,b-8,14*T-12),fill=(224,251,240,190),width=2)
 d.rectangle((a+12,12*T+7,a+15,12*T+20),fill='#f4db9d')
ims['door-closed']=closed
opened=canvas();d=ImageDraw.Draw(opened)
for a in [12*T+12,15*T]:d.rectangle((a,11*T,a+18,14*T-1),fill=(82,166,173,150),outline='#e1bc71',width=3)
ims['door-open']=opened
# Per-layer 32px atlas; same logical coordinate grid, no enlarged map cells.
layers=[];tilesets=[];first=1
for n,im in ims.items():
 atlas=Image.new('RGBA',(512,((W*H+15)//16)*32));data=[];tiles=[]
 for y in range(H):
  for x in range(W):
   idx=y*W+x;tile=im.crop((x*32,y*32,x*32+32,y*32+32));atlas.paste(tile,((idx%16)*32,(idx//16)*32));data.append(first+idx if tile.getbbox() else 0)
   if n=='door-closed' and y==13 and x in [13,14]:tiles.append({'id':idx,'properties':[{'name':'collides','type':'bool','value':True}]})
 atlas.save(O/(n+'.png'));tilesets.append({'firstgid':first,'name':n,'image':n+'.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':32,'tileheight':32,'columns':16,'tilecount':W*H,'tiles':tiles});first+=W*H
 layers.append({'id':len(layers)+1,'name':n,'type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':n!='door-open','data':data})
# Hard perimeter and base glass line. Door closed layer owns only its two threshold cells.
cell=Image.new('RGBA',(32,32));cell.save(O/'collision.png');tilesets.append({'firstgid':first,'name':'collision','image':'collision.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':[{'name':'collides','type':'bool','value':True}]}]})
coll=[first if x in [0,W-1] or y in [0,H-1] or (y==13 and x not in [13,14]) or (y<7) or (x in [3,24] and 7<=y<=13) else 0 for y in range(H) for x in range(W)]
layers.append({'id':5,'name':'permanent-collision','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':coll})
objects=[{'id':1,'name':'start','type':'area','x':13*32,'y':19*32,'width':64,'height':32,'properties':[{'name':'start','type':'bool','value':True}]},{'id':2,'name':'doorstep-union','type':'area','x':12*32,'y':10*32,'width':128,'height':7*32},{'id':3,'name':'doorOpen','type':'variable','point':True,'x':32,'y':32,'properties':[{'name':'default','type':'bool','value':False},{'name':'persist','type':'bool','value':False}]}]
layers.append({'id':6,'name':'floorLayer','type':'objectgroup','objects':objects,'visible':True,'opacity':1,'x':0,'y':0})
m={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','infinite':False,'width':W,'height':H,'tilewidth':32,'tileheight':32,'nextlayerid':7,'nextobjectid':4,'layers':layers,'tilesets':tilesets,'properties':[{'name':'script','type':'string','value':'door.js'},{'name':'mapName','type':'string','value':'Flagship glass door study - isolated fixture'}]}
(O/'fixture.tmj').write_text(json.dumps(m,indent=2))
for state in ['closed','open']:
 out=Image.alpha_composite(ims['ground'],ims['persistent-glass-frame']);out=Image.alpha_composite(out,ims['door-'+state]);out.save(R/'renders'/('fixture-'+state+'.png'))
(R/'source'/'contract.json').write_text(json.dumps({'tileSize':32,'doorCells':[[13,13],[14,13]],'doorstepUnion': [384,320,128,224],'depth':'Every art layer is below floorLayer; no foreground head masks. Tall north glass remains visible.','scope':'Isolated study, no changes to approved stage or liked existing entry. Room variable sharing is prototype only; multiplayer occupancy arbitration still needs acceptance.','authoring':'Original procedural fixture artwork, not copied conference assets.'},indent=2))
