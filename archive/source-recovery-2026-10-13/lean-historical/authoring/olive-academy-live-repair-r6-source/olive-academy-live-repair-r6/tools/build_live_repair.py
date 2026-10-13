"""Deterministic tile/layer correction of the accepted Academy r5b; no engine changes."""
from pathlib import Path
import json,copy,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
src=R/'final/olive-academy-context-r5b'; out=R/'maps/olive-academy-live-repair-r6'
if out.exists(): shutil.rmtree(out)
shutil.copytree(src,out)
for p in ['FREEZE.json','HEAD-GEOMETRY.json','HEAD-DELTA-CHECK.json','TRANSLATION-CHECK.json','NATIVE-ROUTES.json']:
 (out/p).unlink(missing_ok=True)
J=lambda p:json.loads(p.read_text())
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
base=Image.open(src/'assets/base.png').convert('RGBA');above=Image.open(src/'assets/above.png').convert('RGBA');origbase=base.copy()
# Low wall caps begin at the same native32 boundary as their collider.
# Existing cap texture is reused; every cushion, table and approved seat remains unchanged.
for y in [448,704]:
 strip=origbase.crop((1152,y+16,1408,y+48)).resize((256,48),Image.Resampling.NEAREST)
 base.paste(strip,(1152,y))
 # Complete the lower-left stone corner to its blocked tile boundary.
 generated=Image.open(R/'source-assets/lounge-pillar-generated.png').convert('RGBA').resize((192,256),Image.Resampling.LANCZOS)
 pierheight=160 if y==448 else 128
 corner=generated.crop((84,58,128,208)).resize((64,pierheight),Image.Resampling.LANCZOS)
 base.paste(origbase.crop((1088,y-48,1152,y-32)),(1088,y-16))
 base.paste(corner,(1088,y))
# Replace the misleading blue ground-like south perimeter with real stone low-wall caps.
wallspans=[(64,448),(672,960)]
stone=origbase.crop((1152,464,1408,508))
for x0,x1 in wallspans:
 base.paste(stone.resize((x1-x0,32),Image.Resampling.NEAREST),(x0,640))
 # Maintain existing foreground ownership but use corrected wall pixels.
 patch=base.crop((x0,640,x1,672));patch.putalpha(above.crop((x0,640,x1,672)).getchannel('A'));above.paste(patch,(x0,640))
# Existing whole stone posts stand in front of the new low wall; never flatten them.
postmask=Image.new('L',base.size);pd=ImageDraw.Draw(postmask)
for x0,x1 in [(184,214),(318,348),(840,872)]:
 pd.polygon([(x0+2,638),(x1-2,638),(x1-2,674),(x0,674),(x0,645)],fill=255)
base.paste(origbase,(0,0),postmask)
for x0,x1 in wallspans:
 patch=base.crop((x0,640,x1,672));patch.putalpha(above.crop((x0,640,x1,672)).getchannel('A'));above.paste(patch,(x0,640))
# Pull the terminal flowerbed/pier edge back to x864 before opening col27.
# This removes its former 6px spill into the otherwise clear paving cell.
edge=base.crop((840,636,872,736)).resize((24,100),Image.Resampling.LANCZOS)
base.paste(edge,(840,636));base.paste(base.crop((872,636,880,736)),(864,636))
patch=base.crop((840,640,872,672));patch.putalpha(above.crop((840,640,872,672)).getchannel('A'));above.paste(patch,(840,640))
# Keep natural tree artwork below players. Only identified olive foliage is repeated
# above them, at 96/255 alpha: at least 62% of the avatar remains visible behind it.
# In particular, no courtyard painted border is eligible for foreground ownership.
a=np.array(above);mask=Image.new('L',above.size);d=ImageDraw.Draw(mask)
polys=[[(222,759),(254,748),(290,750),(316,744),(350,759),(399,753),(420,774),(442,792),(441,817),(424,832),(408,850),(376,864),(343,875),(291,875),(254,858),(219,849),(215,811)],[(732,759),(766,749),(792,753),(825,744),(857,757),(899,760),(930,781),(947,805),(937,829),(915,851),(881,869),(845,879),(798,876),(760,859),(727,848),(719,812)]]
for poly in polys:d.polygon(poly,fill=255)
region=np.zeros(a.shape[:2],bool);region[720:912,180:976]=True
rgb=a[:,:,:3].astype(float);foliage=(rgb[:,:,1]>=rgb[:,:,0]*.95)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(np.array(mask)>0)
oldalpha=a[:,:,3].copy();a[:,:,3][region]=np.where(foliage[region],np.minimum(oldalpha[region],96),0)
a[a[:,:,3]==0]=0;above=Image.fromarray(a)
base.save(out/'assets/base.png');above.save(out/'assets/above.png')
m=J(src/'map32/map.tmj');layout=J(src/'source/layout.json')
layout['title']='Olive Academy live repair r6'
# Clear paving east of the large-classroom flowerbed is not a wall.
opened=[(27,y) for y in [21,22,23]]+[(x,23) for x in list(range(6,13))+list(range(22,27))]
for x,y in opened:
 layout['collision'][y][x]=0
 next(l for l in m['layers'] if l['name']=='collision')['data'][y*48+x]=0
