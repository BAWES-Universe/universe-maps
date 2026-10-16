const fs=require('node:fs'),path=require('node:path');
const {chromium}=require(path.join(process.env.BAWES_ENGINE_ROOT||'/workspace/workadventure-universe','node_modules/playwright'));
const root=path.resolve(__dirname,'../..');
(async()=>{
const browser=await chromium.connectOverCDP('http://localhost:9222');
try {
const p=browser.contexts()[0].pages()[0];await p.setViewportSize({width:1440,height:900});await p.reload();await p.waitForTimeout(7000);
await p.getByText('Continue without webcam',{exact:true}).click({timeout:1000}).catch(()=>{});
await p.evaluate(async()=>{const {gameManager}=await import('http://localhost:8080/src/front/Phaser/Game/GameManager.ts');window.gs=gameManager.getCurrentGameScene()});
const results=[];
for(const [label,tx,ty,cover] of [['square',22,30,true],['front-interior',22,24,false],['crown-interior',22,9,false],['rear-exit',22,7,true],['rear-terrace',22,3,true],['west-behind',7,3,true],['west-side',7,20,true],['front-return',22,30,true],['east-side',37,20,true],['east-behind',37,3,true],['rear-entry',22,9,false],['upper-work',13,12,false]]) {
const x=tx*32+16,y=ty*32+16;
await p.evaluate(({x,y})=>{gs.moveTo({x,y},false,4).catch(()=>{})},{x,y});
let arrived=false;for(let i=0;i<240;i++){arrived=await p.evaluate(({x,y})=>Math.hypot(gs.CurrentPlayer.x-x,gs.CurrentPlayer.y+16-y)<5,{x,y});if(arrived)break;await p.waitForTimeout(100)}
await p.waitForTimeout(250);
const actual=await p.evaluate(()=>({x:gs.CurrentPlayer.x,y:gs.CurrentPlayer.y,cover:gs.gameMapFrontWrapper.phaserLayers.find(l=>l.layer.name==='tower-glass-cover').visible,scale:gs.CurrentPlayer.scale,zoom:gs.cameras.main.zoom}));
const result={label,arrived,expectedCover:cover,actual,pass:arrived&&actual.cover===cover&&actual.scale===1};results.push(result);console.log(JSON.stringify(result));
if(['crown-interior','rear-terrace','upper-work'].includes(label))await p.screenshot({path:root+'/review/geometry-'+label+'.png'});
}
fs.writeFileSync(root+'/review/geometry-client.json',JSON.stringify(results,null,2)+'\n');
if(results.some(r=>!r.pass))process.exitCode=1;
} finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
