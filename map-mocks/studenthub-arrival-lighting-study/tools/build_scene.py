"""Original, native-scale StudentHub Arrival scene. Blender offline authoring only."""
import bpy, math, random, json, sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]; (R/'renders').mkdir(exist_ok=True)
random.seed(41); W,H=1536,1152; UNIT=32; ZPX=32/math.sqrt(2)
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
DRAFT='--draft' in ARGS
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene; sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=64 if DRAFT else 96;sc.cycles.use_denoising=False;sc.cycles.seed=43
sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.045;sc.cycles.adaptive_min_samples=16;sc.cycles.max_bounces=6;sc.cycles.diffuse_bounces=3;sc.cycles.glossy_bounces=2;sc.cycles.transmission_bounces=2;sc.cycles.transparent_max_bounces=12;sc.cycles.caustics_reflective=False;sc.cycles.caustics_refractive=False;sc.cycles.sample_clamp_indirect=2
sc.render.resolution_x=W;sc.render.resolution_y=H;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
# A restrained renderer-native painterly reconstruction softens stochastic noise at1px without changing geometry.
sc.use_nodes=True;cn=sc.node_tree.nodes;cn.clear();rl=cn.new('CompositorNodeRLayers');ku=cn.new('CompositorNodeKuwahara');ku.variation='ANISOTROPIC';ku.inputs['Size'].default_value=1;co=cn.new('CompositorNodeComposite');sc.node_tree.links.new(rl.outputs['Image'],ku.inputs['Image']);sc.node_tree.links.new(ku.outputs['Image'],co.inputs['Image'])
sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.15,.40,.60,1);sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
G={k:[] for k in ['ground','base','foreground','glass','roof']};BROAD=[];FOOT=[];chairs=[]
def xy(x,y,z=0): return ((x-W/2)/UNIT,(H/2-y)/UNIT*math.sqrt(2),z/ZPX)
def mat(name,color,rough=.85,metal=0,texture=None,bump=.06):
 m=bpy.data.materials.new(name);m.use_nodes=True;ns=m.node_tree.nodes;ls=m.node_tree.links;p=ns.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 tc=ns.new('ShaderNodeTexCoord');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.68;ls.new(tc.outputs['Generated'],noise.inputs['Vector'])
 ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=tuple(c*.77 for c in color)+(1,);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=tuple(min(1,c*1.12) for c in color)+(1,);ls.new(noise.outputs['Fac'],ramp.inputs[0]);ls.new(ramp.outputs[0],p.inputs['Base Color'])
 if texture and (R/'art-source'/texture).exists():
  tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'art-source'/texture),check_existing=True);tex.projection='BOX';tex.projection_blend=.18;ls.new(tc.outputs['Generated'],tex.inputs['Vector']);mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.36;ls.new(ramp.outputs[0],mix.inputs[1]);ls.new(tex.outputs['Color'],mix.inputs[2]);ls.new(mix.outputs[0],p.inputs['Base Color'])
 bn=ns.new('ShaderNodeBump');bn.inputs['Strength'].default_value=.23;bn.inputs['Distance'].default_value=bump;ls.new(noise.outputs['Fac'],bn.inputs['Height']);ls.new(bn.outputs[0],p.inputs['Normal']);return m
