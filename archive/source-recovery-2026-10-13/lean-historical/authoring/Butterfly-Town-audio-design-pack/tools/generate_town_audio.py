#!/usr/bin/env python3
"""Original procedural score and ambience. No samples, paid services or borrowed music.
Run from any directory; outputs deterministic PCM masters + production Vorbis/MP3.
Dependencies: numpy, scipy, ffmpeg. All synthesis parameter choices are authored here.
"""
from pathlib import Path
import json, hashlib, subprocess
import numpy as np
from scipy import signal
from scipy.io import wavfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'map/assets/audio'; MASTERS=ROOT/'art-source/audio'; EVIDENCE=ROOT/'evidence/audio'
for d in (OUT,MASTERS,EVIDENCE):d.mkdir(parents=True,exist_ok=True)
SR=24000; DURATION=48.; N=int(SR*DURATION)
rng=np.random.default_rng(8914)
def midi(m):return 440*2**((m-69)/12)
def stereo(v,pan=0):
    a=(pan+1)*np.pi/4
    return np.stack([v*np.cos(a),v*np.sin(a)],axis=-1)
def circular_add(dst,wave,start):
    start=int(start*SR)%len(dst); n=len(wave); i=(np.arange(n)+start)%len(dst); np.add.at(dst,i,wave)
def lowpass(x,cutoff):
    # Prime the filter from the preceding circular tail, avoiding a first-sample reset.
    k=min(len(x),SR*2)
    return signal.sosfilt(signal.butter(3,cutoff,fs=SR,output='sos'),np.concatenate([x[-k:],x]),axis=0)[k:]
def space(x,wet=.2):
    # Diffuse, cross-fed early reflections; circular processing preserves seamless loops.
    y=x.copy()
    for seconds,gain in [(.113,.35),(.197,.27),(.293,.21),(.431,.16),(.613,.10),(.839,.07)]:
        y+=np.roll(x[:,::-1],int(seconds*SR),axis=0)*wet*gain
    return y

def pad_note(note,duration,phase=0):
    t=np.arange(int(duration*SR))/SR; f=midi(note)
    env=np.sin(np.pi*np.minimum(t/duration,1))**1.7
    # Soft string-like sine partials with subtle detuning, no saw/square transients.
    v=(np.sin(2*np.pi*f*t+phase)+.32*np.sin(2*np.pi*f*1.0015*t+phase+.7)+.18*np.sin(2*np.pi*f*2*t+.4)+.05*np.sin(2*np.pi*f*3*t+1.2))
    return v*env

def pluck(note,duration=4.,vel=.1,pan=0):
    t=np.arange(int(duration*SR))/SR; f=midi(note)
    # Felt/nylon hybrid with softened 25ms onset and slow, non-metallic partial decay.
    env=(1-np.exp(-t/.025))*np.exp(-t/1.2)
    v=np.sin(2*np.pi*f*t)*env
    v+=.27*np.sin(2*np.pi*f*2*t+.4)*(1-np.exp(-t/.018))*np.exp(-t/.7)
    v+=.06*np.sin(2*np.pi*f*3*t+1)*(1-np.exp(-t/.015))*np.exp(-t/.38)
    v*=np.minimum((duration-t)/.35,1).clip(0,1)
    return stereo(v*vel,pan)

def noise_band(n,lo,hi):
    z=rng.normal(0,1,n)
    return signal.sosfilt(signal.butter(3,[lo,hi],btype='bandpass',fs=SR,output='sos'),z)

def seam(x,seconds=.65):
    # Equal linear endpoint blend. Avoids a silence gap and matches first/last slope.
    k=int(SR*seconds); a=np.linspace(0,1,k)[:,None]
    common=x[-k:]*(1-a)+x[:k]*a
    # Re-order a circular seam around an unchanged body; exact length retained.
    y=x.copy(); y[:k]=common
    # Short edge interpolation forces sample continuity only over inaudible 12ms.
    q=int(SR*.012); fix=y[-1]-y[0];y[:q]+=fix[None,:]*(.5+.5*np.cos(np.linspace(0,np.pi,q)))[:,None]
    return y

tracks={}
t=np.arange(N)/SR
# Soft spatially diffuse air, low end removed; no harsh full-band white noise.
breeze=np.stack([noise_band(N,170,1800),noise_band(N,200,2100)],axis=-1)
breeze=lowpass(breeze,1600)
breeze*=((.75+.12*np.sin(2*np.pi*t/16)+.09*np.sin(2*np.pi*t/24))[:,None])*.075
# A few long distant resonances, too quiet to compete with conversation.
for start,note,pan in [(4,79,-.6),(21,74,.7),(37,81,-.3)]:circular_add(breeze,pluck(note,6,.010,pan),start)
tracks['gate-air']=seam(space(breeze,.4))
# Suspended E-minor / C / G / D colours, voiced high and sparse.
gate=np.zeros((N,2))
chords=[[52,59,66,71],[48,55,62,64],[43,55,62,69],[50,57,64,69]]
for c,chord in enumerate(chords):
    for j,note in enumerate(chord):
        v=pad_note(note,18,phase=j*.8)*(.022 if j<2 else .018)
        circular_add(gate,stereo(v,[-.6,.5,-.2,.3][j]),c*12-3)
    for k,note in enumerate([chord[2]+12,chord[3]+12,chord[1]+12]):
        circular_add(gate,pluck(note,6,.027,[-.4,.35,.0][k]),c*12+[2.25,6.75,10.5][k])
