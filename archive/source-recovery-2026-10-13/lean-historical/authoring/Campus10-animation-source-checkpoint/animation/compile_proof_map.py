"""Bounded offline proof only. Stores vector overlay native tiles, reuses original09 static atlases by relative reference."""
from PIL import Image
from pathlib import Path
import json,math,collections,hashlib,os
R=Path('/workspace/shared/magical-campus-standard32-09/map32'); O=Path(__file__).parent; M=O/'proof-map';M.mkdir(exist_ok=True);spec=json.loads((O/'effects/effects.json').read_text());m=json.loads((R/'magical-campus.tmj').read_text());T=32; C=m['width'];N=m['height'];W=C*T;H=N*T; sets=m['tilesets']; audits=[]
for ts in sets:ts['image']=os.path.relpath(R/ts['image'],M)
layers=[l for l in m['layers'] if l['name']!='campus-native-effects'];below=[0]*(C*N);above=[0]*(C*N);gid=max(ts['firstgid']+ts['tilecount'] for ts in sets)
for e in spec['effects']:
 x,y=e['origin'];w,h=e['size'];ex=x//T*T;ey=y//T*T;ew=math.ceil((x-ex+w)/T)*T;eh=math.ceil((y-ey+h)/T)*T;frames=[]
 for f in e['frames']:
  im=Image.new('RGBA',(ew,eh));im.paste(Image.open(O/f).convert('RGBA'),(x-ex,y-ey));frames.append(im)
 groups=[]
 for yy in range(0,eh,T):
  for xx in range(0,ew,T):
   parts=[im.crop((xx,yy,xx+T,yy+T)) for im in frames]
   if all(p.getchannel('A').getbbox() is None for p in parts):continue
   if len({p.tobytes() for p in parts})==1:continue
   groups.append({'cell':((ey+yy)//T)*C+(ex+xx)//T,'parts':parts})
 pages=[];current=[];seen=set();budget=0
 for g in groups:
  unique={p.tobytes() for p in g['parts']};cost=len(unique-seen)+1
  if current and budget+cost>1024:pages.append(current);current=[];seen=set();budget=0;cost=len(unique)+1
  current.append(g);seen|=unique;budget+=cost
 if current:pages.append(current)
 for page,groups0 in enumerate(pages):
  tiles=[];lookup={};animations=[];data=above if e['layer']=='above' else below
  for g in groups0:
   root=len(tiles);tiles.append(g['parts'][0]);ids=[]
   for part in g['parts']:
    b=part.tobytes()
    if b not in lookup:lookup[b]=len(tiles);tiles.append(part)
    ids.append(lookup[b])
   animations.append({'id':root,'animation':[{'tileid':f,'duration':e['duration']} for f in ids]});assert data[g['cell']]==0;data[g['cell']]=gid+root
  cols=min(32,len(tiles));rows=math.ceil(len(tiles)/cols);atlas=Image.new('RGBA',(cols*T,rows*T))
  for i,tile in enumerate(tiles):atlas.paste(tile,((i%cols)*T,(i//cols)*T))
  name=e['name']+f'-native-p{page}';atlas.save(M/f'{name}.png');sets.append({'firstgid':gid,'name':name,'image':f'{name}.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':T,'tileheight':T,'margin':0,'spacing':0,'columns':cols,'tilecount':len(tiles),'tiles':animations});gid+=len(tiles);audits.append({'effect':e['name'],'page':page,'tileCountIncludingRoots':len(tiles),'animatedCells':len(groups0),'atlasSize':list(atlas.size),'atlasBytes':(M/f'{name}.png').stat().st_size})
def layer(name,data):return {'name':name,'type':'tilelayer','width':C,'height':N,'x':0,'y':0,'visible':True,'opacity':1,'data':data}
layers.insert(1,layer('campus-native-effects',below));layers.insert(next(i for i,l in enumerate(layers) if l['name']=='campus-above')+1,layer('campus-native-above-effects',above))
for i,l in enumerate(layers):l['id']=i+1
m['layers']=layers;m['tilesets']=sets;m['nextlayerid']=len(layers)+1;m['properties']=[{'name':'offlineProofOnly','type':'bool','value':True}];(M/'magical-campus.tmj').write_text(json.dumps(m,separators=(',',':'))+'\n');(O/'proof/tile-budget.json').write_text(json.dumps(audits,indent=2)+'\n');print(json.dumps(audits,indent=2))
# Independent ordinary-TMJ renderer resolves animation tile IDs/duration from the generated file.
m=json.loads((M/'magical-campus.tmj').read_text()); atlases=[(ts,Image.open(M/ts['image']).convert('RGBA'),{a['id']:a['animation'] for a in ts.get('tiles',[]) if 'animation'in a}) for ts in m['tilesets']]
def render(box,time):
 l,t,r,b=box;out=Image.new('RGBA',(r-l,b-t),(12,32,41,255))
 for ly in m['layers']:
  if ly['type']!='tilelayer' or ly.get('opacity',1)==0 or not ly.get('visible',True):continue
  lim=Image.new('RGBA',out.size)
  for y in range(t//T,min(N,math.ceil(b/T))):
   for x in range(l//T,min(C,math.ceil(r/T))):
    g=ly['data'][y*C+x]
    if not g:continue
    ts,atlas,anim=next(s for s in reversed(atlases) if g>=s[0]['firstgid']);idx=g-ts['firstgid'];assert idx<ts['tilecount']
    if idx in anim:
     seq=anim[idx];q=time%sum(f['duration'] for f in seq)
     for f in seq:
      if q<f['duration']:idx=f['tileid'];break
      q-=f['duration']
    cols=ts['columns'];tile=atlas.crop((idx%cols*T,idx//cols*T,(idx%cols+1)*T,(idx//cols+1)*T));lim.paste(tile,(x*T-l,y*T-t))
  out.alpha_composite(lim)
 return out.convert('RGB')
for e in spec['effects']:
 x,y=e['origin'];w,h=e['size'];post=[render((x,y,x+w,y+h),k*e['duration']) for k in range(len(e['frames']))]
 for k in [0,3,7]:
  source=Image.open(O/f'proof/{e["name"]}-t{k*e["duration"]:04}-native.png').convert('RGB');assert source.tobytes()==post[k].tobytes(),e['name']
 post[0].save(O/f'proof/{e["name"]}-tmj-native-timed.png',save_all=True,append_images=post[1:],duration=e['duration'],loop=0)
 pal=Image.new('RGB',(w,h*len(post)))
 for i,im in enumerate(post):pal.paste(im,(0,h*i))
 palette=pal.quantize(colors=256);g=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in post];g[0].save(O/f'proof/{e["name"]}-tmj-native-timed.gif',save_all=True,append_images=g[1:],duration=e['duration'],loop=0,disposal=2,optimize=False)
proof={'mapSha256':hashlib.sha256((M/'magical-campus.tmj').read_bytes()).hexdigest(),'ordinaryTiledAnimationReferencesValid':True,'sampledNativeSourceToTmjPixelsIdentical':True,'sourcePhysicsAndCoordinatesPreserved':True,'sourceStaticImagesExternalReadOnly':str(R),'newAtlasPages':len(audits),'newAtlasBytes':sum(a['atlasBytes'] for a in audits),'newTilesIncludingRoots':sum(a['tileCountIncludingRoots'] for a in audits),'browserUsed':False,'finalCampus10Composition':False};(O/'proof/tmj-verification.json').write_text(json.dumps(proof,indent=2)+'\n')
