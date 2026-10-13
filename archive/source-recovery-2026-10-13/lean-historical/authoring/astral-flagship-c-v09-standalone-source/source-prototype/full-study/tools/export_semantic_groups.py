from pathlib import Path
from PIL import Image,ImageChops
import numpy as np,json,hashlib,shutil
from frozen_inputs import frozen_b_input,historical_a_comparison
R=Path(__file__).resolve().parents[1];W,H=2816,2432
rgba=lambda p:Image.open(p).convert('RGBA')
components={n:rgba(R/'assets'/f'{n}.png')for n in ['hall-shell-above-combined','hall-shell-shadow','foyer-shell-shadow','foyer-shell-front-wings','foyer-shell-roof','foyer-shell-entrance','foyer-shell-porch']}
front=components['foyer-shell-entrance'].copy();front.alpha_composite(components['foyer-shell-porch'])
groups={'hall-shadow':components['hall-shell-shadow'],'foyer-shadow':components['foyer-shell-shadow'],'hall-shell':components['hall-shell-above-combined'],'foyer-wings':components['foyer-shell-front-wings'],'foyer-roof':components['foyer-shell-roof'],'foyer-front':front}
for n,im in groups.items():im.save(R/'assets'/f'{n}.png');im.getchannel('A').save(R/'masks'/f'{n}-alpha.png')
def bounds(m):
 y,x=np.where(m>0)
 return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]if len(x)else None
alphas={k:np.array(v)[:,:,3]for k,v in groups.items()}
# Whole semantic roof module overlaps hall ground; no arbitrary strip slicing.
foyer_roof=alphas['foyer-roof'];hall_floor=np.zeros((H,W),bool);hall_floor[256:1200,128:1664]=True
hall_core=np.zeros((H,W),bool);hall_core[256:1345,128:1665]=True
foyer_overlap=(foyer_roof>0)&hall_floor;core_overlap=(foyer_roof>0)&hall_core
wing_roof=(alphas['foyer-wings']>0)&(foyer_roof>0)
entry={'hall':{'core':[128,256,1664,1344],'eastApron':[1536,432,1832,880]},'foyer':{'core':[128,1280,1664,2032],'southApron':[512,1696,1280,2112],'eastApron':[1536,1328,1832,1776]}}
hold={owner:{name:[b[0]-32,b[1]-32,b[2]+32,b[3]+32]for name,b in boxes.items()}for owner,boxes in entry.items()}
contract={
 'status':'Six semantic decorative exports, no runtime/controller install',
 'groups':{
  'hall-shadow':{'asset':'assets/hall-shadow.png','z':'below actors','hiddenWhen':['hallOpen'],'sourceModules':['hall-front-foot shadow','hall east-porch contact shadow']},
  'foyer-shadow':{'asset':'assets/foyer-shadow.png','z':'below actors','hiddenWhen':['foyerOpen'],'sourceModules':['south-wing foot shadows','approved entrance shadow','foyer east-porch contact shadow']},
  'hall-shell':{'asset':'assets/hall-shell.png','z':'above actors, first shell slot','hiddenWhen':['hallOpen'],'sourceModules':['hall front face','hall roof','hall east porch']},
  'foyer-wings':{'asset':'assets/foyer-wings.png','z':'above hall-shell, below foyer-roof','hiddenWhen':['foyerOpen'],'sourceModules':['native south-wing windows and piers']},
  'foyer-roof':{'asset':'assets/foyer-roof.png','z':'above foyer-wings, below foyer-front','hiddenWhen':['hallOpen','foyerOpen'],'condition':'hide if EITHER owner is open','sourceModules':['entire original-size foyer roof master']},
  'foyer-front':{'asset':'assets/foyer-front.png','z':'last shell slot above foyer-roof','hiddenWhen':['foyerOpen'],'sourceModules':['unchanged approved south entrance/pediment','foyer east porch']}
 },
 'allGroupsWorldPixels':[W,H],
 'renderOrder':['permanent base','permanent threshold below actors','hall-shadow if visible','foyer-shadow if visible','actors original32','permanent B interior-above','hall-shell if visible','foyer-wings if visible','foyer-roof if visible','foyer-front if visible'],
 'entryRegionsXYXY':entry,'holdRegionsXYXY':hold,
 'boundaryConvention':'Inclusive. Enter at y1344 for hall from foyer, y2112 south orx1832 east; restore immediately beyond hold boundaries, not while exactly on them.',
 'transition':'Evaluate each logical owner independently; initialize each from its entry-region union; instant visibility changes. Hall camera focus is separate.',
 'dependencies':{'hallOpenHides':['hall-shadow','hall-shell','foyer-roof'],'foyerOpenHides':['foyer-shadow','foyer-wings','foyer-roof','foyer-front']},
 'alphaBoundsXYXY':{n:bounds(a)for n,a in alphas.items()},
 'overlap':{'foyerRoofIntoAcceptedHallFloor':{'pixelCount':int(foyer_overlap.sum()),'boundsXYXY':bounds(foyer_overlap)},'foyerRoofWithinHallRevealCore':{'pixelCount':int(core_overlap.sum()),'boundsXYXY':bounds(core_overlap)},'wingRoofPainterOverlap':{'pixelCount':int(wing_roof.sum()),'boundsXYXY':bounds(wing_roof),'reasonForSeparateWingsSlot':'Wings precede roof while entry and porch follow roof; flattening all foyer-front changes approved composition.'},'handling':'Hide the entire foyer-roof module while hallOpen. No arbitrary horizontal alpha slice. Both shadow groups are ground/contact shadows only and have no foreign-roof dependency.'},
 'measuredFrontBounds':{'hallFront':bounds(np.array(rgba(R/'assets/hall-shell-frontface.png'))[:,:,3]),'hallShadow':bounds(alphas['hall-shadow']),'foyerRoof':bounds(foyer_roof)},
 'hallSouthTriggerSafety':{'playerCenterY':1344,'conservativeFrameTopY':1328,'lastHallFrontAlphaY':1290,'marginPixels':37,'lastHallGroundShadowAlphaY':1304,'shadowBelowActor':True},
 'sourceOwnership':'Original modules, not arbitrary world-coordinate splitting','collisionConstant':True,'outsideCamera':'Ordinary follow/manual zoom; no exterior camera state','hallFocus':'Accepted native hall focus translated only, independent of both reveal owners.'}
