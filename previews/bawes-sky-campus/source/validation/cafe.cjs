const fs=require('fs'),path=require('path');const{chromium}=require('/workspace/workadventure-universe/node_modules/playwright');const root=path.resolve(__dirname,'../..'),layout=require('../layout.json');const results=[];let b;const contexts=[];
function record(label,pass,details){results.push({label,pass,details});fs.writeFileSync(root+'/review/'+'cafe-runtime-checks.json',JSON.stringify(results,null,2));console.log(label,pass,JSON.stringify(details));if(!pass)throw Error(label)}
async function state(p){return p.evaluate(()=>({x:gs.CurrentPlayer.x,y:gs.CurrentPlayer.y,scale:gs.CurrentPlayer.scaleX,zoom:gs.cameras.main.zoom,view:{...gs.cameras.main.worldView},cover:gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='office-cover').visible}))}
async function client(name,mobile=false){const c=await b.newContext({viewport:mobile?{width:430,height:900}:{width:1440,height:900},hasTouch:mobile});contexts.push(c);await c.addInitScript(name=>{if(window.top!==window.self)return;Object.entries({playerName:name,characterTextures:'["female1"]',requestedCameraStateKey:'false',requestedMicrophoneStateKey:'false',helpCameraSettingsShown:'1'}).forEach(([k,v])=>localStorage.setItem(k,v))},name);const p=await c.newPage();p.on('pageerror',e=>console.log('PAGE',e.message));await p.goto('http://localhost:8000/_/global/localhost:8090/campus.tmj');await p.waitForTimeout(10000);await p.getByText('Save',{exact:true}).click({timeout:2000}).catch(()=>{});await p.waitForTimeout(5000);await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});await p.evaluate(async()=>{const{gameManager}=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');window.gs=gameManager.getCurrentGameScene()});await p.waitForFunction(()=>gs?.CurrentPlayer,{timeout:90000});await p.waitForTimeout(3000);await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});await p.waitForFunction(()=>gs.cameras.main.worldView.x>1000,{},{timeout:90000});await p.waitForTimeout(1000);return p}
async function settle(p){await p.waitForTimeout(300);await p.waitForFunction(()=>!gs.CurrentPlayer.pathToFollow&&!gs.pendingMoveTo,{},{timeout:60000});await p.waitForTimeout(300)}
async function move(p,x,y,label){await p.evaluate(([x,y])=>{gs.moveTo({x,y},false,20).catch(e=>console.log('MOVE',e.message))},[x,y]);await settle(p);const s=await state(p);if(label)record(label,Math.hypot(s.x-x,s.y-y)<40,s);return s}
async function enter(p){await move(p,4016,3088);await move(p,4016,3008);await move(p,...layout.waypoints['office-center'])}
async function pointer(p,x,y,touch,label){
 await p.getByText('Continue without webcam',{exact:true}).click({timeout:500}).catch(()=>{});
 let point,s,clicks=0;
 for(;clicks<3;){
  await p.waitForTimeout(600);
  point=await p.evaluate(({x,y})=>{const c=gs.cameras.main,r=gs.game.canvas.getBoundingClientRect();return{x:r.x+(x-c.worldView.x)*c.zoom*r.width/gs.game.canvas.width,y:r.y+(y-c.worldView.y)*c.zoom*r.height/gs.game.canvas.height}},{x,y});
  touch?await p.touchscreen.tap(point.x,point.y):await p.mouse.click(point.x,point.y,{button:'right'});clicks++;await settle(p);s=await state(p);if(Math.hypot(s.x-x,s.y-y)<2)break;
 }
 record(label,Math.hypot(s.x-x,s.y-y)<20,{point,nativeClickCount:clicks,...s});
}
async function api(p){for(const f of p.frames())if(await f.evaluate(()=>!!window.WA).catch(()=>false))return f;throw Error('API frame missing')}
async function cameras(p,label){const points={north:[4024,1536],south:[5688,4576],west:[1960,3280],east:[6248,3312]};for(let i=0;i<5;i++){await p.evaluate(()=>gs.getCameraManager().zoomByFactor(.8,true));await p.waitForTimeout(650)}await p.waitForTimeout(1000);for(const[name,point]of Object.entries(points)){await p.evaluate(([x,y])=>{gs.CurrentPlayer.setPosition(x,y);gs.markDirty()},point);await p.waitForTimeout(800);const s=await state(p),v=s.view;record(label+' camera '+name,v.x>=0&&v.y>=0&&v.x+v.width<=8192&&v.y+v.height<=7168,{method:'camera-only placement, five supported zoomByFactor(.8) operations',...s});await p.screenshot({path:root+'/review/'+label+'-edge-'+name+'.png'})}}
async function visibility(p){return p.evaluate(()=>Object.fromEntries(gs.gameMapFrontWrapper.phaserLayers.filter(l=>['office-cover','office-floor','office-walls','office-furniture','office-chair-fronts','office-window-interior','campus-furniture'].includes(l.layer.name)).map(l=>[l.layer.name,l.visible])))}
async function overview(p,file,factor,cx,cy){await p.getByTestId('map-overview-button').click();await p.evaluate(f=>gs.getCameraManager().zoomByFactor(f,false),factor);await p.waitForTimeout(1000);await p.waitForTimeout(400);await p.screenshot({path:root+'/review/'+file+'.png'});results.push({label:file,details:{...(await state(p)),layers:await visibility(p)}});await p.getByTestId('map-overview-button').click();await p.evaluate(f=>gs.getCameraManager().zoomByFactor(1/f,false),factor);await p.waitForTimeout(1000)}
(async()=>{b=await chromium.connectOverCDP('http://localhost:9222');try{
const p=await client('Cafe Restoration');await move(p,...layout.waypoints['cafe'],'spawn to cafe bridge');
const facing={up:0,right:1,down:2,left:3};const captured=new Set();
for(const [i,s] of layout.seats.entries()){
 if(!['cafe-lounge','cafe-armchair','cafe-bar','outdoor-lounge'].includes(s.group))continue;
 const map=JSON.parse(fs.readFileSync(root+'/campus.tmj')),grid=map.layers.find(l=>l.name==='persistent-collision').data;
 const [dx,dy]=[[32,0],[-32,0],[0,32],[0,-32]].find(([x,y])=>!grid[Math.floor((s.y+y)/16)*map.width+Math.floor((s.x+x)/16)]);
 await p.evaluate(({x,y})=>{gs.CurrentPlayer.setPosition(x,y);gs.markDirty()},{x:s.x+dx,y:s.y+dy});await p.keyboard.down('ArrowRight');await p.waitForTimeout(120);await p.keyboard.up('ArrowRight');await p.waitForTimeout(1000);
 await pointer(p,s.x,s.y,false,'cafe actual seat '+i+' '+s.group);
 for(let j=0;j<4;j++){if(await p.evaluate(()=>gs.CurrentPlayer.lastDirection)===facing[s.facing])break;await p.keyboard.press('r');await p.waitForTimeout(150)}
 record('exact anchor '+i,Math.hypot((await state(p)).x-s.x,(await state(p)).y-s.y)<2,{seat:s,...await state(p)});
 record('facing '+i,await p.evaluate(()=>gs.CurrentPlayer.lastDirection)===facing[s.facing],{seat:s,...await state(p)});
 if(!captured.has(s.group)){captured.add(s.group);await p.screenshot({path:root+'/review/cafe-occupied-'+s.group+'.png'})}
}
await move(p,3152,4320,'portal return to cafe east');await move(p,2840,4320,'main cafe route');await move(p,2568,4352,'left lounge approach');
await p.screenshot({path:root+'/review/cafe-native-close.png'});
await p.evaluate(()=>gs.getCameraManager().zoomByFactor(.55,false));await p.waitForTimeout(1000);await move(p,2736,4352);await p.waitForTimeout(1000);await p.screenshot({path:root+'/review/cafe-full.png'});
await p.evaluate(()=>gs.getCameraManager().zoomByFactor(1/.55,false));await p.waitForTimeout(700);await move(p,4016,3600);await overview(p,'runtime-campus-cafe-restored',.10,4016,3600);
record('native avatar scale',(await state(p)).scale===1,await state(p));
}catch(e){console.error(e);for(const c of contexts)for(const p of c.pages())await p.screenshot({path:root+'/review/cafe-runtime-failure.png'}).catch(()=>{});process.exitCode=1}finally{for(const c of contexts)await c.close();await b?.close()}})();
