from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import numpy as np
r=Path(__file__).resolve().parents[1];p=r/'celestial-transit-garden';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();j=json.loads((p/'source/layout.json').read_text());g=np.array(j['grid']);reg=[]
for x,y in [(744,815),(728,864),(824,815),(760,847),(1240,815),(1320,815),(1304,847),(792,544),(696,512),(1352,512),(888,448),(1160,448),(584,975),(600,975),(648,1007),(1456,975),(632,480),(1416,480),(600,864),(1448,864)]:
 clear=not g[y//32:(y+15)//32+1,(x-8)//32:(x+7)//32+1].any();reg.append({'origin':[x,y],'bodyClear':bool(clear)})
assert not any(a['bodyClear'] for a in reg),reg
(p/'validation/old-visual-blocker-regressions.json').write_text(json.dumps({'allBlocked':True,'cases':reg},indent=2))
reports={n:json.loads((p/'validation'/n).read_text()) for n in ['geometry.json','native-routes.json','spawn-domains.json','exact-collision-delta.json','conifer-detour-native.json','preservation-delta.json','depth-partition.json','full-portal-fixture-audit.json']}
assert reports['geometry.json']['allPass'] and reports['native-routes.json']['allPass'] and reports['spawn-domains.json']['allPass']
receipt={'revision':'celestial-expanded-r4','status':'candidate pending independent full-footprint review','published':False,'engineChanged':False,'runtimeFiles':{f.name:sha(f) for f in (p/'map32').iterdir() if f.is_file()},'geometry':{k:reports['geometry.json'][k] for k in ['walkableCells','reachableCells','unreachableCells','anchorCount','headConflicts','allPass']},'nativeMovement':{k:reports['native-routes.json'][k] for k in ['legs','samples','frames','failures','allPass']},'collisionDelta':reports['exact-collision-delta.json'],'depthPartition':reports['depth-partition.json'],'oldBlockersAllBlocked':True,'detourNative':{k:reports['conifer-detour-native.json'][k] for k in ['legs','samples','frames','allPass']},'quietPass':reports['spawn-domains.json']['allPass'],'fullPortalFixtureAuditPass':reports['full-portal-fixture-audit.json']['allPass'],'physicalFixtureGroups':len(reports['full-portal-fixture-audit.json']['fixtureGroups'])}
(r/'CANDIDATE-RECEIPT.json').write_text(json.dumps(receipt,indent=2))
rt=r/'celestial-expanded-r4-runtime.zip';st=r/'celestial-expanded-r4-source.zip'
with zipfile.ZipFile(rt,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((p/'map32').iterdir()):
  if f.is_file():z.write(f,'map32/'+f.name)
 z.write(r/'README.md','README.md')
sourceNames=['final-composite.png','layout.json','expanded-r2-layout.json','portal-environment-garden-boundaries-master.png','preservation-alpha.png','celestial-transit-garden.tmj','celestial-transit-garden.wam','scenery-collision-repair.json','GENERATION-PROVENANCE.md']
with zipfile.ZipFile(st,'w',zipfile.ZIP_DEFLATED) as z:
 for directory in ['tools','celestial-transit-garden']:
  for f in sorted((r/directory).rglob('*')):
   if f.is_file() and '__pycache__' not in str(f):z.write(f,str(f.relative_to(r)))
 for n in sourceNames:z.write(r/'source'/n,'source/'+n)
 for n in ['README.md','CANDIDATE-RECEIPT.json','conifer-detour-occupied-proof.png']:z.write(r/n,n)
f={'revision':'celestial-expanded-r4','runtimeArchive':str(rt),'runtimeSHA256':sha(rt),'sourceArchive':str(st),'sourceSHA256':sha(st),'receiptSHA256':sha(r/'CANDIDATE-RECEIPT.json'),'rawCharacterSheetsExcluded':True,'status':'immutable candidate awaiting independent review'};(r/'CANDIDATE-FREEZE.json').write_text(json.dumps(f,indent=2));print(json.dumps(f))
