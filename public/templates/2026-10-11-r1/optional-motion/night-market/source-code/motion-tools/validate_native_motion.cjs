/* Actual pinned native plugin, parser, collision and movement methods; no engine edits. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const ROOT=path.resolve(process.argv[2]),read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const meta=read(ROOT+'/source/motion-layout.json'),slug=meta.slug,m=read(ROOT+'/map32/'+slug+'.tmj'),staticMap=read(ROOT+'/source/static-map.tmj'),layout=read(ROOT+'/source/layout.json'),wam=read(ROOT+'/map32/'+slug+'.wam'),g=layout.grid;
const layer=m.layers.find(l=>l.name===meta.layerName),ts=m.tilesets.at(-1);assert(layer&&ts.name==='ambient-native-r01');assert(m.layers.indexOf(layer)<m.layers.findIndex(l=>l.name==='floorLayer'));
const restored=structuredClone(m);restored.layers=restored.layers.filter(l=>l.name!==meta.layerName);restored.tilesets.pop();restored.nextlayerid--;assert.deepEqual(restored,staticMap,'Only overlay tileset, layer and nextlayerid may change');
const originalFiles=Object.entries(meta.originalSHA256).filter(([p])=>p.startsWith('map32/')&&!p.endsWith('.tmj'));
for(const[p,h]of originalFiles)assert.equal(sha(ROOT+'/'+p),h,'Original runtime asset bytes changed: '+p);
const hashes=Object.fromEntries(fs.readdirSync(ROOT+'/map32').map(p=>[p,sha(ROOT+'/map32/'+p)]));
assert.equal(sha(ROOT+'/source/layout.json'),meta.originalSHA256['source/layout.json']);
const placementCells=meta.placements.map(p=>p.cell.join(','));const found=[];
for(let i=0;i<layer.data.length;i++)if(layer.data[i]){let x=i%m.width,y=Math.floor(i/m.width);assert.equal(g[y][x],1);found.push([x,y].join(','));}assert.deepEqual(found.sort(),[...placementCells].sort());
assert(!layer.properties&&!ts.properties);for(const t of ts.tiles){assert(!t.properties);assert.equal(t.animation.length,8);assert.equal(new Set(t.animation.map(f=>f.tileid)).size,8);}
const raw=JSON.stringify(m),wamRaw=JSON.stringify(wam),layoutRaw=JSON.stringify(layout);
const vendor=read(__dirname+'/native-vendor/MANIFEST.json');for(const f of vendor.files)assert.equal(sha(__dirname+'/native-vendor/'+f.path),f.sha256);
const pluginPath=__dirname+'/native-vendor/phaser-animated-tiles/src/plugin/main.js',b=fs.readFileSync(pluginPath),blob=crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');assert.equal(blob,'69d1046e62a6c60577d4591f3fac145f3a733f8b');
const {createNative}=require('./native-fixture/native-runtime-portable.cjs'),N=createNative(),props=new Map();
for(const s of m.tilesets)for(const t of s.tiles||[])props.set(s.firstgid+t.id,Object.fromEntries((t.properties||[]).map(p=>[p.name,p.value])));
const w=new N.NativeWrapper();w.phaserLayers=m.layers.filter(l=>l.type==='tilelayer').map((l,i)=>({visible:l.visible!==false,layerIndex:i,layer:{name:l.name,properties:l.properties||[],data:Array.from({length:m.height},(_,y)=>l.data.slice(y*m.width,(y+1)*m.width).map(gid=>({index:gid||-1,properties:props.get(gid&0x1fffffff)||{}})))},setVisible(v){this.visible=v;return this},setCollisionByProperty(){return this}}));
w.perLayerCollisionGridCache=new Map();w.gameMap={getMap:()=>m};let mapChanges=0;w.mapChangedSubject={next(){}};w.updateCollisionGrid(undefined,false);const collision=()=>JSON.parse(JSON.stringify(w.collisionGrid)).map(r=>r.map(v=>v===1?1:0));assert.deepEqual(collision(),g);w.dynamicAreas=new Map(wam.areas.map(a=>[a.id,{...a,name:a.id}]));w.enterDynamicAreaCallbacks=[];w.leaveDynamicAreaCallbacks=[];
const nativeLayer=w.phaserLayers.find(l=>l.layer.name===meta.layerName),cells=meta.placements.map(p=>nativeLayer.layer.data[p.cell[1]][p.cell[0]]),propertyRefs=w.phaserLayers.flatMap(l=>l.layer.data.flat().map(t=>[t,t.properties]));
const originalRenderLayers=w.phaserLayers.filter(l=>l!==nativeLayer).map(l=>[l,JSON.stringify(l.layer)]);
global.Phaser={Plugins:{ScenePlugin:class{constructor(scene){this.scene=scene;this.systems=scene.sys}}}};
const ParseTilesets=require('./native-vendor/phaser/src/tilemaps/parsers/tiled/ParseTilesets');
// Native ParseTilesets adds bookkeeping to its input; isolate that parser input exactly as a loader boundary.
const parsed=ParseTilesets(structuredClone(m));let events=0;
const animationScene={sys:{settings:{isBooted:true}},time:{timeScale:1},events:{emit(event){assert.equal(event,'tileanimationupdate');events++}}};const AnimatedTiles=require(pluginPath),animated=new AnimatedTiles(animationScene,{});
animated.init({tilesets:parsed.tilesets,layers:w.phaserLayers.map(l=>({tilemapLayer:{type:'TilemapLayer'},data:l.layer.data}))});
const probe=new N.NativeWrapper();probe.phaserLayers=w.phaserLayers;probe.perLayerCollisionGridCache=new Map();probe.gameMap=w.gameMap;let auditProbeEvents=0;probe.mapChangedSubject={next(){auditProbeEvents++}};
let ticks=0,collisionChecks=0;const seen=cells.map(()=>new Set()),captures=[];
function capture(){captures.push({tick:ticks,elapsedMs:ticks*1000/60,gids:cells.map(t=>t.index)});}capture();
function invariants(){assert.equal(JSON.stringify(m),raw,'Plugin wrote raw map');assert.equal(JSON.stringify(wam),wamRaw);assert.equal(JSON.stringify(layout),layoutRaw);propertyRefs.forEach(([t,p])=>assert.equal(t.properties,p));for(const[l,s]of originalRenderLayers)assert.equal(JSON.stringify(l.layer),s,'Plugin altered original rendered tile layer');probe.perLayerCollisionGridCache.clear();probe.updateCollisionGrid(undefined,false);assert.deepEqual(JSON.parse(JSON.stringify(probe.collisionGrid)).map(r=>r.map(v=>v===1?1:0)),g);assert.deepEqual(collision(),g);collisionChecks++;}
function tick(){animated.postUpdate(ticks*1000/60,1000/60);ticks++;cells.forEach((t,i)=>seen[i].add(t.index));if(ticks<=240&&ticks%6===0)capture();if(ticks%600===0)invariants();}
// 60 seconds of independent frame replay, then native movement while animation continues.
for(let i=0;i<3600;i++)tick();
const mgr=new N.PathfindingManager(w.collisionGrid,{width:32,height:32}),p=new N.NativePlayer();Object.assign(p,{x:layout.start[0],y:layout.start[1],walkingSpeed:9,_lastDirection:3,currentPathSegmentDistanceFromStart:0,body:{height:16,offset:{y:8},setDirectControl(v){this.directControl=v}},getBody(){return this.body},stop(){},setDepth(){},playAnimation(){},emit(){},scene:{markDirty(){}}});
const scene=new N.NativeScene();Object.assign(scene,{CurrentPlayer:p,pathfindingManager:mgr,gameMapFrontWrapper:w,getPathfindingManager:()=>mgr,markDirty(){},userInputManager:{isControlsEnabled:true,isRightClickEnabled:true},getCameraManager:()=>({getCamera:()=>({scrollX:0,scrollY:0})})});
w.getMapChangedObservable=()=>({subscribe(cb){w.mapChangedSubject={next(grid){mapChanges++;cb(grid)}};return{unsubscribe(){}}}});scene.subscribeToGameMapChanged();const pointer=new N.NativePointer();pointer.gameScene=scene;
function body(q){const e=1e-7;for(let y=Math.floor((q.y+e)/32);y<=Math.floor((q.y+16-e)/32);y++)for(let x=Math.floor((q.x-8+e)/32);x<=Math.floor((q.x+8-e)/32);x++)if(g[y]?.[x]!==0)return[x,y];return null;}
const routes=[];let samples=0,movementFrames=0,areaChecks=0;
const inside=(a,q)=>q.x>=a.x&&q.x<=a.x+a.width&&q.y+16>=a.y&&q.y+16<=a.y+a.height;
async function route(id,start,click,input='desktop'){
 p.finishFollowingPath(true);mgr.cleanup();await N.scheduler.flush();p.x=start[0];p.y=start[1];let frames=0,collisions=0;pointer.handlePointerUpEvent({x:click[0],y:click[1],wasTouch:input==='touch',leftButtonReleased:()=>false,getDuration:()=>100},[]);await N.scheduler.flush();
 while(p.pathToFollow&&frames++<10000){const old={x:p.x,y:p.y};p.followPath(1000/60);tick();const n=Math.ceil(Math.hypot(p.x-old.x,p.y-old.y)/.5);for(let i=0;i<=n;i++){samples++;if(body({x:old.x+(p.x-old.x)*(n?i/n:1),y:old.y+(p.y-old.y)*(n?i/n:1)}))collisions++;}for(const a of wam.areas){assert.equal(w.getDynamicAreasOnPosition(p).some(q=>q.id===a.id),inside(a,p));areaChecks++;}N.scheduler.now+=1000/60;}
 await N.scheduler.flush();movementFrames+=frames;const fit=mgr.fitBodyWithinTile(...click,32,32),error=Math.hypot(p.x-fit.x,p.y-(fit.y-16));routes.push({id,start,click,input,final:[p.x,p.y],frames,collisions,endpointError:error,pass:!collisions&&error<1e-6&&!p.pathToFollow});return[p.x,p.y];
}
async function main(){
 for(const a of layout.anchors)for(const input of ['desktop','touch']){const end=await route('spawn-to-'+a.id,layout.start,[a.x,a.y+16],input);await route(a.id+'-return',end,[layout.start[0],layout.start[1]+16],input);}
 for(let y=0;y<g.length;y++)for(let x=0;x<g[y].length;x++)if(g[y][x]===0){const end=await route('floor-cell-'+x+'-'+y,layout.start,[x*32+16,y*32+16]);await route('floor-cell-return-'+x+'-'+y,end,[layout.start[0],layout.start[1]+16]);}
 invariants();assert.equal(mapChanges,0);for(const s of seen)assert.equal(s.size,8,'Plugin must reach eight distinct frames per placement');for(const[p,h]of Object.entries(hashes))assert.equal(sha(ROOT+'/map32/'+p),h,'Runtime file changed during replay');
 const failed=routes.filter(r=>!r.pass);const summary={scope:'Unmodified pinned animated-tiles plugin and Phaser Tiled parser, with source-extracted native collision, pointer, movement and area membership. Phaser scene is a test double. Native frame rendering is a separate TMJ/atlas decoder. Not a live browser or deployed room.',engineCommit:'60e7afdc3f96ef32525597cd46bd41175d61a2ef',pluginGitBlob:blob,pluginVersion:'2.0.2',phaserParserVersion:'3.86.0',placements:cells.length,observedDistinctFrames:seen.map(s=>s.size),animationTicks:ticks,renderOnlyEvents:events,collisionRecomputations:collisionChecks,auditProbeRecomputeEvents:auditProbeEvents,collisionGridUnchanged:true,originalLayerDataUnchanged:true,originalRuntimeAssetsByteExact:true,mapPropertiesUnchanged:true,rawMapUnchangedDuringReplay:true,propertyObjectIdentityUnchanged:true,wamByteExact:true,areasUnchanged:true,quietUnchanged:true,cameraUnchanged:true,noRuntimeScripts:true,overlayBelowFloorLayer:true,allOverlayCellsPermanentlyBlocked:true,mapChangeEvents:mapChanges,nativeMovement:{legs:routes.length,frames:movementFrames,samplesAtMostHalfPixel:samples,areaMembershipChecks:areaChecks,failures:failed.length,failedRows:failed},inputRuntimeSHA256:hashes,allPass:failed.length===0};
 fs.writeFileSync(ROOT+'/validation/native-motion.json',JSON.stringify(summary,null,2)+'\n');fs.writeFileSync(ROOT+'/validation/native-motion-routes.json',JSON.stringify(routes,null,2)+'\n');fs.writeFileSync(ROOT+'/validation/plugin-frame-replay.json',JSON.stringify({scope:'Actual plugin-selected global tile IDs, sampled every100ms at60Hz; no emulated frame selection',placements:meta.placements,captures},null,2)+'\n');console.log(JSON.stringify(summary,null,2));assert.equal(failed.length,0);
}
main().catch(e=>{console.error(e);process.exitCode=1});
