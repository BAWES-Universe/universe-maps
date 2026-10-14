from PIL import Image,ImageDraw,ImageChops
from pathlib import Path
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;C=R.parent/'candidate';S=Path('/workspace/shared/recovered-pre-island-package/sources');W,H=2944,2624
base=Image.open(C/'layers/campus-base.png').convert('RGBA')
under=Image.new('RGBA',(W,H));manifest=[]
def paste(source,box,at,reason,mirror=False,poly=None):
 im=Image.open(S/source).convert('RGBA').crop(tuple(box))
 if mirror:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if poly:
  m=Image.new('L',im.size);ImageDraw.Draw(m).polygon(poly,fill=255);im.putalpha(ImageChops.multiply(im.getchannel('A'),m))
 under.alpha_composite(im,tuple(at))
 manifest.append({'source':str(S/source),'sourceCrop':box,'destination':at,'scale':1,'mirrorHorizontal':mirror,'localAlphaPolygon':poly,'purpose':reason})
# A single continuous planted strip provides the second edge of the western promenade.
paste('west-garden/west-base.png',[192,0,416,1024],[512,0],'continuous west promenade planting; original native garden bank',True)
# Roofline planting uses long different source runs, rather than cloned small bushes.
paste('avenue/avenue-base.png',[0,0,704,144],[512,0],'northwest wooded roofline')
paste('court/court-base.png',[864,0,1472,144],[1216,0],'northern wooded roofline')
# Larger continuous forest cuts follow a finite wooded boundary around the meeting wing.
paste('avenue/avenue-base.png',[896,0,1472,576],[1744,0],'continuous northeast woodland')
paste('court/court-base.png',[928,64,1472,384],[2176,288],'native forest slope joining upper and eastern boundary',poly=[(0,0),(224,0),(304,48),(384,96),(488,192),(544,288),(544,320),(0,320)])
paste('court/court-base.png',[864,64,1472,384],[2192,544],'eastern forest bank behind meeting gallery',poly=[(0,0),(480,0),(528,32),(552,80),(568,128),(544,192),(584,240),(584,320),(0,320)])
paste('court/court-base.png',[864,512,1472,704],[2192,864],'lower forest bank meeting preserved garden foundation',poly=[(0,0),(568,0),(592,64),(576,128),(536,192),(0,192)])
# Organic outer contour is a fixed cutout, not a new texture or a color treatment.
shape=Image.new('L',(W,H));d=ImageDraw.Draw(shape)
d.rectangle((512,0,735,1023),fill=255);d.rectangle((512,0,1759,95),fill=255)
outer=[(1744,0),(2160,0),(2184,32),(2232,64),(2224,112),(2272,144),(2264,192),(2304,224),(2320,272),(2360,304),(2344,336),(2400,352),(2424,392),(2480,408),(2464,448),(2544,464),(2592,496),(2640,512),(2664,552),(2696,576),(2680,624),(2728,656),(2744,688),(2728,752),(2760,784),(2752,824),(2784,864),(2768,912),(2744,960),(2752,1008),(2728,1056),(2192,1056),(1744,592)]
d.polygon(outer,fill=255)
g=json.loads((C/'map/collision-grid.json').read_text());grid=np.zeros((g['height'],g['width']),np.uint8);grid.flat[g['blockedIndices']]=1;blocked=np.repeat(np.repeat(grid,8,0),8,1)
ba=np.array(base)[:,:,3];ua=np.array(under)
allowed=(ba==0)&(blocked==1)&(np.array(shape)>0)
ua[:,:,3]=np.where(allowed,ua[:,:,3],0)
under=Image.fromarray(ua);under.save(R/'terrain-underlay-native.png')
# Separate proposed replacement for the duplicated market promenade stripe.
market=Image.open(S/'market/market-base.png').convert('RGBA');patch=Image.new('RGBA',(1120,96));marketops=[]
for xx,ww in [(0,704),(704,416)]:
 # Keep the current source floor pixels below the duplicate stripe exactly.
 box=(0,224,ww,320);patch.alpha_composite(market.crop(box),(xx,0))
 marketops.append({'source':str(S/'market/market-base.png'),'sourceCrop':list(box),'destination':[1760+xx,2288],'scale':1,'purpose':'preserve current forecourt floor'})
 box=(0,256,ww,288);patch.alpha_composite(market.crop(box),(xx,0))
 marketops.append({'source':str(S/'market/market-base.png'),'sourceCrop':list(box),'destination':[1760+xx,2288],'scale':1,'purpose':'replace only extra32px ornamental stripe with its own native clear paving'})
patch.save(R/'market-forecourt-proposed.png')
# One actual composition preview; no writes to the candidate or its source layers.
flat=Image.new('RGBA',(W,H),(12,32,41,255));flat.alpha_composite(under);flat.alpha_composite(base);flat.alpha_composite(patch,(1760,2288))
for n in ['foreground','glass','shade']:flat.alpha_composite(Image.open(C/f'layers/campus-{n}.png').convert('RGBA'))
flat.save(R/'campus-landscape-composite-native.png');flat.resize((1472,1312),Image.Resampling.LANCZOS).save(R/'campus-landscape-composite-half.png')
sourcepaths={p['source']for p in manifest+marketops};j={'canvas':[W,H],'underlay':'terrain-underlay-native.png','renderBelow':'candidate/layers/campus-base.png','nativeScale':1,'resizesInDeliverable':0,'newArtGeneration':False,'candidateFilesChanged':False,'collisionChanged':False,'sourceCrops':manifest,'outerBoundaryPolygon':outer,'alphaPolicy':'Preserve source RGB; alpha only where current campus-base alpha is exactly0 AND current8px collision grid is blocked. Clear all existing module or walkable pixels.','marketProposal':{'file':'market-forecourt-proposed.png','destination':[1760,2288],'size':[1120,96],'status':'proposal only; not applied to candidate','purpose':'replace only extra promenade with clear native sandstone; retain the original market stripe once','operations':marketops},'preview':'campus-landscape-composite-half.png','previewIncludesMarketProposal':True,'sourceHashes':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sorted(sourcepaths)},'candidateBaseSha256':hashlib.sha256((C/'layers/campus-base.png').read_bytes()).hexdigest(),'collisionSha256':hashlib.sha256((C/'map/collision-grid.json').read_bytes()).hexdigest(),'verification':{'underlayNontransparentPixels':int((ua[:,:,3]>0).sum()),'underlayPixelsOverExistingArt':int(((ua[:,:,3]>0)&(ba>0)).sum()),'underlayPixelsOverWalkableCells':int(((ua[:,:,3]>0)&(blocked==0)).sum()),'retainedPixelColorChanges':0}}
(R/'source-crop-manifest.json').write_text(json.dumps(j,indent=2));print(json.dumps(j['verification']))
