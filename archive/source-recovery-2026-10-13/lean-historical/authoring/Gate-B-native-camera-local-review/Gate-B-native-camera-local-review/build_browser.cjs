const fs=require('node:fs'),path=require('node:path'),{stripTypeScriptTypes}=require('node:module'),crypto=require('node:crypto');
const root=__dirname,out=path.join(root,'browser'),vendor=path.join(out,'vendor');fs.mkdirSync(vendor,{recursive:true});
function source(name){return fs.readFileSync(path.join(root,'pinned-source',name+'.ts'),'utf8');}
function body(name){const text=name==='CameraManager'?fs.readFileSync(path.join(root,'engine-patch/play/src/front/Phaser/Game/CameraManager.ts'),'utf8'):source(name);return stripTypeScriptTypes(text.replace(/^import[\s\S]*?;\s*$/gm,''),{mode:'transform'});}
fs.writeFileSync(path.join(vendor,'HdpiManager.mjs'),body('HdpiManager'));
fs.writeFileSync(path.join(vendor,'WaScaleManager.mjs'),`import {HdpiManager} from './HdpiManager.mjs';
const coWebsiteManager={getGameSize:()=>globalThis.gateNativeViewport};
const HtmlUtils={getElementByIdOrFail:id=>document.getElementById(id)};
const ResizableScene=Phaser.Scene;
`+body('WaScaleManager'));
fs.writeFileSync(path.join(vendor,'CameraManager.mjs'),`import {waScaleManager,WaScaleManagerEvent} from './WaScaleManager.mjs';
const mapEditorModeStore={subscribe:fn=>{fn(false);return()=>{};}};
const Easing={SineEaseOut:'Sine.easeOut'},hasMovedEventName='hasMoved',UserInputEvent={},debugZoom=()=>{},Clamp=Phaser.Math.Clamp;
const HtmlUtils={getElementByIdOrFail:id=>document.getElementById(id),querySelectorOrFail:q=>document.querySelector(q)};
`+body('CameraManager'));
for(const file of ['phaser.js','AnimatedTiles.js'])fs.copyFileSync('/workspace/shared/gate-b-native-proof/vendor/'+file,path.join(vendor,file));
fs.copyFileSync('/workspace/shared/magical-campus-return-08/validation-work/easystar-0.4.4.js',path.join(vendor,'easystar.js'));
fs.copyFileSync('/workspace/shared/magical-campus-return-08/validation-work/native-path-model.mjs',path.join(vendor,'native-path-model.mjs'));
for(const file of ['native-path-model.mjs','native-velocity-model.mjs']) { const text=fs.readFileSync('/workspace/shared/magical-campus-return-08/validation-work/'+file,'utf8').replace('const WOKA_SPEED=6,','const WOKA_SPEED=9,'); fs.writeFileSync(path.join(vendor,file),text); }
fs.mkdirSync(path.join(out,'assets'),{recursive:true});fs.copyFileSync('/workspace/shared/gate-b-native-proof/assets/greg.png',path.join(out,'assets/greg.png'));
const mapOut=path.join(out,'public/butterfly-town/gate-b/v2');fs.mkdirSync(mapOut,{recursive:true});
fs.cpSync('/workspace/shared/gate-b-native-audio-v2/checkpoints/audio-only-v2/publish/public/butterfly-town/gate-b/v2',mapOut,{recursive:true});
fs.copyFileSync(path.join(root,'proposal-native-api/gate-camera-b.mjs'),path.join(mapOut,'native-audio/gate-camera-b.mjs'));
const v6=path.join(out,'public/butterfly-town/v6');if(!fs.existsSync(v6))fs.symlinkSync('/workspace/shared/recovered-campus06/public/butterfly-town/v6',v6,'dir');
fs.copyFileSync('/workspace/shared/gate-b-experience/publish/public/butterfly-town/gate-b/v1/native-audio/gate-camera-b.mjs',path.join(out,'baseline-camera.mjs'));
const manifest={engineCommit:'f00b3482f23c51976b4b339d7a891cad683d6498',scope:'Complete native CameraManager, WaScaleManager and HdpiManager classes; actual Phaser; source-extracted native input/path/player. Test page controls, no full Universe HUD/auth/network.',files:['CameraManager','WaScaleManager','HdpiManager','GameScene','Player'].map(name=>({name,sha256:crypto.createHash('sha256').update(source(name)).digest('hex')}))};
fs.writeFileSync(path.join(root,'SOURCE-MANIFEST.json'),JSON.stringify(manifest,null,2)+'\n');
console.log('Built pinned native browser camera classes and isolated test map.');
