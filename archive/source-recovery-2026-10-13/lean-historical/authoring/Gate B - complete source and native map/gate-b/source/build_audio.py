#!/usr/bin/env python3
"""Rebuild only the fixed48-second audio mix. Never changes map/camera/art."""
from pathlib import Path
import subprocess,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[1]; RATE=24000

def decode(p):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar',str(RATE),'-ac','2','pipe:1']),dtype='<f4').reshape(-1,2).astype(np.float64)
def soften(x):
 y=x.copy();n=int(RATE*.008);r=(.5-.5*np.cos(np.linspace(0,np.pi,n)))[:,None];y[:n]*=r;y[-n:]*=r[::-1];return y
music=ROOT/'originals/gate-music.mp3';cascade=ROOT/'originals/cascade-soft.mp3'
assert hashlib.sha256(music.read_bytes()).hexdigest()=='3f859b065fecd1f09c306db77051efdcba4477cb6f8e49481c225c60c42c76ea'
assert hashlib.sha256(cascade.read_bytes()).hexdigest()=='40a838261cd33bbb1d1f4ad8c271ca821ffc76c7923d8bf6a2cea4198a815ff8'
m,c=decode(music),decode(cascade);assert len(m)==RATE*48 and len(c)==RATE*16
mix=.5*soften(m)+.2*np.tile(soften(c),(3,1))
out=ROOT/'gate/map/native-audio/assets/gate-music-waterfalls-loop.mp3'
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(RATE),'-ac','2','-i','pipe:0','-map_metadata','-1','-c:a','libmp3lame','-b:a','96k','-write_xing','1',str(out)],input=mix.astype('<f4').tobytes(),check=True)
assert hashlib.sha256(out.read_bytes()).hexdigest()=='449b6c5d32a9a9589d8297676001a19cf92ab86162758a6bdfc8430bdc2207e3','Codec-version change: remeasure before accepting different bytes.'
print('Mix reproduced exactly.')
