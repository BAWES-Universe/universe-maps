/* Offline CPU evidence only: real Phaser 3.86 tile-layer Canvas routine with @napi-rs/canvas.
 * This is NOT Chromium, WebGL, a full WorkAdventure scene, GPU timing, or browser CSS verification. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.join(__dirname,'repo');const req=p=>require(path.join(root,'node_modules',p));
const {createCanvas,loadImage}=req('@napi-rs/canvas'),ts=req('typescript');
const renderTileLayer=req('phaser/src/tilemaps/TilemapLayerCanvasRenderer');
const Transform=req('phaser/src/gameobjects/components/TransformMatrix');
const Module=require('module'),h=new Module('hdpi');h._compile(ts.transpileModule(fs.readFileSync(path.join(root,'play/src/front/Phaser/Services/HdpiManager.ts'),'utf8'),{compilerOptions:{module:1}}).outputText,'hdpi');
const {HdpiManager}=h.exports;
const evidence=path.join(__dirname,'evidence');fs.mkdirSync(evidence,{recursive:true});
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const summary={warning:'OFFLINE CPU reconstruction; not browser or app acceptance',sourceCommit:'adc13cffd4e57aca6bc0353ad108bba423c61de1',phaser:'3.86.0',sourceAssets:{},cases:[]};
(async()=>{
const woka=await loadImage(path.join(__dirname,'fixture/assets/woka.png'));
for(const mapName of ['studio','reading','pixel-control']){
 const folder=path.join(__dirname,'fixture/assets',mapName),json=JSON.parse(fs.readFileSync(path.join(folder,'map.tmj'))),images={};
 summary.sourceAssets[mapName]={};for(const t of json.tilesets){if(!images[t.image]){const b=fs.readFileSync(path.join(folder,t.image));images[t.image]=await loadImage(b);summary.sourceAssets[mapName][t.image]=digest(b);}}
 const gidMap={};for(const t of json.tilesets)for(let i=0;i<t.tilecount;i++){gidMap[t.firstgid+i]={tileWidth:t.tilewidth,tileHeight:t.tileheight,tileOffset:{x:0,y:0},image:{getSourceImage:()=>images[t.image]},getTileTextureCoordinates:index=>({x:t.margin+((index-t.firstgid)%t.columns)*(t.tilewidth+t.spacing),y:t.margin+Math.floor((index-t.firstgid)/t.columns)*(t.tileheight+t.spacing)})};}
 for(const dpr of [1,2])for(const z of [.5,.75,1,1.25,1.5,2]){
  const manager=new HdpiManager(640*480,196*196);manager.maxZoomOut=0;manager.zoomModifier=z;
  const size=manager.getOptimalGameSize({width:1180*dpr,height:757*dpr});
  const css={width:Math.ceil(size.real.width/dpr),height:Math.ceil(size.real.height/dpr)};
  const inCanvas=size.game.width<=size.real.width&&size.game.height<=size.real.height;
  const base=inCanvas?size.game:size.real;
  const baseZoom=inCanvas?1:manager.zoomModifier*manager.getOptimalZoomLevel(size.real.width*size.real.height);
  const center={x:json.width*16+.25,y:json.height*16+.25};
  function draw(mode){
   const native=mode==='native',source=mode==='source';const width=source?json.width*32:Math.max(1,native?Math.ceil(size.real.width):Math.floor(base.width));const height=source?json.height*32:Math.max(1,native?Math.ceil(size.real.height):Math.floor(base.height));
   const cameraZoom=source?{x:1,y:1}:{x:baseZoom*width/base.width,y:baseZoom*height/base.height};
   const worldWidth=width/cameraZoom.x,worldHeight=height/cameraZoom.y;
   const canvas=createCanvas(width,height),ctx=canvas.getContext('2d');ctx.fillStyle='#252830';ctx.fillRect(0,0,width,height);ctx.save();ctx.scale(cameraZoom.x,cameraZoom.y);
   const camera={matrix:new Transform(),alpha:1,scrollX:source?0:center.x-worldWidth/2,scrollY:source?0:center.y-worldHeight/2};
   function layer(l){if(l.type!=='tilelayer'||l.visible===false)return;const tiles=l.data.map((index,i)=>({index:index&0x1fffffff,pixelX:i%json.width*32,pixelY:Math.floor(i/json.width)*32,rotation:0,flipX:!!(index&0x80000000),flipY:!!(index&0x40000000),alpha:1})).filter(t=>t.index>0);
    renderTileLayer({currentContext:ctx,antialias:false},{cull:()=>tiles,alpha:l.opacity??1,x:l.x||0,y:l.y||0,rotation:0,scaleX:1,scaleY:1,scrollFactorX:1,scrollFactorY:1,gidMap},camera);
   }
   for(const l of json.layers)if(l.name!=='foreground')layer(l);
   ctx.imageSmoothingEnabled=false;if(!source)ctx.drawImage(woka,32,0,32,32,center.x-camera.scrollX-16,center.y-camera.scrollY-16,32,32);
   for(const l of json.layers)if(l.name==='foreground')layer(l);ctx.restore();
   const display=createCanvas(css.width,css.height),out=display.getContext('2d');out.imageSmoothingEnabled=false;out.drawImage(canvas,0,0,css.width,css.height);
   return {canvas,display,width,height,cameraZoom};
  }
  const before=draw('baseline'),filter=draw('filter-only'),after=draw('native');if(dpr===1&&z===1)fs.writeFileSync(path.join(evidence,`${mapName}-source-map.png`),draw('source').canvas.toBuffer('image/png'));
  const b=before.display.getContext('2d').getImageData(0,0,css.width,css.height).data,a=after.display.getContext('2d').getImageData(0,0,css.width,css.height).data,f=filter.display.getContext('2d').getImageData(0,0,css.width,css.height).data;
  let changed=0,filterChanged=0;for(let i=0;i<a.length;i+=4){if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3])changed++;if(f[i]!==b[i]||f[i+1]!==b[i+1]||f[i+2]!==b[i+2]||f[i+3]!==b[i+3])filterChanged++;}
  summary.cases.push({mapName,dprSimulated:dpr,zoomModifier:z,css,baselineBitmap:{width:before.width,height:before.height},candidateBitmap:{width:after.width,height:after.height},framebufferPixelAreaRatio:after.width*after.height/(before.width*before.height),baselineCamera:before.cameraZoom,candidateCamera:after.cameraZoom,displayPixelsChanged:changed,displayChangedFraction:changed/(css.width*css.height),filterOnlyPixelsChanged:filterChanged,worldWidthPreserved:Math.abs(before.width/before.cameraZoom.x-after.width/after.cameraZoom.x)<1e-9,worldHeightPreserved:Math.abs(before.height/before.cameraZoom.y-after.height/after.cameraZoom.y)<1e-9});
  if(dpr===1&&[.5,1,1.5].includes(z)){
   const prefix=`${mapName}-z${z}`;fs.writeFileSync(path.join(evidence,`${prefix}-before.png`),before.display.toBuffer('image/png'));fs.writeFileSync(path.join(evidence,`${prefix}-candidate.png`),after.display.toBuffer('image/png'));
   const sheet=createCanvas(css.width*2,css.height+88),s=sheet.getContext('2d');s.fillStyle='#15191d';s.fillRect(0,0,sheet.width,sheet.height);s.fillStyle='#fff';s.font='bold 22px sans-serif';s.fillText(`${mapName}: OFFLINE CPU, zoom modifier ${z}, simulated DPR ${dpr}`,20,28);s.font='17px sans-serif';s.fillText(`Before: ${before.width}x${before.height} bitmap, nearest enlarged`,20,62);s.fillText(`Candidate: ${after.width}x${after.height} bitmap, nearest, no new artwork`,css.width+20,62);s.drawImage(before.display,0,88);s.drawImage(after.display,css.width,88);fs.writeFileSync(path.join(evidence,`${prefix}-comparison.png`),sheet.toBuffer('image/png'));
  }
 }
}
summary.caveats=['CSS output stage is native-canvas nearest reconstruction, not Chromium pixelated compositor.','DPR is simulated geometry only; not real mobile/high-DPI browser coverage.','All tiles drawn; browser culling, WebGL sampling, physics, controls, camera lifecycle and full-game performance are not validated.','Different pixels are not proof of better quality; native framebuffer preserves sample phase during movement but creates no source detail.','Filter-only reconstruction uses same Canvas tile routine: source-scaleMode is ignored under antialias:false.'];
fs.writeFileSync(path.join(evidence,'OFFLINE-RESULTS.json'),JSON.stringify(summary,null,2));console.log(JSON.stringify({cases:summary.cases.length,filterOnlyChanged:summary.cases.reduce((s,c)=>s+c.filterOnlyPixelsChanged,0),nativeChanged:summary.cases.reduce((s,c)=>s+c.displayPixelsChanged,0)}));
})();
