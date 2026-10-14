const {chromium,expect}=require('/workspace/scratch/universe-local/game/tests/safety-net/node_modules/@playwright/test');
const fs=require('fs');
const ROOT='/workspace/scratch/moonlit-r4/final';
const evidence={checks:[],clients:{}};
let browser;
async function launch(){browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--enable-unsafe-swiftshader']});return browser}
async function client(name,url,mobile=false,configure){
 const context=await browser.newContext({viewport:mobile?{width:428,height:926}:{width:1440,height:900},deviceScaleFactor:mobile?2:1,isMobile:mobile,hasTouch:mobile,permissions:['camera','microphone'],serviceWorkers:'block'});
 const log=evidence.clients[name]={url,mobileEmulation:mobile,errors:[],console:[],blocked:[],failedRequests:[]};
 await context.tracing.start({screenshots:true,snapshots:true,sources:true});
 await context.route('**/*',r=>{const u=new URL(r.request().url());if(['localhost','127.0.0.1','[::1]'].includes(u.hostname)||['data:','blob:','about:'].includes(u.protocol))return r.continue();log.blocked.push(u.href);return r.abort()});
 await context.routeWebSocket(/.*/,ws=>{const u=new URL(ws.url());if(['localhost','127.0.0.1','[::1]'].includes(u.hostname))ws.connectToServer();else{log.blocked.push(u.href);ws.close()}});
 const page=await context.newPage();page.on('pageerror',e=>{log.errors.push(e.message);(log.errorStacks??=[]).push(e.stack)});page.on('console',m=>{if(['error','warning'].includes(m.type()))log.console.push({type:m.type(),text:m.text()})});page.on('requestfailed',r=>log.failedRequests.push({url:r.url(),error:r.failure()}));
 if(configure)await configure({context,page});
 await page.goto(url);await page.getByTestId('loginSceneNameInput').fill(name,{timeout:90000});await page.getByRole('button',{name:'Continue',exact:true}).click();await page.getByRole('heading',{name:'Pick your WOKA'}).first().waitFor();await page.getByRole('button',{name:'Continue',exact:true}).click();await page.getByRole('heading',{name:'Turn on your camera and microphone'}).waitFor();await page.getByRole('button',{name:'Save',exact:true}).click();await page.getByTestId('microphone-button').waitFor({timeout:90000});await page.getByTestId('camera-button').click();await page.getByTestId('microphone-button').click();await page.waitForTimeout(500);
 const c={name,context,page,log};await screenshot(c,'arrival');return c;
}
async function frame(c){await expect.poll(()=>c.page.frames().filter(f=>f.url().includes('/local-script')||f.url()==='about:srcdoc').length).toBeGreaterThan(0);return c.page.frames().find(f=>f.url().includes('/local-script')||f.url()==='about:srcdoc')}
async function wa(c,fn,arg){return (await frame(c)).evaluate(fn,arg)}
async function position(c){return wa(c,async()=>{await WA.onInit();return WA.player.getPosition()})}
async function hold(c,key,ms){await c.page.keyboard.down(key);await c.page.waitForTimeout(ms);await c.page.keyboard.up(key);return position(c)}
async function scene(c,fn,arg){return c.page.evaluate(async({source,arg})=>{const m=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');return new Function('s','arg',`return (${source})(s,arg)`)(m.gameManager.getCurrentGameScene(),arg)},{source:fn.toString(),arg})}
async function screenshot(c,label){await c.page.screenshot({path:`${ROOT}/evidence/${c.name}-${label}.png`})}
async function check(name,fn){try{const detail=await fn();evidence.checks.push({name,status:'pass',detail});console.log('PASS '+name,JSON.stringify(detail??{}))}catch(e){evidence.checks.push({name,status:'fail',error:e.message});console.log('FAIL '+name,e.message)}fs.writeFileSync(`${ROOT}/evidence/${require("path").basename(process.argv[1],".cjs")}-results.json`,JSON.stringify(evidence,null,2))}
async function close(c){await c.context.tracing.stop({path:`${ROOT}/evidence/${c.name}-trace.zip`});await c.context.close()}
async function finish(){if(evidence.checks.some(c=>c.status!=='pass'))process.exitCode=1;fs.writeFileSync(`${ROOT}/evidence/${require("path").basename(process.argv[1],".cjs")}-results.json`,JSON.stringify(evidence,null,2));await browser.close()}
module.exports={launch,client,frame,wa,position,hold,scene,screenshot,check,close,finish,evidence,expect};
async function command(c,label){
 if(!await c.page.getByTestId('settings-window').isVisible()){
  if(!await c.page.getByTestId('profile-menu').isVisible())await c.page.getByTestId('action-user').click();
  await c.page.getByRole('button',{name:'All settings',exact:true}).click();
 }
 const button=c.page.getByRole('button',{name:label,exact:true});if(await button.isVisible())await button.click();else await c.page.getByRole('tab',{name:label,exact:true}).click();
 await c.page.getByTestId('settings-window').waitFor({state:'hidden'});
}
async function move(c,x,y){return wa(c,async p=>WA.player.moveTo(p.x,p.y,4),{x,y})}
async function teleport(c,x,y){await wa(c,p=>WA.player.teleport(p.x,p.y),{x,y});await c.page.waitForTimeout(100)}
async function snapshot(c){return scene(c,s=>{const w=s.getGameMapFrontWrapper(),p=s.CurrentPlayer,cam=s.cameras.main;return{position:{x:p.x,y:p.y},body:{left:p.body.left,right:p.body.right,top:p.body.top,bottom:p.body.bottom},camera:{x:cam.scrollX,y:cam.scrollY,zoom:cam.zoom,width:cam.width,height:cam.height,scaleZoom:s.scale.zoom,modifier:s.cameraManager.waScaleManager.zoomModifier,savedZoom:s.cameraManager.waScaleManager.getSaveZoom(),mode:s.cameraManager.cameraMode},layers:w.phaserLayers.filter(l=>/roof-alpha|door-frame|door-collision|persistent-glass|desk-lip|tea-/.test(l.layer.name)).map(l=>({name:l.layer.name,visible:l.visible,alpha:l.alpha,depth:l.depth})),doorGrid:[w.collisionGrid[13]?.[13],w.collisionGrid[13]?.[14]],playerDepth:p.depth}})}
async function recordStart(c){await scene(c,s=>{window.__moonSamples=[];window.__moonRecorder=setInterval(()=>{const p=s.CurrentPlayer,w=s.getGameMapFrontWrapper(),ls=w.phaserLayers,b=p.body,cam=s.cameras.main;const hits=[];for(let y=Math.floor((b.top+.001)/32);y<=Math.floor((b.bottom-.001)/32);y++)for(let x=Math.floor((b.left+.001)/32);x<=Math.floor((b.right-.001)/32);x++)if(w.collisionGrid[y]?.[x]===1)hits.push([x,y]);const water=ls.find(l=>l.layer.name==='water-motion');window.__moonSamples.push({t:performance.now(),x:p.x,y:p.y,roof:ls.filter(l=>l.visible&&l.layer.name.startsWith('roof-alpha')).map(l=>Number(l.layer.name.slice(-1))),door:ls.filter(l=>l.visible&&l.layer.name.startsWith('door-frame')).map(l=>Number(l.layer.name.slice(-1))),doorGrid:[w.collisionGrid[13]?.[13],w.collisionGrid[13]?.[14]],hits,water:water?.layer.data[3][28]?.index,cam:{x:cam.scrollX,y:cam.scrollY,zoom:cam.zoom,width:cam.width,height:cam.height,scaleZoom:s.scale.zoom,modifier:s.cameraManager.waScaleManager.zoomModifier,savedZoom:s.cameraManager.waScaleManager.getSaveZoom(),mode:s.cameraManager.cameraMode}})},16)})}
async function recordStop(c,label){const samples=await c.page.evaluate(()=>{clearInterval(window.__moonRecorder);return window.__moonSamples});fs.writeFileSync(`${ROOT}/evidence/${c.name}-${label}-samples.json`,JSON.stringify(samples));return samples}
Object.assign(module.exports,{command,move,teleport,snapshot,recordStart,recordStop});

// Layer visibility triggers the engine's own path replan. Preserve the original
// result and await the physical destination, without issuing another move.
async function arrive(c,x,y){const initial=await move(c,x,y);await expect.poll(async()=>{const p=await position(c);return Math.hypot(p.x-x,p.y-y)},{timeout:30000}).toBeLessThan(25);return{initial,actual:await position(c)}}
module.exports.arrive=arrive;
