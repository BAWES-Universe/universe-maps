"""Isolated map-only boundary candidate; does not modify Bv2 or any game source."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,copy,shutil
R=Path(__file__).resolve().parents[1]; B=Path('/workspace/shared/gate-b-map-only-v2'); M=json.loads((R/'baseline/gate-b-v2.tmj').read_text())
O=R/'publish/public/butterfly-town/gate-b/v3';O.mkdir(parents=True,exist_ok=True)
# Preserve all authored scripts, audio, and original shared tilesets byte-for-byte.
for p in (B/'publish/public/butterfly-town/gate-b/v2').rglob('*'):
 if p.is_file() and p.name not in ('gate.tmj','README.md'):
  q=O/p.relative_to(B/'publish/public/butterfly-town/gate-b/v2');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.copytree(B/'dependencies',R/'dependencies',dirs_exist_ok=True)
# Entire 32px tile cells, never fractional per-object collision semantics.
rows={17:(12,17),18:(12,17),19:(12,17),20:(12,17),21:(11,18),22:(11,18),23:(11,18),24:(11,18),25:(11,18),26:(11,18),27:(10,19),28:(10,19),29:(10,19),30:(9,20),31:(9,20),32:(10,19),33:(10,19),34:(11,18),35:(11,18),36:(11,18),37:(11,18),38:(11,18),39:(10,19),40:(10,19),41:(10,19),42:(10,19),43:(10,19),44:(10,19)}
walk={(c,r)for r,(left,right)in rows.items()for c in range(left,right+1)}
# Transparent tile 2 has no collision. Layer-only silent property isolates arrival conversations;
# it does not set any music property and restores the native absence-of-silent value at exit.
silent={'id':55,'name':'spawn-silent-zone','type':'tilelayer','width':30,'height':45,'x':0,'y':0,'opacity':1,'visible':True,'properties':[{'name':'silent','type':'bool','value':True}],'data':[2 if 14<=i%30<=16 and 34<=i//30<=36 else 0 for i in range(1350)]}
M['layers'].insert(3,silent);M['nextlayerid']=57
for p in M['properties']:
 if p['name']=='campusVersion':p['value']='gate-b-v3-native-boundaries-32-review'
def with_mask(walk):
 m=copy.deepcopy(M);next(l for l in m['layers']if l['name']=='permanent-collisions')['data']=[0 if(i%30,i//30)in walk else 1 for i in range(1350)];return m
fallback=with_mask(walk);(R/'stairs-only').mkdir(exist_ok=True);(R/'stairs-only/gate.tmj').write_text(json.dumps(fallback,separators=(',',':'))+'\n')
# Two side floors, connected over the existing paving behind the foreground lamps and cypresses.
# Outer low lamp bases at (3,30) and (26,30) remain blocked.
walk|={(c,30)for c in range(2,28)if c not in(3,4,20,21,25,26)}
walk-={(20,30)}
walk|={(c,31)for c in range(2,28)}
m=with_mask(walk)
# Exact static ground pixels, extracted under silhouette masks. Original ground is untouched.
sets=m['tilesets'];ims={s['name']:Image.open((R/'dependencies/public/butterfly-town/gate-b/v3'/s['image']).resolve()).convert('RGBA')for s in sets}
ground=Image.new('RGBA',(960,1440));layer=next(l for l in m['layers']if l['name']=='gate-ground')
for i,gid in enumerate(layer['data']):
 ts=next(s for s in reversed(sets)if s['firstgid']<=gid);j=gid-ts['firstgid'];tile=ims[ts['name']].crop(((j%ts['columns'])*32,(j//ts['columns'])*32,(j%ts['columns']+1)*32,(j//ts['columns']+1)*32));ground.alpha_composite(tile,(i%30*32,i//30*32))
# Silhouettes traced in world coordinates around pre-existing art. Masks include no new colors.
polygons={
 'west-cypress':[(219,936),(216,943),(216,952),(212,958),(210,969),(204,974),(205,982),(201,986),(203,996),(200,1000),(204,1014),(207,1027),(213,1032),(214,1054),(222,1054),(225,1032),(231,1029),(237,1016),(239,1000),(235,990),(233,981),(232,974),(228,967),(226,955),(224,944)],
 'west-arrival-lamp':[(268,937),(265,947),(264,953),(257,957),(259,964),(257,976),(254,978),(254,982),(259,987),(260,992),(257,996),(251,998),(250,1005),(253,1009),(256,1012),(256,1059),(259,1062),(259,1072),(252,1076),(251,1084),(279,1086),(285,1081),(283,1076),(275,1071),(278,1065),(281,1062),(281,1011),(286,1008),(287,1002),(283,997),(276,994),(275,990),(278,986),(282,982),(282,977),(277,975),(278,960),(276,956),(272,954),(272,947)],
 'east-cypress':[(742,936),(739,945),(737,953),(734,955),(732,967),(727,974),(727,981),(722,988),(722,999),(719,1005),(722,1018),(725,1025),(732,1034),(736,1055),(745,1055),(747,1032),(754,1028),(758,1019),(760,1007),(755,997),(758,987),(753,979),(751,968),(748,961),(747,950)],
 'east-arrival-lamp':[(692,937),(689,948),(688,953),(681,958),(681,975),(678,978),(678,983),(683,987),(685,993),(679,996),(675,997),(673,1003),(675,1009),(680,1013),(680,1061),(683,1065),(685,1072),(677,1076),(677,1083),(704,1086),(710,1083),(709,1077),(701,1073),(703,1065),(706,1060),(705,1014),(710,1010),(712,1004),(709,998),(701,996),(698,992),(698,988),(703,985),(706,981),(705,977),(701,975),(701,960),(699,956),(696,953),(696,946)]}
mask=Image.new('L',ground.size);d=ImageDraw.Draw(mask)
for poly in polygons.values():d.polygon(poly,fill=255)
foreground=ground.copy();foreground.putalpha(mask);foreground.save(R/'results/foreground-cutout.png')
tiles=[];data=[0]*1350;first=max(s['firstgid']+s['tilecount']for s in sets)
for i in range(1350):
 x,y=i%30*32,i//30*32;t=foreground.crop((x,y,x+32,y+32))
 if t.getbbox():data[i]=first+len(tiles);tiles.append(t)
atlas=Image.new('RGBA',(256,((len(tiles)+7)//8)*32))
for i,t in enumerate(tiles):atlas.alpha_composite(t,(i%8*32,i//8*32))
(O/'tilesets').mkdir(exist_ok=True);atlas.save(O/'tilesets/gate-balcony-foreground.png')
m['tilesets'].append({'firstgid':first,'name':'gate-balcony-foreground','image':'tilesets/gate-balcony-foreground.png','imagewidth':atlas.width,'imageheight':atlas.height,'tilewidth':32,'tileheight':32,'columns':8,'tilecount':len(tiles),'margin':0,'spacing':0})
over={'id':56,'name':'gate-balcony-foreground','type':'tilelayer','width':30,'height':45,'x':0,'y':0,'opacity':1,'visible':True,'data':data}
index=next(i for i,l in enumerate(m['layers'])if l['name']=='floorLayer');m['layers'].insert(index+1,over)
(O/'gate.tmj').write_text(json.dumps(m,separators=(',',':'))+'\n')
(R/'results/boundary-design.json').write_text(json.dumps({'rows':rows,'stairsOnlyWalkableCells':sum(v==0 for v in fallback['layers'][0]['data']),'balconyWalkableCells':len(walk),'foregroundPolygons':polygons,'foregroundTiles':len(tiles),'silentBounds':[448,1088,544,1184],'baselinesUntouched':True},indent=2)+'\n')
print(json.dumps({'walkableCells':len(walk),'foregroundTiles':len(tiles),'candidate':str(O/'gate.tmj')}))
