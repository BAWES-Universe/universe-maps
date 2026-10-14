"""Native32 sprite preparation from original built-in imagegen master. No map mutation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
from scipy.ndimage import label,binary_dilation,distance_transform_edt,distance_transform_cdt
R=Path(__file__).resolve().parents[1];S=R/'source';Q=R/'review';master=Image.open(S/'leaf-animation-generated-master.png').convert('RGBA');a=np.asarray(master);frames=[];records=[]
# Equal square crops, common617px source side: same proportional scale for every frame.
# Root registrations were measured on the generated matte shadow, not on varying leaf tips.
for i,(rx,ry) in enumerate([(355,494),(361,494),(356,481),(355,481)]):
 px=i%2*637;py=i//2*617;panel=a[py:py+617,px:px+637].copy();lab,n=label(panel[:,:,3]>16);counts=np.bincount(lab.ravel());counts[0]=0;core=lab==counts.argmax();keep=binary_dilation(core,iterations=3);panel[:,:,3]=np.where(keep,panel[:,:,3],0)
 local=Image.fromarray(panel);left=rx-308;top=ry-480;box=(left,top,left+617,top+617);native=local.crop(box).resize((32,32),Image.Resampling.LANCZOS)
 # Remove invisible alpha dust introduced by resampling, never alter the opaque drawing.
 na=np.asarray(native).copy();na[:,:,3]=np.where(na[:,:,3]<4,0,na[:,:,3]);native=Image.fromarray(na);frames.append(native);records.append({'frame':i,'panelXYWH':[px,py,637,617],'measuredRootLocalXY':[rx,ry],'squareCropLocalXYXY':list(box),'uniformScale':32/617,'alphaCleanup':'Keep largest connected generated tuft +3px original-source fringe; native alpha<4→0'})
# Root and lower leaves stay completely stationary. This is a native animation assembly
# constraint, not additional generated artwork: use the exact neutral root pixels.
for i in range(1,4):frames[i].paste(frames[0].crop((0,23,32,32)),(0,23))
strip=Image.new('RGBA',(128,32))
for i,fr in enumerate(frames):strip.alpha_composite(fr,(i*32,0));fr.save(S/'materials-native'/f'garden-leaf-frame-{i}.png')
strip.save(R/'assets/garden-leaf-accent-native.png')
# Static contact sheet includes real1× art and explicitly labelled8× nearest diagnostics.
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';font=lambda s:ImageFont.truetype(F,s);bold=lambda s:ImageFont.truetype(B,s)
board=Image.new('RGB',(1136,470),'#123036');d=ImageDraw.Draw(board);d.text((24,18),'B GARDEN LEAF / four native32 frames',font=bold(23),fill='#f6dda6');d.text((24,55),'Native1× strip:',font=font(16),fill='#cbddda');board.paste(strip,(162,48),strip)
for i,fr in enumerate(frames):
 x=24+i*278;d.text((x,98),f'Frame{i} / {[350,450,350,650][i]}ms',font=font(17),fill='#e6ca91');tile=Image.new('RGBA',(32,32),'#40542c');tile.alpha_composite(fr);board.paste(tile.resize((256,256),Image.Resampling.NEAREST),(x,132))
d.text((24,411),'8× nearest-neighbor diagnostic. Root pixels stay fixed; motion is confined to leaf tips.',font=font(18),fill='#cbddda');d.text((24,442),'Transparent native128×32 atlas. No map integration or live animation claim in this art preview.',font=font(16),fill='#a9c5bf');board.save(Q/'garden-leaf-animation-contact-sheet.png')
# Paused and temporal preview is review-only, never a runtime GIF asset.
gifframes=[]
for fr in frames:
 tile=Image.new('RGBA',(32,32),'#40542c');tile.alpha_composite(fr);gifframes.append(tile.resize((256,256),Image.Resampling.NEAREST).convert('RGB'))
gifframes[0].save(Q/'garden-leaf-motion-review.gif',save_all=True,append_images=gifframes[1:],duration=[350,450,350,650],loop=0,disposal=2)
base=np.asarray(frames[0]);bmask=base[:,:,3]>64;metrics=[]
for i,fr in enumerate(frames):
 v=np.asarray(fr);m=v[:,:,3]>64;dist=max(float(distance_transform_edt(~bmask)[m].max()),float(distance_transform_edt(~m)[bmask].max()));alpha=v[:,:,3]/255;lum=(v[:,:,:3]*[.2126,.7152,.0722]).sum(axis=2);metrics.append({'frame':i,'alphaWeightedMeanLuminance':round(float((alpha*lum).sum()/alpha.sum()),3),'silhouetteMaxDeviationFromNeutralPx':dist,'nontransparentBounds':list(fr.getbbox()),'rootRows23To31Exact':np.array_equal(v[23:],base[23:]),'silhouetteMaxChebyshevDeviationPx':int(max(distance_transform_cdt(~bmask,metric='chessboard')[m].max(),distance_transform_cdt(~m,metric='chessboard')[bmask].max()))})
report={'status':'Native source-prepared original accent; no integration/live-render verification','sourceMasterSize':list(master.size),'nativeAtlasSize':[128,32],'transparent':True,'frameSize':[32,32],'durationMs':[350,450,350,650],'frameRecords':records,'metrics':metrics,'maximumSilhouetteMotionPx':max(q['silhouetteMaxDeviationFromNeutralPx']for q in metrics),'maximumPerAxisSilhouetteMotionPx':max(q['silhouetteMaxChebyshevDeviationPx']for q in metrics),'brightnessRange':max(q['alphaWeightedMeanLuminance']for q in metrics)-min(q['alphaWeightedMeanLuminance']for q in metrics),'stableRootRows':[23,32],'colorOrBrightnessPulsesAdded':False,'anisotropicResize':False}
(S/'leaf-animation-preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='frameRecords'},indent=2))
