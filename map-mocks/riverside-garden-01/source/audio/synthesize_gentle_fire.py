"""Original gentle fireplace texture. No samples, model, APIs, or borrowed audio.
Reproduce with Python, NumPy, SciPy and FFmpeg. Fixed seed; rights-undecided-no-new-license-grant audio assets.
"""
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets';OUT.mkdir(parents=True,exist_ok=True);RATE=24000;DURATION=16;N=RATE*DURATION
rng=np.random.default_rng(202610091105);freq=np.fft.rfftfreq(N,1/RATE)
def periodic_noise(low,high):
 x=rng.standard_normal(N);s=np.fft.rfft(x)
 weight=(1-np.exp(-(freq/max(low,1))**4))*np.exp(-(freq/high)**4)
 y=np.fft.irfft(s*weight,n=N);return y/max(np.std(y),1e-9)
t=np.arange(N)/RATE
# Broad soft flame movement, with sub-bass removed. All modulators close periodically.
breath=.75+.11*np.sin(2*np.pi*t/DURATION*3)+.08*np.sin(2*np.pi*t/DURATION*7+.8)
left=periodic_noise(140,1500)*.0075*breath
right=.76*left+.24*periodic_noise(140,1500)*.0075*breath
stereo=np.column_stack([left,right])
# Tiny smouldering ticks, rounded attacks and no sharp loud wood snaps.
for _ in range(52):
 start=int(rng.integers(0,N));length=int(RATE*rng.uniform(.035,.14));tt=np.arange(length)/RATE
 noise=rng.standard_normal(length)
 f=np.fft.rfftfreq(length,1/RATE);s=np.fft.rfft(noise);s*=((1-np.exp(-(f/500)**4))*np.exp(-(f/3000)**4))
 tick=np.fft.irfft(s,n=length);tick/=max(np.std(tick),1e-9)
 env=(1-np.exp(-tt/.004))*np.exp(-tt/rng.uniform(.012,.035));env[-int(.006*RATE):]*=np.linspace(1,0,int(.006*RATE))
 tick*=env*rng.uniform(.006,.013);pan=rng.uniform(-.25,.25)
 stereo[(start+np.arange(length))%N,0]+=tick*(1-pan)
 stereo[(start+np.arange(length))%N,1]+=tick*(1+pan)
# Small round saturation smooths occasional high crests without a hard clip.
stereo=np.tanh(stereo/.06)*.06
scale=min(.011/np.sqrt(np.mean(stereo**2)),.072/np.max(np.abs(stereo)));stereo*=scale
wav=OUT/'fire-gentle-original.wav';mp3=OUT/'fire-gentle-original.mp3'
wavfile.write(wav,RATE,np.round(stereo*32767).astype(np.int16))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libmp3lame','-b:a','96k',str(mp3)],check=True)
report={'id':'fire-gentle-original','source':'tools/synthesize_gentle_fire.py','seed':202610091105,'provenance':'New original mathematical synthesis. No third-party audio, samples, paid API or copied Conference Campus material.','license':'rights-undecided-no-new-license-grant','sampleRate':RATE,'channels':2,'durationSeconds':DURATION,'peakDbFS':float(20*np.log10(np.abs(stereo).max())),'rmsDbFS':float(20*np.log10(np.sqrt(np.mean(stereo**2)))),'seamJump':float(np.max(np.abs(stereo[0]-stereo[-1]))),'p999AdjacentSampleStep':float(np.quantile(np.abs(np.diff(stereo,axis=0)),.999)),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [wav,mp3]}}
(OUT/'fire-original-provenance.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
