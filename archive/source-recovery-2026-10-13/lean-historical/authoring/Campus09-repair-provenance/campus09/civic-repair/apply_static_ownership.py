"""Fixed scene ownership derived from reachable physical body space, never actor state."""
from pathlib import Path
from PIL import Image
from collections import deque
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;O=R/'importable-civic';read=lambda p:json.loads(Path(p).read_text());write=lambda p,v:Path(p).write_text(json.dumps(v,indent=2)+'\n')
m=read(O/'module.json');grid=np.array(read(R/'collision-world32.json')['grid'],np.uint8);blocked=grid.repeat(32,0).repeat(32,1);integral=np.pad(blocked.cumsum(0,dtype=np.int32).cumsum(1,dtype=np.int32),((1,0),(1,0)))
# Dense integer world positions plus all12 union mask cover conservative floor/ceil
# rasterization for subpixel placements. No route shape is used for ownership.
y,x=np.indices((1152,640));wy=y+1136;xa=np.maximum(0,x-8);xb=np.minimum(2944,x+8);s=integral[wy+16,xb]-integral[wy,xb]-integral[wy+16,xa]+integral[wy,xa];clear=(s==0)&(x>=8)
reachable=np.zeros_like(grid,bool);q=deque([(29,49)])
while q:
 xx,yy=q.popleft()
 if not(0<=xx<92 and 0<=yy<82)or grid[yy,xx]or reachable[yy,xx]:continue
 reachable[yy,xx]=True;q.extend([(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)])
clear&=reachable[wy//32,x//32]
sp=np.array(Image.open('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png'));u=np.zeros((14,32),bool)
for rr in range(4):
 for cc in range(3):u|=sp[rr*32:rr*32+14,cc*32:cc*32+32,3]>32
reach=np.zeros_like(clear)
for yy,xx in np.argwhere(u):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(640,640-dx);y0=max(0,-dy);y1=min(1152,1152-dy);reach[y0+dy:y1+dy,x0+dx:x1+dx]|=clear[y0:y1,x0:x1]
base=Image.open(O/'furniture-native.png').convert('RGBA');fg=Image.open(O/'foreground-native.png').convert('RGBA');a=np.array(fg);move=reach&(a[:,:,3]>0);moving=np.zeros_like(a);moving[move]=a[move];a[move]=0
# Original empty-scene composite preserved through compositing the exact source
# foreground RGBA into the furniture layer below actors. No chair pixels vanish.
base_before=base.copy();fg_before=fg.copy();base.alpha_composite(Image.fromarray(moving));fg=Image.fromarray(a);base.save(O/'furniture-native.png');fg.save(O/'foreground-native.png')
base_before.save(R/'registered-furniture-before-ownership.png');fg_before.save(R/'registered-foreground-before-ownership.png')
objects=[]
for aobj in m['students']+m['audience']+[m['speaker']]:
 cx,cy=aobj['center'];box=(slice(cy-32,cy+48),slice(cx-40,cx+40));fa=np.array(fg_before)[box][:,:,3]>0;ma=move[box];objects.append({'id':aobj['id'],'originalFixedForegroundPixels':int(fa.sum()),'movedBelowPixels':int(ma.sum()),'retainedAbovePixels':int((fa&~ma).sum())})
arch=Image.open(O/'architecture-native.png').convert('RGBA');old=arch.copy();old.alpha_composite(base_before);old.alpha_composite(fg_before);new=arch.copy();new.alpha_composite(base);new.alpha_composite(fg);delta=np.abs(np.array(old).astype(int)-np.array(new).astype(int));stats={'policy':'Static pixel ownership split against every integer reachable native16x16 body placement and all12 Greg head masks; conservative floor/ceil rasterization. No player state, path-based carveout, actor-following mask or dynamic feature. Exact original foreground RGBA is composited into furniture below actors only where a reachable head can cover it.','reachableBodyPlacements':int(clear.sum()),'movedBelowForegroundPixels':int(move.sum()),'retainedAboveForegroundPixels':int((np.array(fg)[:,:,3]>0).sum()),'emptySceneMaxChannelDifference':int(delta.max()),'emptySceneChangedPixels':int(np.any(delta,axis=2).sum()),'objects':objects}
write(R/'static-ownership-verification.json',stats)
# Re-render final native afterviews and occupied pixel counts.
layer={k:Image.open(O/(k+'-native.png')).convert('RGBA')for k in ['architecture','furniture','foreground','glass','shadow']};empty=layer['architecture'].copy();empty.alpha_composite(layer['furniture']);occupied=empty.copy();sheet=Image.fromarray(sp);occ=[]
for aobj in m['students']+m['audience']+[m['teacher'],m['speaker']]:
 cx,cy=aobj['center'];fr=aobj['frame'];sprite=sheet.crop(((fr%3)*32,(fr//3)*32,(fr%3+1)*32,(fr//3+1)*32));occupied.alpha_composite(sprite,(cx-16,cy-16));sa=np.array(sprite)[:,:,3]>32;fa=np.array(fg)[cy-16:cy+16,cx-16:cx+16,3]>32;torso=sa.copy();torso[:14]=False;occ.append({'id':aobj['id'],'localAnchor':[cx,cy],'frame':fr,'torsoAndLegOpaquePixels':int(torso.sum()),'fixedForegroundOccludedTorsoAndLegPixels':int((torso&fa).sum()),'visibleTorsoAndLegPixels':int((torso&~fa).sum()),'headPixelsOccluded':int((sa[:14]&fa[:14]).sum())})
for k in ['foreground','glass','shadow']:empty.alpha_composite(layer[k]);occupied.alpha_composite(layer[k])
empty.save(R/'after-native.png');occupied.save(R/'after-greg32-native.png');write(R/'after-occupied-pixels.json',occ)
full=np.zeros((2624,2944),np.uint8);full[1136:2288,:640]=np.array(fg)[:,:,3]>32;danger=np.zeros_like(full)
for yy,xx in np.argwhere(u):
 dx=int(xx)-16;dy=int(yy)-16;x0=max(0,-dx);x1=min(2944,2944-dx);y0=max(0,-dy);y1=min(2624,2624-dy);danger[y0:y1,x0:x1]|=full[y0+dy:y1+dy,x0+dx:x1+dx]
(R/'after-greg12-head-danger.bin').write_bytes(danger.tobytes());assert not np.any(danger[1136:2288,:640][clear])
for label,box in [('classroom',(112,176,528,448)),('lectern',(256,640,384,784)),('audience',(112,784,528,1056))]:
 before=Image.open(R/'before-greg32-native.png').crop(box);after=occupied.crop(box);board=Image.new('RGBA',(before.width*2+16,before.height),(22,27,37,255));board.paste(before,(0,0));board.paste(after,(before.width+16,0));board.save(R/(label+'-before-after-greg32-native.png'))
m['registrationRepair']['foregroundPolicy']=stats['policy'];m['registrationRepair']['seatedAppearanceTradeoff']='All30 chair backs are head-reachable from some clear native body position. Their unsafe fixed-foreground pixels are kept in furniture below actors. This intentionally reduces the seated illusion: occupied actors cover the chair back. Safe static lectern rim pixels remain above. This is a map-layer ownership choice; it does not claim other Universe maps cannot render seated characters.';write(O/'module.json',m)
print(json.dumps(stats,indent=2))
