from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,os
R=Path(__file__).resolve().parents[1];P=R/'lantern-souk-bazaar-r5';S=R/'source';layout=json.loads((P/'source/layout.json').read_text())
W=Path(os.environ.get('SOUK_WOKA_REPO','/workspace/shared/native32-replan-baseline'))/'play/public/resources/characters/pipoya'
lookup={'pipoya-female-04-1':'Female 04-1.png','pipoya-male-09-4':'Male 09-4.png'}
if not all((W/n).is_file() for n in lookup.values()):
 raise SystemExit('Optional proof regeneration requires licensed local repo assets. Set SOUK_WOKA_REPO to your existing workadventure-universe checkout; raw third-party Woka sheets are intentionally not bundled.')
im=Image.open(P/'review/empty-native.png').convert('RGBA');proof=[]
for a,name,frame in [(next(a for a in layout['anchors'] if a['id']=='fountain-social-left'),'pipoya-female-04-1',7),(next(a for a in layout['anchors'] if a['id']=='fountain-social-right'),'pipoya-male-09-4',4)]:
 sheet=Image.open(W/lookup[name]).convert('RGBA');sprite=sheet.crop((frame%3*32,frame//3*32,frame%3*32+32,frame//3*32+32));im.alpha_composite(sprite,(a['x']-16,a['y']-16));proof.append(dict(anchor=a['id'],sprite=name,frame=frame,direction=a['direction'],position=[a['x'],a['y']],nativeSize=[32,32],sheetSHA256=hashlib.sha256((W/lookup[name]).read_bytes()).hexdigest()))
im.save(P/'review/occupied-native.png');im.crop((792,768,1128,928)).save(P/'review/opposed-seats-native-100pct.png');im.crop((792,768,1128,928)).resize((1008,480),Image.Resampling.NEAREST).save(P/'review/opposed-seats-3x.png')
# Explicit small tangent contact sheet: native sprites on both sides of new furniture.
anchors=[(904,832,'left back / upper'),(904,848,'left back / lower'),(920,832,'table west / upper'),(920,848,'table west / lower'),(1000,832,'table east / upper'),(1000,848,'table east / lower'),(1016,832,'right back / upper'),(1016,848,'right back / lower')]
out=Image.new('RGB',(768,896),'#142e32');d=ImageDraw.Draw(out);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);checks=[]
for i,(x,y,label) in enumerate(anchors):
 clear=all(layout['grid'][yy][xx]==0 for yy in range(y//32,(y+15)//32+1) for xx in range((x-8)//32,(x+7)//32+1));assert clear
 a=Image.open(P/'review/empty-native.png').convert('RGBA');sheet=Image.open(W/lookup['pipoya-female-04-1']);a.alpha_composite(sheet.crop((32,64,64,96)),(x-16,y-16));crop=a.crop((x-48,y-32,x+48,y+32)).resize((288,192),Image.Resampling.NEAREST);xx=(i%2)*384;yy=(i//2)*224;out.paste(crop,(xx,yy+24));d.text((xx+4,yy+4),label,font=font,fill='white');checks.append(dict(x=x,y=y,bodyClear=clear,fixture=label))
out.save(P/'review/seating-tangent-contact-sheet.png')
(P/'validation/seating-tangents.json').write_text(json.dumps(dict(scope='Actual visible backrest and table tangents, inspected against artwork; source-native 16x16 body clearance.',points=checks,allPass=True),indent=2)+'\n')
(P/'validation/varied-woka-seating.json').write_text(json.dumps(dict(scope='Native 32px repository sprite visual occupancy. Both authored chair anchors already covered by native route replay; no live room or real multi-user test.',sourceRepository='https://github.com/BAWES-Universe/workadventure-universe',sourceCommit='90a148c03e03401e26d236eaac9bea4123b42c57',sourcePath='play/public/resources/characters/pipoya/',attribution='Pipoya free RPG character sprites 32x32: https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32',allVisualSeats=2,occupiedSeats=2,distinctRepositoryWokas=2,facingEachOther=True,fixtures=proof),indent=2)+'\n')
