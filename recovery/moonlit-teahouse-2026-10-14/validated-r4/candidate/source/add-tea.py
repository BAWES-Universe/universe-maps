"""Add only procedural tea layers/objects to an r3 map; reruns are idempotent."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];p=R/'runtime/moonlit.tmj';m=json.loads(p.read_text());W=m['width'];H=m['height']
m['layers']=[l for l in m['layers'] if not l['name'].startswith('tea-')];m['tilesets']=[t for t in m['tilesets'] if t['name']!='tea-ritual']
im=Image.new('RGBA',(128,32));d=ImageDraw.Draw(im)
# Original code-authored porcelain cup/saucer, two steam frames, brewing pot.
d.ellipse((3,22,28,28),fill='#c9ad78');d.ellipse((19,10,28,21),outline='#f4e3b9',width=3);d.rounded_rectangle((7,9,23,24),radius=4,fill='#f4e3b9');d.ellipse((7,7,23,13),fill='#855e3c',outline='#e7ce9b',width=2)
for i in range(2):
 x=32*(i+1)
 for offset in (9,19):d.line([(x+offset,28),(x+offset-3+i*3,21),(x+offset+2-i*3,14),(x+offset,7)],fill=(225,239,222,190),width=2)
d.ellipse((99,22,124,28),fill='#c9ad78');d.rounded_rectangle((101,9,120,25),radius=6,fill='#6f9690',outline='#e7ce9b',width=2);d.polygon([(118,13),(126,10),(121,20)],fill='#6f9690');d.ellipse((105,6,116,11),fill='#e7ce9b')
im.save(R/'runtime/tea-ritual.png')
gid=max(t['firstgid']+t['tilecount'] for t in m['tilesets'])
m['tilesets'].append({'firstgid':gid,'name':'tea-ritual','image':'tea-ritual.png','imagewidth':128,'imageheight':32,'tilewidth':32,'tileheight':32,'columns':4,'tilecount':4,'tiles':[{'id':1,'animation':[{'tileid':1,'duration':350},{'tileid':2,'duration':350}]}]})
# Before floorLayer: decorations never become collision or hide the player.
at=next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer')
for name,x,y,tile in [('tea-preparing',8,8,3),('tea-desk-cup',8,8,0),('tea-desk-steam',8,7,1),('tea-served-cup',31,12,0),('tea-served-steam',31,11,1)]:
 data=[0]*(W*H);data[y*W+x]=gid+tile;m['layers'].insert(at,{'name':name,'type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':False,'data':data});at+=1
floor=next(l for l in m['layers'] if l['name']=='floorLayer');floor['objects']=[o for o in floor['objects'] if not o['name'].startswith('tea-')]
for name,x,y in [('tea-desk-prompt',152,320),('tea-terrace-prompt',848,464)]:
 floor['objects'].append({'id':max(o['id'] for o in floor['objects'])+1,'name':name,'type':'','x':x,'y':y,'width':180,'height':96,'rotation':0,'visible':True})
for i,l in enumerate(m['layers']):l['id']=i+1
m['nextlayerid']=len(m['layers'])+1;m['nextobjectid']=max(o['id'] for o in floor['objects'])+1
p.write_text(json.dumps(m,indent=2))
print('Added local tea fixture layers and anchored prompts')
