const fs=require('fs'),assert=require('assert/strict');const {createNative}=require('./native-runtime-portable.cjs');
const m=JSON.parse(fs.readFileSync(__dirname+'/../runtime/moonlit.tmj'));const rows=[];
async function run(name,start,end,{closed=false,replan=false}={}){
 const N=createNative(),w=new N.NativeWrapper(),props=new Map();for(const ts of m.tilesets)for(const t of ts.tiles||[])props.set(ts.firstgid+t.id,Object.fromEntries((t.properties||[]).map(p=>[p.name,p.value])));
 w.phaserLayers=m.layers.filter(l=>l.type==='tilelayer').map((l,i)=>({visible:l.visible!==false,layerIndex:i,layer:{name:l.name,properties:l.properties||[],data:Array.from({length:m.height},(_,y)=>l.data.slice(y*m.width,(y+1)*m.width).map(gid=>({index:gid||-1,properties:props.get(gid)||{}})))},setVisible(v){this.visible=v;return this},setCollisionByProperty(p,v){this.collisionEnabled=v;return this}}));
 w.perLayerCollisionGridCache=new Map();w.gameMap={getMap:()=>m};w.mapChangedSubject={next(){}};w.updateCollisionGrid(undefined,false);w.setLayerVisibility('door-collision',closed);assert.equal(w.collisionGrid[13][13],closed?1:0);
 const p=new N.NativePlayer();Object.assign(p,{x:start[0],y:start[1],walkingSpeed:9,_lastDirection:3,currentPathSegmentDistanceFromStart:0,body:{height:16,offset:{y:8},setDirectControl(v){this.directControl=v}},getBody(){return this.body},stop(){},setDepth(){},playAnimation(){},emit(){},scene:{markDirty(){}}});
 const mgr=new N.PathfindingManager(w.collisionGrid,{width:32,height:32}),scene=new N.NativeScene();Object.assign(scene,{CurrentPlayer:p,pathfindingManager:mgr,gameMapFrontWrapper:w,getPathfindingManager:()=>mgr,markDirty(){}});w.getMapChangedObservable=()=>({subscribe(cb){w.mapChangedSubject={next:cb};return{unsubscribe(){}}}});scene.subscribeToGameMapChanged();
 const moving=scene.moveTo({x:end[0],y:end[1]},false);await N.scheduler.flush();let frames=0,collisions=0;
 while(p.pathToFollow&&frames++<4000){p.followPath(1000/60);if(replan&&frames===2){w.setLayerVisibility('door-collision',true);w.setLayerVisibility('roof-alpha-4',true);await N.scheduler.flush()}
  for(let yy=Math.floor((p.y+1e-6)/32);yy<=Math.floor((p.y+16-1e-6)/32);yy++)for(let xx=Math.floor((p.x-8+1e-6)/32);xx<=Math.floor((p.x+8-1e-6)/32);xx++)if(w.collisionGrid[yy]?.[xx]===1)collisions++;
 }
 await N.scheduler.flush();const fit=mgr.fitBodyWithinTile(end[0],end[1],32,32),reached=Math.hypot(p.x-fit.x,p.y-(fit.y-16))<.01;assert.equal(reached,true,name);assert.equal(collisions,0,name+' collision');rows.push({name,reached,frames,collisions,closed,replan,final:[p.x,p.y]});
}
(async()=>{const points={garden:[448,720],pavilion:[448,304],terrace:[944,432],deskApproach:[240,304],seatApproach:[592,352]};
for(const closed of [false,true])for(const [a,start] of Object.entries(points))for(const[b,end]of Object.entries(points))if(a!==b)await run(a+' to '+b+(closed?' closed':' open'),start,end,{closed});
await run('close/reveal during approach reroutes via side passage',[448,720],[448,304],{replan:true});
fs.writeFileSync(__dirname+'/native-results.json',JSON.stringify({engineHead:'aa3ca1d60801172bfd97b6619bbf351c17eb3dba',scope:'Source-extracted native pathfinder/player/collision methods with renderer/body adapters; not live game',cases:rows.length,rows},null,2));console.log(rows.length+' native route cases passed; zero sampled body collisions');})().catch(e=>{console.error(e);process.exitCode=1});
