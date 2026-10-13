from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'rendered-inputs-and-outputs.json').read_text())
p=json.loads((ROOT/'source-calculated-viewports.json').read_text())
greg=Image.open(m['greg']['path']).convert('RGBA').crop(tuple(m['greg']['cropXYXY']))
mask=Image.open(m['shellMask']['path']).convert('L')
checks=[]
for r in m['rendered']:
    vp=r['cssViewport'];scale=r['cssScale'];x=r['spawn']['x'];y=r['spawn']['y']
    frame=(x-16,y-16,x+16,y+16)
    source=Image.open(r['source']).convert('RGBA')
    source.alpha_composite(greg,(x-16,y-16))
    expected=source.crop(tuple(r['worldViewXYXY'])).resize((vp['width'],vp['height']),Image.Resampling.NEAREST)
    actual=Image.open(ROOT/r['viewport']).convert('RGBA')
    assert actual.size==(vp['width'],vp['height'])
    assert ImageChops.difference(expected,actual).getextrema() == ((0,0),(0,0),(0,0),(0,0))
    labeled=Image.open(ROOT/r['labeled']).convert('RGB')
    extracted=labeled.crop(tuple(r['viewportRegionInLabeledXYXY']))
    assert ImageChops.difference(actual.convert('RGB'),extracted).getbbox() is None
    overlap=mask.crop(frame).getbbox()
    assert overlap is None
    left,top,right,bottom=r['worldViewXYXY']
    assert left<=768 and right>=1024
    checks.append({'case':r['case'],'kind':r['kind'],'viewportSizeExact':True,'sourceCropAndNearestCanvasScalePixelExact':True,'labeledViewportRegionPixelExact':True,'nativeGregFrameUnchanged':[32,32],'displayedGregFrame':[32*scale,32*scale],'gregFrameShellAlphaOverlapPixels':0,'fullApproachWidthVisible':True,'entranceModuleHorizontalClippingLeftRight':[max(0,left-576),max(0,1216-right)],'shellAlphaEnvelopeClippingLeftTopRightBottom':[max(0,left-128),max(0,top-112),max(0,1776-right),max(0,2055-bottom)] if r['case']!='entry-reveal-boundary' else None})
for kind in ['portrait','desktop']:
    for name in ['recommended-outside','closer-outside','entry-reveal-boundary']:
        cases=[c for c in p['cases'] if c['kind']==kind and c['name']==name]
        assert len(cases)==3
        assert len({tuple(c['worldViewXYXY']) for c in cases})==1
        assert len({c['cssScale'] for c in cases})==1
hashes={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in ROOT.glob('source-calculated-*-*.png')}
result={'status':'All six source-calculated ordinary-follow image checks passed','sourceOnly':True,'browserUsed':False,'runtimeCameraChanged':False,'publicationPerformed':False,'maskBboxHalfOpen':mask.getbbox(),'dpr1Dpr2Dpr3EquivalentForBothTestedCssViewportSizes':True,'checks':checks,'outputPngSha256':hashes,'visualAssessment':'Doorway, threshold, full approach width and Greg are clearly readable in both normal-follow exterior views. Desktop upper facade clipping and portrait outer-module cropping are disclosed. Revealed examples use the supplied revealed composite.'}
(ROOT/'final-viewport-proof.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':len(hashes),'shellBBox':mask.getbbox()},indent=2))