stone=[mat('Limestone '+str(i),(.76+i*.004,.69+i*.004,.50+i*.003),texture='limestone.png') for i in range(8)]
pale=mat('Lime plaster',(.82,.77,.59),texture='limestone.png');stoneEdge=mat('Worn carved stone edge',(.84,.72,.44));grout=mat('Warm mortar',(.34,.31,.24));terra=[mat('Terracotta '+str(i),(.48+i*.03,.23+i*.02,.10+i*.012)) for i in range(4)]
teal=mat('Peacock painted timber',(.022,.25,.29),texture='teal.png');tealLight=mat('Teal edge highlight',(.075,.31,.31));ink=mat('Deep Universe ink',(.027,.07,.09));wood=mat('Warm honey oak',(.58,.34,.12),texture='oak.png');brass=mat('Aged warm brass',(.6,.36,.07),.42,.45);linen=mat('Natural linen',(.73,.66,.43),texture='linen.png');fabric=mat('Sage woven upholstery',(.20,.32,.24));rugMat=mat('Warm cream wool',(.64,.49,.29));rugBorder=mat('Faded muted teal weave',(.12,.29,.26));soil=mat('Deep planted loam',(.055,.075,.038));grass=mat('Ground moss',(.083,.15,.075));bark=mat('Old twisting bark',(.18,.09,.028));greens=[mat('Leaf '+str(i),c) for i,c in enumerate([(.07,.19,.07),(.13,.27,.09),(.19,.34,.11),(.24,.35,.12),(.055,.23,.16),(.22,.30,.15)])]
flowerM=[mat('Flower '+str(i),c) for i,c in enumerate([(.82,.51,.18),(.86,.75,.43),(.45,.23,.51),(.73,.25,.29),(.36,.46,.66)])]
water=mat('Teal fountain water',(.035,.33,.34),.7,0)
wn=water.node_tree.nodes;wl=water.node_tree.links;wp=wn.get('Principled BSDF');wt=wn.new('ShaderNodeTexImage');wt.image=bpy.data.images.load(str(R/'art-source'/'painted-water.png'),check_existing=True);wt.projection='BOX';wt.projection_blend=.05;wc=wn.new('ShaderNodeTexCoord');wl.new(wc.outputs['Generated'],wt.inputs['Vector']);wl.new(wt.outputs['Color'],wp.inputs['Base Color']);wl.new(wt.outputs['Color'],wp.inputs['Emission Color']);wp.inputs['Emission Strength'].default_value=.22
def glow(name,col,strength):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Emission Color'].default_value=(*col,1);p.inputs['Emission Strength'].default_value=strength;return m
amber=glow('Amber lantern glass',(1,.48,.09),3.5);foam=glow('Water glints',(.18,.51,.48),.12);screen=glow('Soft slate screen',(.05,.19,.22),.35)
glass=bpy.data.materials.new('Clear warm conservatory glazing');glass.use_nodes=True;n=glass.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.12;tr=n.new('ShaderNodeBsdfTransparent');p=n.new('ShaderNodeBsdfDiffuse');p.inputs['Color'].default_value=(.27,.72,.76,1);glass.node_tree.links.new(tr.outputs[0],mix.inputs[1]);glass.node_tree.links.new(p.outputs[0],mix.inputs[2]);glass.node_tree.links.new(mix.outputs[0],out.inputs[0])

def reg(o,name,material,group='base',broad=False):
 o.name=name;o.data.materials.append(material);G[group].append(o)
 if broad:BROAD.append(o)
 return o

def mesh_object(name,vs,fs,location,material,group,broad=False):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.location=location;return reg(o,name,material,group,broad)
def box(name,x,y,w,d,h,matr,z=0,group='base',bevel=1.3,broad=False):
 a,b,c=w/UNIT/2,d/UNIT*math.sqrt(2)/2,h/ZPX/2
 vs=[(-a,-b,-c),(a,-b,-c),(a,b,-c),(-a,b,-c),(-a,-b,c),(a,-b,c),(a,b,c),(-a,b,c)]
 fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 o=mesh_object(name,vs,fs,xy(x,y,z+h/2),matr,group,broad)
 if bevel:
  m=o.modifiers.new('soft worn edges','BEVEL');m.width=bevel/UNIT;m.segments=2;o.modifiers.new('weighted corner normals','WEIGHTED_NORMAL')
 return o
def cyl(name,x,y,r,h,matr,z=0,group='base',verts=32,broad=False):
 vs=[(r/UNIT*math.cos(i*math.tau/verts),r/UNIT*math.sqrt(2)*math.sin(i*math.tau/verts),zz) for zz in [-h/ZPX/2,h/ZPX/2] for i in range(verts)];fs=[tuple(reversed(range(verts))),tuple(range(verts,2*verts))]+[(i,(i+1)%verts,(i+1)%verts+verts,i+verts) for i in range(verts)]
 o=mesh_object(name,vs,fs,xy(x,y,z+h/2),matr,group,broad);m=o.modifiers.new('worn rims','BEVEL');m.width=.028;m.segments=2;return o
def sphere(name,x,y,z,rx,ry,rz,matr,group='base',broad=False):
 seg,rows=12,8;vs=[];fs=[]
 for j in range(rows+1):
  a=math.pi*j/rows
  for i in range(seg):
   b=math.tau*i/seg;vs.append((math.sin(a)*math.cos(b)*rx/UNIT,math.sin(a)*math.sin(b)*ry/UNIT*math.sqrt(2),math.cos(a)*rz/ZPX))
 for j in range(rows):
  for i in range(seg):fs.append((j*seg+i,j*seg+(i+1)%seg,(j+1)*seg+(i+1)%seg,(j+1)*seg+i))
 return mesh_object(name,vs,fs,xy(x,y,z),matr,group,broad)
def beam(name,a,b,r,matr,group='base',broad=False):
 aa=Vector(xy(*a));bb=Vector(xy(*b));v=bb-aa;seg=8;vs=[(r/UNIT*math.cos(i*math.tau/seg),r/UNIT*math.sin(i*math.tau/seg),z) for z in [-v.length/2,v.length/2] for i in range(seg)];fs=[tuple(reversed(range(seg))),tuple(range(seg,2*seg))]+[(i,(i+1)%seg,(i+1)%seg+seg,i+seg) for i in range(seg)]
 o=mesh_object(name,vs,fs,(aa+bb)/2,matr,group,broad);o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o
