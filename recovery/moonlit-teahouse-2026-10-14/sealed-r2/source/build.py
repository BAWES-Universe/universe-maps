from pathlib import Path
from PIL import Image,ImageDraw
import json,math
R=Path(__file__).resolve().parents[1];O=R/'runtime';W,H,T=36,26,32
# Replay original procedural test artwork, stopping before its file-writing section.
ns={'__file__':str(R/'source'/'fixture-art-origin.py')}
exec((R/'source'/'fixture-art-origin.py').read_text().split('# Per-layer 32px atlas')[0],ns)
ims={}
base=Image.new('RGBA',(W*T,H*T));d=ImageDraw.Draw(base)
for y in range(H):
 for x in range(W):
  c=['#304a48','#344e4a'][(x+y)%2]
  if x>=25 and 8<=y<=20:c=['#a3a499','#b0afa0'][(x+y)%2]
  if 10<=x<=17 and y>=14:c=['#cbbd9d','#d5c8aa'][(x+y)%2]
  d.rectangle((x*T,y*T,x*T+31,y*T+31),fill=c)
base.alpha_composite(ns['ims']['ground']);d=ImageDraw.Draw(base)
# Extend the garden walk beyond the original fixture and connect an eastern terrace.
for y in range(22,H):
 for x in range(10,18):d.rectangle((x*T,y*T,x*T+31,y*T+31),fill=['#cbbd9d','#d5c8aa'][(x+y)%2])
for y in range(9,12):d.rectangle((23*T,y*T,28*T,y*T+31),fill='#e4d8be')
ims['ground']=base
frame=Image.new('RGBA',base.size);frame.alpha_composite(ns['ims']['persistent-glass-frame']);d=ImageDraw.Draw(frame)
# Clear an actual side opening; no door is advertised here.
d.rectangle((24*T,9*T,25*T-1,12*T-1),fill=(0,0,0,0))
for x,y in [(5,21),(21,21),(27,21),(32,21),(28,8),(33,8)]:
 d.ellipse((x*T,y*T,x*T+43,y*T+43),fill='#233d38',outline='#96ac7a',width=3)
for x in range(28,35):d.rectangle((x*T,2*T,x*T+31,7*T),fill='#264851')
# Terrace rail is visual and has matching permanent collision.
d.line((27*T,21*T,35*T,21*T),fill='#c2a668',width=6)
ims['persistent-glass-frame']=frame
# Original procedural furniture: reachable standing positions, not a sit API.
furniture=Image.new('RGBA',base.size);d=ImageDraw.Draw(furniture)
d.rounded_rectangle((6*T,8*T,9*T-1,9*T+18),radius=8,fill='#775646',outline='#d3b782',width=3)
d.rectangle((6*T+8,9*T+10,6*T+14,10*T),fill='#493f39');d.rectangle((9*T-14,9*T+10,9*T-8,10*T),fill='#493f39')
d.rounded_rectangle((18*T,9*T,19*T+12,10*T),radius=8,fill='#75958b',outline='#d4bd8b',width=3)
ims['furniture']=furniture
# Desk lip above body. Only a shallow 8px strip, never an invented head-height wall.
lip=Image.new('RGBA',base.size);ImageDraw.Draw(lip).rectangle((6*T,9*T+10,9*T-1,9*T+18),fill='#b49368');ims['desk-lip']=lip
for i in range(5):
 im=Image.new('RGBA',base.size);d=ImageDraw.Draw(im);shift=round(i*12)
 for a in [13*T-shift,14*T+shift]:
  d.rectangle((a,11*T,a+31,14*T-1),fill=(73,139,150,175),outline='#e1bc71',width=3)
  d.line((a+6,11*T+9,a+23,14*T-12),fill=(224,251,240,190),width=2)
 ims['door-frame-'+str(i)]=im
