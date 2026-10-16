const fs=require('node:fs'),path=require('node:path');const{chromium}=require('/workspace/workadventure-universe/node_modules/playwright');const root=path.resolve(__dirname,'../..');
(async()=>{const b=await chromium.connectOverCDP('http://localhost:9222'),contexts=[],results=[];
function record(label,pass,details){results.push({label,pass,details});fs.writeFileSync(root+'/review/consistency/checks.json',JSON.stringify(results,null,2));console.log(label,pass,JSON.stringify(details));if(!pass)throw Error(label);}
async function api(p){for(const f of p.frames())if(await f.evaluate(()=>!!window.WA).catch(()=>false))return f;throw Error('No map API frame')}
async function scene(p){await p.evaluate(async()=>{const{gameManager}=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');window.gs=gameManager.getCurrentGameScene()})}
async function client(name,mobile=false){const c=await b.newContext({viewport:mobile?{width:430,height:900}:{width:1440,height:900},hasTouch:mobile});contexts.push(c);await c.addInitScript(name=>{if(window.top!==window.self)return;Object.entries({playerName:name,characterTextures:'["female1"]',requestedCameraStateKey:'false',requestedMicrophoneStateKey:'false',helpCameraSettingsShown:'1'}).forEach(([k,v])=>localStorage.setItem(k,v))},name);const p=await c.newPage();p.on('pageerror',e=>console.log('PAGE',name,e.message));await p.goto('http://localhost:8000/_/global/localhost:8090/campus.tmj');await p.waitForTimeout(7500);await p.getByText('Save',{exact:true}).click({timeout:1000}).catch(()=>{});await p.waitForTimeout(3500);await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});await scene(p);return p;}
async function move(p,x,y){x=x*32+16;y=y*32+16;await p.evaluate(({x,y})=>{gs.moveTo({x,y},false,4).catch(()=>{})},{x,y});await p.waitForFunction(({x,y})=>Math.hypot(gs.CurrentPlayer.x-x,gs.CurrentPlayer.y+16-y)<5,{x,y},{timeout:40000});await p.waitForTimeout(250)}
async function door(p){return p.evaluate(()=>{const l=gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='meeting-door');return {visible:l.visible,collides:l.getTileAt(19,48)?.collides,x:gs.CurrentPlayer.x,y:gs.CurrentPlayer.y}})}
async function action(p,label,touch=false){
 const button=p.getByRole('button',{name:label,exact:true});
 if(!await button.isVisible()){
  const apps=p.getByTestId('apps-button');const menu=await apps.isVisible()?apps:p.getByRole('button',{name:'Open menu',exact:true});
  touch?await menu.tap():await menu.click();
 }
 await button.waitFor({timeout:5000});touch?await button.tap():await button.click();
 const f=await api(p);await f.waitForFunction(expected=>WA.state.loadVariable('bawesMeetingLocked')?.locked===expected,label.startsWith('Lock'),{timeout:7000});
}
async function enter(p){await move(p,22,52);await move(p,22,48);await move(p,21,48)}
async function pointerMove(p,tx,ty,touch,label){
 await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});
 const x=tx*32+16,y=ty*32+16;
 const point=await p.evaluate(({x,y})=>{const c=gs.cameras.main,r=gs.game.canvas.getBoundingClientRect();return{x:r.x+(x-c.worldView.x)*c.zoom*r.width/gs.game.canvas.width,y:r.y+(y-c.worldView.y)*c.zoom*r.height/gs.game.canvas.height,zoom:c.zoom,scale:gs.CurrentPlayer.scaleX}}, {x,y});
 console.log('POINTER',label,JSON.stringify(point));
 if(touch)await p.touchscreen.tap(point.x,point.y);else await p.mouse.click(point.x,point.y,{button:'right'});
 try{await p.waitForFunction(({x,y})=>Math.hypot(gs.CurrentPlayer.x-x,gs.CurrentPlayer.y+16-y)<5,{x,y},{timeout:20000})}catch(e){console.log('FAILED',await door(p));await p.screenshot({path:root+'/review/consistency/pointer-failure.png'});throw e}
 record(label,true,{...point,actual:await door(p)});
}
try{
const owner=await client('Brand Observer'),visitor=await client('Seat Review');
await enter(visitor);await pointerMove(visitor,14,48,false,'desktop-right-click-seat-approach');
await move(owner,22,53);
for(const p of [owner,visitor])await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});
await owner.screenshot({path:root+'/review/consistency/after-frontage.png'});
await visitor.screenshot({path:root+'/review/consistency/after-seat.png'});
await move(owner,22,52);await move(owner,22,46);await owner.screenshot({path:root+'/review/consistency/after-interior.png'});
await move(owner,19,39);await pointerMove(owner,13,38,false,'upper-seat-approach');await owner.screenshot({path:root+'/review/consistency/after-upper-seat.png'});await pointerMove(owner,19,39,false,'upper-seat-exit');await move(owner,22,52);await move(owner,22,60);await pointerMove(owner,13,60,false,'terrace-seat-approach');await owner.screenshot({path:root+'/review/consistency/after-terrace-seat.png'});await pointerMove(owner,18,61,false,'terrace-seat-exit');await move(owner,22,52);await move(owner,22,46);await pointerMove(visitor,18,49,false,'desktop-right-click-seat-exit');
await visitor.bringToFront();await visitor.locator('canvas').first().click({position:{x:700,y:400}});const keyboardBefore=await door(visitor);await visitor.keyboard.down('ArrowLeft');await visitor.waitForTimeout(600);await visitor.keyboard.up('ArrowLeft');const keyboardAfter=await door(visitor);record('keyboard-movement-after-exit',Math.hypot(keyboardAfter.x-keyboardBefore.x,keyboardAfter.y-keyboardBefore.y)>10,{before:keyboardBefore,after:keyboardAfter});
await contexts[1].close();contexts.splice(1,1);
const mobile=await client('Touch Seat Review',true);await enter(mobile);await move(mobile,16,49);
await pointerMove(mobile,14,48,true,'touch-seat-approach');await mobile.screenshot({path:root+'/review/consistency/after-touch.png'});
await pointerMove(mobile,16,49,true,'touch-seat-exit');
record('independent-inside-cover',await mobile.evaluate(()=>!gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='tower-glass-cover').visible),{});
}catch(e){console.error(e);process.exitCode=1}finally{for(const c of contexts)await c.close();await b.close()}
})();
