const fs=require('node:fs'),path=require('node:path');const{chromium}=require('/workspace/workadventure-universe/node_modules/playwright');const root=path.resolve(__dirname,'../..');
(async()=>{const b=await chromium.connectOverCDP('http://localhost:9222'),contexts=[],results=[];
function record(label,pass,details){results.push({label,pass,details});fs.writeFileSync(root+'/review/polished-district.json',JSON.stringify(results,null,2));console.log(label,pass,JSON.stringify(details));if(!pass)throw Error(label);}
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
try{
const owner=await client('Window Observer'),visitor=await client('Window Occupant');
await enter(visitor);await move(visitor,14,48);await move(owner,22,53);
await owner.screenshot({path:root+'/review/polished-outside-occupied.png'});await visitor.screenshot({path:root+'/review/polished-inside-occupied.png'});
record('current-front-seat-reached',true,await door(visitor));
record('current-spawn-outside-cover',await owner.evaluate(()=>gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='tower-glass-cover').visible),{});
record('current-seat-inside-cutaway',await visitor.evaluate(()=>!gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='tower-glass-cover').visible),{});
await move(owner,22,52);await move(owner,22,46);await owner.screenshot({path:root+'/review/polished-team-interior.png'});
await move(owner,12,41);record('lounge-seat-occupied',true,await door(owner));await owner.screenshot({path:root+'/review/polished-lounge.png'});await move(owner,12,42);record('lounge-seat-exit',true,await door(owner));
}catch(e){console.error(e);process.exitCode=1}finally{for(const c of contexts)await c.close();await b.close()}
})();