layout['anchors'].extend([{'name':'large classroom southeast clear floor '+str(y),'cell':[27,y]} for y in [21,22,23]])
layout['anchors'].extend([{'name':'painted paving behind west olive','cell':[9,23]},{'name':'painted paving behind east olive','cell':[25,23]}])
# Exact atlas tile replacement preserves all unrelated TMJ properties and GIDs.
for lname,im in [('architecture-and-furniture',base),('seat-backs',above)]:
 layer=next(l for l in m['layers'] if l['name']==lname)
 atlases={s['firstgid']:Image.open(out/'map32'/s['image']).convert('RGBA') for s in m['tilesets'] if s['name'].startswith(lname)}
 seen={}
 for i,g in enumerate(layer['data']):
  if not g:continue
  s=max((s for s in m['tilesets'] if s['firstgid']<=g),key=lambda s:s['firstgid']);n=g-s['firstgid'];tile=im.crop((i%48*32,i//48*32,i%48*32+32,i//48*32+32))
  if g in seen: assert seen[g]==tile.tobytes(),'Shared GID changed inconsistently'
  seen[g]=tile.tobytes();atlases[s['firstgid']].paste(tile,(n%s['columns']*32,n//s['columns']*32))
 for s in m['tilesets']:
  if s['firstgid'] in atlases:atlases[s['firstgid']].save(out/'map32'/s['image'])
save(out/'map32/map.tmj',m);save(out/'source/layout.json',layout)
# Atlas decode is the proof source, not a separate illustration.
import sys
sys.path.insert(0,str(R/'tools'))
from build_contexts import decode
below,fg=decode(out,m);empty=Image.alpha_composite(below,fg);empty.save(out/'review/empty-native.png')
# Frozen native actor placements are composited in the actual runtime layer order.
actors=Image.open(R/'source-assets/r6-proof-actors.png').convert('RGBA')
occupied=below.copy();occupied.alpha_composite(actors);occupied.alpha_composite(fg)
occupied.save(out/'review/occupied-native.png');occupied.save(out/'review/overview.png')
seatboxes=[(s['anchor'][0]-24,s['anchor'][1]-24,s['anchor'][0]+24,s['anchor'][1]+17) for s in layout['seats']]
assert all(base.crop(b).tobytes()==origbase.crop(b).tobytes() for b in seatboxes)
assert np.array(above)[720:744,:,3].max()==0
assert np.array(above)[752:912,:,3].max()<=96
save(out/'REPAIR-CHECK.json',{'baseline':'olive-academy-context-r5b','nativeTileSize':32,'approvedSeatCount':len(layout['seats']),'approvedSeatArtExact':True,'approvedSeatsAndAnchorsExact':layout['seats']==J(src/'source/layout.json')['seats'],'wamByteExact':(out/'map32/map.wam').read_bytes()==(src/'map32/map.wam').read_bytes(),'terminalFlowerbedEdgeMaximumX':864,'mainClassroomVisibleStoneWallSpans':[[x0,640,x1,672] for x0,x1 in wallspans],'openedClearFloorCells':opened,'treeMaxForegroundAlpha':96,'minimumAvatarContributionBehindCanopy':159/255,'paintedNorthCourtBorderForegroundAlpha':0,'wallCapExtensionRects':[[1088,y,1408,y+48] for y in [448,704]],'scope':'Deterministic native map-layer repair and reconstructed proofs; no live browser assertion.'})
(out/'GUIDE.md').write_text('''# Olive Academy live repair r6

Approved warm cushion lounges and all 30 seats are retained. The two olive canopies use foliage-only foreground at 96/255 opacity so players remain visible. Tree trunks and planters remain solid. Painted paving stays below players. Lower lounge wall caps now start at their native32 collision boundary.

Host the complete map32 directory. No engine changes. WAM configuration is unchanged. Review images are exact-TMJ static reconstructions, not live browser or multi-user playtests.

Rebuild: python tools/build_live_repair.py
Motion: node tools/verify_native_routes.cjs maps/olive-academy-live-repair-r6
''')
print(out)
