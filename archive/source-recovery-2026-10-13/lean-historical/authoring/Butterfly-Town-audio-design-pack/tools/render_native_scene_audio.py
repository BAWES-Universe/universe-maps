#!/usr/bin/env python3
"""Historical musical sketch premixes. Superseded by quiet-world runtime policy; do not activate."""
from pathlib import Path
import json,hashlib,subprocess,numpy as np
from scipy.io import wavfile
R=Path(__file__).resolve().parents[1];A=R/'map/assets/audio';M=R/'art-source/audio';SR=24000
tracks={}
for name in ['gate-air','gate-music','town-music','interior-music','fountain','gate-crossing']:
 sr,x=wavfile.read(M/(name+'.wav'));assert sr==SR;tracks[name]=x.astype(float)/32768
N=48*SR
water=tracks['fountain'][np.arange(N)%len(tracks['fountain'])]
scenes={
'scene-gate':tracks['gate-air']*.46+tracks['gate-music']*.06,
'scene-approach':tracks['gate-air']*.36+tracks['gate-music']*.59,
'scene-town':tracks['gate-air']*.10+tracks['town-music']*.56,
'scene-fountain':tracks['gate-air']*.10+tracks['town-music']*.50+water*.30,
'scene-interior':tracks['interior-music']*.56,
}
arrival=scenes['scene-town'][:SR*8].copy();arrival[:len(tracks['gate-crossing'])]+=tracks['gate-crossing']*.5
# A short native scene; NEVER loop it. If gesture blocked, discard rather than replay late.
arrival[-int(.03*SR):]*=np.linspace(1,0,int(.03*SR))[:,None];scenes['scene-arrival']=arrival
manifest=json.loads((A/'manifest.json').read_text());manifest['tracks']=[t for t in manifest['tracks'] if not t['id'].startswith('scene-')]
for name,x in scenes.items():
 wav=M/(name+'.wav');wavfile.write(wav,SR,(x*32767).round().astype(np.int16))
 out=A/(name+'.mp3');subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libmp3lame','-b:a','96k',str(out)],check=True)
 peak=float(np.abs(x).max());rms=float(np.sqrt(np.mean(x*x)))
 manifest['tracks'].append({'id':name,'duration':len(x)/SR,'peakDbFS':round(20*np.log10(peak),2),'rmsDbFS':round(20*np.log10(rms),2),'loop':name!='scene-arrival','sources':[name+'.mp3'],'role':'Historical musical sketch; superseded and not enabled','runtimeUse':'historical-sketch-not-enabled','sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Rendered six native scene variants; unactivated.')
