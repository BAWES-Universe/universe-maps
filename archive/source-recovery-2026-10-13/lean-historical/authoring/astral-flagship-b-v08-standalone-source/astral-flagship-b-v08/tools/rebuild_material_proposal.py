"""Rebuild local-only Flagship B surface study from frozen A and generated material masters.
No TMJ, collision, audio, foreground, chair, hall or foyer edits.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageFilter,ImageOps
import numpy as np,json,random,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';M=R/'masks';Q=R/'review';W,H=2560,1920
rgba=lambda p:Image.open(p).convert('RGBA');blank=lambda:Image.new('RGBA',(W,H));write=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
# Uniform reductions establish true material scale. No anisotropic resize anywhere.
wood=rgba(S/'deck-generated-master.png').resize((627,627),Image.Resampling.LANCZOS)
stone=rgba(S/'stone-generated-master.png').resize((418,418),Image.Resampling.LANCZOS)
wood.save(S/'materials-native/deck-master-native.png');stone.save(S/'materials-native/stone-master-native.png')
def courses(src,seams,size,seed,name):
 """Native crop quilt: use authored full course height, alternate row source and stagger x.
 Ping-pong extension matches the cut-edge pixels, avoiding large repeated tile seams.
 """
 rng=random.Random(seed);out=Image.new('RGBA',size);y=0;records=[];order=list(range(len(seams)-1));rng.shuffle(order);i=0
 while y<size[1]:
  k=order[i%len(order)];y0,y1=seams[k:k+2];row=src.crop((0,y0,src.width,y1));offset=rng.randrange(src.width)
  ribbon=Image.new('RGBA',(src.width*4,row.height))
  for j in range(4):ribbon.alpha_composite(row if j%2==0 else ImageOps.mirror(row),(j*src.width,0))
  h=min(row.height,size[1]-y);out.alpha_composite(ribbon.crop((offset,0,offset+size[0],h)),(0,y));records.append({'sourceRowXYXY':[0,y0,src.width,y1],'nativeDestinationY':y,'height':h,'horizontalOffset':offset,'nativeMirroredExtension':True});y+=row.height;i+=1
 out.save(S/'materials-native'/f'{name}-field-native.png');return out,records
wf,wr=courses(wood,[26,53,80,107,135,162,189,216,243,270,297,324,351,378,405,432,459,486,513,540,567,594,621],(960,656),287,'deck')
sf,sr=courses(stone,[40,88,131,179,224,271,318,367],(1024,1088),940,'stone')
# An intentionally quiet picture-frame timber edge, same material family, no new obstacle.
woodground=blank();woodground.alpha_composite(wf,(1536,1088));frame=Image.new('L',(W,H));d=ImageDraw.Draw(frame)
d.rectangle((1536,1088,2459,1711),outline=255,width=18)
# The foyer doorway and the garden gate stay legible without a crosswise raised border.
d.rectangle((1536,1312,1567,1471),fill=0);d.rectangle((2144,1088,2271,1105),fill=0)
wa=np.asarray(woodground).copy();fa=np.asarray(frame)>0;wa[fa,:3]=np.clip(wa[fa,:3].astype(float)*.83+[3,2,0],0,255);woodground=Image.fromarray(wa)
# Thin 1px joints at inner frame edge, below furniture and never colliding.
d=ImageDraw.Draw(woodground)
for b in [(1553,1105,2442,1694)]:d.rectangle(b,outline=(113,84,48,255),width=1)
# Do not introduce a threshold seam across either admitted door opening.
woodground.paste(wf.crop((0,224,32,384)),(1536,1312));woodground.paste(wf.crop((608,0,736,18)),(2144,1088))
# Outdoor limestone course continues coherently through garden junction and pavilion.
stoneground=blank();stoneground.alpha_composite(sf,(1536,0));foot=Image.open(M/'garden-original-footprint.png').convert('L')
# Interior stone edging stays inside the exact old footprint; grass/foliage never move.
eroded=foot.filter(ImageFilter.MinFilter(17));edge=ImageChops.subtract(foot,eroded);sa=np.asarray(stoneground).copy();ea=np.asarray(edge)>0
sa[ea,:3]=np.clip(sa[ea,:3].astype(float)*.82+[4,6,3],0,255);stoneground=Image.fromarray(sa)
# A thin muted bronze/teal garden border binds the broad pavilion field to its gold rails.
pat=Image.new('L',(W,H));pd=ImageDraw.Draw(pat);pd.rounded_rectangle((1931,75,2388,372),radius=38,outline=255,width=2);pd.rectangle((2064,340,2240,384),fill=0)
pat=ImageChops.multiply(pat,foot);trim=Image.new('RGBA',(W,H),(104,118,92,255));trim.putalpha(pat);stoneground.alpha_composite(trim)
# Replacement ownership is only existing exposed exterior surfaces.
protected=np.asarray(Image.open(M/'protected-objects-and-doors.png'))>0
wm=np.zeros((H,W),bool);wm[1088:1744,1536:2496]=True;wm&=~protected
sm=np.asarray(foot)>0;sm=sm.copy();sm[:,:1536]=False;sm&=~protected
# Door caps and all structural pixels are immutable; no material behind the hall wall is touched.
wmimg=Image.fromarray(wm.astype('uint8')*255);smimg=Image.fromarray(sm.astype('uint8')*255);wmimg.save(M/'deck-owned-pixels.png');smimg.save(M/'garden-stone-owned-pixels.png')
# Recompose inherited shadow shapes over new surfaces. This deliberately changes only
# the underlying material response, never the translucent shadow geometry or color/alpha.
for n in ['coffee-cast-shadow','terrace-shadows-contact']:woodground.alpha_composite(rgba(S/'overlays'/f'{n}.png'))
for n in ['shadows-exterior-cast','pergola-shadows-below']:stoneground.alpha_composite(rgba(S/'overlays'/f'{n}.png'))
for name,surface in [('deck',woodground),('stone',stoneground)]:
 surface.alpha_composite(rgba(S/'overlays/structure-source-alpha.png'));surface.save(S/'overlays'/f'{name}-new-material-under-furniture.png');surface.alpha_composite(rgba(S/'overlays/furniture-below-source-alpha.png'))
base=rgba(S/'frozen-a/runtime-base.png');oldbase=base.copy();above=rgba(S/'frozen-a/runtime-above.png')
base.paste(woodground,(0,0),wmimg);base.paste(stoneground,(0,0),smimg)
base.save(R/'assets/runtime-base.png');above.save(R/'assets/runtime-above.png')
# These are true native art previews: actors are a separate exact unchanged fixture.
actors=rgba(S/'frozen-a/qa-actors-only.png');occupied=base.copy();occupied.alpha_composite(actors);occupied.alpha_composite(above);oldocc=oldbase.copy();oldocc.alpha_composite(actors);oldocc.alpha_composite(above)
empty=base.copy();empty.alpha_composite(above);empty.save(Q/'flagship-b-empty-native.png');occupied.save(Q/'flagship-b-occupied-native.png')
boxes={'terrace':(1536,1056,2496,1760),'coffee':(1600,1072,2368,1312),'path':(1536,368,2304,624),'pavilion':(1920,48,2400,400),'garden':(1408,0,2496,1120),'garden-terrace-join':(2048,944,2368,1184)}
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
for name,box in boxes.items():
 before=oldocc.crop(box);after=occupied.crop(box);before.save(Q/f'flagship-b-{name}-before-native.png');after.save(Q/f'flagship-b-{name}-occupied-native.png')
 board=Image.new('RGB',(before.width*2+60,before.height+100),'#123036');bd=ImageDraw.Draw(board);bd.text((20,14),name.upper()+' / native 1:1 occupied material proof',font=bold(18),fill='#f6dda6');bd.text((20,49),'Frozen corrective A',font=font(15),fill='#cbddda');bd.text((before.width+40,49),'B surface proposal',font=font(15),fill='#cbddda');board.paste(before,(20,80));board.paste(after,(before.width+40,80));board.save(Q/f'{name}-before-after-native.png')
card=Image.new('RGB',(1664,1400),'#123036');d=ImageDraw.Draw(card);d.text((40,24),'FLAGSHIP B / GARDEN MATERIAL PROPOSAL',font=bold(27),fill='#f6dda6');d.text((40,68),'Mellow timber • Outdoor limestone • Framed pavilion • Exact accepted furniture and routes',font=font(20),fill='#cbddda');card.paste(occupied.resize((1584,1188),Image.Resampling.LANCZOS),(40,112));d.text((40,1320),'Local art proposal. Original hall, foyer, reception, opaque furniture and all foreground pixels preserved.',font=font(19),fill='#ebc77f');d.text((40,1355),'Native source crops supplied separately. Static occupied render, not live gameplay. No TMJ compiled.',font=font(17),fill='#b9cfca');card.save(Q/'flagship-b-overview.png')
allowed=wm|sm;diff=np.any(np.asarray(base)!=np.asarray(oldbase),axis=2);furn=np.asarray(Image.open(M/'protected-furniture.png'))>0
checks={'worldPixels':[W,H],'ownedSurfacePixels':int(allowed.sum()),'changedBasePixels':int(diff.sum()),'changesOutsideOwnedSurfacePixels':int((diff&~allowed).sum()),'protectedObjectDoorPixelsChanged':int((diff&protected).sum()),'opaqueFurniturePixelsChanged':int((diff&furn).sum()),'aboveLayerPixelExact':above.tobytes()==rgba(S/'frozen-a/runtime-above.png').tobytes(),'hallAndFoyerPixelExact':base.crop((0,0,1536,H)).tobytes()==oldbase.crop((0,0,1536,H)).tobytes(),'nativeActorFixturePixelExact':True,'translucentObjectEdges':'Recomposited from unchanged source RGBA over new material; no old floor halos.','materialTransform':{'deck':'1254 square to627 square: uniform0.5; native course crops','stone':'1254 square to418 square: uniform1/3; native course crops'},'anisotropicScaleUsed':False,'runtimeCompiled':False,'collisionChanged':False,'published':False,'animationIntegrated':False,'reservedSingleAccentCellXYWH':[1856,640,32,32]}
assert checks['changesOutsideOwnedSurfacePixels']==0 and checks['protectedObjectDoorPixelsChanged']==0 and checks['opaqueFurniturePixelsChanged']==0 and checks['aboveLayerPixelExact'] and checks['hallAndFoyerPixelExact']
write(R/'validation/material-preservation.json',checks);write(S/'material-course-manifest.json',{'deck':wr,'stone':sr});Image.fromarray(allowed.astype('uint8')*255).save(M/'all-owned-surface-pixels.png');print(json.dumps(checks,indent=2))
