import json, math
from pathlib import Path
root=Path(__file__).resolve().parent
rows=[]
for path in sorted((root/'browser/results').glob('*-routes.json')):
    r=json.loads(path.read_text());m=r['metrics'];stages={s['name']:s for s in r['stages']}
    cold=stages['spawn']['state'];last=r['controller'];first=stages['tap-up']['state'];second=stages['repeat-tap-up']['state']
    frames=[v for v in r['trace'] if v['type']=='frame'];backsteps=0;max_jump=0
    for a,b in zip(frames,frames[1:]):
        if a.get('moving') and b.get('moving') and b['y']<a['y'] and a['mode']==b['mode']=='Follow':
            if b['view']['w']<a['view']['w']-2:backsteps+=1
            max_jump=max(max_jump,abs(b['view']['w']-a['view']['w']))
    row={'file':path.name,'viewport':r['viewport'],'errors':r['errors'],'metrics':m,'coldWidth':cold['camera']['worldView']['width'],'coldHeight':cold['camera']['worldView']['height'],'firstWidth':first['camera']['worldView']['width'],'secondWidth':second['camera']['worldView']['width'],'rearmCount':last['cycles'],'movingUpZoomBacksteps':backsteps,'largestSampledWidthStep':max_jump,'fullUniverseHudTested':False,'physicalIPhoneTested':False}
    row['mechanismPassed']=not r['errors'] and m['movingPositionedFrames']==0 and m['nativeTargetMismatchFrames']==0 and m['maxNativeFollowScrollResidual']<=1.01 and last['cycles']>=2 and backsteps==0
    rows.append(row)
report={'scope':'Real Phaser and complete pinned native CameraManager/scale classes, source path/player/input methods, synthetic touch/joystick; visible test controls are not full Universe HUD. Width-step smoothness is reported separately from preserving Follow.','cases':rows,'mechanismPassed':bool(rows) and all(r['mechanismPassed'] for r in rows)}
(root/'BROWSER-VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
