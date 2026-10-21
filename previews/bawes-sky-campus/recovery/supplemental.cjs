const fs=require('fs'),path=require('path');const{chromium}=require('/workspace/workadventure-universe/node_modules/playwright');const root=path.resolve(__dirname),layout=require('../source/native-cafe-trial/candidate-layout.json');const results=[];let b;const contexts=[];
async function state(p){return p.evaluate(()=>({x:gs.CurrentPlayer.x,y:gs.CurrentPlayer.y,scale:gs.CurrentPlayer.scaleX,zoom:gs.cameras.main.zoom,view:{...gs.cameras.main.worldView},direction:gs.CurrentPlayer._lastDirection,cover:gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='office-cover').visible}))}
async function client(name,mobile=false){const c=await b.newContext({viewport:mobile?{width:430,height:900}:{width:1440,height:900},hasTouch:mobile});contexts.push(c);await c.addInitScript(name=>{if(window.top!==window.self)return;Object.entries({playerName:name,characterTextures:'["female1"]',requestedCameraStateKey:'false',requestedMicrophoneStateKey:'false',helpCameraSettingsShown:'1'}).forEach(([k,v])=>localStorage.setItem(k,v))},name);const p=await c.newPage();p.on('pageerror',e=>console.log('PAGE',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});p.on('requestfailed',r=>console.log('FAILED',r.url(),r.failure()));p.on('response',r=>{if(r.status()>=400)console.log('HTTP',r.status(),r.url())});await p.goto('http://localhost:8000/_/global/localhost:8090/recovery/compact/campus.tmj');
const deadline=Date.now()+180000;
while(Date.now()<deadline){
 for(const label of ['Save','Continue without webcam']){const button=p.getByText(label,{exact:true});if(await button.isVisible().catch(()=>false))await button.click().catch(()=>{});}
 const ready=await p.evaluate(async()=>{try{const{gameManager}=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');window.gs=gameManager.getCurrentGameScene();return !!gs?.CurrentPlayer&&gs.cameras.main.worldView.x>1000}catch{return false}}).catch(()=>false);
 if(ready){await p.waitForTimeout(1000);return p}await p.waitForTimeout(1000);
}throw Error('Client did not enter map: '+await p.locator('body').innerText());}
async function settle(p){await p.waitForTimeout(300);await p.waitForFunction(()=>!gs.CurrentPlayer.pathToFollow&&!gs.pendingMoveTo,{},{timeout:60000});await p.waitForTimeout(1200)}

function save(){fs.writeFileSync(root+'/evidence/supplemental-checks.json',JSON.stringify(results,null,2))}
async function move(p,x,y,name){await p.evaluate(([x,y])=>gs.moveTo({x,y},false,20),[x,y]);await settle(p);const s=await state(p);results.push({name,pass:Math.hypot(s.x-x,s.y-y)<24,...s});save();if(Math.hypot(s.x-x,s.y-y)>=24)throw Error('Unreachable '+name)}
async function clickSeat(p,x,y,name){const point=await p.evaluate(({x,y})=>{const c=gs.cameras.main,r=gs.game.canvas.getBoundingClientRect();return{x:r.x+(x-c.worldView.x)*c.zoom*r.width/gs.game.canvas.width,y:r.y+(y-c.worldView.y)*c.zoom*r.height/gs.game.canvas.height}},{x,y});await p.mouse.click(point.x,point.y,{button:'right'});await settle(p);const s=await state(p);results.push({name,pass:Math.hypot(s.x-x,s.y-y)<20,...s});save();if(Math.hypot(s.x-x,s.y-y)>=20)throw Error('Seat failed '+name)}


(async()=>{b=await chromium.connectOverCDP('http://localhost:9222');try{
const p=await client('Final mobile checks',true);
await move(p,2736,4352,'mobile cafe journey');
const performance=await p.evaluate(async()=>{const samples=[];const gl=gs.game.renderer.gl,ext=gl?.getExtension('WEBGL_debug_renderer_info');for(let i=0;i<180;i++){await new Promise(r=>requestAnimationFrame(r));samples.push(gs.game.loop.actualFps)}samples.sort((a,b)=>a-b);return{fpsMin:samples[0],fpsMedian:samples[90],fpsMax:samples[179],renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):'unknown',viewport:{width:innerWidth,height:innerHeight},devicePixelRatio,physicalPhone:false}});
results.push({name:'mobile viewport performance',pass:true,...performance});save();
// An interrupting keyboard movement must cancel the queued seat-facing adjustment.
await move(p,2568,4304,'seat interruption approach');
await p.evaluate(async()=>{await gs.moveTo({x:2568,y:4208},false,20)});await p.waitForFunction(()=>!gs.CurrentPlayer.pathToFollow&&!gs.pendingMoveTo);await p.keyboard.down('ArrowDown');await p.waitForTimeout(450);await p.keyboard.up('ArrowDown');await p.waitForTimeout(1800);const interrupted=await state(p);results.push({name:'user movement cancels seating adjustment',pass:interrupted.y>4232,...interrupted});save();
for(const target of [{x:6008,y:3696},{x:2736,y:4720},{x:3800,y:3712},{x:4016,y:2368}]){const before=await state(p);const rejected=await p.evaluate(async t=>{try{await gs.moveTo(t,false,20);return false}catch{return true}},target);const after=await state(p);results.push({name:'blocked destination '+target.x+','+target.y,pass:rejected&&Math.hypot(after.x-before.x,after.y-before.y)<2,target,before,after});save()}
await p.screenshot({path:root+'/evidence/supplemental-mobile.png'});
await p.context().close();const desktop=await client('Final occupied review');await move(desktop,2568,4208,'final counter occupancy');const dismiss=desktop.getByText('Continue without webcam',{exact:true});if(await dismiss.isVisible().catch(()=>false))await dismiss.click();await desktop.screenshot({path:root+'/evidence/final-review-counter.png'});await move(desktop,2464,3152,'final clear greenhouse landing');await desktop.screenshot({path:root+'/evidence/final-review-entrance.png'});await move(desktop,2464,3024,'final greenhouse entry');await move(desktop,2328,2896,'final greenhouse occupancy');if(await dismiss.isVisible().catch(()=>false))await dismiss.click();await desktop.screenshot({path:root+'/evidence/final-review-greenhouse.png'});


const captures=[];
for(const region of [{name:'waterfall',cx:2448,cy:4640,x:2450,y:4740,w:40,h:100},{name:'pond',cx:2448,cy:4640,x:2384,y:4544,w:32,h:32},{name:'lantern',cx:2448,cy:3024,x:2320,y:3024,w:16,h:16}]){
 await desktop.evaluate(r=>{gs.cameras.main.stopFollow();gs.cameras.main.centerOn(r.cx,r.cy)},region);await desktop.waitForTimeout(100);
 const clip=await desktop.evaluate(r=>{const c=gs.cameras.main,b=gs.game.canvas.getBoundingClientRect(),scale=c.zoom*b.width/gs.game.canvas.width;return{x:Math.round(b.x+(r.x-c.worldView.x)*scale),y:Math.round(b.y+(r.y-c.worldView.y)*scale),width:Math.round(r.w*scale),height:Math.round(r.h*scale)}},region);
 for(let i=0;i<5;i++){const phase=await desktop.evaluate(()=>gs.animatedTiles.animatedTiles[0].animatedTiles.map(a=>a.currentFrame));await desktop.screenshot({path:root+'/evidence/'+region.name+'-motion-'+i+'.png',clip});captures.push({region:region.name,sample:i,phase,clip});await desktop.waitForTimeout(90)}
}
fs.writeFileSync(root+'/evidence/motion-capture-phases.json',JSON.stringify(captures,null,2));
if(results.some(r=>!r.pass))throw Error('Supplemental failure');console.log('Supplemental passed',results.length);
}catch(e){results.push({name:'supplemental exception',pass:false,error:String(e)});console.error(e);process.exitCode=1}finally{save();for(const c of contexts)await c.close();await b?.close()}})();
