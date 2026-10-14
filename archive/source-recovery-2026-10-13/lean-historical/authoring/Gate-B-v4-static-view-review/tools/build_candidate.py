from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1]
V3=Path('/workspace/shared/gate-cinematic-v3/integrated/public/butterfly-town/gate-b/v3')
V2=Path('/workspace/shared/gate-b-map-only-v2/publish/public/butterfly-town/gate-b/v2')
out=R/'publish/public/butterfly-town/gate-b/v4';out.mkdir(parents=True,exist_ok=True)
for p in V3.rglob('*'):
 if p.is_file():
  target=out/p.relative_to(V3);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
baseline=R/'baseline';baseline.mkdir(exist_ok=True)
for name in ['gate.tmj','native-audio/gate-with-native-audio.js']:
 target=baseline/Path(name).name;shutil.copyfile(V3/name,target)
core=(V2/'native-audio/gate-with-native-audio.js').read_text();(R/'source/preserved-portal-audio-core.js').write_text(core)
controller=(R/'source/mobile-static-view.mjs').read_text().replace('export function','function')
script='''/* Gate B v4: the first IIFE is the byte-preserved portal/audio core.
 * Its camera-free comments apply only to that core. One mobile setup follows.
 */
'''+core+'''\n/* Static mobile arrival only. No cinematic, walking-zoom restore or landing reveal. */
(() => {
'''+controller+'''
  let disposed = false, controller;
  window.addEventListener('pagehide', () => { disposed = true; controller?.dispose(); }, {once: true});
  WA.onInit().then(() => {
    if (!disposed) controller = installMobileStaticView(WA, window);
  }).catch(error => console.warn('Gate initial framing unavailable; native camera retained.', error));
})();
'''
(out/'native-audio/gate-with-native-audio.js').write_text(script)
raw=(V3/'gate.tmj').read_text();d=json.loads(raw)
replacements={'campusVersion':'gate-b-v4-static-mobile-view-balconies-32','gateCameraVersion':'Desktop native view; one mobile wide setup; native follow and user zoom thereafter'}
for name,value in replacements.items():
 old=next(x['value']for x in d['properties']if x['name']==name)
 assert raw.count(json.dumps(old))==1
 raw=raw.replace(json.dumps(old),json.dumps(value),1)
(out/'gate.tmj').write_text(raw)
for tree in ['dependencies','geometry-evidence']:
 source=Path('/workspace/shared/gate-cinematic-v3')/tree
 if source.exists():shutil.copytree(source,R/tree,dirs_exist_ok=True)
shutil.copyfile('/workspace/shared/gate-cinematic-v3/GEOMETRY-INTEGRATION-MANIFEST.json',R/'GEOMETRY-INTEGRATION-MANIFEST.json')
shutil.copyfile('/workspace/shared/gate-cinematic-v3/CALIBRATION.md',R/'CALIBRATION-V3-REFERENCE.md')
shutil.copyfile('/workspace/shared/gate-cinematic-v3/MOBILE-DETECTION-EVIDENCE.md',R/'MOBILE-DETECTION-V3-REFERENCE.md')
print('Built separate v4 local candidate. Map changes restricted to two version metadata values and separate script.')