roof=Image.new('RGBA',base.size);d=ImageDraw.Draw(roof)
d.polygon([(3*T,7*T),(14*T,5*T),(25*T,7*T),(24*T,12*T),(4*T,12*T)],fill=(39,69,74,255),outline='#b49e73')
for x in range(4,25):d.line((x*T,7*T,x*T,12*T),fill='#547876',width=2)
ims['roof']=roof
layers=[];tilesets=[];first=1
for name,im in ims.items():
 atlas=Image.new('RGBA',(512,math.ceil(W*H/16)*T));data=[]
 for y in range(H):
  for x in range(W):
   idx=y*W+x;tile=im.crop((x*T,y*T,(x+1)*T,(y+1)*T));atlas.paste(tile,((idx%16)*T,(idx//16)*T));data.append(first+idx if tile.getbbox() else 0)
 atlas.save(O/(name+'.png'));tilesets.append({'firstgid':first,'name':name,'image':name+'.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'columns':16,'tilecount':W*H});first+=W*H
 layers.append({'name':name,'type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':not name.startswith('door-frame-') or name=='door-frame-4','data':data})
# Native transparent collision carrier. Its visibility controls physics, not image alpha.
Image.new('RGBA',(32,32)).save(O/'collision.png');collision=first
# Reuse its same transparent tile for full-coverage audio metadata.
tilesets.append({'firstgid':first,'name':'collision','image':'collision.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':1,'tilecount':1,'tiles':[{'id':0,'properties':[{'name':'collides','type':'bool','value':True}]}]});first+=1
def layer(name,cells,visible=True,properties=None):return {'name':name,'type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':visible,'data':[collision if (x,y) in cells else 0 for y in range(H) for x in range(W)],'properties':properties or []}
wall={(x,y) for y in range(H) for x in range(W) if x in [0,W-1] or y in [0,H-1] or (y<7 and x<=24) or (y==13 and 3<=x<=24 and x not in [13,14]) or (x==3 and 7<=y<=13) or (x==24 and 7<=y<=13 and y not in [9,10,11]) or (27<=x<=34 and 2<=y<=7) or (y==21 and 27<=x<=34) or (6<=x<=8 and y==8)}
layers+=[layer('permanent-collision',wall),layer('door-collision',{(13,13),(14,13)},False)]
# Audio metadata tile must NOT inherit collision properties.
tilesets.append({'firstgid':first,'name':'metadata','image':'collision.png','imagewidth':32,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':1,'tilecount':1});meta=first;first+=1
layers.append({'name':'native-audio','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':[meta]*(W*H)})
# Four original native32 ripple frames, code-authored technical animation, 720ms loop.
water=Image.new('RGBA',(128,32));d=ImageDraw.Draw(water)
for i in range(4):
 x=i*32;d.rectangle((x,0,x+31,31),fill='#244f5c');d.arc((x+2-i,7-i,x+29+i,25+i),180,355,fill='#75bac2',width=2);d.line((x+5+i,5,x+13+i,5),fill='#a3d5cc',width=1)
water.save(O/'water-motion.png');tilesets.append({'firstgid':first,'name':'water-motion','image':'water-motion.png','imagewidth':128,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':4,'tilecount':4,'tiles':[{'id':0,'animation':[{'tileid':i,'duration':180} for i in range(4)]}]})
layers.append({'name':'water-motion','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':[first if 28<=x<=33 and 3<=y<=6 else 0 for y in range(H) for x in range(W)]})
roof_layer=next(l for l in layers if l['name']=='roof');layers.remove(roof_layer);lip_layer=next(l for l in layers if l['name']=='desk-lip');layers.remove(lip_layer)
objects=[{'id':1,'name':'start','type':'area','class':'area','x':13*T,'y':22*T,'width':64,'height':32,'properties':[{'name':'start','type':'bool','value':True}]},{'id':2,'name':'doorOpen','type':'variable','class':'variable','point':True,'x':32,'y':32,'properties':[{'name':'default','type':'bool','value':True},{'name':'persist','type':'bool','value':False}]}]
layers.append({'name':'floorLayer','type':'objectgroup','objects':objects,'visible':True,'opacity':1,'x':0,'y':0});layers.append(lip_layer)
for i in range(1,5):layers.append(dict(roof_layer,name='roof-alpha-'+str(i),opacity=i/4,visible=False))
for i,l in enumerate(layers):l['id']=i+1
m={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','infinite':False,'width':W,'height':H,'tilewidth':T,'tileheight':T,'nextlayerid':len(layers)+1,'nextobjectid':3,'layers':layers,'tilesets':tilesets,'properties':[{'name':'script','type':'string','value':'moonlit.js'},{'name':'mapName','type':'string','value':'Moonlit Tea House - isolated technical prototype'}]}
(O/'moonlit.tmj').write_text(json.dumps(m,indent=2))
# Actual TMJ decoder, not an independent concept rendering.
for state in ['open-cutaway','closed-qa','roof-exterior']:
 out=Image.new('RGBA',base.size);loaded={s['firstgid']:Image.open(O/s['image']).convert('RGBA') for s in tilesets}
 for l in layers:
  if l['type']!='tilelayer':continue
  show=l['visible'];name=l['name']
  if name.startswith('door-frame-'):show=name==('door-frame-0' if state=='closed-qa' else 'door-frame-4')
  if name.startswith('roof-alpha-'):show=state=='roof-exterior' and name=='roof-alpha-4'
  if not show:continue
  for index,gid in enumerate(l['data']):
   if not gid:continue
   s=next(s for s in reversed(tilesets) if s['firstgid']<=gid);n=gid-s['firstgid'];sx=n%s['columns']*T;sy=n//s['columns']*T;tile=loaded[s['firstgid']].crop((sx,sy,sx+T,sy+T))
   if l['opacity']!=1:tile.putalpha(tile.getchannel('A').point(lambda a:round(a*l['opacity'])))
   out.alpha_composite(tile,((index%W)*T,(index//W)*T))
 out.save(R/'renders'/(state+'.png'))
print('Built moonlit.tmj, 5 door states, 4 roof alpha states, native ripple animation and static decoded review renders')
