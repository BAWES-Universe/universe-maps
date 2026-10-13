import assert from 'node:assert/strict';
import fs from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import {nativeCameraFixture} from './native-camera-model.mjs';
import {installGateCameraB} from './proposal-native-api/gate-camera-b.mjs';
const viewports=[{name:'iphone-small',width:375,height:667,dpr:2},{name:'iphone-medium',width:390,height:844,dpr:3},{name:'iphone-large',width:430,height:932,dpr:3},{name:'iphone-landscape',width:844,height:390,dpr:3},{name:'desktop',width:1280,height:800,dpr:1}];
const results=[];
for(const viewport of viewports)for(const bridgeDelay of [16,80]){
 const f=nativeCameraFixture({...viewport,bridgeDelay,patched:true});
 // Drop all pre-subscription snapshots. Initial close must be independent of these.
 f.advance(bridgeDelay+20);
 const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;
 assert(c.snapshot().started,'cold initialization fetches spawn without a movement event');
 async function tick(){f.advance(16);f.frame();await Promise.resolve();await Promise.resolve();}
 async function idle(frames=50){for(let i=0;i<frames;i++)await tick();}
 let y=1136;async function step(next,moving=true){y=next;f.move(496,y,moving);f.host.setTimeout(()=>c.update({x:496,y:next,moving}),bridgeDelay);await tick();}
 async function travel(target){let sign=Math.sign(target-y);while(Math.abs(target-y)>0.1)await step(sign>0?Math.min(target,y+2):Math.max(target,y-2));}
 await idle();const cold={engine:f.snapshot(),script:c.snapshot()};
 assert(cold.engine.view.width>=416-2&&cold.engine.view.height>=480-2,'close fit uses native actual aspect');
 assert(cold.engine.view.width<Math.max(416,480*viewport.width/viewport.height)+3,'cold fit is not default wide');
 assert.equal(cold.engine.metrics.stopFollowCalls,0);assert.equal(f.camera.follow,f.player);
 await travel(576);await idle();const first={engine:f.snapshot(),script:c.snapshot()};
 assert.equal(first.engine.metrics.stopFollowCalls,0,'no setPosition or stopFollow in moving ascent');assert.equal(f.camera.follow,f.player);
 const before=f.metrics.viewportWrites;await travel(1096);for(let i=0;i<5;i++){await travel(1118);await travel(1096);}
 assert.equal(f.metrics.viewportWrites,before,'retreat and hysteresis boundary retain framing');assert.equal(c.snapshot().cycles,0);
 await travel(1136);await idle(70);assert.equal(c.snapshot().cycles,1);const returned=f.snapshot();
 await travel(576);await idle();const second={engine:f.snapshot(),script:c.snapshot()};
 assert(second.engine.metrics.viewportWrites>first.engine.metrics.viewportWrites+5,'second ascent widens again');
 assert.equal(f.metrics.cameraWrites,0,'all movement framing avoids legacy cameraSet');assert.equal(f.metrics.stopFollowCalls,0);assert.equal(f.metrics.focusCalls,0);assert.equal(f.player.listenerCount('hasMoved'),0);
 const zoom=f.waScaleManager.zoomModifier;f.manual();await travel(1136);await idle();assert.equal(c.snapshot().active,false);assert(Math.abs(f.waScaleManager.zoomModifier/zoom-1)<0.003,'manual opt-out freezes current rendered viewport within native pixel rounding');
 c.dispose();results.push({viewport,bridgeDelay,cold,first,returned,second});
}
const guards=[];
for(const mode of ['Focus','Positioned','Exploration']){const f=nativeCameraFixture({patched:true});f.manager.cameraMode=mode;const z=f.waScaleManager.zoomModifier;f.manager.setViewport(416,480);assert.equal(f.waScaleManager.zoomModifier,z);guards.push(mode);}
for(const key of ['cameraLocked','zoomLocked']){const f=nativeCameraFixture({patched:true});f.manager[key]=true;const z=f.waScaleManager.zoomModifier;f.manager.setViewport(416,480);assert.equal(f.waScaleManager.zoomModifier,z);guards.push(key);}
for(const dimensions of [[0,1],[-1,1],[NaN,1],[Infinity,1],[1,0],[1,NaN],[1e300,1],[1,1e300],[Number.MIN_VALUE,1]]){const f=nativeCameraFixture({patched:true});const z=f.waScaleManager.zoomModifier;f.manager.setViewport(...dimensions);assert.equal(f.waScaleManager.zoomModifier,z);}
{const f=nativeCameraFixture({patched:true});f.camera.setFollowOffset(13,-27);const offset={...f.camera.followOffset},saved=f.waScaleManager.getSaveZoom();f.manager.setViewport(416,480);f.frame();assert.deepEqual(f.camera.followOffset,offset);assert.equal(f.waScaleManager.getSaveZoom(),saved);assert.equal(f.camera.follow,f.player);}
{const f=nativeCameraFixture({patched:true});f.media.matches=true;const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;c.update({x:496,y:1136});f.advance(300);assert.equal(f.metrics.viewportWrites,0);assert.equal(c.snapshot().reason,'reduced-motion');}
{const f=nativeCameraFixture({patched:true});const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;f.advance(100);f.frame();f.media.matches=true;for(const fn of f.media.listeners)fn();assert.equal(c.snapshot().active,false);assert.equal(c.snapshot().reason,'reduced-motion');}
{const f=nativeCameraFixture();const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;c.update({x:496,y:1136});f.advance(100);assert.equal(f.metrics.cameraWrites,0);assert.equal(c.snapshot().reason,'native-viewport-api-unavailable');}
// Native external zoom and orientation changes must release the map controller.
{const f=nativeCameraFixture({patched:true});const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;f.advance(100);f.frame();f.advance(600);f.frame();f.waScaleManager.zoomModifier*=1.4;f.frame();f.advance(20);assert.equal(c.snapshot().active,false);assert.equal(c.snapshot().reason,'manual-or-external-camera');const z=f.waScaleManager.zoomModifier;c.update({x:496,y:800});f.advance(300);assert.equal(f.waScaleManager.zoomModifier,z);}
{const f=nativeCameraFixture({patched:true});const c=installGateCameraB(f.WA,f.host,f.clock);await c.ready;f.advance(100);f.frame();f.advance(600);f.frame();f.updateViewport(844,390);f.advance(20);assert.equal(c.snapshot().active,false);assert.equal(c.snapshot().reason,'viewport-changed');}
{const f=nativeCameraFixture({patched:true});for(const dimensions of [[1,1],[1e6,1e6],[1,1e6],[1e6,1]]){f.manager.setViewport(...dimensions);f.frame();const s=f.snapshot();assert(Number.isFinite(s.zoomModifier)&&s.zoomModifier>0);assert(Number.isFinite(s.view.width)&&Number.isFinite(s.view.height));}}
{const f=nativeCameraFixture({patched:true});f.manager.setViewport(416,480);f.frame();f.manager.zoomByFactor(1.01,false);const z=f.waScaleManager.zoomModifier;f.manager.setViewport(600,800);assert.equal(f.waScaleManager.zoomModifier,z,'even a tiny manual zoom disables framing until map exit');}
{const f=nativeCameraFixture({patched:true});f.manager.setViewport(416,480);f.frame();f.manager.setExplorationMode();f.manager.startFollowPlayer(f.player);const z=f.waScaleManager.zoomModifier;f.manager.setViewport(600,800);assert.equal(f.waScaleManager.zoomModifier,z,'returning from exploration does not let map reclaim camera');}
// Legacy behavior is executed against both full class bodies.
function legacy(patched){const f=nativeCameraFixture({patched});f.manager.setPosition({x:430,y:920,width:600,height:800},0);const positioned=f.snapshot();f.move(496,1120);const resumed=f.snapshot();return{positioned,resumed,trace:f.trace};}
assert.deepEqual(legacy(false),legacy(true));
// Execute the public iframe API method; callbacks/network are explicit adapters.
let source=fs.readFileSync(new URL('./engine-patch/play/src/front/Api/Iframe/camera.ts',import.meta.url),'utf8').replace(/^import[\s\S]*?;\s*$/gm,'');source=stripTypeScriptTypes(source,{mode:'transform'}).replace(/export default new WorkAdventureCameraCommands\(\);/,'').replace(/\bexport\s+/g,'');
const sent=[];class Subject{asObservable(){return this;}next(){}};
const Api=new Function('Subject','IframeApiContribution','sendToWorkadventure','apiCallback',source+';return WorkAdventureCameraCommands;')(Subject,class{},event=>sent.push(event),x=>x);const api=new Api();api.setViewport(416,480);assert.deepEqual(sent.pop(),{type:'cameraViewport',data:{width:416,height:480,smooth:false}});assert.throws(()=>api.setViewport(Infinity,480),RangeError);api.set(1,2,3,4,true,false,0);assert.deepEqual(sent.pop(),{type:'cameraSet',data:{x:1,y:2,width:3,height:4,lock:true,smooth:false,duration:0}});
const report={passed:true,routeCases:results.length,scope:'Full source CameraManager, WaScaleManager and HdpiManager with deterministic Phaser/DOM adapters; actual browser physics is a separate report. No full Universe HUD or physical-device claim.',baseCommit:'f00b3482f23c51976b4b339d7a891cad683d6498',guards,dimensionBoundsAndNativeClamp:true,manualZoomRelease:true,orientationRelease:true,legacyCameraSetUnchanged:true,publicApiExecutionPassed:true,coldStartHasNoMovementOrInitialSnapshot:true,results};fs.writeFileSync(new URL('./NATIVE-API-VERIFICATION.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:true,routeCases:results.length,guards,legacyCameraSetUnchanged:true,coldStartHasNoMovementOrInitialSnapshot:true,movementFollowInterruptions:results.map(x=>x.second.engine.metrics.stopFollowCalls)},null,2));