(R/'semantic-shell-contract.json').write_text(json.dumps(contract,indent=2)+'\n');(R/'layer-ownership.json').write_text(json.dumps(contract,indent=2)+'\n')
# Recomposition of the original-order full outside shell, for renderer handoff.
rebuilt=Image.new('RGBA',(W,H))
for n in ['hall-shell','foyer-wings','foyer-roof','foyer-front']:rebuilt.alpha_composite(groups[n])
old=rgba(R/'assets/full-shell-occlusion-above.png');x=np.array(rebuilt,dtype=np.int16);y=np.array(old,dtype=np.int16);m=np.any(x!=y,axis=2)&((x[:,:,3]>0)|(y[:,:,3]>0));maxdelta=int(np.abs(x-y).max())
# Independent state simulation tests all approaches plus foyer-to-hall transit.
def contains(b,x,y):return b[0]<=x<=b[2]and b[1]<=y<=b[3]
def update(states,x,y):
 return {o:any(contains(b,x,y)for b in (hold[o]if states[o]else entry[o]).values())for o in ['hall','foyer']}
def visible_alpha(states):
 layers=[]
 if not states['hall']:layers.append(alphas['hall-shell'])
 if not states['foyer']:layers.extend([alphas['foyer-wings'],alphas['foyer-front']])
 if not states['hall']and not states['foyer']:layers.append(alphas['foyer-roof'])
 return layers
