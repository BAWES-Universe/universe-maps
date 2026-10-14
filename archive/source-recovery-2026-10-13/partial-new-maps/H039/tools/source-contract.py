from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('static_model',R/'tools/author-static-model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=json.loads((R/'source/design.json').read_text());V=json.loads((R/'validation/state-layers.json').read_text());L=json.loads((R/'source/layout.json').read_text());names=[x['layer']for x in V['forms']];tmj=R/'runtime/map.tmj';obj,g,im,fg,layers,files=m.load_map(tmj);assert np.array_equal(g,np.array(L['collision'],bool));assert im.tobytes()==Image.open(R/'review/decoded-art.png').convert('RGBA').tobytes()
head=m.head_audit(g,fg,R/'source/native-head-union.json');assert head['pass'];rows=[]
for state in V['logicalViews']:
 shown=state['showLayers'];hidden=[n for n in names if n not in shown];o,grid,art,fore,ls,source=m.load_map(tmj,shown,hidden);same=np.array_equal(grid,g);actual=hashlib.sha256(art.tobytes()).hexdigest();assert same and actual==V['stateHashes'][state['name']];assert art.getchannel('A').getextrema()==(255,255);samples=[]
 for z in [.75,1,1.25,1.5,2]:
  scaled=art.resize((round(art.width*z),round(art.height*z)),Image.Resampling.NEAREST if float(z).is_integer()else Image.Resampling.LANCZOS);opaque=scaled.getchannel('A').getextrema()==(255,255);assert opaque;samples.append(dict(scale=z,opaque=opaque,rgbaSHA256=hashlib.sha256(scaled.tobytes()).hexdigest()))
 rows.append(dict(name=state['name'],gridEqual=same,decodedSHA256=actual,opaque=True,staticScales=samples))
zoom=m.zoom_checks(layers,im,R/'review');assert zoom['pass'];assert all(not r['transparent_pixels']for r in zoom['rows'])
# Each rectangular QA bound covers a disjoint actual walkable set; their union is exact.
Q=json.loads((R/'qa-spec.json').read_text());counts={};covered={}
for room in Q['rooms']:
 x0,y0,x1,y1=room['bounds'];cells=[]
 for y,row in enumerate(L['collision']):
  for x,b in enumerate(row):
   if not b and x0<=x*32+16<x1 and y0<=y*32+16<y1:cells.append([x,y]);covered.setdefault((x,y),[]).append(room['id'])
 counts[room['id']]=len(cells)
assert len(covered)==int((~g).sum()) and all(len(v)==1 for v in covered.values())
# The current original native scene, complete-body collision and border cells are drawn afresh.
art=Image.open(R/'source/mill-native.png').convert('RGBA');draw=ImageDraw.Draw(art)
for x in range(0,art.width,32):draw.line((x,0,x,art.height-1),fill='#dd5959')
for y in range(0,art.height,32):draw.line((0,y,art.width-1,y),fill='#dd5959')
for y,row in enumerate(L['collision']):
 for x,b in enumerate(row):draw.text((x*32+1,y*32+1),str(x)+','+str(y),fill='white',stroke_width=1,stroke_fill='black')
art.save(R/'review/grid-candidate.png')
report=dict(scope='Author rerun with a separately maintained actual-TMJ decoder and static toolkit functions. Every physical state, exact native integer head mask, opaque ground and six rational source sampling scales. No independent acceptance, GPU, browser, mobile or live claims.',sourceHashes=files,all64StateRows=rows,head=head,zoom=zoom,qaBoundCoverage=counts,disjointCoverage=len(covered),pass_=True)
(R/'validation/source-contract.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(states=len(rows),headConflicts=head['origins_with_any_foreground_alpha'],scales=len(zoom['rows']),exactQAcoverage=len(covered),pass_=True)))
