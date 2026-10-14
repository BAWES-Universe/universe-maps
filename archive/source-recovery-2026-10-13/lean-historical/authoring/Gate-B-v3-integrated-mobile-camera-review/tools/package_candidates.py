from pathlib import Path
import json,shutil,hashlib,difflib,zipfile
R=Path(__file__).resolve().parents[1]
base=Path('/workspace/shared/gate-b-map-only-v2/publish/public/butterfly-town/gate-b/v2')
base_map=json.loads((base/'gate.tmj').read_text())
core=(base/'native-audio/gate-with-native-audio.js').read_text()
reveal=(R/'source/gate-reveal.mjs').read_text().replace('export function','function')
arrival=(R/'source/mobile-arrival-experiment.mjs').read_text().replace('export function','function')
manifest={'status':'LOCAL REVIEW ONLY; no publication','engineRepository':'BAWES-Universe/workadventure-universe','engineRef':'75666c0ccae779515b6fcbd83446ebd1eee29d1b','baseMapSha256':hashlib.sha256((base/'gate.tmj').read_bytes()).hexdigest(),'variants':[]}
for name,mobile in [('stairs-only',False),('mobile-arrival',True)]:
 out=R/'candidates'/name/'public/butterfly-town/gate-b/v3';out.mkdir(parents=True,exist_ok=True)
 for f in base.rglob('*'):
  if f.is_file():
   target=out/f.relative_to(base);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
 scope='/* Gate B v3: the FIRST IIFE below is the preserved Bv2 portal/audio core.\n * Its camera-free comments apply only to that core. Separate v3 camera controllers follow.\n */\n'
 script=scope+core+'\n/* Separate camera-only v3 experiment; v2 portal/audio core above is byte-preserved. */\n(()=>{\n'+reveal+'\n'+(arrival if mobile else '')+'''\nlet disposed=false,revealController,arrivalController;
window.addEventListener('pagehide',()=>{disposed=true;revealController?.dispose();arrivalController?.dispose();},{once:true});
WA.onInit().then(()=>{if(disposed)return;
'''+('arrivalController=installMobileArrivalExperiment(WA,window);\n' if mobile else '')+'''revealController=installGateReveal(WA,window);
}).catch(error=>console.warn('Gate camera experiment unavailable; native camera retained.',error));
})();
'''
 (out/'native-audio/gate-with-native-audio.js').write_text(script)
 d=json.loads(json.dumps(base_map))
 for p in d['properties']:
  if p['name']=='campusVersion':p['value']='gate-b-v3-camera-review-'+name
  if p['name']=='gateCameraVersion':p['value']='Experimental '+('portrait overview then native walking zoom; ' if mobile else '')+'one modest landing reveal, wider zoom held'
 (out/'gate.tmj').write_text(json.dumps(d,separators=(',',':'))+'\n')
 assert d['layers']==base_map['layers'] and d['tilesets']==base_map['tilesets']
 assert (out/'native-audio/assets/gate-music-waterfalls-loop.mp3').read_bytes()==(base/'native-audio/assets/gate-music-waterfalls-loop.mp3').read_bytes()
 (out/'README.md').write_text(f'''# Gate B v3 camera review: {name}

LOCAL EXPERIMENT, NOT A PUBLISHED MAP. This variant preserves Bv2's art, layers, animation, collisions, native audio, and blank editor-configurable destination. Boundary-v3 geometry is a separate candidate and is not merged here.

{'Portrait coarse-pointer devices begin with an authored overview. After 128px of deliberate ascent, native follow restores ordinary walking zoom. ' if mobile else 'Native arrival framing stays unchanged. '}A single modest first-landing reveal then retains its widened zoom for the rest of this map visit. It does not re-arm on returning to the start. It never disables inputs or writes camera position every frame.

Only existing APIs are used. Manual Look Around during the native pan, or before the mobile walking-zoom restoration, can be reclaimed by native follow. This is a known current-platform limitation, not solved here. The small-screen overview can briefly make the avatar approximately 14.5 CSS px in the modeled smallest canvas; the readable alternative is documented in the review filmstrips. Native autoplay/pause/mute/Stop behavior is unchanged from Bv2.

Source-class simulations passed bounded route checks. Full live game HUD, tap pathfinding, real joystick geometry, physical iPhone behavior, and initialization timing have not been verified. Do not present this candidate as production-ready or as a verified mobile fix.
''')
 files=[{'path':str(f.relative_to(out)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(out.rglob('*')) if f.is_file()]
 manifest['variants'].append({'name':name,'map':str(out/'gate.tmj'),'script':str(out/'native-audio/gate-with-native-audio.js'),'files':files,'sameLayersAndTilesets':True,'sameNativeAudioBytes':True,'blankPortal':next(p['value'] for p in d['properties'] if p['name']=='campusRoomUrl')==''})
 (R/(name+'.patch')).write_text(''.join(difflib.unified_diff(core.splitlines(True),script.splitlines(True),fromfile='gate-b/v2/native-audio/gate-with-native-audio.js',tofile='gate-b/v3/native-audio/gate-with-native-audio.js')))
(R/'CANDIDATE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'variants':[v['name'] for v in manifest['variants']],'layerAndTilesetChanges':0,'audioByteChanges':0,'published':False}))
