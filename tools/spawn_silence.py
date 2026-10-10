"""Add and audit native spawn protection; source map geometry and assets stay unchanged.
Supports this project's finite orthogonal32px TMJs with classified rectangle starts
or ordinary named start tile layers. No engine, scripting or audio integration.
"""
from pathlib import Path
import argparse,copy,json,math

FOOT_OFFSET=16

def props(obj):return {p['name']:p['value']for p in obj.get('properties',[])}
def layers(items,dx=0,dy=0):
 for l in items:
  ox=dx+l.get('offsetx',0);oy=dy+l.get('offsety',0)
  yield l,ox,oy
  yield from layers(l.get('layers',[]),ox,oy)
def rect(o,dx=0,dy=0):return [o['x']+dx,o['y']+dy,o['width'],o['height']]
def inside(r,x,y):return r[0]<=x<=r[0]+r[2] and r[1]<=y<=r[1]+r[3]
def starts(m):
 if m.get('infinite',False) or m.get('orientation','orthogonal')!='orthogonal' or (m.get('tilewidth'),m.get('tileheight'))!=(32,32):raise ValueError('Only finite orthogonal 32px maps are supported')
 if any('source'in ts for ts in m.get('tilesets',[])):raise ValueError('External tilesets must be embedded before auditing property overrides')
 found=[];tw=m['tilewidth'];th=m['tileheight']
 for l,dx,dy in layers(m['layers']):
  for o in l.get('objects',[]):
   if (o.get('class')or o.get('type'))not in ('area','zone'):continue
   if o.get('name')!='start' and props(o).get('start')is not True:continue
   if o.get('rotation',0)or o.get('ellipse')or o.get('polygon'):raise ValueError('Unsupported non-rectangle start')
   x,y,w,h=rect(o,dx,dy)
   if min(w,h)<32:raise ValueError('Start area smaller than native inset')
   # MathUtils.randomFrom is integer inclusive, and area membership uses y+16.
   points=[(xx,yy+FOOT_OFFSET)for yy in range(math.ceil(y+16),math.floor(y+h-16)+1)for xx in range(math.ceil(x+16),math.floor(x+w-16)+1)]
   found.append({'id':o['id'],'name':o['name'],'kind':'classified-area','rect':[x,y,w,h],'footpoints':points})
  if l['type']=='tilelayer'and(l['name']=='start'or props(l).get('startLayer')is True):
   if not isinstance(l.get('data'),list):raise ValueError('Compressed/infinite start layer needs explicit expansion')
   for i,gid in enumerate(l['data']):
    if gid:found.append({'id':l['id'],'name':l['name']+'-cell-'+str(i),'kind':'tile-layer','footpoints':[((i%l['width']+l.get('x',0))*tw+tw/2+dx,(i//l['width']+l.get('y',0))*th+th/2+dy+FOOT_OFFSET)]})
 if not found:raise ValueError('Explicit supported start required; default center fallback is not accepted')
 return found

def silent_regions(m):
 result=[]
 if props(m).get('silent'):raise ValueError('Global map silence is not a scoped spawn fix')
 for l,dx,dy in layers(m['layers']):
  if props(l).get('silent'):raise ValueError('This checker requires classified quiet rectangles, not whole tile-layer silence')
  for o in l.get('objects',[]):
   if (o.get('class')or o.get('type'))in('area','zone')and props(o).get('silent')is True:result.append({'id':o['id'],'name':o['name'],'rect':rect(o,dx,dy)})
 return result

def audit(m):
 ss=starts(m);quiet=silent_regions(m);rows=[]
 conflicts=[]
 for l,_,_ in layers(m['layers']):
  if 'silent'in props(l):conflicts.append('layer:'+l['name'])
  for o in l.get('objects',[]):
   if 'silent'in props(o)and props(o)['silent']is not True:conflicts.append('area:'+o.get('name',''))
 for ts in m.get('tilesets',[]):
  for tile in ts.get('tiles',[]):
   if 'silent'in props(tile):conflicts.append('tileset:'+ts.get('name','')+':'+str(tile['id']))
 for s in ss:
  missing=[p for p in s['footpoints']if not any(inside(q['rect'],*p)for q in quiet)]
  rows.append({'name':s['name'],'kind':s['kind'],'possibleIntegerSpawns':len(s['footpoints']),'unprotectedSpawns':len(missing),'firstMissingFeet':missing[:3]})
 exits=[]
 for q in quiet:
  x,y,w,h=q['rect'];cy=y+h/2;cx=x+w/2
  samples=[(x-1,cy),(x+w+1,cy),(cx,y-1),(cx,y+h+1)]
  exits.append({'name':q['name'],'region':q['rect'],'outsideFootpoints':samples,'allOutsideSpawnSilence':all(not any(inside(z['rect'],*p)for z in quiet)for p in samples)})
 return {'nativeFootOffsetY':16,'areaBoundsInclusive':True,'starts':rows,'silentAreas':quiet,'exitBoundaryChecks':exits,'potentialSilentOverrides':conflicts,'allSpawnsProtected':all(not r['unprotectedSpawns']for r in rows)and not conflicts,'normalAreaStatusAfterExit':all(r['allOutsideSpawnSilence']for r in exits),'scope':'Map membership check only. Native listener returns OthersSilent=false when property becomes undefined. Saved user busy/silent status is not overridden; initial socket grouping is not tested.'}

def apply(m,padding=32):
 m=copy.deepcopy(m);ss=starts(m);layer=next((l for l in m['layers']if l['type']=='objectgroup'),None)
 if layer is None:raise ValueError('Expected existing top-level area layer')
 nextid=max([o['id']for l,_,_ in layers(m['layers'])for o in l.get('objects',[])]+[0])+1
 for s in ss:
  name='spawn-quiet-'+s['name'];xs=[p[0]for p in s['footpoints']];ys=[p[1]for p in s['footpoints']]
  x=max(0,math.floor((min(xs)-padding)/32)*32);y=max(0,math.floor((min(ys)-padding)/32)*32)
  right=min(m['width']*32,math.ceil((max(xs)+padding)/32)*32);bottom=min(m['height']*32,math.ceil((max(ys)+padding)/32)*32)
  layer['objects'].append({'id':nextid,'name':name,'class':'area','type':'area','visible':True,'x':x,'y':y,'width':right-x,'height':bottom-y,'properties':[{'name':'silent','type':'bool','value':True}]});nextid+=1
 m['nextobjectid']=nextid;return m
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('map');p.add_argument('--output');p.add_argument('--report');a=p.parse_args();m=json.loads(Path(a.map).read_text());before=audit(m)
 if a.output:m=apply(m);Path(a.output).write_text(json.dumps(m,separators=(',',':'))+'\n')
 report={'before':before,'after':audit(m)};payload=json.dumps(report,indent=2)+'\n'
 if a.report:Path(a.report).write_text(payload)
 print(payload)
 if not report['after']['allSpawnsProtected']:raise SystemExit(1)
