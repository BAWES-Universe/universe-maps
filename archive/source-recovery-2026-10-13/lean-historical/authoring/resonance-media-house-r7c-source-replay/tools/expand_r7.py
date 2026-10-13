from build_maps import *
import copy
P=R/'r6-preserved';old=json.loads((P/'source/layout.json').read_text());DX,DY=128,96
m=Map('resonance-media-house','Resonance Media House - expanded garden court',1024,896,old['category'],old['style'])
# Generated exterior is a new asset; authorized source-composition restores all approved r6 pixels exactly.
m.base=rgba(S/'r7-exterior-generated.png')
assert m.base.size==(1024,896),m.base.size
m.base.paste(rgba(P/'source/runtime-base.png').crop((0,80,768,608)),(DX,DY+80))
m.above.paste(rgba(P/'source/runtime-above.png').crop((0,80,768,608)),(DX,DY+80))
m.grid=np.pad(np.array(old['grid'],np.uint8),((3,6),(4,4)),constant_values=1)
m.quiet=np.pad(np.array(old['quiet'],np.uint8),((3,6),(4,4)),constant_values=0)
m.spawn=(old['start'][0]+DX,old['start'][1]+DY)
m.anchors=copy.deepcopy(old['anchors']);m.areas=copy.deepcopy(old['areas']);m.fixtures=copy.deepcopy(old['protectedFixtures']);m.objects=copy.deepcopy(old['objects'])
for a in m.anchors+m.areas:a['x']+=DX;a['y']+=DY
for f in m.fixtures:
 x,y,x2,y2=f['solidXYXY'];f['solidXYXY']=[x+DX,y+DY,x2+DX,y2+DY]
for obj in m.objects:
 if 'xy' in obj:obj['xy']=[obj['xy'][0]+DX,obj['xy'][1]+DY]
 if obj.get('collision'):
  x,y,x2,y2=obj['collision'];obj['collision']=[x+DX,y+DY,x2+DX,y2+DY]
# Exterior floor authoring is deliberately conservative and reviewed against the new art.
for box in [(64,128,96,832),(928,128,960,832),(64,128,960,160),(64,672,960,704),(448,704,576,896),(64,800,960,832)]:m.rect(box,False)
for id,x,y in [('court-west',240,687),('court-east',784,687),('garden-south',512,847),('west-side-south',80,591),('west-side-north',80,207),('rear-west',144,143),('rear-center',512,143),('rear-east',880,143),('east-side-north',944,207),('east-side-south',944,591),('bench-west-approach',240,815),('bench-east-approach',784,815),('west-path-termination',80,143),('east-path-termination',944,143)]:m.anchor(id,x,y,'north','landmark')
for name,box in [('west-bench-and-planters',(112,704,384,800)),('east-bench-and-planters',(640,704,912,800)),('west-bottom-garden',(96,832,448,896)),('east-bottom-garden',(576,832,928,896)),('west-path-termination-planter',(64,64,96,128)),('east-path-termination-planter',(928,64,960,128))]:m.protect(name,box)
from repair_chair_depth import repair
chair_exceptions=repair(m)
# Exact independent-review delta: twelve unambiguously clear courtyard cells.
for b in [(384,704,448,800),(576,704,640,800)]:m.rect(b,False)
m.base.save(m.r/'source/runtime-base.png');m.above.save(m.r/'source/runtime-above.png')
jw(m.r/'source/layout.json',dict(title=m.title,category=m.category,style=m.style,world=[m.W,m.H],start=m.spawn,grid=m.grid.tolist(),quiet=m.quiet.tolist(),anchors=m.anchors,areas=m.areas,objects=m.objects,protectedFixtures=m.fixtures,visualSeats=old['visualSeats']))
m.compile();m.validate();m.render()
# Preserve the established, provenance-tracked native32 occupant proof without needing raw sprite redistribution.
# Occupied output is decoded from current TMJ by render_runtime_proofs.py; no old occupied image is pasted.
import subprocess,sys
subprocess.run([sys.executable,str(R/'tools/render_runtime_proofs.py')],check=True)
proof=rgba(m.r/'review/empty-native.png').crop((DX,DY+80,DX+768,DY+608));baseline=rgba(P/'review/empty-native.png').crop((0,80,768,608));diff=np.any(np.array(proof)!=np.array(baseline),axis=2);allowed=np.zeros(diff.shape,bool)
for x0,y0,x1,y1 in chair_exceptions:allowed[max(0,y0-DY-80):y1-DY-80,max(0,x0-DX):x1-DX]=True
assert not (diff & ~allowed).any()
jw(m.r/'validation/r6-preservation.json',dict(originalWorld=[768,608],expandedWorld=[1024,896],offset=[DX,DY],preservedR6Rect=[0,80,768,608],preservedExtentPixels=768*528,preservedPixelCount=768*528-int(diff.sum()),approvedInteriorRect=[0,96,768,608],byteExactOutsideChairCorrections=True,changedInteriorPixels=int(diff.sum()),chairExceptionRects=chair_exceptions,interiorScale=1,wokaScale=1,nativeAvatar=[32,32],r6SourceSHA256=hashlib.sha256((P/'review/empty-native.png').read_bytes()).hexdigest()))
print('Approved interior preserved outside ten explicit seat corrections; offset',DX,DY)
