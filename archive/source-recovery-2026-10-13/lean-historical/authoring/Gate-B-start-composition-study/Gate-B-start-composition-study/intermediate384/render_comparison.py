from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).parent
src=Path('/workspace/shared/gate-water-visibility-audit/gate-normal-first-frame.png')
scene=Image.open(src).convert('RGBA')
gregsrc=Path('/workspace/shared/recovered-pre-island-package/runtime/assets/greg.png')
greg=Image.open(gregsrc).convert('RGBA').crop((32,96,64,128))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
data=json.loads((R/'viewports.json').read_text()); outputs=[]
for item in data['result']:
 x=item['spawn']['x'];y=item['spawn']['y'];v=item['engine']['view']
 world=scene.copy();world.alpha_composite(greg,(x-16,y-16))
 view=world.crop((v['x'],v['y'],v['x']+v['width'],v['y']+v['height'])).resize((390,844),Image.Resampling.NEAREST)
 hud=Image.new('RGBA',(390,844));d=ImageDraw.Draw(hud);d.rectangle((0,748,389,843),fill=(5,15,24,205));d.text((16,767),'Reserved bottom HUD area: 96px',font=small,fill=(227,237,244,255));d.text((16,787),'Composition study, not the live HUD',font=small,fill=(179,201,215,255))
 view=Image.alpha_composite(view,hud); name='centered-baseline-390.png' if x==496 else 'left-waterfall-start-390.png';view.save(R/name)
 bx=(x-16-v['x'])*390/v['width'];by=(y-16-v['y'])*844/v['height'];bw=32*390/v['width'];bh=32*844/v['height']
 outputs.append({'file':name,'nativeWokaFrame':10,'nativeWokaPixels':[32,32],'sourceSha256':hashlib.sha256(gregsrc.read_bytes()).hexdigest(),'cameraWorldView':v,'screenSpriteBounds':[bx,by,bw,bh],'screenSpriteBottom':by+bh,'hudStartsAt':748,'hudClearancePixels':748-(by+bh),'noSeparateSpriteScaling':True})
board=Image.new('RGB',(812,920),(10,20,27));d=ImageDraw.Draw(board)
for i,o in enumerate(outputs):
 xx=8+i*406;board.paste(Image.open(R/o['file']).convert('RGB'),(xx,58));label='CENTERED BASELINE' if i==0 else 'OFFSET START: X384';d.text((xx,9),label,font=font,fill=(236,226,192));d.text((xx,31),f"390 × 844 viewport · native 32px Woka",font=small,fill=(181,202,215))
d.text((8,905),'Same camera scale and gate pixels; source-composited framing only. No camera-motion or phone claim.',font=small,fill=(182,198,209))
board.save(R/'gate-start-comparison-390.png')
(R/'render-verification.json').write_text(json.dumps({'scope':data['scope'],'outputs':outputs},indent=2)+'\n')
print(json.dumps(outputs,indent=2))
