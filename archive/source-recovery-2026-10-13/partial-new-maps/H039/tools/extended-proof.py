from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/design.json').read_text());L=json.loads((R/'source/layout.json').read_text());G=L['collision'];geometry=json.loads((R/'validation/geometry.json').read_text());assert geometry['headConflicts']==0;assert geometry['foregroundExcludedForHeadSafety']==0
bands=D['fullWidthBands']
def body(x,y):return all(G[yy][xx]==0 for yy in range(math.floor(y/32),math.floor((y+16-1e-7)/32)+1)for xx in range(math.floor((x-8)/32),math.floor((x+8-1e-7)/32)+1))
rows=[]
for b in bands:
 x0,y0,x1,y1=b['bounds'];bad=[];n=0
 for y in range(y0,y1+1):
  for x in range(x0,x1+1):
   n+=1
   if not body(x,y):bad.append([x,y])
 rows.append(dict(name=b['name'],bodyOriginRectangle=b['bounds'],samples=n,pass_=not bad,firstFailure=bad[:1]))
assert all(r['pass_']for r in rows),rows
boundary=[]
for y,row in enumerate(G):
 for x,b in enumerate(row):
  if b and any(0<=xx<len(row)and 0<=yy<len(G)and not G[yy][xx]for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):boundary.append([x,y])
contourRows=[]
for c in D['fixtureContours']:
 x0,y0,x1,y1=c['bounds'];cells=sorted(set((x//32,y//32)for y in range(y0,y1)for x in range(x0,x1)));bad=[[x,y]for x,y in cells if G[y][x]==0];contourRows.append(dict(name=c['name'],bounds=c['bounds'],cells=cells,openCells=bad))
assert all(not r['openCells']for r in contourRows),contourRows
out=dict(scope='Author source/static audit only. Explicit floor-width bands and complete projected fixture silhouettes; partial32px cells are blocked at real foliage/wall/rail/foot edges, never a generic extra padding band.',fullWidthBands=rows,borderingBlockedCells=boundary,boundaryCellCount=len(boundary),groundContours=contourRows,headSemantic='Only central3px front stool aprons are foreground-owned. No head clipping; complete opaque ground remains under them. All taller hard fixtures and bridge rails have their full projected silhouettes away from reachable walking origins.',pass_=True)
(R/'validation/full-width-and-contours.json').write_text(json.dumps(out,indent=2)+'\n')
# Every blocked frontier tile is displayed beside its labeled native source crop.
im=Image.open(R/'review/decoded-art.png').convert('RGBA');sheet=Image.new('RGB',(960,math.ceil(len(boundary)/10)*84),'#263330');dr=ImageDraw.Draw(sheet)
for i,(x,y)in enumerate(boundary):
 crop=im.crop((x*32,y*32,x*32+32,y*32+32)).resize((64,64),Image.Resampling.NEAREST);xx=(i%10)*96;yy=(i//10)*84;sheet.paste(crop,(xx,yy));dr.text((xx,yy+65),f'{x},{y} blocked',fill='white')
sheet.save(R/'review/every-blocked-frontier.png')
# Static scales of actual occupied stools and bridge stay opaque; not GPU proof.
im=Image.open(R/'review/occupied-native-arrival.png').convert('RGBA');scales=[];sheet=Image.new('RGB',(1200,960),'#24332b');dr=ImageDraw.Draw(sheet)
for j,b in enumerate([(224,432,300,500),(512,432,588,500),(680,368,1040,456)]):
 for i,z in enumerate([.75,1,1.25,1.5,2]):
  crop=im.crop(b);sz=(round(crop.width*z),round(crop.height*z));scaled=crop.resize(sz,Image.Resampling.NEAREST if float(z).is_integer()else Image.Resampling.LANCZOS);scales.append(dict(crop=j,scale=z,pixelSize=sz,opaque=scaled.getchannel('A').getextrema()==(255,255),rgbaSHA256=hashlib.sha256(scaled.tobytes()).hexdigest()));thumb=scaled.copy();thumb.thumbnail((230,250));sheet.paste(thumb,(i*240,j*300+24));dr.text((i*240,j*300+4),f'Object{j}, static{z}x',fill='white')
sheet.save(R/'review/static-scales.png');(R/'validation/static-scales.json').write_text(json.dumps(dict(scope='Deterministic source resampling only, not GPU camera/mobile acceptance.',scales=scales,allOpaque=all(x['opaque']for x in scales)),indent=2)+'\n');assert all(x['opaque']for x in scales)
print(json.dumps(dict(widthBands=len(rows),boundaryCells=len(boundary),contours=len(contourRows),pass_=True)))