tracks['gate-music']=space(gate,.65)
# Warm, unhurried town motif, 80 BPM, no percussive loop or triumph fanfare.
town=np.zeros((N,2)); chords2=[[43,55,59,62,69],[50,57,62,64,69],[40,55,59,64,67],[48,55,59,62,64]]
for c,chord in enumerate(chords2):
    for j,note in enumerate(chord[:4]):circular_add(town,stereo(pad_note(note,18,j*.65)*.018,[-.5,.4,-.2,.3][j]),c*12-3)
    # A human-spaced twelve-second phrase with breaths rather than continuous arpeggios.
    for k,(beat,idx,octave) in enumerate([(0,2,0),(1.5,3,0),(3,4,0),(5,3,0),(7,1,12),(8.5,2,12),(11,3,0),(13.5,2,0)]):
        circular_add(town,pluck(chord[idx]+octave,5,.045*(.87+.13*np.cos(k)),.27*np.sin(k*2)),c*12+beat*.75)
tracks['town-music']=space(town,.65)
# Indoor score keeps the same harmonic pulse with felt low-pass and a gentler level.
tracks['interior-music']=lowpass(tracks['town-music'],900)*.76
# Water texture: overlapping bubbling sinusoids over narrow soft cascade noise.
F=int(12*SR); ft=np.arange(F)/SR
water=np.stack([noise_band(F,450,2600),noise_band(F,530,2400)],axis=-1)*.040
water*=((.86+.08*np.sin(2*np.pi*ft/4)+.05*np.sin(2*np.pi*ft/3))[:,None])
for i in range(66):
    start=float(rng.uniform(0,12));duration=float(rng.uniform(.075,.20));tt=np.arange(int(duration*SR))/SR
    f=float(rng.uniform(530,1150));phase=2*np.pi*(f*tt+f*.45*tt*tt/duration)
    env=np.sin(np.pi*tt/duration)**2*np.exp(-tt/duration*1.8)
    circular_add(water,stereo(np.sin(phase)*env*float(rng.uniform(.010,.032)),float(rng.uniform(-.5,.5))),start)
tracks['fountain']=seam(space(lowpass(water,2300),.4))
# One soft arrival gesture, no thunder or loud surprise. Starts and ends at silence.
C=int(5*SR); crossing=np.zeros((C,2))
for start,note,vel,pan in [(0,67,.055,-.2),(.24,74,.05,.2),(.58,79,.043,-.1)]:
    w=pluck(note,4.2,vel,pan); a=int(start*SR);crossing[a:min(C,a+len(w))]+=w[:max(0,min(len(w),C-a))]
crossing=space(crossing,.6);crossing[:int(.02*SR)]*=np.linspace(0,1,int(.02*SR))[:,None];crossing[-int(.5*SR):]*=np.linspace(1,0,int(.5*SR))[:,None]
tracks['gate-crossing']=crossing
# One simple native fallback with original air and music, no trigger assumptions.
tracks['town-bed']=tracks['gate-air']*.45+tracks['town-music']*.70
manifest={'schemaVersion':1,'runtimePolicy':'runtime-policy.json','runtimePlanStatus':'Quiet-world policy v2 supersedes scored-town sketch','provenance':'Original procedural synthesis from tools/generate_town_audio.py. No third-party samples, models, recordings or borrowed compositions.','sampleRate':SR,'sourceLicense':'CC0-1.0 for generated audio; generator follows repository code license.','tracks':[]}
for name,x in tracks.items():
    # Shared calibration, preserving meaningful relative loudness. Generous headroom.
    x=x*1.35
    peak=float(np.max(np.abs(x))); assert peak<.6,(name,peak)
    wav=MASTERS/(name+'.wav');wavfile.write(wav,SR,(x*32767).round().astype(np.int16))
    for ext,args in [('ogg',['-c:a','libvorbis','-q:a','4']),('mp3',['-c:a','libmp3lame','-b:a','96k'])]:
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),*args,str(OUT/(name+'.'+ext))],check=True)
    rms=float(np.sqrt(np.mean(x*x))); seam_jump=float(np.max(np.abs(x[0]-x[-1])))
    item={'runtimeUse':'localized-candidate-only' if name=='fountain' else 'optional-disabled-by-default' if name=='gate-crossing' else 'historical-sketch-not-enabled','id':name,'duration':len(x)/SR,'peakDbFS':round(20*np.log10(max(peak,1e-12)),2),'rmsDbFS':round(20*np.log10(max(rms,1e-12)),2),'seamJump':round(seam_jump,7),'loop':name!='gate-crossing','sources':[name+'.ogg',name+'.mp3'],'sha256':hashlib.sha256((OUT/(name+'.ogg')).read_bytes()).hexdigest()}
    manifest['tracks'].append(item)
    print(name,item,flush=True)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'LICENSE.txt').write_text('Original Butterfly Town audio\n\nThese sound recordings are procedural originals generated solely from mathematical synthesis by tools/generate_town_audio.py for Butterfly Town. No third-party samples or soundtrack material is used. To the extent any copyright or related rights exist in these generated assets, they are dedicated to the public domain under CC0 1.0 Universal.\nhttps://creativecommons.org/publicdomain/zero/1.0/\n')
(EVIDENCE/'asset-analysis.json').write_text(json.dumps(manifest,indent=2)+'\n')