def ring(name,x,y,outer,inner,h,matr,z=0,group='base',start=0,end=2*math.pi,segments=64):
 vs=[];fs=[]
 for i in range(segments+1):
  a=start+(end-start)*i/segments
  for r,zz in [(outer,z),(inner,z),(outer,z+h),(inner,z+h)]:vs.append(xy(x+math.cos(a)*r,y+math.sin(a)*r,zz))
 for i in range(segments):
  a=i*4;b=(i+1)*4
  fs.extend([(a,b,b+2,a+2),(a+1,a+3,b+3,b+1),(a+2,b+2,b+3,a+3),(a,a+1,b+1,b)])
 fs.extend([(0,2,3,1),(segments*4,segments*4+1,segments*4+3,segments*4+2)])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);return reg(o,name,matr,group)
def arch(name,x,y,width,baseZ,rise,thickness,depth,material,group='foreground'):
 # An actual vertical architectural arch, not a ring lying on the ground.
 vs=[];fs=[];n=32
 for i in range(n+1):
  a=math.pi*i/n
  for rr,dy in [(width/2,-depth/2),(width/2-thickness,-depth/2),(width/2,depth/2),(width/2-thickness,depth/2)]:
   z=baseZ+math.sin(a)*rise*(rr/(width/2));vs.append(xy(x+math.cos(a)*rr,y+dy,z))
 for i in range(n):
  a=i*4;b=(i+1)*4;fs.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
 return mesh_object(name,vs,fs,(0,0,0),material,group)
def footprint(x,y,w,d,label):FOOT.append(dict(x=x-w/2,y=y-d/2,width=w,height=d,label=label))
def point(x,y,z,energy,color=(1,.52,.19),radius=.65):
 bpy.ops.object.light_add(type='POINT',location=xy(x,y,z));o=bpy.context.object;o.data.energy=energy;o.data.color=color;o.data.shadow_soft_size=radius;return o

def leafmesh(name,centers,group='foreground',broad=True):
 vs=[];fs=[];mi=[]
 for x,y,z,r,a,color in centers:
  idx=len(vs);c=Vector(xy(x,y,z));u=Vector((math.cos(a)*r/UNIT,math.sin(a)*r/UNIT*math.sqrt(2),0));v=Vector((-math.sin(a)*r*.42/UNIT,math.cos(a)*r*.42/UNIT*math.sqrt(2),r*.20/ZPX))
  for k in range(8):
   t=k*math.tau/8;vs.append(tuple(c+u*math.cos(t)+v*math.sin(t)))
  vs.append(tuple(c+Vector((0,0,r*.24/ZPX))))
  for k in range(8):fs.append((idx+k,idx+(k+1)%8,idx+8));mi.append(color)
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
 for m in greens:mesh.materials.append(m)
 for p,i in zip(mesh.polygons,mi):p.material_index=i;p.use_smooth=True
 G[group].append(o)
 if broad:BROAD.append(o)
 return o

def shrub(x,y,r=22,h=25,flowers=False,group='foreground'):
 cs=[]
 for i in range(int(r*8)):
  a=random.random()*math.tau;rr=r*math.sqrt(random.random());z=h*(.35+.65*math.sqrt(max(0,1-(rr/r)**2)))+random.uniform(-5,5);cs.append((x+math.cos(a)*rr,y+math.sin(a)*rr*.7,z,random.uniform(2.5,4.5),random.random()*math.tau,random.randrange(6)))
 leafmesh('Living planted border',cs,group)
 if flowers:
  for i in range(12):
   a=random.random()*math.tau;rr=r*.8*math.sqrt(random.random());xx=x+math.cos(a)*rr;yy=y+math.sin(a)*rr*.7;zz=h+random.uniform(-3,6)
   sphere('Flower head',xx,yy,zz,2.3,2.3,1.9,random.choice(flowerM),group)

def pot(x,y,r=15,h=23,flowers=True):
 cyl('Terracotta pot foot',x,y,r*.68,3,terra[1]);cyl('Terracotta planter',x,y,r,h,terra[2],z=3);ring('Rolled pot rim',x,y,r+2,r-1,3,terra[3],z=h+3);cyl('Pot soil',x,y,r-2,1,soil,z=h+3);shrub(x,y,r*1.45,h+22,flowers);footprint(x,y,r*1.4,r*1.25,'planter')

def tree(x,y,r=105,h=160):
 beam('Old tree trunk',(x,y,0),(x-7,y+1,h*.68),8,bark,broad=True);footprint(x,y,32,32,'tree trunk')
 centers=[]
 for branch in range(9):
  a=branch*math.tau/9+random.uniform(-.3,.3);rr=r*random.uniform(.5,.86);bx=x+math.cos(a)*rr;by=y+math.sin(a)*rr*.65;bz=h+random.uniform(-15,12)
  beam('Canopy branch',(x-5,y,h*.5),(bx,by,bz),3.2,bark,'foreground',True)
  for i in range(180):
   aa=random.random()*math.tau;rad=r*.5*math.sqrt(random.random());centers.append((bx+math.cos(aa)*rad,by+math.sin(aa)*rad*.55,bz+random.uniform(-14,18),random.uniform(3,6),random.random()*math.tau,random.randrange(6)))
 leafmesh('Tree leaves with actual cast shade',centers)

