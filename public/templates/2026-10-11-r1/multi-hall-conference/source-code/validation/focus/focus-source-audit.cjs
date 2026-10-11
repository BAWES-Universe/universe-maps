// Source-executed camera math audit. No DOM/browser renderer, GameScene, networking, map edits or live session.
const fs=require('fs'),vm=require('vm');const repo=process.env.ENGINE_AUDIT_REPO||'/workspace/shared/native32-replan-fix';const ts=require(repo+'/node_modules/typescript/lib/typescript.js');
const P=repo+'/node_modules/phaser/src';
const components=P+'/gameobjects/components';
require.cache[require.resolve(components)]={id:components+'/index.js',filename:components+'/index.js',loaded:true,exports:{AlphaSingle:require(components+'/AlphaSingle'),Visible:require(components+'/Visible'),PostPipeline:{initPostPipeline(){}}}};
const Camera=require(P+'/cameras/2d/Camera'),Emitter=require(repo+'/node_modules/eventemitter3');
function setup(view,dpr,world){
 let size={...view};const element={style:{}};const modules={};let scale;
 const env={console,window:{devicePixelRatio:dpr},Phaser:{Events:{EventEmitter:Emitter},Math:{Clamp:require(P+'/math/Clamp')},Cameras:{Scene2D:{Events:require(P+'/cameras/2d/events')}},Scenes:{Events:{POST_UPDATE:'postupdate',UPDATE:'update',RENDER:'render'}}}};
 const stubs={CoWebsiteStore:{coWebsiteManager:{getGameSize:()=>size}},HtmlUtils:{HtmlUtils:{getElementByIdOrFail:()=>element}},ResizableScene:{ResizableScene:class{}},MapEditorStore:{mapEditorModeStore:{subscribe:cb=>{cb(false);return()=>{}}}},types:{Easing:{SineEaseOut:'Sine.easeOut',QuadEaseOut:'Quad.easeOut'}},Player:{hasMovedEventName:'hasMoved'},UserInputManager:{UserInputEvent:{}},Debuggers:{debugZoom:()=>{}}};
 for(const name of ['HdpiManager','WaScaleManager','CameraManager']) {
  const exports={};const code=ts.transpileModule(fs.readFileSync(__dirname+'/source/'+name+'.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
  vm.runInNewContext(code,{...env,exports,require:p=>{const key=p.split('/').pop();if(modules[key])return modules[key];if(stubs[key])return stubs[key];throw new Error('Missing '+p);}});modules[name]=exports;
 }
 const camera=new Camera(0,0,view.width,view.height);
 const mockScale={width:view.width,height:view.height,zoom:1,canvas:{style:{}},displaySize:{},resize(w,h){this.width=w;this.height=h;camera.setSize(w,h);},setZoom(z){this.zoom=z;},refresh(){}};
 camera.scaleManager=mockScale;camera.sceneManager={customViewports:0};
 const scene={events:new Emitter(),cameras:{main:camera},scale:mockScale,markDirty(){},time:{delayedCall:(n,cb)=>cb()}};
 const game={scale:mockScale,events:new Emitter(),scene:{getScenes:()=>[scene]},markDirty(){}};scene.game=game;
 const wa=new modules.WaScaleManager.WaScaleManager(640*480,196*196);modules.WaScaleManager.waScaleManager=wa;wa.setGame(game);wa.applyNewSize(camera);
 const manager=new modules.CameraManager.CameraManager(scene,world,wa);const player=new Emitter();player.x=768;player.y=512;manager.startFollowPlayer(player);
 function settle(){for(let i=0;i<4;i++){scene.events.emit('postupdate');camera.preRender();}}
 function snapshot(label,target){settle();const v=camera.worldView;return{label,viewport:{...size},dpr,world,zoomModifier:wa.zoomModifier,canvas:{width:mockScale.width,height:mockScale.height,cssWidth:mockScale.canvas.style.width,cssHeight:mockScale.canvas.style.height},scaleZoom:mockScale.zoom,cameraZoom:camera.zoom,worldView:{x:v.x,y:v.y,width:v.width,height:v.height},effectiveCssScale:{x:size.width/(camera.width/camera.zoom),y:size.height/(camera.height/camera.zoom)},targetContains:!target||(v.x<=target.x&&v.y<=target.y&&v.right>=target.x+target.width&&v.bottom>=target.y+target.height)};}
 function focus(rect,margin=0){manager.enterFocusMode({x:rect.x+rect.width/2,y:rect.y+rect.height/2,width:rect.width,height:rect.height},margin,0);settle();}
 function resize(next){size={...next};wa.applyNewSize();wa.refreshFocusOnTarget();settle();}
 function follow(){manager.leaveFocusMode(player,0);settle();}
 return{focus,resize,follow,snapshot,manager,wa,camera,player};
}
const mobile={width:390,height:844},landscape={width:844,height:390},desktop={width:1440,height:900};
const layout=JSON.parse(fs.readFileSync(__dirname+'/../../source/layout.json'));
const world={width:3072,height:2048},rooms=[];
for(const room of layout.focus){const [x,y,width,height]=room.rect,rect={x,y,width,height},needed={...rect},fresh=[],manual=[],rotations=[];
for(const dpr of [1,2,3])for(const[name,view]of[['portrait',mobile],['landscape',landscape],['desktop',desktop]]){const f=setup(view,dpr,world);f.player.x=x+width/2;f.player.y=y+height/2;f.focus(rect,.15);const shot=f.snapshot(name,needed);shot.avatarCssHeight=32*shot.effectiveCssScale.y;fresh.push(shot);f.manager.zoomByFactor(1.2,false);manual.push({name,dpr,before:shot.zoomModifier,after:f.snapshot('manual',needed).zoomModifier});}
for(const[name,from,to]of[['portrait-to-landscape',mobile,landscape],['landscape-to-portrait',landscape,mobile]]){const f=setup(from,1,world);f.focus(rect,.15);const before=f.snapshot('before',needed);f.resize(to);const after=f.snapshot('after',needed);rotations.push({name,before,after});}
rooms.push({id:room.id,rect,needed,fresh,manual,rotations,allFreshContain:fresh.every(x=>x.targetContains),manualZoomAvailable:manual.every(x=>x.before!==x.after),rotationPass:rotations.every(x=>x.after.targetContains)});}
const out={sourceHead:'60e7afdc3f96ef32525597cd46bd41175d61a2ef',scope:'Exact native camera classes and actual Phaser camera math with explicit scene/store/DOM doubles. Source illustration, not browser/device/live evidence.',world,margin:.15,rooms,allFreshContain:rooms.every(r=>r.allFreshContain),manualZoomAvailable:rooms.every(r=>r.manualZoomAvailable),rotationPass:rooms.every(r=>r.rotationPass)};fs.writeFileSync(__dirname+'/focus-results.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({allFreshContain:out.allFreshContain,manualZoomAvailable:out.manualZoomAvailable,rotationPass:out.rotationPass,rooms:rooms.map(r=>({id:r.id,portraitAvatarCssHeight:r.fresh[0].avatarCssHeight}))},null,2));
