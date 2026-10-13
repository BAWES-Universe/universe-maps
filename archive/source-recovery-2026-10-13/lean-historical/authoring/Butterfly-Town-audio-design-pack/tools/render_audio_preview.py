#!/usr/bin/env python3
"""Historical artistic sketch; superseded by the quiet-world runtime plan."""
from pathlib import Path
import json, subprocess, re, os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/butterfly-audio-matplotlib")
import numpy as np
from scipy.io import wavfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; SR=24000; D=68; N=D*SR
names=['gate-air','gate-music','town-music','interior-music','fountain']; masters={}
for name in names+['gate-crossing']:
 sr,x=wavfile.read(ROOT/'art-source/audio'/f'{name}.wav');assert sr==SR;masters[name]=x.astype(float)/32768
# Static auditable listening journey. Equivalent to intended position-directed gains.
scenes=[(0,'Outside the gate',{'gate-air':.46,'gate-music':.06}),(8,'Approaching the arch',{'gate-air':.36,'gate-music':.59}),(22,'Crossing into town',{'gate-air':.10,'town-music':.56}),(35,'Near the fountain',{'gate-air':.10,'town-music':.50,'fountain':.30}),(48,'Inside the café',{'interior-music':.56}),(59,'Back outside',{'gate-air':.10,'town-music':.56})]
gains={name:np.zeros(N)for name in names}
for i,(start,label,values) in enumerate(scenes):
 stop=scenes[i+1][0] if i+1<len(scenes) else D
 for name in names:gains[name][int(start*SR):int(stop*SR)]=values.get(name,0)
# 1.6-second smooth transitions, applied before mix; no hard scene boundaries.
for name,g in gains.items():
 for start,_,_ in scenes[1:]:
  a=int(start*SR);n=int(1.6*SR);v=g[a-1];target=g[a];t=np.linspace(0,1,n);f=t*t*(3-2*t);g[a:a+n]=v+(target-v)*f
mix=np.zeros((N,2))
for name,g in gains.items():x=masters[name];mix+=x[np.arange(N)%len(x)]*g[:,None]
c=masters['gate-crossing']*.50;mix[22*SR:22*SR+len(c)]+=c
mix[:int(SR*.18)]*=np.linspace(0,1,int(SR*.18))[:,None];mix[-2*SR:]*=np.linspace(1,0,2*SR)[:,None]
# Preview-only EBU R128 two-pass mastering. Native game stems are untouched.
# Normalize perceived loudness rather than judging a quiet track by peak alone.
# A -1 dBTP ceiling leaves codec reconstruction headroom; linear mode preserves dynamics.
out=ROOT/'audio-preview/Butterfly-Town-sound-sketch.mp3';wav=ROOT/'audio-preview/Butterfly-Town-sound-sketch.wav'
wavfile.write(wav,SR,mix.astype(np.float32))
def measure(path):
    run=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',run.stderr,re.S)[-1])
first=measure(wav)
af=f"loudnorm=I=-16:TP=-1:LRA=11:measured_I={first['input_i']}:measured_TP={first['input_tp']}:measured_LRA={first['input_lra']}:measured_thresh={first['input_thresh']}:offset={first['target_offset']}:linear=true:print_format=json"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af',af,'-ar','48000','-c:a','libmp3lame','-b:a','192k',str(out)],check=True)
measured=measure(out)
assert -16.6 <= float(measured['input_i']) <= -15.4,measured
assert float(measured['input_tp']) <= -1,measured
# Decode the actual delivery file for plotting, not an assumed gain approximation.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-ar',str(SR),'-ac','2','-f','f32le','-'])
preview=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
summary={'runtimePlan':'Historical musical sketch; superseded by quiet-world policy v2','type':'Offline sound-design sketch, not deployed game audio','durationSeconds':len(preview)/SR,'masteringRevision':2,'targetIntegratedLUFS':-16,'integratedLUFS':float(measured['input_i']),'truePeakDbTP':float(measured['input_tp']),'loudnessRangeLU':float(measured['input_lra']),'audibleFadeInSeconds':.18,'mastering':'Preview-only two-pass EBU R128 loudness normalization; native game assets unchanged','peakDbFS':round(float(20*np.log10(np.abs(preview).max())),2),'chapters':[{'second':s,'label':label}for s,label,_ in scenes],'listeningReview':'Audio-input perception is unavailable in this execution environment. Perceived loudness, true peak, waveform, spectrum and silence are measured; ear review is not claimed.'}
(ROOT/'evidence/audio/preview-mastering.json').write_text(json.dumps({'firstPass':first,'deliveryFile':measured,'summary':summary},indent=2)+'\n')
(ROOT/'audio-preview/README.json').write_text(json.dumps(summary,indent=2)+'\n')
# Readable waveform + source gains evidence.
fig,axes=plt.subplots(2,1,figsize=(12,5),sharex=True,gridspec_kw={'height_ratios':[2,1]});fig.set_facecolor('#f8f8f8')
block=240;seconds=np.arange(N//block)*block/SR;frames=preview[:N//block*block].reshape(-1,block,2);upper=frames.max(axis=(1,2));lower=frames.min(axis=(1,2))
axes[0].fill_between(seconds,lower,upper,color='#436978');axes[0].set_ylim(-1,1);axes[0].set_ylabel('Amplitude');axes[0].set_title('Butterfly Town · original procedural sound sketch')
for name,g in gains.items():axes[1].plot(seconds,g[::block][:len(seconds)],label=name)
for start,label,_ in scenes:axes[0].axvline(start,color='#b6b6b6',linewidth=.6);axes[0].text(start+.3,.80,label,rotation=35,fontsize=8)
axes[1].set_ylabel('Scene gain');axes[1].set_xlabel('Seconds');axes[1].legend(ncol=5,fontsize=7,loc='upper center');fig.tight_layout();fig.savefig(ROOT/'evidence/audio/preview-waveform.png',dpi=150)
print(json.dumps(summary,indent=2))
