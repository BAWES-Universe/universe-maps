from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];j=lambda p:json.load(open(R/p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=j('source/collision-grid.json');seats=j('source/seats.json');fg=np.array(Image.open(R/'assets/runtime-above.png'))[:,:,3]>32;greg=np.array(Image.open(R/'assets/greg-reference.png'));north=greg[96:128,32:64,3]>32;rows=[]
for a in seats+[a for a in h['socialAnchors']if a['kind']in['team','caster']]:
 crop=fg[a['y']-16:a['y']+16,a['x']-16:a['x']+16];over=crop&north;rows.append({'id':a['id'],'headPixelsCovered':int(over[:14].sum()),'lowerTorsoBackrestPixels':int(over[14:].sum()),'pass':bool(not over[:14].any()and over[14:].sum()>15)})
assert all(r['pass']for r in rows);assert sha(R/'assets/greg-reference.png')=='e88ba016c58f6bc7616c831c3c56a4656e66772794940af93c0c0835e85a987d'
report={'scope':'All38 occupied native north chairs intersect actual unchanged Greg v3 head/lower-body alpha. Foreground restores lower torsos, never upper14px heads. Entire-map exhaustive geometry is separate.','chairs':len(rows),'zeroHeadOcclusion':True,'allBackrestsRestoreTorso':True,'minimumBackrestTorsoPixels':min(r['lowerTorsoBackrestPixels']for r in rows),'allPass':True,'details':rows};(R/'validation/chairback-depth.json').write_text(json.dumps(report,indent=2)+'\n')
commit='60e7afdc3f96ef32525597cd46bd41175d61a2ef';repo='/workspace/shared/native32-replan-fix';paths=['play/src/front/Phaser/Game/GameScene.ts','play/src/front/Utils/PathfindingManager.ts','play/src/front/Phaser/Player/Player.ts','play/src/front/Phaser/Game/GameMap/GameMapFrontWrapper.ts','libs/map-editor/src/types.ts','docs/schema/2.0.0/wam.json'];manifest=[]
for p in paths:
 b=subprocess.check_output(['git','-C',repo,'show',commit+':'+p]);work=Path(repo,p).read_bytes();manifest.append({'path':p,'sha256':hashlib.sha256(b).hexdigest(),'workingSourceMatchesCommit':b==work,'source':'https://github.com/BAWES-Universe/workadventure-universe/blob/'+commit+'/'+p})
assert all(a['workingSourceMatchesCommit']for a in manifest);(R/'validation/engine-source-manifest.json').write_text(json.dumps({'commit':commit,'files':manifest,'portableFixtureFiles':[{'file':p.name,'sha256':sha(p)}for p in(R/'validation/route-proof').iterdir()if p.name in['native-runtime-portable.cjs','extracted-current-source.cjs','easystar-0.4.4.js']],'scope':'Read-only pinned source audit, no engine files changed or deployment claim.'},indent=2)+'\n')
# A native-scale proof board shows exact runtime source art before/after actor masking.
base=Image.open(R/'assets/runtime-base.png').convert('RGBA');above=Image.open(R/'assets/runtime-above.png').convert('RGBA');g=Image.open(R/'assets/greg-reference.png').convert('RGBA').crop((32,96,64,128));font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n);board=Image.new('RGB',(736,282),'#111c22');d=ImageDraw.Draw(board);d.text((16,12),'CHAIRBACK DEPTH / ACTUAL NATIVE32 COMPOSITION',font=font(16),fill='#cee0df')
for idx,(caption,actor,foreground)in enumerate([('Empty furniture',False,True),('Actor, no foreground',True,False),('Final safe backrest',True,True)]):
 box=(176,272,368,384);im=base.crop(box)
 if actor:
  for x in[208,272,336]:im.alpha_composite(g,(x-16-box[0],335-16-box[1]))
 if foreground:im.alpha_composite(above.crop(box))
 board.paste(im,(16+idx*240,72));d.text((16+idx*240,46),caption,font=font(13),fill='#d5dddf')
d.text((16,213),'38 chairs: zero head pixels covered; visible lower-torso backrests at every occupied anchor.',font=font(13),fill='#b8cdd0');d.text((16,239),'32px actors / 16×16 bodies / native source pixels. No live browser or device claim.',font=font(13),fill='#b8cdd0');board.save(R/'review/CHAIRBACK-DEPTH-native32.png')
print(json.dumps({k:v for k,v in report.items()if k!='details'},indent=2))