sweeps={
 'south-entry-reverse-exit':([(896,y)for y in range(2240,1695,-1)]+[(896,y)for y in range(1696,2241)]),
 'hall-east-entry-reverse-exit':([(x,752)for x in range(1920,1535,-1)]+[(x,752)for x in range(1536,1921)]),
 'foyer-east-entry-reverse-exit':([(x,1648)for x in range(1920,1535,-1)]+[(x,1648)for x in range(1536,1921)]),
 'foyer-hall-transition-reverse':([(1104,y)for y in range(1504,1135,-1)]+[(1104,y)for y in range(1136,1505)])}
results={}
for name,path in sweeps.items():
 state={'hall':False,'foyer':False};hits=[];changes=[]
 for x,y in path:
  new=update(state,x,y)
  if new!=state:changes.append({'center':[x,y],'state':new.copy()})
  state=new
  if any((a[y-16:y+16,x-16:x+16]>0).any()for a in visible_alpha(state)):hits.append([x,y])
 results[name]={'samples':len(path),'visibleShell32pxFrameIntersections':hits,'stateTransitions':changes}
proof={'semanticRecompositionVisibleDifferencePixels':int(m.sum()),'semanticRecompositionMaximumChannelDifference':maxdelta,'note':'Precomposing independent PNG groups can change integer alpha rounding by1 channel level; native component pixels are unchanged.','sweeps':results,'allSweepsHeadSafe':all(not r['visibleShell32pxFrameIntersections']for r in results.values()),'runtimeTest':False,'cameraChanged':False}
(R/'validation/semantic-reveal-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
# Integrate the semantic contract and exact B changes in the parent handoff.
g=json.loads((R/'geometry-contract.json').read_text());g['revealStateContract']={'semanticContract':'semantic-shell-contract.json','entryRegionsXYXY':entry,'holdRegionsXYXY':hold,'dependencies':contract['dependencies'],'outsideCamera':'ordinary follow/manual zoom','hallFocus':'independent accepted native hall focus'}
# A-to-B deltas are archived provenance, not a fresh external A comparison.
# The helper first checks the regenerated C base/above against the exact frozen
# outputs covered by that historical proof; B inputs are individually pinned.
archived=historical_a_comparison()
frozen_b_input('source/collision-grid.json')
g['approvedBIntegration']=archived['approvedBIntegration']
changes=g['approvedBIntegration']['changedSocialAnchors']
g['spawn']['body16Anchor']='x±8; y..y+16, native engine anchor, not y±8';g['semanticExportAssets']={n:'assets/'+n+'.png'for n in groups};(R/'geometry-contract.json').write_text(json.dumps(g,indent=2)+'\n')
# Preserve B's native animation asset/coordinates for the parent's compiler.
shutil.copy2(frozen_b_input('assets/garden-leaf-accent-native.png'),R/'assets/garden-leaf-accent-native.png')
an=json.loads((frozen_b_input('source/animation-placement.json')).read_text());an['sourceCoordinateTranslationTiles']=[4,8]
for p in an['placements']:p['cell']=[p['cell'][0]+4,p['cell'][1]+8]
an['status']='Source-only translated B animation placement; not compiled or installed';(R/'b-animation-placement-translated.json').write_text(json.dumps(an,indent=2)+'\n')
# Deprecated single-shell proofs cannot stand in for the final split model.
for p in [R/'validation/reveal-state-proposal.json',R/'validation/full32-frame-state-sweep.json']:
 p.write_text(json.dumps({'status':'Superseded by semantic-reveal-proof.json; source now has independent hall and foyer owners','replacement':'semantic-reveal-proof.json'},indent=2)+'\n')
print(json.dumps({'groups':list(groups),'hallFrontMaxY':1290,'hallShadowMaxY':1304,'foyerRoofMinY':1154,'foyerRoofHallOverlap':contract['overlap']['foyerRoofIntoAcceptedHallFloor'],'allSweepsHeadSafe':proof['allSweepsHeadSafe'],'recomposePixels':int(m.sum()),'recomposeMaxDelta':maxdelta,'BChangedAnchors':changes},indent=2))
