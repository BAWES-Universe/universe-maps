"""Optional isolated composition sketch only. Does not write runtime assets or geometry."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';A=R.parent/'grand-auditorium-07-clean';Q=R/'review';rgba=lambda p:Image.open(p).convert('RGBA');W,H=2560,1920
cfg=json.loads((S/'frozen-a/runtime-layout.json').read_text());old=[p for p in cfg['furniture']if p['id'].startswith('garden-pair-')]
base=rgba(R/'assets/runtime-base.png');above=rgba(R/'assets/runtime-above.png');clear=rgba(S/'overlays/stone-new-material-under-furniture.png')
# Only optional preview removes/repositions existing chairs. All production candidate assets stay frozen.
for p in old:
 x,y,w,h=p['x'],p['y'],p['width'],p['height'];box=(x,y,x+w,y+h);base.paste(clear.crop(box),(x,y));above.paste((0,0,0,0),box)
actors=rgba(S/'frozen-a/qa-actors-only.png');actors.paste((0,0,0,0),(1992,184,2344,272))
chair=rgba(A/'source/repair-assets/assets/lounge-chair-north.png');table=rgba(A/'source/repair-assets/assets/low-lounge-table.png');greg=rgba(S/'frozen-a/greg-reference.png');actor=greg.crop((32,96,64,128));placements=[]
for i,x in enumerate([2016,2064,2240,2288]):
 p=old[i];lo=rgba(A/p['belowAsset']);hi=rgba(A/p['aboveAsset']);base.alpha_composite(lo,(x,215));above.alpha_composite(hi,(x,215));actors.alpha_composite(actor,(x+8,215));placements.append({'id':'optional-seat-'+str(i+1),'artXYWH':[x,215,48,44],'anchor':[x+24,231],'direction':'north','source':p['asset']})
for i,x in enumerate([2032,2256]):base.alpha_composite(table,(x,152));placements.append({'id':'optional-table-'+str(i+1),'artXYWH':[x,152,64,36],'source':'source/repair-assets/assets/low-lounge-table.png'})
render=base.copy();render.alpha_composite(actors);render.alpha_composite(above);box=(1920,48,2400,400);option=render.crop(box);option.save(Q/'optional-pavilion-composition-native.png')
oldrender=rgba(Q/'flagship-b-pavilion-occupied-native.png');F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
board=Image.new('RGB',(1020,500),'#123036');d=ImageDraw.Draw(board);d.text((20,14),'OPTIONAL PAVILION COMPOSITION / native 1:1',font=bold(20),fill='#f6dda6');d.text((20,52),'B material-only candidate: existing seating',font=font(16),fill='#cbddda');d.text((520,52),'Optional: paired seats + accepted low tables',font=font(16),fill='#cbddda');board.paste(oldrender,(20,82));board.paste(option,(520,82));d.text((20,453),'48px partner anchors; 128px central clear strip. Geometry sketch only; collision not changed.',font=font(16),fill='#e6ca91');board.save(Q/'optional-pavilion-before-after-native.png')
# Separate analytical annotation, never baked into art.
annot=option.copy();d=ImageDraw.Draw(annot);d.rectangle((2112-1920,112-48,2239-1920,351-48),fill=(45,157,159,38),outline=(71,173,170,200),width=1);annot.save(Q/'optional-pavilion-clearance-native.png')
(S/'optional-pavilion-placement-proposal.json').write_text(json.dumps({'status':'Separate optional sketch only; not applied to B assets or collision. Needs geometry/entry review before accepting.','placements':placements,'partnerAnchorDistancePx':48,'centralClearStripXYWH':[2112,112,128,240],'clearTurnaroundSquareXYWH':[2112,128,128,128],'newFurnitureArtwork':False,'existingChairScaleChanged':False,'proposedChanges':['Move second left chair 8px west and first right chair 8px east.','Add two existing64×36px low tables, each ahead of one paired seat group.'],'noCompiledGeometryChange':True},indent=2)+'\n')
print('Optional native pavilion sketch saved separately; runtime assets unchanged.')
