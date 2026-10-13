/* Map-specific adapter around unchanged native engine methods, source pin 60e7afdc. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {createNative}=require('./native-runtime-portable.cjs'),N=createNative();
const ROOT=path.resolve(process.argv[2]),layout=JSON.parse(fs.readFileSync(ROOT+'/source/layout.json')),slug=path.basename(ROOT),m=JSON.parse(fs.readFileSync(ROOT+'/map32/'+slug+'.tmj')),g=layout.grid;
const flat=m.layers,props=new Map();for(const ts of m.tilesets)for(const t of ts.tiles||[])props.set(ts.firstgid+t.id,Object.fromEntries((t.properties||[]).map(p=>[p.name,p.value])));
const w=new N.NativeWrapper();w.phaserLayers=flat.filter(l=>l.type==='tilelayer').map((l,i)=>({visible:true,layerIndex:i,layer:{name:l.name,properties:l.properties||[],data:Array.from({length:m.height},(_,y)=>l.data.slice(y*m.width,(y+1)*m.width).map(gid=>({index:gid||-1,properties:props.get(gid&0x1fffffff)||{}})))},setVisible(){return this},setCollisionByProperty(){return this}}));
w.perLayerCollisionGridCache=new Map();w.gameMap={getMap:()=>m};w.mapChangedSubject={next(){}};w.updateCollisionGrid(undefined,false);assert.deepEqual(JSON.parse(JSON.stringify(w.collisionGrid)).map(r=>r.map(v=>v===1?1:0)),g);w.dynamicAreas=new Map();w.enterDynamicAreaCallbacks=[];w.leaveDynamicAreaCallbacks=[];
const mgr=new N.PathfindingManager(w.collisionGrid,{width:32,height:32}),p=new N.NativePlayer();Object.assign(p,{x:layout.start[0],y:layout.start[1],walkingSpeed:9,_lastDirection:3,currentPathSegmentDistanceFromStart:0,body:{height:16,offset:{y:8},setDirectControl(v){this.directControl=v}},getBody(){return this.body},stop(){},setDepth(){},playAnimation(){},emit(){},scene:{markDirty(){}}});
const scene=new N.NativeScene();Object.assign(scene,{CurrentPlayer:p,pathfindingManager:mgr,gameMapFrontWrapper:w,getPathfindingManager:()=>mgr,markDirty(){},userInputManager:{isControlsEnabled:true,isRightClickEnabled:true},getCameraManager:()=>({getCamera:()=>({scrollX:0,scrollY:0})})});
let mapChanges=0;w.getMapChangedObservable=()=>({subscribe(cb){w.mapChangedSubject={next(grid){mapChanges++;cb(grid)}};return{unsubscribe(){}}}});scene.subscribeToGameMapChanged();const pointer=new N.NativePointer();pointer.gameScene=scene;
function body(q){const e=1e-7;for(let y=Math.floor((q.y+e)/32);y<=Math.floor((q.y+16-e)/32);y++)for(let x=Math.floor((q.x-8+e)/32);x<=Math.floor((q.x+8-e)/32);x++)if(g[y]?.[x]!==0)return[x,y];return null;}
const rows=[];let samples=0,framesTotal=0;
async function route(id,start,click,input='desktop'){
 p.finishFollowingPath(true);mgr.cleanup();await N.scheduler.flush();p.x=start[0];p.y=start[1];let frames=0,collisions=0,installs=0;const orig=p.setPathToFollow;p.setPathToFollow=function(...args){installs++;return orig.apply(this,args)};
 pointer.handlePointerUpEvent({x:click[0],y:click[1],wasTouch:input==='touch',leftButtonReleased:()=>false,getDuration:()=>100},[]);await N.scheduler.flush();
 while(p.pathToFollow&&frames++<10000){const old={x:p.x,y:p.y};p.followPath(1000/60);const n=Math.ceil(Math.hypot(p.x-old.x,p.y-old.y)/.5);for(let i=0;i<=n;i++){samples++;if(body({x:old.x+(p.x-old.x)*(n?i/n:1),y:old.y+(p.y-old.y)*(n?i/n:1)}))collisions++;}N.scheduler.now+=1000/60;}
 await N.scheduler.flush();p.setPathToFollow=orig;framesTotal+=frames;const f=mgr.fitBodyWithinTile(...click,32,32),err=Math.hypot(p.x-f.x,p.y-(f.y-16));const row={id,start,click,input,final:[p.x,p.y],frames,pathInstalls:installs,collisions,endpointError:err,pass:!collisions&&err<1e-6&&!p.pathToFollow};rows.push(row);return[p.x,p.y];
}
async function main(){
 for(const [name,start,end] of [['west-east',[808,1007],[856,1007]],['west-west',[856,1007],[808,1007]],['east-east',[1208,1007],[1256,1007]],['east-west',[1256,1007],[1208,1007]]]){
 await route(name+'-approach',layout.start,[start[0],start[1]+16]);
 await route(name,start,[end[0],end[1]+16]);
 }
 const report={legs:rows.length,samples,frames:framesTotal,allPass:rows.every(r=>r.pass),rows};fs.writeFileSync(ROOT+'/validation/conifer-detour-native.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
}
main().catch(e=>{console.error(e);process.exitCode=1});
