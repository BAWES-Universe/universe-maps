#!/usr/bin/env python3
"""Compare real directional Woka head alpha against the assembled foreground."""
import hashlib,json
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parent
ART=ROOT.parents[1]
g=json.loads((ROOT/'source-coordinate-geometry.json').read_text())
sprite_path=Path('../universe-native-team-fixture/assets/greg-reference.png')
fg_path=ART/'layers/office-v2-foreground.png'
sheet=Image.open(sprite_path).convert('RGBA');fg=Image.open(fg_path).convert('RGBA')
frames={'south':1,'west':4,'east':7,'north':10};checks=[]
for goal in g['goals']:
 if goal['kind']=='checkpoint':continue
 frame=frames[goal['facing']];sx=(frame%3)*32;sy=(frame//3)*32
 head=np.array(sheet.crop((sx,sy,sx+32,sy+14)))[:,:,3]>0
 x=goal['x']+32-16;y=goal['y']+32-16
 alpha=np.array(fg.crop((x,y,x+32,y+14)))[:,:,3]
 overlap=int((head&(alpha>0)).sum())
 checks.append(dict(id=goal['id'],facing=goal['facing'],protectedHeadOpaquePixels=int(head.sum()),
                    protectedHeadForegroundPixels=overlap,passed=overlap==0))
failed=[v for v in checks if not v['passed']]
report=dict(status='failed' if failed else 'passed',testCount=len(checks),failedCount=len(failed),checks=checks,
            foreground=dict(path=str(fg_path),sha256=hashlib.sha256(fg_path.read_bytes()).hexdigest()),
            sprite=dict(path=str(sprite_path),sha256=hashlib.sha256(sprite_path.read_bytes()).hexdigest(),frameSize=32,scale=1),
            scope='Actual directional Woka alpha in upper14sprite rows against assembled furniture foreground. Separate low-alpha overhead shade intentionally tints actors and is not treated as a clipping occluder.')
(ROOT/'assembled-head-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],count=len(checks),failures=failed),indent=2))
raise SystemExit(bool(failed))
