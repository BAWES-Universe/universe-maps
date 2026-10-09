"""Audit actual native browser captures against unchanged sprite and frozen layers."""
from pathlib import Path
from PIL import Image
import hashlib,json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runtime-work/results'
ORDER=['floor','environment','rugs','objects','foreground','glass','overhead-shade','labels']
LAYERS={n:Image.open(ROOT/'layers'/f'office-v2-{n}.png').convert('RGBA') for n in ORDER}
SHEET=Image.open(ROOT/'runtime-work/assets/greg.png').convert('RGBA')


def main():
    frozen=json.loads((ROOT/'docs/RUNTIME-LAYER-FREEZE-03.json').read_text())
    hashes=[{'path':p,'unchanged':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha} for p,sha in frozen['files'].items()]
    checks=[]
    for state_path in sorted(OUT.glob('*-state.json')):
        state=json.loads(state_path.read_text());name=state_path.name[:-11]
        image_path=OUT/(name+'-native-1x.png')
        if not image_path.exists():continue
        actual=Image.open(image_path).convert('RGB')
        p,c=state['player'],state['camera'];x,y=round(p['x']),round(p['y']);sx,sy=round(c['scrollX']),round(c['scrollY'])
        frame=p['frame'];sprite=SHEET.crop(((frame%3)*32,(frame//3)*32,(frame%3)*32+32,(frame//3)*32+32))
        head=np.array(sprite)[:14,:,3]>0;opaque_head=np.array(sprite)[:14,:,3]>=250
        box=(x-16,y-16,x+16,y+16);alpha=np.array(LAYERS['foreground'].crop(box))[:14,:,3]
        other_opaque=np.zeros((14,32),dtype=bool)
        for n in ['glass','labels']:other_opaque|=np.array(LAYERS[n].crop(box))[:14,:,3]>=128
        expected=Image.new('RGBA',(1024,704),(12,32,41,255))
        view=(sx,sy,sx+1024,sy+704)
        for n in ORDER[:4]:expected.alpha_composite(LAYERS[n].crop(view))
        expected.alpha_composite(sprite,(x-16-sx,y-16-sy))
        for n in ['foreground','glass']:expected.alpha_composite(LAYERS[n].crop(view))
        unshaded=expected.copy()
        expected.alpha_composite(LAYERS['overhead-shade'].crop(view))
        for n in ['labels']:
            expected.alpha_composite(LAYERS[n].crop(view));unshaded.alpha_composite(LAYERS[n].crop(view))
        crop=(x-16-sx,y-16-sy,x+16-sx,y+16-sy)
        seen=np.array(actual.crop(crop)).astype(int);predicted=np.array(expected.convert('RGB').crop(crop)).astype(int)
        without=np.array(unshaded.convert('RGB').crop(crop)).astype(int)
        difference=np.abs(seen-predicted);tint=np.max(np.abs(predicted-without),axis=2)
        head_error=difference[:14][opaque_head]
        # Browser premultiplied-alpha rounding differs from Pillow by up to1 RGB
        # level in current captures. Require a robust expected6-level tint and
        # an observed3-level tint, alongside the independent <=3 RGB match check.
        tinted_head=(tint[:14]>=6)&opaque_head
        tint_seen=np.max(np.abs(seen-without),axis=2)[:14]>=3
        check=dict(name=name,player={'x':x,'y':y,'frame':frame},nativeCanvas=list(actual.size),nativeSprite=[p['width'],p['height']],scale=[p['scaleX'],p['scaleY']],
                   headPixels=int(head.sum()),hardForegroundHeadOverlap=int((head&(alpha>0)).sum()),otherOpaqueHeadOverlap=int((head&other_opaque).sum()),
                   opaqueHeadPixels=int(opaque_head.sum()),actualHeadMaxChannelError=int(head_error.max()) if head_error.size else None,
                   actualHeadMeanChannelError=float(head_error.mean()) if head_error.size else None,
                   sourceShadeHeadPixels=int(tinted_head.sum()),observedShadeHeadPixels=int((tinted_head&tint_seen).sum()),
                   shadeDeltaThreshold={'predicted':6,'observed':3},
                   shadeAppliedAtNativeAlpha=next(l['alpha'] for l in state['layers'] if l['name']=='office-overhead-shade')==1)
        check['headAndShadePassed']=check['hardForegroundHeadOverlap']==0 and check['otherOpaqueHeadOverlap']==0 and (check['actualHeadMaxChannelError'] or 0)<=3 and check['sourceShadeHeadPixels']==check['observedShadeHeadPixels'] and check['shadeAppliedAtNativeAlpha']
        checks.append(check)
        # Native crop for convenient visual review. No image rescaling.
        tight=(max(0,x-sx-128),max(0,y-sy-112),min(1024,x-sx+128),min(704,y-sy+112))
        actual.crop(tight).save(OUT/(name+'-tight-native-1x.png'))
    report=dict(status='pass' if checks and all(c['headAndShadePassed'] for c in checks) and all(h['unchanged'] for h in hashes) else 'needs review',
                checks=checks,sourceFreeze=hashes,
                scope='Actual Phaser canvas captures compared with the frozen RGBA layer stack and unchanged directional Greg pixels. Top14 sprite rows are protected heads. Low-alpha overhead shade is intentional color tint; opaque furniture foreground must not cut these pixels.')
    (OUT/'native-pixel-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'captures':len(checks),'failed':[c for c in checks if not c['headAndShadePassed']],'shadeHeadPixels':sum(c['observedShadeHeadPixels'] for c in checks),'frozenSourcesUnchanged':all(h['unchanged'] for h in hashes)},indent=2))


if __name__=='__main__':main()
