const fs=require('fs'),path=require('path');const{chromium}=require('/workspace/workadventure-universe/node_modules/playwright');const root=path.resolve(__dirname),layout=require('../source/native-cafe-trial/candidate-layout.json');const results=[];let b;const contexts=[];
async function state(p){return p.evaluate(()=>({x:gs.CurrentPlayer.x,y:gs.CurrentPlayer.y,scale:gs.CurrentPlayer.scaleX,zoom:gs.cameras.main.zoom,view:{...gs.cameras.main.worldView},direction:gs.CurrentPlayer._lastDirection,cover:gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='office-cover').visible}))}
async function client(name,mobile=false){const c=await b.newContext({viewport:mobile?{width:430,height:900}:{width:1440,height:900},hasTouch:mobile});contexts.push(c);await c.addInitScript(name=>{if(window.top!==window.self)return;Object.entries({playerName:name,characterTextures:'["female1"]',requestedCameraStateKey:'false',requestedMicrophoneStateKey:'false',helpCameraSettingsShown:'1'}).forEach(([k,v])=>localStorage.setItem(k,v))},name);const p=await c.newPage();p.on('pageerror',e=>console.log('PAGE',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});p.on('requestfailed',r=>console.log('FAILED',r.url(),r.failure()));p.on('response',r=>{if(r.status()>=400)console.log('HTTP',r.status(),r.url())});await p.goto('http://localhost:8000/_/global/localhost:8090/source/native-cafe-trial/playable/campus.tmj');
const deadline=Date.now()+180000;
while(Date.now()<deadline){
 for(const label of ['Save','Continue without webcam']){const button=p.getByText(label,{exact:true});if(await button.isVisible().catch(()=>false))await button.click().catch(()=>{});}
 const ready=await p.evaluate(async()=>{try{const{gameManager}=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');window.gs=gameManager.getCurrentGameScene();return !!gs?.CurrentPlayer&&gs.cameras.main.worldView.x>1000}catch{return false}}).catch(()=>false);
 if(ready){await p.waitForTimeout(1000);return p}await p.waitForTimeout(1000);
}throw Error('Client did not enter map: '+await p.locator('body').innerText());}
async function settle(p){await p.waitForTimeout(300);await p.waitForFunction(()=>!gs.CurrentPlayer.pathToFollow&&!gs.pendingMoveTo,{},{timeout:60000});await p.waitForTimeout(1200)}

function save(){fs.writeFileSync(root+'/evidence/acceptance-checks.json',JSON.stringify(results,null,2))}
async function move(p,x,y,name){await p.evaluate(([x,y])=>gs.moveTo({x,y},false,20),[x,y]);await settle(p);const s=await state(p);results.push({name,pass:Math.hypot(s.x-x,s.y-y)<24,...s});save();if(Math.hypot(s.x-x,s.y-y)>=24)throw Error('Unreachable '+name)}
async function clickSeat(p,x,y,name){const point=await p.evaluate(({x,y})=>{const c=gs.cameras.main,r=gs.game.canvas.getBoundingClientRect();return{x:r.x+(x-c.worldView.x)*c.zoom*r.width/gs.game.canvas.width,y:r.y+(y-c.worldView.y)*c.zoom*r.height/gs.game.canvas.height}},{x,y});await p.mouse.click(point.x,point.y,{button:'right'});await settle(p);const s=await state(p);results.push({name,pass:Math.hypot(s.x-x,s.y-y)<20,...s});save();if(Math.hypot(s.x-x,s.y-y)>=20)throw Error('Seat failed '+name)}

(async()=>{b=await chromium.connectOverCDP('http://localhost:9222');try{
 const started=Date.now(),p=await client('Recovery acceptance');
 results.push({name:'client startup',pass:true,milliseconds:Date.now()-started});save();
 await move(p,4016,3088,'gate approach');await p.waitForTimeout(1000);await move(p,4016,2976,'office entry');
 for(let i=0;i<layout.seats.length;i++){
  if(i===11){await move(p,4480,2960,'meeting 1 door approach');await p.waitForTimeout(1000);await move(p,4480,2848,'meeting 1 entry');}
  if(i===15){await move(p,4480,2848,'meeting 1 exit approach');await move(p,4480,2960,'meeting 1 exit');await move(p,4880,2960,'meeting 2 door approach');await p.waitForTimeout(1000);await move(p,4880,2848,'meeting 2 entry');}
  if(i===19){await move(p,4880,2848,'meeting 2 exit approach');await move(p,4880,2960,'meeting 2 exit');await move(p,4016,2976,'office exit approach');await move(p,4016,3136,'office exit');await move(p,5768,3248,'stage aisle');}
  if(i===51)await move(p,2736,4352,'cafe arrival');
  if(i===61){await move(p,2464,3152,'greenhouse entrance');await move(p,2464,3024,'greenhouse inside');}
  if(i===63)await move(p,2464,3168,'greenhouse exit');
  const seat=layout.seats[i];
  await move(p,seat.x,seat.y,'seat '+i+' '+seat.group);
  await p.waitForTimeout(1500);
  const st=await state(p),expected={up:0,right:1,down:2,left:3}[seat.facing];
  results.push({name:'facing '+i,pass:st.direction===expected,expected,...st});save();
  if([0,11,19,23,50,51,55,57,61,62,63,69].includes(i))await p.screenshot({path:root+'/evidence/acceptance-seat-'+i+'.png'});
  console.log('Seat',i,'position',st.x,st.y,'facing',st.direction,expected);
 }
 const perf=await p.evaluate(async()=>{const samples=[];for(let i=0;i<120;i++){await new Promise(r=>requestAnimationFrame(r));samples.push(gs.game.loop.actualFps)}return{fpsMin:Math.min(...samples),fpsMedian:samples.sort((a,b)=>a-b)[60],renderer:gs.game.renderer.type,viewport:{width:innerWidth,height:innerHeight}}});results.push({name:'desktop performance',pass:true,...perf});save();
 const mobile=await client('Recovery mobile viewport',true);await move(mobile,4016,4320,'mobile square');await move(mobile,2736,4352,'mobile cafe');await mobile.screenshot({path:root+'/evidence/acceptance-mobile.png'});
 results.push({name:'mobile viewport emulation only',pass:true,viewport:{width:430,height:900},physicalPhone:false});save();
 if(results.some(r=>!r.pass))throw Error('Failed acceptance checks');
 console.log('Acceptance passed',results.length);
}catch(e){results.push({name:'acceptance exception',pass:false,error:String(e)});console.error(e);for(const c of contexts)for(const p of c.pages())await p.screenshot({path:root+'/evidence/acceptance-failure.png'}).catch(()=>{});process.exitCode=1}
finally{save();for(const c of contexts)await c.close();await b?.close()}})();
