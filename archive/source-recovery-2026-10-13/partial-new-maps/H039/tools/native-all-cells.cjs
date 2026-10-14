// Author rerun adapted from the independent native adapter; unchanged pinned methods. No browser or sockets.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const input=JSON.parse(fs.readFileSync(process.argv[2])),output=path.resolve(process.argv[3]);
const fixture=path.resolve(__dirname,'native-fixture'),pin={files:JSON.parse(fs.readFileSync(path.resolve(__dirname,'../source/NATIVE-FIXTURE-PINS.json')))};
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const [f,h] of Object.entries(pin.files))assert.equal(sha(fixture+'/'+f),h,'Pinned native fixture changed: '+f);
const {createNative}=require(fixture+'/native-runtime-portable.cjs'),N=createNative(),g=input.grid,W=input.width,H=input.height;
const mgr=new N.PathfindingManager(g,{width:32,height:32}),p=new N.NativePlayer();
Object.assign(p,{x:0,y:0,walkingSpeed:9,_lastDirection:3,currentPathSegmentDistanceFromStart:0,body:{height:16,offset:{y:8},setDirectControl(){}},getBody(){return this.body},stop(){},setDepth(){},playAnimation(){},emit(){},scene:{markDirty(){}}});
const scene=new N.NativeScene();Object.assign(scene,{CurrentPlayer:p,pathfindingManager:mgr,getPathfindingManager:()=>mgr});
const rows=[];let samples=0;
function blocked(x,y){const e=1e-7;if(x-8<0||x+8>W*32||y<0||y+16>H*32)return true;for(let yy=Math.floor((y+e)/32);yy<=Math.floor((y+16-e)/32);yy++)for(let xx=Math.floor((x-8+e)/32);xx<=Math.floor((x+8-e)/32);xx++)if(g[yy]?.[xx]!==0)return true;return false;}
async function reset(start){p.finishFollowingPath(true);mgr.cleanup();await N.scheduler.flush();p.x=start[0];p.y=start[1];}
async function finish(name,start,click,expected,getError){
 let frames=0,hits=blocked(p.x,p.y)?1:0,localSamples=1;samples++;
 while(p.pathToFollow&&frames++<10000){const a=[p.x,p.y];p.followPath(1000/60);const n=Math.max(1,Math.ceil(Math.hypot(p.x-a[0],p.y-a[1])/.5));for(let k=0;k<=n;k++){samples++;localSamples++;if(blocked(a[0]+(p.x-a[0])*k/n,a[1]+(p.y-a[1])*k/n))hits++;}N.scheduler.now+=1000/60;}
 await N.scheduler.flush();const fit=mgr.fitBodyWithinTile(...click,32,32),nativeFitted=[fit.x,fit.y-16],target=expected||nativeFitted,endpointError=Math.hypot(p.x-target[0],p.y-target[1]);
 const row={name,start,click,expected:target,nativeFitted,final:[p.x,p.y],finalDirection:p._lastDirection,frames,bodySamples:localSamples,bodyCollisionSamples:hits,endpointError,error:getError(),pass:!hits&&!getError()&&endpointError<1e-6&&frames<10000&&!p.pathToFollow};rows.push(row);return row.final;
}
async function route(name,start,click,expected){await reset(start);let error=null;scene.moveTo({x:click[0],y:click[1]}).catch(e=>error=e.message);await N.scheduler.flush();return finish(name,start,click,expected,()=>error);}
async function main(){
 const bounds=input.bounds||[0,0,W*32,H*32],spawn=input.spawn,returnClick=input.returnClick||[spawn[0],spawn[1]+16],returnAnchor=input.returnAnchor;
 for(let y=0;y<H;y++)for(let x=0;x<W;x++)if(!g[y][x]&&x*32+16>=bounds[0]&&x*32+16<bounds[2]&&y*32+16>=bounds[1]&&y*32+16<bounds[3]){
  for(const [dx,dy]of [[16,31],[8,16],[24,16],[8,31],[24,31]]){
   const click=[x*32+dx,y*32+dy],end=await route(`cell-${x}-${y}-${dx}-${dy}`,spawn,click);await route(`return-${x}-${y}-${dx}-${dy}`,end,returnClick,returnAnchor);
  }
 }
 const targets=[...(input.seats||[]),...(input.anchors||[]),...(input.visibleFloor||[]).map(v=>({name:v.name,anchor:v.origin,floorClick:[v.origin[0],v.origin[1]+16]})),...(input.doors||[]).map(d=>({name:d.name,anchor:d.approach,floorClick:d.floorClick||[d.approach[0],d.approach[1]+16]}))];
 for(const [i,start]of [spawn,...(input.spawnOutcomes||[])].entries())for(const t of targets){const end=await route(`spawn-${i} ${t.name}`,start,t.floorClick||[t.anchor[0],t.anchor[1]+16],t.anchor);await route(`spawn-${i} ${t.name} return-to-arrival`,end,returnClick,returnAnchor);}
 // Exercise supersession in the actual pinned path-request methods, not a fake movement implementation.
 const cancellation=[];
 if(targets.length>=2){
  const a=targets[0],b=targets.at(-1);await reset(spawn);let oldError=null,newError=null;
  scene.moveTo({x:a.floorClick?.[0]??a.anchor[0],y:a.floorClick?.[1]??a.anchor[1]+16}).catch(e=>oldError=e.message);
  const click=b.floorClick||[b.anchor[0],b.anchor[1]+16];scene.moveTo({x:click[0],y:click[1]}).catch(e=>newError=e.message);await N.scheduler.flush();
  await finish('superseded move goes to latest target',spawn,click,b.anchor,()=>newError);cancellation.push({case:'two requests before scheduler flush',oldError,newError,pass:rows.at(-1).pass});
 }
 const failures=rows.filter(r=>!r.pass),report={scope:'Author rerun of independent-adapter logic. Historical source-extracted native PathfindingManager/Player/GameScene in a stub scene. All admitted room cells sampled at center and four fit extrema, both directions; explicit targets from supplied spawn outcomes; <=0.5px Euclidean movement sampling with full16x16body. Supplied spawn outcomes are replayed, not independently generated. No browser, keyboard, mobile device, Phaser GPU, gameplay scripting, real autositting or facing proof.',room:input.id,tmj_sha256:input.tmj_sha256,input_sha256:sha(process.argv[2]),fixture_pin:pin.files,body:{width:16,height:16,origin:'x center, y top of collision body; floorClick y is origin+16'},legs:rows.length,samples,failures,cancellation,pass:!failures.length,rows};
 fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({room:input.id,legs:rows.length,samples,failures:failures.length,pass:report.pass}));if(!report.pass)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1});