def lantern(x,y,z=30,post=True):
 if post:
  box('Lantern pier foot',x,y,22,22,5,stoneEdge);box('Lantern stone pier',x,y,15,15,z-4,pale,z=4);box('Pier capital',x,y,22,22,4,stoneEdge,z=z)
 box('Lantern warm glass',x,y,10,10,14,amber,z=z+6,bevel=1)
 for dx in [-6,6]:
  for dy in [-6,6]:beam('Lantern cage',(x+dx,y+dy,z+3),(x+dx,y+dy,z+23),.8,brass)
 cyl('Lantern cap',x,y,10,3,brass,z=z+22,verts=4);sphere('Lantern finial',x,y,z+28,2,2,3,brass)
 point(x,y,z+13,45,radius=.34)
 if post:footprint(x,y,22,22,'lantern pier')

def chair(x,y,face='north',label='chair'):
 # Seat positions are intentionally passable; only backrest's genuine pixels occlude an occupant.
 box(label+' seat',x,y,27,23,4,fabric,z=6,bevel=2)
 for dx in [-10,10]:
  for dy in [-8,8]:box(label+' leg',x+dx,y+dy,3,3,6,wood,bevel=.4)
 by=y+(10 if face=='north' else -10)
 grp='foreground' if face=='north' else 'base'
 box(label+' backrest',x,by,28,4,15,teal,z=10,group=grp,bevel=2)
 box(label+' back cushion',x,by-1 if face=='north' else by+1,23,2,10,fabric,z=12,group=grp,bevel=1.6)
 box(label+' brass back rail',x,by,24,5,1.2,brass,z=24,group=grp,bevel=.3)
 chairs.append(dict(x=x,y=y,face=face,occupied={'x':x,'y':y-15},label=label))
def table(x,y,w=112,d=58,label='Shared table'):
 top=25 if label=='Reception' else (12 if label=='Low tea table' else 17)
 box(label+' tabletop',x,y,w,d,4,wood,z=top,bevel=3)
 box(label+' apron',x,y,w-12,d-12,5,teal,z=top-5,bevel=.6)
 for dx in [-w/2+10,w/2-10]:
  for dy in [-d/2+8,d/2-8]:box(label+' leg',x+dx,y+dy,4,4,top-1,wood,bevel=.7)
 footprint(x,y,w-10,d-10,label)
def notebook(x,y,z=23):
 box('Notebook',x,y,12,16,1.2,linen,z=z,bevel=.3);box('Notebook binding',x-5,y,1,16,1.4,teal,z=z,bevel=.2)
def laptop(x,y,z=23):
 box('Slate laptop base',x,y,24,15,1.4,ink,z=z,bevel=1);box('Laptop display',x,y-6,24,2,15,teal,z=z+1,bevel=1);box('Laptop soft screen',x,y-7.2,20,.5,11,screen,z=z+3,bevel=.2)
def couch(x,y,w=112,face='south'):
 box('Sofa oak plinth',x,y,w,40,6,wood,z=4,bevel=2)
 for dx in [-w/2+9,w/2-9]:
  for dy in [-13,13]:box('Sofa little foot',x+dx,y+dy,5,5,6,wood,bevel=.7)
 for i in range(3):box('Sofa seat cushion',x-w/3+i*w/3,y,w/3-2,32,9,linen,z=10,bevel=4)
 by=y-17 if face=='south' else y+17;box('Sofa curved upholstered back',x,by,w,10,22,fabric,z=11,group='foreground' if face=='north' else 'base',bevel=5)
 for dx in [-w/2,w/2]:box('Sofa rounded arm',x+dx,y,10,44,16,fabric,z=8,bevel=4)
 for dx in [-w*.3,w*.3]:sphere('Handwoven pillow',x+dx,by+7 if face=='south' else by-7,24,12,5,10,linen)
 footprint(x,y,w+4,42,'sofa')
def glazing_h(x1,x2,y,h=64,group='glass'):
 box('Clear glass pane', (x1+x2)/2,y,x2-x1,1,h,glass,z=8,group=group,bevel=0)
 for x in range(int(x1),int(x2)+1,64):box('Slender teal mullion',x,y,3,5,h+8,teal,z=0,group=group,bevel=.3)
 box('Glass top rail',(x1+x2)/2,y,x2-x1+4,5,3,brass,z=h+7,group=group,bevel=.3);box('Glazing stone sill',(x1+x2)/2,y,x2-x1+8,10,8,stoneEdge,z=0)
