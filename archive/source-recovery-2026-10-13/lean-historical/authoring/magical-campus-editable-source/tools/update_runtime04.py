from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];audio=R/'audio'
if not audio.exists():shutil.copytree(R.parent/'universe-connected-audio',audio)
p=R/'runtime16/harness.js';s=p.read_text();s="import {createPreviewAudio} from '../audio/arrival-audio.mjs';\nconst atlasManifest=await (await fetch('../map16/asset-manifest.json')).json();\nconst audioGeometry=await (await fetch('../audio/geometry.json')).json();\nconst sound=createPreviewAudio({...audioGeometry});sound.setScene('campus');\n"+s
start=s.index("for(const name of ['base','above'])this.load.image")
end=s.index("}\nasync create()",start)
s=s[:start]+"for(const ts of atlasManifest.tilesets)this.load.image(ts.name,'../map16/'+ts.image);"+s[end:]
s=s.replace("function snapshot(){", "function memory(){const m=performance.memory;return m?{usedJSHeapSize:m.usedJSHeapSize,totalJSHeapSize:m.totalJSHeapSize,jsHeapSizeLimit:m.jsHeapSizeLimit}:null;}\nfunction snapshot(){")
s=s.replace("return {phase,player:","return {phase,memory:memory(),audio:sound.snapshot(),player:")
s=s.replace("body:JSON.stringify({name,[kind]:value})", "body:JSON.stringify({name,[kind]:kind==='report'&&name.startsWith('load-stage')?{...value,memory:memory(),time:performance.now()}:value})")
s=s.replace("const stream=game.canvas.captureStream(24),chunks=[]", "const videoStream=game.canvas.captureStream(24),audioStream=sound.getCaptureStream(),stream=new MediaStream([...videoStream.getVideoTracks(),...(audioStream?.getAudioTracks()??[])]),chunks=[]")
s=s.replace("stream.getTracks().forEach(t=>t.stop());", "videoStream.getTracks().forEach(t=>t.stop());")
s=s.replace("mimeType:'video/webm;codecs=vp9'", "mimeType:'video/webm;codecs=vp9,opus'")
s=s.replace("if(!this.player)return;const p=this.player", "if(!this.player)return;sound.setPosition({x:this.player.x,y:this.player.y});const p=this.player")
s=s.replace("show('Ready. Native campus map, all authored positions connected;16px candidate.');", "show('Ready. Revision04, native16px tile map.');await rendered();await save('load-stage16','report',{stage:'ready and rendered',snapshot:snapshot()});")
s=s.replace("game=new Phaser.Game", "document.querySelector('#sound').onclick=async()=>{try{await sound.start();sound.setScene('campus');sound.setPosition({x:scene.player.x,y:scene.player.y});show('Sound on. Nearby water and fire; work areas stay quiet.');document.querySelector('#sound').textContent='Sound ready';}catch(e){show(String(e))}};\ndocument.querySelector('#mute').onclick=()=>{sound.setMuted(!sound.snapshot().muted);document.querySelector('#mute').textContent=sound.snapshot().muted?'Unmute':'Mute';};\ngame=new Phaser.Game")
p.write_text(s)
p=R/'runtime16/index.html';s=p.read_text().replace('<button id="verify"','<button id="sound">Start sound</button><button id="mute">Mute</button><button id="verify"').replace('<script src="harness.js">','<script type="module" src="harness.js">');p.write_text(s)
