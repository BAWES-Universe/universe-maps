#!/usr/bin/env python3
"""Original quiet cascade noise. No music, samples, models, or paid services.
Preserves the existing fountain stem. Match its measured -31.39 LUFS raw level;
position gain and native user volume provide the actual game mix.
"""
from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np
from scipy.io import wavfile
ROOT=Path(__file__).resolve().parents[1];SR=24000;SECONDS=16;N=SR*SECONDS
OUT=ROOT/'map/assets/audio';MASTER=ROOT/'art-source/audio';E=ROOT/'evidence/audio'
for p in [OUT,MASTER,E]:p.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(581302);freq=np.fft.rfftfreq(N,1/SR);time=np.arange(N)/SR
# FFT-filtered circular textures give a seamless period without a silence gap.
def band(lo,hi):
 x=rng.normal(size=N);h=1/(1+(lo/np.maximum(freq,.0001))**6)/np.sqrt(1+(freq/hi)**8)
 h[0]=0;v=np.fft.irfft(np.fft.rfft(x)*h,n=N);return v/np.sqrt(np.mean(v*v))
common=band(160,1100)*.68+band(650,2800)*.30+band(1600,4000)*.08
sides=[band(250,2700)for _ in range(2)]
# Very slow depth variations; no repetitive splashes or pitched bubble effects.
flow=.94+.035*np.sin(2*np.pi*time/8)+.025*np.sin(2*np.pi*time/16+.8)
x=np.stack([(common+.22*sides[0])*flow,(common+.22*sides[1])*flow],axis=-1)*.018
raw=MASTER/'cascade-soft-unmastered.wav';wavfile.write(raw,SR,x.astype(np.float32))
def measure(path):
 r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-af','loudnorm=I=-31.4:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1])
a=measure(raw);gain=-31.39-float(a['input_i']);master=MASTER/'cascade-soft.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-af',f'volume={gain}dB','-c:a','pcm_s16le',str(master)],check=True)
for ext,args in [('mp3',['-c:a','libmp3lame','-b:a','96k']),('ogg',['-c:a','libvorbis','-q:a','4'])]:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),*args,str(OUT/f'cascade-soft.{ext}')],check=True)
mp3=measure(OUT/'cascade-soft.mp3');assert -32.5<float(mp3['input_i'])<-30.5;assert float(mp3['input_tp'])<-15
report={'id':'cascade-soft','duration':SECONDS,'loop':True,'sources':['cascade-soft.mp3','cascade-soft.ogg'],'runtimeUse':'localized-candidate-only','provenance':'Original deterministic FFT-filtered noise synthesis; no recordings, borrowed samples, melodies or paid tools','integratedLUFS':float(mp3['input_i']),'truePeakDbTP':float(mp3['input_tp']),'loudnessRangeLU':float(mp3['input_lra']),'targetRawIntegratedLUFS':-31.39,'authoredGainNote':'At .35 authored gain, approximately9.12dB below raw, then native master volume. Ear calibration remains pending.','sha256':hashlib.sha256((OUT/'cascade-soft.mp3').read_bytes()).hexdigest()}
m=json.loads((OUT/'manifest.json').read_text());m['tracks']=[t for t in m['tracks']if t['id']!='cascade-soft']+[report];(OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(E/'cascade-calibration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