def glazing_v(x,y1,y2,h=64):
 box('Clear side glass',x,(y1+y2)/2,1,y2-y1,h,glass,z=8,group='glass',bevel=0)
 for y in range(int(y1),int(y2)+1,64):box('Side glass slender frame',x,y,4,4,h+8,teal,group='glass',bevel=.3)
 box('Side glass top rail',x,(y1+y2)/2,4,y2-y1+4,3,brass,z=h+7,group='glass',bevel=.3);box('Side glazing sill',x,(y1+y2)/2,10,y2-y1,8,stoneEdge)

print('Scene materials ready',flush=True)
# Continuous planted estate ground, irregular details rather than tile stamps.
box('Continuous moss ground',768,576,1536,1152,3,grass,z=-4,group='ground',bevel=0)
# Main court and interior are one physically joined pale stone foundation.
box('Garden court foundation',768,882,928,408,8,stone[1],z=-8,group='ground',bevel=14)
box('Commons foundation',768,512,1056,512,8,stone[2],z=-8,group='ground',bevel=6)
# Stone bond is fine enough for Woka, irregular warm variation, no checker pattern.
for y in range(304,1073,24):
 for x in range(272,1280,32):
  xx=x+(16 if (y//24)%2 else 0)
  if (y<768 and 272<xx<1264) or (y>=768 and 336<xx<1200):box('Individually worn paving',xx,y,31,23,1.6,random.choice(stone),z=-.8,group='ground',bevel=.6)
# Broad path from threshold and restrained inset border.
for y in range(1072,1153,32):
 for x in [720,768,816]:box('Arrival stone',x,y,47,31,2,random.choice(stone),z=-1,group='ground',bevel=.6)
for x in [272,1264]:box('Foundation inset edge',x,512,12,492,3,stoneEdge,z=0,group='ground',bevel=1)
for y in [288,752]:box('Foundation edge band',768,y,1004,12,3,stoneEdge,z=0,group='ground',bevel=1)
# Pale architectural back wall with real thickness and rhythm.
box('Rear wall solid masonry',768,272,1024,24,70,pale,bevel=2)
box('Rear wall plinth',768,288,1028,12,12,stoneEdge,bevel=1)
box('Rear carved cornice',768,272,1040,34,8,stoneEdge,z=70,group='foreground',bevel=2)
for x in [272,464,656,848,1040,1264]:
 box('Masonry pilaster',x,285,20,28,76,stone[5],bevel=2)
 box('Pilaster capital',x,282,28,32,6,stoneEdge,z=74,group='foreground')
# Warm high arched windows; no giant opaque department facades.
for x in [368,560,752,944,1152]:
 box('Tall teal window recess',x,287,90,3,42,teal,z=24,bevel=2)
 box('Amber window interior',x,289,78,1,33,glass,z=29,group='base',bevel=0)
 for xx in [x-24,x,x+24]:box('Window muntin',xx,290,2,3,36,brass,z=27,bevel=.2)
 box('Window ledge',x,294,102,14,5,stoneEdge,z=21)
 arch('Carved arched window crown',x,295,103,55,31,5,8,stoneEdge,'base')
# A restrained carved roof-edge rhythm belongs to the building, in matching stone and brass.
for xx in range(288,1260,32):
 box('Roof edge carved dentil',xx,411,9,9,7,stoneEdge,z=44,group='roof',bevel=1)
# Structural posts preserve silhouette after roof is removed.
for x in [272,640,896,1264]:
 box('Front structural pier',x,752,22,24,65,pale,bevel=2);box('Pier foot',x,752,32,32,7,stoneEdge);box('Pier crown',x,752,32,30,7,stoneEdge,z=62,group='foreground')
 footprint(x,752,28,28,'front stone pier')
# A recognizable warm conservatory entrance, preserving the shared sightline.
for x in [688,848]:
 box('Entry column pedestal',x,752,33,30,9,stoneEdge);box('Entry carved shaft',x,752,19,21,82,pale,z=8,bevel=2)
 for z in [12,22,78,86]:box('Entry column moulding',x,752,26,26,3,stoneEdge,z=z,group='foreground',bevel=.8)
 footprint(x,752,32,32,'entry pier')
arch('Welcome sandstone arch',768,752,182,84,66,12,18,stoneEdge)
arch('Fine inner brass arch',768,758,155,85,52,2,5,brass)
for x in [460,1060]:arch('Glazed front bay arch',x,752,316,67,47,4,7,teal)
for x in [288,624,864,1248]:box('Front timber stile',x,752,7,10,72,teal,group='foreground',bevel=.8)
# Transparent frontage with generous direct main entry at704..832.
glazing_h(288,624,752);glazing_h(848,1248,752)
footprint(456,752,352,20,'front glass');footprint(1048,752,400,20,'front glass')
glazing_v(272,304,736);glazing_v(1264,304,736);footprint(272,520,20,448,'left glass');footprint(1264,520,20,448,'right glass');footprint(768,272,1056,32,'rear wall')
# Two low ornamental oak roof slopes: exported only to a removable cover group.
for y in range(292,409,18):
 for x in range(276,1260,32):
  z=88-(y-292)*.35
  box('Original teal roof shingle',x+(16 if (y//18)%2 else 0),y,31,22,3,teal,z=z,group='roof',bevel=1.1)
box('Roof ridge warm brass',768,280,1054,7,7,brass,z=94,group='roof')
# Fine inset border belongs to the floor material, not a separate carpet rectangle.
for xx in range(304,1240,24):
 for yy in [322,729]:
  ob=box('Small teal stone tessera',xx,yy,5,5,.3,teal,z=2,group='ground',bevel=.4);ob.rotation_euler.z=math.pi/4
# Six neighbors share one workbench edge, each chair naturally faces its own desk.
for idx,x in enumerate([352,448,544,704,800,896]):
 table(x,368,72,38,'Team station '+str(idx+1));laptop(x,360);notebook(x+22,368,23);chair(x,401,'north','Team chair '+str(idx+1))
# Compact nearby shared table, coherent opposing pairs.
table(784,560,128,58)
for x in [752,816]:chair(x,516,'south','North shared chair');chair(x,603,'north','South shared chair')
notebook(758,563,23);notebook(812,554,23);cyl('Water carafe',788,557,4,11,glass,z=30);cyl('Little table plant',785,569,5,8,terra[1],z=23)
# Cozy conversation pocket, rug ties furniture together.
box('Lounge rug border',440,609,232,166,1.3,rugBorder,z=1,group='ground',bevel=8);box('Lounge rug cream center',440,609,213,148,1.5,rugMat,z=1.3,group='ground',bevel=6)
for x in range(339,543,12):
 for yy in [531,687]:box('Rug tassel',x,yy,2,10,.5,linen,z=2,group='ground',bevel=.2)
couch(440,550,132,'south');couch(440,660,132,'north');table(440,606,64,34,'Low tea table')
for x in [424,446]:cyl('Tea cup',x,602,4,4,linen,z=17,verts=12)
notebook(454,611,17)
# Adjoining glass room with west doorway y528..592. All are a few steps away.
glazing_v(1008,448,528);glazing_v(1008,592,704);glazing_h(1008,1248,704);glazing_h(1008,1248,448)
footprint(1008,488,20,80,'meeting glass north segment');footprint(1008,648,20,112,'meeting glass south segment');footprint(1128,704,240,20,'meeting front glass');footprint(1128,448,240,20,'meeting back glass')
table(1128,561,104,54,'Glass room table')
for x in [1102,1154]:chair(x,518,'south','Meeting north chair');chair(x,608,'north','Meeting south chair')
notebook(1106,560,23);notebook(1150,565,23)
# Reception is beside arrival, not across it. Desk opening visible from shared room.
table(934,721,106,42,'Reception');box('Reception front teal panel',934,739,96,4,25,teal,z=3);box('Reception brass inset',934,742,80,1,2,brass,z=15);chair(934,676,'south','Reception chair');laptop(950,716,31);notebook(909,720,31)
# Lectern occupies a real focus edge; speaker approaches from north.
box('Presentation oak board',1175,326,106,7,55,wood,z=13);box('Presentation teal board',1175,331,93,2,42,teal,z=20)
for x in [1134,1216]:box('Board foot',x,336,7,20,5,wood)
box('Lectern pedestal',1152,390,32,26,22,teal);box('Lectern top ledge',1152,390,45,33,4,wood,z=22,group='foreground',bevel=2)
box('Lectern raised rim',1152,403,46,4,7,brass,z=24,group='foreground',bevel=.6);beam('Lectern microphone',(1166,381,25),(1162,377,40),.7,ink,'foreground');sphere('Microphone head',1162,377,40,2,2,2,ink,'foreground');footprint(1152,397,32,26,'lectern base')
# Indoor planting and lamps anchor the rooms to architecture.
for x,y in [(302,465),(602,466),(973,459),(1230,660)]:pot(x,y,13,18,False)
for x in [305,620,977,1230]:lantern(x,303,z=45,post=False)
for x in [669,867]:lantern(x,754,z=65,post=False)
# Beautiful composed garden edges: curved, layered, leaf detail and real stone returns.
for side in [-1,1]:
 cx=768+side*520
 ring('Garden visible loam',cx,906,178,143,2,soil,z=1,group='ground',start=(-.55 if side<0 else 2.05),end=(1.08 if side<0 else 3.7),segments=40)
 ring('Curved garden retaining wall',cx,906,146,135,16,stone[3],start=(-.55 if side<0 else 2.05),end=(1.08 if side<0 else 3.7),segments=40)
 for i in range(8):
  a=(-.5 if side<0 else 2.1)+i*.22;x=cx+math.cos(a)*158;y=906+math.sin(a)*158;shrub(x,y,29,31,i%2==0)
# Outer beds join the building base and sides; never broad walkable grass.
for x in range(320,1240,52):shrub(x,212,27,35,x%3==0)
for y in range(342,980,57):
 shrub(211,y,34,42,y%2==0);shrub(1330,y,38,43,y%3==0)
# Two real canopies frame the court and cast shade across walkable paving.
tree(332,862,105,153);tree(1240,920,93,150)
# Planter foundations are grounded and furnish collision only at bases.
for x,y in [(344,753),(600,773),(860,786),(1195,770),(684,1056),(855,1056)]:pot(x,y,17,24,True)
# Small surrounding sett circles bed the fountain into the court, rather than a disk pasted onto a grid.
for rr in [101,115,129]:
 count=round(math.tau*rr/18)
 for i in range(count):
  a=i*math.tau/count;xx=560+math.cos(a)*rr;yy=920+math.sin(a)*rr;ob=box('Fountain radial stone setts',xx,yy,16,11,2,stone[i%8],z=1,group='ground',bevel=.4);ob.rotation_euler.z=-a
# Off-axis warm fountain: concentric carved stone, luminous water, sculpted small jet.
fx,fy=560,920
cyl('Fountain lower step',fx,fy,98,5,stone[3]);ring('Fountain lower moulding',fx,fy,91,83,7,stoneEdge,z=5);cyl('Fountain pool under water',fx,fy,81,8,teal,z=5);cyl('Fountain living water',fx,fy,81,1,water,z=14);ring('Carved fountain coping',fx,fy,90,79,12,stone[5],z=12)
for i in range(32):
 a=i*math.tau/32;beam('Fountain coping joint',(fx+math.cos(a)*80,fy+math.sin(a)*80,25),(fx+math.cos(a)*90,fy+math.sin(a)*90,25),.35,grout)
cyl('Fountain pedestal',fx,fy,14,25,stoneEdge,z=14);ring('Fountain upper bowl',fx,fy,28,22,8,stone[4],z=39);cyl('Upper bowl water',fx,fy,22,1,water,z=45)
for i,r in enumerate([34,49,65,76]):
 for a,b in [(i*.7,i*.7+.9),(i*.7+2.4,i*.7+3.1)]:ring('Fine water ripple',fx,fy,r,r-.55,.2,foam,z=15.3,start=a,end=b,segments=20)
for i in range(8):
 a=i*math.tau/8;beam('Falling cascade',(fx+math.cos(a)*23,fy+math.sin(a)*23,45),(fx+math.cos(a)*39,fy+math.sin(a)*39,16),.9,foam)
beam('Small fountain jet',(fx,fy,46),(fx,fy,77),1.3,foam);sphere('Fountain jet droplet',fx,fy,80,1.4,1.4,2.2,foam);footprint(fx,fy,176,176,'fountain basin');point(fx,fy,31,25,(.08,.66,.62),.6)
# Intentional lamps connect foreground garden to door, illuminate real receivers.
for x,y in [(652,830),(864,835),(395,1005),(1072,1005),(688,1110),(848,1110)]:lantern(x,y,36)
# Shaped center stone cup with small carved lobes, not a plain diagram disk.
for i in range(8):
 a=i*math.tau/8;sphere('Fountain carved bowl lobe',fx+math.cos(a)*24,fy+math.sin(a)*24,42,7,7,5,stoneEdge)
# Brass/pale inlays integrate magic into the masonry, not giant sticker symbols.
for x,y in [(768,999),(768,830)]:
 ring('Inlaid wayfinding circle',x,y,23,21,.3,brass,z=2.2,group='ground')
 for a in [0,math.pi/2,math.pi,3*math.pi/2]:beam('Inlaid compass ray',(x+math.cos(a)*7,y+math.sin(a)*7,2.3),(x+math.cos(a)*18,y+math.sin(a)*18,2.3),.7,brass,'ground')
print('Scene geometry ready',flush=True)
# Hanging ivy baskets tie the glass frontage into the planted garden.
for xx in [382,552,976,1150]:
 yy=747
 ring('Hanging basket copper rim',xx,yy,14,12,4,brass,z=61)
 cyl('Hanging basket bowl',xx,yy,13,10,terra[2],z=52)
 for dx in [-12,12]:beam('Basket chain',(xx+dx,yy,61),(xx,yy,89),.45,brass,'foreground')
 for i in range(6):
  zz=65-i*7;leafmesh('Trailing ivy',[(xx+math.sin(i*1.1)*8,yy+2,zz,4.4,j*1.6,4) for j in range(5)])
 for dx in [-8,0,8]:sphere('Hanging flower',xx+dx,yy,67,2.5,2.5,3,flowerM[3],'foreground')
# A few tall flowering accents give the border silhouettes a hierarchy.
for x,y in [(240,748),(1286,743),(365,1038),(1162,1038)]:
 for z in range(5,76,13):
  radius=max(8,24-z*.18);shrub(x+math.sin(z)*3,y,radius,z+14,False)
 for z in range(50,88,12):sphere('Tall garden bloom',x+math.sin(z)*7,y,z,3,3,3,flowerM[1],'foreground')
# Small architectural butterflies above the welcome, original simple shapes.
for x,y,z in [(710,773,49),(827,789,38),(687,870,24),(914,894,33)]:
 sphere('Butterfly left wing',x-3,y,z,3.5,1.5,3,brass,'foreground');sphere('Butterfly right wing',x+3,y,z,3.5,1.5,3,brass,'foreground');beam('Butterfly body',(x,y,z-3),(x,y,z+3),.5,ink,'foreground')
# Broad directional light sets coherent contact shadows; warm local lamps supplement it.
bpy.ops.object.light_add(type='AREA',location=xy(430,930,470));key=bpy.context.object;key.name='Golden diffuse sky';key.data.energy=1700;key.data.color=(.63,.84,1);key.data.size=10;key.rotation_euler=(Vector(xy(768,550,0))-key.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='SUN',location=(0,0,15));sun=bpy.context.object;sun.name='Low warm sun';sun.data.energy=.9;sun.data.color=(1,.87,.65);sun.data.angle=.12;sun.rotation_euler=(math.radians(30),math.radians(-26),math.radians(-38))
bpy.ops.object.camera_add(location=(0,-32,32));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=48;sc.camera=cam
bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view
o=world_to_camera_view(sc,cam,Vector(xy(768,576)));a=world_to_camera_view(sc,cam,Vector(xy(800,576)));b=world_to_camera_view(sc,cam,Vector(xy(768,608)))
assert abs((a.x-o.x)*W-32)<.01 and abs((o.y-b.y)*H-32)<.01
# Export only genuine occupied-seat and lectern occluders as independent semantic layers.
G['chair-backs']=[o for o in G['foreground'] if 'chair' in o.name.lower()]
G['lectern-rim']=[o for o in G['foreground'] if 'lectern' in o.name.lower() or 'microphone' in o.name.lower()]
G['foreground']=[o for o in G['foreground'] if o not in G['chair-backs'] and o not in G['lectern-rim']]
# Roof is a local visual cutaway, never an unexplained dark ceiling shadow.
for o in G['roof']:o.visible_shadow=False
# Save editable source, logical footprints and exact group metadata before rendering.
layout={'width':W,'height':H,'tile':32,'spawn':{'x':768,'y':1104},'footprints':FOOT,'chairs':chairs,'inside':{'x':288,'y':296,'width':960,'height':444},'roofReveals':[{'area':'commons-inside','layers':['roof']}],'assetMethod':'original calibrated orthographic scene; no reused furniture cutouts','projection':{'xUnitPixels':32,'yUnitPixels':32}}
(R/'art-source'/'scene-layout.json').write_text(json.dumps(layout,indent=2))
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'art-source'/'studenthub-arrival.blend'))
def render(n):sc.render.filepath=str(R/'renders'/n);bpy.ops.render.render(write_still=True)
if DRAFT:
 for o in G['roof']:o.visible_camera=False
 render('draft.png')
 for o in G['roof']:o.visible_camera=True
 render('draft-covered.png')
else:
 for group,obs in G.items():
  for o in obs:o.visible_camera=group!='roof'
 # Final review composites use the actual independent exported groups.
 for group,obs in G.items():
  for o in obs:o.visible_camera=True
 # Covered composite is assembled from the same groups plus the roof.
 for active in ['ground','base','foreground','chair-backs','lectern-rim','glass','roof']:
  for group,obs in G.items():
   for o in obs:o.visible_camera=group==active
  # Covers are a cutaway visual; they intentionally never darken the inhabited room.
  for o in G['roof']:o.visible_shadow=False
  # The broad foliage shade will be applied once above players, not baked twice.
  for o in BROAD:o.visible_shadow=False
  render(active+'.png')
 # Exact floor shadow differential from the same scene/seed produces the player overlay.
 for group,obs in G.items():
  for o in obs:o.visible_camera=group=='ground'
 for o in BROAD:o.visible_shadow=True
 render('ground-with-canopy-shadow.png')
(R/'renders'/'render-contract.json').write_text(json.dumps({'width':W,'height':H,'draft':DRAFT,'samples':sc.cycles.samples,'engine':'Blender Cycles CPU','groups':{k:len(v) for k,v in G.items()},'broadShadowCasters':len(BROAD)},indent=2))
