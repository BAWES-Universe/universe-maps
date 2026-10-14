from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];G=R.parent/'universe-bounded-gate';D=R/'gate';D.mkdir(exist_ok=True)
for f in ['map','qa/gate-scene.mjs','qa/greg.png','qa/vendor/AnimatedTiles.js','INTEGRATION.md','docs/final-source-hashes.json']:
 s=G/f;d=D/f;d.parent.mkdir(parents=True,exist_ok=True)
 if s.is_dir():shutil.copytree(s,d,dirs_exist_ok=True)
 else:shutil.copy2(s,d)
p=R/'runtime16/harness.js';s=p.read_text();s=s.replace("class NativeCampusScene extends Phaser.Scene{", "class NativeCampusScene extends Phaser.Scene{\nconstructor(){super({key:'campus'});}")
s=s.replace("async create(){scene=this;", "async create(){scene=this;sound.setScene('campus');")
s=s.replace("await sound.start();sound.setScene('campus');", "await sound.start();sound.setScene(scene?.sys?.settings?.key==='bounded-gate'?'gate':'campus');")
ix=s.index("game=new Phaser.Game")
s=s[:ix]+'''const gateMode=new URLSearchParams(location.search).has('gate');let GateScene=null,gateQA=null;
async function runGateProof(){if(running)return;running=true;report=freshReport();let finish;
 try{assert('user-started gate audio ready',sound.snapshot().ready,sound.snapshot());finish=record('bounded-gate-to-campus');const result=await gateQA.journey({onCheckpoint:async(name,state)=>{await rendered();await save('gate-'+name+'-native','png',game.canvas.toDataURL('image/png'));await save('gate-'+name+'-state','report',state);}});let waited=0;while((!scene?.player||scene.sys.settings.key!=='campus')&&waited<30000){await pause(50);waited+=50;}await pause(500);await capture('gate-handoff-arrival');assert('gate actual permanent tiles clear',result.report.samples.every(s=>!s.overlap),{samples:result.report.samples.length});assert('one source navigation event',result.report.navigations.length===1,result.report.navigations);assert('campus scene native arrival',scene.sys.settings.key==='campus'&&scene.player.x===1504&&scene.player.y===2912,snapshot());assert('quiet arrival after gate cue',sound.snapshot().quiet&&sound.snapshot().gate===null,sound.snapshot());report.gate=result;report.video=await finish();finish=null;report.completed=true;await save('bounded-gate-to-campus-verification','report',report);show('PASS: original bounded gate → native campus arrival. Local scene handoff.');}
 catch(e){report.errors.push(String(e));if(finish)report.video=await finish();await save('bounded-gate-to-campus-verification','report',report);show('FAIL: '+String(e));}finally{running=false;}}
if(gateMode){const {createGateScene}=await import('../gate/qa/gate-scene.mjs');GateScene=createGateScene({Phaser,fork,audio:sound,baseUrl:'../gate/',onStatus:show,onReady:(qa,gateScene)=>{gateQA=qa;scene=gateScene;document.querySelector('#verify').disabled=false;document.querySelector('#verify').textContent='Record original gate arrival';document.querySelector('#verify').onclick=runGateProof;},onNavigate:async({scene:gateScene})=>{gateScene.scene.start('campus');}});}
''' +s[ix:]
s=s.replace("scene:NativeCampusScene});", "scene:gateMode?[GateScene,NativeCampusScene]:NativeCampusScene});")
p.write_text(s)
